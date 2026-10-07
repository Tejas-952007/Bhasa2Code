# Bhasha2Code — Quality Assurance

## Phase 16 — QA

**Project:** Bhasha2Code  
**Phase:** 16 — Quality Assurance  
**Version:** 1.0  
**Status:** COMPLETE  
**QA Type:** Functional + User-Centric + Multilingual + Offline + Release QA  
**Primary Runtime:** Localhost

---

# 1. Purpose

This document defines the formal Quality Assurance process for Bhasha2Code.

The objective is to verify that the complete application is:

```text id="3q7m1v"
Functional
+
Reliable
+
Usable
+
Multilingual
+
Context-Aware
+
Offline-Capable
+
Secure
+
Consistent
```

QA begins after:

```text id="8x2k5m"
Development
↓
Testing
↓
Security Review
↓
Code Review
↓
Preview
```

have reached their required gates.

---

# 2. QA Principle

> **QA validates the product from the user's point of view, not only from the developer's point of view.**

A feature can pass a unit test and still fail QA.

Example:

```text id="c4m8r2"
API works
+
Database works
+
LLM works
```

but:

```text id="p9v1x6"
User cannot understand the response
```

means the feature still has a QA problem.

---

# 3. QA Scope

QA covers:

```text id="s6n3q8"
Core Coding
Multilingual Input
NLP
Context
LLM
Code Generation
Debugging
Explanation
Optimization
Conversion
Suggestions
Sessions
Search
Saved Messages
Notes
Study Mode
PDF Export
Sandbox
Offline Operation
UI / UX
Accessibility
Recovery
Performance
Security Regression
```

---

# 4. QA Entry Criteria

QA may begin only when:

```text id="k3v7m2"
[ ] Local preview is operational
[ ] Core integration tests pass
[ ] No unresolved critical implementation blocker
[ ] Security baseline exists
[ ] Database persistence works
[ ] Ollama/local model is available
[ ] Sandbox is operational
[ ] Critical user journey can be started
```

---

# 5. QA Environment

The QA environment should represent the intended local production setup as closely as practical.

Expected:

```text id="n8q2c5"
Frontend
+
FastAPI
+
SQLite
+
NLP Models
+
Ollama
+
Configured Coding Model
+
Docker Sandbox
```

---

# 6. QA Environment Record

Record actual values:

```text id="y4m8q1"
OS:
Python:
Node:
Backend:
Frontend:
Ollama:
Model:
Docker:
CPU:
RAM:
GPU:
```

Do not manually invent values.

---

# 7. QA User Profiles

Test Bhasha2Code using realistic users.

## QA Persona 1 — Beginner Student

Needs:

```text id="q5r2m8"
Simple explanations
Examples
Basic debugging
Study support
```

---

## QA Persona 2 — Engineering Student

Needs:

```text id="d8v3n1"
Coding
Assignments
Exam preparation
Debugging
Code conversion
Concept explanation
```

---

## QA Persona 3 — Programming Learner

Needs:

```text id="m2c9x7"
Code generation
Optimization
Code review
Practice
```

---

## QA Persona 4 — Mixed-Language User

Uses:

```text id="p6n4q2"
Marathi
Hindi
English
Hinglish
Code-switched input
```

---

## QA Persona 5 — Debugging User

Primarily uses:

```text id="v7m1c8"
Error explanation
Debugging
Validation
Corrected code
```

---

# 8. QA Language Matrix

Required:

```text id="j5q8n3"
English
Hindi
Marathi
Hinglish
Marathi-English
Hindi-English
```

---

# 9. QA Language Rule

The same functional request should be tested in multiple languages.

Example:

```text id="a3m7v1"
English:
Create a Python calculator.

Hindi:
Python में calculator बनाओ.

Marathi:
Python मध्ये calculator तयार कर.

Hinglish:
Python me calculator bana.

Marathi-English:
Python madhe calculator bana.
```

The exact response may vary, but the intended task should remain consistent.

---

# 10. QA Functional Priority

Features are tested in this order:

```text id="x7c2m9"
MUST HAVE
↓
IMPORTANT
↓
V2 / Deferred
```

MUST HAVE failures have the highest release impact.

---

# 11. MUST-HAVE Features

QA must verify:

```text id="r4n8k2"
Multilingual Input
Code Generation
Context-Aware Coding Conversation
Debugging
Code Explanation
Offline LLM
Language Detection
Intent Classification
Tone Classification
Programming Language Detection
Code Validation
Persistent Sessions
Session Reopen / Continue
PDF Export
Study Mode
```

---

# 12. IMPORTANT Features

Also verify:

```text id="w6q1m4"
Code Optimization
Code Conversion
Chat Search
Saved Messages
Personal Notes
Safe Code Sandbox
Docker
Code Review
Performance Suggestions
Security Suggestions
Approach Suggestions
Feature Suggestions
```

---

# 13. QA Scenario Structure

Each QA scenario should contain:

```text id="u8m2v5"
QA ID
Persona
Feature
Precondition
Steps
Input
Expected Result
Actual Result
Status
Severity
Evidence
Notes
```

---

# 14. QA Status

Use:

```text id="q3n7c1"
PASS
FAIL
BLOCKED
NOT APPLICABLE
PASS WITH LIMITATION
```

---

# 15. QA-001 — Application Startup

### Preconditions

Required local services installed.

### Steps

```text id="v5m8q2"
Start Backend
↓
Start Frontend
↓
Open Browser
```

### Expected

```text id="k7c3x9"
Application loads successfully.
```

---

# 16. QA-002 — Health Check

Expected:

```text id="p4n8m1"
Backend health endpoint responds correctly.
```

No uncaught startup exception.

---

# 17. QA-003 — New Chat

Steps:

```text id="w2q6m4"
Open application
↓
Click New Chat
```

Expected:

```text id="r9v3c7"
New session created.
```

---

# 18. QA-004 — Marathi Code Generation

Input:

```text id="x8m1q5"
python madhe calculator bana
```

Expected:

```text id="c4n7v2"
Request understood.
Python code generated.
Relevant explanation available.
```

---

# 19. QA-005 — Hindi Code Generation

Input:

```text id="m6q2v8"
Python में calculator बनाओ.
```

Expected:

```text id="n5c1r4"
Equivalent coding task understood.
```

---

# 20. QA-006 — English Code Generation

Input:

```text id="p3v8k1"
Create a Python calculator.
```

Expected:

```text id="q7m2n5"
Python code generated.
```

---

# 21. QA-007 — Hinglish Code Generation

Input:

```text id="r4x9c2"
Python me calculator bana.
```

Expected:

```text id="j8n3v6"
Mixed-language request understood.
```

---

# 22. QA-008 — Context Follow-Up

First:

```text id="5w2q7m"
Create a Python calculator.
```

Then:

```text id="y1c8n4"
Add division by zero handling.
```

Expected:

```text id="m6v3p9"
Existing calculator is modified.
```

---

# 23. QA-009 — Marathi Follow-Up

First:

```text id="t8n2c5"
Create a Python calculator.
```

Then:

```text id="q4m7v1"
yat error handling add kar
```

Expected:

```text id="d9x3k6"
Correct previous code referenced.
```

---

# 24. QA-010 — Explain Current Code

Input:

```text id="u7m5q2"
हा code Marathi मध्ये explain कर.
```

Expected:

```text id="n8c4r1"
Explanation refers to current code.
```

---

# 25. QA-011 — Debug Current Code

Provide invalid code.

Ask:

```text id="m3v8q5"
हा code debug कर.
```

Expected:

```text id="k2q7n1"
Problem
+
Cause
+
Fix
+
Corrected Code
+
Validation
```

---

# 26. QA-012 — Validate Correct Code

Provide valid supported code.

Expected:

```text id="x5c9m2"
Validated
```

only after actual validation.

---

# 27. QA-013 — Validate Invalid Code

Provide:

```python id="g7m4r1"
print("Hello"
```

Expected:

```text id="q2n8v5"
Validation Failed
```

---

# 28. QA-014 — Optimize Code

Ask:

```text id="c6m1x8"
हा code optimize कसा करता येईल?
```

Expected:

```text id="j5q3n7"
Current code analyzed.
Relevant improvements suggested.
```

---

# 29. QA-015 — Code Review

Ask:

```text id="v8m2q4"
या code चा review कर.
```

Expected:

```text id="r3n7c1"
Correctness
Readability
Potential Issues
Best Practices
```

---

# 30. QA-016 — Security Question

Ask:

```text id="p6x1m9"
हा code production साठी safe आहे का?
```

Expected:

```text id="k4n8v2"
Potential security risks
+
Mitigations
```

No absolute security guarantee should be claimed.

---

# 31. QA-017 — Free-Form Coding Question

Input:

```text id="x3q7m5"
माझ्या code मध्ये memory जास्त का वापरते?
```

Expected:

```text id="u1m8c4"
System provides contextual performance analysis.
```

No predefined mode selection required.

---

# 32. QA-018 — Approach Suggestion

Input:

```text id="n5v2q8"
हा approach योग्य आहे का?
```

Expected:

```text id="c7m4x1"
Context-aware assessment.
```

---

# 33. QA-019 — Feature Suggestion

Input:

```text id="r8m3q6"
माझ्या project ला पुढे काय features add करू?
```

Expected:

```text id="j2v7n5"
Suggestions based on current project/context.
```

---

# 34. QA-020 — Session Persistence

Steps:

```text id="w5c1n8"
Create Session
↓
Send Messages
↓
Close Application
↓
Restart
↓
Open Session
```

Expected:

```text id="q9m4v2"
Messages persist.
```

---

# 35. QA-021 — Continue After Reopen

After reopening:

```text id="p7n2c5"
Add another modification to the code.
```

Expected:

```text id="x3m8q1"
Correct existing context restored.
```

---

# 36. QA-022 — Session Rename

Expected:

```text id="v4q7n2"
New session title appears consistently.
```

---

# 37. QA-023 — Session Delete

Expected:

```text id="m1c8x5"
Only selected session is deleted.
```

No unrelated session should disappear.

---

# 38. QA-024 — Search

Search for:

```text id="j6n3q8"
calculator
```

Expected:

```text id="r2v7m4"
Relevant sessions/messages found.
```

---

# 39. QA-025 — Saved Message

Save an assistant response.

Expected:

```text id="q8m1c6"
Response appears in Saved.
```

---

# 40. QA-026 — Saved Persistence

Restart application.

Expected:

```text id="n3v9x5"
Saved response still available.
```

---

# 41. QA-027 — Personal Notes

Create:

```text id="y7m2q4"
Python Functions — important for revision.
```

Expected:

```text id="c1n8v6"
Note saved and editable.
```

---

# 42. QA-028 — Study Mode

Topic:

```text id="m5q3x8"
Python Functions
```

Expected:

```text id="p9v1n4"
Explanation
Examples
Important Points
Common Mistakes
Practice Questions
Mini Quiz
```

---

# 43. QA-029 — Study Context

After generating study content:

```text id="r7m2c5"
Create a quiz from this topic.
```

Expected:

```text id="x4n8q1"
Quiz uses current study context.
```

---

# 44. QA-030 — PDF Export

Expected:

```text id="j1v6m9"
PDF generated locally.
```

---

# 45. QA-031 — PDF Content

Verify:

```text id="q3c8n5"
Session Title
Messages
Code
Explanation
Validation
Study Content where selected
```

---

# 46. QA-032 — Code Execution

Run supported code.

Expected:

```text id="m7n2v4"
Execution happens inside sandbox.
```

---

# 47. QA-033 — Sandbox Timeout

Use:

```python id="x9q1c6"
while True:
    pass
```

Expected:

```text id="c5m8r2"
Execution terminates safely.
```

---

# 48. QA-034 — Sandbox Network Restriction

Attempt outbound network access.

Expected:

```text id="v3n7q1"
Network unavailable/blocked.
```

---

# 49. QA-035 — Sandbox Filesystem Restriction

Attempt sensitive file access.

Expected:

```text id="m2q8c4"
Access restricted according to sandbox policy.
```

---

# 50. QA-036 — Docker Failure

Stop Docker and request execution.

Expected:

```text id="r6v1n9"
Execution unavailable.
No host fallback.
```

---

# 51. QA-037 — Ollama Failure

Stop Ollama.

Expected:

```text id="q4m8c2"
Model status becomes unavailable.
User receives understandable recovery guidance.
```

---

# 52. QA-038 — Recovery After Ollama Restart

Restart Ollama.

Retry request.

Expected:

```text id="n7x3v5"
Local generation works again.
```

---

# 53. QA-039 — Database Restart Recovery

Restart application after persistent data is stored.

Expected:

```text id="m2c7q8"
Data remains available.
```

---

# 54. QA-040 — Invalid Input

Test:

```text id="x8n4v1"
Empty Message
Malformed API Request
Unknown Session ID
Unsupported Language
Invalid Code
```

Expected:

```text id="c5q9m2"
Safe validation errors.
```

---

# 55. QA-041 — Multilingual Consistency

Execute the same task in:

```text id="v7m3q6"
English
Hindi
Marathi
Hinglish
Marathi-English
Hindi-English
```

Compare:

```text id="n2c8x4"
Task Understanding
Language Detection
Intent
Tone
Generated Code
Validation
Explanation
```

---

# 56. QA-042 — Programming Language Matrix

Test:

```text id="j5m1q8"
Python
C
C++
Java
JavaScript
SQL
```

Where applicable verify:

```text id="p8v3n2"
Detection
Generation
Parsing
Validation
```

---

# 57. QA-043 — Tone Matrix

Test:

```text id="r4x7m1"
Simple
Formal
Technical
Detailed
Short
Casual
```

Expected:

```text id="c9q2n6"
Response style adapts appropriately.
```

---

# 58. QA-044 — Intent Matrix

Test every supported intent.

Expected:

```text id="m6v1q8"
Correct or reasonable routing.
Low-confidence cases handled safely.
```

---

# 59. QA-045 — Context Chain

Full conversation:

```text id="y3n8c2"
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
Review
↓
Security Check
```

Expected:

```text id="q7m4x1"
All operations reference current code/context.
```

---

# 60. QA-046 — Cross-Session Isolation

Session A:

```text id="c2v9m5"
Python Calculator
```

Session B:

```text id="n7q1x4"
C++ Student Management
```

Ask follow-up in Session B.

Expected:

```text id="m8c3v6"
Session A context is not used.
```

---

# 61. QA-047 — Long Conversation

Create a lengthy session.

Check:

```text id="r5n2q8"
Context relevance
UI responsiveness
Database performance
Memory behavior
```

---

# 62. QA-048 — Large Code

Use a larger source file.

Check:

```text id="x1m7c4"
Editor
Scrolling
Copy
Parsing
Validation
LLM context handling
```

---

# 63. QA-049 — Long Response

Generate a detailed explanation.

Check:

```text id="v6q3n8"
Rendering
Scrolling
Layout
Response readability
No UI freeze
```

---

# 64. QA-050 — Repeated Requests

Perform several requests in the same session.

Expected:

```text id="m4c8q2"
No duplicated messages.
No corrupted context.
No unexplained crashes.
```

---

# 65. QA-051 — Application Restart

Perform:

```text id="j9n3v6"
Chat
Save
Note
Study
Close
Restart
```

Verify persistence.

---

# 66. QA-052 — Full Offline Test

Procedure:

```text id="p5m8x1"
Prepare local environment
↓
Disable Internet
↓
Start application
↓
Create Chat
↓
Generate Code
↓
Debug
↓
Explain
↓
Validate
↓
Save
↓
Reopen
↓
Study Mode
↓
PDF Export
```

Expected:

```text id="c7q2n4"
Core local workflow works without Internet.
```

---

# 67. QA-053 — Offline Sandbox

With Internet disabled:

```text id="m1v7q5"
Run supported local code.
```

Expected:

```text id="x8c3n9"
Sandbox still works for local execution.
```

---

# 68. QA-054 — Offline Search

Search sessions while offline.

Expected:

```text id="r6m2q1"
Local stored content remains searchable.
```

---

# 69. QA-055 — Offline PDF

Export a session while offline.

Expected:

```text id="n4c8v7"
PDF generated locally.
```

---

# 70. QA-056 — UI Loading State

During LLM generation:

```text id="q2m5x9"
Loading / streaming state visible.
```

Expected:

```text id="c7n1v4"
User understands that generation is in progress.
```

---

# 71. QA-057 — UI Error State

Simulate backend/model failure.

Expected:

```text id="m8q3r6"
Readable error
+
Reason where appropriate
+
Recovery action
```

---

# 72. QA-058 — Empty State

Open a new application with no sessions.

Expected:

```text id="x4n7m2"
Clean empty-state screen.
```

It should not look like a broken application.

---

# 73. QA-059 — Search Empty State

Search for unavailable content.

Expected:

```text id="v9c2q5"
Clear "No results" state.
```

---

# 74. QA-060 — Accessibility

Verify:

```text id="j3m8n1"
Keyboard Navigation
Focus
Labels
Contrast
Status Indicators
```

---

# 75. QA-061 — Keyboard Shortcuts

Verify:

```text id="m6q2v8"
Enter → Send
Shift+Enter → New Line
Ctrl/Cmd+K → Search
Esc → Close appropriate UI
```

---

# 76. QA-062 — Visual Design

Verify against `DESIGN.md`.

Required:

```text id="x5n1c7"
Minimalist
White-first
Professional
Clean
Coding-focused
Study-friendly
```

---

# 77. QA-063 — UI Clutter Check

Reject unnecessary:

```text id="q8m4v2"
Cards
Colors
Gradients
Animations
Panels
Dashboard Widgets
```

unless justified.

---

# 78. QA-064 — Responsive Check

Test laptop/desktop widths.

Expected:

```text id="n2c7x5"
Sidebar usable
Main content readable
Composer accessible
Code editor usable
No critical overflow
```

---

# 79. QA-065 — Error Recovery

Test:

```text id="m7q1c8"
Ollama Failure
Docker Failure
Database Error
Validation Failure
PDF Failure
```

Expected:

```text id="v4n9x2"
Application remains recoverable.
```

---

# 80. QA-066 — No Host Execution

Review and test execution path.

Expected:

```text id="c3m8q1"
No generated code executes directly on the host.
```

This is a release-blocking QA condition.

---

# 81. QA-067 — No Data Leakage

Verify that one session cannot access another session's context.

Expected:

```text id="r7q2n5"
No cross-session leakage.
```

---

# 82. QA-068 — No Secret Leakage

Review user-visible:

```text id="x8m3c6"
Errors
Logs exposed through UI
API responses
Frontend bundle
```

Expected:

```text id="n1q7v4"
No real secrets exposed.
```

---

# 83. QA-069 — Suggestion Quality

After multiple requests:

```text id="m5c2x8"
Check relevance of suggestions.
```

Expected:

```text id="q9n4v1"
No generic repeated suggestion spam.
```

---

# 84. QA-070 — Study Quality

Review generated study content for:

```text id="r3m7q2"
Topic Relevance
Clarity
Examples
Correctness
Practice Questions
Quiz Relevance
```

---

# 85. QA-071 — PDF Quality

Inspect actual PDF pages.

Check:

```text id="x6c1n8"
Page Breaks
Code Formatting
Multilingual Text
Headings
Readability
Long Sessions
```

---

# 86. QA-072 — Session Naming

Check auto-generated session titles.

Expected:

```text id="m4q8v2"
Title is understandable.
```

---

# 87. QA-073 — Saved Message Integrity

Save different message types:

```text id="c7n2x5"
Code
Explanation
Debugging Response
Study Content
```

Verify correct content is retained.

---

# 88. QA-074 — Notes Integrity

Test:

```text id="v1m6q9"
Create
Edit
Delete
Search
Restart
```

No unrelated note should change.

---

# 89. QA-075 — Database Integrity

After normal and failure scenarios verify:

```text id="q3n8c4"
Sessions
Messages
Saved Messages
Notes
Generated Code
Debug History
```

remain structurally consistent.

---

# 90. QA-076 — Performance Baseline

Record actual:

```text id="x7m2q5"
Startup Time
Model Load Time
First Token Latency
Total Response Time
Validation Time
PDF Export Time
RAM
CPU
GPU
```

Do not invent target values.

---

# 91. QA-077 — Resource Stability

Repeat representative operations.

Check:

```text id="m8c4n1"
RAM Growth
CPU Behavior
VRAM Behavior
Disk Growth
Docker Process Cleanup
```

---

# 92. QA-078 — Sandbox Cleanup

After execution verify:

```text id="q2v7m5"
Container exits
Temporary files handled
No abandoned processes
```

---

# 93. QA-079 — Dependency Failure

Temporarily make a required dependency unavailable.

Expected:

```text id="n6m1c8"
Clear failure
+
No silent fallback that violates security
```

---

# 94. QA-080 — Regression Smoke Test

After fixing QA bugs:

```text id="x5c8q2"
Application Starts
↓
New Chat
↓
Generate
↓
Follow-Up
↓
Validate
↓
Save
```

must still pass.

---

# 95. QA Test Matrix

| Area | Core QA | Release Impact |
|---|---|---|
| Startup | Required | High |
| Multilingual | Required | High |
| NLP | Required | High |
| Code Generation | Required | Critical |
| Context | Required | Critical |
| Debugging | Required | Critical |
| Explanation | Required | High |
| Validation | Required | Critical |
| Sessions | Required | Critical |
| Reopen | Required | Critical |
| Study Mode | Required | High |
| PDF | Required | High |
| Sandbox | Required | Critical |
| Offline | Required | Critical |
| Search | Required | Medium |
| Saved | Required | Medium |
| Notes | Required | Medium |
| UI/UX | Required | High |
| Accessibility | Required | Medium |
| Performance | Required | High |
| Security Regression | Required | Critical |

---

# 96. Bug Triage

Every QA failure must be classified.

```text id="p7m3x9"
BLOCKER
HIGH
MEDIUM
LOW
```

---

# 97. QA Blocker

Examples:

```text id="c2n8q5"
Host Code Execution
Sandbox Bypass
Cross-Session Leakage
Data Loss
Offline Core Failure
Application Cannot Start
MUST-HAVE Feature Unusable
```

QA cannot pass with an unresolved blocker.

---

# 98. High QA Issue

Examples:

```text id="m4q1v8"
Frequent context loss
Debugging unusable
Persistent history unreliable
Major multilingual failure
PDF consistently broken
Serious UI usability issue
```

Normally blocks release.

---

# 99. Medium QA Issue

Examples:

```text id="x9c3n7"
Specific edge-case failure
Minor search issue
Occasional UI inconsistency
Non-critical response formatting issue
```

May be deferred with justification.

---

# 100. Low QA Issue

Examples:

```text id="q6m2v5"
Small spacing issue
Minor wording problem
Cosmetic inconsistency
```

May be deferred.

---

# 101. QA Bug Lifecycle

```text id="r8n4c2"
FOUND
↓
CLASSIFIED
↓
ASSIGNED
↓
FIXED
↓
RETESTED
↓
REGRESSION TEST
↓
CLOSED
```

---

# 102. Retest Rule

A fixed bug is not CLOSED until:

```text id="m3q7x1"
Original Test Passes
+
Relevant Regression Test Passes
```

---

# 103. QA Evidence

Preserve where useful:

```text id="v5c1n8"
Screenshots
Screen Recordings
Logs
Test Output
PDF Samples
Validation Output
Performance Measurements
Sandbox Results
```

Evidence must represent actual system behavior.

---

# 104. Real-User QA

At least one full manual walkthrough should be performed without looking at internal implementation details.

The tester should behave like a normal user.

Example:

```text id="q2m8v4"
"What can I do here?"
↓
New Chat
↓
Ask Marathi Coding Question
↓
Follow-Up
↓
Debug
↓
Study
↓
Save
↓
Reopen
↓
PDF
```

---

# 105. User Experience Questions

During manual QA ask:

```text id="n7c3m1"
Can the user understand what to do?
Can the user understand the response?
Can the user find previous work?
Can the user continue old work?
Can the user identify validation status?
Can the user recover from failures?
```

---

# 106. Response Quality Review

Review whether answers are:

```text id="x4q8m2"
Relevant
Understandable
Contextual
Technically Reasonable
Language-Appropriate
Tone-Appropriate
```

---

# 107. Hallucination QA

Test requests where the system may not know enough.

Expected:

```text id="m1c6v9"
System should communicate uncertainty.
```

It should not invent:

```text id="q7n3x5"
Libraries
APIs
Compiler Results
Performance Results
Security Guarantees
```

---

# 108. LLM Variability QA

Repeat important LLM scenarios.

Judge stable properties such as:

```text id="r2m8c4"
Correct Task
Correct Language
Correct Code Structure
Validation
Context Usage
```

Do not require identical wording across every run.

---

# 109. Offline QA Rule

Offline is a release feature, not a demonstration trick.

The core user journey must be tested without Internet connectivity.

---

# 110. Production-Like QA

The final QA cycle should use:

```text id="c5q1m7"
Production-like Configuration
Real Local Model
Real SQLite
Real Sandbox
Real Frontend
Real Backend
```

Mocks must not replace critical core components during final QA.

---

# 111. QA Exit Criteria

QA can pass only when:

```text id="v8m3n2"
[ ] All MUST-HAVE features verified
[ ] Critical user journey passes
[ ] No unresolved blocker
[ ] No unresolved release-blocking security issue
[ ] Session persistence verified
[ ] Session reopen verified
[ ] Multilingual flows verified
[ ] Offline core flow verified
[ ] Sandbox controls verified
[ ] PDF export verified
[ ] Study Mode verified
[ ] Major UI/UX issues resolved
[ ] Regression smoke test passes
[ ] Known limitations documented
```

---

# 112. Release Readiness Categories

Use:

```text id="q4n7x1"
READY
READY WITH LIMITATIONS
NOT READY
```

---

# 113. READY

Use when:

```text id="m8c2v5"
MUST-HAVES Pass
No Release Blockers
Critical Journey Passes
Security Gate Passes
Offline Gate Passes
```

---

# 114. READY WITH LIMITATIONS

Use when:

```text id="x1q6m8"
Core product works
+
Known non-critical limitations remain
```

Every limitation must be documented.

---

# 115. NOT READY

Use when:

```text id="c7m3n9"
Critical failure
+
Release-blocking issue
```

---

# 116. QA Summary Report

At the end of QA record:

```text id="v5n8q2"
Total Test Cases
Passed
Failed
Blocked
Not Applicable
Passed With Limitation
Critical Bugs
High Bugs
Medium Bugs
Low Bugs
Security Issues
Offline Status
Performance Summary
Known Limitations
Final Recommendation
```

---

# 117. QA Report Example

```text id="j2m7x4"
QA Cycle:
QA-01

Environment:
<Actual Environment>

Total Tests:
<Actual>

Passed:
<Actual>

Failed:
<Actual>

Blocked:
<Actual>

Critical Bugs:
<Actual>

High Bugs:
<Actual>

Offline:
PASS / FAIL

Sandbox:
PASS / FAIL

Critical User Journey:
PASS / FAIL

Recommendation:
READY /
READY WITH LIMITATIONS /
NOT READY
```

Actual values must come from executed QA.

---

# 118. QA vs Testing

Testing asks:

```text id="r6m1c8"
Does the implementation behave correctly?
```

QA asks:

```text id="q3n7v2"
Is the complete product reliable and usable enough for release?
```

Both are required.

---

# 119. QA vs Code Review

Code Review:

```text id="m8c4x1"
Implementation Quality
```

QA:

```text id="v2n7q5"
Product Quality
```

Neither replaces the other.

---

# 120. QA vs Security Review

Security Review:

```text id="c5m1x8"
Security Risks
```

QA:

```text id="q7n3v4"
Does the product behave safely in realistic use?
```

Security regression checks remain part of QA.

---

# 121. QA Automation

Automate repeatable checks where practical:

```text id="n4m8c2"
API Regression
Unit Tests
Integration Tests
Sandbox Tests
Database Tests
Offline Checks
```

Manual QA remains necessary for:

```text id="v6q2m7"
UI
UX
Multilingual conversation quality
Study experience
Visual consistency
Real-world workflows
```

---

# 122. Antigravity QA Prompt

```text id="x3m7q1"
Execute QA for Bhasha2Code using docs/16_qa/QA.md.

Before making changes:
1. Inspect the current preview environment.
2. Inspect testing results.
3. Inspect security review results.
4. Inspect code review findings.
5. Inspect known issues.

Test from a real-user perspective.

Required language coverage:
- English
- Hindi
- Marathi
- Hinglish
- Marathi-English
- Hindi-English

Required MUST-HAVE flow:
New Chat
→ Generate
→ Context Follow-Up
→ Debug
→ Validate
→ Explain
→ Save
→ Close
→ Reopen
→ Continue
→ Study
→ PDF

Also test:
- Search
- Notes
- Suggestions
- Optimization
- Conversion
- Sandbox
- Offline operation
- Failure recovery

Do not claim PASS unless the test was actually executed.

For failures:
1. Record QA ID.
2. Record severity.
3. Record steps.
4. Record expected result.
5. Record actual result.
6. Preserve evidence.
7. Do not hide the failure.

At completion report:
- Total tests
- Passed
- Failed
- Blocked
- Critical issues
- High issues
- Offline result
- Sandbox result
- Critical journey result
- Final recommendation
```

---

# 123. Final QA Checklist

```text id="p8m2c6"
[ ] Application startup verified
[ ] Backend verified
[ ] Frontend verified
[ ] Database verified
[ ] NLP verified
[ ] Multilingual inputs verified
[ ] Intent verified
[ ] Tone verified
[ ] Programming language detection verified
[ ] Code generation verified
[ ] Context verified
[ ] Debugging verified
[ ] Explanation verified
[ ] Optimization verified
[ ] Conversion verified
[ ] Suggestions verified
[ ] Sessions verified
[ ] Reopen verified
[ ] Search verified
[ ] Saved messages verified
[ ] Notes verified
[ ] Study Mode verified
[ ] PDF verified
[ ] Sandbox verified
[ ] Offline verified
[ ] Error recovery verified
[ ] Accessibility checked
[ ] UI/UX checked
[ ] Performance baseline recorded
[ ] Security regression checked
[ ] Regression smoke test passed
[ ] Known limitations documented
```

---

# 124. Phase 16 Acceptance Criteria

- [x] QA purpose defined
- [x] QA scope defined
- [x] QA entry criteria defined
- [x] QA exit criteria defined
- [x] Real-user personas defined
- [x] Language coverage defined
- [x] MUST-HAVE QA defined
- [x] IMPORTANT feature QA defined
- [x] Functional scenarios defined
- [x] Context scenarios defined
- [x] Session scenarios defined
- [x] Study Mode scenarios defined
- [x] PDF scenarios defined
- [x] Sandbox scenarios defined
- [x] Offline QA defined
- [x] UI/UX QA defined
- [x] Accessibility QA defined
- [x] Performance QA defined
- [x] Failure recovery QA defined
- [x] Regression QA defined
- [x] Bug severity defined
- [x] QA evidence defined
- [x] QA reporting defined
- [x] Release readiness categories defined
- [x] Antigravity QA workflow defined

---

# 125. Phase 16 Status

**STATUS: COMPLETE**

Bhasha2Code now has a formal QA gate that evaluates the system as a complete product rather than as independent modules.

The release path is now:

```text id="c4m8q1"
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

QA must establish evidence for the final release recommendation.

---

# 126. Next Phase

## Phase 17 — Production

The next phase will define the actual **local production deployment**:

```text id="v7n2m5"
Production Configuration
↓
Build
↓
Database Setup
↓
Ollama
↓
Docker Sandbox
↓
Frontend
↓
Backend
↓
Startup
↓
Health Checks
↓
Backup
↓
Recovery
↓
Rollback
↓
Final Release
```

The first production target remains **localhost / local machine**, with public deployment treated as a later separate deployment path.