"""Integration tests for live local Ollama instance and full Bhasha2Code pipeline.

These tests execute only when RUN_OLLAMA_INTEGRATION=1 is set in the environment.
"""

import os
import time
import pytest

from backend.app.context.schemas import ContextCode, ContextMessage, ContextMetadata, ContextPackage
from backend.app.llm.config import get_ollama_settings
from backend.app.llm.llm_service import LLMService
from backend.app.llm.ollama_client import OllamaClient
from backend.app.nlp.pipeline import NLPPipeline
from backend.app.prompt.prompt_builder import PromptBuilder

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_OLLAMA_INTEGRATION") != "1",
    reason="Live Ollama integration tests run only when RUN_OLLAMA_INTEGRATION=1 is set.",
)


@pytest.fixture(scope="module")
def live_llm_service():
    """Verify live Ollama availability and return configured LLMService."""
    settings = get_ollama_settings()
    client = OllamaClient(settings=settings)
    if not client.is_available():
        pytest.skip(f"Ollama daemon unreachable at {settings.base_url}")
    if not client.is_model_available(settings.model):
        pytest.skip(
            f"Configured model '{settings.model}' is not installed locally in Ollama. "
            f"Run 'ollama pull {settings.model}'."
        )
    return LLMService(client=client, settings=settings)


@pytest.fixture(scope="module")
def nlp_pipeline():
    """Load default NLP pipeline."""
    return NLPPipeline.load_default()


@pytest.fixture(scope="module")
def prompt_builder():
    """Return PromptBuilder instance."""
    return PromptBuilder()


def test_ollama_basic_smoke(live_llm_service):
    """Smoke test: verify simple Python function generation and response metadata."""
    prompt = "Write a Python function to add two numbers."
    response = live_llm_service.generate_text(prompt, options={"num_predict": 128})

    assert response.text and len(response.text.strip()) > 0
    assert "def " in response.text or "add" in response.text
    assert response.model == live_llm_service.settings.model
    assert response.total_duration_ms is not None and response.total_duration_ms > 0
    assert response.done is True


def test_bhasha2code_full_generation_pipeline(live_llm_service, nlp_pipeline, prompt_builder):
    """End-to-End Test: 'python madhe calculator bana' through NLP -> Prompt -> LLM."""
    user_message = "python madhe calculator bana"

    # 1. NLP Pipeline (T14)
    nlp_result = nlp_pipeline.analyze(user_message)
    assert nlp_result.detected_language in ("MARATHI_ENGLISH", "HINGLISH", "MARATHI")
    assert nlp_result.detected_intent == "GENERATE_CODE"

    # 2. Prompt Builder (T16)
    prompt_spec = prompt_builder.build(
        user_message=user_message,
        nlp_result=nlp_result,
        study_mode=False,
    )
    assert "Code" in prompt_spec.response_sections

    # 3. LLM Generation (T17)
    response = live_llm_service.generate(prompt_spec, options={"num_predict": 256})

    assert response.text and len(response.text.strip()) > 0
    # Must contain Python code or calculator logic
    assert ("def " in response.text) or ("class " in response.text) or ("calc" in response.text.lower())
    assert response.prompt_tokens is not None
    assert response.completion_tokens is not None


def test_study_mode_generation(live_llm_service, nlp_pipeline, prompt_builder):
    """Study Mode Test: verifies structured learning response generation."""
    user_message = "python madhe calculator bana"

    nlp_result = nlp_pipeline.analyze(user_message)
    prompt_spec = prompt_builder.build(
        user_message=user_message,
        nlp_result=nlp_result,
        study_mode=True,
    )

    assert prompt_spec.study_mode is True
    assert "Algorithm" in prompt_spec.response_sections or "Problem Understanding" in prompt_spec.response_sections

    response = live_llm_service.generate(prompt_spec, options={"num_predict": 256})
    assert response.text and len(response.text.strip()) > 0
    # Response contains educational structure or code
    text_lower = response.text.lower()
    assert any(term in text_lower for term in ["algorithm", "step", "code", "calculator", "function", "input"])


def test_explicit_format_generation(live_llm_service, nlp_pipeline, prompt_builder):
    """Explicit Format Test: 'python madhe calculator bana algorithm ani flowchart pan de'."""
    user_message = "python madhe calculator bana algorithm ani flowchart pan de"

    nlp_result = nlp_pipeline.analyze(user_message)
    prompt_spec = prompt_builder.build(
        user_message=user_message,
        nlp_result=nlp_result,
        study_mode=False,
    )

    # Prompt builder must include Algorithm and Flowchart
    assert "Algorithm" in prompt_spec.response_sections
    assert "Flowchart" in prompt_spec.response_sections

    response = live_llm_service.generate(prompt_spec, options={"num_predict": 256})
    assert response.text and len(response.text.strip()) > 0


def test_code_only_generation(live_llm_service, nlp_pipeline, prompt_builder):
    """Code-Only Test: 'fakt code de' should strictly constrain the response."""
    user_message = "fakt code de"

    nlp_result = nlp_pipeline.analyze(user_message)
    prompt_spec = prompt_builder.build(
        user_message=user_message,
        nlp_result=nlp_result,
        study_mode=False,
    )

    assert "Code only" in prompt_spec.response_sections

    response = live_llm_service.generate(prompt_spec, options={"num_predict": 256})
    assert response.text and len(response.text.strip()) > 0


def test_multi_turn_followup_generation(live_llm_service, nlp_pipeline, prompt_builder):
    """Follow-Up Test: Turn 1 calculator -> Turn 2 'yat error handling add kar'."""
    calc_code = (
        "def calculator(a, b, op):\n"
        "    if op == '+': return a + b\n"
        "    if op == '-': return a - b\n"
        "    if op == '*': return a * b\n"
        "    if op == '/': return a / b\n"
    )

    follow_up_message = "yat error handling add kar"

    context_package = ContextPackage(
        session_id="test-session-123",
        current_message=follow_up_message,
        messages=[
            ContextMessage(message_id="msg-1", role="user", content="python madhe calculator bana"),
            ContextMessage(message_id="msg-2", role="assistant", content=f"Here is calculator:\n```python\n{calc_code}```"),
        ],
        generated_code=[
            ContextCode(
                generated_code_id="code-1",
                message_id="msg-2",
                language="python",
                code=calc_code,
            )
        ],
        current_code=calc_code,
        metadata=ContextMetadata(
            is_follow_up=True,
            language="MARATHI_ENGLISH",
            tone="CASUAL",
            intent="GENERATE_CODE",
        ),
    )

    nlp_result = nlp_pipeline.analyze(follow_up_message)

    prompt_spec = prompt_builder.build(
        user_message=follow_up_message,
        nlp_result=nlp_result,
        context_package=context_package,
        study_mode=False,
    )

    # Prompt specification must incorporate current code artifact and follow-up guidance
    assert prompt_spec.current_code is not None
    assert "calculator" in prompt_spec.current_code

    response = live_llm_service.generate(prompt_spec, options={"num_predict": 256})

    assert response.text and len(response.text.strip()) > 0
    # Must mention error handling or try/except or ZeroDivisionError or conditional check
    text_lower = response.text.lower()
    assert any(term in text_lower for term in ["try", "except", "error", "zero", "division", "handling"])


def test_performance_benchmarks(live_llm_service):
    """Benchmark local generation for 5 simple prompts and record latency statistics."""
    prompts = [
        "Write a Python function to check if a number is prime.",
        "Write a Python function to reverse a string.",
        "Write a Python function to find the maximum in a list.",
        "Write a Python function to calculate factorial of a number.",
        "Write a Python function to check if a string is palindrome.",
    ]

    durations: list[float] = []

    for prompt in prompts:
        start_time = time.time()
        resp = live_llm_service.generate_text(prompt, options={"num_predict": 128})
        elapsed_s = time.time() - start_time
        durations.append(resp.total_duration_ms or (elapsed_s * 1000.0))
        assert resp.text and len(resp.text.strip()) > 0

    total_duration_ms = sum(durations)
    avg_duration_ms = total_duration_ms / len(durations)
    min_duration_ms = min(durations)
    max_duration_ms = max(durations)

    print(
        f"\n[BENCHMARK RESULTS] 5 Prompts on {live_llm_service.settings.model}:\n"
        f"  Total Duration: {total_duration_ms:.1f} ms\n"
        f"  Average Duration: {avg_duration_ms:.1f} ms\n"
        f"  Min Duration: {min_duration_ms:.1f} ms\n"
        f"  Max Duration: {max_duration_ms:.1f} ms\n"
    )

    assert avg_duration_ms > 0
