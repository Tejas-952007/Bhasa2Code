"""Base class and models for language-specific sandbox execution runners."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from backend.app.sandbox.config import SandboxConfig


class LanguageExecutionPlan(BaseModel):
    """Execution plan containing files to stage and container command."""

    language: str
    image_tag: str
    files: Dict[str, str] = Field(
        ...,
        description="Dictionary mapping workspace relative filenames to string contents.",
    )
    entrypoint: List[str] = Field(
        ...,
        description="Command argument array to execute inside container workspace.",
    )
    is_ml: bool = Field(
        default=False,
        description="Flag indicating if workload requires scientific/ML environment profile.",
    )
    timeout_seconds: Optional[float] = Field(
        default=None,
        description="Recommended timeout for this execution plan.",
    )
    memory_limit_mb: Optional[int] = Field(
        default=None,
        description="Recommended memory limit for this execution plan.",
    )


class BaseLanguageRunner(ABC):
    """Abstract base class for sandbox language adapters."""

    @property
    @abstractmethod
    def language(self) -> str:
        """Primary identifier for this language."""

    @abstractmethod
    def build_plan(self, code: str, config: SandboxConfig) -> LanguageExecutionPlan:
        """Build the execution plan for the given source code and configuration."""
