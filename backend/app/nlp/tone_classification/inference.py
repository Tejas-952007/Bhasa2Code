from typing import Optional, Union

from backend.app.nlp.schemas import PreprocessedText, ToneClassificationResult
from backend.app.nlp.tone_classification.tone_classifier import ToneClassifier

_cached_classifier: Optional[ToneClassifier] = None


def get_tone_classifier() -> ToneClassifier:
    """Retrieve or initialize the cached global ToneClassifier instance."""
    global _cached_classifier
    if _cached_classifier is None:
        _cached_classifier = ToneClassifier()
    return _cached_classifier


def predict_tone(
    input_data: Union[str, PreprocessedText, None],
) -> ToneClassificationResult:
    """Convenience function to predict tone from text or PreprocessedText."""
    classifier = get_tone_classifier()
    return classifier.predict(input_data)
