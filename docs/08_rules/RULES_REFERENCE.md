# Bhasha2Code — Rules Reference

## Phase 8 — Development Rules Reference

**Project:** Bhasha2Code  
**Phase:** 8 — Rules  
**Version:** 1.0  
**Status:** COMPLETE  
**Primary Development Tool:** Antigravity

---

# 1. Purpose

This document provides the operational development rules for Bhasha2Code.

The root-level `RULES.md` acts as the project constitution.

This document converts those principles into practical rules that developers and Antigravity should follow during implementation.

---

# 2. Rule Priority

When making a technical decision, use this priority:

```text id="kg8m4p"
Security
   ↓
Correctness
   ↓
Approved Architecture
   ↓
PRD Requirements
   ↓
User Experience
   ↓
Performance
   ↓
Maintainability
   ↓
Development Speed
```

Fast implementation must never override security or correctness.

---

# 3. Golden Rule

> **Inspect first. Change second. Verify third.**

Before modifying code:

```text id="ml7g4x"
Read
↓
Understand
↓
Plan
↓
Modify
↓
Test
↓
Review
```

---

# 4. Antigravity Operating Rule

Antigravity must not treat the repository as an empty project.

Before implementing a feature it must inspect:

```text id="k1d3yq"
README.md
PROJECT_WORKFLOW.md
RULES.md
Relevant PRD
Relevant Architecture
Relevant Design
Existing Source Code
Existing Tests
```

Only the relevant documents need to be loaded for each task.

---

# 5. No Unnecessary Rewrite

If a working module already exists:

```text id="7l0rmw"
DO NOT
replace the entire module

WITHOUT
a clear technical reason.
```

Preferred:

```text id="5o5l3z"
Reuse
↓
Extend
↓
Refactor carefully
```

---

# 6. No Duplicate Components

Before creating a:

- Function
- Class
- Service
- Utility
- API route
- React component

check whether equivalent functionality already exists.

Prefer reuse.

---

# 7. Requirement Traceability

Major implementation work should map to a requirement.

Example:

```text id="h6r8z0"
FR-007
Code Generation
↓
Task
↓
Implementation
↓
Test
```

Unplanned major features must not silently enter V1.

---

# 8. Scope Rule

Feature priority:

```text id="y7x2p9"
MUST HAVE
   ↓
IMPORTANT
   ↓
V2
```

Do not implement a V2 feature while a critical MUST HAVE feature remains broken.

---

# 9. Architecture Rule

Each feature must have a clear home.

```text id="dj3x8c"
NLP
→ backend/nlp/

Context
→ backend/context/

LLM
→ backend/llm/

Code
→ backend/code_engine/

Sandbox
→ backend/sandbox/

Database
→ backend/database/

API
→ backend/api/

Study
→ backend/study/

Export
→ backend/export/
```

---

# 10. Layering Rule

Use:

```text id="qy4atd"
Frontend
↓
API
↓
Service
↓
Domain Component
↓
Repository / External Service
```

Avoid:

```text id="97x8ns"
Frontend
↓
Database
```

or:

```text id="m1k0j8"
API Route
↓
500 lines of business logic
```

---

# 11. Frontend Rules

Frontend:

```text id="44t4n8"
React + Vite
```

The frontend must:

- Communicate with FastAPI
- Maintain UI state
- Display responses
- Manage user interaction

The frontend must NOT:

- Access SQLite directly
- Access Ollama directly
- Execute arbitrary code
- Contain backend business logic

---

# 12. UI Design Rules

The approved visual identity is:

```text id="04o9qw"
Minimalist
White-first
Professional
Study-friendly
Coding-focused
Clean
```

The UI must not become:

- Neon
- Gaming-like
- Overly colorful
- Card-heavy
- Animation-heavy
- Dashboard-heavy

---

# 13. UI Hierarchy Rule

Visual priority:

```text id="q2whg4"
Content
↓
Code
↓
Actions
↓
Metadata
```

The user should not have to search through decoration to find the important information.

---

# 14. No UI Overengineering

Do not create:

- A dashboard for simple information
- A card for every object
- A modal for every action
- A button for every internal operation
- Multiple sidebars without a strong reason

Prefer the simplest usable interface.

---

# 15. NLP Rules

The NLP layer must remain independent from the UI.

Pipeline:

```text id="l4y8dg"
Input
↓
Preprocessing
↓
Language
↓
Tone
↓
Intent
↓
Programming Language
↓
Requirement Extraction
```

---

# 16. NLP Confidence Rule

Classifiers should expose confidence where practical.

Example:

```text id="5j11c7"
Intent
+
Confidence
```

When confidence is low:

```text id="nt9j2w"
Fallback
or
Clarification
```

Do not force a low-confidence prediction into a major action.

---

# 17. Code-Switching Rule

The system must support mixed-language input as a first-class use case.

Examples:

```text id="t15ld2"
python madhe code de

हा Python code explain कर

Hindi mein error fix karo
```

Code-switching must not be treated as malformed input.

---

# 18. Programming-Language Detection Rule

Programming language may be inferred from:

```text id="0y1s9b"
User Text
+
Code
+
Syntax
+
Keywords
```

Explicit user input should have strong priority.

Conflicts should be detected rather than silently ignored.

---

# 19. Intent Rule

The UI should not force users to select intent.

The user can ask:

```text id="8d8dbp"
"हा code slow का आहे?"
```

and the system should route it to the appropriate analysis path.

---

# 20. LLM Rule

The LLM is one component of the system.

It is NOT the entire system.

The application must maintain:

```text id="s9f4jl"
NLP
+
Context
+
Prompt Builder
+
LLM
+
Validation
+
Persistence
```

---

# 21. Local LLM Rule

The default V1 model is:

```text id="x3v9c0"
Qwen2.5-Coder 3B
```

The model must remain configurable.

Do not hard-code model names throughout the codebase.

Use configuration.

---

# 22. LLM Abstraction Rule

All LLM interaction should go through an internal interface.

Example:

```text id="0f0t3g"
LLMService
├── generate()
├── stream()
├── health_check()
└── model_info()
```

The initial implementation may be:

```text id="w5g2r8"
OllamaLLMService
```

---

# 23. Prompt Rules

Prompt generation must be centralized.

Do not create many unrelated prompts across random files.

Use:

```text id="f2y8ep"
Prompt Builder
```

with reusable templates.

---

# 24. Context Rules

Context should be:

- Relevant
- Structured
- Limited
- Session-specific

Do not send the entire database history to the LLM by default.

---

# 25. Context Priority

When selecting context, prefer:

```text id="e9h1m3"
Current User Request
↓
Current Code
↓
Current Task
↓
Current Error
↓
Relevant Recent Messages
↓
Older Context
```

---

# 26. Context Integrity

A follow-up request must remain associated with the correct active session.

Example:

```text id="03x7cd"
Turn 1:
Create calculator.

Turn 2:
Add error handling.
```

`Turn 2` must not accidentally modify code from another session.

---

# 27. Code Generation Rules

Generated code must:

- Match requested language
- Match known requirements
- Be readable
- Follow basic best practices
- Avoid unnecessary complexity

The assistant should prefer simple correct code over unnecessarily clever code.

---

# 28. Code Validation Rule

LLM-generated code is not automatically considered correct.

Where possible:

```text id="j0mtzv"
Generate
↓
Validate
↓
Report Result
```

Possible result:

```text id="5b7u0n"
Validated
Validation Failed
Not Validated
Unsupported
```

---

# 29. Debugging Rule

Debugging should provide:

```text id="g7b6r2"
Problem
↓
Cause
↓
Fix
↓
Corrected Code
↓
Validation
```

Do not simply return a replacement code block without explaining the important issue.

---

# 30. Repair Loop Rule

When automated repair is enabled:

```text id="3qccj7"
Generate Fix
↓
Validate
↓
PASS
```

or:

```text id="8o4fwu"
Validate
↓
FAIL
↓
Repair
↓
Validate
```

A maximum repair attempt count is mandatory.

---

# 31. Infinite Loop Prevention

The system must not endlessly retry LLM repairs.

Example configuration:

```text id="6s1qxo"
MAX_REPAIR_ATTEMPTS = 3
```

After the limit:

```text id="6td4je"
Stop
↓
Report failure
↓
Ask for user guidance if required
```

---

# 32. Code Execution Rule

This is one of the strictest rules:

> **Generated or user-provided code must never execute directly on the host machine.**

Never do:

```python
os.system(user_code)
```

or equivalent unrestricted execution on the host.

---

# 33. Sandbox Rule

Supported code execution must go through the sandbox.

Preferred architecture:

```text id="w9x6y3"
Code
↓
Policy Check
↓
Docker
↓
Restricted Execution
```

---

# 34. Sandbox Restrictions

The execution environment must enforce, where technically practical:

```text id="c3g8n1"
Network Disabled
CPU Limit
Memory Limit
Execution Timeout
Restricted Filesystem
Non-root User
Controlled Process
```

Exact values are defined during security implementation.

---

# 35. Security Rule

Security is considered during every development phase.

Primary threats:

```text id="2l5qjv"
Prompt Injection
Command Injection
Code Execution
Sandbox Escape
Path Traversal
File Abuse
Secret Leakage
Malicious Dependencies
```

---

# 36. Prompt Injection Rule

Treat user input as untrusted data.

A user message must not be allowed to disable:

- Security controls
- Sandbox restrictions
- Application rules
- Access boundaries

---

# 37. Secret Rule

Never store secrets in:

- Source code
- Git
- Prompts
- Logs
- User-visible errors

Use:

```text id="x0yd7n"
.env
.env.example
```

---

# 38. Database Rules

Database:

```text id="u2m5cr"
SQLite
```

Database access should go through:

```text id="l9ey1a"
Repository / Data Access Layer
```

Avoid scattering SQL statements throughout services and routes.

---

# 39. Session Rules

A session must have a unique identifier.

Messages must belong to the correct session.

Session updates must preserve:

- History
- Current code
- Context
- Metadata

---

# 40. Data Loss Rule

Operations such as:

```text id="r5k1b8"
Delete Session
Clear History
Delete Note
```

must be intentionally triggered.

The application must not silently delete user content.

---

# 41. Search Rule

Search should use indexed/searchable local data.

Do not load the entire database into memory just to perform every search.

---

# 42. PDF Rule

PDF generation must be treated as an export operation.

Failure to generate a PDF must not delete or corrupt:

- Sessions
- Messages
- Notes
- Study content

---

# 43. Testing Rule

Every important feature requires tests.

Minimum expectation:

```text id="v8g4kq"
Implementation
↓
Unit Test
↓
Integration Test
```

Critical user journeys require end-to-end testing.

---

# 44. Test Pyramid

Preferred structure:

```text id="m3u8cy"
        E2E
       /   \
 Integration
   /       \
   Unit Tests
```

Most tests should remain fast unit tests.

---

# 45. NLP Testing

NLP tests must cover:

### Language

```text id="rbj2s4"
English
Hindi
Marathi
Hinglish
Mixed
```

### Intent

All initial intent categories.

### Tone

All initial tone categories.

### Programming Language

All supported languages.

---

# 46. Context Testing

Test conversations such as:

```text id="8xw5zs"
Create Python calculator
↓
Add error handling
↓
Explain in Marathi
↓
Convert to C++
```

Verify that each turn references the correct current code and task.

---

# 47. Validation Testing

Test:

```text id="j1j7hn"
Valid Code
Invalid Code
Syntax Error
Compile Error
Runtime Error
Timeout
Unsupported Language
```

---

# 48. Offline Testing

The core application must be tested with internet connectivity disabled.

Verify:

```text id="wv3b2k"
UI
NLP
LLM
Database
Sessions
Study Mode
PDF
Validation
```

where the required local dependencies are already installed.

---

# 49. Performance Testing

Measure:

- First-token latency
- Total response latency
- RAM usage
- CPU usage
- VRAM usage
- Model loading time
- Context processing time

Do not invent performance numbers.

---

# 50. Logging Rule

Logs should contain useful diagnostics without exposing sensitive information.

Good:

```text id="e1m9vu"
Request failed
Model unavailable
Validation failed
```

Avoid:

```text id="2z4m0q"
API keys
Passwords
Full sensitive user data
```

---

# 51. Dependency Rule

Before adding a dependency:

```text id="q4yn1j"
Need?
↓
Existing Solution?
↓
Offline?
↓
Maintenance?
↓
Security?
↓
Add
```

Do not add dependencies merely to save a few lines of code.

---

# 52. Version Rule

Dependencies must be intentionally managed.

Do not casually install packages globally.

Use the project environment.

---

# 53. File Organization Rule

Files must follow the approved project structure.

Avoid:

```text id="w1s2q3"
random_helper.py
final2.py
new_test.py
temp.py
old_version.py
```

Use meaningful names.

---

# 54. Naming Rule

Use clear names.

Examples:

```text id="m6d8b1"
context_manager.py
prompt_builder.py
validation_service.py
session_repository.py
```

Avoid:

```text id="q9c4w7"
helper2.py
newservice.py
tempfix.py
```

---

# 55. Function Rule

Prefer:

- Small functions
- Single responsibility
- Clear parameters
- Explicit return values

Avoid giant functions containing multiple unrelated responsibilities.

---

# 56. Service Rule

Services should coordinate business operations.

They should not become dumping grounds for unrelated functionality.

---

# 57. API Route Rule

API routes should remain thin.

Preferred:

```text id="l9a3k2"
Route
↓
Service
↓
Component
```

Avoid:

```text id="c8p1f4"
Route
↓
NLP
↓
LLM
↓
DB
↓
Validation
↓
Everything in one file
```

---

# 58. Error Handling Rule

Never silently swallow an error.

Bad:

```python
try:
    ...
except:
    pass
```

Better:

```text id="7p5r2v"
Catch expected error
↓
Log useful details
↓
Return safe response
```

---

# 59. Error Message Rule

User-facing errors must be understandable.

Example:

```text id="2h9w6n"
The local model is unavailable.
Please start Ollama and try again.
```

Do not expose raw stack traces to normal users.

---

# 60. Git Rules

Use meaningful commits.

Examples:

```text id="f4a9u8"
feat: add multilingual intent classifier
feat: add session context manager
feat: integrate ollama
fix: preserve context after reopening session
test: add debugging workflow tests
docs: update architecture
refactor: simplify prompt builder
```

---

# 61. Branch Rules

Use:

```text id="6r2d8x"
main
feature/*
fix/*
```

Do not push unfinished experimental work directly into `main`.

---

# 62. Commit Rule

A commit should represent a meaningful change.

Avoid:

```text id="qj5z7k"
update
changes
final
final2
test123
```

---

# 63. Code Review Rule

Before merging a significant feature, verify:

```text id="1xd5p0"
Requirement
Correctness
Security
Tests
Architecture
Performance
Maintainability
```

---

# 64. Antigravity Prompt Rule

Prompts given to Antigravity should specify:

```text id="n6q1d3"
Goal
Context
Files to Inspect
Constraints
Expected Output
Acceptance Criteria
```

Example structure:

```text id="45f3i2"
Goal:
Implement intent classification.

Inspect:
backend/nlp/
docs/04_prd/PRD.md
docs/06_architecture/ARCHITECTURE.md

Constraints:
Use TF-IDF + Logistic Regression.
Do not add transformer dependencies.

Acceptance:
Classifier predicts initial intents.
Tests pass.
```

---

# 65. Antigravity Change Rule

When Antigravity finishes a task, it should report:

```text id="8o1v7c"
Files Changed
What Changed
Why
Tests Added
Tests Passed
Known Issues
Next Step
```

---

# 66. No Fake Completion Rule

Never report:

```text id="j7d2k4"
Production Ready
Secure
Fully Tested
Offline Verified
```

without evidence.

Use accurate language:

```text id="e5p8x1"
Implemented
Unit Tested
Integration Tested
Manually Verified
Offline Verified
Production Candidate
```

---

# 67. Documentation Update Rule

A change that affects:

- Architecture
- API
- Database
- UI
- Security
- Requirements

must update the relevant documentation.

---

# 68. Change Impact Rule

Before modifying a shared component, identify its consumers.

Example:

```text id="f1a7c9"
context_manager.py
        ↓
ChatService
DebugService
StudyService
```

A change to Context Manager must consider all consumers.

---

# 69. Backward Compatibility Rule

A change should not silently break existing sessions, APIs, or important UI flows.

When breaking a contract is necessary:

```text id="h6y9w2"
Identify
↓
Document
↓
Update Consumers
↓
Test
```

---

# 70. Research Integrity Rule

Never fabricate:

- Accuracy
- Latency
- Code success rate
- User-study results
- Benchmark scores
- Research conclusions

All experimental claims must come from actual experiments.

---

# 71. Academic Integrity

When citing research:

- Use the original source where practical
- Preserve correct paper metadata
- Do not fabricate citations
- Clearly distinguish published work from preprints
- Do not claim novelty without evidence

---

# 72. Product vs Research Rule

A feature can exist because it is useful to users without being claimed as novel research.

Example:

```text id="c1w8y3"
PDF Export
→ Product Feature

Multilingual Code-Mixed Evaluation
→ Research Component
```

Do not convert every product feature into a research novelty claim.

---

# 73. Scope Protection Rule

When a new idea appears:

```text id="6ckx2p"
New Idea
↓
Check PRD
↓
Check Scope
↓
MUST / IMPORTANT / V2
↓
Document Decision
```

Do not automatically implement every new idea.

---

# 74. Performance Rule

Avoid unnecessary:

- LLM calls
- Repeated model loads
- Duplicate preprocessing
- Large context prompts
- Database scans
- Expensive sandbox startups

---

# 75. Local Hardware Rule

The target environment is resource-constrained.

Therefore:

```text id="9k1s7v"
Small model first
+
Measured performance
+
Controlled context
+
Efficient services
```

Do not assume unlimited compute.

---

# 76. Model Rule

Do not assume a larger local model is always better.

Evaluate:

```text id="8w7d3c"
Quality
Latency
RAM
VRAM
Context
Multilingual Capability
```

before changing the default model.

---

# 77. Offline Rule

Core functionality must work without internet after installation and model setup.

No mandatory cloud services may be introduced into:

```text id="2p5m8x"
Chat
NLP
LLM
Sessions
Study
PDF
```

---

# 78. External Network Rule

The application should not silently send user code or conversation content to external services.

Any future online integration must be explicit and separately documented.

---

# 79. Feature Suggestion Rule

Suggestions should be generated only when contextually useful.

Do not append generic:

```text id="f8j2l6"
"You could also add..."
```

to every answer.

---

# 80. Study Mode Rule

Study Mode should promote understanding.

The system should support:

```text id="n1v5q7"
Explanation
+
Examples
+
Important Points
+
Common Mistakes
+
Practice
+
Quiz
```

Avoid making Study Mode only a code generator.

---

# 81. Beginner-Friendly Rule

When the user requests a simple explanation:

```text id="w4m0t3"
Use simpler language
+
Shorter steps
+
Concrete examples
```

Technical detail should remain available when requested.

---

# 82. Response Rule

The response format should depend on intent.

Example:

```text id="g3r8k2"
Generate
→ Code + Brief Explanation

Debug
→ Problem + Cause + Fix + Code

Explain
→ Explanation

Security
→ Risk + Mitigation

Performance
→ Bottleneck + Improvement
```

---

# 83. No Unnecessary Hallucination

When the system does not know something:

```text id="c8j4m6"
State uncertainty
```

Do not invent APIs, libraries, compiler results, or validation status.

---

# 84. Production Rule

Before production packaging:

```text id="y8f6p1"
Development
↓
Testing
↓
Security Review
↓
Code Review
↓
Preview
↓
QA
↓
Production
```

Critical gates cannot be skipped.

---

# 85. Definition of Done

A feature is DONE only when:

```text id="d0g9w2"
Requirement Identified
        +
Implementation Complete
        +
Tests Pass
        +
Security Considered
        +
Documentation Updated
        +
Manual Verification Complete
        +
No Known Critical Blocker
```

---

# 86. Forbidden Practices

The following are prohibited:

```text id="n7c2s4"
❌ Direct host execution of generated code
❌ Hard-coded secrets
❌ Blind large-scale rewrites
❌ Duplicate functionality
❌ Fake benchmark results
❌ Fake completion claims
❌ Unnecessary dependencies
❌ Random file creation
❌ Uncontrolled LLM repair loops
❌ Silent data deletion
❌ Cloud dependency in offline core
❌ Bypassing security controls
```

---

# 87. Final Antigravity Checklist

Before completing a task:

```text id="7a4m2x"
[ ] Did I inspect existing code?
[ ] Did I inspect relevant documentation?
[ ] Am I following the architecture?
[ ] Am I following the PRD?
[ ] Did I avoid duplicate logic?
[ ] Did I avoid unnecessary rewrites?
[ ] Did I add tests?
[ ] Did I consider security?
[ ] Did I verify the implementation?
[ ] Did I update documentation if needed?
[ ] Did I report known issues honestly?
```

---

# 88. Phase 8 Acceptance Criteria

- [x] Rule priority defined
- [x] Antigravity operating rules defined
- [x] Architecture rules defined
- [x] UI rules defined
- [x] NLP rules defined
- [x] LLM rules defined
- [x] Context rules defined
- [x] Code-generation rules defined
- [x] Validation rules defined
- [x] Sandbox rules defined
- [x] Security rules defined
- [x] Database rules defined
- [x] Session rules defined
- [x] Testing rules defined
- [x] Git rules defined
- [x] Documentation rules defined
- [x] Research integrity rules defined
- [x] Performance rules defined
- [x] Offline rules defined
- [x] Scope-control rules defined
- [x] Forbidden practices defined
- [x] Antigravity completion checklist defined

---

# 89. Phase 8 Status

**STATUS: COMPLETE**

The project now has a formal operational rule layer for AI-assisted development.

The root `RULES.md` remains the project constitution.

This document serves as the detailed implementation reference.

---

# 90. Next Phase

## Phase 9 — Task Breakdown

The next phase converts the approved product into executable development work:

```text id="t9n4k1"
Epic
↓
Feature
↓
Task
↓
Subtask
↓
Dependency
↓
Acceptance Criteria
↓
Status
```

The objective is to give Antigravity small, controlled, testable tasks instead of asking it to build the entire application in one prompt.