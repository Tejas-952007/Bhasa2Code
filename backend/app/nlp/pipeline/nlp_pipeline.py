import logging
import os
from pathlib import Path
from typing import Optional, Union

from backend.app.nlp.intent_classification.intent_classifier import (
    DEFAULT_MODEL_PATH as DEFAULT_INTENT_MODEL_PATH,
    IntentClassifier,
)
from backend.app.nlp.language_detection.language_detector import LanguageDetector
from backend.app.nlp.pipeline.schemas import NLPPipelineResult
from backend.app.nlp.preprocessing.text_preprocessor import TextPreprocessor
from backend.app.nlp.schemas import PreprocessedText
from backend.app.nlp.tone_classification.tone_classifier import (
    DEFAULT_MODEL_PATH as DEFAULT_TONE_MODEL_PATH,
    ToneClassifier,
)

logger = logging.getLogger("bhasha2code.nlp.pipeline")


def select_classifier_text(preprocessed: PreprocessedText) -> str:
    """Select the primary natural language text for downstream classifiers.

    Selection hierarchy:
    1. Natural-language text segments (isolated from fenced code blocks or unfenced raw code).
    2. Classifier text produced by T08 preprocessing if available.
    3. Fallback to raw code content or normalized text for code-only inputs, ensuring
       classifiers gracefully handle non-conversational input without raising errors.

    Args:
        preprocessed: Normalized PreprocessedText instance from TextPreprocessor.

    Returns:
        Clean natural-language text string tailored for tone and intent inference.
    """
    if preprocessed.is_empty:
        return ""

    # Primary: Isolated natural language commentary preceding or following code blocks
    if preprocessed.text_segments:
        return " ".join(preprocessed.text_segments).strip()

    # Secondary: T08 designated classifier_text if not purely code
    if preprocessed.classifier_text and not preprocessed.has_code:
        return preprocessed.classifier_text.strip()

    # Fallback for code-only inputs: pass classifier_text as a best-effort hint
    if preprocessed.classifier_text:
        return preprocessed.classifier_text.strip()

    return preprocessed.normalized_text.strip()


class NLPPipeline:
    """Deterministic, offline, unified NLP pipeline for Bhasha2Code.

    Sequential orchestration flow:
    1. TextPreprocessor (T08): Unicode NFC normalization and code/natural-language separation.
    2. LanguageDetector (T09): Deterministic conversational language detection.
    3. ToneClassifier (T11): Multi-class conversational tone classification.
    4. IntentClassifier (T13): Multi-class user intent classification.

    All components execute locally without network access or cloud dependencies.
    """

    def __init__(
        self,
        preprocessor: Optional[TextPreprocessor] = None,
        language_detector: Optional[LanguageDetector] = None,
        tone_classifier: Optional[ToneClassifier] = None,
        intent_classifier: Optional[IntentClassifier] = None,
    ) -> None:
        self.preprocessor = preprocessor or TextPreprocessor()
        self.language_detector = language_detector or LanguageDetector(
            preprocessor=self.preprocessor
        )

        # Tone Classifier initialization & validation
        if tone_classifier is not None:
            self.tone_classifier = tone_classifier
        else:
            if not os.path.exists(DEFAULT_TONE_MODEL_PATH):
                raise FileNotFoundError(
                    f"Tone classifier model file missing at '{DEFAULT_TONE_MODEL_PATH}'. "
                    "Run `python scripts/train_tone_classifier.py` before initializing pipeline."
                )
            self.tone_classifier = ToneClassifier(model_path=DEFAULT_TONE_MODEL_PATH)

        # Intent Classifier initialization & validation
        if intent_classifier is not None:
            self.intent_classifier = intent_classifier
        else:
            if not os.path.exists(DEFAULT_INTENT_MODEL_PATH):
                raise FileNotFoundError(
                    f"Intent classifier model file missing at '{DEFAULT_INTENT_MODEL_PATH}'. "
                    "Run `python scripts/train_intent_classifier.py` before initializing pipeline."
                )
            self.intent_classifier = IntentClassifier(model_path=DEFAULT_INTENT_MODEL_PATH)

        # Verify that internal ML pipelines are ready
        if self.tone_classifier.pipeline is None:
            raise RuntimeError("ToneClassifier model failed to load its internal pipeline.")
        if self.intent_classifier.pipeline is None:
            raise RuntimeError("IntentClassifier model failed to load its internal pipeline.")

    @classmethod
    def load_default(cls) -> "NLPPipeline":
        """Load and return an instance of the default pipeline."""
        return cls()

    def select_classifier_text(self, preprocessed: PreprocessedText) -> str:
        """Instance method exposing classifier text selection helper."""
        return select_classifier_text(preprocessed)

    def analyze(
        self,
        input_data: Union[str, PreprocessedText, None],
    ) -> NLPPipelineResult:
        """Execute the complete sequential NLP pipeline on the user's input.

        Args:
            input_data: Raw user message string, already preprocessed PreprocessedText, or None.

        Returns:
            NLPPipelineResult containing all intermediate and final NLP stage outputs.

        Raises:
            TypeError: If input_data is of an unsupported type (e.g., dict, list, int).
        """
        if input_data is not None and not isinstance(input_data, (str, PreprocessedText)):
            raise TypeError(
                f"Unsupported input type for NLP pipeline: {type(input_data).__name__}. "
                "Expected str, PreprocessedText, or None."
            )

        # Stage 1: Text Preprocessing (T08)
        if isinstance(input_data, PreprocessedText):
            preprocessed = input_data
        else:
            preprocessed = self.preprocessor.preprocess(input_data)

        logger.debug(
            "Stage 1 Preprocessing complete (has_code=%s, is_empty=%s)",
            preprocessed.has_code,
            preprocessed.is_empty,
        )

        # Stage 2: Language Detection (T09)
        language_result = self.language_detector.detect(preprocessed)
        logger.debug(
            "Stage 2 Language detection complete: %s (confidence=%.2f)",
            language_result.language.value,
            language_result.confidence,
        )

        # Stage 3: Conversational Tone Classification (T11)
        tone_result = self.tone_classifier.predict(preprocessed)
        logger.debug(
            "Stage 3 Tone classification complete: %s (confidence=%.2f)",
            tone_result.tone,
            tone_result.confidence,
        )

        # Stage 4: User Intent Classification (T13)
        intent_result = self.intent_classifier.predict(preprocessed)
        logger.debug(
            "Stage 4 Intent classification complete: %s (confidence=%.2f)",
            intent_result.intent,
            intent_result.confidence,
        )

        # Unified Result Assembly
        return NLPPipelineResult(
            preprocessed_text=preprocessed,
            language=language_result,
            tone=tone_result,
            intent=intent_result,
        )

    def process(
        self,
        input_data: Union[str, PreprocessedText, None],
    ) -> NLPPipelineResult:
        """Alias for analyze() to provide unified method compatibility."""
        return self.analyze(input_data)

    def __call__(
        self,
        input_data: Union[str, PreprocessedText, None],
    ) -> NLPPipelineResult:
        """Allow pipeline instance to be called directly like a function."""
        return self.analyze(input_data)


# Module-level cached pipeline singleton for high performance across calls
_cached_pipeline: Optional[NLPPipeline] = None


def get_nlp_pipeline() -> NLPPipeline:
    """Retrieve or initialize the cached global NLPPipeline singleton."""
    global _cached_pipeline
    if _cached_pipeline is None:
        _cached_pipeline = NLPPipeline.load_default()
    return _cached_pipeline


def analyze_text(
    input_data: Union[str, PreprocessedText, None],
) -> NLPPipelineResult:
    """Convenience function to analyze text through the global cached NLP pipeline."""
    pipeline = get_nlp_pipeline()
    return pipeline.analyze(input_data)
