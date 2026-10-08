"""Base class and models for language-specific sandbox execution runners."""

from abc import ABC, abstractmethod
from typing import Dict, List
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


class BaseLanguageRunner(ABC):
    """Abstract base class for sandbox language adapters."""

    @property
    @abstractmethod
    def language(self) -> str:
        """Primary identifier for this language."""

    @abstractmethod
    def build_plan(self, code: str, config: SandboxConfig) -> LanguageExecutionPlan:
        """Build the execution plan for the given source code and configuration."""
