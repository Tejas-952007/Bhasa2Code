# Bhasha2Code — Technology Stack

## Phase 5 — Technology Stack

**Project:** Bhasha2Code  
**Phase:** 5 — Technology Stack  
**Version:** 1.1  
**Status:** LOCKED FOR ARCHITECTURE  
**Development Tool:** Antigravity  
**Primary Deployment:** Localhost / Offline  
**Target User:** Student / Beginner-to-Intermediate Programmer

---

# 1. Purpose

This document defines the final technology direction for Bhasha2Code.

The selected stack must be:

- Offline-friendly
- Lightweight
- Maintainable
- Easy to develop using Antigravity
- Suitable for a 16 GB RAM consumer laptop
- Expandable for future versions
- Appropriate for an academic/research project
- Practical for a working localhost product

The project will prioritize a reliable V1 over unnecessarily large infrastructure.

---

# 2. Hardware Constraint

The initial development environment is a consumer laptop with approximately:

```text
RAM
16 GB

GPU
NVIDIA RTX 3050 Mobile
4 GB VRAM

Storage
1 TB NVMe SSD
```

The application must therefore avoid assuming that large local models can run fully inside VRAM.

Model selection must consider:

```text
Model Size
+
RAM Usage
+
VRAM Usage
+
Context Size
+
Response Speed
+
Code Quality
```

---

# 3. Technology Selection Principle

The technology decision hierarchy is:

```text
Practicality
      ↓
Offline Support
      ↓
Reliability
      ↓
Low Resource Usage
      ↓
Development Speed
      ↓
Maintainability
      ↓
Future Scalability
```

A technology should not be selected only because it is modern or popular.

---

# 4. Final V1 Stack

```text
Frontend
React + Vite

Backend
Python 3.11 + FastAPI

Database
SQLite

ORM
SQLAlchemy

NLP
scikit-learn + spaCy + Regex

Language Detection
Offline detector + project rules

Intent / Tone
TF-IDF + Logistic Regression

LLM Runtime
Ollama

Default Coding LLM
Qwen2.5-Coder 3B

Optional Benchmark Model
Qwen2.5-Coder 7B

Code Validation
AST + Language Compilers / Runtimes

Sandbox
Docker

PDF
ReportLab

Testing
pytest + httpx + React Testing Library / Vitest

E2E
Playwright

Version Control
Git
```

---

# 5. Backend

## Selected Technology

**Python 3.11**

### Why

Python is the primary backend language because the project requires:

- NLP
- Machine Learning
- Local LLM integration
- Code analysis
- API development
- PDF generation
- Database integration

Python 3.11 is selected as the initial compatibility target because it provides a stable ecosystem for the planned libraries.

---

# 6. API Framework

## Selected Technology

**FastAPI**

### Responsibilities

FastAPI will handle:

- Chat requests
- NLP pipeline
- LLM communication
- Context management
- Sessions
- Database operations
- Code validation
- Debugging
- Study Mode
- Notes
- PDF export
- Health checks

### Why FastAPI?

- Native Python integration
- Fast development
- Type-hint support
- Automatic API documentation
- Good async support
- Easy testing

---

# 7. Frontend

## Selected Technology

**React + Vite**

### Why

The final application is not only a chatbot.

It requires:

```text
Chat
+
Session Sidebar
+
Code Editor
+
Saved Messages
+
Notes
+
Study Mode
+
Search
+
PDF Export
+
Settings
```

A component-based frontend is therefore more suitable than a basic demo UI.

### Why not Streamlit as final V1?

Streamlit remains useful for quick experiments, but the intended product requires more control over:

- Layout
- Chat state
- Session navigation
- Code editor
- Streaming
- Interactive controls
- Persistent application state

Therefore:

```text
Rapid Experiment
→ Streamlit allowed temporarily

Final Application
→ React + Vite
```

---

# 8. Code Editor

## Selected Technology

**Monaco Editor**

### Purpose

The coding interface will use a browser-based editor for:

- Syntax highlighting
- Code editing
- Language selection
- Error display
- Current-code context

The editor should be isolated as a frontend component so it can be replaced later.

---

# 9. NLP Stack

Bhasha2Code will use a **hybrid NLP architecture** rather than an expensive transformer-based NLP pipeline.

```text
Rules
+
Regex
+
Script Detection
+
Machine Learning
```

This keeps the system lightweight and offline.

---

# 10. scikit-learn

## Purpose

Used primarily for:

- Intent classification
- Tone classification

Initial pipeline:

```text
User Text
↓
Preprocessing
↓
TF-IDF
↓
Logistic Regression
↓
Prediction
```

### Why?

- Lightweight
- Fast
- Offline
- Easy to retrain
- Easy to evaluate
- Academically explainable

---

# 11. Intent Classifier

## Model

**TF-IDF + Logistic Regression**

### Initial Classes

```text
GENERATE_CODE
DEBUG_CODE
EXPLAIN_CODE
OPTIMIZE_CODE
CONVERT_CODE
ALGORITHM
CONCEPT
CODE_REVIEW
CODE_SUGGESTION
PERFORMANCE_ANALYSIS
ERROR_EXPLANATION
APPROACH_SUGGESTION
BEST_PRACTICE
ARCHITECTURE_SUGGESTION
FEATURE_SUGGESTION
TEST_CASE_GENERATION
SECURITY_ANALYSIS
```

### Requirement

The classifier must have a confidence score.

If confidence is too low:

```text
Unknown / Ambiguous
↓
Clarification or fallback
```

The system must not blindly execute a wrong action.

---

# 12. Tone Classifier

## Model

**TF-IDF + Logistic Regression**

### Classes

```text
CASUAL
FORMAL
SIMPLE
TECHNICAL
SHORT
DETAILED
```

Tone affects response style.

It must never change technical correctness.

---

# 13. spaCy

## Purpose

Use spaCy for:

- Tokenization
- Text preprocessing
- Linguistic utilities
- Future entity extraction

spaCy is a supporting NLP component, not the complete language-understanding system.

---

# 14. Regex and Rule Engine

A lightweight rule layer is mandatory for predictable information.

It will help detect:

- Programming-language names
- Common coding commands
- Error keywords
- Code blocks
- Explicit conversion requests
- Optimization requests
- File extensions
- Technical keywords

Example:

```text
"python madhe calculator banav"
```

may produce:

```text
Programming Language = Python
Task = Calculator
```

without requiring an LLM call.

---

# 15. Language Detection

## Initial Approach

Use an offline language detector combined with project-specific rules.

Potential components:

```text
Language Detector
+
Script Detection
+
Romanized-Word Rules
+
Confidence
```

Target categories:

```text
ENGLISH
HINDI
MARATHI
HINGLISH
HINDI_ENGLISH
MARATHI_ENGLISH
```

### Important Constraint

Generic language-detection libraries may perform poorly on short Romanized Marathi/Hindi text and heavily code-switched text.

Therefore, Bhasha2Code will not depend on a single library.

The final implementation will be validated using the project's own evaluation dataset.

---

# 16. Programming Language Detection

A hybrid approach will be used.

```text
Explicit User Mention
        +
Code Block
        +
Syntax
        +
Keywords
        +
File Extension
        ↓
Programming Language
```

Initial languages:

```text
Python
C
C++
Java
JavaScript
SQL
```

---

# 17. Requirement Extraction

Requirement extraction will initially use a lightweight structured approach.

Potential fields:

```text
task
programming_language
input
output
constraints
features
error
target_language
optimization_goal
security_requirement
```

Initial implementation:

```text
Intent
+
Regex
+
Keywords
+
Context
```

A dedicated transformer model is **not required for V1**.

---

# 18. Local LLM Runtime

## Selected Technology

**Ollama**

Ollama will act as the local model-serving layer:

```text
FastAPI
   ↓
Ollama
   ↓
Local Coding LLM
```

The core application must not require a cloud LLM API.

---

# 19. Local Coding Model Strategy

The model will be selected based on the actual hardware and benchmark results.

## Default Model

**Qwen2.5-Coder 3B**

The current Ollama model listing provides small Qwen2.5-Coder variants, including 3B, making this size practical as the first local benchmark target. [Qwen2.5-Coder models on Ollama](https://ollama.com/library/qwen2.5-coder?utm_source=chatgpt.com)

### Why 3B?

- Relatively small model
- More practical for 16 GB RAM
- Lower inference cost than larger coding models
- Suitable for initial code-generation experiments
- Suitable for localhost MVP development

---

# 20. Secondary Model

**Qwen2.5-Coder 7B**

7B will be treated as an optional benchmark candidate, not a mandatory dependency.

The Ollama listing provides a 7B Qwen2.5-Coder variant. [Qwen2.5-Coder 7B on Ollama](https://ollama.com/library/qwen2.5-coder%3A7b-instruct?utm_source=chatgpt.com)

### Purpose

Compare:

```text
3B
vs.
7B
```

on:

- Code quality
- Debugging
- Explanation
- Multilingual prompts
- Context handling
- Latency
- Resource consumption

---

# 21. Model Selection Rule

The project must NOT assume:

```text
Larger Model = Better Model
```

The final model decision will use:

```text
Code Quality
+
Debugging Quality
+
Multilingual Quality
+
Context Quality
+
Latency
+
RAM
+
VRAM
```

The model with the best practical trade-off becomes the default model.

---

# 22. Models Excluded from V1 Default

Large models such as:

```text
14B
32B
30B+
```

are not required for the first version.

For example, current Ollama listings show `qwen3-coder:30b` at roughly 19 GB, which is already large relative to the project's 16 GB RAM target. [Qwen3-Coder on Ollama](https://ollama.com/library/qwen3-coder?utm_source=chatgpt.com)

Therefore:

```text
Large Models
→ Optional high-resource experiment

Not
→ V1 requirement
```

---

# 23. Important Hardware Rule

A model's downloaded file size must NOT be treated as its total runtime memory requirement.

Actual inference resources depend on:

```text
Model
+
Quantization
+
Context
+
KV Cache
+
Runtime Overhead
```

Therefore, actual RAM usage must be measured during Phase 10 Setup / model benchmarking.

---

# 24. GPU Strategy

The application must remain functional even when GPU acceleration is unavailable.

```text
Preferred:
GPU + CPU

Fallback:
CPU only
```

The software architecture must not hard-depend on the NVIDIA GPU.

---

# 25. Context Manager

## Technology

Python service layer + SQLite-backed session state.

### Responsibilities

- Track current task
- Track current code
- Track programming language
- Track relevant conversation history
- Track user language
- Track user tone
- Resolve follow-up references

Example:

```text
User:
Create calculator.

Assistant:
[code]

User:
yat error handling add kar.
```

The context manager should resolve:

```text
"yat"
→ current calculator code
```

---

# 26. Context Strategy

The system must not send unlimited history to the LLM.

Instead:

```text
Conversation History
↓
Relevance Selection
↓
Current Code
+
Current Task
+
Recent Messages
↓
Prompt Builder
```

This reduces memory use and inference latency.

---

# 27. Prompt Builder

The prompt builder converts structured application context into the local LLM request.

Input:

```text
User Question
Language
Tone
Intent
Programming Language
Requirements
Current Code
Relevant History
```

Output:

```text
Structured Local-LLM Prompt
```

---

# 28. Database

## Selected Technology

**SQLite**

### Why?

- Completely local
- No separate database server
- Low resource usage
- Easy backup
- Easy deployment
- Good for initial single-user localhost product

---

# 29. ORM

## Selected Technology

**SQLAlchemy**

### Purpose

Provide structured database access for:

```text
sessions
messages
saved_messages
notes
generated_code
debug_history
study_sessions
```

---

# 30. Database Migration

**Alembic** will be introduced before stable production packaging if the schema requires ongoing versioned migrations.

It is not necessary to add migration complexity on day one if the schema is still rapidly changing.

---

# 31. Code Validation

Code should be checked using deterministic tools whenever possible.

```text
Generated Code
↓
Syntax / Static Check
↓
Compiler / Interpreter
↓
Validation Result
```

The LLM must not be treated as the validator of its own output.

---

# 32. Python Validation

Use:

```text
Python AST
+
Controlled Interpreter
```

Pipeline:

```text
Python Code
↓
AST Parse
↓
Syntax Check
↓
Controlled Execution
```

---

# 33. C / C++ Validation

Use:

```text
gcc
g++
```

Pipeline:

```text
Code
↓
Compile
↓
Capture stderr
↓
Validation Result
```

---

# 34. Java Validation

Use:

```text
javac
java
```

Execution must occur inside the sandbox.

---

# 35. JavaScript Validation

Use:

```text
Node.js
```

for controlled syntax/runtime validation.

---

# 36. SQL Validation

SQL will initially use a controlled local database/parser approach.

Generated SQL must never be executed against a real production database.

---

# 37. Sandbox

## Selected Technology

**Docker**

Generated code must never directly execute on the host.

Minimum controls:

```text
No Network
CPU Limit
Memory Limit
Timeout
Restricted Filesystem
Non-root User
Controlled Process
```

The exact Docker security configuration will be finalized during:

```text
Phase 13 — Security Review
```

---

# 38. Sandbox Scope

The first execution-support target should be:

```text
Python
C
C++
JavaScript
```

Additional languages may be added after sandbox stability is verified.

SQL execution will remain isolated through a controlled local database environment.

---

# 39. PDF Export

## Selected Technology

**ReportLab**

Purpose:

- Session export
- Study notes
- Coding notes
- Code snippets
- Learning material

Possible output:

```text
Bhasha2Code Study Session
        ↓
PDF
```

---

# 40. Testing

## Backend

**pytest**

Test levels:

```text
Unit
Integration
System
```

---

# 41. API Testing

**httpx**

will be used for API integration tests.

---

# 42. Frontend Testing

Use:

```text
Vitest
+
React Testing Library
```

Test:

- Components
- Chat interaction
- Session UI
- Error states
- Loading states
- Saved messages
- Study Mode

---

# 43. End-to-End Testing

## Selected Technology

**Playwright**

Critical workflow:

```text
Open Application
↓
Create Session
↓
Ask Marathi/Hinglish Query
↓
Generate Code
↓
Follow-up
↓
Debug
↓
Save
↓
Close Session
↓
Reopen
↓
Continue
↓
Export PDF
```

---

# 44. Version Control

## Selected Technology

**Git**

Use Git for:

- Version history
- Branches
- Rollbacks
- Feature development
- Release tags

---

# 45. GitHub

GitHub will be the remote repository and collaboration platform.

The project should use:

```text
main
+
feature branches
```

Meaningful commit messages are required.

---

# 46. Environment

Use:

```text
.env
.env.example
```

`.env` must never be committed.

Potential configuration:

```text
OLLAMA_HOST
OLLAMA_MODEL
DATABASE_URL
LOG_LEVEL
SANDBOX_TIMEOUT
SANDBOX_MEMORY
SANDBOX_CPU
```

---

# 47. Logging

Use Python standard logging initially.

Levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Logs must not expose:

- Passwords
- Tokens
- API keys
- Secrets
- Sensitive local data

---

# 48. API Design Direction

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

Exact endpoint definitions will be finalized in:

**Phase 6 — Architecture**

---

# 49. Project Technology Boundaries

The project must keep technologies separated.

```text
backend/
├── api/
├── core/
├── nlp/
├── llm/
├── context/
├── code_engine/
├── sandbox/
├── database/
├── sessions/
├── study/
└── export/
```

Frontend:

```text
frontend/
└── src/
    ├── components/
    ├── pages/
    ├── services/
    ├── hooks/
    ├── store/
    ├── types/
    └── utils/
```

---

# 50. Offline Compatibility

| Technology | Offline | V1 |
|---|---:|---:|
| Python | Yes | Required |
| FastAPI | Yes | Required |
| React | Yes after dependencies are installed | Required |
| Vite | Yes after dependencies are installed | Required |
| SQLite | Yes | Required |
| SQLAlchemy | Yes | Required |
| scikit-learn | Yes | Required |
| spaCy | Yes after local model/data installation | Required |
| Regex | Yes | Required |
| Ollama | Yes | Required |
| Qwen2.5-Coder 3B | Yes | Default |
| Qwen2.5-Coder 7B | Yes | Optional benchmark |
| Docker | Yes | Required before code execution |
| ReportLab | Yes | Required |
| pytest | Yes | Required |
| Playwright | Yes after browser installation | Required for E2E |

---

# 51. Technology Alternatives

| Area | Selected | Alternative | Decision |
|---|---|---|---|
| Backend | FastAPI | Flask | FastAPI selected |
| Frontend | React + Vite | Streamlit | React for final product |
| Database | SQLite | PostgreSQL | SQLite for offline V1 |
| ORM | SQLAlchemy | Raw SQL | SQLAlchemy |
| Intent ML | TF-IDF + Logistic Regression | Transformer | Lightweight baseline |
| NLP | spaCy + Rules | Heavy Transformer Pipeline | Lower resource requirement |
| LLM Runtime | Ollama | llama.cpp | Easier initial integration |
| Coding Model | Qwen2.5-Coder 3B | Qwen2.5-Coder 7B | 3B default, 7B benchmark |
| Sandbox | Docker | VM | Docker for initial implementation |
| PDF | ReportLab | WeasyPrint | ReportLab |
| Testing | pytest | unittest | pytest |
| E2E | Playwright | Cypress | Playwright |

---

# 52. Why Not a Transformer-Based Intent Model?

A large transformer classifier would increase:

- Model size
- RAM usage
- Inference overhead
- Deployment complexity

The project already has a local coding LLM.

Therefore, using another large model for simple routing tasks is unnecessary for V1.

Initial:

```text
TF-IDF
+
Logistic Regression
```

is sufficient as an interpretable research baseline.

A transformer classifier can become a V2 experiment.

---

# 53. Why Not a Separate Embedding Database?

A dedicated vector database is not mandatory for V1.

The first version primarily requires:

- Conversation context
- Session history
- Current code
- Notes

SQLite is sufficient initially.

A local vector store can be introduced later if repository/document retrieval becomes necessary.

---

# 54. Why Not PostgreSQL?

PostgreSQL is powerful but introduces a separate database service.

For a localhost single-user offline application:

```text
SQLite
→ simpler
→ lower resource usage
→ easier installation
→ easier backup
```

PostgreSQL can be introduced for future multi-user deployment.

---

# 55. Why Docker Is Not Used for Everything

Docker will primarily isolate unsafe code execution.

The following can remain directly installed/local:

```text
FastAPI
React
SQLite
Ollama
NLP
```

This reduces unnecessary container complexity during development.

Docker should not become an obstacle to fast development.

---

# 56. Local Resource Strategy

The application should minimize resource usage through:

### LLM

Use 3B default model.

### Context

Send only relevant context.

### NLP

Use lightweight local classifiers.

### Database

Use SQLite.

### Services

Avoid unnecessary background services.

### Model Loading

Avoid repeatedly loading/unloading the local model.

### Frontend

Keep UI lightweight and component-based.

---

# 57. Recommended V1 Runtime

```text
                 Bhasha2Code
                      │
          ┌───────────┴───────────┐
          │                       │
       React                   FastAPI
          │                       │
          │                ┌──────┼──────┐
          │                │      │      │
          │               NLP   Context  DB
          │                │      │     SQLite
          │                └──────┼──────┘
          │                       │
          │                    Ollama
          │                       │
          │               Qwen2.5-Coder 3B
          │                       │
          │                  Code Engine
          │                       │
          │                  Validator
          │                       │
          │                    Docker
          │
          └────────────── UI Response
```

---

# 58. Model Benchmark Gate

Before declaring the LLM final:

```text
Qwen2.5-Coder 3B
        ↓
Benchmark
        ↓
Qwen2.5-Coder 7B
        ↓
Benchmark
        ↓
Compare
```

Evaluation:

```text
Code Generation
Debugging
Explanation
Multilingual Input
Code-Mixed Input
Context Follow-up
Latency
RAM
VRAM
```

The benchmark result determines the final default model.

---

# 59. Product vs Research Components

## Product Components

```text
React
FastAPI
SQLite
Ollama
Code Engine
Sessions
Study Mode
PDF
```

## Research Components

```text
Language Detection
Intent Classification
Tone Classification
Requirement Extraction
Multilingual Evaluation
Code-Mixed Evaluation
Context Evaluation
Validation Loop Evaluation
```

This separation helps ensure that the project remains both:

```text
Working Product
+
Research Project
```

---

# 60. Technology Risks

## TR-001 — Small Model Quality

3B may not perform as strongly as larger coding models.

### Mitigation

Benchmark 7B and evaluate actual tasks.

---

## TR-002 — CPU-Only Inference

If GPU acceleration is unavailable, response latency may increase.

### Mitigation

The system must support CPU fallback and optimize context/model settings.

---

## TR-003 — Code-Mixed NLP

Marathi-English and Hindi-English input may be difficult for traditional classifiers.

### Mitigation

Use:

```text
Rules
+
ML
+
Confidence
+
Project Dataset
```

---

## TR-004 — React Development Effort

React requires more frontend work than Streamlit.

### Mitigation

Keep the frontend architecture simple and component-based.

---

## TR-005 — Sandbox Security

Docker is not a magical security guarantee.

### Mitigation

Perform a dedicated Security Review before enabling execution.

---

# 61. Locked Technology Decisions

The following are locked for V1:

```text
Python 3.11
FastAPI
React
Vite
SQLite
SQLAlchemy
scikit-learn
spaCy
Regex / Rules
Ollama
Qwen2.5-Coder 3B
Docker
ReportLab
pytest
Git
```

---

# 62. Benchmark / Conditional Decisions

These are deliberately not permanently locked until testing:

```text
Qwen2.5-Coder 7B
Exact language-detection library
Exact PDF formatting approach
Exact Monaco configuration
Exact sandbox limits
Exact context-window settings
```

---

# 63. V1 Technologies Explicitly Avoided

The following are not required initially:

```text
Kubernetes
Redis
PostgreSQL
Kafka
Cloud LLM APIs
Separate vector database
Microservices
Multiple LLM servers
Large 30B+ local models
Complex agent frameworks
```

These may be introduced only if a genuine requirement appears.

---

# 64. Final Technology Decision

The final V1 technology philosophy is:

> **Use the smallest practical technology stack that can satisfy the product requirements and research objectives.**

Therefore:

```text
Lightweight NLP
+
Small Local Coding LLM
+
Simple Local Database
+
Structured Backend
+
Proper Frontend
+
Controlled Sandbox
```

is preferred over a large infrastructure stack.

---

# 65. Phase 5 Acceptance Criteria

- [x] Hardware constraint documented
- [x] Backend finalized
- [x] Frontend finalized
- [x] Database finalized
- [x] NLP strategy finalized
- [x] LLM runtime finalized
- [x] Default local model selected
- [x] Secondary benchmark model defined
- [x] Large models excluded from V1 default
- [x] Code validation stack defined
- [x] Sandbox defined
- [x] PDF stack defined
- [x] Testing stack defined
- [x] Offline compatibility documented
- [x] Resource strategy documented
- [x] Alternatives documented
- [x] Unlocked decisions documented
- [x] Unnecessary V1 technologies explicitly excluded

---

# 66. Phase 5 Status

**STATUS: COMPLETE**

The V1 technology stack is locked around practical localhost/offline operation on consumer hardware.

The exact local LLM will still be benchmark-verified during Setup before final production configuration.

---

# 67. Next Phase

## Phase 6 — Architecture

The technology stack will now be converted into the detailed technical architecture:

```text
System Architecture
        ↓
Component Architecture
        ↓
Frontend Architecture
        ↓
Backend Architecture
        ↓
NLP Pipeline
        ↓
Context Architecture
        ↓
LLM Architecture
        ↓
Database Schema
        ↓
API Architecture
        ↓
Code Validation
        ↓
Docker Sandbox
        ↓
Security Boundaries
        ↓
Deployment Architecture
```

**Phase 6 must describe how all selected technologies communicate with each other before development begins.**