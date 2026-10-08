import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import joblib

from backend.app.nlp.schemas import Intent, IntentClassificationResult, PreprocessedText

DEFAULT_MODEL_PATH = str(
    Path(__file__).resolve().parents[4] / "models" / "intent" / "intent_classifier.joblib"
)


class IntentClassifier:
    """Offline, deterministic conversational intent classifier for Bhasha2Code.

    Classifies user messages into exactly one of 18 supported intent classes:
    - GENERATE_CODE
    - DEBUG_CODE
    - EXPLAIN_CODE
    - OPTIMIZE_CODE
    - CONVERT_CODE
    - ALGORITHM
    - CONCEPT
    - CODE_REVIEW
    - CODE_SUGGESTION
    - PERFORMANCE_ANALYSIS
    - ERROR_EXPLANATION
    - APPROACH_SUGGESTION
    - BEST_PRACTICE
    - ARCHITECTURE_SUGGESTION
    - FEATURE_SUGGESTION
    - TEST_CASE_GENERATION
    - SECURITY_ANALYSIS
    - SEARCH
    """

    def __init__(
        self,
        pipeline: Optional[Any] = None,
        model_path: Optional[str] = None,
    ) -> None:
        if pipeline is not None:
            self.pipeline = pipeline
        elif model_path is not None:
            self.pipeline = self._load_pipeline(model_path)
        else:
            if os.path.exists(DEFAULT_MODEL_PATH):
                self.pipeline = self._load_pipeline(DEFAULT_MODEL_PATH)
            else:
                self.pipeline = None

    @staticmethod
    def _load_pipeline(path: str) -> Any:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Intent classifier model file not found at: '{path}'")
        try:
            return joblib.load(path)
        except Exception as exc:
            raise ValueError(f"Corrupted or invalid intent classifier model at '{path}': {exc}") from exc

    @classmethod
    def load(cls, model_path: str) -> "IntentClassifier":
        """Load a trained intent classification pipeline from disk."""
        return cls(model_path=model_path)

    def save(self, model_path: str) -> None:
        """Persist the trained intent classification pipeline to disk."""
        if self.pipeline is None:
            raise ValueError("Cannot save an uninitialized intent classification pipeline")
        os.makedirs(os.path.dirname(os.path.abspath(model_path)), exist_ok=True)
        joblib.dump(self.pipeline, model_path)

    def predict(self, input_data: Union[str, PreprocessedText, None]) -> IntentClassificationResult:
        """Predict the primary intent of the user's conversational message."""
        if self.pipeline is None:
            raise RuntimeError(
                "IntentClassifier model is not initialized or trained model file is missing. "
                "Train the model via `python scripts/train_intent_classifier.py` or provide a valid model path."
            )

        if input_data is None:
            text = ""
        elif isinstance(input_data, str):
            text = input_data
        elif isinstance(input_data, PreprocessedText):
            text = (
                " ".join(input_data.text_segments)
                if input_data.text_segments
                else input_data.classifier_text
            )
        else:
            raise TypeError(
                f"Unsupported input type for intent classification: {type(input_data).__name__}. "
                "Expected str, PreprocessedText, or None."
            )

        stripped = text.strip()
        if not stripped:
            # Fallback neutral result for empty or whitespace-only input
            default_prob = round(1.0 / len(Intent), 4)
            return IntentClassificationResult(
                intent=Intent.CONCEPT.value,
                confidence=0.0,
                probabilities={i.value: default_prob for i in Intent},
            )

        pred_label = str(self.pipeline.predict([stripped])[0])
        prob_matrix = self.pipeline.predict_proba([stripped])[0]
        classes = self.pipeline.classes_

        probabilities: Dict[str, float] = {
            str(cls_name): float(prob) for cls_name, prob in zip(classes, prob_matrix)
        }
        confidence = float(max(prob_matrix))

        return IntentClassificationResult(
            intent=pred_label,
            confidence=confidence,
            probabilities=probabilities,
        )
