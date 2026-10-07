# Bhasha2Code — Development Guide

## Phase 11 — Development

**Project:** Bhasha2Code  
**Phase:** 11 — Development  
**Version:** 1.0  
**Status:** COMPLETE  
**Primary Development Tool:** Antigravity  
**Development Target:** Localhost / Offline-first

---

# 1. Purpose

This document defines the actual implementation process for Bhasha2Code.

Development must be incremental.

The project must not be generated as one large uncontrolled AI coding task.

The implementation process is:

```text
Task
↓
Inspect
↓
Plan
↓
Implement
↓
Run
↓
Test
↓
Review
↓
Document
↓
Done
```

---

# 2. Development Principles

The development process must follow:

```text
Correctness First
Security First
Reuse Existing Code
Small Changes
Test Frequently
Document Important Changes
No Fake Completion
```

---

# 3. Development Order

The approved implementation order is:

```text
1. Backend Foundation
2. Database
3. NLP Preprocessing
4. Language Detection
5. Intent Classification
6. Tone Classification
7. Programming Language Detection
8. Requirement Extraction
9. NLP Pipeline Integration
10. Ollama Integration
11. Prompt Builder
12. Context Manager
13. Code Generation
14. Code Parser
15. Code Validation
16. Debugging
17. Explanation
18. Optimization
19. Conversion
20. Context-Aware Conversation
21. Suggestions
22. Sessions
23. Chat History
24. Saved Messages
25. Notes
26. Study Mode
27. PDF Export
28. Safe Sandbox
29. Frontend
30. API Integration
31. Streaming
32. Testing
33. Security Review
34. Code Review
35. Preview
36. QA
37. Production
```

---

# 4. Development Rule

Never skip dependencies.

Example:

```text
Context Manager
```

should not be implemented before:

```text
Database
+
Session Model
+
LLM Service
```

unless the task is specifically designed as an isolated prototype.

---

# 5. Development Milestone D01 — Backend Foundation

## Goal

Create the stable backend foundation.

Tasks:

```text
T01
T02
T03
```

Expected:

```text
FastAPI
+
Application Config
+
Health Check
+
Basic Error Handling
```

---

## Acceptance Criteria

```text
[ ] Backend starts
[ ] /health works
[ ] Configuration loads
[ ] Errors are handled
[ ] Project structure follows architecture
[ ] Basic backend tests pass
```

---

# 6. Development Milestone D02 — Database

Tasks:

```text
T05
T06
T07
```

Implement:

```text
Users
Sessions
Messages
Saved Messages
Notes
Generated Code
Debug History
```

---

## Database Architecture

```text
API
↓
Service
↓
Repository
↓
SQLAlchemy / SQLite
```

Database-specific logic should remain inside the database layer.

---

# 7. Development Milestone D03 — NLP Preprocessing

Task:

```text
T08
```

Pipeline:

```text
Raw Input
↓
Cleaning
↓
Normalization
↓
Code/Text Separation where required
↓
Normalized Input
```

Important:

Mixed-language input must remain understandable.

Example:

```text
"हा Python code explain कर"
```

must not become unusable after preprocessing.

---

# 8. Development Milestone D04 — Language Detection

Task:

```text
T09
```

Output example:

```json
{
  "language": "marathi",
  "confidence": 0.91
}
```

For mixed input:

```json
{
  "language": "marathi-english",
  "confidence": 0.84
}
```

The exact confidence value must come from the implemented detector.

---

# 9. Development Milestone D05 — Intent Classification

Tasks:

```text
T12
T13
```

Initial intents:

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

Initial architecture:

```text
Text
↓
TF-IDF
↓
Logistic Regression
↓
Intent
+
Confidence
```

---

# 10. Development Milestone D06 — Tone Classification

Tasks:

```text
T10
T11
```

Tone classes:

```text
CASUAL
FORMAL
SIMPLE
TECHNICAL
SHORT
DETAILED
```

The result should influence response style.

Example:

```text
Tone = SIMPLE
```

should produce a beginner-friendly explanation.

---

# 11. Development Milestone D07 — Programming Language Detection

Task:

```text
T14
```

Supported V1 languages:

```text
Python
C
C++
Java
JavaScript
SQL
```

Detection sources:

```text
Explicit User Request
+
Existing Code
+
Syntax
+
Keywords
+
Editor Selection
```

---

# 12. Development Milestone D08 — Requirement Extraction

Task:

```text
T15
```

Expected structured information:

```text
Task
Programming Language
Input
Output
Constraints
Error
Requested Transformation
Requested Tone
Framework
```

Missing information should remain empty rather than being fabricated.

---

# 13. Development Milestone D09 — NLP Pipeline Integration

Task:

```text
T16
```

Complete flow:

```text
User Request
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
Structured NLP Result
```

Example:

User:

```text
"python madhe palindrome check karun de simple explanation sobat"
```

Possible structured output:

```text
Language:
Marathi-English

Intent:
GENERATE_CODE

Tone:
SIMPLE

Programming Language:
Python

Task:
Palindrome Checker
```

---

# 14. Development Milestone D10 — Ollama Integration

Tasks:

```text
T17
T18
```

Architecture:

```text
Bhasha2Code Backend
        ↓
LLM Service
        ↓
Ollama
        ↓
Local Coding Model
```

The model name must come from configuration.

---

# 15. LLM Service Requirements

Minimum interface:

```python
class LLMService:
    def generate(self, prompt):
        ...

    def stream(self, prompt):
        ...

    def health_check(self):
        ...

    def model_info(self):
        ...
```

The exact implementation may differ, but responsibilities should remain separated.

---

# 16. Development Milestone D11 — Prompt Builder

Tasks:

```text
T19
T20
```

Prompt input:

```text
User Request
+
Detected Language
+
Detected Tone
+
Detected Intent
+
Programming Language
+
Current Code
+
Relevant Context
+
Error Information
```

Prompt output:

```text
Structured LLM Prompt
```

---

# 17. Prompt Separation

Use separate logical prompt templates for:

```text
Code Generation
Debugging
Explanation
Optimization
Conversion
Review
Suggestions
Study Mode
```

Do not use one giant universal prompt for every operation.

---

# 18. Development Milestone D12 — Context Manager

Tasks:

```text
T21
T22
```

The Context Manager is responsible for:

```text
Current Request
+
Current Code
+
Current Task
+
Recent Conversation
+
Relevant Session Data
```

---

# 19. Context Example

Conversation:

```text
User:
python madhe calculator bana

Assistant:
[calculator code]

User:
yat error handling add kar
```

System must understand:

```text
"yat"
=
previous calculator code
```

and modify the correct code.

---

# 20. Context Isolation

Session A:

```text
Python Calculator
```

Session B:

```text
C++ Student Management
```

A follow-up in Session B must never accidentally modify Session A.

---

# 21. Development Milestone D13 — Code Generation

Task:

```text
T23
```

Flow:

```text
User Request
↓
NLP
↓
Context
↓
Prompt Builder
↓
Local LLM
↓
Generated Response
```

Response should be structured rather than treated as arbitrary text.

---

# 22. Code Generation Output

Preferred internal structure:

```json
{
  "language": "python",
  "code": "...",
  "explanation": "...",
  "warnings": [],
  "suggestions": []
}
```

The exact schema may evolve during implementation.

---

# 23. Development Milestone D14 — Code Parser

Task:

```text
T24
```

Parser responsibilities:

```text
Detect Code Fence
Extract Code
Detect Language
Extract Explanation
Extract Warnings
Extract Suggestions
```

It must safely handle malformed LLM output.

---

# 24. Development Milestone D15 — Code Validation

Tasks:

```text
T25
T26
```

Validation:

```text
Generated Code
↓
Language Detector
↓
Language-Specific Validator
↓
Validation Result
```

Result states:

```text
VALIDATED
VALIDATION_FAILED
NOT_VALIDATED
UNSUPPORTED
```

---

# 25. Development Milestone D16 — Debugging

Tasks:

```text
T27
T28
```

Debug flow:

```text
Code
+
Error
+
Context
↓
Debug Service
↓
LLM
↓
Proposed Fix
↓
Validation
```

---

# 26. Debugging Response

The interface should prioritize:

```text
Problem
Cause
Fix
Corrected Code
Validation
```

The final validation state must be honest.

---

# 27. Automated Repair

Maximum retry count:

```text
3
```

Flow:

```text
Fix
↓
Validate
↓
PASS → Stop
FAIL
↓
Retry
```

After the maximum:

```text
Stop
+
Return failure details
```

---

# 28. Development Milestone D17 — Explanation

Task:

```text
T29
```

Explanation modes:

```text
Simple
Detailed
Technical
```

The system should explain the actual current code.

---

# 29. Development Milestone D18 — Optimization

Task:

```text
T30
```

Analyze:

```text
Time Complexity
Repeated Operations
Unnecessary Loops
Memory Use
Readability
Potential Bottlenecks
```

The system must distinguish between:

```text
Observed Issue
```

and:

```text
Possible Improvement
```

It must not present an unmeasured performance estimate as a proven result.

---

# 30. Development Milestone D19 — Code Conversion

Task:

```text
T31
```

Flow:

```text
Source Language
+
Source Code
+
Target Language
↓
LLM
↓
Converted Code
↓
Validation
```

---

# 31. Development Milestone D20 — Context-Aware Coding Conversation

Task:

```text
T32
```

This is a MUST HAVE feature.

Users are not restricted to buttons.

Examples:

```text
हा code slow का आहे?

हा approach योग्य आहे का?

याला function मध्ये convert कर.

Memory जास्त का वापरते?

हा code production साठी safe आहे का?

माझ्या project ला पुढे काय feature add करू?
```

---

# 32. Conversation Intent Routing

The system should decide whether a request requires:

```text
Code Generation
Debugging
Explanation
Optimization
Review
Performance Analysis
Security Analysis
Approach Suggestion
Feature Suggestion
General Coding Answer
```

The user should not need to manually select every operation.

---

# 33. Development Milestone D21 — Suggestion Engine

Task:

```text
T33
```

Suggestions should be context-aware.

Example:

```text
Generated Calculator

Suggestions:
1. Add input validation
2. Handle division by zero
3. Separate logic into functions
```

Do not show unrelated suggestions.

Maximum visible suggestions:

```text
3–5
```

---

# 34. Development Milestone D22 — Sessions

Tasks:

```text
T34
T35
T36
T37
```

Required:

```text
Create Session
Open Session
Rename Session
Delete Session
Continue Session
Search
```

---

# 35. Session Persistence

After application restart:

```text
Application Restart
↓
Open Session
↓
History Restored
↓
Context Restored
↓
Continue Conversation
```

---

# 36. Development Milestone D23 — Saved Messages

Task:

```text
T38
```

Actions:

```text
Save
Unsave
View Saved
```

Saved content must remain available across application restarts.

---

# 37. Development Milestone D24 — Personal Notes

Task:

```text
T39
```

Notes should support:

```text
Create
Edit
Delete
Search
```

Notes are user-owned study content and must not be silently deleted.

---

# 38. Development Milestone D25 — Study Mode

Task:

```text
T40
```

Study Mode flow:

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

# 39. Study Mode Requirements

Study Mode should be useful for:

```text
Concept Learning
Programming Practice
Assignments
Revision
Exam Preparation
```

The interface should remain minimalist.

---

# 40. Development Milestone D26 — PDF Export

Task:

```text
T41
```

PDF may include:

```text
Session Title
Messages
Code
Explanations
Validation Results
Study Content
Selected Notes
```

The export is local.

---

# 41. Development Milestone D27 — Safe Sandbox

Tasks:

```text
T42
T43
T44
```

Architecture:

```text
User / LLM Code
↓
Policy Check
↓
Docker Sandbox
↓
Restricted Execution
↓
Output
```

---

# 42. Sandbox Rules

Execution environment should enforce:

```text
No Network
CPU Limit
Memory Limit
Timeout
Restricted Filesystem
Non-root User
Controlled Process
```

Generated code must never bypass the sandbox.

---

# 43. Development Milestone D28 — Frontend Core

Tasks:

```text
T45
T46
T47
T48
T49
T50
```

Main structure:

```text
┌──────────────┬─────────────────────────────┐
│   Sidebar    │       Main Workspace        │
│              │                             │
│ New Chat     │ Conversation                │
│ Recent       │                             │
│ Saved        │ Code                        │
│ Notes        │ Explanation                 │
│ Study Mode   │ Validation                  │
│ Search       │ Suggestions                 │
│ Settings     │                             │
└──────────────┴─────────────────────────────┘
```

The layout must remain minimalist.

---

# 44. Frontend Design Rules

Use:

```text
White / soft-white
+
Subtle borders
+
Dark readable text
+
One restrained accent
```

Avoid:

```text
Neon
Heavy gradients
Large decorative cards
Excessive shadows
Animated AI graphics
```

---

# 45. Development Milestone D29 — Monaco Editor

Task:

```text
T50
```

Required:

```text
Syntax Highlighting
Line Numbers
Editing
Search
Error Markers
Language Selection
```

The editor must integrate with generated code and validation.

---

# 46. Development Milestone D30 — Validation UI

Task:

```text
T51
```

Display:

```text
✓ Validated
✕ Validation Failed
○ Not Validated
⚠ Unsupported
```

Status should not depend only on color.

---

# 47. Development Milestone D31 — Debug UI

Task:

```text
T52
```

Required visual order:

```text
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

---

# 48. Development Milestone D32 — Suggestion UI

Task:

```text
T53
```

Suggestions should be:

```text
Compact
Relevant
Readable
Dismissible where appropriate
```

---

# 49. Development Milestone D33 — Session UI

Tasks:

```text
T54
T55
T56
```

Session actions:

```text
Create
Open
Rename
Delete
Continue
```

Delete must be intentional.

---

# 50. Development Milestone D34 — Study UI

Tasks:

```text
T57
T58
```

Study interface should resemble:

```text
Digital Notebook
```

rather than:

```text
Colorful Education Dashboard
```

---

# 51. Development Milestone D35 — Search & Saved UI

Tasks:

```text
T59
T60
```

Search should support:

```text
Sessions
Messages
Saved Content
Notes
```

where appropriate.

---

# 52. Development Milestone D36 — Settings

Tasks:

```text
T61
T62
```

Settings:

```text
Appearance
AI Model
Execution
Data
```

Model status:

```text
Ready
Loading
Busy
Unavailable
Error
```

---

# 53. Development Milestone D37 — API Layer

Tasks:

```text
T63
T64
T65
T66
T67
T68
T69
T70
T71
```

Possible API groups:

```text
/chat
/debug
/explain
/optimize
/convert
/validate
/sessions
/study
/export
```

Exact endpoint names may be refined during implementation.

---

# 54. API Rule

API routes must remain thin.

Preferred:

```text
Route
↓
Service
↓
Domain Component
```

Avoid putting full LLM/NLP/database workflows directly into route handlers.

---

# 55. Development Milestone D38 — Streaming

Task:

```text
T72
```

Flow:

```text
LLM
↓
Streaming Response
↓
FastAPI
↓
Frontend
↓
Incremental Rendering
```

Streaming is important for user experience but must not break core non-streaming functionality.

---

# 56. Development Milestone D39 — End-to-End Integration

Tasks:

```text
T73
T74
```

All components must connect:

```text
Frontend
↓
FastAPI
↓
NLP
↓
Context
↓
Prompt Builder
↓
Ollama
↓
Code Engine
↓
Validation
↓
Database
↓
Frontend
```

---

# 57. MUST-HAVE Integration Test

The following journey must work:

```text
New Chat
↓
Marathi Query
↓
Generate Python Code
↓
Follow-up
↓
Add Error Handling
↓
Validate
↓
Explain in Marathi
↓
Optimize
↓
Save
↓
Close
↓
Reopen
↓
Continue
↓
Export PDF
```

This is the primary Bhasha2Code demonstration workflow.

---

# 58. Development Milestone D40 — Unit Testing

Task:

```text
T75
```

Unit test major isolated components:

```text
NLP
Language Detector
Intent Classifier
Tone Classifier
Programming Language Detector
Requirement Extractor
Context Manager
Prompt Builder
Parser
Validator
Repositories
Services
```

---

# 59. Development Milestone D41 — Integration Testing

Task:

```text
T76
```

Test:

```text
NLP → Service
Service → LLM
LLM → Parser
Parser → Validator
Session → Context
API → Database
```

---

# 60. Development Milestone D42 — E2E Testing

Task:

```text
T77
```

Test the actual user workflow from frontend to backend.

Do not rely only on unit tests.

---

# 61. Development Milestone D43 — Multilingual Testing

Task:

```text
T78
```

Required input categories:

```text
English
Hindi
Marathi
Hinglish
Marathi-English
Hindi-English
```

Example:

```text
"Python madhe list sort kar"
"Python में list reverse कैसे करें?"
"हा code explain कर"
"Write a C++ program for sorting"
```

---

# 62. Development Milestone D44 — Context Continuity Testing

Task:

```text
T79
```

Required flow:

```text
Generate
↓
Modify
↓
Explain
↓
Debug
↓
Optimize
↓
Reopen
↓
Continue
```

Correct session association is mandatory.

---

# 63. Development Milestone D45 — Security Implementation Review

Tasks:

```text
T80
T81
T82
T83
```

Review:

```text
Prompt Injection
Command Injection
Code Execution
Sandbox Escape
File Access
Path Traversal
Secret Leakage
Malicious Input
```

---

# 64. Security Development Rule

Security fixes cannot be postponed simply because the feature is working.

A feature involving code execution is not considered complete until its execution boundary has been reviewed.

---

# 65. Development Milestone D46 — Code Review

Tasks:

```text
T84
T85
T86
```

Review:

```text
Correctness
Architecture
Security
Maintainability
Performance
Dependencies
Tests
Documentation
```

---

# 66. Development Milestone D47 — Local Preview

Tasks:

```text
T87
T88
```

Production-like local environment:

```text
Frontend
+
FastAPI
+
SQLite
+
Ollama
+
Docker Sandbox
```

The environment must behave as close as practical to the intended production setup.

---

# 67. Development Milestone D48 — QA

Tasks:

```text
T89
T90
```

Test users such as:

```text
Beginner Student
Engineering Student
Programming Learner
Mixed-Language User
Debugging User
Study User
```

---

# 68. Development Milestone D49 — Production

Tasks:

```text
T91
T92
T93
T94
```

Required:

```text
Build
Configuration
Startup
Recovery
Backup
Docker Compose
```

---

# 69. Development Milestone D50 — Monitoring

Tasks:

```text
T95
T96
```

Track locally:

```text
Response Latency
First Token Latency
LLM Errors
API Errors
CPU
RAM
GPU where available
Database Errors
Validation Results
```

---

# 70. Development Workflow for Antigravity

For every task:

```text
1. Read TASK ID
2. Inspect existing implementation
3. Read relevant project documents
4. Identify affected files
5. Describe intended change
6. Implement minimum required change
7. Run tests
8. Inspect failures
9. Fix only relevant issues
10. Report result
```

---

# 71. Antigravity Prompt Template

Use:

```text
Implement TASK TXX from docs/09_task_breakdown/TASKS.md.

Before editing:
1. Inspect the existing repository.
2. Inspect relevant documentation.
3. Identify existing reusable components.
4. Identify affected files.

Constraints:
- Follow RULES.md.
- Follow ARCHITECTURE.md.
- Follow DESIGN.md where UI is involved.
- Do not rewrite working modules unnecessarily.
- Do not introduce unnecessary dependencies.
- Do not change unrelated features.

Implementation:
<task-specific requirement>

Acceptance Criteria:
<task criteria>

Testing:
<tests to run>

At completion report:
1. Files changed
2. What changed
3. Tests run
4. Test result
5. Known issues
6. Documentation affected
```

---

# 72. Small-Task Rule

Prefer:

```text
Implement language detection
```

over:

```text
Implement the complete NLP system.
```

Prefer:

```text
Create session repository
```

over:

```text
Build all session management.
```

Small tasks produce easier reviews and safer AI-assisted development.

---

# 73. Commit Strategy

After a meaningful stable task:

```bash
git add .
git commit -m "feat: implement language detection"
```

Use meaningful commit messages.

Do not wait until dozens of unrelated changes accumulate.

---

# 74. Development Checkpoint

After each major milestone:

```text
Code
↓
Tests
↓
Git Commit
↓
Documentation Update
↓
Next Milestone
```

---

# 75. Rollback Strategy

If a task introduces serious regression:

```text
Stop
↓
Identify Last Known Good Commit
↓
Inspect Change
↓
Revert / Fix
↓
Run Tests
↓
Continue
```

Never build additional features on top of a broken core.

---

# 76. No Scope Creep Rule

During development, new ideas must be classified:

```text
MUST HAVE
IMPORTANT
V2
```

Do not interrupt the current critical path for a non-critical idea.

---

# 77. Development Quality Gates

## Gate 1 — Backend

```text
FastAPI works
Database works
Tests pass
```

## Gate 2 — AI

```text
NLP works
Ollama works
Prompt Builder works
Context works
```

## Gate 3 — Coding

```text
Generate
Debug
Explain
Validate
```

## Gate 4 — Persistence

```text
Sessions
History
Reopen
Save
Notes
```

## Gate 5 — Safety

```text
Sandbox
Security Tests
```

## Gate 6 — Product

```text
Frontend
Integration
Study
PDF
```

## Gate 7 — Release

```text
Testing
Review
QA
Production
```

---

# 78. Definition of Done

A development feature is complete only if:

```text
[ ] Requirement mapped
[ ] Dependency satisfied
[ ] Existing implementation inspected
[ ] Code implemented
[ ] Tests written/updated
[ ] Tests pass
[ ] Error handling considered
[ ] Security considered
[ ] Documentation updated if required
[ ] No critical regression
[ ] Git checkpoint created
```

---

# 79. Development Completion Condition

The application is considered development-complete only when the complete MUST-HAVE workflow works:

```text
Multilingual Input
        ↓
NLP Detection
        ↓
Intent / Tone Detection
        ↓
Programming Language Detection
        ↓
Context Manager
        ↓
Offline LLM
        ↓
Code Generation
        ↓
Validation
        ↓
Debugging
        ↓
Explanation
        ↓
Persistent Session
        ↓
Reopen / Continue
        ↓
Study Mode
        ↓
PDF Export
```

---

# 80. Phase 11 Acceptance Criteria

- [x] Development order defined
- [x] Backend implementation flow defined
- [x] Database implementation flow defined
- [x] NLP implementation flow defined
- [x] LLM integration flow defined
- [x] Prompt builder flow defined
- [x] Context manager flow defined
- [x] Code generation flow defined
- [x] Validation flow defined
- [x] Debugging flow defined
- [x] Explanation flow defined
- [x] Optimization flow defined
- [x] Conversion flow defined
- [x] Context-aware conversation defined
- [x] Suggestion engine defined
- [x] Sessions defined
- [x] Study Mode defined
- [x] PDF export defined
- [x] Sandbox defined
- [x] Frontend implementation defined
- [x] API integration defined
- [x] Streaming defined
- [x] Testing flow defined
- [x] Security review flow defined
- [x] Code review flow defined
- [x] QA flow defined
- [x] Production flow defined
- [x] Antigravity execution process defined
- [x] Quality gates defined

---

# 81. Phase 11 Status

**STATUS: COMPLETE**

Bhasha2Code now has a controlled implementation process from the first backend task to local production.

Development must proceed task-by-task using `TASKS.md`, while `RULES.md`, architecture, design, and PRD remain the governing references.

---

# 82. Next Phase

## Phase 12 — Testing

The next phase will define the complete testing strategy:

```text
Unit Testing
↓
NLP Testing
↓
LLM Testing
↓
Context Testing
↓
API Testing
↓
Database Testing
↓
Sandbox Testing
↓
Frontend Testing
↓
Integration Testing
↓
End-to-End Testing
↓
Offline Testing
↓
Performance Testing
↓
Regression Testing
```

The final goal will be to prove what works, identify what fails, and prevent false “production-ready” claims.