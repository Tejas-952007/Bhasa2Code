# Bhasha2Code — Verified Project Facts & Technical Baseline

**Document Type:** Technical Baseline & Fact Verification  
**Project:** Bhasha2Code (Working Title: *Bhasha2Code: An Offline-First Multilingual Natural Language-to-Code Generation, Debugging and Explanation Assistant*)  
**Verification Date:** October 2026  
**Audience:** B.E. Artificial Intelligence & Data Science / Computer Engineering Faculty, Project Guide, Evaluators  

---

## 1. Verified Project Purpose

Bhasha2Code is an offline-first, privacy-preserving AI programming assistant tailored for bilingual engineering students in India. It accepts natural language queries written in English, Hindi, Marathi, Hinglish, and code-mixed Marathi-English, interprets user intent, extracts programming constraints, and leverages a locally hosted quantized Large Language Model (LLM) via Ollama to generate, debug, explain, and review code.

Unlike general-purpose conversational LLM wrappers, Bhasha2Code enforces strict algorithmic guardrails:
1. **Preservation of Standard Syntax:** Programming language keywords (`def`, `for`, `class`, `public static void main`) and identifiers remain in standard English ASCII characters, while conversational explanations and documentation adapt to the user's regional dialect.
2. **Deterministic Code Validation:** Generated code passes Abstract Syntax Tree (AST) validation before presentation or execution.
3. **Isolated Sandboxed Execution:** Untrusted code execution occurs in ephemeral, resource-capped Docker containers completely isolated from the host machine and the internet.
4. **Pedagogical Scaffolding (Study Mode):** Generates step-by-step algorithms, visual flowcharts, line-by-line code breakdowns, time/space complexity analysis, and curriculum-aligned viva questions.

---

## 2. Problem Statement & Motivation

### Problem Statement
> *"To design, implement, and validate an offline, zero-recurring-cost programming assistant that accurately detects linguistic intent from code-mixed Indian vernacular prompts (Marathi, Hindi, Hinglish, Marathi-English), synthesizes syntactically verifiable source code using local open-weights LLMs, and provides sandboxed runtime validation and curriculum-focused pedagogical explanations (Study Mode) on consumer-grade hardware."*

### Motivation & Background
- **Linguistic Cognitive Gap:** In Tier-2 and Tier-3 engineering colleges across Maharashtra and India, students predominantly think and reason algorithmically in their native tongue (Marathi/Hindi). Formulating complex syntax inquiries in formal English introduces significant cognitive friction.
- **Deficiencies of Commercial AI Assistants:**
  - *Cloud Dependency & Recurring Costs:* Services like GitHub Copilot or ChatGPT Plus require steady high-bandwidth internet and paid subscriptions ($20/month), which are prohibitive for many Indian college students.
  - *Data Privacy & Cloud Exposure:* Academic code and proprietary student projects are transmitted to third-party offshore cloud servers.
  - *Lack of Pedagogical Depth:* Commercial assistants prioritize rapid production code over conceptual explanation, promoting passive copying rather than algorithmic learning.
  - *Hallucinations on Code-Mixed Input:* Standard commercial models frequently stumble on transliterated Romanized Marathi/Hindi words (e.g., confusing the Marathi word `yat` ("in this") or homographs like `the` in English vs. `थे` in Hindi).

---

## 3. Verified Project Objectives

1. **Deterministic NLP Processing:** Build an offline 4-stage pipeline (preprocessing, language identification, tone classification, intent classification) with zero cloud API dependencies and sub-10ms CPU latency.
2. **Local Model Orchestration:** Integrate local open-source coding LLMs (`Qwen2.5-Coder:1.5B` / `3B`) using Ollama, executing on consumer-grade CPUs with sub-second time-to-first-token on warm models (~290 ms; ~5.6s cold start).
3. **Automated Static Code Validation:** Implement multi-language static syntax analysis (Python AST, host compiler syntax checking for JS, Java, C, C++, and regex checking for SQL) to filter out malformed code before display.
4. **Secure Containerized Execution:** Construct an ephemeral Docker execution sandbox with strict cgroup resource constraints (memory, CPU, process count) and complete network denial (`--network none`).
5. **Educational Study Mode:** Provide structured educational artifacts including SVG/structured flowchart nodes, step-by-step algorithmic breakdowns, complexity metrics, and automatic viva-voce Q&A generation.
6. **Persistent Local Workspace:** Maintain session history, conversation context, generated code artifacts, personal notes, and debug logs using a local SQLite database.

---

## 4. Actual Verified Technology Stack

| Layer | Component | Verified Implementation |
| :--- | :--- | :--- |
| **Frontend UI** | Framework & Build Tool | **React 18.3.1**, **Vite 5.4.21** |
| | Styling & Icons | Vanilla CSS + Tailwind CSS utilities, Lucide React icons |
| | Code Workspace | Monaco Editor / CodeMirror, Custom syntax highlighter, Diff viewer |
| | Visualization | Custom Interactive SVG / Visual Flowchart Component (`VisualFlowchart.jsx`) |
| | Terminal & Communication | Native WebSocket client (`InteractiveTerminal.jsx`), EventSource / fetch SSE streaming |
| **Backend API** | Web Framework | **FastAPI 0.115.0+**, **ASGI / Uvicorn** |
| | Concurrency & Protocol | Server-Sent Events (SSE) via `StreamingResponse`, WebSockets for interactive stdin |
| | Schema Validation | **Pydantic v2.9+** |
| | Database & ORM | **SQLite 3**, **SQLAlchemy 2.0+** (`bhasha2code.db`) |
| **NLP & ML Tier** | Machine Learning Core | **scikit-learn 1.5+ / 1.9.1**, **NumPy**, **Joblib 1.4+** |
| | Feature Extraction | Character N-grams (`char_wb`, range 3–5), Word N-grams (range 1–2), Sublinear TF |
| | Classifiers | Logistic Regression (`solver='lbfgs'`, `C=3.0`, `class_weight='balanced'`) |
| | Preprocessing & Rules | Unicode NFC normalization (`unicodedata`), Regex tokenization, Lexical dictionary lookups |
| **Local Inference** | LLM Engine | **Ollama Local Daemon** (`http://127.0.0.1:11434`) |
| | Active Default Model | `qwen2.5-coder:1.5b` (Q4_K_M quantized GGUF, ~986 MB footprint) / `qwen2.5-coder:3b` |
| | Inference Parameters | `temperature=0.2`, `num_ctx=8192`, `num_predict=600` (configurable up to 2048 via `.env`) |
| **Validation & Sandbox** | Static Code Validation | Python `ast.parse()`, host compiler checks (`gcc -fsyntax-only`, `javac`, `node --check`), regex for ANSI SQL |
| | Sandbox Isolation | **Docker Engine 24.0+ / 27.0+** (`docker run --network none --cap-drop ALL --read-only`) |
| | Sandbox Images | Alpine/Debian slim images: `python`, `python-ml`, `cpp`, `java`, `javascript` |
| | Resource Limits | 256 MB RAM (768 MB for ML), 0.5 CPU, 64 PIDs, 3.0s timeout (10.0s ML), 64 KB stdout cap |

---

## 5. Verified Implemented Features

### A. Natural Language Processing (NLP) Pipeline
- **Stage 1 — Text Preprocessing (`TextPreprocessor`):**
  - Unicode NFC normalization.
  - Separation of fenced code blocks (```) and raw code lines from natural language text.
  - Extraction of clean text segments for downstream classifiers.
- **Stage 2 — Conversational Language Detection (`LanguageDetector`):**
  - Offline, deterministic classification of 6 language categories: `ENGLISH`, `HINDI`, `MARATHI`, `HINGLISH`, `MARATHI_ENGLISH`, and `HINDI_ENGLISH`.
  - Homograph disambiguation engine addressing Latin-script collisions (e.g., English "the" vs Hindi "थे", "me" vs "मी").
- **Stage 3 — Conversational Tone Classification (`ToneClassifier`):**
  - 6 tone classes: `CASUAL`, `FORMAL`, `SIMPLE`, `TECHNICAL`, `SHORT`, and `DETAILED`.
  - Pre-trained TF-IDF + Logistic Regression model (`models/tone/tone_classifier.joblib`).
- **Stage 4 — Programming Intent Classification (`IntentClassifier`):**
  - 18 intent classes: `GENERATE_CODE`, `DEBUG_CODE`, `EXPLAIN_CODE`, `CONCEPT`, `ALGORITHM`, `CODE_REVIEW`, `OPTIMIZE_CODE`, `CONVERT_CODE`, `ERROR_EXPLANATION`, `TEST_CASE_GENERATION`, `PERFORMANCE_ANALYSIS`, `SECURITY_ANALYSIS`, `APPROACH_SUGGESTION`, `ARCHITECTURE_SUGGESTION`, `BEST_PRACTICE`, `CODE_SUGGESTION`, `FEATURE_SUGGESTION`, and `SEARCH`.
  - Pre-trained TF-IDF + Logistic Regression model (`models/intent/intent_classifier.joblib`).

### B. Prompt Engineering & Context Management
- **Sliding History Window:** Retains past conversational turns, extracted code snippets, and language state across multi-turn sessions.
- **Code Preservation Mandate:** Dynamic system prompt enforcement instructing the LLM to output English ASCII identifiers and syntax while explaining in the user's detected dialect.
- **Dynamic Token Budgeting:** Sets sufficient context and prediction limits (up to 2048 tokens) to prevent abrupt mid-sentence code truncation.

### C. Code Validation & Execution Sandbox
- **Static Syntax Validation Endpoint (`POST /api/v1/code/validate`):**
  - Python AST parsing with line/column diagnostic extraction.
  - Diagnostics for syntax errors, unexpected indentation, unclosed brackets.
- **Docker Isolated Execution (`POST /api/v1/code/run` and WebSocket `/api/v1/code/interactive-run`):**
  - Real container execution with `--network none`, `--cap-drop ALL`, non-root user (`UID 1000`), read-only rootfs, and 256MB memory cap.
  - Interactive WebSocket terminal session supporting interactive stdin (e.g. `input()` in Python or `cin` in C++).
- **Multi-language Execution Plans:**
  - Python (Standard and Python ML with NumPy/Pandas/Scikit-learn/SciPy).
  - C and C++ via GCC/G++.
  - Java via OpenJDK.
  - JavaScript via Node.js.

### D. Study Mode Scaffolding
- Dual-mode switch in UI: **Developer Mode** (compact code focus) vs. **Study Mode** (pedagogical focus).
- Structured output parsing dividing responses into:
  1. *Problem Understanding*
  2. *Step-by-step Algorithm*
  3. *Visual Flowchart* (rendered into structured SVG interactive nodes)
  4. *Complete Source Code Artifact*
  5. *Line-by-line Code Explanation*
  6. *Complexity Analysis (Time & Space)*
  7. *Curriculum Viva-Voce Questions with Answers*

### E. Frontend & Session Management
- Full single-page application with sidebar session navigation.
- Persistent SQLite storage for chats, messages, generated code artifacts, personal study notes, and debug histories.
- Markdown prose rendering with syntax-highlighted code blocks, copy-to-clipboard, and direct run triggers.

---

## 6. Partially Implemented & Boundary Features

1. **Static AST Analyzers for Non-Python Languages:**
   - Python syntax validation uses Python's native `ast.parse()`, providing full Abstract Syntax Tree parsing and accurate line numbers.
   - For C, C++, Java, and JavaScript, validation executes host compilers/interpreters via subprocess (`gcc -fsyntax-only`, `javac`, `node --check`) without execution. For SQL, validation uses regex and lexical balance checkers (`backend/app/validation/validators/sql_validator.py`).
2. **Interactive WebSocket Stdin in Production Builds:**
   - The WebSocket interactive terminal (`/api/v1/code/interactive-run`) is fully implemented in backend and frontend components, but requires a running Docker daemon on the host. When Docker is not running or images are not built, the system gracefully falls back to static validation.
3. **Audio / Speech-to-Text Input:**
   - Planned in documentation and architecture as future work; current verified implementation handles text-based code-mixed input.

---

## 7. Verified System Limitations

1. **Hardware Dependent Inference Speed:** On low-power dual-core CPUs with 8GB RAM, local 3B model inference can take 20–40 seconds per response. The lighter 1.5B model (`qwen2.5-coder:1.5b`) is recommended for live classroom demonstrations.
2. **Language Model Size Trade-off:** Lightweight local models (1.5B parameters) may occasionally produce simplistic code for advanced distributed architectures or complex frameworks.
3. **Devanagari Transliteration Variance:** Extreme slang or uncommon phonetic spellings not covered by the Romanized dictionary may default to standard English or require user rephrasing.
4. **Host Docker Requirement:** Sandbox execution requires the local host to have Docker Engine installed and the user added to the `docker` group.

---

## 8. Verified Test Results

Actual test suite execution performed directly in the project environment:

### Backend Test Suite (Pytest)
- **Command:** `.venv/bin/pytest -q`
- **Total Test Cases:** **567**
- **Passed:** **541 tests** (`100%` pass rate for non-skipped tests)
- **Skipped:** **26 tests** (specifically Docker integration tests where host Docker daemon was not running during unit run)
- **Failed:** **0 tests**
- **Execution Duration:** 22.79 seconds

### Frontend Test Suite (Node Native Runner)
- **Command:** `npm test` (inside `frontend/`)
- **Total Tests:** **20 tests**
- **Passed:** **20 tests** (`100% PASS`)
- **Failed:** **0 tests**
- **Execution Duration:** 365 ms
- **Verified Areas:** Diagnostic parsing, code revision stale-state detection, execution gating, debounce typing behavior, concurrency lock, flowchart node security, Study Mode view models, and SSE message streaming.

### Intent & Tone Classifier Metadata Benchmarks (from `models/*/metadata.json`)
- **Intent Classification (18 classes, 1080 samples total):**
  - Train: 756 samples | Validation: 162 samples | Test: 162 samples
  - Validation Accuracy: **91.36%** | Macro F1: **91.14%**
  - Test Accuracy: **92.59%** | Macro F1: **92.39%**
  - Code-mixed Hinglish Test Accuracy: **100%** (30/30)
  - Code-mixed Marathi-English Test Accuracy: **100%** (37/37)
- **Tone Classification (6 classes, 600 samples total):**
  - Train: 420 samples | Validation: 90 samples | Test: 90 samples
  - Validation Accuracy: **97.78%** | Macro F1: **97.78%**
  - Test Accuracy: **100.00%** (90/90 on held-out test set)

### Verified Latency & Throughput Benchmarks (Host CPU)
- **4-Stage NLP Pipeline:** Mean end-to-end execution latency is **8.12 ms** (measured on 12th Gen Intel Core i7-12650H CPU; individual Intent Classifier: ~4.0 ms, Tone Classifier: ~3.9 ms, Preprocessor: ~0.04 ms, Language Detector: ~0.07 ms).
- **LLM Streaming (Qwen2.5-Coder:1.5B via Ollama):**
  - Warm Time-to-First-Token (TTFT): **289.1 ms** (< 300 ms, sub-second).
  - Cold-Start Initial Model Load: **~5.6 seconds**.
  - Generation Throughput: **27.1 tokens/sec** on CPU.

---

## 9. Details for Student/College Presentation Confirmation

- **Candidate Name:** Tejas Ingle (PRN: `[Student PRN]`)
- **Department:** Computer Engineering / Artificial Intelligence & Data Science
- **College:** Nutan Maharashtra Institute of Engineering & Technology (NMIET), Talegaon Dabhade, Pune (Affiliated to Savitribai Phule Pune University - SPPU)
- **Project Guide:** Prof. Gajanan Godage (Assistant Professor)
- **Academic Year:** 2025–2026
- **Live Demo Configuration:** Ollama running `qwen2.5-coder:1.5b` on `http://127.0.0.1:11434`, backend running on port 8000, Vite frontend on port 5173.
