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

Preprocessing may include:

- Whitespace normalization
- Unicode normalization
- Code block separation
- Text normalization
- Basic tokenization
- Noise reduction where appropriate

The system must avoid over-normalizing code.

For example:

```text
Natural Language
```

and:

```text
Code Block
```

must be treated separately.

---

# 10. Language Detection

The Language Detection component identifies:

- English
- Hindi
- Marathi
- Hinglish
- Hindi-English
- Marathi-English

Possible flow:

```text
Input
 ↓
Script Detection
 ↓
Language Detector
 ↓
Project Rules
 ↓
Confidence
 ↓
Language Result
```

Short or ambiguous input may produce:

```text
language = UNKNOWN
confidence = LOW
```

instead of forcing a wrong classification.

---

# 11. Tone Detection

Tone detector identifies:

```text
CASUAL
FORMAL
SIMPLE
TECHNICAL
SHORT
DETAILED
```

The result is used by the Prompt Builder.

Example:

```text
User Tone = SIMPLE
```

can instruct the LLM to explain concepts using beginner-friendly language.

---

# 12. Intent Engine

Intent detection determines what the user is trying to accomplish.

Example:

```text
"python madhe calculator banav"
→ GENERATE_CODE

"हा code error ka detoy?"
→ DEBUG_CODE

"simple Marathi madhe samjav"
→ EXPLAIN_CODE

"हा code slow ka aahe?"
→ PERFORMANCE_ANALYSIS
```

The classifier must produce:

```text
Intent
+
Confidence
```

Low-confidence cases should use a fallback path.

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

Conceptual schema:

```text
users
  │
  └── sessions
         │
         ├── messages
         ├── generated_code
         ├── debug_history
         ├── saved_messages
         ├── notes
         └── study_sessions
```

---

# 35. Core Entities

## User

```text
id
name
created_at
settings
```

---

## Session

```text
id
title
created_at
updated_at
status
current_language
current_task
current_code
```

---

## Message

```text
id
session_id
role
content
timestamp
intent
language
tone
programming_language
```

---

## GeneratedCode

```text
id
session_id
message_id
language
code
validation_status
created_at
```

---

## DebugHistory

```text
id
session_id
code_version
error
suggested_fix
validation_result
timestamp
```

---

## SavedMessage

```text
id
session_id
message_id
created_at
```

---

## Note

```text
id
session_id
title
content
created_at
updated_at
```

---

## StudySession

```text
id
session_id
topic
content
quiz_data
created_at
```

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