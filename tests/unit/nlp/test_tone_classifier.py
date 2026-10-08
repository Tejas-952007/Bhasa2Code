import json
import math
import os
import pytest
from typing import Dict

from backend.app.nlp.schemas import PreprocessedText, Tone, ToneClassificationResult
from backend.app.nlp.tone_classification.inference import get_tone_classifier, predict_tone
from backend.app.nlp.tone_classification.tone_classifier import ToneClassifier

MODEL_PATH = os.path.join("models", "tone", "tone_classifier.joblib")
METADATA_PATH = os.path.join("models", "tone", "metadata.json")

EXPECTED_TONES = {"CASUAL", "FORMAL", "SIMPLE", "TECHNICAL", "SHORT", "DETAILED"}


@pytest.fixture
def classifier() -> ToneClassifier:
    return ToneClassifier(model_path=MODEL_PATH)


class TestToneModelArtifacts:
    def test_model_artifact_exists(self) -> None:
        assert os.path.exists(MODEL_PATH), f"Model artifact missing at {MODEL_PATH}"
        assert os.path.getsize(MODEL_PATH) > 1000

    def test_metadata_artifact_exists_and_valid(self) -> None:
        assert os.path.exists(METADATA_PATH), f"Metadata file missing at {METADATA_PATH}"
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)

        assert meta["task"] == "tone_classification"
        assert meta["model"] == "tfidf_logistic_regression"
        assert set(meta["labels"]) == EXPECTED_TONES
        assert meta["train_samples"] == 420
        assert meta["validation_samples"] == 90
        assert meta["test_samples"] == 90
        assert meta["metrics"]["validation"]["accuracy"] >= 0.80
        assert meta["metrics"]["validation"]["macro_f1"] >= 0.80
        assert meta["metrics"]["test"]["accuracy"] >= 0.78
        assert meta["metrics"]["test"]["macro_f1"] >= 0.78


class TestToneClassifierSchema:
    def test_prediction_schema_and_types(self, classifier: ToneClassifier) -> None:
        res = classifier.predict("Please explain this function in detail.")
        assert isinstance(res, ToneClassificationResult)
        assert res.tone in EXPECTED_TONES
        assert 0.0 <= res.confidence <= 1.0
        assert isinstance(res.probabilities, dict)
        assert set(res.probabilities.keys()) == EXPECTED_TONES

        # Sum of probabilities should be approximately 1.0
        prob_sum = sum(res.probabilities.values())
        assert math.isclose(prob_sum, 1.0, abs_tol=1e-3)

    def test_to_dict_serialization(self, classifier: ToneClassifier) -> None:
        res = classifier.predict("bro check this code")
        d = res.to_dict()
        assert d["tone"] == res.tone
        assert "confidence" in d
        assert "probabilities" in d
        assert set(d["probabilities"].keys()) == EXPECTED_TONES


class TestToneClassifierMultilingualInference:
    @pytest.mark.parametrize(
        "text,expected_tone",
        [
            ("Please explain the architecture of this module.", "FORMAL"),
            ("कृपया इस फंक्शन के कार्यप्रणाली की व्याख्या करें।", "FORMAL"),
            ("कृपया या पायथन फंक्शनच्या कार्यपद्धतीचे स्पष्टीकरण द्यावे.", "FORMAL"),
            ("bro can you check why my python loop is infinite", "CASUAL"),
            ("अरे भाई यह कोड बार-बार क्रैश क्यों हो रहा है", "CASUAL"),
            ("अरे भावा हा पायथन कोड का क्रॅश होतोय बघ ना", "CASUAL"),
            ("fakt answer de", "SHORT"),
            ("बस कोड दीजिए, कोई व्याख्या नहीं।", "SHORT"),
            ("फक्त कोड दे, बाकी काहीही नको.", "SHORT"),
            ("Explain this recursion concept using very simple words for a beginner.", "SIMPLE"),
            ("इस रिकर्शन को बिल्कुल आसान और सरल शब्दों में समझाओ।", "SIMPLE"),
            ("हा रिकर्शन संकल्पना अगदी सोप्या भाषेत नवशिक्यासाठी समजावून सांग.", "SIMPLE"),
            ("Analyze the algorithmic time and space complexity with formal Big-O proofs.", "TECHNICAL"),
            ("इस एल्गोरिदम की समय और स्थान जटिलता का औपचारिक बिग-ओ विश्लेषण प्रस्तुत करें।", "TECHNICAL"),
            ("Explain this code step by step with complete details and examples.", "DETAILED"),
            ("इस कोड को हर एक स्टेप के साथ पूरी तरह विस्तार से उदाहरण सहित समझाओ।", "DETAILED"),
        ],
    )
    def test_multilingual_tone_predictions(
        self, classifier: ToneClassifier, text: str, expected_tone: str
    ) -> None:
        res = classifier.predict(text)
        assert res.tone == expected_tone
        assert res.confidence >= 0.30


class TestToneClassifierBoundaryCases:
    @pytest.mark.parametrize(
        "text,expected_tone",
        [
            ("bro explain this code", "CASUAL"),
            ("bro explain this code in detail", "DETAILED"),
            ("simple language madhe explain kar", "SIMPLE"),
            ("technical explanation with time complexity de", "TECHNICAL"),
            ("fakt answer de", "SHORT"),
            ("Please provide a professional explanation", "FORMAL"),
            ("bro हा code detail madhe samjhav", "DETAILED"),
            ("mujhe simple language me samjhao", "SIMPLE"),
            ("कृपया याचे व्यावसायिक स्पष्टीकरण द्या", "FORMAL"),
            ("बस code दे", "SHORT"),
        ],
    )
    def test_tone_boundary_contrastive_pairs(
        self, classifier: ToneClassifier, text: str, expected_tone: str
    ) -> None:
        res = classifier.predict(text)
        assert res.tone == expected_tone


class TestToneClassifierEdgeCases:
    def test_empty_string(self, classifier: ToneClassifier) -> None:
        res = classifier.predict("")
        assert res.confidence == 0.0
        assert len(res.probabilities) == 6

    def test_whitespace_string(self, classifier: ToneClassifier) -> None:
        res = classifier.predict("   \n\t  ")
        assert res.confidence == 0.0

    def test_none_input(self, classifier: ToneClassifier) -> None:
        res = classifier.predict(None)
        assert res.confidence == 0.0

    def test_unsupported_type_raises_type_error(self, classifier: ToneClassifier) -> None:
        with pytest.raises(TypeError):
            classifier.predict(12345)  # type: ignore

    def test_preprocessed_text_input(self, classifier: ToneClassifier) -> None:
        prep = PreprocessedText(
            original_text="bro check this code",
            normalized_text="bro check this code",
            text_segments=["bro check this code"],
            code_segments=[],
            classifier_text="bro check this code",
            is_empty=False,
        )
        res = classifier.predict(prep)
        assert res.tone == "CASUAL"

    def test_missing_model_file_raises_error(self) -> None:
        with pytest.raises(FileNotFoundError):
            ToneClassifier.load("models/non_existent_tone_model.joblib")


class TestToneClassifierDeterminism:
    def test_repeated_runs_identical_results(self, classifier: ToneClassifier) -> None:
        test_inputs = [
            "Please provide a formal explanation of this method.",
            "bro ha code check kar na",
            "simple language madhe samjhav",
            "step by step detail madhe explain kar",
            "fakt answer de",
        ]
        for query in test_inputs:
            runs = [classifier.predict(query) for _ in range(10)]
            first = runs[0]
            for r in runs[1:]:
                assert r.tone == first.tone
                assert math.isclose(r.confidence, first.confidence, abs_tol=1e-6)
                for k in EXPECTED_TONES:
                    assert math.isclose(r.probabilities[k], first.probabilities[k], abs_tol=1e-6)


class TestToneClassifierInferenceModule:
    def test_get_tone_classifier_and_predict_tone(self) -> None:
        c1 = get_tone_classifier()
        c2 = get_tone_classifier()
        assert c1 is c2

        res = predict_tone("Kindly provide an explanation of this function.")
        assert res.tone == "FORMAL"
        assert res.confidence >= 0.40
