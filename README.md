# Bhasha2Code

> **An Offline Multilingual, Context-Aware AI Coding and Study Assistant**

---

## 1. Overview

Bhasha2Code is an offline AI-powered coding assistant designed to understand natural programming requests written in English, Hindi, Marathi, Hinglish, and mixed-language input.

It uses NLP techniques to understand the user's language, tone, intent, programming language, and requirements before passing structured information to a local coding LLM.

The system can generate, debug, explain, review, optimize, and improve code while maintaining conversation context.

It also provides persistent coding/study sessions, Study Mode, personal notes, saved content, and PDF export.

---

## 2. Why Bhasha2Code?

Many coding assistants assume that users communicate primarily in English and often require users to formulate technically precise prompts.

Bhasha2Code focuses on a more natural interaction model.

A student can ask:

> "bhai python madhe palindrome check karnara code de"

instead of writing a formal programming prompt.

The system should understand the request and respond appropriately.

---

## 3. Core Capabilities

### Multilingual NLP

- English
- Hindi
- Marathi
- Hinglish
- Marathi-English
- Hindi-English

### Coding

- Code generation
- Debugging
- Explanation
- Code review
- Optimization
- Conversion
- Algorithm generation
- Code validation

### Context Awareness

- Follow-up questions
- Previous code context
- Conversation context
- Current programming language
- Current task context

### AI Suggestions

The assistant can suggest:

- Better approaches
- Best practices
- Performance improvements
- Security improvements
- Error handling
- Relevant features

Suggestions are generated only when useful.

### Offline AI

- Local LLM
- Ollama
- Local NLP
- Local database
- No mandatory cloud API

### Study System

- Persistent sessions
- Session reopening
- Study Mode
- Saved messages
- Personal notes
- Search
- PDF export

---

## 4. Example

### User

```text
bhai python madhe calculator banav
```

### Bhasha2Code

The system identifies:

```text
Language: Marathi-English
Tone: Casual
Intent: Code Generation
Programming Language: Python
Task: Calculator
```

It then generates the code using the local LLM.

The user can continue:

```text
yat error handling add kar
```

The system understands that the request refers to the previously generated calculator.

---

## 5. System Architecture

```text
                 USER
                   ↓
             Offline UI
                   ↓
              FastAPI
                   ↓
             NLP Pipeline
                   ↓
            Context Manager
                   ↓
             Prompt Builder
                   ↓
                Ollama
                   ↓
             Local LLM
                   ↓
       ┌───────────┼───────────┐
       ↓           ↓           ↓
      Code       Explain     Suggestions
       ↓
   Validation
       ↓
 Safe Execution
       ↓
    Response
```

Supporting components:

```text
SQLite
Session Manager
PDF Export
Docker Sandbox
```

---

## 6. Technology Direction

### Backend

- Python
- FastAPI

### NLP

- spaCy
- NLTK
- TF-IDF
- Logistic Regression
- Regex / rule-based processing
- Language detection

### AI

- Ollama
- Local coding LLM

### Database

- SQLite

### Frontend

- Initial development: Streamlit
- Architecture should allow a richer frontend later

### Code Validation

- Python AST
- gcc/g++
- javac

### Security

- Docker sandbox
- Resource limits
- Timeout
- Restricted filesystem
- No network access for generated code

---

## 7. Deployment

### Primary Target

A production-quality application running locally:

```text
localhost
    +
Ollama
    +
FastAPI
    +
Frontend
    +
SQLite
    +
Sandbox
```

The application should continue functioning without internet after installation and model setup.

### Future

An optional public deployment may be created for portfolio/demo purposes.

---

## 8. Development Tool

Primary Vibe-Coding Tool:

**Antigravity**

Antigravity-generated code must follow the project rules in `RULES.md`.

Generated code must be reviewed and tested before being considered complete.

---

## 9. Project Workflow

```text
01 Idea
02 Research
03 User Definition
04 PRD
05 Tech Stack
06 Architecture
07 Design
08 Rules
09 Task Breakdown
10 Setup
11 Development
12 Testing
13 Security Review
14 Code Review
15 Preview Development
16 QA Testing
17 Production Deployment
18 Monitoring
```

---

## 10. Project Documentation

```text
PROJECT_WORKFLOW.md
RULES.md
README.md

docs/
├── 01_idea/
├── 02_research/
├── 03_user_definition/
├── 04_prd/
├── 05_tech_stack/
├── 06_architecture/
├── 07_design/
├── 08_rules/
├── 09_task_breakdown/
├── 10_setup/
├── 11_development/
├── 12_testing/
├── 13_security/
├── 14_code_review/
├── 15_preview/
├── 16_qa/
├── 17_production/
└── 18_monitoring/
```

---

## 11. Development Principle

Bhasha2Code is not intended to be a simple LLM wrapper.

The system combines:

```text
Traditional NLP
+
Machine Learning
+
Local LLM
+
Code Analysis
+
Context Management
+
Safe Execution
+
Study Management
```

---

## 12. Project Goal

The final application should allow a student to naturally communicate with an offline AI coding assistant, receive useful and context-aware programming help, safely work with code, and preserve their learning journey locally.

---

## 13. Current Status

**Phase 0 — Foundation**

Status:

`IN PROGRESS`

Next:

**Phase 1 — Idea & Problem Definition**