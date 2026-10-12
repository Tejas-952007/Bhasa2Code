"""Pydantic schemas for the Ollama / Local LLM integration."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    """Metadata describing a model installed locally in Ollama."""

    name: str
    model: Optional[str] = None
    size: Optional[int] = None
    digest: Optional[str] = None
    modified_at: Optional[str] = None
    parameter_size: Optional[str] = None
    quantization_level: Optional[str] = None
    family: Optional[str] = None

    @classmethod
    def from_api_dict(cls, data: Dict[str, Any]) -> "ModelInfo":
        """Build ModelInfo from Ollama /api/tags JSON item."""
        details = data.get("details") or {}
        return cls(
            name=data.get("name", ""),
            model=data.get("model"),
            size=data.get("size"),
            digest=data.get("digest"),
            modified_at=data.get("modified_at"),
            parameter_size=details.get("parameter_size"),
            quantization_level=details.get("quantization_level"),
            family=details.get("family"),
        )


class HealthStatus(BaseModel):
    """Health status and reachability of the local Ollama daemon."""

    status: str
    available: bool = True
    version: Optional[str] = None
    models_count: Optional[int] = None


class GenerationOptions(BaseModel):
    """Fine-grained generation hyperparameters passed to Ollama."""

    temperature: Optional[float] = None
    num_ctx: Optional[int] = None
    num_predict: Optional[int] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    stop: Optional[List[str]] = None

    def to_ollama_options(self) -> Dict[str, Any]:
        """Convert non-None options to Ollama parameter dictionary."""
        opts: Dict[str, Any] = {}
        if self.temperature is not None:
            opts["temperature"] = self.temperature
        if self.num_ctx is not None:
            opts["num_ctx"] = self.num_ctx
        if self.num_predict is not None:
            opts["num_predict"] = self.num_predict
        if self.top_k is not None:
            opts["top_k"] = self.top_k
        if self.top_p is not None:
            opts["top_p"] = self.top_p
        if self.stop is not None:
            opts["stop"] = self.stop
        return opts


class LLMResponse(BaseModel):
    """Structured response returned by local LLM generation."""

    text: str
    model: str
    total_duration_ms: Optional[float] = None
    time_to_first_token_ms: Optional[float] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    done: bool = True
    done_reason: Optional[str] = "stop"
    raw_metadata: Dict[str, Any] = Field(default_factory=dict)
