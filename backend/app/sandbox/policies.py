"""Security policies, validation invariants, and diagnostics sanitization."""

import os
import re
from typing import List

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.exceptions import (
    SandboxConfigurationError,
    SandboxSecurityViolationError,
    UnsupportedLanguageError,
)
from backend.app.sandbox.schemas import ExecutionRequest

# Explicitly supported runtime languages in T19
SUPPORTED_RUNTIME_LANGUAGES = frozenset({"python", "c", "cpp", "java", "javascript"})

# Explicitly excluded runtime targets in T19
EXCLUDED_RUNTIME_LANGUAGES = frozenset({"sql"})


class SandboxSecurityPolicy:
    """Enforces strict security rules and prevents untrusted execution breaches."""

    def __init__(self, config: SandboxConfig | None = None) -> None:
        self.config = config or SandboxConfig()
        self.config.validate_config()

    def validate_request(self, request: ExecutionRequest) -> None:
        """Validate an execution request against security constraints."""
        lang = request.language.strip().lower()
        if not lang:
            raise UnsupportedLanguageError("Language must not be empty.")

        if lang in EXCLUDED_RUNTIME_LANGUAGES:
            raise UnsupportedLanguageError(
                f"Language '{lang}' is not supported for sandbox runtime execution in T19. "
                "SQL execution against real databases is intentionally excluded."
            )

        # Basic size bounds
        if not request.code or not request.code.strip():
            raise SandboxSecurityViolationError("Code source must not be empty.")

        code_bytes = len(request.code.encode("utf-8"))
        if code_bytes > self.config.max_code_bytes:
            raise SandboxSecurityViolationError(
                f"Source code size ({code_bytes} bytes) exceeds limit ({self.config.max_code_bytes} bytes)."
            )

        if request.stdin:
            stdin_bytes = len(request.stdin.encode("utf-8"))
            if stdin_bytes > self.config.max_stdin_bytes:
                raise SandboxSecurityViolationError(
                    f"Standard input size ({stdin_bytes} bytes) exceeds limit ({self.config.max_stdin_bytes} bytes)."
                )

    def validate_security_invariants(self, docker_args: List[str]) -> None:
        """Verify that constructed Docker command preserves mandatory isolation flags."""
        args_str = " ".join(docker_args)

        if "--privileged" in docker_args:
            raise SandboxSecurityViolationError("CRITICAL: --privileged container execution is forbidden.")

        if "--network none" not in args_str and "--net=none" not in args_str:
            raise SandboxSecurityViolationError("CRITICAL: Container must execute with isolated network (--network none).")

        if "--cap-drop ALL" not in args_str and "--cap-drop=ALL" not in args_str:
            raise SandboxSecurityViolationError("CRITICAL: Linux capabilities must be dropped (--cap-drop ALL).")

        # Prohibit sensitive host volume binds
        forbidden_mount_patterns = [
            r"-v\s+/:",
            r"-v\s+\./:",
            r"-v\s+/home",
            r"-v\s+~",
            r"-v\s+/etc",
            r"-v\s+/var/run/docker\.sock",
            r"docker\.sock",
            r"\.env",
            r"\.git",
        ]
        for pattern in forbidden_mount_patterns:
            if re.search(pattern, args_str):
                raise SandboxSecurityViolationError(
                    f"CRITICAL: Forbidden host filesystem or socket mount detected: {pattern}"
                )

    @staticmethod
    def sanitize_output(text: str) -> str:
        """Sanitize host paths and sensitive strings from user-facing error/diagnostic messages."""
        if not text:
            return ""

        sanitized = text

        # Strip user home directory patterns like /home/username/
        home_dir = os.path.expanduser("~")
        if home_dir and home_dir != "/":
            sanitized = sanitized.replace(home_dir, "/sandbox_host_dir")

        # Strip generic /home/<user>/ patterns
        sanitized = re.sub(r"/home/[a-zA-Z0-9_-]+", "/sandbox_host_dir", sanitized)

        # Strip docker socket mentions if any leaked in internal errors
        sanitized = sanitized.replace("/var/run/docker.sock", "/<hidden_sock>")

        return sanitized
