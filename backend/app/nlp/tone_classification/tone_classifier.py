import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import joblib

from backend.app.nlp.schemas import PreprocessedText, Tone, ToneClassificationResult

DEFAULT_MODEL_PATH = str(
    Path(__file__).resolve().parents[4] / "models" / "tone" / "tone_classifier.joblib"
)


class ToneClassifier:
    """Offline, deterministic conversational tone classifier for Bhasha2Code.

    Classifies user messages into:
    - CASUAL
    - FORMAL
    - SIMPLE
    - TECHNICAL
    - SHORT
    - DETAILED
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
            raise FileNotFoundError(f"Tone classifier model file not found at: '{path}'")
        try:
            return joblib.load(path)
        except Exception as exc:
            raise ValueError(f"Corrupted or invalid tone classifier model at '{path}': {exc}") from exc

    @classmethod
    def load(cls, model_path: str) -> "ToneClassifier":
        """Load a trained tone classification pipeline from disk."""
        return cls(model_path=model_path)

    def save(self, model_path: str) -> None:
        """Persist the trained tone classification pipeline to disk."""
        if self.pipeline is None:
            raise ValueError("Cannot save an uninitialized tone classification pipeline")
        os.makedirs(os.path.dirname(os.path.abspath(model_path)), exist_ok=True)
        joblib.dump(self.pipeline, model_path)

    def predict(self, input_data: Union[str, PreprocessedText, None]) -> ToneClassificationResult:
        """Predict the primary tone of the user's conversational message."""
        if self.pipeline is None:
            raise RuntimeError(
                "ToneClassifier model is not initialized or trained model file is missing. "
                "Train the model via `python scripts/train_tone_classifier.py` or provide a valid model path."
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
                f"Unsupported input type for tone classification: {type(input_data).__name__}. "
                "Expected str, PreprocessedText, or None."
            )

        stripped = text.strip()
        if not stripped:
            # Fallback neutral result for empty or whitespace-only input
            default_prob = round(1.0 / len(Tone), 4)
            return ToneClassificationResult(
                tone=Tone.SIMPLE.value,
                confidence=0.0,
                probabilities={t.value: default_prob for t in Tone},
            )

        pred_label = str(self.pipeline.predict([stripped])[0])
        prob_matrix = self.pipeline.predict_proba([stripped])[0]
        classes = self.pipeline.classes_

        probabilities: Dict[str, float] = {
            str(cls_name): float(prob) for cls_name, prob in zip(classes, prob_matrix)
        }
        confidence = float(max(prob_matrix))

        return ToneClassificationResult(
            tone=pred_label,
            confidence=confidence,
            probabilities=probabilities,
        )
