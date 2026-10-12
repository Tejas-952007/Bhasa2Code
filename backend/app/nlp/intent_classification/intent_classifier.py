import os
import re
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

        # Disambiguation: Detect concept / library / definitional inquiries
        is_code_present = False
        if isinstance(input_data, PreprocessedText):
            is_code_present = input_data.has_code
        else:
            is_code_present = bool(
                re.search(
                    r"```|def\s+\w+\s*\(|class\s+\w+|for\s+\w+\s+in|while\s+|=>|;\s*$|<[a-zA-Z0-9]+.*>|import\s+\w+",
                    stripped,
                )
            )

        explicit_code_request = bool(
            re.search(
                r"\b(code|function|script|snippet|program|implementation|line\s+by\s+line|"
                r"हा\s+कोड|या\s+कोड|हा\s+प्रोग्राम|हे\s+फंक्शन|फंक्शन|प्रोग्राम|कोड)\b",
                stripped,
                re.IGNORECASE,
            )
        )

        excluded_signals = bool(
            re.search(
                r"\b(best\s*practice|recommended\s*way|search|find\s+our|previous\s+discussion|"
                r"taking\s*so\s*long|why\s+is\s+(?:this|my).*(?:slow|taking)|profile|faster)\b",
                stripped,
                re.IGNORECASE,
            )
        )

        algorithm_inquiry = bool(
            re.search(
                r"\b(binary\s*search|linear\s*search|dijkstra|bubble\s*sort|merge\s*sort|"
                r"quick\s*sort|insertion\s*sort|selection\s*sort|heap\s*sort|bfs|dfs|"
                r"algorithm|अल्गोरिदम)\b",
                stripped,
                re.IGNORECASE,
            )
        )

        definitional_inquiry = bool(
            re.search(
                r"\b(mhanje\s+kay|mhnje\s+kay|म्हणजे\s*काय|काय\s*आहे|kay\s+ahe|kaay\s+aahe|kya\s+hai|kya\s+hota\s+hai|arth\s+kay)\b|"
                r"^\s*what\s+is\s+(?:a\s+|an\s+|the\s+)?[a-zA-Z0-9_\-\s]+\??$",
                stripped,
                re.IGNORECASE,
            )
        )

        concept_library_inquiry = bool(
            re.search(
                r"\b(library|package|module|framework|concept|api|sdk|toolkit|tool|"
                r"recursion|polymorphism|inheritance|encapsulation|abstraction|oops|oop|"
                r"badal\s+sang|vishayi\s+sang|baddal\s+sang|baddal\s+bol|vishayi\s+bol|"
                r"matplotlib|numpy|pandas|scipy|sklearn|seaborn|tensorflow|pytorch|keras|"
                r"flask|django|fastapi|react|vue|angular|express|docker|kubernetes|git)\b",
                stripped,
                re.IGNORECASE,
            )
        )

        raw_full = ""
        if isinstance(input_data, PreprocessedText):
            raw_full = input_data.original_text.strip()
        elif isinstance(input_data, str):
            raw_full = input_data.strip()
        search_target = f"{raw_full} {stripped}".strip()

        explain_code_inquiry = bool(
            re.search(
                r"\b("
                r"(?:please\s+|can\s+you\s+)?explain\s+(?:me\s+)?(?:this\s+|the\s+)?(?:code|program|script|function|snippet|implementation|algorithm)?"
                r"|(?:code|program|script|function)\s*(?:ko\s*)?(?:explain|samjhao|samjha|batao|samjav|samjhav|sang|sanga)"
                r"|(?:ha|he|ya|ye|is)\s*(?:code|program|function|script)\s*(?:la\s*)?(?:explain|samjav|samjhav|samjhao|sang|sanga)"
                r"|(?:code|program)\s*(?:explain\s*(?:karr*|kr|kara|karo|batao|sang|sanga)|samjav|samjhav)"
                r"|what\s+does\s+this\s+(?:code|program|script|function)\s+do"
                r"|how\s+does\s+this\s+(?:code|program|script|function)\s+work"
                r"|walk\s*(?:me\s*)?through\s+this\s+(?:code|program)"
                r"|line\s+by\s+line\s+explanation"
                r"|हा\s+कोड\s+(?:समजाव|समजावून\s+सांग|explain\s+कर)"
                r"|ये\s+कोड\s+(?:समझाओ|explain\s+करो)"
                r")\b",
                search_target,
                re.IGNORECASE,
            )
        )

        debug_inquiry = bool(
            re.search(
                r"\b(fix|bug|debug|error|exception|crash|traceback|syntaxerror|nameerror|typeerror)\b",
                search_target,
                re.IGNORECASE,
            )
        )

        optimize_inquiry = bool(
            re.search(
                r"\b(optimize|faster|slow|speed\s+up|reduce\s+memory|performance)\b",
                search_target,
                re.IGNORECASE,
            )
        )

        search_signal = bool(
            re.search(
                r"\b(search|find\s+(?:my|our|the|a)?\s*previous|previous\s+(?:chat|conversation|discussion|message|code)|earlier\s+(?:chat|discussion|conversation)|history|खोज|शोध)\b",
                search_target,
                re.IGNORECASE,
            )
        )

        # Override to EXPLAIN_CODE when code explanation intent is explicitly requested
        if explain_code_inquiry and not debug_inquiry and not optimize_inquiry and not excluded_signals and not search_signal:
            pred_label = Intent.EXPLAIN_CODE.value
            confidence = max(confidence, 0.92)
            probabilities[Intent.EXPLAIN_CODE.value] = confidence

        # Guard against spurious SEARCH intent when no search signals exist
        elif pred_label == Intent.SEARCH.value and not search_signal:
            if is_code_present or explicit_code_request:
                pred_label = Intent.EXPLAIN_CODE.value
                confidence = max(confidence, 0.88)
                probabilities[Intent.EXPLAIN_CODE.value] = confidence
            else:
                pred_label = Intent.CONCEPT.value
                confidence = max(confidence, 0.85)
                probabilities[Intent.CONCEPT.value] = confidence

        elif not is_code_present and not explicit_code_request and not excluded_signals and not algorithm_inquiry:
            if definitional_inquiry or (pred_label == Intent.EXPLAIN_CODE.value and concept_library_inquiry):
                pred_label = Intent.CONCEPT.value
                concept_prob = probabilities.get(Intent.CONCEPT.value, 0.0)
                confidence = max(confidence, concept_prob, 0.88)
                probabilities[Intent.CONCEPT.value] = confidence

        # Normalize probabilities to ensure they sum to 1.0
        total_p = sum(probabilities.values())
        if total_p > 0:
            probabilities = {k: v / total_p for k, v in probabilities.items()}

        return IntentClassificationResult(
            intent=pred_label,
            confidence=confidence,
            probabilities=probabilities,
        )

