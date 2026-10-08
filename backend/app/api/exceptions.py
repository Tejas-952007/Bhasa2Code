"""Standard API exceptions and error codes conforming to the T21 error contract."""

from typing import Optional


class APIException(Exception):
    """Base API Exception producing standard JSON errors."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[dict] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class SessionNotFoundAPIError(APIException):
    def __init__(self, message: str = "The requested session was not found.") -> None:
        super().__init__(code="SESSION_NOT_FOUND", message=message, status_code=404)


class UnauthorizedSessionAPIError(APIException):
    def __init__(self, message: str = "Access to this session is unauthorized.") -> None:
        super().__init__(code="UNAUTHORIZED_SESSION", message=message, status_code=403)


class OllamaUnavailableAPIError(APIException):
    def __init__(
        self,
        message: str = "The local model is unavailable. Please check Ollama and try again.",
    ) -> None:
        super().__init__(code="OLLAMA_UNAVAILABLE", message=message, status_code=503)


class OllamaModelNotFoundAPIError(APIException):
    def __init__(self, model_name: str) -> None:
        super().__init__(
            code="OLLAMA_MODEL_NOT_FOUND",
            message=f"Configured model '{model_name}' not found in local Ollama installation.",
            status_code=503,
        )


class ValidationFailedAPIError(APIException):
    def __init__(self, message: str = "Code validation failed.", details: Optional[dict] = None) -> None:
        super().__init__(code="VALIDATION_FAILED", message=message, status_code=400, details=details)


class SandboxAPIError(APIException):
    def __init__(self, message: str = "The code sandbox encountered an error.", details: Optional[dict] = None) -> None:
        super().__init__(code="SANDBOX_ERROR", message=message, status_code=500, details=details)


class ExecutionTimeoutAPIError(APIException):
    def __init__(self, message: str = "Code execution timed out.") -> None:
        super().__init__(code="EXECUTION_TIMEOUT", message=message, status_code=504)


class BadRequestAPIError(APIException):
    def __init__(self, message: str = "Invalid request parameters.") -> None:
        super().__init__(code="BAD_REQUEST", message=message, status_code=400)
