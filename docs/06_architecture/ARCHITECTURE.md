# Bhasha2Code — System Architecture

## Phase 6 — Architecture

**Project:** Bhasha2Code  
**Phase:** 6 — Architecture  
**Version:** 1.0  
**Status:** COMPLETE — READY FOR DESIGN  
**Deployment Target:** Localhost / Offline  
**Backend:** FastAPI  
**Frontend:** React + Vite  
**Database:** SQLite  
**LLM Runtime:** Ollama  
**Default Model:** Qwen2.5-Coder 3B

---

# 1. Purpose

This document defines the technical architecture of Bhasha2Code.

It describes:

- System architecture
- Component architecture
- Data flow
- API flow
- NLP pipeline
- Context management
- LLM interaction
- Code validation
- Debugging loop
- Database architecture
- Sandbox boundaries
- Frontend/backend communication
- Deployment architecture
- Security boundaries

The purpose is to ensure that development happens in a structured way instead of creating disconnected features.

---

# 2. Architecture Principles

The architecture follows these principles:

```text
Local First
     ↓
Modular
     ↓
Simple
     ↓
Testable
     ↓
Secure
     ↓
Replaceable Components
```

Additional rules:

1. Core features must work offline.
2. LLM logic must remain separate from API logic.
3. NLP logic must remain separate from UI logic.
4. Database access must remain separate from business logic.
5. Generated code must never execute directly on the host.
6. Existing architecture must be respected when new features are added.
7. Every major component must be independently testable.

---

# 3. High-Level System Architecture

```text
                           USER
                             │
                             ▼
                    ┌─────────────────┐
                    │   React + Vite  │
                    │    Web UI        │
                    └────────┬────────┘
                             │
                       HTTP / Streaming
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastAPI     │
                    │   API Layer     │
                    └────────┬────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
      ┌────────────┐ ┌──────────────┐ ┌─────────────┐
      │ NLP Engine │ │Context Engine│ │ Session/DB  │
      └─────┬──────┘ └──────┬───────┘ └──────┬──────┘
            │               │                │
            └───────────────┼────────────────┘
                            ▼
                    ┌─────────────────┐
                    │  Prompt Builder │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Ollama      │
                    └────────┬────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │ Qwen2.5-Coder 3B       │
                │ Local Coding LLM       │
                └────────────┬───────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Response Engine │
                    └────────┬────────┘
                             │
                ┌────────────┴─────────────┐
                │                          │
                ▼                          ▼
       ┌─────────────────┐        ┌────────────────┐
       │ Code Validation │        │ Study / Format │
       └────────┬────────┘        └───────┬────────┘
                │                         │
                └────────────┬────────────┘
                             ▼
                          Response
                             │
                             ▼
                       React Frontend
```

---

# 4. Major Components

The system is divided into the following major components:

```text
1. Frontend
2. API Layer
3. NLP Engine
4. Context Engine
5. Prompt Builder
6. LLM Service
7. Response Engine
8. Code Engine
9. Validation Engine
10. Sandbox
11. Session Manager
12. Study Engine
13. Export Engine
14. Database
15. Logging / Monitoring
```

---

# 5. Component Responsibilities

## 5.1 Frontend

Technology:

```text
React + Vite
```

Responsibilities:

- Chat UI
- Session sidebar
- Code editor
- Message rendering
- Streaming responses
- Saved messages
- Notes
- Study Mode
- Search
- PDF export controls
- Settings
- Error messages

Frontend must not directly communicate with Ollama or the database.

All backend interaction should happen through FastAPI.

---

# 6. API Layer

Technology:

```text
FastAPI
```

Responsibilities:

- Request validation
- Authentication/session identification where applicable
- Routing
- Service orchestration
- Response streaming
- Error handling
- Health checks

The API layer should not contain heavy NLP/LLM implementation logic.

---

# 7. Service Layer

The API should call application services rather than implementing business logic inside route functions.

Example:

```text
API Route
   ↓
Service
   ↓
NLP / Context / LLM / DB
```

Potential services:

```text
ChatService
SessionService
ValidationService
DebugService
StudyService
ExportService
SearchService
SuggestionService
```

---

# 8. NLP Engine

The NLP Engine converts raw user text into structured metadata.

Pipeline:

```text
Raw User Input
      ↓
Preprocessing
      ↓
Language Detection
      ↓
Tone Detection
      ↓
Intent Detection
      ↓
Programming Language Detection
      ↓
Requirement Extraction
      ↓
NLP Result
```

Example NLP result:

```json
{
  "language": "MARATHI_ENGLISH",
  "tone": "CASUAL",
  "intent": "GENERATE_CODE",
  "programming_language": "PYTHON",
  "task": "calculator",
  "confidence": 0.91
}
```

---

# 9. NLP Preprocessing

Implemented in `backend/app/nlp/preprocessing/text_preprocessor.py`.

Preprocessing operations:
- **Unicode NFC Normalization**: Canonical composition preserving Devanagari (Marathi, Hindi), Latin, technical symbols, and emoji.
- **Canonical Line Endings**: Converts `\r\n` and `\r` to `\n`.
- **Harmless Whitespace Normalization**: Collapses repeated internal spaces while strictly preserving code indentation and multi-line structures.
- **Code Boundary Preservation**: Extracts Markdown fenced blocks (```` ``` ````, `~~~`) and detects unfenced raw code/stack traces without altering indentation or newlines.
- **Multilingual Preservation**: Does NOT translate, stem, or lowercase mixed-language text.

### Preprocessing Schema (`backend/app/nlp/schemas.py`):

```python
class CodeSegment(BaseModel):
    content: str
    language_hint: Optional[str] = None

class PreprocessedText(BaseModel):
    original_text: str
    normalized_text: str
    text_segments: List[str]
    code_segments: List[CodeSegment]
    classifier_text: str
    is_empty: bool
```

Guarantees:
- **Idempotent**: `preprocess(preprocess(text).normalized_text).normalized_text == preprocess(text).normalized_text`
- **Deterministic**: Identical inputs yield identical outputs.
- **Non-destructive**: Preserves `original_text` for context and debugging.

---

# 10. Language Detection

Implemented in `backend/app/nlp/language_detection/language_detector.py`.

The Language Detection component determines the conversational language from the normalized output of Text Preprocessing (`PreprocessedText`).

### Pipeline Architecture:

```text
PreprocessedText
      ↓
LanguageDetector
      ├── Script Analysis (Devanagari vs Latin characters)
      ├── Lexical Analysis (Native Devanagari Hindi & Marathi)
      ├── Transliteration Detection (Latin Hindi & Marathi)
      ├── Technical Vocabulary Filtering (Neutral programming terms)
      └── Mixed-Language Decision (Homograph resolution & code-mixing)
      ↓
LanguageDetectionResult
```

### Supported Labels:
- `ENGLISH`: Natural English conversational inquiries without Indian language markers.
- `HINDI`: Dominant Hindi vocabulary in Devanagari or Latin transliteration.
- `MARATHI`: Dominant Marathi vocabulary in Devanagari or Latin transliteration.
- `HINGLISH`: Colloquial Hindi-English phrasing patterns or mixed Indian markers in Latin script.
- `HINDI_ENGLISH`: Hindi conversational grammar mixed with English conversational or technical vocabulary.
- `MARATHI_ENGLISH`: Marathi conversational grammar mixed with English conversational or technical vocabulary.
- `UNKNOWN`: Code-only inputs, stack traces without inquiry, numbers, URLs, file paths, or insufficient linguistic evidence.

### Schema (`backend/app/nlp/language_detection/schemas.py`):

```python
class Language(str, Enum):
    ENGLISH = "ENGLISH"
    HINDI = "HINDI"
    MARATHI = "MARATHI"
    HINGLISH = "HINGLISH"
    MARATHI_ENGLISH = "MARATHI_ENGLISH"
    HINDI_ENGLISH = "HINDI_ENGLISH"
    UNKNOWN = "UNKNOWN"

class LanguageDetectionResult(BaseModel):
    language: Language
    confidence: float
    evidence: list[str] = Field(default_factory=list)
```

### Key Guarantees & Features:
- **Technical-Vocabulary Neutrality**: Programming keywords (e.g. `python`, `code`, `function`, `debug`, `error`, `exception`, `calculator`) are classified as neutral technical vocabulary and do not inappropriately skew classification toward pure English.
- **Transliteration Support**: Robust centralized lexical resources support common Latin-script transliterated Marathi (e.g. `mala`, `madhe`, `aahe`, `samjat`, `karaycha`) and Hindi (e.g. `mujhe`, `samajh`, `karna`, `chahiye`, `banao`).
- **Devanagari & Cross-Script Detection**: Handles native Devanagari script for Marathi and Hindi, including mixed Devanagari-Latin inputs (e.g. `mala हा program debug karaycha aahe`).
- **Code & Traceback Weighting**: Code segments and Python tracebacks receive low influence; the user's natural language inquiry determines the detected conversational language. Code-only inputs safely receive `UNKNOWN` with low confidence.
- **Deterministic & 100% Offline**: Zero external network, cloud API, or LLM dependencies. Repeated runs on the same input produce identical language labels, confidence scores, and evidence lists.
- **Calibrated Confidence**: Confidence scores range from `0.0` to `1.0` reflecting the strength of linguistic evidence, with ambiguous or noise inputs receiving low confidence rather than false certainty.

---

# 11. Tone Classification

Implemented in `backend/app/nlp/tone_classification/tone_classifier.py`.

The Tone Classification component determines the user's desired communication style to guide the Prompt Builder and local LLM response generation.

### Pipeline Flow:

```text
PreprocessedText
      ↓
LanguageDetector (T09) [Language isolated]
      ↓
ToneClassifier (T11)
      ├── TF-IDF Word N-Grams (1, 2)
      ├── TF-IDF Char N-Grams (3, 5, char_wb)
      └── Multi-class Logistic Regression
      ↓
ToneClassificationResult (tone, confidence, probabilities)
```

> **Separation of Responsibilities**:
> - `T09 Language Detection` identifies *what natural language* the user is speaking (`Language`).
> - `T11 Tone Classification` identifies *what communication style* the user expects (`Tone`).
> - The classifier learns tone cues (e.g., formal politeness, brevity markers, technical depth requests) independently of language, ensuring that polite Marathi, polite Hindi, and polite English are all classified as `FORMAL`.

### Supported Tone Classes:
- `CASUAL`: Informal, friendly, conversational, slang-oriented requests (`bro`, `bhai`, `yaar`, `re`).
- `FORMAL`: Polite, respectful, professional, academic phrasing (`Please`, `Kindly`, `कृपया`).
- `SIMPLE`: Explicit requests for beginner-friendly, plain language, or non-technical analogies.
- `TECHNICAL`: Explicit requests for low-level architecture, internals, Big-O proofs, and algorithmic mechanics.
- `SHORT`: Explicit requests for concise, direct, one-line, or code-only responses (`just the code`, `fakt code de`).
- `DETAILED`: Explicit requests for comprehensive, step-by-step walk-throughs with edge cases and examples.

### Schema (`backend/app/nlp/tone_classification/schemas.py`):

```python
class Tone(str, Enum):
    CASUAL = "CASUAL"
    FORMAL = "FORMAL"
    SIMPLE = "SIMPLE"
    TECHNICAL = "TECHNICAL"
    SHORT = "SHORT"
    DETAILED = "DETAILED"

class ToneClassificationResult(BaseModel):
    tone: str
    confidence: float = Field(ge=0.0, le=1.0)
    probabilities: dict[str, float] = Field(default_factory=dict)
```

### Key Guarantees & Features:
- **Offline & Deterministic**: Zero network or cloud API calls. Uses local scikit-learn pipeline persisted at `models/tone/tone_classifier.joblib`.
- **Hybrid Representation**: Word n-grams `(1, 2)` capture semantic intent; subword character n-grams `(3, 5)` capture Indian-language transliterations and spelling variations.
- **Calibrated Probabilities**: Produces true probability distributions over all 6 tone classes.
- **Edge Case Robustness**: Safely handles empty string, whitespace, `None`, and multi-line code segments.

---

# 12. Intent Engine

Intent detection determines what action or deliverable the user wants the system to perform.

### Pipeline Progression:

```text
T09 Language Detection
        ↓
T10 Tone Dataset
        ↓
T11 Tone Classifier
        ↓
T12 Intent Dataset
        ↓
Future Intent Classifier (T13)
```

### Semantic Separation of Core NLP Responsibilities:
- **Language** = *What language or linguistic style is the user using?* (e.g., `ENGLISH`, `HINDI`, `MARATHI`, `HINGLISH`, `MARATHI_ENGLISH`, `HINDI_ENGLISH`)
- **Tone** = *How should the response sound or be formatted?* (e.g., `CASUAL`, `FORMAL`, `SIMPLE`, `TECHNICAL`, `SHORT`, `DETAILED`)
- **Intent** = *What does the user want the system to do or provide?* (e.g., `GENERATE_CODE`, `DEBUG_CODE`, `EXPLAIN_CODE`, etc.)

### Orthogonality Examples:
```text
"bro ha code debug kar na"
Language = MARATHI_ENGLISH
Tone     = CASUAL
Intent   = DEBUG_CODE

"Please explain this algorithm in detail."
Language = ENGLISH
Tone     = DETAILED
Intent   = ALGORITHM

"simple language madhe ha code samjhav"
Language = MARATHI_ENGLISH
Tone     = SIMPLE
Intent   = EXPLAIN_CODE
```

### Supported Intent Taxonomy (18 Labels):
1. `GENERATE_CODE`: User wants new implementation created from scratch.
2. `DEBUG_CODE`: User provides code or error and wants it fixed.
3. `EXPLAIN_CODE`: User wants existing code logic or behavior explained.
4. `OPTIMIZE_CODE`: User wants existing code made faster, cleaner, or less memory-intensive.
5. `CONVERT_CODE`: User wants code translated into another programming language.
6. `ALGORITHM`: User asks about algorithm behavior, design, or algorithmic selection.
7. `CONCEPT`: User asks to understand a general computer science or programming concept.
8. `CODE_REVIEW`: User requests an overall code quality, style, and maintainability critique.
9. `CODE_SUGGESTION`: User asks for incremental coding-level tips or improvements.
10. `PERFORMANCE_ANALYSIS`: User wants performance profiling, bottleneck detection, or latency analysis.
11. `ERROR_EXPLANATION`: User wants the meaning and root cause of an error/exception explained.
12. `APPROACH_SUGGESTION`: User asks for high-level strategy or methodology before writing code.
13. `BEST_PRACTICE`: User asks for recommended conventions, standards, or idioms.
14. `ARCHITECTURE_SUGGESTION`: User asks for system-level design, tier layout, or component architecture.
15. `FEATURE_SUGGESTION`: User asks for feature ideas or capability additions for a project.
16. `TEST_CASE_GENERATION`: User wants test cases, unit tests, mock scenarios, or edge cases.
17. `SECURITY_ANALYSIS`: User asks for vulnerability discovery, injection risks, or security audits.
18. `SEARCH`: User asks to locate previously saved code, conversation history, notes, or project items.

### Labeled Intent Dataset (T12):
- **Location**: `data/datasets/intent/`
  - `intent_dataset.csv` / `intent_dataset.jsonl` (1080 samples, 60 per intent, 180 per language)
  - `intent_train.csv` (756 samples, 70% stratified split)
  - `intent_validation.csv` (162 samples, 15% stratified split)
  - `intent_test.csv` (162 samples, 15% stratified split)
- **Validation**: Deterministic split isolation, zero data leakage, verified via `scripts/validate_intent_dataset.py`.
- **Classification Output (Future T13)**: Intent label + Confidence score with fallback for low-confidence inputs.

---

# 13. Programming Language Detection

Programming language detection uses:

```text
User Text
+
Code Block
+
Syntax
+
Keywords
+
File Extension
```

Output:

```text
Python
C
C++
Java
JavaScript
SQL
Unknown
```

---

# 14. Requirement Extraction

The Requirement Extraction component converts natural requests into structured fields.

Example:

```text
"Python madhe calculator banav, divide by zero handle kar"
```

Result:

```json
{
  "task": "calculator",
  "language": "Python",
  "requirements": [
    "calculator operations",
    "division by zero handling"
  ]
}
```

---

# 15. Context Engine

The Context Engine is responsible for maintaining coding conversation state.

It combines:

```text
Current Question
+
Current Code
+
Current Task
+
Programming Language
+
Recent Relevant Messages
+
NLP Metadata
+
Session Metadata
```

---

# 16. Context State

The active context may contain:

```text
session_id
current_task
current_code
programming_language
current_intent
user_language
user_tone
recent_messages
requirements
last_error
last_validation_result
```

---

# 17. Context Example

Conversation:

```text
User:
Create a Python calculator.

Assistant:
[calculator code]

User:
yat error handling add kar.

User:
ata Marathi madhe explain kar.
```

The system should retain:

```text
current_task = calculator
programming_language = Python
current_code = previous calculator
```

and only update the requested part.

---

# 18. Context Selection Strategy

Do NOT send the complete conversation history to the LLM every time.

Use:

```text
Full History
     ↓
Relevance Selection
     ↓
Recent Important Messages
+
Current Code
+
Current Task
+
Current Error
     ↓
Prompt Builder
```

This improves:

- Speed
- Memory usage
- Prompt quality
- Context efficiency

---

# 19. Prompt Builder

The Prompt Builder converts structured context into a local LLM prompt.

Conceptual input:

```text
SYSTEM INSTRUCTIONS
+
USER QUESTION
+
LANGUAGE
+
TONE
+
INTENT
+
PROGRAMMING LANGUAGE
+
REQUIREMENTS
+
CURRENT CODE
+
RELEVANT HISTORY
```

Output:

```text
Local LLM Prompt
```

---

# 20. Prompt Builder Rule

The Prompt Builder must not blindly insert every database field into every prompt.

Only relevant information should be included.

Example:

For `EXPLAIN_CODE`:

```text
Current Code
+
Desired Explanation Language
+
Tone
```

For `DEBUG_CODE`:

```text
Current Code
+
Error
+
Execution Feedback
+
Relevant History
```

---

# 21. LLM Service

Technology:

```text
Ollama
```

Responsibilities:

- Connect to local model
- Send prompts
- Stream output
- Handle model errors
- Track latency
- Return structured/raw output to Response Engine

Ollama must remain isolated behind an internal service interface.

---

# 22. LLM Abstraction

The application should not hard-code model-specific logic throughout the system.

Use an abstraction such as:

```text
LLMService
    ├── generate()
    ├── stream()
    ├── health_check()
    └── model_info()
```

The initial implementation:

```text
OllamaLLMService
```

Future implementations can replace it.

---

# 23. Local Model

Initial default:

```text
Qwen2.5-Coder 3B
```

Optional benchmark:

```text
Qwen2.5-Coder 7B
```

The Architecture must support replacing the model through configuration.

Example:

```text
OLLAMA_MODEL=qwen2.5-coder:3b
```

---

# 24. Response Engine

The Response Engine decides how the model output should be returned to the user.

It may perform:

- Response parsing
- Code block extraction
- Explanation separation
- Validation status attachment
- Suggestions
- Error formatting

Possible final structure:

```json
{
  "answer": "...",
  "code": "...",
  "language": "python",
  "validation": {
    "status": "PASS"
  },
  "suggestions": [
    "Add input validation"
  ]
}
```

Not every response needs every field.

---

# 25. Code Engine

The Code Engine is responsible for code-specific operations.

Responsibilities:

- Code extraction
- Code formatting
- Language identification support
- Code transformation
- Code analysis
- Validation integration
- Debugging integration

Potential modules:

```text
parser
formatter
converter
analyzer
reviewer
```

---

# 26. Code Validation Engine

The Validation Engine uses deterministic tools.

```text
Generated / Modified Code
          ↓
     Language Detector
          ↓
     Validation Strategy
          ↓
 ┌────────┼──────────┐
 │        │          │
Python   C/C++      Java
 │        │          │
AST    gcc/g++     javac
```

JavaScript and SQL have separate validation paths.

---

# 27. Validation Result

Possible states:

```text
PASS
FAIL
TIMEOUT
ERROR
NOT_VALIDATED
UNSUPPORTED
```

Example:

```json
{
  "status": "FAIL",
  "language": "python",
  "message": "SyntaxError on line 8"
}
```

---

# 28. Debugging Architecture

Debugging is implemented as a controlled feedback loop.

```text
User Code
   +
Error / Failure
       ↓
NLP Intent
       ↓
Debug Service
       ↓
LLM Analysis
       ↓
Proposed Fix
       ↓
Validator
       ↓
PASS ─────────→ Final Response
       │
       ▼
      FAIL
       │
       ▼
Repair Attempt
       │
       ▼
Validator
```

A maximum repair iteration count must be configured.

Example:

```text
MAX_REPAIR_ATTEMPTS = 3
```

This prevents endless loops.

---

# 29. Safe Code Execution

Execution architecture:

```text
User / LLM Code
      ↓
Validation
      ↓
Sandbox Request
      ↓
Docker Container
      ↓
Execution
      ↓
stdout / stderr / exit code
      ↓
Validation Result
```

The host machine must not directly execute untrusted generated code.

---

# 30. Sandbox Boundary

The sandbox must be treated as a separate security boundary.

```text
                 HOST
─────────────────────────────────────
FastAPI
SQLite
Frontend
Ollama
                  │
                  │ Controlled Request
                  ▼
            ┌─────────────┐
            │ Docker      │
            │ Sandbox     │
            ├─────────────┤
            │ Code        │
            │ Runtime     │
            │ Temp Files  │
            └─────────────┘
```

---

# 31. Sandbox Restrictions

The container should have:

```text
Network = Disabled
CPU = Limited
Memory = Limited
Timeout = Limited
Filesystem = Restricted
User = Non-root
Process = Controlled
```

Exact values will be finalized during Security Review.

---

# 32. Session Manager

The Session Manager provides:

```text
Create Session
Open Session
Rename Session
Delete Session
Continue Session
```

It connects the UI to the database and Context Engine.

---

# 33. Session Lifecycle

```text
New Session
    ↓
Messages
    ↓
Code / Context Updates
    ↓
Save to SQLite
    ↓
Close Application
    ↓
Reopen Session
    ↓
Restore Context
    ↓
Continue Conversation
```

---

# 34. Database Architecture

Initial database:

```text
SQLite
```

Conceptual schema and relationships:

```text
User
 │
 ├───────────────┐
 │               │
 ▼               ▼
Sessions        Notes
 │
 ▼
Messages
 │  │
 │  ├──────────────→ GeneratedCode
 │  │
 │  └──────────────→ DebugHistory (optional message link)
 │
 └────────────────→ SavedMessage
```

---

# 35. Core Entities

## User

```text
id (UUID, String 36, PK)
name (String 100)
created_at (DateTime UTC)
updated_at (DateTime UTC)
```

Relationships:
- `sessions`: 1-to-N Session (cascade delete)
- `saved_messages`: 1-to-N SavedMessage (cascade delete)
- `notes`: 1-to-N Note (cascade delete)

---

## Session

```text
id (UUID, String 36, PK)
user_id (UUID, FK -> users.id, indexed, cascade delete)
title (String 255)
status (String 50, default 'active')
current_language (String 50, optional)
programming_language (String 50, optional)
current_code (Text, optional)
created_at (DateTime UTC)
updated_at (DateTime UTC)
```

Relationships:
- `user`: N-to-1 User
- `messages`: 1-to-N Message (cascade delete, ordered by created_at)
- `generated_codes`: 1-to-N GeneratedCode (cascade delete)
- `debug_histories`: 1-to-N DebugHistory (cascade delete)
- `notes`: 1-to-N Note (on session delete, note session_id SET NULL)

---

## Message

```text
id (UUID, String 36, PK)
session_id (UUID, FK -> sessions.id, indexed, cascade delete)
role (String 20, check constraint: 'user', 'assistant', 'system')
content (Text)
detected_language (String 50, optional)
intent (String 50, optional)
tone (String 50, optional)
programming_language (String 50, optional)
context_metadata (JSON, optional)
created_at (DateTime UTC, indexed)
```

Relationships:
- `session`: N-to-1 Session
- `generated_codes`: 1-to-N GeneratedCode (cascade delete)
- `debug_histories`: 1-to-N DebugHistory (on message delete, message_id SET NULL)
- `saved_messages`: 1-to-N SavedMessage (cascade delete)

---

## GeneratedCode

```text
id (UUID, String 36, PK)
session_id (UUID, FK -> sessions.id, indexed, cascade delete)
message_id (UUID, FK -> messages.id, indexed, cascade delete)
language (String 50, default 'python')
code (Text)
validation_status (String 50, default 'unvalidated')
created_at (DateTime UTC)
```

Relationships:
- `session`: N-to-1 Session
- `message`: N-to-1 Message

---

## DebugHistory

```text
id (UUID, String 36, PK)
session_id (UUID, FK -> sessions.id, indexed, cascade delete)
message_id (UUID, FK -> messages.id, optional, indexed, ondelete SET NULL)
original_code (Text)
error_message (Text)
corrected_code (Text, optional)
validation_status (String 50, default 'pending')
attempt_count (Integer, default 1)
created_at (DateTime UTC)
```

Relationships:
- `session`: N-to-1 Session
- `message`: N-to-1 Message (optional)

---

## SavedMessage

```text
id (UUID, String 36, PK)
user_id (UUID, FK -> users.id, indexed, cascade delete)
message_id (UUID, FK -> messages.id, indexed, cascade delete)
label (String 100, optional)
created_at (DateTime UTC)
```

Constraints:
- Unique(`user_id`, `message_id`)

Relationships:
- `user`: N-to-1 User
- `message`: N-to-1 Message

---

## Note

```text
id (UUID, String 36, PK)
user_id (UUID, FK -> users.id, indexed, cascade delete)
session_id (UUID, FK -> sessions.id, optional, indexed, ondelete SET NULL)
title (String 255, default 'Untitled Note')
content (Text)
created_at (DateTime UTC)
updated_at (DateTime UTC)
```

Relationships:
- `user`: N-to-1 User
- `session`: N-to-1 Session (optional, notes can exist independently of sessions)

---

# 35.1 Database Repository Layer

Target Architecture:

```text
API → Service → Repository → SQLAlchemy Session → SQLite
```

Repositories reside in `backend/app/database/repositories/`:
- `BaseRepository`: Shared generic base providing queries, existence checks, pagination, and transactional `_save()` / `delete()`.
- `UserRepository`: User creation, lookup, listing, update, and deletion.
- `SessionRepository`: Conversation sessions with user ownership filtering, deterministic ordering (`updated_at DESC`), title search, and status tracking.
- `MessageRepository`: Conversation messages with strict session isolation, deterministic ordering (`created_at ASC`), content search, and latest retrieval.
- `SavedMessageRepository`: Bookmarked messages with idempotent duplicate handling, label updates, unsave support, and user isolation.
- `NoteRepository`: User personal notes (session-linked or standalone) with ownership filtering, search, and ordering.
- `GeneratedCodeRepository`: Code artifacts linked to sessions/messages with validation status tracking.
- `DebugHistoryRepository`: Append-oriented debugging records preserving chronological iterations without unnecessary modification.

Transaction Strategy:
- Repositories default to committing self-contained write operations (`commit=True`), immediately rolling back the session upon any database exception and re-raising.
- Multi-repository transactions support deferred commit (`commit=False`), allowing services to coordinate atomic operations across repositories.

---

# 36. Data Flow — Chat

```text
User
 ↓
React
 ↓
POST /chat
 ↓
FastAPI
 ↓
NLP Engine
 ↓
Context Engine
 ↓
Prompt Builder
 ↓
Ollama
 ↓
Local LLM
 ↓
Response Engine
 ↓
Validation (when code)
 ↓
SQLite
 ↓
Stream Response
 ↓
React
```

---

# 37. Data Flow — Debugging

```text
User
 ↓
React
 ↓
POST /debug
 ↓
FastAPI
 ↓
NLP
 ↓
Context
 ↓
Debug Service
 ↓
LLM
 ↓
Code Fix
 ↓
Validation
 ↓
PASS?
 ├── YES → Response
 └── NO  → Limited Repair Loop
 ↓
SQLite
 ↓
Frontend
```

---

# 38. Data Flow — Study Mode

```text
User
 ↓
Study Mode
 ↓
POST /study
 ↓
FastAPI
 ↓
Context
 ↓
Prompt Builder
 ↓
Local LLM
 ↓
Structured Study Content
 ↓
SQLite
 ↓
Frontend
```

---

# 39. Data Flow — PDF Export

```text
Session / Study Content
        ↓
Export Service
        ↓
PDF Generator
        ↓
PDF File
        ↓
exports/
```

The original session must remain stored even if PDF generation fails.

---

# 40. Frontend Architecture

```text
frontend/src/
│
├── components/
│   ├── Chat/
│   ├── CodeEditor/
│   ├── SessionSidebar/
│   ├── Message/
│   ├── Suggestions/
│   └── Study/
│
├── pages/
│   ├── ChatPage
│   ├── SessionsPage
│   ├── StudyPage
│   ├── NotesPage
│   └── SettingsPage
│
├── services/
│   ├── api
│   ├── chat
│   ├── sessions
│   └── export
│
├── hooks/
├── store/
├── types/
└── utils/
```

---

# 41. Backend Architecture

```text
backend/
│
├── api/
│   ├── chat.py
│   ├── sessions.py
│   ├── validation.py
│   ├── debug.py
│   ├── study.py
│   ├── notes.py
│   ├── saved.py
│   ├── search.py
│   └── export.py
│
├── core/
│   ├── config.py
│   ├── logging.py
│   └── errors.py
│
├── nlp/
│   ├── preprocessing.py
│   ├── language.py
│   ├── intent.py
│   ├── tone.py
│   ├── programming_language.py
│   └── requirement_extractor.py
│
├── context/
│   ├── manager.py
│   ├── selector.py
│   └── state.py
│
├── llm/
│   ├── base.py
│   ├── ollama_service.py
│   └── prompt_builder.py
│
├── code_engine/
│   ├── parser.py
│   ├── validator.py
│   ├── debugger.py
│   ├── reviewer.py
│   └── optimizer.py
│
├── sandbox/
│   ├── docker_runner.py
│   └── policies.py
│
├── database/
│   ├── models/
│   ├── session.py
│   └── repositories/
│
├── services/
│   ├── chat_service.py
│   ├── session_service.py
│   ├── debug_service.py
│   ├── study_service.py
│   ├── search_service.py
│   └── suggestion_service.py
│
└── export/
    └── pdf.py
```

---

# 42. API Architecture

Initial API groups:

```text
/chat
/sessions
/messages
/validate
/debug
/study
/notes
/saved
/search
/export
/health
```

---

# 43. Chat API Flow

```text
POST /chat
      ↓
Request Validation
      ↓
ChatService
      ↓
NLP
      ↓
Context
      ↓
LLM
      ↓
Response
```

Streaming should be supported for local LLM responses.

---

# 44. Health Architecture

The application should provide:

```text
GET /health
```

and optionally component checks:

```text
API
Database
Ollama
Model
Sandbox
```

Example conceptual result:

```json
{
  "api": "ok",
  "database": "ok",
  "ollama": "ok",
  "model": "ok",
  "sandbox": "ok"
}
```

---

# 45. Error Architecture

Errors should be categorized.

```text
ValidationError
LLMError
DatabaseError
SandboxError
ExportError
ConfigurationError
NLPError
```

The API converts internal errors into user-safe responses.

---

# 46. Error Flow

```text
Internal Component Error
        ↓
Error Handler
        ↓
Log Technical Details
        ↓
Generate Safe User Message
        ↓
Return API Error
        ↓
Frontend Error State
```

Sensitive internal details must not be shown to users.

---

# 47. Offline Architecture

During normal offline operation:

```text
Internet
   X
   │
   │
Local Machine
│
├── React
├── FastAPI
├── SQLite
├── NLP
├── Ollama
├── Local LLM
└── Docker Sandbox
```

No cloud AI API is required.

---

# 48. Deployment Architecture

Initial production target:

```text
                    LOCAL MACHINE
                         │
             ┌───────────┼───────────┐
             │           │           │
           React       FastAPI     Ollama
             │           │           │
             │           │      Local Model
             │           │
             │        SQLite
             │
             └──── Browser
```

Docker is used specifically for controlled code execution.

---

# 49. Startup Flow

Expected startup:

```text
Start Application
       ↓
Check Configuration
       ↓
Check SQLite
       ↓
Check Ollama
       ↓
Check Model
       ↓
Check Sandbox
       ↓
Start Backend
       ↓
Start Frontend
       ↓
Ready
```

If Ollama is unavailable:

```text
Application
→ Start
→ Show "Local model unavailable"
```

The UI should remain usable for non-LLM functionality where practical.

---

# 50. Security Architecture

Primary boundaries:

```text
USER INPUT
    ↓
NLP / VALIDATION
    ↓
APPLICATION SERVICES
    ↓
LLM
    ↓
VALIDATION
    ↓
SANDBOX
```

No untrusted user/LLM output should directly access:

```text
Host Shell
Host Filesystem
Host Network
Secrets
Production Database
```

---

# 51. Secret Boundary

Secrets must remain outside:

```text
LLM prompts
User-visible errors
Logs
Generated code
Git repository
```

---

# 52. Prompt Injection Boundary

User content must be treated as untrusted input.

The system should not allow a user message or generated code to override:

- Application security policies
- Sandbox restrictions
- System instructions
- Access boundaries

Prompt-injection handling will be detailed further in Phase 13.

---

# 53. Code Execution Boundary

```text
LLM Output
   ↓
Validation
   ↓
Security Policy
   ↓
Docker Sandbox
```

Never:

```text
LLM Output
   ↓
os.system(...)
```

on the host.

---

# 54. Performance Architecture

Performance-sensitive areas:

```text
NLP latency
LLM first-token latency
LLM generation latency
Context building
Database queries
Validation
Sandbox startup
Frontend rendering
```

The system should measure these rather than guessing.

---

# 55. Resource Optimization

## LLM

Use small local model by default.

## Context

Send relevant context only.

## NLP

Use lightweight classifiers.

## Database

Use indexed session/message queries.

## Frontend

Avoid unnecessary rerendering.

## Sandbox

Use controlled timeouts and resource limits.

---

# 56. Modularity

The following components must be replaceable:

```text
NLP classifier
Language detector
LLM model
LLM runtime
Database
Frontend
Code editor
PDF engine
Sandbox implementation
```

Example:

```text
Ollama
↓
LLMService Interface
↓
Another Runtime
```

should not require rewriting ChatService.

---

# 57. Research Experiment Boundary

The architecture should allow baseline comparison.

## Baseline

```text
User
↓
Local LLM
↓
Response
```

## Proposed

```text
User
↓
NLP
↓
Context
↓
Structured Prompt
↓
Local LLM
↓
Validation
↓
Response
```

This separation is important for research evaluation.

---

# 58. Observability

The system should record local metrics such as:

```text
Request ID
Intent
Language
LLM model
First token latency
Total latency
Validation result
Repair attempts
Errors
```

Sensitive user content should not be logged unnecessarily.

---

# 59. Architecture Risks

## AR-001 — Context Growth

Large history may increase latency and model memory.

### Mitigation

Context selection and summarization.

---

## AR-002 — Local LLM Quality

Small models may produce incorrect code.

### Mitigation

Validation + repair + model benchmarking.

---

## AR-003 — NLP Misclassification

Wrong intent/language may route the request incorrectly.

### Mitigation

Confidence scoring + fallback + testing.

---

## AR-004 — Sandbox Risk

Unsafe execution can still be dangerous if incorrectly configured.

### Mitigation

Dedicated Security Review.

---

## AR-005 — Service Coupling

Poor implementation may cause components to depend directly on each other.

### Mitigation

Service interfaces and clear boundaries.

---

# 60. Architecture Rules

1. Frontend never accesses SQLite directly.
2. Frontend never accesses Ollama directly.
3. API routes should not contain complex business logic.
4. NLP should remain independent of UI.
5. LLM access should go through an LLM service abstraction.
6. Code execution should go through the Sandbox service.
7. Database access should go through repositories/services.
8. Context selection should remain separate from prompt formatting.
9. Validation should remain separate from LLM generation.
10. Generated code must never directly execute on the host.
11. Components should expose clear interfaces.
12. New dependencies require justification.

---

# 61. Architecture-to-Repository Mapping

```text
Frontend
→ frontend/

API
→ backend/api/

NLP
→ backend/nlp/

Context
→ backend/context/

LLM
→ backend/llm/

Code Engine
→ backend/code_engine/

Sandbox
→ backend/sandbox/

Database
→ backend/database/

Services
→ backend/services/

Study
→ backend/services/study-related modules

Export
→ backend/export/

Tests
→ tests/

Documentation
→ docs/
```

---

# 62. End-to-End Example

## User Query

```text
"python madhe calculator banav ani divide by zero handle kar"
```

### Step 1 — Frontend

React sends:

```text
POST /chat
```

---

### Step 2 — FastAPI

Request reaches ChatService.

---

### Step 3 — NLP

System detects:

```text
Language = MARATHI_ENGLISH
Tone = CASUAL
Intent = GENERATE_CODE
Programming Language = PYTHON
```

---

### Step 4 — Requirement Extraction

```text
Task = Calculator
Requirement = Division by zero handling
```

---

### Step 5 — Context

Current session context is loaded.

---

### Step 6 — Prompt Builder

Builds structured local prompt.

---

### Step 7 — Ollama

FastAPI sends the prompt to Ollama.

---

### Step 8 — Local LLM

Qwen2.5-Coder 3B generates code.

---

### Step 9 — Validation

Python AST/parser checks syntax.

Optional sandbox execution verifies behavior.

---

### Step 10 — Response

Response Engine returns:

```text
Explanation
+
Code
+
Validation Status
+
Relevant Suggestion
```

---

### Step 11 — Persistence

Session and message are stored in SQLite.

---

### Step 12 — Frontend

React displays the response and code.

---

# 63. Follow-Up Example

User:

```text
yat error handling add kar
```

System:

```text
Current Session
+
Current Calculator Code
+
Current Task
+
New Intent = MODIFY / DEBUG
```

The system modifies the current code instead of creating an unrelated calculator.

---

# 64. Architecture Acceptance Criteria

- [x] High-level architecture defined
- [x] Component architecture defined
- [x] Frontend architecture defined
- [x] Backend architecture defined
- [x] NLP pipeline defined
- [x] Context flow defined
- [x] Prompt-building flow defined
- [x] LLM architecture defined
- [x] Code validation architecture defined
- [x] Debugging loop defined
- [x] Sandbox boundary defined
- [x] Session architecture defined
- [x] Database architecture defined
- [x] API direction defined
- [x] Offline architecture defined
- [x] Deployment architecture defined
- [x] Security boundaries defined
- [x] Research baseline/proposed architecture separated
- [x] Performance considerations documented

---

# 65. Phase 6 Status

**STATUS: COMPLETE**

The technical architecture is defined sufficiently to begin application design.

---

# 66. Next Phase

## Phase 7 — Design

The next phase will define:

```text
UI Principles
      ↓
Page / Screen Structure
      ↓
Navigation
      ↓
Chat Layout
      ↓
Code Editor
      ↓
Session Sidebar
      ↓
Study Mode
      ↓
Notes
      ↓
Search
      ↓
Error States
      ↓
Loading / Streaming States
      ↓
Responsive Behavior
```

The Design phase will describe **what the user sees and how the user interacts with the system**, without yet implementing the UI.