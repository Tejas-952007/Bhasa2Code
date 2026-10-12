"""Unit tests for sandbox schemas and enums."""

import pytest
from backend.app.sandbox.schemas import (
    ExecutionRequest,
    ExecutionStatus,
    SandboxResult,
)


def test_execution_status_enum_values():
    """Verify all 8 specified execution status enum values."""
    expected = {
        "SUCCESS",
        "RUNTIME_ERROR",
        "TIMEOUT",
        "RESOURCE_LIMIT",
        "VALIDATION_FAILED",
        "UNSUPPORTED",
        "SANDBOX_ERROR",
        "OUTPUT_LIMIT",
        "DEPENDENCY_ERROR",
    }
    actual = {s.value for s in ExecutionStatus}
    assert actual == expected


def test_sandbox_result_defaults():
    """Verify SandboxResult defaults and properties."""
    res = SandboxResult(
        status=ExecutionStatus.SUCCESS,
        language="python",
        stdout="hello\n",
    )
    assert res.status == ExecutionStatus.SUCCESS
    assert res.language == "python"
    assert res.stdout == "hello\n"
    assert res.stderr == ""
    assert res.exit_code is None
    assert res.duration_ms is None
    assert res.timed_out is False
    assert res.output_truncated is False
    assert res.diagnostics == []
    assert res.is_success is True


def test_sandbox_result_error_status():
    """Verify is_success property for error statuses."""
    res = SandboxResult(
        status=ExecutionStatus.RUNTIME_ERROR,
        language="python",
        stderr="ZeroDivisionError",
        exit_code=1,
    )
    assert res.is_success is False
    assert res.exit_code == 1


def test_execution_request_schema():
    """Verify ExecutionRequest fields and validation."""
    req = ExecutionRequest(
        language="python",
        code="print(1)",
        stdin="abc",
        timeout_seconds=5.0,
    )
    assert req.language == "python"
    assert req.code == "print(1)"
    assert req.stdin == "abc"
    assert req.timeout_seconds == 5.0
    assert req.bypass_validation is False
