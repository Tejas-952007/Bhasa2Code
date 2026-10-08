"""Unit tests for DockerRuntime with mocked container lifecycle and subprocesses."""

from unittest.mock import MagicMock, patch
import pytest

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.docker_runtime import DockerRuntime
from backend.app.sandbox.languages.base import LanguageExecutionPlan
from backend.app.sandbox.schemas import ExecutionStatus


@pytest.fixture
def dummy_plan():
    return LanguageExecutionPlan(
        language="python",
        image_tag="bhasha2code-sandbox-python:1.0.0",
        files={"main.py": "print(1)"},
        entrypoint=["python3", "-u", "main.py"],
    )


def test_is_available_when_docker_missing():
    """Verify is_available returns False when docker command fails."""
    runtime = DockerRuntime()
    with patch("subprocess.run", side_effect=FileNotFoundError):
        assert runtime.is_available() is False


def test_is_available_when_docker_succeeds():
    """Verify is_available returns True when docker info succeeds."""
    runtime = DockerRuntime()
    mock_res = MagicMock(returncode=0)
    with patch("subprocess.run", return_value=mock_res):
        assert runtime.is_available() is True


def test_execute_when_docker_unavailable(dummy_plan):
    """Verify execute returns SANDBOX_ERROR when docker is unavailable."""
    runtime = DockerRuntime()
    with patch.object(runtime, "is_available", return_value=False):
        res = runtime.execute(dummy_plan)
        assert res.status == ExecutionStatus.SANDBOX_ERROR
        assert "Docker runtime is unavailable" in res.diagnostics[0]


def test_execute_successful_mocked_run(dummy_plan):
    """Verify successful mocked container execution."""
    runtime = DockerRuntime()
    runtime._no_new_privs_supported = False

    with patch.object(runtime, "is_available", return_value=True), \
         patch("subprocess.run") as mock_run, \
         patch("subprocess.Popen") as mock_popen:

        # mock volume create, stage tar, cleanup rm
        mock_run.return_value = MagicMock(returncode=0, stdout="vol-id\n", stderr="")

        # mock container process
        mock_proc = MagicMock()
        mock_proc.stdout.read.side_effect = [b"HELLO SANDBOX\n", b""]
        mock_proc.stderr.read.side_effect = [b"", b""]
        mock_proc.poll.side_effect = [None, 0]
        mock_proc.returncode = 0
        mock_proc.stdin = MagicMock()
        mock_popen.return_value = mock_proc

        result = runtime.execute(dummy_plan)

        assert result.status == ExecutionStatus.SUCCESS
        assert result.stdout == "HELLO SANDBOX\n"
        assert result.exit_code == 0
        assert result.timed_out is False


def test_execute_runtime_error_mocked_run(dummy_plan):
    """Verify non-zero exit code translates to RUNTIME_ERROR."""
    runtime = DockerRuntime()
    runtime._no_new_privs_supported = False

    with patch.object(runtime, "is_available", return_value=True), \
         patch("subprocess.run") as mock_run, \
         patch("subprocess.Popen") as mock_popen:

        mock_run.return_value = MagicMock(returncode=0, stdout="vol-id\n", stderr="")

        mock_proc = MagicMock()
        mock_proc.stdout.read.side_effect = [b"", b""]
        mock_proc.stderr.read.side_effect = [b"ZeroDivisionError\n", b""]
        mock_proc.poll.side_effect = [None, 1]
        mock_proc.returncode = 1
        mock_proc.stdin = MagicMock()
        mock_popen.return_value = mock_proc

        result = runtime.execute(dummy_plan)

        assert result.status == ExecutionStatus.RUNTIME_ERROR
        assert result.exit_code == 1
        assert "ZeroDivisionError" in result.stderr


def test_execute_oom_killed_translates_to_resource_limit(dummy_plan):
    """Verify exit code 137 translates to RESOURCE_LIMIT."""
    runtime = DockerRuntime()
    runtime._no_new_privs_supported = False

    with patch.object(runtime, "is_available", return_value=True), \
         patch("subprocess.run") as mock_run, \
         patch("subprocess.Popen") as mock_popen:

        mock_run.return_value = MagicMock(returncode=0, stdout="vol-id\n", stderr="")

        mock_proc = MagicMock()
        mock_proc.stdout.read.side_effect = [b"", b""]
        mock_proc.stderr.read.side_effect = [b"", b""]
        mock_proc.poll.side_effect = [None, 137]
        mock_proc.returncode = 137
        mock_proc.stdin = MagicMock()
        mock_popen.return_value = mock_proc

        result = runtime.execute(dummy_plan)

        assert result.status == ExecutionStatus.RESOURCE_LIMIT
        assert result.exit_code == 137
        assert "resource constraints" in result.diagnostics[0]


def test_execute_timeout_handling(dummy_plan):
    """Verify execution exceeding wall-clock timeout yields TIMEOUT status."""
    runtime = DockerRuntime()
    runtime._no_new_privs_supported = False

    with patch.object(runtime, "is_available", return_value=True), \
         patch("subprocess.run") as mock_run, \
         patch("subprocess.Popen") as mock_popen:

        mock_run.return_value = MagicMock(returncode=0, stdout="vol-id\n", stderr="")

        mock_proc = MagicMock()
        mock_proc.stdout.read.side_effect = [b"", b""]
        mock_proc.stderr.read.side_effect = [b"", b""]
        # Never finishes before poll timeout
        mock_proc.poll.return_value = None
        mock_proc.returncode = None
        mock_proc.stdin = MagicMock()
        mock_popen.return_value = mock_proc

        result = runtime.execute(dummy_plan, timeout_seconds=0.05)

        assert result.status == ExecutionStatus.TIMEOUT
        assert result.timed_out is True
        assert result.exit_code is None
        assert "timed out" in result.diagnostics[0]


def test_execute_output_limit_breach(dummy_plan):
    """Verify output breaching output_limit_bytes returns OUTPUT_LIMIT."""
    cfg = SandboxConfig(output_limit_bytes=1024)
    runtime = DockerRuntime(config=cfg)
    runtime._no_new_privs_supported = False

    with patch.object(runtime, "is_available", return_value=True), \
         patch("subprocess.run") as mock_run, \
         patch("subprocess.Popen") as mock_popen:

        mock_run.return_value = MagicMock(returncode=0, stdout="vol-id\n", stderr="")

        mock_proc = MagicMock()
        # Generates output exceeding limit
        big_chunk = b"A" * 2048
        mock_proc.stdout.read.side_effect = [big_chunk, b""]
        mock_proc.stderr.read.side_effect = [b"", b""]
        mock_proc.poll.side_effect = [None, 0]
        mock_proc.returncode = 0
        mock_proc.stdin = MagicMock()
        mock_popen.return_value = mock_proc

        result = runtime.execute(dummy_plan)

        assert result.status == ExecutionStatus.OUTPUT_LIMIT
        assert result.output_truncated is True
        assert "Output exceeded maximum configured limit" in result.diagnostics[0]
