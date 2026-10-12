# Bhasha2Code: 12-Slide Engineering Mini-Project Presentation Master

> **Format:** Copy-ready slides for Microsoft PowerPoint, Google Slides, Canva, or NotebookLM.  
> **Student:** Tejas Ingle (PRN: `[Student PRN]`)  
> **Project Guide:** Prof. Gajanan Godage  
> **Department:** Department of Computer Engineering / Artificial Intelligence & Data Science  
> **College:** Nutan Maharashtra Institute of Engineering & Technology (NMIET), Pune  
> **Academic Year:** 2025–2026  

---

## SLIDE 1: Title Slide

### Slide Content (Copy-Ready Text)
* **Title:** **Bhasha2Code**
* **Subtitle:** An Offline-First Multilingual Natural Language-to-Code Generation, Debugging, and Explanation Assistant
* **Domain:** Natural Language Processing (NLP) & Edge AI / Educational Technology
* **Candidate:** Tejas Ingle (PRN: `[Student PRN]`)
* **Project Guide:** Prof. Gajanan Godage
* **Institution:** Department of Computer Engineering, NMIET Pune (Affiliated to SPPU)

### Suggested Visual
- Minimalist technical title layout with college logo on the top right, clean gradient banner, and badges: `Offline Edge AI` | `Code-Mixed Indic NLP` | `Educational Sandbox`.

### Presenter Notes (What to Speak Aloud)
> *"Respected guide, head of department, and external examiners, good morning. Today, I am presenting my third-year engineering mini-project titled **Bhasha2Code: An Offline-First Multilingual Natural Language-to-Code Generation, Debugging, and Explanation Assistant** under the guidance of Prof. Gajanan Godage. This project bridges the digital divide between regional language computational thinking and professional programming syntax."*

* **Approximate Duration:** 45 seconds

---

## SLIDE 2: Introduction and Project Overview

### Slide Content (Copy-Ready Text)
* **Vernacular Cognitive Thinking:** Over 70% of engineering students from non-metro colleges conceptualize algorithms in regional languages (Marathi/Hindi).
* **The AI Translation Barrier:** Commercial AI coding assistants assume formal English prompts, creating cognitive friction for bilingual learners.
* **Core Value Proposition:** Bhasha2Code accepts natural code-mixed prompts (e.g., *"Python madhe binary search samjhava"*), analyzes intent in 3 ms, and synthesizes verifiable code.
* **Zero-Cost & Offline Architecture:** Operates completely on local consumer hardware without cloud APIs, monthly subscriptions, or data privacy risks.
* **Dual-Mode Experience:** Features a compact **Developer Mode** for rapid code synthesis and an academic **Study Mode** for curriculum comprehension.

### Suggested Visual
- A side-by-side contrast graphic: Left side shows a student struggling to write complex English prompts; Right side shows Bhasha2Code accepting natural Marathi-English text and producing code + flowchart.

### Presenter Notes (What to Speak Aloud)
> *"In our engineering colleges across Maharashtra, students intuitively think in Marathi or Hindi when learning programming logic. When forced to translate their thoughts into formal English prompts for tools like ChatGPT, it creates cognitive overhead. Bhasha2Code solves this by allowing students to ask coding queries in their natural code-mixed dialect, while ensuring the generated code strictly follows standard English syntax."*

* **Approximate Duration:** 60 seconds

---

## SLIDE 3: Problem Statement and Motivation

### Slide Content (Copy-Ready Text)
* **Problem Statement:** To design an offline, zero-recurring-cost programming assistant that accurately detects intent from code-mixed Indian vernacular prompts, generates syntactically valid code using local LLMs, and provides sandboxed execution with academic scaffolding.
* **Prohibitive Recurring Costs:** Commercial tools (ChatGPT Plus, GitHub Copilot) cost $10–$20/month (₹850–₹1,700/month), which is financially inaccessible for many students.
* **Cloud & Internet Vulnerability:** Mandatory cloud access renders commercial tools unusable in air-gapped or low-connectivity college laboratories.
* **Hallucination of Code Keywords:** Naive prompting of smaller open-source models often causes non-English variable or keyword hallucinations.
* **Lack of Pedagogical Depth:** Commercial tools dump raw code without providing algorithmic steps, visual flowcharts, or viva examination preparation.

### Suggested Visual
- A quadrant diagram highlighting the 4 major challenges: 1. Linguistic Friction, 2. Financial Inaccessibility, 3. Cloud Dependency, 4. Lack of Academic Scaffolding.

### Presenter Notes (What to Speak Aloud)
> *"The problem we address is twofold: linguistic accessibility and educational relevance. Existing commercial tools require paid dollar subscriptions, require continuous internet connectivity, and merely output raw code blocks. They do not teach the student how the algorithm works, nor do they help them prepare for university lab vivas. Bhasha2Code was built to address these specific gaps."*

* **Approximate Duration:** 60 seconds

---

## SLIDE 4: Aim and Objectives

### Slide Content (Copy-Ready Text)
* **Project Aim:** Develop a self-contained, privacy-first bilingual coding assistant combining offline NLP, quantized local LLMs, AST validation, and containerized sandboxes.
* **Objective 1:** Build a deterministic 4-stage NLP pipeline (preprocessing, language detection, tone classification, intent classification) with sub-10ms CPU latency.
* **Objective 2:** Deploy a 4-bit quantized open-source coding LLM (`Qwen2.5-Coder:1.5B/3B`) locally via Ollama with zero API token billing.
* **Objective 3 (Code Preservation Mandate):** Enforce strict prompt policies ensuring programming keywords remain in English ASCII while explanations mirror the user's regional dialect.
* **Objective 4:** Implement multi-language static Abstract Syntax Tree (AST) validation to catch syntax errors before code display.
* **Objective 5:** Engineer an ephemeral Docker execution sandbox with strict cgroup isolation (256MB RAM, 0.5 CPU, `--network none`).
* **Objective 6:** Build educational **Study Mode** scaffolding generating visual flowcharts, step-by-step algorithms, and viva Q&A pairs.

### Suggested Visual
- A clean sequential checklist of 6 milestone icons (NLP Pipeline → Local LLM → Code Preservation → AST Check → Docker Sandbox → Study Mode).

### Presenter Notes (What to Speak Aloud)
> *"Our project objectives are clear and measurable: First, build an offline NLP pipeline for intent classification. Second, host an open-weights coding LLM locally using Ollama. Third, enforce our Code Preservation Mandate. Fourth, validate syntax with Abstract Syntax Trees. Fifth, execute code safely inside Docker containers. And sixth, provide our curriculum-aligned Study Mode."*

* **Approximate Duration:** 60 seconds

---

## SLIDE 5: Existing System and Its Limitations

### Slide Content (Copy-Ready Text)
* **Commercial AI Assistants (ChatGPT, GitHub Copilot):**
  - High recurring subscription expenses ($20/month per user).
  - Strictly cloud-dependent; no offline functionality for rural/college labs.
  - Frequent phonetic misunderstanding of Romanized Marathi and Hindi.
* **Standard Open-Source LLMs (Llama 3, Mistral 7B):**
  - High computational barrier (require 16GB+ GPU VRAM for unquantized inference).
  - Lack built-in compiler validation or sandboxed code execution safety.
  - Fail to provide structured academic breakdown (flowcharts, viva questions).
* **Research Gap Identified:** Absence of a lightweight, privacy-preserving, localized coding mentor designed specifically for bilingual engineering students on CPU hardware.

### Suggested Visual
- A comparative feature table:

| Feature | ChatGPT / Copilot | Raw Local LLM | **Bhasha2Code** |
| :--- | :--- | :--- | :--- |
| **Code-Mixed Dialects** | Weak phonetic recognition | Hallucinates keywords | **Native Lexical & Rule Pipeline** |
| **Offline Privacy** | Cloud-dependent | GPU required | **100% Offline (Runs on CPU)** |
| **Recurring Cost** | $20 / month | Heavy hardware cost | **₹0 / Open Source** |
| **Syntax Validation** | None | None | **Pre-Render AST Syntax Parsing** |
| **Execution Safety** | Cloud E2B | Host OS risk | **Ephemeral Docker Sandbox** |
| **Pedagogical Depth** | Code only | Flat text | **Study Mode (Flowchart + Viva)** |

### Presenter Notes (What to Speak Aloud)
> *"When we compare Bhasha2Code against existing market tools, the differences are significant. Commercial tools require high recurring fees, require constant internet connectivity, and execute code on remote servers. Standard open-source models require expensive GPUs. Bhasha2Code runs on standard laptop CPUs, validates code before rendering, runs it inside a locked Docker container, and costs absolutely nothing."*

* **Approximate Duration:** 60 seconds

---

## SLIDE 6: Proposed System and Key Features

### Slide Content (Copy-Ready Text)
* **Two-Tier AI Architecture:** Decouples sub-10ms classification (Scikit-Learn NLP) from generative code synthesis (Qwen2.5-Coder LLM).
* **Code Preservation Mandate:** Explanations and comments follow the student's regional dialect, while programming tokens (`def`, `class`, `for`) remain strictly in English ASCII.
* **Curriculum-Focused Study Mode:**
  - Automated step-by-step algorithmic breakdown.
  - Interactive SVG visual flowchart rendering.
  - Line-by-line explanation of code logic.
  - Automatic generation of 3–5 practical viva-voce questions and answers.
* **Abstract Syntax Tree (AST) Validation:** Static pre-render validation gates code execution and badges code status (`VALID`, `SYNTAX_ERROR`).
* **Isolated Container Sandbox:** Ephemeral Docker runtime with zero network access and strict resource caps prevents any host security damage.

### Suggested Visual
- A high-level infographic showcasing the student typing a prompt, the system splitting it into NLP routing vs LLM generation, and delivering code + flowchart + viva cards.

### Presenter Notes (What to Speak Aloud)
> *"Our proposed solution is built on a clean two-tier AI architecture. Rather than relying entirely on a slow generative model for classification, our lightweight Scikit-Learn NLP pipeline classifies language, tone, and intent in approximately 8 milliseconds. This directly steers the prompt sent to our local Qwen2.5-Coder model. Most importantly, our Study Mode deconstructs the generated solution into algorithmic steps, visual flowcharts, and viva questions."*

* **Approximate Duration:** 60 seconds

---

## SLIDE 7: System Architecture

### Slide Content (Copy-Ready Text)
* **Tier 1 (Client UI):** React 18, Vite, Monaco Editor, Lucide React, and Server-Sent Events (SSE) streaming listener.
* **Tier 2 (Gateway & Context):** FastAPI asynchronous ASGI service with SQLite database managed via SQLAlchemy.
* **Tier 3 (Offline NLP Pipeline):** 4-stage sequential pipeline (Text Preprocessing → Language Detection → Tone Classification → Intent Classification).
* **Tier 4 (Local Inference Engine):** Ollama daemon hosting 4-bit quantized `qwen2.5-coder:1.5b` (Q4_K_M GGUF).
* **Tier 5 (Verification & Execution):** Python AST parser and ephemeral Docker sandbox with strict cgroup resource constraints.

### Simplified Architecture Diagram (For PowerPoint Reproduction)

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PRESENTATION TIER (React 18 + Vite)                  │
│       [Chat Stream UI]   [Monaco Code Workspace]   [Study Mode View]   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / SSE Token Stream
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               BACKEND APPLICATION TIER (FastAPI & SQLite)              │
│  ┌──────────────────────┐  ┌────────────────────┐  ┌────────────────┐  │
│  │ 4-Stage NLP Pipeline │  │  Prompt Builder    │  │ Context Memory │  │
│  │ (Lang, Tone, Intent) │  │  & Safety Policies │  │ (Sliding Hist) │  │
│  └──────────────────────┘  └────────────────────┘  └────────────────┘  │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │ Local HTTP (Port 11434)         │ Docker CLI / Socket
                   ▼                                 ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│       LOCAL INFERENCE TIER           │  │   ISOLATED DOCKER SANDBOX    │
│            (Ollama Daemon)           │  │   (--network none, 256MB)    │
│   Active Model: Qwen2.5-Coder:1.5B   │  │   Python, C/C++, Java, JS    │
└──────────────────────────────────────┘  └──────────────────────────────┘
```

### Presenter Notes (What to Speak Aloud)
> *"This slide presents our system architecture. The React frontend interacts with the FastAPI backend over HTTP and Server-Sent Events. When a query arrives, our deterministic NLP pipeline cleans the text and classifies language, tone, and intent. The Prompt Builder incorporates conversation history from SQLite and enforces the Code Preservation Mandate before calling Ollama. Tokens are streamed back in real-time, validated against Abstract Syntax Trees, and rendered in the workspace."*

* **Approximate Duration:** 90 seconds

---

## SLIDE 8: Methodology and Working Flow

### Slide Content (Copy-Ready Text)
* **Step 1 — Preprocessing & Code Segregation:** Normalizes input via Unicode NFC; strips attached code blocks to isolate conversational intent.
* **Step 2 — Deterministic Language Detection:** Counts Devanagari script ratios and evaluates dictionary lookups for Hindi/Marathi with homograph disambiguation.
* **Step 3 — TF-IDF & Logistic Regression:**
  - Extracts word n-grams (1, 2) and character n-grams (3, 5).
  - Computes class probabilities via Softmax Logistic Regression across 18 intent classes.
* **Step 4 — Prompt Synthesis & LLM Streaming:** Injects detected metadata, conversation history, and Study Mode templates into the local LLM.
* **Step 5 — Static AST Validation:** Parses generated Python code using `ast.parse()`; extracts line-numbered syntax diagnostics.
* **Step 6 — Isolated Docker Sandbox Execution:** Executes validated code inside a non-root, network-disabled container with a 3.0-second timeout.

### Suggested Visual
- A horizontal step-by-step workflow pipeline with numbering from 1 to 6.

### Presenter Notes (What to Speak Aloud)
> *"Here is the exact lifecycle of a user request. First, the text is normalized and separated from raw code. Second, our lexical rule engine identifies the dialect and resolves homographs. Third, our TF-IDF Logistic Regression model predicts the intent. Fourth, the Prompt Builder synthesizes instructions and queries Ollama. Fifth, as tokens finish streaming, Python's AST module validates the syntax. Finally, if the student clicks Run, the code executes inside an isolated Docker container."*

* **Approximate Duration:** 75 seconds

---

## SLIDE 9: Technology Stack and Major Modules

### Slide Content (Copy-Ready Text)
* **Frontend Web Stack:**
  - React 18.3.1, Vite 5.4.2, Tailwind CSS, Monaco Editor, Lucide Icons.
  - Native Server-Sent Events (SSE) stream consumer and WebSocket terminal client.
* **Backend Framework:**
  - Python 3.11, FastAPI (Asynchronous ASGI gateway), Pydantic v2 schemas.
  - SQLAlchemy 2.0 ORM with local SQLite 3 database (`bhasha2code.db`).
* **Machine Learning & NLP:**
  - scikit-learn 1.5+, NumPy, Joblib model serialization.
  - TF-IDF vectorizer (Sublinear TF, character n-grams range 3–5).
* **Local Inference & Sandboxing:**
  - Ollama Daemon (`http://127.0.0.1:11434`), Model: `qwen2.5-coder:1.5b` (Q4_K_M GGUF).
  - Docker Engine 24.0+ with Alpine/Debian slim sandbox execution images.

### Suggested Visual
- Tech stack logos / badges grouped by layer: React, Vite, FastAPI, Python, Scikit-learn, SQLite, Ollama, Docker.

### Presenter Notes (What to Speak Aloud)
> *"Our technology stack is 100% open-source and local. For the frontend, we use React 18 and Vite for fast, responsive UI updates. For the backend, we use FastAPI with asynchronous SSE streaming. For NLP, we use Scikit-Learn for sub-10ms classifications. Local model execution is handled by Ollama running a 4-bit quantized Qwen2.5-Coder model, and execution isolation is achieved using Docker Engine."*

* **Approximate Duration:** 60 seconds

---

## SLIDE 10: Implementation, Testing and Verified Results

### Slide Content (Copy-Ready Text)
* **Intent Classification Accuracy:**
  - Achieved **92.59% accuracy** and **92.39% Macro F1-score** across 18 intent classes on held-out test data.
  - **100% accuracy** on code-mixed Marathi-English (37/37) and Hinglish (30/30) test subsets.
* **Tone Classification Accuracy:**
  - Achieved **97.78% validation accuracy** and **100.00% test accuracy** across 6 tone classes.
* **Automated Test Suite Pass Rates:**
  - **Backend (Pytest):** **541 tests passed**, 26 skipped, 0 failed (`100% pass rate`).
  - **Frontend (Node Test Runner):** **20 tests passed**, 0 failed (`100% pass rate`).
* **Local Inference Throughput (Consumer CPU):**
  - Warm Time-to-First-Token (TTFT): **~290 – 450 ms**; Cold start: **~5.6 s**; Throughput: **22 – 27 tokens/second**.
  - Total response latency: **8–12 seconds** on consumer CPU with zero GPU requirement.

### Suggested Visual
- Side-by-side metric cards:
  - Card 1: `92.59% Intent Accuracy`
  - Card 2: `561 Total Automated Tests Passing`
  - Card 3: `22–27 tokens/sec on CPU`
  - Card 4: `3.0s Sandbox Timeout`

### Presenter Notes (What to Speak Aloud)
> *"We thoroughly benchmarked our implementation. On our held-out test dataset, our 18-class intent classifier achieved 92.59% accuracy, scoring 100% on Romanized Marathi-English queries. Our automated test suite includes 541 passing backend unit tests and 20 passing frontend integration tests with zero failures. On a standard laptop without any GPU, inference begins in under 500 milliseconds on a warm model and generates at 22 to 27 tokens per second."*

* **Approximate Duration:** 75 seconds

---

## SLIDE 11: Limitations and Future Scope

### Slide Content (Copy-Ready Text)
* **Verified System Limitations:**
  - CPU inference latency on older dual-core processors can take 20–30 seconds.
  - Highly non-standard phonetic spellings or slang outside the lexicon may default to standard English.
  - Static AST parsing for C/C++ and Java currently relies on lexical rules until compiled in Docker.
  - Sandboxed code execution requires the local machine to have Docker Engine installed.
* **Future Scope & Enhancements:**
  - **Multimodal Indic Voice Input:** Integrating offline Indic Whisper / AI4Bharat Bhashini models for direct spoken queries.
  - **Expansion to More Languages:** Broadening lexical resources to include Gujarati, Telugu, Kannada, and Tamil.
  - **Syllabus-Aligned Fine-Tuning:** Fine-tuning compact models on Savitribai Phule Pune University (SPPU) lab assignments and viva question banks.
  - **Visual Step-Through Debugger:** Implementing animated variable tracking and memory state visualization for data structures.

### Suggested Visual
- A two-column slide: Left column labeled "Current Boundaries & Constraints", Right column labeled "Engineering Roadmap & Enhancements".

### Presenter Notes (What to Speak Aloud)
> *"Every engineering project has constraints and a growth path. Currently, local LLM generation speed depends on CPU clock frequency, and sandboxing requires Docker on the host. In our future scope, we plan to integrate Indic Whisper for voice input, extend support to Gujarati, Kannada, and Telugu, and fine-tune our models on SPPU university lab manuals for automated lab manual generation."*

* **Approximate Duration:** 60 seconds

---

## SLIDE 12: Conclusion and Q&A

### Slide Content (Copy-Ready Text)
* **Conclusion:**
  - Successfully designed, implemented, and verified **Bhasha2Code** as a self-contained, offline multilingual programming assistant.
  - Overcame major barriers of commercial coding assistants: eliminated recurring costs, guaranteed complete data privacy, and solved code-mixed language comprehension.
  - Validated educational efficacy through dual-mode operation: Developer Mode for rapid coding and Study Mode for visual and algorithmic comprehension.
* **Demonstrated Engineering Feasibility:** Proved that lightweight NLP pipelines coupled with quantized local LLMs can deliver robust educational AI on everyday consumer hardware.
* **Acknowledgements:** Sincere gratitude to project guide Prof. Gajanan Godage and the Department of Computer Engineering.
* **Open for Questions & Defense:** Thank you! We welcome questions from the panel.

### Suggested Visual
- Closing slide with contact info, GitHub repo reference placeholder, and prominent "Questions & Answers" prompt.

### Presenter Notes (What to Speak Aloud)
> *"In conclusion, Bhasha2Code proves that cutting-edge AI assistance does not have to be expensive, cloud-dependent, or exclusively English-centric. By combining offline NLP classification, local quantized models, AST validation, Docker sandboxing, and Study Mode, we have created a truly accessible coding mentor for engineering students. Thank you, and I look forward to your questions."*

* **Approximate Duration:** 45 seconds

---

## Presentation Delivery Summary

| Slide # | Slide Title | Speaking Time |
| :---: | :--- | :---: |
| 1 | Title Slide | 0:45 |
| 2 | Introduction and Project Overview | 1:00 |
| 3 | Problem Statement and Motivation | 1:00 |
| 4 | Aim and Objectives | 1:00 |
| 5 | Existing System and Its Limitations | 1:00 |
| 6 | Proposed System and Key Features | 1:00 |
| 7 | System Architecture | 1:30 |
| 8 | Methodology and Working Flow | 1:15 |
| 9 | Technology Stack and Major Modules | 1:00 |
| 10 | Implementation, Testing and Verified Results | 1:15 |
| 11 | Limitations and Future Scope | 1:00 |
| 12 | Conclusion and Q&A | 0:45 |
| **Total** | **Full Project Defense** | **~12 Minutes** |
