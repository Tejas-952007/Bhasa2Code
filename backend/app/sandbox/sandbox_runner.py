"""High-level SandboxRunner orchestrating T18 validation, security policies, and Docker runtime."""

import logging
from typing import Any, Dict, Optional

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.docker_runtime import DockerRuntime
from backend.app.sandbox.exceptions import (
    SandboxSecurityViolationError,
    UnsupportedLanguageError,
)
from backend.app.sandbox.languages import (
    get_language_runner,
    normalize_sandbox_language,
)
from backend.app.sandbox.policies import SandboxSecurityPolicy
from backend.app.sandbox.schemas import (
    ExecutionRequest,
    ExecutionStatus,
    SandboxResult,
)
from backend.app.validation.schemas import ValidationStatus
from backend.app.validation.validators import (
    BaseCodeValidator,
    CValidator,
    CppValidator,
    JavaValidator,
    JavaScriptValidator,
    PythonValidator,
)

logger = logging.getLogger(__name__)


class SandboxRunner:
    """Safe code execution manager gating untrusted code behind T18 validation and isolated Docker runtime."""

    def __init__(
        self,
        config: Optional[SandboxConfig] = None,
        docker_runtime: Optional[DockerRuntime] = None,
        security_policy: Optional[SandboxSecurityPolicy] = None,
    ) -> None:
        self.config = config or SandboxConfig()
        self.config.validate_config()
        self.security_policy = security_policy or SandboxSecurityPolicy(self.config)
        self.docker_runtime = docker_runtime or DockerRuntime(self.config, self.security_policy)

        # T18 static validators for supported sandbox languages
        self._validators: Dict[str, BaseCodeValidator] = {
            "python": PythonValidator(),
            "c": CValidator(),
            "cpp": CppValidator(),
            "java": JavaValidator(),
            "javascript": JavaScriptValidator(),
        }

    def is_available(self) -> bool:
        """Expose whether Docker runtime environment is healthy and operational."""
        return self.docker_runtime.is_available()

    def check_runtime(self) -> Dict[str, Any]:
        """Perform comprehensive capability and health inspection."""
        return self.docker_runtime.check_runtime()

    def execute(self, request: ExecutionRequest) -> SandboxResult:
        """Execute validated untrusted code under isolated Docker sandbox."""
        lang_raw = request.language
        canonical_lang = normalize_sandbox_language(lang_raw)

        # 1. Validate language support
        if not canonical_lang or canonical_lang not in self._validators:
            return SandboxResult(
                status=ExecutionStatus.UNSUPPORTED,
                language=lang_raw,
                diagnostics=[
                    f"Language '{lang_raw}' is not supported for execution in T19. "
                    f"Supported languages: {sorted(self._validators.keys())}."
                ],
            )

        # 2. Check security policy on request
        try:
            self.security_policy.validate_request(request)
        except (UnsupportedLanguageError, SandboxSecurityViolationError) as e:
            return SandboxResult(
                status=ExecutionStatus.SANDBOX_ERROR,
                language=canonical_lang,
                diagnostics=[str(e)],
            )

        # 3. T18 Static Validation Gate
        if not request.bypass_validation:
            validator = self._validators[canonical_lang]
            validation_res = validator.validate(request.code)

            if validation_res.status != ValidationStatus.VALID:
                diagnostics = [
                    f"[{d.severity}] {d.message}" + (f" (line {d.line})" if d.line else "")
                    for d in validation_res.diagnostics
                ]
                if not diagnostics:
                    diagnostics = [f"Code failed T18 static syntax validation for {canonical_lang}."]

                return SandboxResult(
                    status=ExecutionStatus.VALIDATION_FAILED,
                    language=canonical_lang,
                    diagnostics=diagnostics,
                )

        # 4. Check Docker availability
        if not self.docker_runtime.is_available():
            return SandboxResult(
                status=ExecutionStatus.SANDBOX_ERROR,
                language=canonical_lang,
                diagnostics=["Docker runtime is unavailable or daemon is not accessible."],
            )

        # 5. Build Language Execution Plan
        try:
            runner = get_language_runner(canonical_lang)
            plan = runner.build_plan(request.code, self.config)
        except Exception as e:
            return SandboxResult(
                status=ExecutionStatus.SANDBOX_ERROR,
                language=canonical_lang,
                diagnostics=[f"Failed to build execution plan: {str(e)}"],
            )

        # 6. Isolated Container Execution
        return self.docker_runtime.execute(
            plan=plan,
            stdin=request.stdin,
            timeout_seconds=request.timeout_seconds,
            memory_limit_mb=request.memory_limit_mb,
        )

    def execute_code(
        self,
        language: str,
        code: str,
        stdin: str = "",
        timeout_seconds: Optional[float] = None,
        memory_limit_mb: Optional[int] = None,
        bypass_validation: bool = False,
    ) -> SandboxResult:
        """Convenience method to execute code with raw parameters."""
        req = ExecutionRequest(
            language=language,
            code=code,
            stdin=stdin,
            timeout_seconds=timeout_seconds,
            memory_limit_mb=memory_limit_mb,
            bypass_validation=bypass_validation,
        )
        return self.execute(req)
