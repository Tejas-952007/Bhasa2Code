"""Comprehensive integration tests for Code Validate and Run API endpoints."""

from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

from backend.app.api.deps import get_sandbox_runner
from backend.app.main import app
from backend.app.sandbox.schemas import ExecutionStatus, SandboxResult


@pytest.fixture
def client():
    return TestClient(app)


def test_code_validate_valid_python(client):
    code = "def add(a, b):\n    return a + b\n"
    resp = client.post("/api/v1/code/validate", json={"language": "python", "code": code})
    assert resp.status_code == 200
    data = resp.json()
    assert data["language"] == "python"
    assert data["is_valid"] is True
    assert data["status"] == "VALID"
    assert len(data["diagnostics"]) == 0
    assert data["line_count"] == 2


def test_code_validate_invalid_python(client):
    code = "def invalid_func(\n    return 42"
    resp = client.post("/api/v1/code/validate", json={"language": "python", "code": code})
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_valid"] is False
    assert data["status"] == "INVALID"
    assert len(data["diagnostics"]) > 0


def test_code_validate_unsupported_language(client):
    code = "some arbitrary text"
    resp = client.post("/api/v1/code/validate", json={"language": "brainfuck", "code": code})
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_valid"] is False
    assert data["status"] == "UNSUPPORTED"


def test_code_run_validation_gate_rejection(client):
    """Ensure invalid code fails the validation gate before execution."""
    invalid_code = "def broken(:\n    pass"
    resp = client.post("/api/v1/code/run", json={"language": "python", "code": invalid_code})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "VALIDATION_FAILED"
    assert len(data["diagnostics"]) > 0


def test_code_run_mocked_success(client):
    """Test successful sandbox execution flow."""
    mock_runner = MagicMock()
    mock_runner.execute.return_value = SandboxResult(
        status=ExecutionStatus.SUCCESS,
        language="python",
        stdout="Hello World\n",
        stderr="",
        exit_code=0,
        duration_ms=45.2,
        diagnostics=[],
    )

    app.dependency_overrides[get_sandbox_runner] = lambda: mock_runner
    try:
        resp = client.post("/api/v1/code/run", json={"language": "python", "code": "print('Hello World')"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "SUCCESS"
        assert data["stdout"] == "Hello World\n"
        assert data["exit_code"] == 0
        assert data["duration_ms"] == 45.2
    finally:
        app.dependency_overrides.clear()


def test_code_run_timeout(client):
    """Test execution timeout handling."""
    mock_runner = MagicMock()
    mock_runner.execute.return_value = SandboxResult(
        status=ExecutionStatus.TIMEOUT,
        language="python",
        stdout="",
        stderr="Execution timed out",
        exit_code=124,
        duration_ms=5000.0,
        diagnostics=["Execution exceeded timeout limit."],
    )

    app.dependency_overrides[get_sandbox_runner] = lambda: mock_runner
    try:
        resp = client.post("/api/v1/code/run", json={"language": "python", "code": "while True: pass"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "TIMEOUT"
        assert data["exit_code"] == 124
    finally:
        app.dependency_overrides.clear()
