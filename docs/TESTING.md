# Bhasha2Code — Testing Strategy

## Phase 12 — Testing

**Project:** Bhasha2Code  
**Phase:** 12 — Testing  
**Version:** 1.0  
**Status:** COMPLETE  
**Primary Development Tool:** Antigravity  
**Testing Philosophy:** Test every critical behavior, not only whether the application starts.

---

# 1. Purpose

This document defines the testing strategy for Bhasha2Code.

The objective is to verify:

```text
Correctness
+
Reliability
+
Security
+
Context Continuity
+
Multilingual Behavior
+
Offline Operation
+
User Experience
+
Performance
```

Testing must provide evidence for implementation claims.

---

# 2. Testing Principle

The fundamental rule is:

> **Implemented does not mean working. Tested does not automatically mean correct.**

A feature is accepted only after its defined behavior has been verified.

---

# 3. Testing Hierarchy

Bhasha2Code follows:

```text
Unit Tests
    ↓
Component Tests
    ↓
Integration Tests
    ↓
System Tests
    ↓
End-to-End Tests
    ↓
QA
    ↓
Release
```

Each higher level verifies more of the actual system.

---

# 4. Test Categories

The project must cover:

```text
1. Unit Testing
2. NLP Testing
3. LLM Testing
4. Context Testing
5. Code Engine Testing
6. Database Testing
7. API Testing
8. Sandbox Testing
9. Frontend Testing
10. Integration Testing
11. End-to-End Testing
12. Multilingual Testing
13. Offline Testing
14. Performance Testing
15. Security Testing
16. Regression Testing
17. Usability Testing
```

---

# 5. Test Environment

Testing should be performed in:

```text
Development
↓
Local Preview
↓
Production-like Local Environment
```

The final critical tests must run against the same architecture intended for local production.

---

# 6. Test Environment Documentation

Record:

```text
OS
Python Version
Node Version
Backend Version
Frontend Version
Ollama Version
Model Name
Docker Version
CPU
RAM
GPU
```

Do not fabricate environment details.

---

# 7. Test ID Convention

Use:

```text
UT   → Unit Test
NLP  → NLP Test
LLM  → LLM Test
CTX  → Context Test
COD  → Code Engine Test
DB   → Database Test
API  → API Test
SND  → Sandbox Test
UI   → Frontend Test
INT  → Integration Test
E2E  → End-to-End Test
OFF  → Offline Test
PERF → Performance Test
SEC  → Security Test
REG  → Regression Test
UX   → Usability Test
```

Example:

```text
NLP-001
CTX-004
E2E-012
SEC-006
```

---

# 8. Test Status

Use:

```text
TODO
PASS
FAIL
BLOCKED
NOT APPLICABLE
```

A test should not be marked PASS without executing it.

---

# 9. Unit Testing

Unit tests verify individual functions/classes without requiring the complete application.

Test:

```text
Preprocessor
Language Detector
Intent Classifier
Tone Classifier
Programming Language Detector
Requirement Extractor
Context Manager
Prompt Builder
Code Parser
Validator
Repositories
Services
Utility Functions
```

---

# 10. Unit Test Rule

A unit test should ideally verify one clear behavior.

Example:

```text
Input:
"python madhe calculator bana"

Expected:
Intent = GENERATE_CODE
```

---

# 11. NLP Preprocessing Tests

## NLP-001 — English Input

Input:

```text
Create a Python calculator.
```

Expected:

```text
Text processed successfully.
```

---

## NLP-002 — Marathi Input

Input:

```text
Python मध्ये calculator तयार कर.
```

Expected:

```text
Text remains semantically usable.
```

---

## NLP-003 — Hinglish

Input:

```text
Python me calculator bana.
```

Expected:

```text
Mixed-language text preserved.
```

---

## NLP-004 — Marathi-English

Input:

```text
हा Python code explain कर.
```

Expected:

```text
English code terms preserved.
Marathi conversational text preserved.
```

---

# 12. Language Detection Testing

Supported categories:

```text
English
Hindi
Marathi
Hinglish
Marathi-English
Hindi-English
```

---

## NLP-005

Input:

```text
Write a Python program.
```

Expected:

```text
English
```

---

## NLP-006

Input:

```text
Python में program बनाओ.
```

Expected:

```text
Hindi / Hindi-English
```

---

## NLP-007

Input:

```text
Python मध्ये program बनव.
```

Expected:

```text
Marathi / Marathi-English
```

---

## NLP-008

Input:

```text
Python madhe list sort kar.
```

Expected:

```text
Marathi-English
```

---

# 13. Language Detection Edge Cases

Test:

```text
Empty Input
Very Short Input
Numbers Only
Code Only
English + Marathi
English + Hindi
Marathi + Hindi
Technical Terms
Programming Keywords
```

The detector must fail safely rather than inventing a language.

---

# 14. Tone Testing

Supported classes:

```text
CASUAL
FORMAL
SIMPLE
TECHNICAL
SHORT
DETAILED
```

Example:

```text
Explain recursion simply.
```

Expected:

```text
Tone = SIMPLE
```

Another:

```text
Provide a technically detailed explanation of recursion.
```

Expected:

```text
Tone = TECHNICAL / DETAILED
```

---

# 15. Tone Testing Rule

Tone classification does not need to perfectly predict every natural-language variation.

The key requirement is:

```text
reasonable classification
+
safe fallback
+
appropriate response style
```

---

# 16. Intent Testing

Every supported intent must have test cases.

Required:

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

---

# 17. Intent Examples

## Generate

```text
Python madhe calculator bana.
```

Expected:

```text
GENERATE_CODE
```

## Debug

```text
हा code error देतोय fix कर.
```

Expected:

```text
DEBUG_CODE
```

## Explain

```text
हा code line by line explain कर.
```

Expected:

```text
EXPLAIN_CODE
```

## Performance

```text
माझा code slow का आहे?
```

Expected:

```text
PERFORMANCE_ANALYSIS
```

## Security

```text
हा code production साठी safe आहे का?
```

Expected:

```text
SECURITY_ANALYSIS
```

---

# 18. Low-Confidence Intent

Test ambiguous input:

```text
Make this better.
```

Expected behavior:

```text
Low confidence
↓
Safe interpretation
or
Request clarification
```

The system must not confidently perform an unrelated operation.

---

# 19. Programming Language Detection Tests

Test languages:

```text
Python
C
C++
Java
JavaScript
SQL
```

Input sources:

```text
User Statement
Code Syntax
Editor Selection
Previous Context
```

---

# 20. Programming Language Conflict Test

Example:

```text
User says:
Convert this Python code to Java.

Code contains:
Python

Expected:
Source = Python
Target = Java
```

The system must distinguish source and target languages.

---

# 21. Requirement Extraction Tests

Test extraction of:

```text
Task
Language
Input
Output
Constraints
Error
Framework
Tone
Transformation
```

Example:

```text
Create a Python calculator that handles
division by zero and explain it simply.
```

Expected structured information:

```text
Task:
Calculator

Language:
Python

Constraint:
Division by zero handling

Tone:
Simple
```

---

# 22. NLP Pipeline Integration Test

## NLP-INT-001

Input:

```text
Python madhe palindrome program bana simple explanation sobat.
```

Expected structured output should contain:

```text
Language
Intent
Tone
Programming Language
Requirement
```

The exact classifier probabilities are not predetermined.

---

# 23. LLM Testing

LLM testing verifies:

```text
Response Availability
Prompt Correctness
Output Structure
Code Relevance
Instruction Following
Language Matching
Tone Matching
Context Use
```

---

# 24. LLM Availability Test

When Ollama is running:

```text
Expected:
LLM request succeeds.
```

When Ollama is unavailable:

```text
Expected:
Human-readable error.
```

The application must not crash.

---

# 25. LLM Model Test

Verify:

```text
Configured Model
↓
Ollama
↓
Response
```

The application must use the configured local model rather than silently switching to another model.

---

# 26. LLM Output Test

For a code-generation request:

```text
Generate a Python factorial program.
```

The response should contain usable code.

It must not be judged correct solely because the LLM returned text.

Code validation must follow.

---

# 27. LLM Language Test

Input:

```text
हा Python code explain कर.
```

Expected:

```text
Explanation should be primarily Marathi or appropriate Marathi-English.
```

The response language must follow user requirements where practical.

---

# 28. LLM Tone Test

Input:

```text
Explain recursion in simple language.
```

Expected:

```text
Beginner-friendly response.
```

---

# 29. Prompt Builder Tests

Verify that prompt construction includes the appropriate:

```text
User Request
Intent
Language
Tone
Programming Language
Current Code
Relevant Context
Error
```

and excludes irrelevant context.

---

# 30. Context Testing

Context is a MUST-HAVE system capability.

---

# 31. CTX-001 — Basic Follow-Up

Conversation:

```text
User:
Create a Python calculator.

User:
Add error handling.
```

Expected:

```text
Second request modifies the previously generated calculator.
```

---

# 32. CTX-002 — Explanation Follow-Up

Conversation:

```text
Create a Python calculator.

Explain this in Marathi.
```

Expected:

```text
The same calculator is explained.
```

The assistant must not generate an unrelated program.

---

# 33. CTX-003 — Optimization Follow-Up

```text
Create a Python program.

How can I make this faster?
```

Expected:

```text
Optimization analysis of current code.
```

---

# 34. CTX-004 — Conversion Follow-Up

```text
Create Python code.

Convert this to C++.
```

Expected:

```text
Current Python code
↓
C++ conversion
```

---

# 35. CTX-005 — Session Isolation

Session A:

```text
Python Calculator
```

Session B:

```text
C++ Student Management
```

Ask in Session B:

```text
Add validation.
```

Expected:

```text
Only Session B context is used.
```

---

# 36. CTX-006 — Reopen Context

Flow:

```text
Create Code
↓
Close Session
↓
Restart Application
↓
Open Session
↓
Ask Follow-Up
```

Expected:

```text
Previous context available.
```

---

# 37. CTX-007 — Context Limit

Create a long conversation.

Expected:

```text
System remains responsive.
Relevant context retained.
Unnecessary old context controlled.
```

The system must avoid uncontrolled context growth.

---

# 38. Code Generation Testing

Test:

```text
Simple Program
Complex Program
Multiple Inputs
Edge Cases
Different Languages
Mixed-Language Requests
```

---

# 39. Code Parser Testing

Test LLM responses containing:

```text
```python
code
```
```

Plain code:

```text
print("Hello")
```

Response with explanation + code.

Malformed code fence.

Multiple code blocks.

The parser must behave predictably.

---

# 40. Validation Testing

Required conditions:

```text
Valid Code
Syntax Error
Compile Error
Runtime Error
Timeout
Unsupported Language
Empty Code
Malformed Code
```

---

# 41. Python Validation

Example valid code:

```python
print("Hello")
```

Expected:

```text
VALIDATED
```

Example invalid code:

```python
print("Hello"
```

Expected:

```text
VALIDATION_FAILED
```

---

# 42. C / C++ Validation

Test:

```text
Correct Source
Syntax Error
Missing Header
Compilation Error
```

The validator must report compiler failure safely.

---

# 43. Java Validation

Test:

```text
Valid Class
Syntax Error
Compile Error
Incorrect Class Declaration
```

---

# 44. JavaScript Validation

Test:

```text
Valid Syntax
Malformed Syntax
Unsupported Runtime Feature
```

---

# 45. SQL Validation

Test appropriate validation cases.

The system must clearly distinguish:

```text
Syntax validation
```

from:

```text
Actual database execution
```

---

# 46. Debugging Tests

Required:

```text
Syntax Error
Logic Error
Runtime Error
Incorrect Output
Missing Validation
Potential Security Issue
```

---

# 47. Debug Loop Test

Flow:

```text
Invalid Code
↓
Debug
↓
Fix
↓
Validate
```

Expected:

```text
If valid:
STOP
```

If still invalid:

```text
Repair
↓
Validate
```

Maximum:

```text
3 attempts
```

---

# 48. Debug Failure Test

If all repair attempts fail:

```text
Expected:
Repair stops.
Failure is reported honestly.
```

No infinite retry loop.

---

# 49. Explanation Testing

Test:

```text
Simple
Detailed
Technical
Line-by-line
Conceptual
```

Verify that explanation corresponds to the actual code.

---

# 50. Optimization Testing

Test cases with:

```text
Repeated Loops
Unnecessary Computation
Repeated Database Calls
Inefficient Data Structures
High Memory Usage
```

Expected:

```text
Bottleneck identified where reasonably inferable.
Improvement suggested.
```

The system must not claim measured speedups without benchmarking.

---

# 51. Code Conversion Testing

Test:

```text
Python → C++
Python → Java
Python → JavaScript
C++ → Java
Java → Python
```

Where supported.

Verify:

```text
Logic preservation
Target language syntax
Validation
```

---

# 52. Context-Aware Conversation Testing

This is separate from basic intent classification.

Test:

```text
"हा code slow का आहे?"
"यात function वापर."
"इथे error handling add कर."
"हे production साठी safe आहे का?"
"यात test cases add कर."
"याला better architecture दे."
```

The system must answer based on the current code and session context.

---

# 53. Suggestion Testing

Suggestions should be:

```text
Relevant
Contextual
Limited
Non-repetitive
```

Bad behavior:

```text
Every response:
"Add authentication."
"Add dark mode."
"Add database."
```

Good behavior:

```text
Only suggestions relevant to current task.
```

---

# 54. Session Testing

Test:

```text
Create
Open
Rename
Delete
Search
Continue
Restart
```

---

# 55. Session Persistence Test

Flow:

```text
Create Session
↓
Add Messages
↓
Restart Application
↓
Open Session
```

Expected:

```text
Messages preserved.
```

---

# 56. Saved Messages Testing

Test:

```text
Save
Unsave
Restart
View Saved
```

Saved message data must persist.

---

# 57. Notes Testing

Test:

```text
Create Note
Edit Note
Delete Note
Search Note
Restart
```

---

# 58. Study Mode Testing

Test:

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

Expected:

```text
All required sections generated where requested.
```

---

# 59. Study Mode Context Test

Conversation:

```text
User:
Explain Python functions.

User:
Create a quiz on this.
```

Expected:

```text
Quiz is based on the current study topic/context.
```

---

# 60. PDF Testing

Test:

```text
Short Session
Long Session
Code Blocks
Multilingual Text
Validation Results
Study Content
Notes
```

Expected:

```text
Readable PDF
```

---

# 61. PDF Failure Test

Simulate export failure.

Expected:

```text
User receives an understandable error.
Stored session remains unchanged.
```

---

# 62. Database Testing

Test CRUD operations for:

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

# 63. Database Integrity

Verify:

```text
Message belongs to correct session.
Saved message references correct message.
Notes do not accidentally belong to another user/session.
Deleted session behavior is consistent.
```

---

# 64. API Testing

Test:

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

Exact endpoint names should follow the final implementation.

---

# 65. API Error Testing

For invalid requests:

```text
Missing Field
Invalid Type
Empty Input
Unknown Session
Unsupported Language
Invalid Code
Unavailable Model
```

Expected:

```text
Safe HTTP response
+
Human-readable message
```

---

# 66. Frontend Testing

Test:

```text
New Chat
Chat Input
Send
Streaming
Code Display
Copy
Edit
Validate
Run
Debug
Suggestions
Sessions
Search
Saved
Notes
Study Mode
Settings
PDF Export
```

---

# 67. UI State Testing

Test:

```text
Loading
Success
Validation Failed
Model Unavailable
API Error
Empty State
No Search Results
Long Response
Long Code
```

---

# 68. Keyboard Testing

Required:

```text
Enter
Shift+Enter
Ctrl/Cmd+K
Esc
Tab
```

Verify keyboard navigation and focus behavior.

---

# 69. Responsive Testing

Primary target:

```text
Desktop
Laptop
```

Also test narrower windows.

Expected:

```text
Sidebar can collapse.
Main workspace remains usable.
No critical content is hidden.
```

---

# 70. Offline Testing

Offline testing is a major release gate.

---

# 71. OFF-001 — No Internet Core Test

Procedure:

```text
Install everything required
↓
Disable network
↓
Start Bhasha2Code
↓
Create Chat
↓
Generate Code
↓
Explain
↓
Debug
↓
Save
↓
Reopen
```

Expected:

```text
Core workflow works locally.
```

---

# 72. Offline Feature Matrix

| Feature | Expected Offline |
|---|---|
| Chat | PASS |
| NLP | PASS |
| Intent Detection | PASS |
| Tone Detection | PASS |
| Language Detection | PASS |
| LLM | PASS |
| Code Generation | PASS |
| Debugging | PASS |
| Explanation | PASS |
| Validation | PASS |
| Sessions | PASS |
| Search | PASS |
| Saved Messages | PASS |
| Notes | PASS |
| Study Mode | PASS |
| PDF | PASS |
| Sandbox | PASS |
| Optional Cloud Features | Not Required |

---

# 73. Offline Network Verification

The application must not silently send:

```text
User Code
Conversation
Study Data
Session Data
```

to external services during core operation.

---

# 74. Sandbox Testing

Sandbox testing is a high-priority security area.

Test:

```text
Infinite Loop
Large Memory Request
Network Access
File Access
Path Traversal
Process Creation
Long Execution
Large Output
```

---

# 75. Sandbox Timeout Test

Example:

```python
while True:
    pass
```

Expected:

```text
Execution terminated by timeout.
```

The host process should remain protected.

---

# 76. Sandbox Network Test

Example:

```python
import requests
requests.get("https://example.com")
```

Expected:

```text
Network access denied or unavailable inside sandbox.
```

---

# 77. Sandbox File Test

Attempt:

```python
open("/etc/passwd").read()
```

Expected:

```text
Restricted / denied according to sandbox policy.
```

Exact error behavior may vary by sandbox implementation.

---

# 78. Security Testing

Security testing verifies that malicious or malformed inputs cannot bypass application boundaries.

Test:

```text
Prompt Injection
Command Injection
Code Execution
Sandbox Escape
Path Traversal
File Access
Secret Leakage
Malicious Input
```

Detailed security review belongs to Phase 13.

Phase 12 still includes basic security regression tests.

---

# 79. Performance Testing

Measure:

```text
Application Startup
Model Loading
First Token Latency
Total Response Time
NLP Processing Time
Validation Time
PDF Generation Time
Database Query Time
Memory Usage
CPU Usage
GPU Usage
```

---

# 80. Performance Measurement Rule

Do not define fictional targets such as:

```text
"Response always under 2 seconds."
```

unless actual requirements specify them.

Record actual observed values.

---

# 81. Baseline Test

For a representative prompt record:

```text
Prompt
Model
Input Length
Context Size
First Token Time
Total Response Time
Output Tokens where available
RAM
CPU
GPU
```

Repeat tests where practical to account for variability.

---

# 82. Resource Testing

Test:

```text
Short Conversation
Medium Conversation
Long Conversation
Small Code
Large Code
Multiple Sessions
```

Expected:

```text
No uncontrolled memory growth.
```

---

# 83. Regression Testing

Every major change should trigger relevant previous tests.

Example:

Changing:

```text
Context Manager
```

should trigger:

```text
CTX Tests
LLM Tests
Debug Tests
Session Tests
E2E Tests
```

where affected.

---

# 84. Change Impact Testing

When a shared component changes:

```text
Identify Consumers
↓
Run Direct Tests
↓
Run Dependent Tests
↓
Run Relevant E2E
```

---

# 85. Test Data Policy

Test data should:

```text
Be reproducible
Be documented
Avoid unnecessary personal data
Include multilingual examples
Include valid and invalid inputs
```

---

# 86. NLP Dataset Testing

For intent and tone classifiers:

Split data into:

```text
Training
Validation
Testing
```

Do not evaluate only on training data.

---

# 87. NLP Evaluation Metrics

Where applicable, record:

```text
Accuracy
Precision
Recall
F1-score
Confusion Matrix
```

For imbalanced classes, pay particular attention to per-class metrics.

---

# 88. Research Experiment Testing

For the project's research component, compare:

```text
Baseline
vs
NLP-Assisted Structured Prompting
```

Possible task languages:

```text
English
Hindi
Marathi
Hinglish
Marathi-English
```

Measure actual results such as:

```text
Code correctness
Validation success
Compilation success
Response latency
Explanation quality
```

All reported numbers must come from actual experiments.

---

# 89. LLM Evaluation Rule

Do not evaluate an LLM response only by textual similarity.

For generated code, include objective checks where possible:

```text
Syntax
Compilation
Execution
Test Cases
Expected Output
```

---

# 90. Test Case Structure

Each formal test case should contain:

```text
Test ID
Feature
Purpose
Preconditions
Input
Expected Result
Actual Result
Status
Environment
Notes
```

---

# 91. Example Test Case

```text
Test ID:
CTX-001

Feature:
Context-Aware Conversation

Purpose:
Verify follow-up modifies current code.

Precondition:
Session exists.

Input:
Turn 1:
Create a Python calculator.

Turn 2:
Add division-by-zero handling.

Expected:
Existing calculator is modified.

Actual:
<Record actual result>

Status:
PASS / FAIL

Notes:
<Optional>
```

---

# 92. Test Automation

Automate repeatable tests wherever practical.

Preferred tools:

```text
pytest
Frontend test framework
API test client
Docker-based sandbox tests
```

Manual testing remains necessary for:

```text
UX
Visual layout
Study experience
Real multilingual conversation
Some LLM behavior
```

---

# 93. Test Directory Structure

Recommended:

```text id="vt0g0r"
tests/
├── unit/
│   ├── nlp/
│   ├── context/
│   ├── llm/
│   ├── code_engine/
│   └── database/
├── integration/
├── e2e/
├── security/
├── sandbox/
├── offline/
└── fixtures/
```

---

# 94. Test Fixtures

Reusable test inputs should be stored centrally.

Examples:

```text id="0i1yhm"
English prompts
Hindi prompts
Marathi prompts
Mixed-language prompts
Valid code
Invalid code
Errors
Long conversations
```

---

# 95. Test Isolation

Tests should not corrupt development data.

Use:

```text
Test Database
```

instead of the real development database where practical.

---

# 96. Test Cleanup

Automated tests should clean up:

```text
Temporary Files
Temporary Containers
Temporary Database Records
Generated Test Exports
```

where applicable.

---

# 97. Test Logging

Test failures should provide enough information to debug.

A failure should identify:

```text
Input
Expected
Actual
Relevant Error
Environment
```

---

# 98. Flaky Test Rule

A test that sometimes passes and sometimes fails is not considered healthy.

Flaky tests must be:

```text
Investigated
Fixed
or
Explicitly documented
```

Never hide flaky tests by simply disabling them.

---

# 99. LLM Variability Rule

LLM responses may vary.

Therefore, tests should prefer deterministic properties where possible.

Example:

Instead of:

```text
Expected exact sentence
```

test:

```text
Contains code
Uses Python syntax
Passes validation
Respects requested language
```

---

# 100. Acceptance Threshold Rule

Each feature must define its own acceptance condition.

Do not use one arbitrary threshold for every component.

Examples:

```text
Code Validation:
Expected validation state

Session:
Data persists correctly

Intent Classifier:
Measured evaluation metrics

PDF:
Readable generated file

Sandbox:
Unsafe operations contained
```

---

# 101. MUST-HAVE Test Gate

The following must all have passing critical tests:

```text
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
Session Reopen
PDF Export
Study Mode
```

---

# 102. Critical User Journey Test

## E2E-001

```text
New Chat
↓
Marathi Query
↓
Generate Python Code
↓
Follow-Up
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

This is the primary release demonstration workflow.

---

# 103. Failure Recovery Testing

Test when each dependency fails.

```text
Ollama Down
Database Error
Docker Unavailable
Invalid Model
LLM Timeout
Invalid User Input
PDF Export Error
Compiler Missing
```

Expected:

```text
Graceful Error
+
No Silent Data Loss
+
Application Remains Recoverable
```

---

# 104. Startup Testing

Test:

```text
Fresh Startup
Normal Restart
Restart after Error
Restart after Model Failure
Restart after Database Failure
```

---

# 105. Persistence Testing

Restart application after:

```text
Chat
Saved Message
Note
Study Session
Generated Code
```

Verify persistence.

---

# 106. Recovery Testing

If the application terminates during a session:

```text
Restart
↓
Open Session
```

Previously persisted data should remain available.

---

# 107. QA Entry Criteria

Formal QA starts only when:

```text
Core Features Implemented
Critical Unit Tests Pass
Integration Tests Pass
Major Known Errors Documented
Security Baseline Available
Local Preview Running
```

---

# 108. QA Exit Criteria

QA can complete only when:

```text
MUST-HAVE Tests Pass
Critical Bugs Closed
No Critical Data-Loss Issue
No Critical Security Issue
Primary E2E Journey Passes
Offline Core Test Passes
Known Limitations Documented
```

---

# 109. Bug Severity

Use:

```text
P0 — Critical
P1 — High
P2 — Medium
P3 — Low
```

---

# 110. P0 — Critical

Examples:

```text
Host Code Execution
Sandbox Escape
Data Loss
Database Corruption
Major Security Bypass
Complete Application Failure
```

P0 blocks release.

---

# 111. P1 — High

Examples:

```text
MUST-HAVE Feature Broken
Session Context Lost
Debugging Completely Broken
Offline Core Flow Broken
Persistent History Fails
```

P1 normally blocks release.

---

# 112. P2 — Medium

Examples:

```text
UI Inconsistency
Some Edge Cases
Non-critical Search Issue
Minor Performance Regression
```

May block depending on release requirements.

---

# 113. P3 — Low

Examples:

```text
Cosmetic Issue
Minor Copy Issue
Small Layout Adjustment
```

Can be deferred when appropriate.

---

# 114. Bug Report Structure

Use:

```text
Bug ID
Severity
Feature
Environment
Steps to Reproduce
Expected Result
Actual Result
Evidence
Root Cause
Fix
Regression Test
Status
```

---

# 115. Evidence Rule

Where appropriate, preserve evidence such as:

```text
Screenshot
Test Output
Log
Validation Result
Compiler Output
Performance Measurement
```

Do not fabricate evidence.

---

# 116. Test Reporting

At the end of a test cycle report:

```text
Total Tests
Passed
Failed
Blocked
Not Applicable
Critical Bugs
High Bugs
Known Limitations
Release Recommendation
```

---

# 117. Release Recommendation

Possible outcomes:

```text
RELEASE
RELEASE WITH KNOWN LIMITATIONS
BLOCKED
```

---

# 118. No Fake Testing Rule

Never write:

```text
"All tests passed"
```

unless the tests were actually executed.

Never claim:

```text
"Offline verified"
```

without performing the offline test.

Never claim:

```text
"Secure"
```

based only on code inspection.

---

# 119. Testing With Antigravity

Antigravity may create or modify tests, but every generated test must be reviewed for:

```text
Correctness
Meaningful Assertion
Relevant Input
False Positive Risk
Coverage
```

A test that always passes is not useful.

---

# 120. Antigravity Testing Prompt Template

```text
Run the tests related to TASK TXX.

Before changing anything:
1. Inspect the existing implementation.
2. Inspect the existing tests.
3. Identify expected behavior from the documentation.

Do not modify production code just to make a failing test pass.

If a test fails:
1. Identify whether the bug is in implementation or test.
2. Explain the root cause.
3. Make the minimum required change.
4. Re-run affected tests.
5. Run relevant regression tests.

Report:
- Tests executed
- Passed
- Failed
- Changes made
- Remaining issues
```

---

# 121. Testing Workflow

The complete development cycle is:

```text
Implement
↓
Unit Test
↓
Component Test
↓
Integration Test
↓
Regression Test
↓
Security Test
↓
E2E Test
↓
Offline Test
↓
QA
```

---

# 122. Phase 12 Acceptance Criteria

- [x] Testing hierarchy defined
- [x] Unit testing defined
- [x] NLP testing defined
- [x] LLM testing defined
- [x] Context testing defined
- [x] Code generation testing defined
- [x] Validation testing defined
- [x] Debugging testing defined
- [x] Explanation testing defined
- [x] Optimization testing defined
- [x] Conversion testing defined
- [x] Session testing defined
- [x] Study Mode testing defined
- [x] PDF testing defined
- [x] Database testing defined
- [x] API testing defined
- [x] Frontend testing defined
- [x] Sandbox testing defined
- [x] Security regression testing defined
- [x] Offline testing defined
- [x] Performance testing defined
- [x] Regression testing defined
- [x] E2E critical journey defined
- [x] Bug severity defined
- [x] QA entry/exit criteria defined
- [x] No-fake-testing rule defined
- [x] Antigravity testing workflow defined

---

# 123. Phase 12 Status

**STATUS: COMPLETE**

Bhasha2Code now has a complete testing strategy covering:

```text
Code
+
NLP
+
LLM
+
Context
+
Database
+
Sandbox
+
Frontend
+
Security
+
Offline
+
Performance
+
End-to-End QA
```

The testing strategy is designed to prove actual behavior rather than relying on implementation claims.

---

# 124. Next Phase

## Phase 13 — Security Review

The next phase will perform a dedicated security review of:

```text
Prompt Injection
↓
Malicious Input
↓
Code Generation
↓
Code Execution
↓
Docker Sandbox
↓
Filesystem
↓
Secrets
↓
Database
↓
Session Isolation
↓
API Security
↓
Offline / Network Boundaries
```

The main security rule remains:

> **User-generated or AI-generated code must never receive unrestricted access to the host system.**