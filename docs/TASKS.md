# Bhasha2Code — Task Breakdown

## Phase 9 — Development Task Breakdown

**Project:** Bhasha2Code  
**Phase:** 9 — Task Breakdown  
**Version:** 1.0  
**Status:** COMPLETE  
**Primary Development Tool:** Antigravity

---

# 1. Purpose

This document converts the approved Bhasha2Code requirements, architecture, design, and rules into executable development work.

The purpose is to ensure that development happens:

- Incrementally
- In dependency order
- With clear acceptance criteria
- With testing at each meaningful stage
- Without uncontrolled AI-generated changes

---

# 2. Task Hierarchy

All development work follows:

```text
EPIC
  ↓
FEATURE
  ↓
TASK
  ↓
SUBTASK
```

Each task should have:

```text
Task ID
Title
Description
Dependencies
Files / Modules
Acceptance Criteria
Testing
Status
```

---

# 3. Status Definitions

```text
TODO
IN PROGRESS
BLOCKED
REVIEW
DONE
```

### TODO
Not started.

### IN PROGRESS
Currently being implemented.

### BLOCKED
Cannot continue because a dependency or issue exists.

### REVIEW
Implementation completed and requires review/testing.

### DONE
Acceptance criteria and required tests are complete.

---

# 4. Development Strategy

Build the application in the following order:

```text
Foundation
↓
Backend
↓
Database
↓
NLP
↓
LLM
↓
Code Engine
↓
Context
↓
Core Coding Features
↓
Sessions
↓
Study Features
↓
Export
↓
Sandbox
↓
Frontend Integration
↓
Testing
↓
Security
↓
Production
```

---

# 5. EPIC E01 — Project Foundation

## E01-F01 Repository Foundation

### T01 — Create Project Structure

**Goal:** Create the approved Bhasha2Code directory structure.

**Dependencies:** None

**Expected directories:**

```text
backend/
frontend/
data/
models/
tests/
exports/
docker/
docs/
```

**Acceptance Criteria:**

- Required directories exist
- No unnecessary directories created
- Git repository initialized

**Status:** DONE

---

### T02 — Create Backend Environment

**Goal:** Create isolated Python development environment.

**Dependencies:** T01

**Acceptance Criteria:**

- Virtual environment works
- Python version documented
- Dependencies can be installed
- Backend can start

**Status:** DONE

---

### T03 — Create Backend Skeleton

**Goal:** Create initial FastAPI application.

**Dependencies:** T02

**Acceptance Criteria:**

- FastAPI starts
- Health endpoint works
- Project follows approved architecture

Example:

```text
GET /health
```

Expected:

```text
healthy
```

**Status:** DONE

---

### T04 — Create Frontend Skeleton

**Goal:** Create React + Vite frontend.

**Dependencies:** T01

**Acceptance Criteria:**

- Frontend starts
- Basic application renders
- No unnecessary UI components
- Design follows `DESIGN.md`

**Status:** TODO

---

# 6. EPIC E02 — Database

## E02-F01 Database Foundation

### T05 — Configure SQLite

**Dependencies:** T03

**Acceptance Criteria:**

- SQLite database created
- Connection configuration implemented
- Database path configurable

**Status:** DONE

---

### T06 — Create Database Models

Create initial models for:

```text
users
sessions
messages
saved_messages
notes
generated_code
debug_history
```

**Dependencies:** T05

**Acceptance Criteria:**

- Models defined
- Relationships documented
- Database initializes successfully

**Status:** DONE

---

### T07 — Create Repository Layer

**Goal:** Centralize database access.

**Dependencies:** T06

**Acceptance Criteria:**

- CRUD operations available
- API routes do not directly contain database logic
- Tests added

**Status:** DONE

---

# 7. EPIC E03 — NLP Pipeline

## E03-F01 Text Preprocessing

### T08 — Implement Text Preprocessing

Support:

```text
English
Hindi
Marathi
Hinglish
Marathi-English
Hindi-English
```

**Dependencies:** T03

**Acceptance Criteria:**

- Input normalization works
- Code is preserved correctly
- Mixed-language text is not destroyed

**Status:** DONE

---

## E03-F02 Language Detection

### T09 — Implement Language Detection

**Goal:** Detect user language.

**Dependencies:** T08

**Acceptance Criteria:**

- English detected
- Hindi detected
- Marathi detected
- Hinglish handled
- Mixed input handled reasonably
- Confidence available where practical

**Status:** DONE

---

## E03-F03 Tone Classification

### T10 — Create Tone Dataset

Classes:

```text
CASUAL
FORMAL
SIMPLE
TECHNICAL
SHORT
DETAILED
```

**Dependencies:** T08

**Acceptance Criteria:**

- Dataset documented
- Training/test split created
- Data quality checked

**Status:** DONE

---

### T11 — Train Tone Classifier

Preferred initial approach:

```text
TF-IDF
+
Logistic Regression
```

**Dependencies:** T10

**Acceptance Criteria:**

- Classifier trains
- Evaluation metrics generated
- Model can predict supported tone classes
- Model saved locally

**Status:** DONE

---

## E03-F04 Intent Classification

### T12 — Create Intent Dataset

Initial classes (18 intent labels):

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
SEARCH
```

**Dependencies:** T08

**Acceptance Criteria:**

- All 18 classes represented (balanced at exactly 60 samples each, 1080 total)
- Dataset documented (`data/datasets/intent/README.md`)
- Balanced across 6 language varieties: English, Hindi, Marathi, Hinglish, Marathi-English, Hindi-English
- Mixed-language and transliterated queries included
- Orthogonality from Tone verified
- Deterministic 70% train / 15% val / 15% test splits with zero data leakage
- Comprehensive validation script (`scripts/validate_intent_dataset.py`) passes

**Status:** DONE

---

### T13 — Train Intent Classifier

Preferred approach:

```text
TF-IDF
+
Logistic Regression
```

**Dependencies:** T12

**Acceptance Criteria:**

- Model trains successfully
- Evaluation performed
- Model saved locally
- Low-confidence fallback defined

**Status:** TODO

---

## E03-F05 Programming Language Detection

### T14 — Implement Programming Language Detector

Initial languages:

```text
Python
C
C++
Java
JavaScript
SQL
```

**Dependencies:** T08

**Acceptance Criteria:**

- Detect from code syntax
- Detect from explicit user request
- Handle code + text combinations
- Resolve conflicts predictably

**Status:** TODO

---

## E03-F06 Requirement Extraction

### T15 — Implement Requirement Extraction

Extract useful entities such as:

```text
Programming Language
Task
Framework
Input
Output
Constraints
Error
Requested Tone
Requested Transformation
```

**Dependencies:** T09, T13, T14

**Acceptance Criteria:**

- Structured output generated
- Missing fields handled safely
- Tests added

**Status:** TODO

---

## E03-F07 NLP Pipeline Integration

### T16 — Integrate Complete NLP Pipeline

Flow:

```text
User Input
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

**Dependencies:** T09, T11, T13, T14, T15

**Acceptance Criteria:**

- Single pipeline API available
- Structured result returned
- Unit tests pass

**Status:** TODO

---

# 8. EPIC E04 — Local LLM

## E04-F01 Ollama Integration

### T17 — Configure Ollama

**Goal:** Connect backend to local Ollama service.

**Dependencies:** T03

**Acceptance Criteria:**

- Ollama health check works
- Model configuration externalized
- Backend detects unavailable model safely

**Status:** TODO

---

### T18 — Implement LLM Service

Expected abstraction:

```text
LLMService
├── generate()
├── stream()
├── health_check()
└── model_info()
```

**Dependencies:** T17

**Acceptance Criteria:**

- Backend can send prompt to local model
- Response returned
- Errors handled
- No hard-coded business logic inside provider

**Status:** TODO

---

# 9. EPIC E05 — Prompt Builder

### T19 — Implement Prompt Templates

Prompt categories:

```text
Code Generation
Debugging
Explanation
Optimization
Conversion
Review
Suggestion
Study
```

**Dependencies:** T16, T18

**Acceptance Criteria:**

- Prompts centralized
- Context variables supported
- User language respected
- Requested tone respected

**Status:** TODO

---

### T20 — Implement Structured Prompt Builder

Input:

```text
User Request
Language
Tone
Intent
Programming Language
Current Code
Relevant Context
Error
```

Output:

```text
Structured LLM Prompt
```

**Dependencies:** T19

**Acceptance Criteria:**

- Correct prompt selected by intent
- Unnecessary context excluded
- Tests added

**Status:** TODO

---

# 10. EPIC E06 — Context Manager

### T21 — Create Context Manager

Flow:

```text
Current Request
+
Current Code
+
Current Task
+
Recent Messages
+
Session Information
↓
Context Manager
```

**Dependencies:** T07, T20

**Acceptance Criteria:**

- Context stored per session
- Relevant context returned
- Context size controlled

**Status:** TODO

---

### T22 — Implement Context-Aware Follow-Up

Example:

```text
User:
python madhe calculator bana

User:
yat error handling add kar
```

Second request must operate on the correct calculator context.

**Dependencies:** T21

**Acceptance Criteria:**

- Follow-up recognized
- Previous code available
- Modified code generated
- Session isolation verified

**Status:** TODO

---

# 11. EPIC E07 — Code Generation

### T23 — Implement Code Generation Service

**Dependencies:** T20, T21

**Acceptance Criteria:**

- User request converted to prompt
- Local LLM generates code
- Programming language retained
- Result structured correctly

**Status:** TODO

---

### T24 — Implement Code Response Parser

Expected output structure:

```text
Explanation
Code
Language
Warnings
Suggestions
```

**Dependencies:** T23

**Acceptance Criteria:**

- Code extracted reliably
- Markdown/code fences handled
- Plain-text responses handled safely

**Status:** TODO

---

# 12. EPIC E08 — Code Validation

### T25 — Implement Static Validation

Initial support:

```text
Python AST
C syntax/compilation
C++ compilation
Java compilation
JavaScript syntax
SQL validation where practical
```

**Dependencies:** T24

**Acceptance Criteria:**

- Syntax errors detected
- Supported languages reported
- Unsupported execution clearly reported

**Status:** TODO

---

### T26 — Implement Validation Result Model

States:

```text
VALIDATED
VALIDATION_FAILED
NOT_VALIDATED
UNSUPPORTED
```

**Dependencies:** T25

**Acceptance Criteria:**

- Standard response format
- Validation details preserved

**Status:** TODO

---

# 13. EPIC E09 — Debugging

### T27 — Implement Debugging Service

Input:

```text
Code
Error
Language
Context
```

Output:

```text
Problem
Cause
Fix
Corrected Code
```

**Dependencies:** T20, T24, T26

**Status:** TODO

---

### T28 — Implement Validation-Repair Loop

Flow:

```text
Generate Fix
↓
Validate
↓
Pass?
 ├── YES → Return
 └── NO → Repair
```

Maximum attempts:

```text
3
```

**Dependencies:** T27

**Acceptance Criteria:**

- Maximum attempts enforced
- Successful fixes stop the loop
- Failed fixes report honestly

**Status:** TODO

---

# 14. EPIC E10 — Explanation

### T29 — Implement Code Explanation

Support levels:

```text
Simple
Detailed
Technical
```

Languages:

```text
English
Hindi
Marathi
```

**Dependencies:** T20, T24

**Acceptance Criteria:**

- Explanation follows requested tone
- Code remains unchanged unless modification requested

**Status:** TODO

---

# 15. EPIC E11 — Optimization

### T30 — Implement Code Optimization

The service should identify:

```text
Time Complexity
Repeated Work
Unnecessary Loops
Memory Issues
Readability Problems
```

**Dependencies:** T20, T24

**Acceptance Criteria:**

- Bottleneck identified
- Improvement suggested
- Optimized code optional
- No unsupported performance claims

**Status:** TODO

---

# 16. EPIC E12 — Code Conversion

### T31 — Implement Code Conversion

Examples:

```text
Python → C++
Python → Java
C++ → Java
Java → Python
```

**Dependencies:** T20, T24

**Acceptance Criteria:**

- Target language correctly applied
- Logic preserved as far as practical
- Result validated where supported

**Status:** TODO

---

# 17. EPIC E13 — Context-Aware Coding Conversation

### T32 — Implement Free-Form Coding Conversation

Users must be able to ask unrestricted coding questions.

Examples:

```text
हा code slow का आहे?

यात loop ऐवजी दुसरं काही वापरता येईल का?

माझ्या code मध्ये memory जास्त का वापरते?

हा approach योग्य आहे का?

हा code production साठी safe आहे का?

माझ्या project ला पुढे काय features add करू?
```

**Dependencies:** T16, T21, T23

**Acceptance Criteria:**

- No forced intent buttons
- System classifies relevant intent
- Existing code/context can be used
- Appropriate response type selected

**Status:** TODO

---

# 18. EPIC E14 — Suggestion Engine

### T33 — Implement Contextual Suggestions

Suggestion types:

```text
Code Review
Performance
Security
Best Practice
Approach
Architecture
Feature
Testing
```

**Dependencies:** T32

**Acceptance Criteria:**

- Suggestions are context-aware
- Maximum 3–5 relevant suggestions
- No suggestion spam
- Suggestions do not override direct answers

**Status:** TODO

---

# 19. EPIC E15 — Sessions

### T34 — Create Session Manager

Operations:

```text
Create
Open
Rename
Delete
Continue
```

**Dependencies:** T07, T21

**Acceptance Criteria:**

- Sessions persist
- Unique session IDs
- Correct session loading

**Status:** TODO

---

### T35 — Implement Chat History

**Dependencies:** T34

**Acceptance Criteria:**

- Messages saved
- Messages loaded correctly
- History remains after application restart

**Status:** TODO

---

### T36 — Implement Session Reopen / Continue

**Dependencies:** T35, T21

**Acceptance Criteria:**

```text
Close session
↓
Reopen session
↓
Previous context restored
↓
Follow-up works
```

**Status:** TODO

---

### T37 — Implement Chat Search

**Dependencies:** T35

**Acceptance Criteria:**

- Search sessions
- Search messages
- Results local
- Search does not break active context

**Status:** TODO

---

# 20. EPIC E16 — Saved Messages & Notes

### T38 — Implement Saved Messages

Operations:

```text
Save
Unsave
View Saved
```

**Dependencies:** T35

**Status:** TODO

---

### T39 — Implement Personal Notes

Operations:

```text
Create
Edit
Delete
Search
```

**Dependencies:** T07

**Status:** TODO

---

# 21. EPIC E17 — Study Mode

### T40 — Create Study Mode

Structure:

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

**Dependencies:** T20, T35

**Acceptance Criteria:**

- Study content can be generated
- Existing session context can be used
- Content is understandable
- Study mode is visually minimalist

**Status:** TODO

---

# 22. EPIC E18 — PDF Export

### T41 — Implement Session PDF Export

Export:

```text
Session Information
Messages
Code
Explanations
Validation Results
Study Content
Notes where selected
```

**Dependencies:** T35, T40

**Acceptance Criteria:**

- PDF generated locally
- Formatting readable
- Long sessions handled
- Export failure does not affect stored data

**Status:** TODO

---

# 23. EPIC E19 — Safe Code Sandbox

### T42 — Create Docker Execution Environment

**Dependencies:** T25

**Acceptance Criteria:**

- Docker execution available
- Non-root execution
- Network disabled
- Resource limits configurable
- Timeout implemented

**Status:** TODO

---

### T43 — Implement Sandbox Execution Service

**Dependencies:** T42

**Acceptance Criteria:**

- Supported code can execute inside sandbox
- Host filesystem inaccessible
- Process timeout enforced
- Output captured safely

**Status:** TODO

---

### T44 — Sandbox Security Tests

Test:

```text
Infinite Loop
Large Memory Allocation
Network Request
File Access
Path Traversal
Process Abuse
```

**Dependencies:** T43

**Acceptance Criteria:**

- Unsafe operations blocked or contained
- Host remains protected
- Results documented

**Status:** TODO

---

# 24. EPIC E20 — Frontend

## E20-F01 Core Layout

### T45 — Implement Main Application Layout

Layout:

```text
Sidebar
+
Main Chat Workspace
```

**Dependencies:** T04

**Acceptance Criteria:**

- Minimalist white-first design
- Desktop/laptop optimized
- No unnecessary permanent right panel

**Status:** TODO

---

### T46 — Implement Sidebar

Include:

```text
New Chat
Recent
Saved
Notes
Study Mode
Search
Settings
```

**Dependencies:** T45

**Status:** TODO

---

### T47 — Implement Chat Interface

**Dependencies:** T45

**Acceptance Criteria:**

- User message display
- Assistant response display
- Comfortable reading width
- Free-form input

**Status:** TODO

---

### T48 — Implement Composer

Features:

```text
Enter → Send
Shift+Enter → New Line
```

**Dependencies:** T47

**Status:** TODO

---

### T49 — Implement Code Block UI

Actions:

```text
Copy
Edit
Validate
Run
```

where supported.

**Dependencies:** T47

**Status:** TODO

---

### T50 — Integrate Monaco Editor

Support:

```text
Syntax Highlighting
Line Numbers
Editing
Search
Error Markers
Language Selection
```

**Dependencies:** T49

**Status:** TODO

---

### T51 — Implement Validation UI

Display:

```text
✓ Validated
✕ Validation Failed
○ Not Validated
⚠ Unsupported
```

**Dependencies:** T26, T50

**Status:** TODO

---

### T52 — Implement Debugging UI

Structure:

```text
Problem
Cause
Fix
Corrected Code
Validation
```

**Dependencies:** T27, T51

**Status:** TODO

---

### T53 — Implement Suggestions UI

**Dependencies:** T33

**Acceptance Criteria:**

- Suggestions compact
- Maximum 3–5 displayed
- No visual clutter

**Status:** TODO

---

# 25. EPIC E21 — Session UI

### T54 — Session List

**Dependencies:** T34, T46

**Status:** TODO

---

### T55 — Session Rename/Delete

**Dependencies:** T54

**Acceptance Criteria:**

- Intentional actions
- No accidental deletion
- Confirmation where appropriate

**Status:** TODO

---

### T56 — Reopen and Continue Session

**Dependencies:** T36, T55

**Status:** TODO

---

# 26. EPIC E22 — Study UI

### T57 — Study Mode Interface

**Dependencies:** T40

**Acceptance Criteria:**

- Minimalist notebook style
- Easy reading
- Practice and quiz sections usable

**Status:** TODO

---

### T58 — Notes Interface

**Dependencies:** T39

**Status:** TODO

---

# 27. EPIC E23 — Search & Saved UI

### T59 — Search Interface

**Dependencies:** T37

**Status:** TODO

---

### T60 — Saved Messages Interface

**Dependencies:** T38

**Status:** TODO

---

# 28. EPIC E24 — Settings

### T61 — Settings Interface

Settings:

```text
Appearance
AI Model
Execution
Data
```

**Dependencies:** T46

**Status:** TODO

---

### T62 — Local Model Status

Statuses:

```text
Ready
Loading
Busy
Unavailable
Error
```

**Dependencies:** T17, T18

**Status:** TODO

---

# 29. EPIC E25 — API Integration

### T63 — Create Chat API

**Dependencies:** T23, T34

**Status:** TODO

---

### T64 — Create Debug API

**Dependencies:** T27

**Status:** TODO

---

### T65 — Create Explain API

**Dependencies:** T29

**Status:** TODO

---

### T66 — Create Optimize API

**Dependencies:** T30

**Status:** TODO

---

### T67 — Create Convert API

**Dependencies:** T31

**Status:** TODO

---

### T68 — Create Validate API

**Dependencies:** T25, T26

**Status:** TODO

---

### T69 — Create Session APIs

Operations:

```text
Create
List
Open
Rename
Delete
```

**Dependencies:** T34, T35

**Status:** TODO

---

### T70 — Create Study API

**Dependencies:** T40

**Status:** TODO

---

### T71 — Create PDF Export API

**Dependencies:** T41

**Status:** TODO

---

# 30. EPIC E26 — Streaming

### T72 — Implement LLM Streaming

**Dependencies:** T18, T63

**Acceptance Criteria:**

- Tokens displayed incrementally
- UI remains responsive
- Cancel/error states handled

**Status:** TODO

---

# 31. EPIC E27 — Integration

### T73 — Integrate Frontend with Backend

**Dependencies:** T45–T72

**Acceptance Criteria:**

- Chat works end-to-end
- Sessions work
- Code operations work
- Study Mode works
- PDF export works

**Status:** TODO

---

### T74 — Complete Primary User Journey

Required journey:

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

**Dependencies:** T73

**Status:** TODO

---

# 32. EPIC E28 — Testing

### T75 — Unit Test Suite

Test:

```text
NLP
Context
Prompt Builder
Parser
Validator
Repositories
Services
```

**Dependencies:** Relevant implementation tasks

**Status:** TODO

---

### T76 — Integration Test Suite

Test:

```text
API
Database
NLP → LLM
LLM → Validation
Session → Context
```

**Dependencies:** T75

**Status:** TODO

---

### T77 — End-to-End Test Suite

Test complete user journeys.

**Dependencies:** T74

**Status:** TODO

---

### T78 — Multilingual Test Suite

Test:

```text
English
Hindi
Marathi
Hinglish
Marathi-English
Hindi-English
```

**Dependencies:** T77

**Status:** TODO

---

### T79 — Context Continuity Test Suite

Example:

```text
Create code
↓
Modify code
↓
Explain code
↓
Debug code
↓
Optimize code
↓
Reopen session
↓
Continue
```

**Dependencies:** T77

**Status:** TODO

---

# 33. EPIC E29 — Security

### T80 — Prompt Injection Review

**Dependencies:** Core implementation complete

**Status:** TODO

---

### T81 — Code Execution Security Review

**Dependencies:** T44

**Status:** TODO

---

### T82 — File and Secret Security Review

Check:

```text
.env
logs
uploads
exports
filesystem access
path traversal
```

**Dependencies:** Core implementation

**Status:** TODO

---

### T83 — Security Regression Tests

**Dependencies:** T80, T81, T82

**Status:** TODO

---

# 34. EPIC E30 — Code Review

### T84 — Architecture Review

Check:

```text
Frontend
API
Services
NLP
Context
LLM
Database
Sandbox
```

**Dependencies:** T73

**Status:** TODO

---

### T85 — Code Quality Review

Check:

```text
Duplicate Code
Large Functions
Unused Code
Naming
Error Handling
Maintainability
```

**Dependencies:** T73

**Status:** TODO

---

### T86 — Dependency Review

Check:

```text
Unused Packages
Security Concerns
Offline Compatibility
Version Constraints
```

**Dependencies:** T73

**Status:** TODO

---

# 35. EPIC E31 — Preview

### T87 — Production-Like Local Preview

Environment:

```text
localhost
+
FastAPI
+
Frontend
+
SQLite
+
Ollama
+
Docker Sandbox
```

**Dependencies:** T83, T84, T85, T86

**Status:** TODO

---

### T88 — Full Manual Preview

Run the critical flow:

```text
Marathi
→ Generate
→ Follow-up
→ Debug
→ Explain
→ Optimize
→ Save
→ Reopen
→ Continue
→ PDF
```

**Dependencies:** T87

**Status:** TODO

---

# 36. EPIC E32 — QA

### T89 — QA Scenario Execution

Test realistic user scenarios.

Examples:

```text
Beginner Student
Engineering Student
Programming Learner
Mixed-Language User
Debugging User
Study User
```

**Dependencies:** T88

**Status:** TODO

---

### T90 — MUST-HAVE QA Gate

Every MUST HAVE feature must pass.

Required:

```text
Multilingual Input
Code Generation
Context-Aware Conversation
Debugging
Explanation
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

**Dependencies:** T89

**Status:** TODO

---

# 37. EPIC E33 — Production

### T91 — Local Production Configuration

**Dependencies:** T90

**Status:** TODO

---

### T92 — Startup and Recovery

Handle:

```text
Ollama unavailable
Database unavailable
Docker unavailable
Invalid request
Model error
```

**Dependencies:** T91

**Status:** TODO

---

### T93 — Backup and Recovery

Define:

```text
SQLite backup
Important export backup
Configuration backup
Recovery procedure
```

**Dependencies:** T91

**Status:** TODO

---

### T94 — Docker Compose

Services where appropriate:

```text
Frontend
Backend
Sandbox
```

Ollama may remain a host/local dependency depending on the final deployment architecture.

**Dependencies:** T92

**Status:** TODO

---

# 38. EPIC E34 — Monitoring

### T95 — Local Performance Monitoring

Track:

```text
First Token Latency
Total Response Time
LLM Errors
API Errors
RAM
CPU
GPU
Database
Validation Results
```

**Dependencies:** T91

**Status:** TODO

---

### T96 — Local Error Monitoring

Record safe operational events.

**Dependencies:** T95

**Status:** TODO

---

# 39. Recommended Implementation Milestones

## Milestone M1 — Foundation

```text
T01–T07
```

Result:

```text
Project
+
FastAPI
+
React
+
SQLite
```

---

## Milestone M2 — NLP

```text
T08–T16
```

Result:

```text
Multilingual NLP Pipeline
```

---

## Milestone M3 — Local AI

```text
T17–T24
```

Result:

```text
NLP
+
Context
+
Ollama
+
Prompt Builder
+
Code Generation
```

---

## Milestone M4 — Code Intelligence

```text
T25–T33
```

Result:

```text
Validation
+
Debugging
+
Explanation
+
Optimization
+
Conversion
+
Suggestions
```

---

## Milestone M5 — Persistence & Study

```text
T34–T41
```

Result:

```text
Sessions
+
History
+
Saved
+
Notes
+
Study Mode
+
PDF
```

---

## Milestone M6 — Safe Execution

```text
T42–T44
```

Result:

```text
Docker Sandbox
```

---

## Milestone M7 — Frontend

```text
T45–T62
```

Result:

```text
Complete Bhasha2Code UI
```

---

## Milestone M8 — API & Integration

```text
T63–T74
```

Result:

```text
Working End-to-End Application
```

---

## Milestone M9 — Quality

```text
T75–T90
```

Result:

```text
Tested
+
Reviewed
+
Security Checked
+
QA Verified
```

---

## Milestone M10 — Local Production

```text
T91–T96
```

Result:

```text
Local Production-Ready Candidate
```

---

# 40. Critical Path

The most important dependency path is:

```text
Project Foundation
↓
FastAPI
↓
SQLite
↓
NLP Pipeline
↓
Ollama
↓
Prompt Builder
↓
Context Manager
↓
Code Generation
↓
Validation
↓
Debugging
↓
Sessions
↓
Frontend
↓
Integration
↓
Testing
↓
Security
↓
QA
↓
Local Production
```

---

# 41. V1 Priority Order

When development time is limited, follow this priority:

### Priority 1 — Core AI

```text
NLP
+
Ollama
+
Prompt Builder
+
Context
+
Code Generation
```

### Priority 2 — Core Coding

```text
Validation
+
Debugging
+
Explanation
+
Context-Aware Conversation
```

### Priority 3 — Persistence

```text
Sessions
+
History
+
Reopen
```

### Priority 4 — Study

```text
Study Mode
+
Notes
+
Saved Messages
```

### Priority 5 — Export

```text
PDF
```

### Priority 6 — Safe Execution

```text
Docker Sandbox
```

### Priority 7 — Polish

```text
Streaming
+
Animations
+
Advanced UI
```

Polish must never take priority over broken core functionality.

---

# 42. Antigravity Task Execution Format

Each Antigravity task should use this structure:

```text
TASK ID:
TXX

GOAL:
<What should be built?>

INSPECT:
<List existing files/docs to inspect>

DEPENDENCIES:
<Required completed tasks>

CONSTRAINTS:
<Project rules>

IMPLEMENTATION:
<What should be changed?>

ACCEPTANCE CRITERIA:
<How success will be verified>

TEST:
<Required tests>

REPORT:
<Files changed + tests + known issues>
```

---

# 43. Example Antigravity Task

```text
TASK ID:
T22

GOAL:
Implement context-aware follow-up handling.

INSPECT:
backend/context/
backend/database/
backend/llm/
docs/06_architecture/ARCHITECTURE.md
docs/08_rules/RULES_REFERENCE.md

DEPENDENCIES:
T21

CONSTRAINTS:
- Preserve session isolation.
- Do not rewrite working modules unnecessarily.
- Do not send unlimited history to the LLM.
- Follow existing architecture.

IMPLEMENTATION:
Support follow-up requests that refer to previously generated code.

Example:
"python madhe calculator bana"
→ generate calculator

"yat error handling add kar"
→ modify the same calculator

ACCEPTANCE CRITERIA:
- Correct session selected
- Previous code available
- Follow-up resolved
- Modified code generated
- Existing tests pass

TEST:
Add context continuity tests.

REPORT:
Files changed
Tests passed
Known limitations
```

---

# 44. Definition of Done for Any Task

A task can move to `DONE` only when:

```text
[ ] Goal understood
[ ] Dependencies satisfied
[ ] Existing code inspected
[ ] Implementation completed
[ ] Acceptance criteria satisfied
[ ] Tests completed
[ ] No critical error remains
[ ] Relevant documentation updated
[ ] Antigravity reports files changed
[ ] Known limitations documented
```

---

# 45. Development Rule

Never give Antigravity the instruction:

```text
"Build the complete Bhasha2Code project."
```

Preferred:

```text
"Implement T22 — Context-Aware Follow-Up."
```

One task at a time.

For larger tasks:

```text
Task
↓
Subtask
↓
Implementation
↓
Test
↓
Review
```

---

# 46. Phase 9 Acceptance Criteria

- [x] Full feature hierarchy defined
- [x] Tasks converted into executable units
- [x] Dependencies identified
- [x] Acceptance criteria added
- [x] Testing associated with major tasks
- [x] MUST HAVE priority protected
- [x] Antigravity task format defined
- [x] Milestones defined
- [x] Critical path defined
- [x] Definition of Done defined
- [x] Local production path defined

---

# 47. Phase 9 Status

**STATUS: COMPLETE**

Bhasha2Code now has a structured implementation backlog that can be executed incrementally using Antigravity.

The task system is designed to prevent:

- uncontrolled AI changes
- duplicate implementation
- scope creep
- dependency confusion
- untested features
- false completion claims

---

# 48. Next Phase

## Phase 10 — Setup

The next phase will define the exact development environment required to run Bhasha2Code:

```text
OS
↓
Python
↓
Virtual Environment
↓
Node.js
↓
React/Vite
↓
FastAPI
↓
SQLite
↓
spaCy / NLTK
↓
Ollama
↓
Local Coding Model
↓
Docker
↓
Git
↓
Antigravity
```

The output will be:

```text
Fresh Machine
↓
Setup Commands
↓
Dependencies Installed
↓
Backend Running
↓
Frontend Running
↓
Ollama Running
↓
First Local AI Response
```