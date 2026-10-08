"""Domain exceptions for Ollama / Local LLM integration."""

from typing import Optional


class OllamaError(Exception):
    """Base exception for all Ollama-related errors."""

    def __init__(self, message: str, cause: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.message = message
        self.cause = cause


class OllamaUnavailableError(OllamaError):
    """Raised when the local Ollama daemon is unreachable or not running."""

    def __init__(
        self,
        message: str = "Local AI service unavailable. Please start Ollama and verify the configured model.",
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message, cause=cause)


class OllamaModelNotFoundError(OllamaError):
    """Raised when the requested or configured model is not installed locally in Ollama."""

    def __init__(
        self,
        model_name: str,
        message: Optional[str] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        self.model_name = model_name
        if not message:
            message = (
                f"Ollama service reachable, but configured model '{model_name}' is not installed. "
                f"Run the appropriate local Ollama command manually: 'ollama pull {model_name}'."
            )
        super().__init__(message, cause=cause)


class OllamaTimeoutError(OllamaError):
    """Raised when Ollama request exceeds configured timeout threshold."""

    def __init__(
        self,
        timeout_seconds: float,
        message: Optional[str] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        if not message:
            message = f"Ollama generation timed out after {timeout_seconds} seconds."
        super().__init__(message, cause=cause)


class OllamaGenerationError(OllamaError):
    """Raised when Ollama generation fails, returns HTTP errors, or yields empty text."""

    def __init__(
        self,
        message: str = "Ollama generation failed or returned an empty response.",
        status_code: Optional[int] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        self.status_code = status_code
        super().__init__(message, cause=cause)
