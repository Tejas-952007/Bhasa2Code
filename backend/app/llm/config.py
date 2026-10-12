"""Configuration settings for local Ollama integration."""

import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


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
    # T23: Cap max output tokens to prevent runaway generation.
    # Default 600 tokens ≈ ~450 words — enough for a working code block + short explanation.
    # Users can set OLLAMA_NUM_PREDICT=0 to disable the cap.
    num_predict: int = Field(
        default_factory=lambda: int(os.getenv("OLLAMA_NUM_PREDICT", "600"))
    )
    # T23: Additional stop sequences that terminate generation early for safety.
    stop_sequences: Optional[List[str]] = Field(
        default_factory=lambda: None  # None = use Ollama model defaults
    )
    debug_logging: bool = Field(
        default_factory=lambda: os.getenv("OLLAMA_DEBUG_LOGGING", "false").lower() in ("true", "1", "yes")
    )

    def get_generation_options(self) -> Dict[str, Any]:
        """Return the default options dict for Ollama /api/generate."""
        opts: Dict[str, Any] = {
            "temperature": self.temperature,
            "num_ctx": self.num_ctx,
        }
        # Apply token cap only when explicitly set (>0)
        if self.num_predict and self.num_predict > 0:
            opts["num_predict"] = self.num_predict
        if self.stop_sequences:
            opts["stop"] = self.stop_sequences
        return opts


def get_ollama_settings() -> OllamaSettings:
    """Return an OllamaSettings instance populated from the environment."""
    return OllamaSettings()
