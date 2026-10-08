"""Schemas for the Context Manager module."""

from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field


class ContextMessage(BaseModel):
    """Represents a single contextual conversation message turn."""

    message_id: Union[str, int]
    role: str
    content: str
    created_at: Optional[str] = None
    relevance: str = "recent"

    def to_dict(self) -> dict[str, Any]:
        """Serialize message to dictionary."""
        return self.model_dump()

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class ContextCode(BaseModel):
    """Represents a generated code artifact linked into the conversational context."""

    generated_code_id: Union[str, int]
    message_id: Optional[Union[str, int]] = None
    language: Optional[str] = None
    code: str
    validation_status: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize code artifact to dictionary."""
        return self.model_dump()

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class ContextMetadata(BaseModel):
    """Metadata capturing NLP classifications, follow-up flags, and diagnostic info."""

    language: Optional[str] = None
    tone: Optional[str] = None
    intent: Optional[str] = None
    is_follow_up: bool = False
    confidence_scores: dict[str, float] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize context metadata to dictionary."""
        return self.model_dump()

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class ContextPackage(BaseModel):
    """Structured context payload packaging multi-turn session history, code, and metadata."""

    session_id: Union[str, int]
    user_id: Optional[Union[str, int]] = None
    current_message: str
    current_code: Optional[str] = None
    messages: List[ContextMessage] = Field(default_factory=list)
    generated_code: List[ContextCode] = Field(default_factory=list)
    metadata: Optional[ContextMetadata] = None
    session_metadata: Optional[dict[str, Any]] = None
    total_messages: int = 0
    truncated: bool = False

    @property
    def has_code(self) -> bool:
        """Return True if current input or conversation history contains code."""
        return bool(self.current_code) or len(self.generated_code) > 0

    @property
    def has_history(self) -> bool:
        """Return True if previous session messages exist."""
        return len(self.messages) > 0

    def to_dict(self) -> dict[str, Any]:
        """Serialize package into a clean nested dictionary."""
        return self.model_dump()

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)
