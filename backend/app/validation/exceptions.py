"""Domain exceptions for code and response validation."""

from typing import Optional


class ValidationException(Exception):
    """Base exception for code validation operations."""

    def __init__(self, message: str, cause: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.message = message
        self.cause = cause


class ValidatorTimeoutError(ValidationException):
    """Raised when an external compiler/syntax validator exceeds the allowed timeout."""

    def __init__(self, language: str, timeout_seconds: float, cause: Optional[Exception] = None) -> None:
        super().__init__(
            f"Validation for language '{language}' timed out after {timeout_seconds} seconds.",
            cause=cause,
        )
        self.language = language
        self.timeout_seconds = timeout_seconds


class ValidatorExecutionError(ValidationException):
    """Raised when an external validator subprocess cannot be started or encounters IO error."""

    def __init__(self, language: str, message: str, cause: Optional[Exception] = None) -> None:
        super().__init__(f"Validation execution failed for language '{language}': {message}", cause=cause)
        self.language = language
