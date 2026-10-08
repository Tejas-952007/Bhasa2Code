"""Unit tests for OllamaClient with mocked HTTP transport."""

import json
import httpx
import pytest

from backend.app.llm.config import OllamaSettings
from backend.app.llm.exceptions import (
    OllamaGenerationError,
    OllamaModelNotFoundError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from backend.app.llm.ollama_client import OllamaClient


def test_health_check_success():
    """Verify health check returns ok when Ollama daemon responds."""
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/version":
            return httpx.Response(200, json={"version": "0.21.0"})
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": [{"name": "qwen2.5-coder:3b"}]})
        return httpx.Response(404)

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    status = client.health_check()
    assert status.status == "ok"
    assert status.available is True
    assert status.version == "0.21.0"
    assert status.models_count == 1
    assert client.is_available() is True


def test_health_check_connection_failure():
    """Verify health check raises OllamaUnavailableError on connection failure."""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused")

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    with pytest.raises(OllamaUnavailableError) as exc_info:
        client.health_check(raise_for_status=True)
    assert "Local AI service unavailable" in str(exc_info.value)

    # When raise_for_status is False, should return status model
    status = client.health_check(raise_for_status=False)
    assert status.available is False
    assert status.status == "unavailable"
    assert client.is_available() is False


def test_health_check_timeout():
    """Verify health check timeout handling."""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Read timed out")

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    with pytest.raises(OllamaTimeoutError):
        client.health_check(raise_for_status=True)

    status = client.health_check(raise_for_status=False)
    assert status.available is False
    assert status.status == "timeout"


def test_list_models_success():
    """Verify listing models parses model list from /api/tags."""
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/tags"
        data = {
            "models": [
                {
                    "name": "qwen2.5-coder:3b",
                    "model": "qwen2.5-coder:3b",
                    "size": 1929912626,
                    "digest": "f72c60cabf62",
                    "details": {
                        "parameter_size": "3.1B",
                        "quantization_level": "Q4_K_M",
                        "family": "qwen2",
                    },
                },
                {
                    "name": "llama3.2:latest",
                    "model": "llama3.2:latest",
                    "size": 2019393189,
                    "details": {
                        "parameter_size": "3.2B",
                        "quantization_level": "Q4_K_M",
                        "family": "llama",
                    },
                },
            ]
        }
        return httpx.Response(200, json=data)

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    models = client.list_models()
    assert len(models) == 2
    assert models[0].name == "qwen2.5-coder:3b"
    assert models[0].parameter_size == "3.1B"
    assert models[0].quantization_level == "Q4_K_M"
    assert models[0].size == 1929912626
    assert models[1].name == "llama3.2:latest"


def test_list_models_connection_failure():
    """Verify list_models raises OllamaUnavailableError on connection failure."""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Network is unreachable")

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    with pytest.raises(OllamaUnavailableError):
        client.list_models()


def test_list_models_malformed_json():
    """Verify list_models raises OllamaGenerationError on malformed response."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="not a json {")

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    with pytest.raises(OllamaGenerationError) as exc_info:
        client.list_models()
    assert "Malformed JSON" in str(exc_info.value)


def test_is_model_available():
    """Verify model presence check with exact and tag-normalized queries."""
    def handler(request: httpx.Request) -> httpx.Response:
        data = {
            "models": [
                {"name": "qwen2.5-coder:3b", "model": "qwen2.5-coder:3b"},
                {"name": "llama3.2:latest", "model": "llama3.2:latest"},
            ]
        }
        return httpx.Response(200, json=data)

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    # Exact name match
    assert client.is_model_available("qwen2.5-coder:3b") is True
    assert client.is_model_available("llama3.2:latest") is True

    # Untagged match with :latest or prefix
    assert client.is_model_available("llama3.2") is True
    assert client.is_model_available("qwen2.5-coder") is True

    # Non-existent model
    assert client.is_model_available("mistral:7b") is False


def test_generate_success():
    """Verify successful generation request and response parsing."""
    captured_payload = {}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/generate"
        nonlocal captured_payload
        captured_payload = json.loads(request.content.decode("utf-8"))
        data = {
            "model": "qwen2.5-coder:3b",
            "response": "def add(a, b):\n    return a + b\n",
            "done": True,
            "total_duration": 1500000000,  # 1.5s in ns -> 1500.0 ms
            "prompt_eval_count": 42,
            "eval_count": 18,
            "load_duration": 100000000,
        }
        return httpx.Response(200, json=data)

    settings = OllamaSettings(
        model="qwen2.5-coder:3b",
        temperature=0.2,
        num_ctx=8192,
        timeout_seconds=60.0,
    )
    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(settings=settings, http_client=mock_client)

    resp = client.generate(prompt="Write add function in Python", options={"top_p": 0.9})

    assert resp.text == "def add(a, b):\n    return a + b"
    assert resp.model == "qwen2.5-coder:3b"
    assert resp.total_duration_ms == 1500.0
    assert resp.prompt_tokens == 42
    assert resp.completion_tokens == 18
    assert resp.done is True

    # Verify payload passed
    assert captured_payload["model"] == "qwen2.5-coder:3b"
    assert captured_payload["stream"] is False
    assert captured_payload["prompt"] == "Write add function in Python"
    assert captured_payload["options"]["temperature"] == 0.2
    assert captured_payload["options"]["num_ctx"] == 8192
    assert captured_payload["options"]["top_p"] == 0.9


def test_generate_empty_prompt():
    """Verify empty prompt raises ValueError."""
    client = OllamaClient()
    with pytest.raises(ValueError) as exc_info:
        client.generate(prompt="   ")
    assert "Prompt cannot be empty" in str(exc_info.value)


def test_generate_model_not_found():
    """Verify HTTP 404 response raises OllamaModelNotFoundError."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"error": "model 'nonexistent-model' not found"})

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    with pytest.raises(OllamaModelNotFoundError) as exc_info:
        client.generate(prompt="hello", model="nonexistent-model")
    assert "nonexistent-model" in str(exc_info.value)
    assert exc_info.value.model_name == "nonexistent-model"


def test_generate_timeout():
    """Verify request timeout raises OllamaTimeoutError."""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Generation timed out")

    settings = OllamaSettings(timeout_seconds=30.0)
    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(settings=settings, http_client=mock_client)

    with pytest.raises(OllamaTimeoutError) as exc_info:
        client.generate(prompt="generate huge code")
    assert exc_info.value.timeout_seconds == 30.0
    assert "timed out" in str(exc_info.value)


def test_generate_empty_response():
    """Verify empty response text from model raises OllamaGenerationError."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"model": "qwen2.5-coder:3b", "response": "   ", "done": True})

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    with pytest.raises(OllamaGenerationError) as exc_info:
        client.generate(prompt="hello")
    assert "empty response" in str(exc_info.value)


def test_generate_server_error():
    """Verify HTTP 500 error raises OllamaGenerationError."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="Internal Server Error: Out of memory")

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    client = OllamaClient(http_client=mock_client)

    with pytest.raises(OllamaGenerationError) as exc_info:
        client.generate(prompt="hello")
    assert exc_info.value.status_code == 500
    assert "HTTP 500" in str(exc_info.value)


def test_context_manager():
    """Verify OllamaClient functions safely as context manager."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"version": "0.21.0"})

    mock_client = httpx.Client(transport=httpx.MockTransport(handler), base_url="http://127.0.0.1:11434")
    with OllamaClient(http_client=mock_client) as client:
        status = client.health_check()
        assert status.status == "ok"
