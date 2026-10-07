# Bhasha2Code — Product Requirements Document

## Phase 4 — Product Requirements Document

**Project:** Bhasha2Code  
**Document:** PRD.md  
**Version:** 1.0  
**Status:** APPROVED FOR TECHNICAL DESIGN  
**Primary Development Tool:** Antigravity  
**Primary Deployment Target:** Localhost Offline Production-Quality Application

---

# 1. Purpose

This Product Requirements Document defines what Bhasha2Code must do, how users should interact with it, and how feature completion will be verified.

This document converts the findings from:

```text
Idea
+
Research
+
User Definition
```

into concrete product requirements.

---

# 2. Product Vision

Bhasha2Code is an offline, multilingual, context-aware AI coding and study assistant.

The system should allow a user to communicate naturally in:

- English
- Hindi
- Marathi
- Hinglish
- Hindi-English
- Marathi-English

and receive coding assistance through a local LLM.

The application must support:

```text
Generate
Explain
Debug
Review
Optimize
Convert
Suggest
Learn
Save
Continue
Export
```

without requiring the user to understand internal system operations.

---

# 3. Product Goals

## G1 — Natural Coding Interaction

Allow users to ask programming questions naturally instead of requiring structured prompts.

## G2 — Multilingual Understanding

Support the initial Indian multilingual and code-switched input categories.

## G3 — Context Awareness

Maintain relevant coding context across follow-up messages.

## G4 — Reliable Code Assistance

Validate generated code where technically possible.

## G5 — Offline Operation

Provide core coding functionality through local components.

## G6 — Learning Support

Combine coding assistance with Study Mode and persistent study sessions.

## G7 — Safe Execution

Never execute generated code directly on the production host.

---

# 4. Product Scope

## 4.1 MUST HAVE 🔴

### NLP

- Multilingual input
- Language detection
- Intent classification
- Tone classification
- Programming-language detection
- Requirement extraction

### Coding

- Code generation
- Context-aware coding conversation
- Debugging
- Code explanation
- Code validation

### Offline

- Local LLM
- Ollama
- Local NLP
- Local database

### Sessions

- Create session
- Reopen session
- Continue session
- Rename session
- Delete session
- Persistent history

### Study

- Study Mode
- Personal notes

### Export

- PDF export

---

# 5. IMPORTANT 🟠

- Code optimization
- Code conversion
- Chat search
- Saved messages
- Safe code sandbox
- Docker
- Code review
- Performance suggestions
- Security suggestions
- Approach suggestions
- Feature suggestions

---

# 6. V2 / FUTURE 🟢

- Advanced test generation
- Additional programming languages
- Advanced personalization
- Advanced analytics
- Public deployment improvements
- Advanced monitoring

---

# 7. Target Users

Primary:

```text
Engineering Students
Beginner Programmers
Intermediate Student Developers
```

Secondary:

```text
Self-Learners
Hackathon Participants
Beginner Developers
```

---

# 8. Supported User Languages

Initial:

```text
ENGLISH
HINDI
MARATHI
HINGLISH
HINDI_ENGLISH
MARATHI_ENGLISH
```

The architecture must allow future language expansion.

---

# 9. Supported Programming Languages

## V1

```text
Python
C
C++
Java
JavaScript
SQL
```

## Future

```text
HTML
CSS
PHP
Go
Rust
```

---

# 10. Tone Categories

The system should initially support:

```text
CASUAL
FORMAL
SIMPLE
TECHNICAL
SHORT
DETAILED
```

Tone should affect communication style, not technical correctness.

---

# 11. Intent Categories

Initial intent taxonomy:

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

The classifier may map multiple closely related intents into an action group internally.

---

# 12. Functional Requirements

# FR-001 — Multilingual Input

### Requirement

The application shall accept coding questions written in supported languages and code-switched combinations.

### Examples

```text
python madhe calculator banav

Python mein calculator ka code do

Create a Python calculator

हा code error का देतोय?

python madhe हा program optimize kar
```

### Acceptance Criteria

- Input is accepted without requiring English.
- Supported language categories are detected.
- Mixed-language input does not crash the pipeline.
- The detected language is made available to downstream components.

---

# FR-002 — Language Detection

### Requirement

The system shall identify the dominant user language and relevant code-switching behavior.

### Acceptance Criteria

For representative test inputs:

- language is correctly classified
- mixed-language inputs are identified where possible
- uncertain cases are handled gracefully

---

# FR-003 — Intent Classification

### Requirement

The system shall determine the user's likely coding intent.

### Example

```text
"code de"
→ GENERATE_CODE

"error ka aa raha hai?"
→ DEBUG_CODE / ERROR_EXPLANATION

"simple Marathi madhe explain kar"
→ EXPLAIN_CODE

"ha slow ka aahe?"
→ PERFORMANCE_ANALYSIS
```

### Acceptance Criteria

- Intent is predicted before final response generation.
- Unknown/ambiguous intent is handled safely.
- The pipeline does not crash when confidence is low.

---

# FR-004 — Tone Classification

### Requirement

The system shall identify the preferred communication style.

### Acceptance Criteria

A user's style can influence:

- Explanation complexity
- Response length
- Formality
- Language style

Technical correctness must remain unchanged.

---

# FR-005 — Programming Language Detection

### Requirement

The system shall identify the requested or existing programming language.

### Examples

```text
Python
C
C++
Java
JavaScript
SQL
```

### Acceptance Criteria

- Explicit language mentions are detected.
- Code blocks can provide additional evidence.
- Conflicting information is handled safely.

---

# FR-006 — Requirement Extraction

### Requirement

The system shall extract relevant coding requirements from natural-language requests.

Potential fields:

```text
Task
Programming Language
Inputs
Outputs
Constraints
Features
Error Handling
Optimization Requirement
Conversion Target
```

### Acceptance Criteria

Extracted requirements are available to the prompt builder.

---

# FR-007 — Code Generation

### Requirement

The system shall generate code using a local coding LLM.

### Input

```text
User Requirement
+
NLP Metadata
+
Relevant Context
```

### Output

```text
Explanation
+
Code
+
Relevant Suggestions
```

### Acceptance Criteria

- Correct programming language is used.
- The request is reflected in the generated code.
- Output is displayed clearly.
- Code can be validated.

---

# FR-008 — Context-Aware Conversation

### Requirement

The system shall preserve relevant context during an active session.

### Example

```text
Turn 1:
Create a Python calculator.

Turn 2:
Add error handling.

Turn 3:
Explain it in Marathi.

Turn 4:
Convert it to C++.
```

### Acceptance Criteria

The system correctly understands references to:

- Previous code
- Current task
- Programming language
- Previous modifications

without unnecessary repetition by the user.

---

# FR-009 — Context Management

### Requirement

The system shall maintain structured coding context.

Possible context:

```text
Session ID
Current Task
Current Code
Programming Language
Recent Messages
Intent
User Language
User Tone
Requirements
```

Context should be selectively included in LLM prompts.

---

# FR-010 — Code Explanation

### Requirement

The system shall explain code at the requested level.

Possible explanation modes:

```text
Simple
Technical
Short
Detailed
Language-specific
Line-by-line
Concept-based
```

### Acceptance Criteria

Explanation must correspond to the current code.

---

# FR-011 — Debugging

### Requirement

The system shall analyze code and errors and suggest or generate corrections.

### Workflow

```text
Code
+
Error / Failure
↓
Analyze
↓
Identify Cause
↓
Explain
↓
Generate Fix
↓
Validate
```

### Acceptance Criteria

The assistant should provide:

1. Error/cause
2. Location where possible
3. Recommended fix
4. Corrected code where appropriate

---

# FR-012 — Code Validation

### Requirement

Generated or modified code shall be validated using deterministic mechanisms where available.

Examples:

```text
Python → AST / interpreter checks
C/C++ → compiler
Java → javac
JavaScript → syntax/runtime checks
SQL → parser/database validation where practical
```

### Acceptance Criteria

System clearly distinguishes:

```text
Validated
Not validated
Validation failed
```

It must not represent untested code as guaranteed correct.

---

# FR-013 — Code Optimization

### Requirement

The system should identify meaningful opportunities for:

- Performance
- Memory
- Readability
- Maintainability

### Acceptance Criteria

Optimization suggestions should explain the reason for the proposed change.

---

# FR-014 — Code Conversion

### Requirement

The system should convert supported code between supported programming languages where practical.

Example:

```text
Python → C++
Python → Java
C++ → Python
```

### Acceptance Criteria

- Target language is identified.
- Functional intent is preserved as far as practical.
- Converted code is presented separately from source code.
- Validation is attempted where supported.

---

# FR-015 — Code Review

### Requirement

The system should review code for:

- Correctness
- Readability
- Maintainability
- Security
- Performance
- Structure

---

# FR-016 — Context-Aware Coding Questions

### Requirement

The user shall be able to ask unrestricted coding questions without selecting a predefined button.

Examples:

```text
हा approach योग्य आहे का?

हा code slow का आहे?

loop ऐवजी काय वापरता येईल?

memory जास्त का वापरते?

हा production साठी safe आहे का?

माझ्या project मध्ये पुढे काय feature add करू?
```

### Acceptance Criteria

The system classifies the request and responds appropriately.

---

# FR-017 — Suggestions

### Requirement

The system may provide relevant coding suggestions.

Categories:

```text
Performance
Security
Best Practice
Architecture
Error Handling
Testing
Feature Improvement
```

### Acceptance Criteria

Suggestions:

- Are relevant
- Are concise
- Are actionable
- Do not appear unnecessarily

---

# FR-018 — Persistent Sessions

### Requirement

Sessions shall persist locally.

Operations:

```text
Create
Open
Rename
Continue
Delete
```

---

# FR-019 — Session Context Reopening

### Requirement

A reopened session shall restore sufficient relevant context to continue the conversation.

### Acceptance Criteria

Example:

```text
Close session
↓
Reopen session
↓
Ask:
"add login validation"
```

The system should associate the request with the reopened coding context.

---

# FR-020 — Chat History

### Requirement

Conversation messages shall be stored locally.

Each message should support metadata such as:

```text
Message ID
Session ID
Role
Content
Timestamp
Intent
Language
Programming Language
```

---

# FR-021 — Saved Messages

### Requirement

Users should be able to save important assistant/user messages for later reference.

---

# FR-022 — Personal Notes

### Requirement

Users should be able to create notes associated with sessions or study topics.

---

# FR-023 — Study Mode

### Requirement

Study Mode shall provide structured learning assistance.

Preferred structure:

```text
Topic
↓
Explanation
↓
Examples
↓
Important Points
↓
Common Mistakes
↓
Practice Questions
↓
Mini Quiz
```

---

# FR-024 — PDF Export

### Requirement

The user shall be able to export a session or selected study/coding material to PDF.

PDF should contain:

- Title
- Session/topic
- Conversation or selected content
- Code formatting where practical
- Timestamp
- Optional notes

---

# FR-025 — Offline LLM

### Requirement

Core coding interaction shall use a local LLM.

The application shall communicate with the local model service rather than requiring a cloud AI API.

---

# FR-026 — Local Database

### Requirement

The initial application shall use SQLite for persistent local data.

---

# FR-027 — Safe Code Sandbox

### Requirement

Generated code must not execute directly on the host system.

Execution shall use a controlled sandbox.

Minimum controls:

```text
Timeout
CPU Limit
Memory Limit
Restricted Filesystem
No Network
Controlled Process
```

---

# FR-028 — Docker Execution

### Requirement

Docker should be used as the preferred production sandbox mechanism for supported code execution.

---

# FR-029 — Error Recovery

### Requirement

The application shall handle failures involving:

- LLM unavailable
- Model loading failure
- Invalid input
- Database failure
- Validation failure
- Sandbox failure
- PDF generation failure

The user must receive an understandable error message.

---

# FR-030 — Local Monitoring

### Requirement

The application should record useful local operational metrics in later phases.

Potential metrics:

```text
Response Latency
First Token Latency
LLM Errors
API Errors
Memory
CPU
GPU
Validation Result
Debug Success
```

---

# 13. Non-Functional Requirements

# NFR-001 — Offline Availability

After installation and model setup, the core application must operate without internet access.

---

# NFR-002 — Performance

The application should provide reasonable response latency for the selected local model and hardware.

Performance targets must be measured during implementation rather than invented.

---

# NFR-003 — Reliability

Critical application paths should fail gracefully.

---

# NFR-004 — Security

The system must protect against:

- Prompt injection
- Command injection
- Unsafe code execution
- Sandbox escape
- File-system abuse
- Secret leakage
- Malicious input

---

# NFR-005 — Maintainability

Code should follow the architecture and project rules defined in `RULES.md`.

---

# NFR-006 — Scalability

The architecture should allow future replacement of:

- Local LLM
- Frontend
- NLP classifiers
- Database
- Sandbox

without rewriting the entire application.

---

# NFR-007 — Extensibility

New languages and intents should be addable without major architectural changes.

---

# NFR-008 — Privacy-Oriented Operation

Coding content, sessions, and notes should remain local during normal offline operation.

No stronger privacy/security guarantee may be claimed unless technically verified.

---

# NFR-009 — Usability

A beginner should be able to start a coding conversation without understanding internal NLP or LLM terminology.

---

# 14. User Stories

## US-001

**As a student,**  
I want to ask coding questions in Marathi, Hindi, Hinglish, or English  
**so that** I can communicate naturally.

### Acceptance

Supported multilingual inputs produce an appropriate response.

---

## US-002

**As a student,**  
I want the assistant to remember my current code  
**so that** I do not need to paste it again.

---

## US-003

**As a beginner,**  
I want my error explained simply  
**so that** I understand why the code failed.

---

## US-004

**As a learner,**  
I want explanations in simple language  
**so that** I can understand programming concepts.

---

## US-005

**As a developer,**  
I want performance and security suggestions  
**so that** I can improve my code.

---

## US-006

**As a user,**  
I want to close and reopen a coding session  
**so that** I can continue later.

---

## US-007

**As a student,**  
I want Study Mode  
**so that** I can learn a topic systematically.

---

## US-008

**As a user,**  
I want to export important coding/study content to PDF  
**so that** I can keep it offline.

---

# 15. Edge Cases

## EC-001 — Unknown Language

Input:

```text
"make this thing work"
```

System should not fail simply because the programming language is missing.

It may ask for clarification only when necessary.

---

## EC-002 — Mixed Languages

Input may contain:

```text
Marathi + English + code
Hindi + English + code
```

System must continue processing.

---

## EC-003 — Ambiguous Intent

Example:

```text
"python code"
```

The system may ask a concise clarification instead of guessing a major requirement.

---

## EC-004 — No Code in Debugging Request

If the user asks:

```text
"माझा code error देतोय"
```

without code/error details, system should request only the necessary missing information.

---

## EC-005 — Unsupported Programming Language

The system should explain that the requested language is not currently supported rather than generating unreliable output silently.

---

## EC-006 — Invalid Generated Code

If validation fails:

```text
Generated Code
↓
Validation Failed
↓
Debug / Repair
```

The system should not falsely report success.

---

## EC-007 — Model Unavailable

The UI should clearly communicate that the local model service is unavailable.

---

## EC-008 — Long Conversation

The system should summarize/select relevant context rather than blindly sending unlimited history to the model.

---

## EC-009 — Dangerous Code

Unsafe or potentially destructive execution requests must not be directly executed on the host.

---

## EC-010 — PDF Failure

If PDF generation fails, the conversation must not be lost.

---

# 16. Response Requirements

A standard coding response may contain:

```text
Answer
↓
Explanation
↓
Code
↓
Validation Status
↓
Suggestions
```

Not every section must appear for every query.

The response format should depend on intent.

---

# 17. Intent-to-Response Mapping

| Intent | Primary Response |
|---|---|
| GENERATE_CODE | Code + brief explanation |
| DEBUG_CODE | Cause + fix + corrected code |
| ERROR_EXPLANATION | Error explanation |
| EXPLAIN_CODE | Explanation |
| OPTIMIZE_CODE | Improved code + rationale |
| CONVERT_CODE | Converted code + notes |
| ALGORITHM | Approach + algorithm |
| CONCEPT | Concept explanation |
| CODE_REVIEW | Review findings |
| PERFORMANCE_ANALYSIS | Bottlenecks + improvements |
| SECURITY_ANALYSIS | Risks + mitigations |
| APPROACH_SUGGESTION | Recommended approach |
| BEST_PRACTICE | Relevant best practices |
| ARCHITECTURE_SUGGESTION | Architecture recommendation |
| FEATURE_SUGGESTION | Relevant feature ideas |
| TEST_CASE_GENERATION | Test cases |
| CODE_SUGGESTION | Practical coding improvements |

---

# 18. Session Requirements

Each session should conceptually contain:

```text
Session
├── Metadata
├── Messages
├── Current Code
├── Current Programming Language
├── Context
├── Saved Messages
├── Notes
└── Study Content (when applicable)
```

---

# 19. High-Level Data Entities

Initial logical entities:

```text
users
sessions
messages
saved_messages
notes
generated_code
debug_history
study_sessions
```

User accounts may remain local/simple in the initial version.

---

# 20. API Requirements

The final API design will be defined in the Architecture phase.

Initial conceptual endpoints may include:

```text
POST   /chat
POST   /sessions
GET    /sessions
GET    /sessions/{id}
PATCH  /sessions/{id}
DELETE /sessions/{id}

POST   /validate
POST   /debug

POST   /study
POST   /notes
POST   /saved-messages

GET    /search

POST   /export/pdf
GET    /health
```

These are provisional and must be reviewed during Phase 6 Architecture.

---

# 21. Offline Requirement Flow

```text
User
 ↓
Frontend
 ↓
FastAPI
 ↓
Local NLP
 ↓
Context Manager
 ↓
Ollama
 ↓
Local LLM
 ↓
Validator
 ↓
SQLite
 ↓
Frontend
```

No mandatory cloud AI dependency is allowed in this path.

---

# 22. Feature Priority Matrix

| Feature | Priority | Initial Release |
|---|---|---|
| Multilingual Input | MUST | Yes |
| Language Detection | MUST | Yes |
| Intent Detection | MUST | Yes |
| Tone Detection | MUST | Yes |
| Programming Language Detection | MUST | Yes |
| Requirement Extraction | MUST | Yes |
| Code Generation | MUST | Yes |
| Context-Aware Conversation | MUST | Yes |
| Debugging | MUST | Yes |
| Code Explanation | MUST | Yes |
| Code Validation | MUST | Yes |
| Offline LLM | MUST | Yes |
| Persistent Sessions | MUST | Yes |
| Reopen/Continue Session | MUST | Yes |
| Study Mode | MUST | Yes |
| PDF Export | MUST | Yes |
| Optimization | IMPORTANT | After core stability |
| Conversion | IMPORTANT | After core stability |
| Search | IMPORTANT | After core stability |
| Saved Messages | IMPORTANT | After core stability |
| Notes | IMPORTANT | Yes / lightweight |
| Sandbox | IMPORTANT | Before execution feature |
| Docker | IMPORTANT | With sandbox |
| Code Review | IMPORTANT | After core |
| Suggestions | IMPORTANT | Controlled rollout |
| Advanced Testing | V2 | Later |
| More Languages | V2 | Later |
| Advanced Personalization | V2 | Later |

---

# 23. MVP Definition

The MVP is:

```text
Offline UI
+
FastAPI
+
NLP Pipeline
+
Context Manager
+
Ollama
+
Local Coding LLM
+
Code Generation
+
Debugging
+
Explanation
+
Validation
+
SQLite
+
Sessions
+
Study Mode
+
PDF Export
```

The MVP should NOT require every IMPORTANT feature before a working demo exists.

---

# 24. MVP Critical Path

```text
Backend
 ↓
Database
 ↓
NLP
 ↓
Ollama
 ↓
Context
 ↓
Code Generation
 ↓
Validation
 ↓
Debugging
 ↓
Sessions
 ↓
Study
 ↓
PDF
 ↓
UI
```

---

# 25. Definition of Done — Product Level

The V1 product is complete when:

### Functional

- User can create a session.
- User can ask a multilingual coding question.
- Language and intent are processed.
- Local LLM generates a response.
- Relevant context is preserved.
- Code can be validated.
- Debugging works on supported cases.
- Code explanation works.
- Sessions persist.
- Sessions can be reopened.
- Study Mode works.
- PDF export works.

### Offline

- Core workflow works without internet.

### Security

- Generated code is not directly executed on host.
- Secrets are not exposed or committed.

### Quality

- Critical tests pass.
- Manual QA scenarios pass.
- Known critical defects are resolved.

---

# 26. PRD Constraints

The following constraints are fixed unless formally changed:

1. Core AI must be local.
2. Ollama is the initial local model-serving layer.
3. SQLite is the initial local database.
4. Antigravity is the primary vibe-coding tool.
5. Generated code must not directly execute on host.
6. MUST HAVE features take priority over V2.
7. AI-generated code must be verified.
8. No fake completion or unsupported claims.
9. Existing code must be inspected before modification.
10. Core product must remain usable offline.

---

# 27. Open Product Questions

These will be resolved in later technical phases:

### OQ-001
Which local coding model gives the best quality/performance trade-off?

### OQ-002
Should the first UI be Streamlit or a custom frontend?

### OQ-003
Which NLP classifier architecture provides sufficient accuracy with low local resource usage?

### OQ-004
How much conversation context should be retained dynamically?

### OQ-005
Which programming languages should receive sandbox execution first?

---

# 28. Phase 4 Acceptance Criteria

- [x] Product vision defined
- [x] Goals defined
- [x] Scope defined
- [x] MUST HAVE / IMPORTANT / V2 locked
- [x] Functional requirements defined
- [x] Non-functional requirements defined
- [x] User stories defined
- [x] Edge cases defined
- [x] Response requirements defined
- [x] Session requirements defined
- [x] Logical entities defined
- [x] Provisional API requirements defined
- [x] MVP defined
- [x] Product-level Definition of Done defined
- [x] Open product questions documented

---

# 29. Phase 4 Status

**STATUS: COMPLETE**

The product requirements are defined and ready to be translated into technical architecture.

---

# 30. Next Phase

## Phase 5 — Technology Stack

The next phase will finalize:

```text
Requirement
↓
Technology
↓
Why Selected
↓
Alternative
↓
Version
↓
Hardware Requirement
↓
Offline Compatibility
↓
Deployment Constraint
```

The most important decision in Phase 5 will be selecting the local coding LLM and the frontend/backend stack that can realistically run on the target machine.