"""Exception hierarchy for safe code sandbox execution."""


class SandboxException(Exception):
    """Base exception for all sandbox-related errors."""


SandboxError = SandboxException


class SandboxUnavailableError(SandboxException):
    """Raised when the container runtime (Docker) is unavailable."""


class SandboxTimeoutError(SandboxException):
    """Raised when execution exceeds the configured wall-clock timeout."""


class ResourceLimitExceededError(SandboxException):
    """Raised when container execution violates memory, CPU, or PID limits."""


class OutputLimitExceededError(SandboxException):
    """Raised when execution output exceeds the configured buffer threshold."""


class UnsupportedLanguageError(SandboxException):
    """Raised when execution is requested for an unsupported runtime language."""


class ValidationFailedError(SandboxException):
    """Raised when T18 code syntax validation fails before execution."""


class SandboxConfigurationError(SandboxException):
    """Raised when sandbox policy or configuration is invalid."""


class SandboxSecurityViolationError(SandboxException):
    """Raised when an execution violates strict security policies."""


class SandboxRuntimeError(SandboxException):
    """Raised when the sandbox infrastructure fails unexpectedly."""
