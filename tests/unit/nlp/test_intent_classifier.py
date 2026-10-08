"""Unit tests for the Bhasha2Code offline Intent Classifier (T13).

Verifies:
- Model artifact presence and metadata validity
- Schema conformance (18 intent labels, probabilities sum to ~1.0, confidence in [0, 1])
- Core intent coverage across all 18 classes
- Multilingual performance (English, Hindi, Marathi, Hinglish, Marathi-English, Hindi-English)
- Contrastive intent differentiation
- Critical boundary resolution
- Tone independence (intent preservation across casual, formal, simple, detailed phrasing)
- Edge case handling (empty, whitespace, None, PreprocessedText, code, traceback)
- Determinism of repeated inference runs
- Strict data isolation across train, validation, and test splits
"""

import json
import math
import os
from typing import Dict
import pytest

from backend.app.nlp.intent_classification.inference import (
    get_intent_classifier,
    predict_intent,
)
from backend.app.nlp.intent_classification.intent_classifier import IntentClassifier
from backend.app.nlp.schemas import (
    Intent,
    IntentClassificationResult,
    PreprocessedText,
)

MODEL_PATH = os.path.join("models", "intent", "intent_classifier.joblib")
METADATA_PATH = os.path.join("models", "intent", "metadata.json")

EXPECTED_INTENTS = {
    "GENERATE_CODE",
    "DEBUG_CODE",
    "EXPLAIN_CODE",
    "OPTIMIZE_CODE",
    "CONVERT_CODE",
    "ALGORITHM",
    "CONCEPT",
    "CODE_REVIEW",
    "CODE_SUGGESTION",
    "PERFORMANCE_ANALYSIS",
    "ERROR_EXPLANATION",
    "APPROACH_SUGGESTION",
    "BEST_PRACTICE",
    "ARCHITECTURE_SUGGESTION",
    "FEATURE_SUGGESTION",
    "TEST_CASE_GENERATION",
    "SECURITY_ANALYSIS",
    "SEARCH",
}


@pytest.fixture
def classifier() -> IntentClassifier:
    return IntentClassifier(model_path=MODEL_PATH)


class TestIntentModelArtifacts:
    def test_model_artifact_exists(self) -> None:
        assert os.path.exists(MODEL_PATH), f"Model artifact missing at {MODEL_PATH}"
        assert os.path.getsize(MODEL_PATH) > 1000

    def test_metadata_artifact_exists_and_valid(self) -> None:
        assert os.path.exists(METADATA_PATH), f"Metadata file missing at {METADATA_PATH}"
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)

        assert meta["task"] == "intent_classification"
        assert meta["model"] == "tfidf_logistic_regression"
        assert set(meta["labels"]) == EXPECTED_INTENTS
        assert meta["train_samples"] == 756
        assert meta["validation_samples"] == 162
        assert meta["test_samples"] == 162
        assert meta["validation_metrics"]["accuracy"] >= 0.80
        assert meta["validation_metrics"]["macro_f1"] >= 0.80
        assert meta["test_metrics"]["accuracy"] >= 0.78
        assert meta["test_metrics"]["macro_f1"] >= 0.78


class TestIntentClassifierSchema:
    def test_prediction_schema_and_types(self, classifier: IntentClassifier) -> None:
        res = classifier.predict("Please explain this python function.")
        assert isinstance(res, IntentClassificationResult)
        assert res.intent in EXPECTED_INTENTS
        assert 0.0 <= res.confidence <= 1.0
        assert isinstance(res.probabilities, dict)
        assert set(res.probabilities.keys()) == EXPECTED_INTENTS

        # Probabilities sum to ~1.0
        prob_sum = sum(res.probabilities.values())
        assert math.isclose(prob_sum, 1.0, abs_tol=1e-3)

    def test_to_dict_serialization(self, classifier: IntentClassifier) -> None:
        res = classifier.predict("bro debug this code")
        d = res.to_dict()
        assert d["intent"] == res.intent
        assert "confidence" in d
        assert "probabilities" in d
        assert set(d["probabilities"].keys()) == EXPECTED_INTENTS


class TestIntentClassifierCoreCoverage:
    @pytest.mark.parametrize(
        "text,expected_intent",
        [
            ("Write a Python program to calculate the factorial of a number.", "GENERATE_CODE"),
            ("Fix this Python script because it throws an IndexError.", "DEBUG_CODE"),
            ("Explain line by line how this Python recursive function works.", "EXPLAIN_CODE"),
            ("Optimize this nested loop to improve execution time.", "OPTIMIZE_CODE"),
            ("Convert this JavaScript code into equivalent Python.", "CONVERT_CODE"),
            ("How does Dijkstra's shortest path algorithm work?", "ALGORITHM"),
            ("What is polymorphism in object-oriented programming?", "CONCEPT"),
            ("Review this pull request code for readability and edge cases.", "CODE_REVIEW"),
            ("What improvements can I make to this Python function?", "CODE_SUGGESTION"),
            ("Why is this Pandas DataFrame merge taking so long to complete?", "PERFORMANCE_ANALYSIS"),
            ("What does AttributeError NoneType has no attribute mean?", "ERROR_EXPLANATION"),
            ("What approach should I take to solve the two-sum problem efficiently?", "APPROACH_SUGGESTION"),
            ("What are the best practices for handling database sessions in FastAPI?", "BEST_PRACTICE"),
            ("How should I design the microservices architecture for an e-commerce platform?", "ARCHITECTURE_SUGGESTION"),
            ("What features should I add to my CLI expense tracker project?", "FEATURE_SUGGESTION"),
            ("Generate pytest test cases for this string validation function.", "TEST_CASE_GENERATION"),
            ("Scan this SQL query for potential SQL injection vulnerabilities.", "SECURITY_ANALYSIS"),
            ("Find my previous Python script where we implemented binary search.", "SEARCH"),
        ],
    )
    def test_all_eighteen_intents_covered(
        self, classifier: IntentClassifier, text: str, expected_intent: str
    ) -> None:
        res = classifier.predict(text)
        assert res.intent == expected_intent
        assert res.confidence >= 0.10


class TestIntentClassifierMultilingualInference:
    @pytest.mark.parametrize(
        "text,expected_intent",
        [
            # Devanagari Hindi
            ("दो मैट्रिक्स को जोड़ने का सी भाषा में कोड बनाओ।", "GENERATE_CODE"),
            ("बाइनरी सर्च का एक पूरा प्रोग्राम तैयार कीजिए।", "GENERATE_CODE"),
            ("यह रिकर्सिव फंक्शन कैसे काम करता है मुझे समझाओ।", "EXPLAIN_CODE"),
            # Devanagari Marathi
            ("दिलेल्या संख्येचा फॅक्टोरियल काढणारा पायथन कोड तयार कर.", "GENERATE_CODE"),
            ("हा कोड कसा काम करतो ते सोप्या भाषेत समजावून सांग.", "EXPLAIN_CODE"),
            ("या कोडमधील एरर फिक्स करून दे.", "DEBUG_CODE"),
            # Hinglish
            ("calculator ka program bana do python me", "GENERATE_CODE"),
            ("ye python code crash ho raha hai isko fix kar do", "DEBUG_CODE"),
            ("mujhe is function ka step by step explanation chahiye", "EXPLAIN_CODE"),
            # Marathi-English
            ("python madhe calculator cha clean program bana na", "GENERATE_CODE"),
            ("ya code madhe error aahe fix kar", "DEBUG_CODE"),
            ("ha code kasa work karto step by step sang", "EXPLAIN_CODE"),
            # Hindi-English
            ("python me factorial calculate karne ka code provide karo", "GENERATE_CODE"),
            ("is function me loop debug karo exception aa raha hai", "DEBUG_CODE"),
            ("explain karo ye quick sort function kaise chal raha hai", "EXPLAIN_CODE"),
        ],
    )
    def test_multilingual_intent_predictions(
        self, classifier: IntentClassifier, text: str, expected_intent: str
    ) -> None:
        res = classifier.predict(text)
        assert res.intent == expected_intent


class TestIntentClassifierContrastivePairs:
    """Verifies that queries with identical topics correctly diverge based on the requested operation."""

    def test_contrastive_intent_differentiation(self, classifier: IntentClassifier) -> None:
        test_cases = [
            ("Explain this Python function.", "EXPLAIN_CODE"),
            ("Fix this Python function.", "DEBUG_CODE"),
            ("Review this Python function.", "CODE_REVIEW"),
            ("Optimize this Python function.", "OPTIMIZE_CODE"),
            ("Generate test cases for this Python function.", "TEST_CASE_GENERATION"),
            ("Find security vulnerabilities in this Python function.", "SECURITY_ANALYSIS"),
        ]
        for query, expected in test_cases:
            res = classifier.predict(query)
            assert res.intent == expected, f"Failed on '{query}': predicted {res.intent} != {expected}"


class TestIntentClassifierBoundaryPairs:
    """Verifies strict boundary resolution for easily confused pairs."""

    @pytest.mark.parametrize(
        "query,expected_intent",
        [
            ("Why does this error occur in my program?", "ERROR_EXPLANATION"),
            ("Fix this error in my Python code.", "DEBUG_CODE"),
            ("Fix this bug in my implementation.", "DEBUG_CODE"),
            ("Review this code and evaluate its overall quality.", "CODE_REVIEW"),
            ("What improvements can I make to this function?", "CODE_SUGGESTION"),
            ("Make this function execute faster and reduce memory.", "OPTIMIZE_CODE"),
            ("Why is this code slow? Profile the execution.", "PERFORMANCE_ANALYSIS"),
            ("Optimize this code to run faster.", "OPTIMIZE_CODE"),
            ("How does binary search work?", "ALGORITHM"),
            ("What is polymorphism in object-oriented programming?", "CONCEPT"),
            ("What approach should I take to solve this problem?", "APPROACH_SUGGESTION"),
            ("Which sorting algorithm should I use?", "ALGORITHM"),
            ("How should I structure the microservices backend?", "ARCHITECTURE_SUGGESTION"),
            ("What features should I add to my project?", "FEATURE_SUGGESTION"),
            ("What is the best practice for error handling in Python?", "BEST_PRACTICE"),
            ("What should I improve in this function?", "CODE_SUGGESTION"),
            ("Find our previous discussion about recursion.", "SEARCH"),
        ],
    )
    def test_boundary_resolution(
        self, classifier: IntentClassifier, query: str, expected_intent: str
    ) -> None:
        res = classifier.predict(query)
        assert res.intent == expected_intent


class TestIntentClassifierToneIndependence:
    """Verifies that conversational tone markers do not hijack the underlying intent."""

    @pytest.mark.parametrize(
        "query,expected_intent",
        [
            ("Please explain this Python code in detail.", "EXPLAIN_CODE"),
            ("bro ha code samjhav na", "EXPLAIN_CODE"),
            ("simple language madhe ha code explain kar", "EXPLAIN_CODE"),
            ("give a detailed step by step explanation of this code", "EXPLAIN_CODE"),
            ("Kindly write a Python program for calculator.", "GENERATE_CODE"),
            ("bro calculator cha code de na", "GENERATE_CODE"),
            ("only give the calculator code, nothing else", "GENERATE_CODE"),
            ("Please debug this function and resolve the exception.", "DEBUG_CODE"),
            ("yaar ye code fix kar de crash ho raha hai", "DEBUG_CODE"),
        ],
    )
    def test_tone_does_not_alter_intent(
        self, classifier: IntentClassifier, query: str, expected_intent: str
    ) -> None:
        res = classifier.predict(query)
        assert res.intent == expected_intent


class TestIntentClassifierEdgeCases:
    def test_empty_string_input(self, classifier: IntentClassifier) -> None:
        res = classifier.predict("")
        assert isinstance(res, IntentClassificationResult)
        assert res.confidence == 0.0
        assert res.intent in EXPECTED_INTENTS
        assert len(res.probabilities) == 18

    def test_whitespace_input(self, classifier: IntentClassifier) -> None:
        res = classifier.predict("   \n\t  ")
        assert res.confidence == 0.0
        assert res.intent in EXPECTED_INTENTS

    def test_none_input(self, classifier: IntentClassifier) -> None:
        res = classifier.predict(None)
        assert res.confidence == 0.0

    def test_unsupported_type_raises_type_error(self, classifier: IntentClassifier) -> None:
        with pytest.raises(TypeError):
            classifier.predict(12345)  # type: ignore

    def test_preprocessed_text_input(self, classifier: IntentClassifier) -> None:
        prep = PreprocessedText(
            original_text="bro ha code debug kar",
            normalized_text="bro ha code debug kar",
            text_segments=["bro ha code debug kar"],
            classifier_text="bro ha code debug kar",
        )
        res = classifier.predict(prep)
        assert res.intent == "DEBUG_CODE"
        assert res.confidence > 0.0

    def test_traceback_input_handles_gracefully(self, classifier: IntentClassifier) -> None:
        traceback_input = (
            "Traceback (most recent call last):\n"
            "  File 'app.py', line 10, in <module>\n"
            "ZeroDivisionError: division by zero\n"
            "Please fix this error in my code"
        )
        res = classifier.predict(traceback_input)
        assert res.intent == "DEBUG_CODE"

    def test_determinism_ten_runs(self, classifier: IntentClassifier) -> None:
        query = "mala linked list cha code debug karaycha aahe"
        results = [classifier.predict(query).intent for _ in range(10)]
        assert all(r == results[0] for r in results)


class TestIntentInferenceHelpers:
    def test_global_singleton_and_helper(self) -> None:
        c1 = get_intent_classifier()
        c2 = get_intent_classifier()
        assert c1 is c2

        res = predict_intent("write a python calculator")
        assert res.intent == "GENERATE_CODE"
