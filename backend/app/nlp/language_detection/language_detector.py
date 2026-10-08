from typing import Optional, Union

from backend.app.nlp.language_detection.rules import classify_language
from backend.app.nlp.language_detection.schemas import Language, LanguageDetectionResult
from backend.app.nlp.preprocessing.text_preprocessor import TextPreprocessor
from backend.app.nlp.schemas import PreprocessedText


class LanguageDetector:
    """Deterministic, fully offline conversational language detector for Bhasha2Code.
    
    Identifies:
    - ENGLISH
    - HINDI
    - MARATHI
    - HINGLISH
    - MARATHI_ENGLISH
    - HINDI_ENGLISH
    - UNKNOWN
    
    Consumes PreprocessedText from T08 and isolates natural language inquiries from code.
    """

    def __init__(self, preprocessor: Optional[TextPreprocessor] = None) -> None:
        self.preprocessor = preprocessor or TextPreprocessor()

    def detect(self, input_data: Union[PreprocessedText, str, None]) -> LanguageDetectionResult:
        """Detect conversational language from PreprocessedText or raw string input."""
        # Ensure input is preprocessed
        if input_data is None:
            preprocessed = self.preprocessor.preprocess("")
        elif isinstance(input_data, str):
            preprocessed = self.preprocessor.preprocess(input_data)
        elif isinstance(input_data, PreprocessedText):
            preprocessed = input_data
        else:
            preprocessed = self.preprocessor.preprocess(str(input_data))

        # Check for empty input
        if preprocessed.is_empty:
            return LanguageDetectionResult(
                language=Language.UNKNOWN,
                confidence=0.0,
                evidence=["Empty or whitespace input"],
            )

        # Check for code-only input without natural language
        if preprocessed.has_code and not preprocessed.text_segments:
            return LanguageDetectionResult(
                language=Language.UNKNOWN,
                confidence=0.10,
                evidence=["Code-only input without conversational context"],
            )

        # Extract natural language text primarily
        if preprocessed.text_segments:
            natural_text = " ".join(preprocessed.text_segments)
        else:
            natural_text = preprocessed.classifier_text

        return classify_language(
            natural_text=natural_text,
            has_code_attachment=preprocessed.has_code,
            is_empty_input=preprocessed.is_empty,
        )
