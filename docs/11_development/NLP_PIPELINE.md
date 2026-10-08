# NLP Pipeline Integration Guide (T14)

## 1. Purpose

The Bhasha2Code NLP Pipeline integrates the completed NLP modules into a single, deterministic, offline, and reusable pipeline:
- **T08 Text Preprocessing**: Unicode NFC composition, line endings, code isolation.
- **T09 Language Detection**: Deterministic rule-based conversational language classification.
- **T11 Tone Classification**: Multi-class communication tone classification.
- **T13 Intent Classification**: Multi-class user intent classification.

The output is a single unified `NLPPipelineResult` model consumed by downstream modules (Context Manager, Prompt Builder, Local LLM).

---

## 2. Architecture & Data Flow

```text
                         Raw User Text
                              │
                              ▼
                     ┌──────────────────┐
                     │ TextPreprocessor │ (T08)
                     └────────┬─────────┘
                              │
                       PreprocessedText
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
    ┌──────────────────┐            ┌────────────────────────┐
    │ LanguageDetector │ (T09)      │ select_classifier_text │
    └─────────┬────────┘            └───────────┬────────────┘
              │                                 │
    LanguageDetectionResult              Classifier Text
              │                                 │
              │                      ┌──────────┴──────────┐
              │                      ▼                     ▼
              │            ┌────────────────┐    ┌──────────────────┐
              │            │ ToneClassifier │    │ IntentClassifier │
              │            └───────┬────────┘    └────────┬─────────┘
              │                    │ (T11)                │ (T13)
              │                    ▼                      ▼
              │          ToneClassificationResult IntentClassificationResult
              │                    │                      │
              └────────────────────┼──────────────────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ NLPPipelineResult │
                         └───────────────────┘
```

---

## 3. Module Responsibilities

| Stage | Module | Primary Question / Output | Technique |
|---|---|---|---|
| **T08 Preprocessing** | `TextPreprocessor` | Cleans text, normalizes Unicode NFC, separates natural language from code/tracebacks. | Regex + Unicode NFC + structural analysis |
| **T09 Language** | `LanguageDetector` | *What language or style is being used?* (`ENGLISH`, `HINDI`, `MARATHI`, `HINGLISH`, `MARATHI_ENGLISH`, `HINDI_ENGLISH`, `UNKNOWN`) | Deterministic lexical rules + script analysis |
| **T11 Tone** | `ToneClassifier` | *How should the response sound?* (`CASUAL`, `FORMAL`, `SIMPLE`, `TECHNICAL`, `SHORT`, `DETAILED`) | TF-IDF (word 1-2 + char 3-5) + Logistic Regression |
| **T13 Intent** | `IntentClassifier` | *What does the user want done?* (18 intent labels) | TF-IDF (word 1-2 + char 3-5) + Logistic Regression |
| **T14 Orchestration** | `NLPPipeline` | Coordinates sequential execution, selects classifier text, and formats unified output. | Pure Python application orchestrator |

---

## 4. Classifier Text Selection

To prevent code snippets, stack traces, and formatting tokens from distorting language detection, tone, or intent:

1. **Natural-Language Precedence**: When natural language text segments exist (e.g. before or after code fences), only those segments are passed to the tone and intent classifiers.
2. **Code Isolation**: Attached code blocks (e.g., `def add(a, b): return a + b`) do not skew language to English or distort user intent.
3. **Code-Only Fallback**: When an inquiry consists entirely of code without conversational text:
   - Language is classified as `Language.UNKNOWN` (confidence 0.10).
   - Classifiers evaluate the code content safely without raising exceptions, returning valid predictions with low confidence.

---

## 5. Model Loading & Lifecycle

- **Offline**: Zero network calls or external APIs required.
- **Eager Validation**: On pipeline instantiation, verifies that both model artifacts exist on disk:
  - `models/tone/tone_classifier.joblib` (1.3 MB)
  - `models/intent/intent_classifier.joblib` (3.9 MB)
  Missing or corrupted files fail immediately with `FileNotFoundError` or `ValueError`.
- **Cached Singleton**: `get_nlp_pipeline()` caches the initialized pipeline globally, avoiding repetitive multi-megabyte model deserialization on each incoming message.

---

## 6. Unified Result Schema

Implemented in `backend/app/nlp/pipeline/schemas.py`:

```python
class NLPPipelineResult(BaseModel):
    preprocessed_text: PreprocessedText
    language: LanguageDetectionResult
    tone: ToneClassificationResult
    intent: IntentClassificationResult

    @property
    def raw_text(self) -> str
    @property
    def normalized_text(self) -> str
    @property
    def has_code(self) -> bool
    @property
    def detected_language(self) -> str
    @property
    def detected_tone(self) -> str
    @property
    def detected_intent(self) -> str

    def to_dict(self) -> dict
```

Each stage retains its native calibrated confidence score:
- `language.confidence`: Linguistic evidence ratio ($0.0 \dots 1.0$)
- `tone.confidence`: Logistic regression softmax probability ($0.0 \dots 1.0$)
- `intent.confidence`: Logistic regression softmax probability ($0.0 \dots 1.0$)

---

## 7. Edge Cases & Robustness

- **Empty / Whitespace Input (`""`, `"   "`)**: Returns valid result with `is_empty=True`, `Language.UNKNOWN`, and zero-confidence safe fallbacks (`Tone.SIMPLE`, `Intent.CONCEPT`).
- **None Input**: Safely treated as empty input.
- **Punctuation / Numeric Only**: Language outputs `UNKNOWN`; classifiers return baseline predictions without crashing.
- **Traceback Queries**: Natural language question takes precedence; tracebacks are extracted as technical context for downstream tools.
- **Unsupported Types**: Raises descriptive `TypeError` if input is not `str`, `PreprocessedText`, or `None`.

---

## 8. Determinism & Performance

- **Determinism**: 10 repeated executions on identical inputs produce byte-for-byte identical results across all four stages.
- **Throughput**: ~200 queries/second (> 200 ms total for 100 sequential requests, ~4.9 ms average per query) on a single standard CPU thread.

---

## 9. Usage Examples

```python
from backend.app.nlp.pipeline import get_nlp_pipeline, analyze_text

# 1. Using convenience function
result = analyze_text("mala ha code simple madhe explain kar")

print(result.detected_language)  # "MARATHI_ENGLISH"
print(result.detected_tone)      # "SIMPLE"
print(result.detected_intent)    # "EXPLAIN_CODE"
print(result.has_code)           # False

# 2. Using loaded pipeline instance
pipeline = get_nlp_pipeline()
result = pipeline.analyze("bro ha code debug kar na")
print(result.to_dict())
```

---

## 10. Future Integration Flow

The NLP Pipeline produces the structured input for downstream components:

```text
User Message
     ↓
NLP Pipeline (T14)
     ↓
Context Manager (T15)
     ↓
Prompt Builder
     ↓
Local Ollama Model
     ↓
Response Engine
```
