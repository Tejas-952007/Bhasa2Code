"""Unit tests for SandboxRunner orchestration and T18 validation gating."""

from unittest.mock import MagicMock
import pytest

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.docker_runtime import DockerRuntime
from backend.app.sandbox.sandbox_runner import SandboxRunner
from backend.app.sandbox.schemas import ExecutionRequest, ExecutionStatus, SandboxResult


@pytest.fixture
def mock_runtime():
    runtime = MagicMock(spec=DockerRuntime)
    runtime.is_available.return_value = True
    runtime.check_runtime.return_value = {"available": True}
    runtime.execute.return_value = SandboxResult(
        status=ExecutionStatus.SUCCESS,
        language="python",
        stdout="OK\n",
        exit_code=0,
    )
    return runtime


def test_t18_validation_gate_rejects_invalid_code(mock_runtime):
    """CRITICAL: Malformed code rejected by T18 must return VALIDATION_FAILED and NOT invoke Docker."""
    runner = SandboxRunner(docker_runtime=mock_runtime)

    # Invalid Python syntax (missing colon)
    bad_code = "def add(a, b)\n    return a + b"
    req = ExecutionRequest(language="python", code=bad_code)

    res = runner.execute(req)

    # Must fail at T18 gate
    assert res.status == ExecutionStatus.VALIDATION_FAILED
    assert res.language == "python"
    assert len(res.diagnostics) > 0
    # Docker must NEVER have been called
    mock_runtime.execute.assert_not_called()


def test_t18_validation_bypass_option(mock_runtime):
    """When bypass_validation is explicitly True, T18 validation is skipped."""
    runner = SandboxRunner(docker_runtime=mock_runtime)

    # Invalid Python syntax, but bypass_validation=True
    bad_code = "def add(a, b)\n    return a + b"
    req = ExecutionRequest(language="python", code=bad_code, bypass_validation=True)

    res = runner.execute(req)

    assert res.status == ExecutionStatus.SUCCESS
    mock_runtime.execute.assert_called_once()


def test_t18_validation_gate_passes_valid_code(mock_runtime):
    """Valid Python code passes T18 gate and proceeds to isolated execution."""
    runner = SandboxRunner(docker_runtime=mock_runtime)

    valid_code = "def add(a, b):\n    return a + b\nprint(add(2, 3))"
    req = ExecutionRequest(language="python", code=valid_code)

    res = runner.execute(req)

    assert res.status == ExecutionStatus.SUCCESS
    assert res.stdout == "OK\n"
    mock_runtime.execute.assert_called_once()


def test_unsupported_language_returns_unsupported(mock_runtime):
    """Unsupported languages return UNSUPPORTED and do not invoke Docker."""
    runner = SandboxRunner(docker_runtime=mock_runtime)

    req = ExecutionRequest(language="rust", code="fn main() {}")
    res = runner.execute(req)

    assert res.status == ExecutionStatus.UNSUPPORTED
    mock_runtime.execute.assert_not_called()


def test_sql_execution_rejected_as_unsupported(mock_runtime):
    """SQL is explicitly excluded from T19 execution."""
    runner = SandboxRunner(docker_runtime=mock_runtime)

    req = ExecutionRequest(language="sql", code="SELECT * FROM users;")
    res = runner.execute(req)

    assert res.status == ExecutionStatus.UNSUPPORTED
    mock_runtime.execute.assert_not_called()


def test_docker_unavailable_returns_sandbox_error():
    """When Docker runtime is unavailable, runner returns SANDBOX_ERROR."""
    mock_rt = MagicMock(spec=DockerRuntime)
    mock_rt.is_available.return_value = False

    runner = SandboxRunner(docker_runtime=mock_rt)
    req = ExecutionRequest(language="python", code="print(1)")

    res = runner.execute(req)

    assert res.status == ExecutionStatus.SANDBOX_ERROR
    assert "Docker runtime is unavailable" in res.diagnostics[0]
    mock_rt.execute.assert_not_called()


def test_empty_code_rejected_by_policy(mock_runtime):
    """Empty code input is rejected as SANDBOX_ERROR."""
    runner = SandboxRunner(docker_runtime=mock_runtime)

    req = ExecutionRequest(language="python", code="   ")
    res = runner.execute(req)

    assert res.status == ExecutionStatus.SANDBOX_ERROR
    assert "Code source must not be empty" in res.diagnostics[0]
    mock_runtime.execute.assert_not_called()


def test_convenience_execute_code_method(mock_runtime):
    """Verify execute_code helper behaves identical to execute(ExecutionRequest)."""
    runner = SandboxRunner(docker_runtime=mock_runtime)

    res = runner.execute_code(
        language="python",
        code="print('test')",
        stdin="in",
        timeout_seconds=2.0,
    )

    assert res.status == ExecutionStatus.SUCCESS
    mock_runtime.execute.assert_called_once()
