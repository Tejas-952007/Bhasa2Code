"""Unit tests for sandbox security policies and configuration validation."""

import pytest
from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.exceptions import (
    SandboxConfigurationError,
    SandboxSecurityViolationError,
    UnsupportedLanguageError,
)
from backend.app.sandbox.policies import SandboxSecurityPolicy
from backend.app.sandbox.schemas import ExecutionRequest


def test_sandbox_config_defaults():
    """Verify default values comply with specification."""
    cfg = SandboxConfig()
    assert cfg.timeout_seconds == 3.0
    assert cfg.memory_limit_mb == 256
    assert cfg.cpu_limit == 0.5
    assert cfg.pids_limit == 64
    assert cfg.output_limit_bytes == 65536
    assert cfg.workspace_limit_mb == 64
    assert cfg.network_enabled is False
    assert cfg.run_as_non_root is True
    assert cfg.read_only_rootfs is True


def test_sandbox_config_validation_errors():
    """Verify invalid config bounds are rejected."""
    with pytest.raises(SandboxConfigurationError):
        SandboxConfig(timeout_seconds=0).validate_config()

    with pytest.raises(SandboxConfigurationError):
        SandboxConfig(memory_limit_mb=8).validate_config()

    with pytest.raises(SandboxConfigurationError):
        SandboxConfig(cpu_limit=-1).validate_config()

    with pytest.raises(SandboxConfigurationError):
        SandboxConfig(network_enabled=True).validate_config()


def test_policy_validates_request():
    """Verify policy accepts valid execution request."""
    policy = SandboxSecurityPolicy()
    req = ExecutionRequest(language="python", code="print(1)")
    policy.validate_request(req)


def test_policy_rejects_sql_execution():
    """Verify SQL runtime execution is explicitly rejected."""
    policy = SandboxSecurityPolicy()
    req = ExecutionRequest(language="sql", code="SELECT 1;")
    with pytest.raises(UnsupportedLanguageError) as exc_info:
        policy.validate_request(req)
    assert "SQL execution against real databases is intentionally excluded" in str(exc_info.value)


def test_policy_rejects_empty_code():
    """Verify empty code raises security violation."""
    policy = SandboxSecurityPolicy()
    req = ExecutionRequest(language="python", code="   ")
    with pytest.raises(SandboxSecurityViolationError):
        policy.validate_request(req)


def test_policy_rejects_oversized_code():
    """Verify oversized code is rejected."""
    cfg = SandboxConfig(max_code_bytes=100)
    policy = SandboxSecurityPolicy(config=cfg)
    req = ExecutionRequest(language="python", code="x = 1\n" * 50)
    with pytest.raises(SandboxSecurityViolationError):
        policy.validate_request(req)


def test_policy_rejects_oversized_stdin():
    """Verify oversized stdin is rejected."""
    cfg = SandboxConfig(max_stdin_bytes=10)
    policy = SandboxSecurityPolicy(config=cfg)
    req = ExecutionRequest(language="python", code="x = 1", stdin="x" * 20)
    with pytest.raises(SandboxSecurityViolationError):
        policy.validate_request(req)


def test_validate_security_invariants_privileged_rejection():
    """Verify --privileged is strictly rejected."""
    policy = SandboxSecurityPolicy()
    args = ["docker", "run", "--privileged", "--network", "none", "--cap-drop", "ALL"]
    with pytest.raises(SandboxSecurityViolationError) as exc_info:
        policy.validate_security_invariants(args)
    assert "--privileged container execution is forbidden" in str(exc_info.value)


def test_validate_security_invariants_network_none():
    """Verify missing network isolation is rejected."""
    policy = SandboxSecurityPolicy()
    args = ["docker", "run", "--cap-drop", "ALL"]
    with pytest.raises(SandboxSecurityViolationError):
        policy.validate_security_invariants(args)


def test_validate_security_invariants_forbidden_mounts():
    """Verify forbidden host mounts are blocked."""
    policy = SandboxSecurityPolicy()
    bad_mounts = [
        ["docker", "run", "--network", "none", "--cap-drop", "ALL", "-v", "/:/workspace"],
        ["docker", "run", "--network", "none", "--cap-drop", "ALL", "-v", "/home/user:/workspace"],
        ["docker", "run", "--network", "none", "--cap-drop", "ALL", "-v", "/var/run/docker.sock:/var/run/docker.sock"],
    ]
    for args in bad_mounts:
        with pytest.raises(SandboxSecurityViolationError):
            policy.validate_security_invariants(args)


def test_sanitize_output():
    """Verify sanitization of sensitive host directories."""
    text = "Error in /home/tejas/Desktop/Bhasa2code/script.py and socket /var/run/docker.sock"
    sanitized = SandboxSecurityPolicy.sanitize_output(text)
    assert "/home/tejas" not in sanitized
    assert "/var/run/docker.sock" not in sanitized
    assert "/sandbox_host_dir" in sanitized
    assert "<hidden_sock>" in sanitized
