# Bhasha2Code — Concept Mastery & Technical Guide

**Audience:** Third-Year B.E. Engineering Students, Viva Evaluators, and Technical Mentors  
**Style:** Clear, Student-Friendly English with Marathi-English Explanations for Complex Concepts  
**Goal:** Build deep intuition about the architecture, algorithms, and practical code so you can confidently answer any question in your project viva.

---

## Quick Navigation: The 15 Core Project Questions

1. [What Problem Does Bhasha2Code Solve?](#1-what-problem-does-bhasha2code-solve)
2. [Why Is This Project Useful? (The "So What?" Question)](#2-why-is-this-project-useful-the-so-what-question)
3. [What Is Natural Language Processing (NLP)?](#3-what-is-natural-language-processing-nlp)
4. [What Is Intent Detection?](#4-what-is-intent-detection)
5. [What Is Tone Classification?](#5-what-is-tone-classification)
6. [What Is Language Detection?](#6-what-is-language-detection)
7. [How Do TF-IDF and Logistic Regression Work in This Project?](#7-how-do-tf-idf-and-logistic-regression-work-in-this-project)
8. [What Is a Large Language Model (LLM) and What Role Does Ollama Play?](#8-what-is-a-large-language-model-llm-and-what-role-does-ollama-play)
9. [What Is Prompt Construction and Why Is It Necessary?](#9-what-is-prompt-construction-and-why-is-it-necessary)
10. [How Does Code Validation Differ From Code Execution?](#10-how-does-code-validation-differ-from-code-execution)
11. [Why Is Docker Used as an Execution Sandbox?](#11-why-is-docker-used-as-an-execution-sandbox)
12. [What Roles Do React, FastAPI, SQLite, SQLAlchemy, and SSE Play?](#12-what-roles-do-react-fastapi-sqlite-sqlalchemy-and-sse-play)
13. [How Does Study Mode Work in Bhasha2Code?](#13-how-does-study-mode-work-in-bhasha2code)
14. [How Are Incomplete Outputs and Runtime Errors Handled?](#14-how-are-incomplete-outputs-and-runtime-errors-handled)
15. [What Are the System's Limitations and Future Scope?](#15-what-are-the-systems-limitations-and-future-scope)

---

## Fundamental Architecture Rule: Classifiers vs. The LLM

> **Crucial Distinction for Faculty Viva:**  
> **Never say:** *"The LLM is a TF-IDF classifier."* That is technically incorrect.  
> **Always say:** *"Bhasha2Code has two distinct AI tiers: First, a lightweight, deterministic **internal NLP pipeline** (using TF-IDF and Logistic Regression) runs locally in approximately 8 milliseconds on CPU (with individual classifier models executing in 1.2 to 4.0 ms) to detect language, intent, and tone. Second, a **local generative coding LLM** (Qwen2.5-Coder running on Ollama) takes structured prompts to write and explain the code."*

---

### 1. What Problem Does Bhasha2Code Solve?

#### Definition
Bhasha2Code is an offline programming and educational assistant that bridges the linguistic divide between Indian vernacular computational thinking and formal English programming syntax.

#### Why It Is Needed
In Maharashtra and across India, engineering students conceptualize algorithm logic in Marathi or Hindi. When forced to write formal English prompts into tools like ChatGPT or Copilot (e.g., *"Write an algorithm to find the maximum element using divide and conquer"*), they face linguistic friction. If they type naturally in colloquial Hinglish or Marathi-English (*"bhai python madhe array madhla mottha number kasa kadhaycha?"*), commercial tools either fail to catch the nuance, hallucinate non-English variable names, or require expensive internet-connected cloud APIs.

#### How It Works in Bhasha2Code
The user can type in Romanized Marathi, Hindi, English, or Devanagari. Bhasha2Code understands what the user wants, preserves standard English programming syntax for keywords (`def`, `for`, `int`), explains the concept in the user's dialect, validates the code syntax using Abstract Syntax Trees, and runs it safely inside a local container.

#### Simple Example
- **User Input:** *"bhai python madhe palindrome check karayla code de"*
- **System Recognition:** Language = `MARATHI_ENGLISH`, Intent = `GENERATE_CODE`, Target Language = `Python`.
- **System Output:** Clean Python code with English function names (`is_palindrome(text)`), accompanied by a friendly explanation in Marathi-English.

#### Marathi-English Explanation (मराठीत सोप्या भाषेत)
> *आपल्या इंजिनिअरिंगच्या मुलांना विचार करताना डोक्यात मराठी किंवा हिंदीत विचार येतो: "ह्यात लूप कसा लावायचा?". पण ChatGPT ला विचारायला त्यांना कठीण इंग्रजी बनवावं लागतं. Bhasha2Code काय करतो? विद्यार्थ्याने आपल्या बोलीभाषेत विचारलं तरी ते समजून घेतो, योग्य कोड देतो, आणि तो समजावून सांगतो.*

#### What to Speak to Your Professor
> *"Sir, Bhasha2Code eliminates the cognitive friction faced by bilingual students who think in Marathi or Hindi but must write software in English syntax. It provides an offline, zero-cost, localized coding mentor."*

---

### 2. Why Is This Project Useful? (The "So What?" Question)

#### Definition
The practical utility, societal relevance, and engineering merit of the system.

#### Why It Is Needed
College faculty frequently ask: *"Why shouldn't I just use ChatGPT?"* Bhasha2Code provides four key advantages:
1. **Zero Recurring Cost:** ChatGPT Plus ($20/month) is unaffordable for typical college students. Bhasha2Code costs ₹0.
2. **100% Offline & Private:** Operates without internet access inside college labs; student code never leaves the laptop.
3. **Pedagogical Scaffolding:** ChatGPT gives a raw wall of code. Bhasha2Code has **Study Mode**, which generates algorithms, visual flowcharts, and viva questions.
4. **Safety & Execution:** Directly checks code syntax and executes it safely in a sandbox on the student's machine.

#### How It Works in Bhasha2Code
All services (FastAPI, SQLite, Scikit-learn models, Ollama, Docker) run locally on `localhost`. An air-gapped laptop with no Wi-Fi can run the complete pipeline.

#### Simple Example
A student sitting in a college computer lab with no internet connectivity opens `http://localhost:5173`, types their lab question, receives valid code with an algorithm flowchart, and runs it immediately.

#### What to Speak to Your Professor
> *"Sir, commercial LLMs are cloud-dependent, costly, and prioritize developer productivity over student learning. Bhasha2Code is completely offline, cost-free, and designed specifically for pedagogy through our Study Mode and AST validation."*

---

### 3. What Is Natural Language Processing (NLP)?

#### Definition
Natural Language Processing is a subfield of Artificial Intelligence and Computational Linguistics that enables computers to parse, interpret, understand, and generate human language.

#### Why It Is Needed
Computers understand structured syntax (e.g., Python code or JSON), not messy conversational human sentences with typos, transliterations, and grammatical variations. NLP converts raw text into structured features that algorithms can process.

#### How It Works in Bhasha2Code
Our pipeline does not pass raw user text directly to the model. It first runs:
1. **Unicode NFC Normalization:** Standardizes combined Devanagari characters.
2. **Code/Text Separation:** Pulls apart code blocks from natural language questions.
3. **Tokenization:** Breaks sentences into word and character n-grams.
4. **Classification:** Feeds tokens to trained models to label language, tone, and intent.

#### Simple Example
Raw string: `"bhai    Python madhe\n\nfactorial banav ```print(5)```"`  
Preprocessed output: Isolated text segment = `"bhai Python madhe factorial banav"`, attached code = `"print(5)"`.

#### Marathi-English Explanation (मराठीत)
> *NLP म्हणजे कॉम्प्युटरला माणसाची भाषा समजायला शिकवणं. युझर जेव्हा उलट-सुलट स्पेसिंग किंवा कोड मिक्स करून टाईप करतो, तेव्हा त्याला नीट क्लीन करून कॉम्प्युटरला समजेल अशा फॉरमॅटमध्ये आणण्याचं काम NLP करतं.*

#### What to Speak to Your Professor
> *"Sir, we use NLP as an intelligent preprocessing and routing layer. It standardizes noisy, transliterated inputs and extracts explicit engineering parameters before any LLM inference occurs."*

---

### 4. What Is Intent Detection?

#### Definition
Intent detection is a multi-class text classification task that determines the user's primary goal or task from their input sentence.

#### Why It Is Needed
If a student pastes a broken Python function, did they want the system to:
- Generate new code from scratch (`GENERATE_CODE`)?
- Find the bug and fix it (`DEBUG_CODE`)?
- Explain how it works line by line (`EXPLAIN_CODE`)?
- Review its security and efficiency (`CODE_REVIEW`)?
Without intent detection, the AI must guess, often leading to irrelevant responses.

#### How It Works in Bhasha2Code
We built an 18-class intent classifier (`IntentClassifier`) in `backend/app/nlp/intent_classification/`. It uses character and word n-gram TF-IDF vectors followed by Logistic Regression, achieving **92.59% accuracy** on the held-out test dataset.

The 18 intents include: `GENERATE_CODE`, `DEBUG_CODE`, `EXPLAIN_CODE`, `ALGORITHM`, `CONCEPT`, `CODE_REVIEW`, `OPTIMIZE_CODE`, `CONVERT_CODE`, `TEST_CASE_GENERATION`, `ERROR_EXPLANATION`, etc.

#### Simple Example
- Query: *"ह्या कोड मध्ये काय चूक आहे?"* or *"yat error ka yetoy?"*
- Detected Intent: `DEBUG_CODE` (Confidence: 0.94).
- System Action: Instructs prompt builder to activate debugging instructions and generate a patch diff.

#### What to Speak to Your Professor
> *"Sir, our intent classifier uses a balanced Logistic Regression model trained on 18 programming intents. It achieves 92.59% test accuracy and informs the prompt builder exactly what task to instruct the LLM to perform."*

---

### 5. What Is Tone Classification?

#### Definition
Tone classification determines the conversational style and desired depth of response indicated by the user's prompt phrasing.

#### Why It Is Needed
Different students need different explanation styles:
- A student revising 5 minutes before lab viva wants a concise summary (`SHORT` or `SIMPLE`).
- A student studying a concept for the first time wants an in-depth breakdown (`DETAILED` or `TECHNICAL`).
- A quick interactive query uses informal language (`CASUAL`).

#### How It Works in Bhasha2Code
We trained a 6-class tone classifier (`ToneClassifier`) on 600 annotated samples. Classes:
`CASUAL`, `FORMAL`, `SIMPLE`, `TECHNICAL`, `SHORT`, and `DETAILED`.  
It uses sublinear TF-IDF features with Logistic Regression, reaching **97.78% validation accuracy** and **100% on the test set**.

#### Simple Example
- Query: *"ekdum short madhe sang, time complexity kiti ahe"* → Detected Tone: `SHORT`.  
  Response: A concise, 2-bullet summary.
- Query: *"Please provide an in-depth technical analysis of memory allocation in C"* → Detected Tone: `TECHNICAL`.  
  Response: Low-level stack vs heap breakdown.

#### What to Speak to Your Professor
> *"Sir, tone classification allows our prompt builder to modulate response verbosity and technical depth dynamically, matching the student's learning preference."*

---

### 6. What Is Language Detection?

#### Definition
Language detection determines the linguistic medium and dialect mixture of the input query.

#### Why It Is Needed
Students frequently code-mix. For example:
- Romanized Marathi: *"yat bubble sort cha code dakhva"*
- Hinglish: *"isme loop kaise chalega"*
- Pure English: *"write binary search in python"*
- Devanagari Marathi: *"पायथन मध्ये फॅक्टोरिअल कसा काढायचा?"*

Standard off-the-shelf language detectors (like Google Compact Language Detector or langdetect) fail completely on Romanized Marathi because they mistake phonetic Marathi words for English or Portuguese.

#### How It Works in Bhasha2Code
We built a deterministic, lexical-rule language detector (`LanguageDetector`) in `backend/app/nlp/language_detection/`:
1. Checks Devanagari character frequency.
2. Checks exclusive Marathi characters (e.g., `'ळ'`).
3. Uses offline dictionaries of unambiguous Marathi roots (`madhe`, `kasa`, `kadhaycha`, `banav`) and Hindi roots (`kaise`, `karna`, `chahiye`).
4. Implements **Homograph Disambiguation** for overlapping words (e.g., distinguishing English *"the"* from Hindi *"the"* / थे, or English *"me"* from Marathi *"मी"*).
5. Categorizes input into: `ENGLISH`, `HINDI`, `MARATHI`, `HINGLISH`, `MARATHI_ENGLISH`, or `HINDI_ENGLISH`.

#### Simple Example
- Input: *"python madhe stack implement kara"*
- Analysis: `python`, `stack`, `implement` = English technical keywords. `madhe`, `kara` = unambiguous Marathi grammatical particles.
- Detected Language: `MARATHI_ENGLISH` (Marathi-English code-mixed).

#### Marathi-English Explanation (मराठीत)
> *साधे लँग्वेज डिटेक्टर्स रोमन लिपीत लिहिलेली मराठी ओळखू शकत नाहीत. 'Madhe' किंवा 'kara' बघितल्यावर ते कन्फ्युज होतात. आम्ही एक खास लेक्सिकल डिक्शनरी आणि होमोग्राफ रूल्स बनवले आहेत, जे रोमन मराठी आणि हिंग्लिश अचूक ओळखतात.*

#### What to Speak to Your Professor
> *"Sir, standard libraries fail on Romanized Indic text. Our LanguageDetector uses an offline rule-and-lexicon engine with homograph resolution to reliably classify 6 languages, specifically targeting code-mixed Marathi-English."*

---

### 7. How Do TF-IDF and Logistic Regression Work in This Project?

#### Definition
- **TF-IDF (Term Frequency – Inverse Document Frequency):** A mathematical feature extraction technique that converts text strings into numerical vectors based on word importance.
- **Logistic Regression:** A supervised linear classification algorithm that maps feature vectors to class probabilities using the softmax / logistic function.

#### Why They Are Needed
Deep learning models (like BERT or RoBERTa) have large parameter footprints (500MB+) and require 50–150ms of CPU compute time. TF-IDF + Logistic Regression is extremely lightweight (~5MB), runs in under **3 milliseconds** on a CPU, and requires zero GPU resources.

#### How It Works in This Project
1. **Feature Extraction (TF-IDF):**
   - Word n-grams: Range (1, 2) — captures single words and two-word phrases (e.g., *"code de"*, *"bug fix"*).
   - Character n-grams: Range (3, 5) with `char_wb` (character n-grams inside word boundaries) — captures Indic root inflections (e.g., `kar-to`, `kar-a`, `kar-ayla`).
   - Sublinear TF: Replaces raw term count $tf$ with $1 + \log(tf)$ to prevent frequent words from dominating the vector.
2. **Classification (Logistic Regression):**
   - Calculates dot product of weight vectors $w$ and TF-IDF features $x$:
     $$z_k = w_k^T \cdot x + b_k$$
   - Applies Softmax function to generate probability distribution across classes:
     $$P(y = k \mid x) = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}$$
   - Hyperparameters: Regularization parameter $C = 3.0$, solver = `lbfgs`, class weighting = `balanced` (to handle uneven dataset samples).

#### Simple Example
If the input contains the bigram `"bug fix"`, the TF-IDF weight for that phrase is high. The trained weight matrix for `DEBUG_CODE` has a strong positive weight for `"bug fix"`, producing a high probability score for debugging.

#### What to Speak to Your Professor
> *"Sir, we chose TF-IDF with character and word n-grams coupled with L2-regularized Logistic Regression because it executes in under 3 milliseconds on standard CPUs, requires no GPU VRAM, and yields 92.59% accuracy across 18 intent classes."*

---

### 8. What Is a Large Language Model (LLM) and What Role Does Ollama Play?

#### Definition
- **Large Language Model (LLM):** A deep neural network (transformer architecture) trained on vast volumes of code and natural language text, capable of understanding prompts and generating coherent text and code.
- **Ollama:** An open-source, local inference engine that runs quantized LLMs directly on local hardware via optimized C++ backends (llama.cpp) without requiring cloud servers.

#### Why It Is Needed
TF-IDF and Logistic Regression can classify *what* the user wants (e.g., `GENERATE_CODE`), but they cannot *generate* a 50-line working QuickSort algorithm. Generating clean code and human-like explanations requires a generative LLM. Ollama allows us to run this LLM offline on consumer laptops.

#### How It Works in Bhasha2Code
- **Model Selected:** `Qwen2.5-Coder:1.5B` (or `3B`), developed by Alibaba Cloud, specialized in code generation.
- **Quantization:** 4-bit quantized (Q4_K_M GGUF format), compressing the model to under **1.0 GB RAM**.
- **Communication:** FastAPI sends an HTTP POST request to Ollama's local endpoint (`http://127.0.0.1:11434/api/generate`) and streams back tokens in real-time.
- **Parameters:** `temperature=0.2` (low temperature ensures deterministic, correct syntax with minimal hallucination), `num_ctx=8192` (large context window), `num_predict=600` (token cap preventing runaway generation, configurable via `.env`).

#### Simple Example
FastAPI sends: *"Generate a Python function to check prime numbers"*.  
Ollama streams tokens: `def`, ` `, `is_prime`, `(`, `n`, `):` directly to the server.

#### Marathi-English Explanation (मराठीत)
> *क्लासिफायर फक्त सांगतो की युझरला काय हवंय (उदा. 'कोड जनरेट कर'). पण प्रत्यक्षात ५० ओळींचा कोड लिहिण्याचं काम **Qwen2.5-Coder** नावाचा लोकल LLM करतो. आणि त्याला आपल्या लॅपटॉपवर विना-इंटरनेट चालवायचं काम **Ollama** हे टूल करतं.*

#### What to Speak to Your Professor
> *"Sir, we use a 4-bit quantized Qwen2.5-Coder model hosted locally via Ollama. It consumes less than 1 GB of memory, requires zero external API keys, operates at 20–27 tokens per second on CPU with sub-second warm TTFT (~290 ms), and guarantees complete offline privacy."*

---

### 9. What Is Prompt Construction and Why Is It Necessary?

#### Definition
Prompt construction (or prompt engineering) is the process of synthesizing system instructions, user queries, past conversation context, and formatting rules into a structured instruction template for the LLM.

#### Why It Is Needed
Small local LLMs (1.5B parameters) do not have the reasoning capacity of 70B cloud models. If given an ambiguous or casual prompt, they may:
- Write variable names in Marathi transliteration (e.g., `sankhya = 10` instead of `number = 10`).
- Mix Hindi characters inside code blocks, breaking compilation.
- Produce disorganized text with no headings.

#### How It Works in Bhasha2Code
Our `PromptBuilder` (`backend/app/prompt/prompt_builder.py`) wraps the user query with strict behavioral policies:
1. **The Code Preservation Mandate:** System policy strictly enforces that all code, function names, keywords, and syntax MUST be standard English ASCII.
2. **Linguistic Mirroring Policy:** Directs the model to write prose explanations in the detected user dialect (e.g., explaining in Marathi-English while keeping code in Python).
3. **Study Mode Templates:** Injects structured headers (`### Problem Understanding`, `### Algorithm`, `### Flowchart`, `### Code`, `### Viva Questions`).
4. **Context Injection:** Injects past code snippets from the SQLite database so follow-up queries work seamlessly.

#### Simple Example
Instead of sending raw text: `"yat loop lav"`, PromptBuilder sends:
```text
[SYSTEM] You are Bhasha2Code. Target Language: Python. Intent: GENERATE_CODE.
Preserve all code keywords in English ASCII. Explain using Marathi-English.
[PREVIOUS CODE] def factorial(n): ...
[USER QUERY] yat loop lav
```

#### What to Speak to Your Professor
> *"Sir, small local models require deterministic steering. Our PromptBuilder enforces our Code Preservation Mandate—guaranteeing that code syntax remains in standard English while pedagogical explanations mirror the student's regional language."*

---

### 10. How Does Code Validation Differ From Code Execution?

#### Definition
- **Code Validation (Static Syntax Analysis):** Inspecting the structure and syntax of source code **without running it** to confirm that it follows the grammar rules of the programming language.
- **Code Execution (Dynamic Runtime):** Actually running the compiled/interpreted program with CPU instructions and memory allocation to evaluate output and behavior.

#### Why Both Are Needed
Running unvalidated code directly in an execution environment wastes CPU cycles and exposes the system to crashes on simple typos. Static validation acts as an immediate syntax filter. Once valid, execution dynamically verifies logic against test cases.

#### How It Works in Bhasha2Code
1. **Static Validation (`ResponseValidator`):**
   - **For Python:** Uses Python's native `ast.parse(code)`. If there is a missing colon, unexpected indentation, or ML data leakage, the AST parser and ML consistency visitor emit precise diagnostics without running the code.
   - **For JS, C, C++, and Java:** Executes host compilers/interpreters via subprocess with syntax-checking flags (`gcc -fsyntax-only`, `javac`, `node --check`) without execution.
   - **For SQL:** Uses regex balance checkers (quotes, parentheses, keyword order).
   - Badges the artifact in the UI as `VALID`, `INCOMPLETE`, `INVALID`, or `UNSUPPORTED`.
   - *Academic Limitation:* Syntax validation only verifies grammatical well-formedness; it does NOT prove algorithmic correctness, absence of logical bugs (e.g. division by zero, infinite loop), or that the code accurately solves the student's problem.
2. **Execution Gating:**
   - If code has a syntax error, the frontend disables the **"Run"** button to prevent unnecessary execution failures.
   - When the user clicks **"Run"**, the code is dispatched to the Docker sandbox.

#### Simple Example
```python
def add(a, b)
    return a + b
```
- **Static AST Validation:** Catches missing colon `:` on line 1 in 0.2ms. Reports: `[ERROR] expected ':' (line 1)`.
- **Execution:** Never reached because the AST validation gate blocked it.

#### What to Speak to Your Professor
> *"Sir, validation is compile-time/static syntax parsing using the Abstract Syntax Tree (AST) for Python and compiler syntax flags for other languages, executing without running the code. It guarantees syntactic validity before execution, but not algorithmic logic. Execution is dynamic runtime processing inside our isolated Docker container."*

---

### 11. Why Is Docker Used as an Execution Sandbox?

#### Definition
Docker is an OS-level virtualization platform that packages software in lightweight, standalone containers running on isolated Linux cgroups and namespaces.

#### Why It Is Needed
Executing user-provided or LLM-generated code on the host operating system creates critical security vulnerabilities:
- Malicious system commands: `os.system("rm -rf /")` could wipe the host disk.
- Infinite loops: `while True: pass` could peg the host CPU at 100%.
- Fork bombs: `import os; [os.fork() for _ in range(100)]` could crash the OS.
- Network attacks: Socket scripts could launch port scans or reverse shells.

#### How It Works in Bhasha2Code
Our `DockerRuntime` (`backend/app/sandbox/docker_runtime.py`) spawns temporary, ephemeral containers with strict kernel-level constraints:
1. `--network none`: Strict network denial (no LAN or internet access).
2. `--memory 256m`: Maximum 256 MB RAM (768 MB for ML container). Exceeding this triggers an immediate `OOMKilled` signal.
3. `--cpus 0.5`: Capped at half a CPU core.
4. `--pids-limit 64`: Blocks fork bombs from spawning runaway processes.
5. `--read-only`: The container root filesystem cannot be modified.
6. `--tmpfs /tmp:rw,noexec,nosuid`: Temporary scratch space with execution disallowed.
7. `--user 1000:1000`: Runs as an unprivileged non-root user.
8. **Wall-clock timeout:** Hard process kill after **3.0 seconds** (10.0s for ML workloads).
9. **Automatic Cleanup:** Orphaned containers and temporary volumes (`b2c-run-*`) are automatically pruned on startup and teardown.

#### Simple Example
If a student runs an infinite loop `while True: pass`, the sandbox runner kills the container after exactly 3.0 seconds and returns: `[TIMEOUT] Execution timed out after 3.0 seconds`. The host laptop remains completely stable.

#### Marathi-English Explanation (मराठीत)
> *जर एखाद्या युझरने चुकून किंवा मुद्दाम व्हायरस किंवा लूप असलेला कोड टाकला, तर लॅपटॉप क्रॅश होऊ नये म्हणून आम्ही **Docker Sandbox** वापरतो. तो कोड एका सुरक्षित, बंदिस्त डब्यात (कंटेनर) चालतो. त्याला इंटरनेट नसतं, रॅमची मर्यादा असते, आणि ३ सेकंदात तो आपोआप बंद होतो.*

#### What to Speak to Your Professor
> *"Sir, we enforce defense-in-depth sandbox security. Code executes inside non-root Docker containers with zero network access, a 256MB memory quota, cgroup PID limits against fork bombs, and a 3-second hard timeout."*

---

### 12. What Roles Do React, FastAPI, SQLite, SQLAlchemy, and SSE Play?

#### Component Breakdown

| Technology | Architectural Role | Why Chosen |
| :--- | :--- | :--- |
| **React 18 + Vite** | Single Page Application (SPA) frontend | Fast DOM updates, modular component hierarchy, rapid HMR during development. |
| **FastAPI** | High-performance asynchronous backend API | Native async/await support, automatic Pydantic schema validation, clean dependency injection. |
| **Server-Sent Events (SSE)** | Unidirectional streaming protocol | Streams tokens from Ollama to the browser in real-time over standard HTTP without WebSocket overhead. |
| **SQLite 3** | Lightweight local database engine | Serverless, zero-configuration, zero-network overhead; stored locally in `bhasha2code.db`. |
| **SQLAlchemy 2.0** | Object-Relational Mapping (ORM) layer | Type-safe database queries, relationship mapping across Users, Sessions, Messages, and Code artifacts. |

#### How They Interact
1. React frontend posts a message via `fetch()` to `/api/v1/chat/stream`.
2. FastAPI processes the message through the NLP pipeline and prompt builder asynchronously.
3. FastAPI requests Ollama streaming and yields tokens via an SSE `StreamingResponse`.
4. React reads chunk by chunk via `ReadableStreamDefaultReader` and updates the UI state in real-time.
5. On stream completion, FastAPI commits the user message, assistant response, code artifact, and metadata into SQLite via SQLAlchemy.

#### What to Speak to Your Professor
> *"Sir, we use a modern decoupled architecture: React 18 consumes real-time token events via Server-Sent Events from an asynchronous FastAPI gateway. All state persistence is managed locally through SQLAlchemy and SQLite."*

---

### 13. How Does Study Mode Work in Bhasha2Code?

#### Definition
Study Mode is an educational scaffolding setting in Bhasha2Code designed to maximize conceptual comprehension rather than just outputting raw code.

#### Why It Is Needed
In regular "Developer Mode", AI coding assistants output compact code blocks. While useful for working professionals, this hinders student learning. When preparing for college lab practicals and viva-voce examinations, students need to understand the underlying algorithm, see the logic visually, and practice answering faculty questions.

#### How It Works in Bhasha2Code
When the **Study Mode toggle** is enabled in the UI (`payload.study_mode = true`):
1. **Specialized Prompt Injection:** The prompt builder instructs the LLM to output 5 structured educational sections:
   - `### Problem Understanding`: Brief summary of input/output constraints.
   - `### Algorithm`: Step-by-step logic in numbered format.
   - `### Flowchart`: Logic flow description and ASCII diagram.
   - `### Code`: Clean, well-commented implementation.
   - `### Viva Questions`: 3–5 college examination Q&A pairs.
2. **Backend Parsing (`backend/app/api/parsers.py`):**
   - The response parser extracts each section into a structured `StudySectionResponse` object.
   - For common data structure algorithms (e.g. Linear Search, Binary Search), it generates structured flowchart nodes.
3. **Frontend Visual Rendering (`VisualFlowchart.jsx` & `StudySections.jsx`):**
   - Renders an interactive SVG visual flowchart displaying Start, Initialization, Decision Condition, Loop Body, and End nodes with color-coded badges.
   - Renders an expandable accordion for viva questions and answers.

#### Simple Example
- Query: *"Linear search samjhava"* with Study Mode ON.
- Result:
  - Algorithm steps: 1. Start from index 0. 2. Compare `arr[i]` with target. 3. If matched, return index. 4. If end reached, return -1.
  - Visual Flowchart: Interactive diagram showing loop condition `i < len(arr)`.
  - Viva Q&A: *"What is the worst-case time complexity of Linear Search?"* → *"O(n), when the element is at the end or absent."*

#### What to Speak to Your Professor
> *"Sir, Study Mode is our primary educational innovation. It deconstructs generated solutions into algorithmic steps, visual SVG flowcharts, complexity metrics, and curriculum-aligned viva questions."*

---

### 14. How Are Incomplete Outputs and Runtime Errors Handled?

#### Definition
Error resilience mechanisms designed to detect and recover from model token cutoffs, compiler syntax errors, and container runtime exceptions.

#### Why It Is Needed
Local 1.5B/3B models running with token caps can occasionally stop generating mid-loop or leave an unclosed code fence (```). If unhandled, this produces broken code artifacts and confusing error messages.

#### How It Works in Bhasha2Code
1. **Token Truncation Detection (`check_is_incomplete`):**
   - Inspects Ollama's `done_reason` attribute. If `done_reason == "length"`, the generation hit the token ceiling.
   - Inspects trailing markdown: If an unclosed code block (```) is detected, the parser cleanly caps it and marks the artifact status as `INCOMPLETE`.
   - The UI presents a **"Continue Generation"** suggestion button.
2. **Deterministic Algorithm Fallback:**
   - For core curriculum benchmarks (e.g., Linear Search, Binary Search, Prime Check), if the model output truncates, the system guarantees an authentic, valid code block to prevent presenting broken code to the student.
3. **Docker Runtime Diagnostics:**
   - If user code crashes during execution (e.g., `ZeroDivisionError` or C++ `Segmentation fault`), the sandbox captures stderr and exit codes cleanly, formats the stack trace, and displays it in the UI terminal without crashing the application.

#### What to Speak to Your Professor
> *"Sir, we handle failures gracefully: token truncations are flagged via AST and done_reason checks, syntax errors are badged with exact line diagnostics, and container runtime exceptions are safely routed to the terminal."*

---

### 15. What Are the System's Limitations and Future Scope?

#### Verified Current Limitations
1. **CPU Inference Latency:** On older dual-core laptops with 8GB RAM, generating a complete Study Mode response with a 3B model can take 20–35 seconds. (The 1.5B model solves this by generating in 10–12 seconds).
2. **Grammar Range:** Highly localized regional slang or rare phonetic transliterations outside our lexicon may default to standard English.
3. **Static Syntax Analysis for Non-Python:** Python uses true AST compilation; C, C++, and Java use regex/lexical pattern checkers until executed inside the Docker compiler.
4. **Host Docker Requirement:** Sandboxed execution requires Docker installed on the host OS.

#### Future Enhancements
1. **Indic Voice Interface:** Incorporate offline AI4Bharat Bhashini or Indic Whisper models for direct speech-to-code in Marathi and Hindi.
2. **Expansion to More Languages:** Expand dictionaries and datasets to include Gujarati, Telugu, Kannada, and Tamil.
3. **SPPU Syllabus Fine-Tuning:** Fine-tune `Qwen2.5-Coder` directly on Savitribai Phule Pune University laboratory assignments and viva question banks.
4. **Visual Step-Through Debugger:** Add line-by-line variable state inspection to watch loops and data structures update visually.

#### What to Speak to Your Professor
> *"Sir, while current execution relies on text queries and consumer CPUs, our future roadmap includes Indic voice input via Whisper, fine-tuning on university lab manuals, and visual line-by-line algorithm debuggers."*
