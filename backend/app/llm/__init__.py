"""Local Ollama LLM integration module for Bhasha2Code."""

from backend.app.llm.config import OllamaSettings, get_ollama_settings
from backend.app.llm.exceptions import (
    OllamaError,
    OllamaGenerationError,
    OllamaModelNotFoundError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from backend.app.llm.llm_service import LLMService
from backend.app.llm.ollama_client import OllamaClient
from backend.app.llm.schemas import (
    GenerationOptions,
    HealthStatus,
    LLMResponse,
    ModelInfo,
)

__all__ = [
    "OllamaSettings",
    "get_ollama_settings",
    "OllamaClient",
    "LLMService",
    "ModelInfo",
    "HealthStatus",
    "LLMResponse",
    "GenerationOptions",
    "OllamaError",
    "OllamaUnavailableError",
    "OllamaModelNotFoundError",
    "OllamaTimeoutError",
    "OllamaGenerationError",
]
