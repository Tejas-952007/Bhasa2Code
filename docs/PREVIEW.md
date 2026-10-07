# Bhasha2Code — Preview Development

## Phase 15 — Preview Development

**Project:** Bhasha2Code  
**Phase:** 15 — Preview Development  
**Version:** 1.0  
**Status:** COMPLETE  
**Preview Type:** Local Production-Like Preview  
**Primary Runtime:** Localhost  
**Primary Development Tool:** Antigravity

---

# 1. Purpose

This document defines how Bhasha2Code will be assembled and tested as a complete product before formal QA and production deployment.

The objective is to verify:

```text id="q8f3m1"
Frontend
+
Backend
+
NLP
+
Context
+
Local LLM
+
Code Engine
+
Database
+
Sandbox
+
Study Mode
+
PDF Export
```

work together as one system.

---

# 2. Preview Philosophy

The preview environment should be as close as practical to the intended local production environment.

The preview is not merely:

```text
"Does the frontend open?"
```

It is:

```text id="x4p7j2"
Can a real user complete the full Bhasha2Code workflow?
```

---

# 3. Preview Architecture

```text id="y3d8n1"
                   BROWSER
                      │
                      ▼
              ┌──────────────┐
              │ React + Vite │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │   FastAPI    │
              └──────┬───────┘
                     │
          ┌──────────┼───────────┐
          ▼          ▼           ▼
         NLP      Context      SQLite
          │          │
          └─────┬────┘
                ▼
         Prompt Builder
                │
                ▼
             Ollama
                │
                ▼
       Local Coding Model
                │
                ▼
         Output Parser
                │
        ┌───────┴────────┐
        ▼                ▼
    Validator          Sandbox
        │                │
        └───────┬────────┘
                ▼
             Result
                │
                ▼
             Browser
```

---

# 4. Preview Environment

The target preview should contain:

```text id="u8x9c2"
Frontend
Backend
SQLite
NLP Models
Ollama
Configured Coding Model
Docker
Sandbox
Local File Storage
PDF Export
```

---

# 5. Preview Configuration

Preview configuration must be separate from development configuration where practical.

Example:

```text id="m3x5n7"
APP_ENV=preview

BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=qwen2.5-coder:3b-instruct

DATABASE_URL=sqlite:///./data/preview.db
```

The preview database must not accidentally become the main development database.

---

# 6. Preview Startup Order

Use:

```text id="h6s4w2"
1. Database
2. Ollama
3. Docker
4. Backend
5. Frontend
```

Conceptually:

```text id="3q7y1a"
Dependencies
↓
Backend
↓
Frontend
```

---

# 7. Startup Checklist

Before opening the UI:

```text id="s5a2e9"
[ ] Python environment active
[ ] SQLite available
[ ] Ollama running
[ ] Correct model installed
[ ] Docker running
[ ] Backend running
[ ] Frontend running
```

---

# 8. Backend Preview Check

Verify:

```text id="j4n6w9"
GET /health
```

Expected:

```json id="4v8k2r"
{
  "status": "healthy"
}
```

Where implemented, also verify service health:

```text id="7f6p1m"
Database
Ollama
Sandbox
```

---

# 9. Frontend Preview Check

Verify:

```text id="m8x1q4"
Application loads
Sidebar visible
Main workspace visible
Composer visible
No blocking console error
```

---

# 10. Visual Preview Standard

The preview must match the approved design identity:

```text id="a9z4c1"
Minimalist
White-first
Professional
Clean
Study-friendly
Coding-focused
```

---

# 11. Preview UI Structure

Expected main structure:

```text id="p2k8d5"
┌──────────────┬──────────────────────────────────┐
│              │                                  │
│   Sidebar    │       Main Workspace             │
│              │                                  │
│ + New Chat   │  Conversation                    │
│ Recent       │                                  │
│ Saved        │  Code                            │
│ Notes        │  Explanation                     │
│ Study Mode   │  Validation                      │
│ Search       │  Suggestions                     │
│ Settings     │                                  │
│              │  Composer                        │
└──────────────┴──────────────────────────────────┘
```

No permanent right-side context panel is required.

---

# 12. Preview Header

The header should remain minimal.

Example:

```text id="c2m7d4"
Bhasha2Code
● Local Model
```

The model status should be visible without becoming visually dominant.

---

# 13. Model Status Preview

Possible states:

```text id="8f2a1c"
Ready
Loading
Busy
Unavailable
Error
```

Test every relevant state.

---

# 14. Preview Scenario P01 — New Chat

Action:

```text id="u8b4m1"
Click + New Chat
```

Expected:

```text id="w4n6r2"
New empty session created.
Composer focused or available.
```

---

# 15. Preview Scenario P02 — Marathi Input

Input:

```text id="x7q3c5"
python madhe calculator bana
```

Expected system flow:

```text id="5r2k8m"
Language Detection
↓
Marathi-English
↓
Intent
GENERATE_CODE
↓
Programming Language
Python
↓
Prompt Builder
↓
Ollama
↓
Code Response
```

Actual detection output must be recorded rather than assumed.

---

# 16. Preview Scenario P03 — Code Generation

Expected response:

```text id="n8f3s5"
Python Code
+
Relevant Explanation
+
Optional Relevant Suggestions
```

The response must not contain unnecessary UI clutter.

---

# 17. Preview Scenario P04 — Code Display

Verify:

```text id="r5j2b6"
Syntax Highlighting
Line Numbers where appropriate
Copy
Edit
Validate
Run where supported
```

---

# 18. Preview Scenario P05 — Context Follow-Up

User:

```text id="d8v1s3"
yat division by zero error handling add kar
```

Expected:

```text id="z6m9q2"
System recognizes the reference to the current calculator.
```

It must not ask the user to paste the code again unless the required context is genuinely unavailable.

---

# 19. Context Verification

Verify that:

```text id="s3c8m2"
Current Session
+
Previous Code
+
Follow-Up Request
```

remain associated.

---

# 20. Preview Scenario P06 — Validation

Click:

```text id="y7d4n9"
Validate
```

Expected state:

```text id="m5q8r1"
✓ Validated
```

or the appropriate actual result.

The system must not show `Validated` before validation is actually performed.

---

# 21. Preview Scenario P07 — Debugging

Introduce or provide invalid code.

Ask:

```text id="p4w6j2"
हा code debug कर
```

Expected:

```text id="u7c3m8"
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

# 22. Preview Scenario P08 — Explain in Marathi

Ask:

```text id="e3r7x1"
हा code Marathi मध्ये explain कर
```

Expected:

```text id="k4b9n6"
Explanation primarily follows Marathi / appropriate Marathi-English usage.
```

The code should remain unchanged unless modification is requested.

---

# 23. Preview Scenario P09 — Optimization

Ask:

```text id="n6p2y7"
हा code आणखी optimize कसा करता येईल?
```

Expected:

```text id="b8m5v3"
Potential bottleneck
+
Reason
+
Improvement
```

The system must not fabricate measured performance gains.

---

# 24. Preview Scenario P10 — Free-Form Coding Question

Ask:

```text id="t1c7s4"
माझ्या code मध्ये memory जास्त का वापरते?
```

Expected:

```text id="q9f2d8"
System answers as a contextual coding question.
```

No predefined button should be required.

---

# 25. Preview Scenario P11 — Code Review

Ask:

```text id="y4v9m2"
या code चा review कर.
```

Expected:

```text id="z2r6c8"
Correctness
+
Readability
+
Potential Issues
+
Best Practices
```

Relevant suggestions may follow.

---

# 26. Preview Scenario P12 — Performance Analysis

Ask:

```text id="a6k3p1"
हा code slow का आहे?
```

Expected:

```text id="v5n8q4"
Performance-oriented analysis of current code.
```

---

# 27. Preview Scenario P13 — Security Analysis

Ask:

```text id="c8h2m5"
हा code production साठी safe आहे का?
```

Expected:

```text id="j7r3x9"
Security Risks
+
Mitigations
```

The answer must not claim absolute security.

---

# 28. Preview Scenario P14 — Suggestions

After a relevant code response:

```text id="6s1qf4"
Suggestions
```

should appear only when useful.

Example:

```text id="m9v3k7"
Add input validation
Handle division by zero
Add test cases
```

---

# 29. Suggestion Spam Test

Send several ordinary requests.

Expected:

```text id="q4d8p2"
Suggestions remain relevant.
No repeated generic feature spam.
```

---

# 30. Preview Scenario P15 — Save Message

Action:

```text id="e8m1s6"
Save
```

Expected:

```text id="w3c7n5"
Message appears in Saved.
```

---

# 31. Preview Scenario P16 — Personal Note

Create a note:

```text id="r6p2y8"
Python Functions — important for exam revision.
```

Expected:

```text id="f1q9m4"
Note persists.
```

---

# 32. Preview Scenario P17 — Study Mode

Select:

```text id="j5k8x2"
Study Mode
```

Topic:

```text id="v2n6c9"
Python Functions
```

Expected structure:

```text id="u4m7p3"
Explanation
Examples
Important Points
Common Mistakes
Practice Questions
Mini Quiz
```

---

# 33. Preview Scenario P18 — Study Context

After studying:

```text id="a2r8m1"
Create a quiz on this topic.
```

Expected:

```text id="s7c4n5"
Quiz should reference the current study topic.
```

---

# 34. Preview Scenario P19 — Session Rename

Rename:

```text id="k9y3b6"
Python Calculator Practice
```

Expected:

```text id="e4m8q2"
New session title appears consistently.
```

---

# 35. Preview Scenario P20 — Close and Reopen

Flow:

```text id="h3v7c1"
Close Session
↓
Open Recent
↓
Select Session
```

Expected:

```text id="n8q2m5"
Previous messages available.
Current context available.
```

---

# 36. Preview Scenario P21 — Continue After Reopen

Ask:

```text id="f6r1y9"
आता यामध्ये test cases add कर.
```

Expected:

```text id="j2m7v4"
System continues with the reopened code/session context.
```

---

# 37. Preview Scenario P22 — Search

Search:

```text id="c5k8p2"
calculator
```

Expected:

```text id="m1v6q7"
Relevant session/message results.
```

---

# 38. Preview Scenario P23 — PDF Export

Export the current session.

Expected:

```text id="b9r3x5"
PDF created locally.
```

PDF should preserve:

```text id="u6p2n8"
Session Title
Conversation
Code
Explanation
Validation
Study Content where selected
```

---

# 39. Preview Scenario P24 — Local Sandbox

Use supported code and choose:

```text id="e2v7m4"
Run
```

Expected:

```text id="x8q1c6"
Execution happens inside sandbox.
```

Never execute directly on host.

---

# 40. Preview Scenario P25 — Sandbox Timeout

Test:

```python id="l4m9p2"
while True:
    pass
```

Expected:

```text id="q7c2v8"
Execution terminated by timeout.
```

The application remains usable.

---

# 41. Preview Scenario P26 — Sandbox Network

Test code attempting an external network request.

Expected:

```text id="k3n6x1"
Network access blocked/unavailable.
```

---

# 42. Preview Scenario P27 — Sandbox Filesystem

Test access to sensitive host paths.

Expected:

```text id="v8m2q5"
Restricted.
```

---

# 43. Preview Scenario P28 — Model Failure

Stop Ollama.

Open the application.

Expected:

```text id="z4c7r2"
Application remains available.
Model status:
Unavailable
```

A coding request should produce a clear recovery message rather than crash the application.

---

# 44. Preview Scenario P29 — Docker Failure

Stop Docker.

Attempt code execution.

Expected:

```text id="j6n1p8"
Execution unavailable.
Host execution is NOT used as fallback.
```

---

# 45. Preview Scenario P30 — Database Failure

Simulate database failure safely.

Expected:

```text id="m3q8v5"
Clear error.
No silent data corruption.
```

---

# 46. Preview Scenario P31 — Invalid Input

Test:

```text id="p7x2c4"
Empty message
Very long message
Malformed request
Unknown session
Invalid code
```

Expected:

```text id="n9k4m1"
Safe validation response.
```

---

# 47. Preview Scenario P32 — Multilingual Matrix

Run the same coding task in:

```text id="b3m7x8"
English
Hindi
Marathi
Hinglish
Marathi-English
Hindi-English
```

Record:

```text id="q5r1n6"
Detected Language
Detected Intent
Detected Tone
Generated Code
Validation Result
Response Language
Latency
```

Do not fill results manually.

Use actual observed values.

---

# 48. Preview Scenario P33 — Programming Language Matrix

Run representative tasks for:

```text id="d8v2k6"
Python
C
C++
Java
JavaScript
SQL
```

Verify:

```text id="u1m5q9"
Detection
Generation
Parsing
Validation
```

where supported.

---

# 49. Preview Scenario P34 — Full Context Chain

Run:

```text id="g4n8c1"
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

All operations should operate on the current task/code context.

---

# 50. Preview Scenario P35 — Session Isolation

Create:

```text id="x2m7v5"
Session A:
Python Calculator

Session B:
C++ Student Management
```

Then ask context-dependent questions in both.

Expected:

```text id="r9c4n8"
No cross-session context leakage.
```

---

# 51. Preview Scenario P36 — Restart Recovery

Flow:

```text id="p6y1m3"
Create Session
↓
Generate Code
↓
Save
↓
Close Application
↓
Restart
↓
Reopen Session
↓
Continue
```

Expected:

```text id="v2q8k5"
Persistent data remains available.
```

---

# 52. Preview Scenario P37 — Offline Mode

Procedure:

```text id="h8m3c7"
Prepare environment
↓
Disable network
↓
Start application
↓
New Chat
↓
Generate
↓
Debug
↓
Explain
↓
Save
↓
Reopen
↓
Study
↓
PDF
```

Expected:

```text id="k1r6v9"
Core local workflow continues.
```

---

# 53. Preview Scenario P38 — Long Conversation

Create a long session.

Verify:

```text id="a4n8q2"
UI remains usable
Context remains relevant
Response generation remains stable
Database remains responsive
Memory does not grow uncontrollably
```

---

# 54. Preview Scenario P39 — Long Code

Use a larger code sample.

Verify:

```text id="s6m2x9"
Editor performance
Parser behavior
Validation behavior
Scrolling
Copy
Editing
```

---

# 55. Preview Scenario P40 — Concurrent Local Requests

Where supported, test multiple local requests.

Verify:

```text id="c9q3v6"
Session isolation
No corrupted responses
No database race causing data loss
Controlled resource consumption
```

---

# 56. Preview Scenario P41 — Loading State

During a model response:

```text id="j3m8p1"
Loading / streaming indicator
```

Expected:

```text id="q7r2c5"
User clearly knows the system is working.
```

---

# 57. Preview Scenario P42 — Error State

For an LLM failure:

```text id="x5n9v4"
Human-readable error
+
Possible recovery action
```

Avoid raw stack traces.

---

# 58. Preview Scenario P43 — Accessibility

Verify:

```text id="m6q1y8"
Keyboard Navigation
Focus
Labels
Contrast
Status Indicators
```

Color alone must not communicate critical states.

---

# 59. Preview Scenario P44 — Minimalist UI Check

Review the complete application visually.

Confirm:

```text id="d2v7k9"
No unnecessary cards
No excessive gradients
No neon elements
No large AI illustrations
No unnecessary dashboards
No excessive animation
```

---

# 60. Preview Scenario P45 — Desktop / Laptop Check

Test typical laptop widths.

Expected:

```text id="u8m3q5"
Sidebar usable
Main workspace readable
Code editor usable
Composer visible
No critical overflow
```

---

# 61. Preview Scenario P46 — Recovery Workflow

Test:

```text id="n2c7v4"
Ollama fails
↓
User sees error
↓
Ollama restarted
↓
Retry
↓
Chat works
```

---

# 62. Preview Scenario P47 — Validation Failure Recovery

Flow:

```text id="m9p1x6"
Generate
↓
Validation Failed
↓
Debug
↓
Fix
↓
Validate
```

Expected:

```text id="q4v8n2"
Recovery is visible and understandable.
```

---

# 63. Preview Scenario P48 — PDF After Reopen

Flow:

```text id="b7m2c9"
Create Session
↓
Close
↓
Reopen
↓
Export PDF
```

Expected:

```text id="r5x8p1"
PDF contains restored session content.
```

---

# 64. Preview Scenario P49 — Search After Restart

Flow:

```text id="k3q7v2"
Create Session
↓
Restart
↓
Search Session
```

Expected:

```text id="n6m1c8"
Stored data remains searchable.
```

---

# 65. Preview Scenario P50 — Study Content Persistence

Flow:

```text id="x9v4p7"
Create Study Material
↓
Save
↓
Restart
↓
Reopen
```

Expected:

```text id="m2q8c5"
Study content remains available where persistence is supported.
```

---

# 66. Preview Smoke Test

Before every preview session run:

```text id="t7n3v5"
[ ] Backend starts
[ ] Frontend starts
[ ] Health endpoint works
[ ] Ollama available
[ ] Model available
[ ] Database available
[ ] Docker available
```

---

# 67. Preview Smoke Test — Core

Then verify:

```text id="c5x2m8"
New Chat
↓
Simple Coding Request
↓
Response
↓
Session Save
```

If this fails, do not continue to cosmetic preview testing.

---

# 68. Preview Gate 1 — Infrastructure

Pass only when:

```text id="p8m1v4"
Backend
Frontend
Database
Ollama
Docker
```

are operational.

---

# 69. Preview Gate 2 — Core AI

Pass only when:

```text id="q3n7c5"
NLP
+
Prompt Builder
+
Context
+
LLM
```

work together.

---

# 70. Preview Gate 3 — Coding

Pass only when:

```text id="m6x2v8"
Generate
+
Validate
+
Debug
+
Explain
```

work.

---

# 71. Preview Gate 4 — Persistence

Pass only when:

```text id="r9c3n6"
Session
+
History
+
Reopen
+
Saved
+
Notes
```

work.

---

# 72. Preview Gate 5 — Study & Export

Pass only when:

```text id="k4m7p1"
Study Mode
+
PDF Export
```

work.

---

# 73. Preview Gate 6 — Safety

Pass only when:

```text id="x8q2v5"
Sandbox
+
Timeout
+
Network Restriction
+
Filesystem Restriction
```

have been verified.

---

# 74. Preview Gate 7 — Full Journey

Required:

```text id="h5n1c9"
Generate
↓
Follow-Up
↓
Debug
↓
Validate
↓
Explain
↓
Optimize
↓
Save
↓
Reopen
↓
Continue
↓
Study
↓
PDF
```

---

# 75. Preview Evidence

For important scenarios, retain evidence:

```text id="s3v7m2"
Screenshots
Test Output
Logs
PDF Sample
Validation Output
Docker Configuration
Observed Performance
```

Evidence must represent actual execution.

---

# 76. Preview Issue Recording

When a problem is discovered:

```text id="q8m4c1"
Preview Issue
↓
Severity
↓
Scenario
↓
Steps
↓
Expected
↓
Actual
↓
Evidence
↓
Owner
↓
Status
```

---

# 77. Preview Severity

Use:

```text id="v5n2x8"
BLOCKER
HIGH
MEDIUM
LOW
```

---

# 78. Preview Blockers

Examples:

```text id="r1c6m9"
Application cannot start
MUST-HAVE feature completely broken
Data loss
Host code execution
Session context leakage
Sandbox bypass
Core offline workflow broken
```

---

# 79. Preview High Issues

Examples:

```text id="n7q3v2"
Debugging frequently fails
Session reopen loses context
PDF export consistently fails
Major multilingual path broken
Severe UI usability issue
```

---

# 80. Preview Medium Issues

Examples:

```text id="m2x8c4"
Edge-case failure
Minor search issue
Small layout problem
Occasional non-critical timeout
```

---

# 81. Preview Low Issues

Examples:

```text id="p6v1k9"
Cosmetic issue
Minor copy issue
Small spacing inconsistency
```

---

# 82. Preview Data Reset

The preview environment may use a resettable database.

Example:

```text id="1q7m4c"
data/preview.db
```

Reset only preview data.

Never accidentally delete production or important development data.

---

# 83. Preview Configuration Check

Verify that preview does not accidentally point to:

```text id="y4c9n1"
Real user data
Production database
Sensitive backup
Unexpected filesystem
```

---

# 84. Preview Security Boundary

The preview should preserve the same fundamental security rules as production-like execution:

```text id="r7m3x8"
No Host Code Execution
No Unrestricted Network
No Sensitive Host Mounts
No Secrets in Source
```

---

# 85. Preview Performance Snapshot

For one representative coding request record:

```text id="a6v2p9"
Input
Model
Context Size
First Token Latency
Total Response Time
Validation Time
Memory
CPU
GPU if available
```

Use actual observations.

---

# 86. Preview Stability Test

Repeat representative operations several times.

Example:

```text id="x3n8c5"
Generate × 5
Debug × 5
Session Open × 5
PDF Export × 3
```

Record failures rather than ignoring them.

---

# 87. Preview Production-Likeness

The preview should avoid development-only shortcuts such as:

```text id="w2m7q4"
Hard-coded test responses
Fake LLM output
Fake validation
Fake PDF generation
Host code execution
Mock-only critical workflows
```

Mocks may be used for isolated tests, but the full preview journey must use the real local stack.

---

# 88. Preview Completion Checklist

```text id="n5c1v7"
[ ] Backend starts
[ ] Frontend starts
[ ] SQLite works
[ ] NLP works
[ ] Ollama works
[ ] Configured model works
[ ] Prompt Builder works
[ ] Context works
[ ] Code generation works
[ ] Code validation works
[ ] Debugging works
[ ] Explanation works
[ ] Optimization works
[ ] Code conversion works
[ ] Free-form coding conversation works
[ ] Suggestions work
[ ] Sessions work
[ ] Reopen works
[ ] Search works
[ ] Saved Messages work
[ ] Notes work
[ ] Study Mode works
[ ] PDF Export works
[ ] Sandbox works
[ ] Sandbox timeout works
[ ] Sandbox network restriction works
[ ] Sandbox filesystem restriction works
[ ] Offline core flow works
```

---

# 89. Full Preview Flow

The canonical preview journey is:

```text id="j8q4m1"
START
 ↓
New Chat
 ↓
"python madhe calculator bana"
 ↓
Language Detection
 ↓
Intent Detection
 ↓
Python Detection
 ↓
Generate Code
 ↓
Validate
 ↓
"yat division by zero error handling add kar"
 ↓
Context Manager
 ↓
Modify Code
 ↓
Validate
 ↓
"हा code Marathi मध्ये explain कर"
 ↓
Explain
 ↓
"हा code आणखी optimize कसा करता येईल?"
 ↓
Optimization
 ↓
Save
 ↓
Close
 ↓
Reopen
 ↓
"आता test cases add कर"
 ↓
Continue
 ↓
Study Mode
 ↓
PDF Export
 ↓
END
```

---

# 90. Preview Success Criteria

The preview is successful when:

```text id="c4n7x2"
The application behaves as one coherent product
```

and not merely as disconnected working modules.

---

# 91. Preview Failure Criteria

Preview must be considered failed if:

```text id="r5m2v8"
A MUST-HAVE feature is unusable
Context is lost
Persistent data is lost
Generated code executes on host
Sandbox can be bypassed
Offline core workflow fails
Application repeatedly crashes
```

---

# 92. Preview Exit Criteria

Before entering Phase 16 QA:

```text id="q1v8c4"
[ ] Infrastructure stable
[ ] Critical user journey works
[ ] MUST-HAVE features verified
[ ] Security baseline verified
[ ] Persistence verified
[ ] Offline core tested
[ ] Major preview blockers resolved
[ ] Evidence collected
[ ] Known limitations documented
```

---

# 93. Antigravity Preview Prompt

```text id="m7c2x9"
Prepare Bhasha2Code for local production-like preview.

Before changing code:
1. Inspect the repository.
2. Inspect TASKS.md.
3. Inspect TESTING.md.
4. Inspect SECURITY_REVIEW.md.
5. Inspect CODE_REVIEW.md.
6. Inspect the existing preview configuration.

Do not add fake responses or mock critical workflows.

Verify:
- Backend
- Frontend
- SQLite
- NLP
- Ollama
- Local coding model
- Context Manager
- Code generation
- Validation
- Debugging
- Sessions
- Study Mode
- PDF
- Docker sandbox

Run the canonical preview workflow:

New Chat
→ Marathi request
→ Generate
→ Follow-up
→ Debug
→ Validate
→ Explain
→ Optimize
→ Save
→ Close
→ Reopen
→ Continue
→ Study
→ PDF

Report:
1. Services working
2. Scenarios passed
3. Scenarios failed
4. Security issues
5. Performance observations
6. Known limitations
7. Recommended fixes
```

---

# 94. Phase 15 Acceptance Criteria

- [x] Local production-like preview defined
- [x] Preview architecture defined
- [x] Startup sequence defined
- [x] Infrastructure checks defined
- [x] Core AI preview defined
- [x] Multilingual preview defined
- [x] Context preview defined
- [x] Code generation preview defined
- [x] Validation preview defined
- [x] Debugging preview defined
- [x] Explanation preview defined
- [x] Optimization preview defined
- [x] Free-form coding conversation preview defined
- [x] Suggestion preview defined
- [x] Session persistence preview defined
- [x] Search preview defined
- [x] Saved messages preview defined
- [x] Notes preview defined
- [x] Study Mode preview defined
- [x] PDF preview defined
- [x] Sandbox preview defined
- [x] Failure recovery preview defined
- [x] Offline preview defined
- [x] Performance snapshot defined
- [x] Preview evidence defined
- [x] Preview issue severity defined
- [x] Preview exit criteria defined
- [x] Canonical full product journey defined
- [x] Antigravity preview workflow defined

---

# 95. Phase 15 Status

**STATUS: COMPLETE**

Bhasha2Code now has a complete production-like local preview process.

The key principle is:

```text id="u7m3q9"
Separate Modules
      ↓
Integrated System
      ↓
Real User Journey
      ↓
Preview Evidence
      ↓
QA
```

---

# 96. Next Phase

## Phase 16 — QA

The next phase will define formal **Quality Assurance** after preview stabilization.

QA will test Bhasha2Code from a real-user perspective across:

```text id="a5n8c2"
English
Hindi
Marathi
Hinglish
Marathi-English
Hindi-English
```

and across the complete product surface:

```text id="m4q7x1"
Coding
Debugging
Explanation
Optimization
Conversion
Context
Sessions
Study
PDF
Sandbox
Offline
```

The goal is to decide whether Bhasha2Code is ready to enter the production deployment phase.