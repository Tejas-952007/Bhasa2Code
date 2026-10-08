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


class Tone(str, Enum):
    """Supported conversational tone classes in Bhasha2Code."""

    CASUAL = "CASUAL"
    FORMAL = "FORMAL"
    SIMPLE = "SIMPLE"
    TECHNICAL = "TECHNICAL"
    SHORT = "SHORT"
    DETAILED = "DETAILED"


class ToneClassificationResult(BaseModel):
    """Result of conversational tone classification."""

    tone: str
    confidence: float = Field(ge=0.0, le=1.0)
    probabilities: dict[str, float] = Field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize result to a dictionary."""
        return {
            "tone": self.tone,
            "confidence": round(self.confidence, 4),
            "probabilities": {k: round(v, 4) for k, v in self.probabilities.items()},
        }

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class Intent(str, Enum):
    """Supported user intent classes in Bhasha2Code."""

    GENERATE_CODE = "GENERATE_CODE"
    DEBUG_CODE = "DEBUG_CODE"
    EXPLAIN_CODE = "EXPLAIN_CODE"
    OPTIMIZE_CODE = "OPTIMIZE_CODE"
    CONVERT_CODE = "CONVERT_CODE"
    ALGORITHM = "ALGORITHM"
    CONCEPT = "CONCEPT"
    CODE_REVIEW = "CODE_REVIEW"
    CODE_SUGGESTION = "CODE_SUGGESTION"
    PERFORMANCE_ANALYSIS = "PERFORMANCE_ANALYSIS"
    ERROR_EXPLANATION = "ERROR_EXPLANATION"
    APPROACH_SUGGESTION = "APPROACH_SUGGESTION"
    BEST_PRACTICE = "BEST_PRACTICE"
    ARCHITECTURE_SUGGESTION = "ARCHITECTURE_SUGGESTION"
    FEATURE_SUGGESTION = "FEATURE_SUGGESTION"
    TEST_CASE_GENERATION = "TEST_CASE_GENERATION"
    SECURITY_ANALYSIS = "SECURITY_ANALYSIS"
    SEARCH = "SEARCH"


class IntentClassificationResult(BaseModel):
    """Result of user intent classification."""

    intent: str
    confidence: float = Field(ge=0.0, le=1.0)
    probabilities: dict[str, float] = Field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize result to a dictionary."""
        return {
            "intent": self.intent,
            "confidence": round(self.confidence, 4),
            "probabilities": {k: round(v, 4) for k, v in self.probabilities.items()},
        }

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


class NLPPipelineResult(BaseModel):
    """Unified result produced by the sequential Bhasha2Code NLP Pipeline."""

    preprocessed_text: PreprocessedText
    language: LanguageDetectionResult
    tone: ToneClassificationResult
    intent: IntentClassificationResult

    @property
    def raw_text(self) -> str:
        """Original raw user input text before normalization."""
        return self.preprocessed_text.original_text

    @property
    def normalized_text(self) -> str:
        """Normalized natural language text from text preprocessing."""
        return self.preprocessed_text.normalized_text

    @property
    def has_code(self) -> bool:
        """Return True if any code blocks or stack traces were identified."""
        return self.preprocessed_text.has_code

    @property
    def detected_language(self) -> str:
        """Detected natural language or code-mixed category value."""
        return self.language.language.value

    @property
    def detected_tone(self) -> str:
        """Predicted communication tone label."""
        return self.tone.tone

    @property
    def detected_intent(self) -> str:
        """Predicted user operational intent label."""
        return self.intent.intent

    def to_dict(self) -> dict:
        """Serialize the complete pipeline result into a structured dictionary."""
        return {
            "preprocessed_text": self.preprocessed_text.to_dict(),
            "language": self.language.to_dict(),
            "tone": self.tone.to_dict(),
            "intent": self.intent.to_dict(),
        }

    def __getitem__(self, item: str) -> Any:
        """Enable dictionary-like subscripting for pipeline stages."""
        return getattr(self, item)

