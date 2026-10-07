# Bhasha2Code — Project Workflow

## 1. Project Identity

**Project Name:** Bhasha2Code

**Project Type:** Offline Multilingual AI Coding & Study Assistant

**Primary Development Tool:** Antigravity

**Primary Deployment Target:** Localhost Offline Production-Quality Application

**Future Target:** Optional Public Deployment

---

## 2. Project Vision

Bhasha2Code is an offline, multilingual, context-aware coding assistant that allows users to ask programming-related questions naturally in English, Hindi, Marathi, Hinglish, and mixed-language input.

The system can understand the user's language, tone, intent, programming language, and conversation context, then use a local LLM to generate, debug, explain, review, optimize, or improve code.

The system also provides persistent study sessions, saved messages, personal notes, Study Mode, and PDF export.

---

## 3. Development Philosophy

Bhasha2Code will be developed as an engineered software product, not merely as a Vibe-Coded prototype.

Antigravity may generate or modify code, but every generated implementation must be:

1. Reviewed
2. Tested
3. Verified against requirements
4. Checked for security
5. Integrated into the existing architecture

AI-generated code must never be accepted blindly.

---

# 4. Scope

## 4.1 MUST HAVE

The first production-quality version must include:

### NLP
- Multilingual input
- Language detection
- Code-switching detection
- Tone detection
- Intent classification
- Programming-language detection
- Requirement extraction

### Coding Intelligence
- Natural-language code generation
- Context-aware coding conversation
- Code debugging
- Code explanation
- Code validation
- Relevant coding suggestions
- Follow-up coding questions
- Previous-code/context awareness

### Offline AI
- Local LLM
- Ollama
- Offline operation
- Streaming responses

### Sessions
- New sessions
- Persistent chat history
- Reopen sessions
- Continue previous conversations
- Session naming
- Local storage

### Study
- Study Mode
- Important points
- Examples
- Practice questions
- Personal notes

### Export
- PDF export
- Text export

---

## 4.2 IMPORTANT

These features should be implemented after the core MVP is stable:

- Code optimization
- Code conversion
- Chat/session search
- Saved messages
- Personal notes
- Safe code sandbox
- Docker-based execution
- Code review
- Performance suggestions
- Security suggestions
- Approach suggestions
- Feature suggestions
- Best-practice suggestions

---

## 4.3 V2 / FUTURE

- Advanced test-case generation
- More programming languages
- Advanced personalization
- Advanced code analysis
- Public deployment improvements
- Advanced monitoring
- Advanced analytics

---

# 5. Supported User Languages

Initial target:

- English
- Hindi
- Marathi
- Hinglish
- Marathi-English
- Hindi-English

The architecture should allow additional languages later.

---

# 6. Initial Programming Languages

Primary:

- Python
- C
- C++
- Java
- JavaScript
- SQL

Future:

- HTML
- CSS
- PHP
- Go
- Rust

---

# 7. Core User Experience

A user should NOT need to understand technical commands or choose the correct operation manually.

The user can simply ask:

> "bhai python madhe palindrome cha code de"

or:

> "हा code slow का आहे?"

or:

> "यात error handling add कर"

or:

> "हा code simple Marathi madhe samjav"

or:

> "Python ऐवजी C++ मध्ये convert कर"

The system must determine the appropriate action from context.

---

# 8. Context-Aware Conversation

Bhasha2Code must maintain relevant conversation context.

Example:

User:

> Create a Python calculator.

Assistant:

> Generates calculator.

User:

> Add error handling.

The system must understand that "it" refers to the previously generated calculator.

Context can include:

- Previous user messages
- Previous assistant responses
- Current code
- Programming language
- Detected intent
- User language
- User tone
- Current session
- Relevant saved context

---

# 9. Suggestion System

The assistant may provide relevant development suggestions when useful.

Example:

> Suggestions:
> - Add input validation.
> - Handle division by zero.
> - Use functions for better organization.

Suggestions must be:

- Relevant
- Concise
- Technically justified
- Non-intrusive

The assistant must not generate unnecessary suggestions on every response.

---

# 10. Offline Requirement

The core application must work without internet after required models and dependencies are installed.

Offline components include:

- Web UI
- Backend
- NLP pipeline
- Local LLM
- Database
- Chat history
- Study Mode
- PDF export
- Code validation
- Local code execution sandbox

No mandatory cloud AI API is allowed for the core system.

---

# 11. High-Level Architecture

```text
User
  ↓
Offline Web UI
  ↓
FastAPI Backend
  ↓
NLP Pipeline
  ├── Language Detection
  ├── Tone Detection
  ├── Intent Classification
  ├── Programming Language Detection
  └── Requirement Extraction
  ↓
Context Manager
  ↓
Prompt Builder
  ↓
Ollama
  ↓
Local Coding LLM
  ↓
Code / Answer / Explanation / Suggestions
  ↓
Code Validator
  ↓
Response Formatter
  ↓
User
```

Supporting services:

```text
SQLite
Session Manager
PDF Generator
Safe Code Sandbox
Docker
```

---

# 12. Development Workflow

Bhasha2Code will follow these 18 phases:

1. Idea
2. Research
3. User Definition
4. PRD
5. Technology Stack
6. Architecture
7. Design
8. Rules
9. Task Breakdown
10. Setup
11. Development
12. Testing
13. Security Review
14. Code Review
15. Preview Development
16. QA Testing
17. Production Deployment
18. Monitoring

---

# 13. Standard Phase Structure

Each phase must document:

1. Purpose
2. Goal
3. Inputs
4. Current Context
5. Decisions
6. Requirements / Specifications
7. Deliverables
8. Tools / Technologies
9. Risks & Open Questions
10. Acceptance Criteria
11. Validation / Evidence
12. Status
13. Next Step

Phase-specific sections may be added where necessary.

---

# 14. Phase Completion Rule

A phase is not considered complete merely because files were created.

A phase is complete only when:

- Required deliverables exist
- Decisions are documented
- Acceptance criteria are satisfied
- Relevant work is validated
- Open blockers are recorded
- Next phase has enough information to start

---

# 15. Traceability

Requirements must remain traceable throughout development.

Example:

```text
PRD Requirement
      ↓
Architecture Component
      ↓
Development Task
      ↓
Implementation
      ↓
Test
      ↓
QA
      ↓
Production
```

Requirement IDs should be used when practical.

Example:

```text
FR-001 = Multilingual Input
FR-002 = Code Generation
FR-003 = Debugging
```

---

# 16. Source of Truth

Priority of project documentation:

1. Current approved PRD
2. Architecture
3. RULES.md
4. Task breakdown
5. Implementation documentation
6. Code

If implementation conflicts with an approved requirement, the conflict must be identified rather than silently ignored.

---

# 17. Phase 0 Definition of Done

Phase 0 is complete when:

- Project identity is locked
- Scope is locked
- MUST HAVE features are defined
- IMPORTANT features are defined
- V2 features are defined
- Development tool is defined
- Deployment target is defined
- Workflow is defined
- Documentation standards are defined
- Coding rules are defined
- Security principles are defined
- Testing principles are defined
- Antigravity operating rules are defined

---

# 18. Next Phase

After Phase 0 is approved:

**Phase 1 — Idea & Problem Definition**

will define the problem, motivation, solution, USP, objectives, non-goals, and success criteria in detail.