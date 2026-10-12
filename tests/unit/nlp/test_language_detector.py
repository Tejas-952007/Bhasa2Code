import pytest

from backend.app.nlp.language_detection.language_detector import LanguageDetector
from backend.app.nlp.language_detection.schemas import Language, LanguageDetectionResult
from backend.app.nlp.preprocessing.text_preprocessor import TextPreprocessor


@pytest.fixture
def detector() -> LanguageDetector:
    return LanguageDetector()


@pytest.fixture
def preprocessor() -> TextPreprocessor:
    return TextPreprocessor()


class TestLanguageDetectorEnglish:
    @pytest.mark.parametrize(
        "text",
        [
            "write a python program for calculator",
            "Write a Python program for calculator",
            "explain this function",
            "how does binary search work",
            "Explain this function in detail",
        ],
    )
    def test_english_queries(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.ENGLISH
        assert result.confidence >= 0.90
        assert len(result.evidence) > 0


class TestLanguageDetectorHindi:
    @pytest.mark.parametrize(
        "text",
        [
            "मुझे यह कोड समझ नहीं आ रहा",
            "कृपया इस प्रोग्राम को समझाओ",
        ],
    )
    def test_hindi_native(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.HINDI
        assert result.confidence >= 0.90
        assert any("Hindi" in e for e in result.evidence)

    @pytest.mark.parametrize(
        "text",
        [
            "mujhe code samajh nahi aa raha",
            "mujhe ye code samajh nahi aa raha",
            "ye program samjha do",
        ],
    )
    def test_hindi_latin(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.HINDI
        assert result.confidence >= 0.90


class TestLanguageDetectorMarathi:
    @pytest.mark.parametrize(
        "text",
        [
            "मला हा कोड समजत नाही",
            "हा प्रोग्राम समजावून सांग",
        ],
    )
    def test_marathi_native(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.MARATHI
        assert result.confidence >= 0.90
        assert any("Marathi" in e for e in result.evidence)

    @pytest.mark.parametrize(
        "text",
        [
            "mala code samjat nahi",
            "mala ha code samjat nahi",
            "ha program samjavun sang",
        ],
    )
    def test_marathi_latin(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.MARATHI
        assert result.confidence >= 0.90


class TestLanguageDetectorHinglish:
    @pytest.mark.parametrize(
        "text",
        [
            "mujhe ek python program banana hai",
            "python me ye error kaise fix kare",
            "python me calculator banao",
        ],
    )
    def test_hinglish(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.HINGLISH
        assert result.confidence >= 0.85


class TestLanguageDetectorCodeMixed:
    @pytest.mark.parametrize(
        "text",
        [
            "mala Python function explain kar",
            "ya code madhe error aahe",
            "python madhe calculator bana",
            "mala हा program debug karaycha aahe",
            "मला calculator चा program पाहिजे",
            "mala Python function debug kar",
            "ya code madhe exception aahe",
        ],
    )
    def test_marathi_english(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.MARATHI_ENGLISH
        assert result.confidence >= 0.85

    @pytest.mark.parametrize(
        "text",
        [
            "mujhe Python code explain karo",
            "is function me error aa raha hai",
            "mujhe ye program debug karna hai",
            "मुझे calculator का program चाहिए",
            "mujhe SQL query explain karo",
        ],
    )
    def test_hindi_english(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.HINDI_ENGLISH
        assert result.confidence >= 0.85


class TestLanguageDetectorTechnicalBias:
    @pytest.mark.parametrize(
        "text,expected_lang",
        [
            ("mala Python function debug kar", Language.MARATHI_ENGLISH),
            ("mujhe SQL query explain karo", Language.HINDI_ENGLISH),
            ("ya code madhe exception aahe", Language.MARATHI_ENGLISH),
        ],
    )
    def test_technical_words_do_not_dominate(
        self,
        detector: LanguageDetector,
        text: str,
        expected_lang: Language,
    ) -> None:
        result = detector.detect(text)
        assert result.language != Language.ENGLISH
        assert result.language == expected_lang


class TestLanguageDetectorCodeAndTracebacks:
    def test_code_only(self, detector: LanguageDetector) -> None:
        code_input = "def add(a, b):\n    return a + b"
        result = detector.detect(code_input)
        assert result.language == Language.UNKNOWN
        assert result.confidence <= 0.20

    def test_single_line_code_only(self, detector: LanguageDetector) -> None:
        result = detector.detect("def add(a, b): return a+b")
        assert result.language == Language.UNKNOWN
        assert result.confidence <= 0.20

    def test_code_with_marathi(self, detector: LanguageDetector) -> None:
        text = "mala ha code explain kar\n\ndef add(a, b):\n    return a + b"
        result = detector.detect(text)
        assert result.language == Language.MARATHI
        assert result.confidence >= 0.85

    def test_code_with_hindi(self, detector: LanguageDetector) -> None:
        text = "mujhe ye code samjhao\n\ndef add(a, b):\n    return a + b"
        result = detector.detect(text)
        assert result.language == Language.HINDI
        assert result.confidence >= 0.85

    def test_marathi_with_traceback(self, detector: LanguageDetector) -> None:
        text = (
            "mala ha error ka aahe?\n\n"
            "Traceback (most recent call last):\n"
            '  File "app.py", line 10\n'
            "  ValueError: invalid input"
        )
        result = detector.detect(text)
        assert result.language == Language.MARATHI
        assert result.confidence >= 0.85


class TestLanguageDetectorNoiseAndLowInformation:
    @pytest.mark.parametrize(
        "text",
        [
            "",
            "   ",
            "123456",
            "!!! ???",
            "/home/user/project",
            "https://example.com",
        ],
    )
    def test_low_information_inputs(self, detector: LanguageDetector, text: str) -> None:
        result = detector.detect(text)
        assert result.language == Language.UNKNOWN
        assert result.confidence <= 0.20

    def test_none_input(self, detector: LanguageDetector) -> None:
        result = detector.detect(None)
        assert result.language == Language.UNKNOWN
        assert result.confidence == 0.0


class TestLanguageDetectorPreprocessedTextContract:
    def test_consumes_preprocessed_text_directly(
        self,
        detector: LanguageDetector,
        preprocessor: TextPreprocessor,
    ) -> None:
        preprocessed = preprocessor.preprocess("मला calculator चा program पाहिजे")
        result = detector.detect(preprocessed)
        assert isinstance(result, LanguageDetectionResult)
        assert result.language == Language.MARATHI_ENGLISH
        assert result.confidence >= 0.90


class TestLanguageDetectorDeterminism:
    def test_repeated_runs_are_deterministic(self, detector: LanguageDetector) -> None:
        sample_queries = [
            "Write a Python program for calculator",
            "मला calculator चा program पाहिजे",
            "mujhe code samajh nahi aa raha",
            "def add(a, b): return a + b",
            "python madhe calculator bana",
        ]
        for query in sample_queries:
            results = [detector.detect(query) for _ in range(5)]
            first = results[0]
            for r in results[1:]:
                assert r.language == first.language
                assert r.confidence == first.confidence
                assert r.evidence == first.evidence
