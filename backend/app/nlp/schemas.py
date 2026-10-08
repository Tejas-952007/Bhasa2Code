from enum import Enum
from typing import Any, List, Optional
from pydantic import BaseModel, Field


class CodeSegment(BaseModel):
    """Represents a code snippet identified during text preprocessing."""

    content: str
    language_hint: Optional[str] = None

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class PreprocessedText(BaseModel):
    """Structured result of safe multilingual text preprocessing."""

    original_text: str
    normalized_text: str
    text_segments: List[str] = Field(default_factory=list)
    code_segments: List[CodeSegment] = Field(default_factory=list)
    classifier_text: str = ""
    is_empty: bool = False

    @property
    def has_code(self) -> bool:
        """Return True if any code segment was identified."""
        return len(self.code_segments) > 0

    def to_dict(self) -> dict:
        """Convert the preprocessed text model to a dictionary."""
        return self.model_dump()

    def __getitem__(self, item: str) -> Any:
        """Allow dict-like subscripting for convenience."""
        return getattr(self, item)


class Language(str, Enum):
    """Supported conversational language classifications in Bhasha2Code."""

    ENGLISH = "ENGLISH"
    HINDI = "HINDI"
    MARATHI = "MARATHI"
    HINGLISH = "HINGLISH"
    MARATHI_ENGLISH = "MARATHI_ENGLISH"
    HINDI_ENGLISH = "HINDI_ENGLISH"
    UNKNOWN = "UNKNOWN"


class LanguageDetectionResult(BaseModel):
    """Result of deterministic conversational language detection."""

    language: Language
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: List[str] = Field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialize result to a dictionary."""
        return {
            "language": self.language.value,
            "confidence": round(self.confidence, 2),
            "evidence": self.evidence,
        }

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)
