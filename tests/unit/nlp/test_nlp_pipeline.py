"""Unit and integration tests for the unified Bhasha2Code NLP Pipeline (T14).

Verifies:
- End-to-end sequential execution: Preprocessing -> Language -> Tone -> Intent
- Unified schema conformance and accessors
- All 9 required canonical validation examples
- Multilingual coverage (English, Hindi, Marathi, Hinglish, Marathi-English, Hindi-English)
- Code handling (code-only, mixed code + text, traceback + text)
- Edge-case handling (None, empty, whitespace, punctuation, numbers, invalid types)
- Determinism across repeated calls (10 runs)
- Model loading lifecycle (valid, missing, corrupted)
- Cross-component consistency & isolation (matching direct detector/classifier outputs)
"""

import math
import os
import tempfile
from typing import Union
import pytest

from backend.app.nlp.intent_classification import IntentClassifier, predict_intent
from backend.app.nlp.language_detection import LanguageDetector
from backend.app.nlp.pipeline import (
    NLPPipeline,
    NLPPipelineResult,
    analyze_text,
    get_nlp_pipeline,
    select_classifier_text,
)
from backend.app.nlp.preprocessing import TextPreprocessor
from backend.app.nlp.schemas import (
    Intent,
    IntentClassificationResult,
    Language,
    LanguageDetectionResult,
    PreprocessedText,
    Tone,
    ToneClassificationResult,
)
from backend.app.nlp.tone_classification import ToneClassifier, predict_tone


@pytest.fixture
def pipeline() -> NLPPipeline:
    return NLPPipeline.load_default()


class TestNLPPipelineBasicFlow:
    def test_pipeline_executes_all_four_stages(self, pipeline: NLPPipeline) -> None:
        query = "mala ha code simple madhe explain kar"
        result = pipeline.analyze(query)

        assert isinstance(result, NLPPipelineResult)

        # Stage 1: PreprocessedText
        assert isinstance(result.preprocessed_text, PreprocessedText)
        assert result.raw_text == query
        assert result.normalized_text == query
        assert not result.has_code

        # Stage 2: LanguageDetectionResult
        assert isinstance(result.language, LanguageDetectionResult)
        assert result.detected_language in [lang.value for lang in Language]
        assert 0.0 <= result.language.confidence <= 1.0

        # Stage 3: ToneClassificationResult
        assert isinstance(result.tone, ToneClassificationResult)
        assert result.detected_tone in [t.value for t in Tone]
        assert 0.0 <= result.tone.confidence <= 1.0
        assert math.isclose(sum(result.tone.probabilities.values()), 1.0, abs_tol=1e-3)

        # Stage 4: IntentClassificationResult
        assert isinstance(result.intent, IntentClassificationResult)
        assert result.detected_intent in [i.value for i in Intent]
        assert 0.0 <= result.intent.confidence <= 1.0
        assert math.isclose(sum(result.intent.probabilities.values()), 1.0, abs_tol=1e-3)

    def test_to_dict_serialization(self, pipeline: NLPPipeline) -> None:
        query = "bro ha code debug kar na"
        result = pipeline.analyze(query)
        d = result.to_dict()

        assert "preprocessed_text" in d
        assert "language" in d
        assert "tone" in d
        assert "intent" in d
        assert d["preprocessed_text"]["original_text"] == query
        assert d["language"]["language"] == result.detected_language
        assert d["tone"]["tone"] == result.detected_tone
        assert d["intent"]["intent"] == result.detected_intent

    def test_callable_interface(self, pipeline: NLPPipeline) -> None:
        query = "write a python calculator"
        res1 = pipeline.analyze(query)
        res2 = pipeline(query)
        assert res1.detected_intent == res2.detected_intent
        assert res1.detected_tone == res2.detected_tone


class TestNLPPipelineCanonicalValidationExamples:
    """Tests the 9 canonical user interaction patterns specified in T14 requirements."""

    def test_example_1_marathi_english_explanation(self, pipeline: NLPPipeline) -> None:
        # Example 1: Marathi-English explanation
        query = "mala ha code simple madhe explain kar"
        res = pipeline.analyze(query)
        assert res.detected_language == "MARATHI_ENGLISH"
        assert res.detected_tone == "SIMPLE"
        assert res.detected_intent == "EXPLAIN_CODE"

    def test_example_2_hindi_debugging(self, pipeline: NLPPipeline) -> None:
        # Example 2: Hindi debugging
        query = "mujhe ye Python code fix karna hai"
        res = pipeline.analyze(query)
        assert res.detected_language in ["HINDI", "HINDI_ENGLISH"]
        assert res.detected_intent == "DEBUG_CODE"

    def test_example_3_casual_debugging(self, pipeline: NLPPipeline) -> None:
        # Example 3: Casual debugging
        query = "bro ha code debug kar na"
        res = pipeline.analyze(query)
        assert res.detected_tone == "CASUAL"
        assert res.detected_intent == "DEBUG_CODE"

    def test_example_4_technical_optimization(self, pipeline: NLPPipeline) -> None:
        # Example 4: Technical optimization
        query = "Analyze the algorithmic complexity and optimize this implementation."
        res = pipeline.analyze(query)
        assert res.detected_tone in ["TECHNICAL", "FORMAL"]
        assert res.detected_intent == "OPTIMIZE_CODE"

    def test_example_5_short_code_generation(self, pipeline: NLPPipeline) -> None:
        # Example 5: Short code request
        query = "fakt code de"
        res = pipeline.analyze(query)
        assert res.detected_tone == "SHORT"
        assert res.detected_intent == "GENERATE_CODE"

    def test_example_6_architecture_suggestion(self, pipeline: NLPPipeline) -> None:
        # Example 6: Architecture query
        query = "FastAPI React project architecture suggest kar"
        res = pipeline.analyze(query)
        assert res.detected_intent == "ARCHITECTURE_SUGGESTION"

    def test_example_7_search_request(self, pipeline: NLPPipeline) -> None:
        # Example 7: Search request
        query = "find my previous Python code"
        res = pipeline.analyze(query)
        assert res.detected_language == "ENGLISH"
        assert res.detected_intent == "SEARCH"

    def test_example_8_code_plus_marathi_error(self, pipeline: NLPPipeline) -> None:
        # Example 8: Code + Marathi traceback
        query = (
            "mala ha error ka aahe?\n\n"
            "Traceback:\n"
            "ValueError: invalid input"
        )
        res = pipeline.analyze(query)
        assert res.detected_intent == "ERROR_EXPLANATION"
        assert "MARATHI" in res.detected_language

    def test_example_9_code_only_input(self, pipeline: NLPPipeline) -> None:
        # Example 9: Code-only
        query = "def add(a, b):\n    return a + b"
        res = pipeline.analyze(query)
        assert res.detected_language == "UNKNOWN"
        assert res.has_code
        assert res.detected_tone in [t.value for t in Tone]
        assert res.detected_intent in [i.value for i in Intent]


class TestNLPPipelineMultilingualCoverage:
    @pytest.mark.parametrize(
        "query,expected_lang,expected_intent",
        [
            ("Write a Python script to calculate prime numbers.", "ENGLISH", "GENERATE_CODE"),
            ("दो मैट्रिक्स को जोड़ने का सी भाषा में कोड बनाओ।", "HINDI", "GENERATE_CODE"),
            ("दिलेल्या संख्येचा फॅक्टोरियल काढणारा पायथन कोड तयार कर.", "MARATHI", "GENERATE_CODE"),
            ("calculator ka program bana do python me", "HINGLISH", "GENERATE_CODE"),
            ("python madhe calculator cha clean program bana na", "MARATHI_ENGLISH", "GENERATE_CODE"),
            ("python me factorial calculate karne ka code provide karo", ["HINGLISH", "HINDI_ENGLISH"], "GENERATE_CODE"),
        ],
    )
    def test_multilingual_queries(
        self,
        pipeline: NLPPipeline,
        query: str,
        expected_lang: Union[str, list],
        expected_intent: str,
    ) -> None:
        res = pipeline.analyze(query)
        if isinstance(expected_lang, list):
            assert res.detected_language in expected_lang
        else:
            assert res.detected_language == expected_lang
        assert res.detected_intent == expected_intent


class TestNLPPipelineCodeAndTracebackHandling:
    def test_natural_language_commentary_isolated_from_code(
        self, pipeline: NLPPipeline
    ) -> None:
        query = (
            "mala ha code simple madhe explain kar\n\n"
            "```python\n"
            "def multiply(x, y):\n"
            "    return x * y\n"
            "```"
        )
        res = pipeline.analyze(query)
        assert res.has_code
        assert res.detected_language in ["MARATHI", "MARATHI_ENGLISH"]
        assert res.detected_tone == "SIMPLE"
        assert res.detected_intent == "EXPLAIN_CODE"

    def test_classifier_text_selection_helper(self) -> None:
        prep = TextPreprocessor().preprocess(
            "explain this function\n\n```python\ndef foo(): pass\n```"
        )
        selected = select_classifier_text(prep)
        assert selected == "explain this function"
        assert "def foo" not in selected


class TestNLPPipelineEdgeCases:
    def test_empty_string(self, pipeline: NLPPipeline) -> None:
        res = pipeline.analyze("")
        assert res.preprocessed_text.is_empty
        assert res.detected_language == "UNKNOWN"
        assert res.language.confidence == 0.0
        assert res.tone.confidence == 0.0
        assert res.intent.confidence == 0.0

    def test_whitespace_string(self, pipeline: NLPPipeline) -> None:
        res = pipeline.analyze("   \n\t  ")
        assert res.preprocessed_text.is_empty
        assert res.detected_language == "UNKNOWN"
        assert res.tone.confidence == 0.0
        assert res.intent.confidence == 0.0

    def test_none_input(self, pipeline: NLPPipeline) -> None:
        res = pipeline.analyze(None)
        assert res.preprocessed_text.is_empty
        assert res.detected_language == "UNKNOWN"
        assert res.tone.confidence == 0.0
        assert res.intent.confidence == 0.0

    def test_punctuation_only(self, pipeline: NLPPipeline) -> None:
        res = pipeline.analyze("!@#$%^&*()?")
        assert res.detected_language == "UNKNOWN"
        assert res.detected_tone in [t.value for t in Tone]
        assert res.detected_intent in [i.value for i in Intent]

    def test_numeric_only(self, pipeline: NLPPipeline) -> None:
        res = pipeline.analyze("1234567890 987654321")
        assert res.detected_language == "UNKNOWN"
        assert res.detected_tone in [t.value for t in Tone]
        assert res.detected_intent in [i.value for i in Intent]

    def test_unsupported_type_raises_type_error(self, pipeline: NLPPipeline) -> None:
        with pytest.raises(TypeError) as exc_info:
            pipeline.analyze({"invalid": "type"})  # type: ignore
        assert "Unsupported input type" in str(exc_info.value)

    def test_preprocessed_text_pass_through(self, pipeline: NLPPipeline) -> None:
        tp = TextPreprocessor()
        prep = tp.preprocess("bro ha code debug kar na")
        res = pipeline.analyze(prep)
        assert res.detected_intent == "DEBUG_CODE"
        assert res.detected_tone == "CASUAL"


class TestNLPPipelineDeterminism:
    def test_repeated_calls_produce_identical_results(
        self, pipeline: NLPPipeline
    ) -> None:
        query = "mala binary search cha algorithm samjhav"
        first_res = pipeline.analyze(query)

        for _ in range(9):
            repeat_res = pipeline.analyze(query)
            assert repeat_res.detected_language == first_res.detected_language
            assert repeat_res.language.confidence == first_res.language.confidence
            assert repeat_res.detected_tone == first_res.detected_tone
            assert repeat_res.tone.confidence == first_res.tone.confidence
            assert repeat_res.detected_intent == first_res.detected_intent
            assert repeat_res.intent.confidence == first_res.intent.confidence


class TestNLPPipelineCrossComponentConsistency:
    """Verifies that the orchestrator does not mutate or alter the standalone component outputs."""

    @pytest.mark.parametrize(
        "query",
        [
            "Write a Python program to calculate the factorial of a number.",
            "bro ha code debug kar na",
            "simple language madhe ha code explain kar",
            "find my previous Python code",
        ],
    )
    def test_pipeline_matches_direct_component_calls(
        self, pipeline: NLPPipeline, query: str
    ) -> None:
        prep = pipeline.preprocessor.preprocess(query)

        direct_lang = pipeline.language_detector.detect(prep)
        direct_tone = pipeline.tone_classifier.predict(prep)
        direct_intent = pipeline.intent_classifier.predict(prep)

        pipe_res = pipeline.analyze(query)

        assert pipe_res.detected_language == direct_lang.language.value
        assert pipe_res.language.confidence == direct_lang.confidence
        assert pipe_res.detected_tone == direct_tone.tone
        assert math.isclose(pipe_res.tone.confidence, direct_tone.confidence, abs_tol=1e-5)
        assert pipe_res.detected_intent == direct_intent.intent
        assert math.isclose(pipe_res.intent.confidence, direct_intent.confidence, abs_tol=1e-5)


class TestNLPPipelineModelLoadingAndLifecycle:
    def test_global_singleton_reuse(self) -> None:
        p1 = get_nlp_pipeline()
        p2 = get_nlp_pipeline()
        assert p1 is p2

        res = analyze_text("write a python calculator")
        assert res.detected_intent == "GENERATE_CODE"

    def test_missing_tone_model_raises_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            ToneClassifier(model_path="nonexistent_tone_path.joblib")

    def test_missing_intent_model_raises_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            IntentClassifier(model_path="nonexistent_intent_path.joblib")

    def test_corrupted_model_file_raises_error(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".joblib", delete=False) as f:
            f.write(b"NOT A VALID JOBLIB FILE")
            corrupt_path = f.name

        try:
            with pytest.raises(ValueError):
                ToneClassifier(model_path=corrupt_path)
            with pytest.raises(ValueError):
                IntentClassifier(model_path=corrupt_path)
        finally:
            if os.path.exists(corrupt_path):
                os.remove(corrupt_path)
