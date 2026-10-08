"""Configuration settings for local Ollama integration."""

import os
from typing import Any, Dict
from pydantic import BaseModel, Field


class OllamaSettings(BaseModel):
    """Configuration parameters for connecting to the local Ollama daemon."""

    base_url: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    )
    model: str = Field(default_factory=lambda: os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b"))
    timeout_seconds: float = Field(
        default_factory=lambda: float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120.0"))
    )
    temperature: float = Field(
        default_factory=lambda: float(os.getenv("OLLAMA_TEMPERATURE", "0.2"))
    )
    num_ctx: int = Field(default_factory=lambda: int(os.getenv("OLLAMA_NUM_CTX", "8192")))
    debug_logging: bool = Field(
        default_factory=lambda: os.getenv("OLLAMA_DEBUG_LOGGING", "false").lower() in ("true", "1", "yes")
    )

    def get_generation_options(self) -> Dict[str, Any]:
        """Return the default options dict for Ollama /api/generate."""
        return {
            "temperature": self.temperature,
            "num_ctx": self.num_ctx,
        }


def get_ollama_settings() -> OllamaSettings:
    """Return an OllamaSettings instance populated from the environment."""
    return OllamaSettings()
