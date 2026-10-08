from typing import Any
from pydantic import BaseModel

from backend.app.nlp.schemas import (
    IntentClassificationResult,
    LanguageDetectionResult,
    PreprocessedText,
    ToneClassificationResult,
)


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


__all__ = ["NLPPipelineResult"]
