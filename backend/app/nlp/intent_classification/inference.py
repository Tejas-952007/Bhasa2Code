from typing import Optional, Union

from backend.app.nlp.schemas import IntentClassificationResult, PreprocessedText
from backend.app.nlp.intent_classification.intent_classifier import IntentClassifier

_cached_classifier: Optional[IntentClassifier] = None


def get_intent_classifier() -> IntentClassifier:
    """Retrieve or initialize the cached global IntentClassifier instance."""
    global _cached_classifier
    if _cached_classifier is None:
        _cached_classifier = IntentClassifier()
    return _cached_classifier


def predict_intent(
    input_data: Union[str, PreprocessedText, None],
) -> IntentClassificationResult:
    """Convenience function to predict intent from text or PreprocessedText."""
    classifier = get_intent_classifier()
    return classifier.predict(input_data)
