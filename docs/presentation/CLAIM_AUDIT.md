# Bhasha2Code — Technical Claim Audit & Verification Report

**Auditor Role:** Independent Technical Auditor & External Engineering Examiner  
**Audit Target:** Bhasha2Code Mini-Project Repository (`/home/tejas/Desktop/Bhasa2code`)  
**Audit Date:** October 2026  
**Status Taxonomy:** `VERIFIED`, `PARTIALLY VERIFIED`, `UNVERIFIED`, `INCORRECT`  

---

## 1. Executive Summary & Verdict Matrix

This audit evaluates the empirical veracity of ten key engineering claims made across project presentation and documentation artifacts. All findings are derived directly from source code inspection, configuration files, live test suite runs, and hardware execution benchmarks on the host system.

| # | Claim Audited | Claimed Metric / Behavior | Verified Reality | Audit Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Intent Classifier Accuracy | 92.59% accuracy on held-out test data | Exactly 92.59% (150/162 correct) on 18-class synthetic test split; macro F1: 92.39% | **VERIFIED** *(with dataset scope caveats)* |
| **2** | NLP Inference Latency | "< 3 ms" latency on CPU | Full 4-stage pipeline mean is **8.12 ms** (i7-12650H CPU). 1.2–2.8 ms refers to isolated single-classifier inference | **PARTIALLY VERIFIED** *(misattributed to entire pipeline)* |
| **3** | Automated Test Suites | 541 backend passed, 26 skipped; 20 frontend passed | Fresh execution: **541 passed, 26 skipped** in Pytest; **20 passed, 0 skipped** in Node test runner | **VERIFIED** |
| **4** | Sub-Second Streaming | Sub-second Time-to-First-Token (TTFT) | Warm model TTFT is **289.1 ms** (sub-second); Cold-start initial model load takes **~5.6 s** | **VERIFIED** *(for warm model)* |
| **5** | Ollama Models & Context | Qwen2.5-Coder:1.5B Q4_K_M, 8192 context, operational | Installed: `qwen2.5-coder:1.5b` (986MB) & `3b` (1.9GB), Q4_K_M GGUF. `num_ctx=8192`, `num_predict=600`. Operational on localhost | **VERIFIED** *(num_predict is 600, not 2048)* |
| **6** | Offline Operation | 100% offline from clean setup | Runtime inference is 100% offline & air-gapped; initial setup requires ~3 GB of downloads (pip, npm, Ollama, Docker) | **PARTIALLY VERIFIED** *(requires distinction between setup & runtime)* |
| **7** | AST Validation Capabilities | Pre-render AST validation for Python, JS, C, C++, Java, SQL | Python uses native `ast.parse()`. JS/C/C++/Java shell out to host compilers (`gcc`, `node`, `javac`). SQL uses regex | **PARTIALLY VERIFIED** *(non-Python are compiler/regex checks)* |
| **8** | Docker Sandbox Security | Network isolation, non-root, read-only rootfs, memory/CPU/PID limits | All security invariants enforced in `docker_runtime.py`. All 5 required images built and present | **VERIFIED** |
| **9** | Study Mode Generation | Generates all 5 educational sections reliably | Pydantic schema and UI support all 5 sections; LLM outputs rely on regex parsing & deterministic heuristics due to token caps | **PARTIALLY VERIFIED** *(schema verified; generation relies on fallbacks)* |
| **10** | Architecture Diagram Accuracy | Diagram reflects implementation & backend routes | Pipeline matches design, but diagram omits `/api/v1/code` prefix for WebSocket and misplaces validator in live token stream | **PARTIALLY VERIFIED** *(route prefix & streaming topology discrepancies)* |

---

## 2. Detailed Claim-by-Claim Evidence & Technical Findings

### Claim 1: Intent Classifier Accuracy (92.59%)
- **Source Files:**
  - Model metadata: [`models/intent/metadata.json`](file:///home/tejas/Desktop/Bhasa2code/models/intent/metadata.json)
  - Evaluation script: [`scripts/evaluate_intent_classifier.py`](file:///home/tejas/Desktop/Bhasa2code/scripts/evaluate_intent_classifier.py)
  - Dataset file: [`data/datasets/intent/intent_test.csv`](file:///home/tejas/Desktop/Bhasa2code/data/datasets/intent/intent_test.csv)
- **Audit Execution Command:**
  ```bash
  .venv/bin/python scripts/evaluate_intent_classifier.py
  ```
- **Observed Fresh Output:**
  ```text
  Test Accuracy   : 0.9259 (target >= 0.78)
  Test Macro F1   : 0.9239 (target >= 0.78)
  Test Weighted F1: 0.9239
  Misclassifications: 12 / 162 total
  Average confidence: 0.5107
  Determinism check (10 runs on identical input): PASS
  ```
- **Technical Analysis & Scope:**
  - **Dataset Size:** 1,080 samples total (756 train [70%], 162 validation [15%], 162 test [15%]).
  - **Class Balance:** Exactly 18 balanced classes with 9 test samples per class (`ALGORITHM`, `APPROACH_SUGGESTION`, `ARCHITECTURE_SUGGESTION`, `BEST_PRACTICE`, `CODE_REVIEW`, `CODE_SUGGESTION`, `CONCEPT`, `CONVERT_CODE`, `DEBUG_CODE`, `ERROR_EXPLANATION`, `EXPLAIN_CODE`, `FEATURE_SUGGESTION`, `GENERATE_CODE`, `OPTIMIZE_CODE`, `PERFORMANCE_ANALYSIS`, `SEARCH`, `SECURITY_ANALYSIS`, `TEST_CASE_GENERATION`).
  - **Language Breakdown:** English test accuracy is 85.19% (23/27), Hindi is 82.61% (19/23), Marathi is 84.00% (21/25). Hinglish (30/30), Marathi-English (37/37), and Hindi-English (20/20) achieved 100% test accuracy on the synthetic dataset.
  - **Auditor Note:** The dataset is synthetically compiled and curated for project evaluation. The 92.59% accuracy is verified on this closed-set holdout split; it must not be claimed as guaranteed accuracy for arbitrary open-domain user prompts.

---

### Claim 2: NLP Inference Latency (< 3 ms)
- **Source Files:**
  - [`backend/app/nlp/pipeline/nlp_pipeline.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/nlp/pipeline/nlp_pipeline.py#L55-L180)
  - [`docs/presentation/PROJECT_REPORT.md`](file:///home/tejas/Desktop/Bhasa2code/docs/presentation/PROJECT_REPORT.md#L555-L563)
- **Audit Benchmark Execution:**
  Direct latency measurement across 100 iterations on host CPU (`12th Gen Intel Core i7-12650H`):
  ```bash
  .venv/bin/python -c '
  import time, statistics
  from backend.app.nlp.pipeline.nlp_pipeline import NLPPipeline
  pipeline = NLPPipeline()
  # Warmup & test prompt: "बायनरी सर्च अल्गोरिदमचा संपूर्ण जावा कोड लिहून दे."
  times = []
  for _ in range(100):
      t0 = time.perf_counter()
      pipeline.analyze("बायनरी सर्च अल्गोरिदमचा संपूर्ण जावा कोड लिहून दे.")
      times.append((time.perf_counter() - t0) * 1000)
  print(f"Full NLPPipeline Mean: {statistics.mean(times):.2f} ms")
  '
  ```
- **Observed Fresh Output:**
  - **Full 4-Stage `NLPPipeline.analyze()` Mean:** **8.12 ms** (Median: 8.07 ms, Min: 7.84 ms, Max: 9.39 ms)
  - Stage 1 `TextPreprocessor`: **0.038 ms**
  - Stage 2 `LanguageDetector`: **0.070 ms**
  - Stage 3 `ToneClassifier`: **3.96 ms**
  - Stage 4 `IntentClassifier`: **4.06 ms**
- **Discrepancy Analysis:**
  - `PROJECT_REPORT.md` Table 10.1 and 10.2 recorded:
    - *Intent Classifier Isolated Latency:* 2.8 ms (on CPU)
    - *Tone Classifier Isolated Latency:* 1.2 ms (on CPU)
  - Presentation documents conflated these isolated model metrics to claim that the *entire NLP pipeline* executes in "< 3 ms".
  - **Correction:** The end-to-end 4-stage pipeline executes in **~8 ms** on modern multi-core CPUs. Safe academic phrasing is **"sub-10ms CPU latency for the full 4-stage pipeline, with individual classifier inference at ~3–4 ms."**

---

### Claim 3: Backend & Frontend Test Results (541 Passed, 26 Skipped; 20 Passed)
- **Source Files:**
  - Backend configuration: [`pytest.ini`](file:///home/tejas/Desktop/Bhasa2code/pytest.ini), [`tests/`](file:///home/tejas/Desktop/Bhasa2code/tests/)
  - Frontend configuration: [`frontend/package.json`](file:///home/tejas/Desktop/Bhasa2code/frontend/package.json#L10)
- **Audit Execution Commands & Outputs:**
  1. **Backend Tests:**
     ```bash
     .venv/bin/pytest
     ```
     *Output:* `541 passed, 26 skipped, 1 warning in 48.71s` (567 items collected).
     - **Verification of 26 Skipped Tests:**
       - 19 tests in `tests/integration/sandbox/test_docker_sandbox.py` (marked `@pytest.mark.skipif` when running unit tests without live container execution harness).
       - 7 tests in `tests/unit/llm/test_ollama_integration.py` (marked for live Ollama integration test harness).
  2. **Frontend Tests:**
     ```bash
     npm test  # inside frontend/
     ```
     *Output:* `tests 20, suites 0, pass 20, fail 0, skipped 0, duration_ms 432.5ms`.
- **Verdict:** **VERIFIED**. Test tallies in documentation match actual test runner execution output.

---

### Claim 4: Sub-Second Streaming Performance
- **Source Files:**
  - Transport client: [`backend/app/llm/ollama_client.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/llm/ollama_client.py#L315-L370)
  - Diagnostic documentation: [`docs/11_development/STREAMING_PERFORMANCE.md`](file:///home/tejas/Desktop/Bhasa2code/docs/11_development/STREAMING_PERFORMANCE.md#L44-L60)
- **Audit Benchmark Execution:**
  Live end-to-end streaming test against resident Ollama daemon:
- **Observed Results:**
  - **Cold-Start Request (Initial load into RAM from disk):** TTFT = **5,627.4 ms** (~5.6 seconds).
  - **Warm Streaming Request (Model resident in RAM):** TTFT = **289.1 ms** (< 300 ms, strictly sub-second).
  - **Generation Throughput:** **27.1 tokens/sec** on Intel Core i7-12650H CPU.
- **Verdict:** **VERIFIED** for warm model inference. The presentation must state that sub-second latency applies to subsequent requests once the model is resident in RAM.

---

### Claim 5: Ollama Models, Quantization, Context Length & Operational State
- **Source Files:**
  - Configuration: [`backend/app/llm/config.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/llm/config.py#L11-L37), [`.env`](file:///home/tejas/Desktop/Bhasa2code/.env)
- **Audit Commands & Observations:**
  1. `ollama list`:
     - `qwen2.5-coder:1.5b` (ID: `d7372fd82851`, 986 MB) — **Present**
     - `qwen2.5-coder:3b` (ID: `f72c60cabf62`, 1.9 GB) — **Present**
  2. `ollama show qwen2.5-coder:1.5b`:
     - Architecture: `qwen2`
     - Parameters: `1.5B`
     - Quantization: `Q4_K_M`
     - Native context length: `32768`
  3. API status: `curl http://127.0.0.1:11434/api/tags` returns HTTP 200 with all installed tags.
  4. Environment Settings (`.env`):
     - `OLLAMA_MODEL=qwen2.5-coder:1.5b`
     - `OLLAMA_NUM_CTX=8192`
     - `OLLAMA_NUM_PREDICT=600`
- **Discrepancy:** `PROJECT_FACTS.md` line 67 stated `num_predict=2048`. In reality, `.env` and `config.py` default to `600` to prevent runaway generation on CPU. Corrected in documentation.

---

### Claim 6: Offline Operation Boundaries
- **Verification of Network Boundaries:**
  - Scanned network activity and endpoints in `backend/app/`:
    - All inference requests route to `http://127.0.0.1:11434` (Ollama loopback).
    - Database queries route to local file `sqlite:///./data/bhasha2code.db`.
    - No telemetry or external cloud APIs are imported.
    - Container execution explicitly specifies `--network none`.
- **Distinction for Academic Integrity:**
  - **First-Time Setup:** NOT offline. Downloading Python wheels, Node modules, Docker base images, and Ollama GGUF weights requires internet connectivity (~3 GB total).
  - **Runtime Execution:** 100% offline. Once installed, the system functions on a physically air-gapped machine with zero network access.

---

### Claim 7: AST Validation Capabilities and Limitations
- **Source Files:**
  - [`backend/app/validation/validators/python_validator.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/validation/validators/python_validator.py)
  - [`backend/app/validation/validators/javascript_validator.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/validation/validators/javascript_validator.py)
  - [`backend/app/validation/validators/c_validator.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/validation/validators/c_validator.py)
  - [`backend/app/validation/validators/java_validator.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/validation/validators/java_validator.py)
  - [`backend/app/validation/validators/sql_validator.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/validation/validators/sql_validator.py)
- **Technical Capabilities:**
  - **Python:** True Abstract Syntax Tree analysis using standard library `ast.parse()`. Includes an `MLCodeConsistencyChecker(ast.NodeVisitor)` checking ML data leakage (fit vs transform on test data) and label types.
  - **JavaScript:** Subprocess execution running `node --check <tmp_file>`. Returns `UNSUPPORTED` if `node` is absent on host.
  - **C & C++:** Subprocess execution running `gcc -fsyntax-only` and `g++ -fsyntax-only`. Returns `UNSUPPORTED` if GCC is absent on host.
  - **Java:** Subprocess execution running `javac <tmp_file>`. Returns `UNSUPPORTED` if `javac` is absent on host.
  - **SQL:** Pure regex and string pattern heuristics (quote balance, parenthesis balance, semicolon statement separation). No AST built.
- **Fundamental Limitations:**
  - Syntax validation guarantees syntactic validity; it **does NOT guarantee semantic correctness, runtime safety, or absence of logical bugs**.
  - Non-Python validation depends on host CLI tools.

---

### Claim 8: Docker Sandbox Isolation Settings
- **Source Files:**
  - [`backend/app/sandbox/config.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/sandbox/config.py)
  - [`backend/app/sandbox/docker_runtime.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/sandbox/docker_runtime.py#L127-L180)
  - [`backend/app/sandbox/policies.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/sandbox/policies.py)
- **Verified Command Line Flags in `build_docker_run_args`:**
  - Network isolation: `--network none`
  - Privilege restriction: `--cap-drop ALL`, `--security-opt no-new-privileges`
  - Non-root user: `--user 1000:1000`
  - Read-only rootfs: `--read-only`
  - Resource limits: `--memory 256m` (768m for ML), `--cpus 0.5`, `--pids-limit 64`
  - Scratch space: `--tmpfs /tmp:rw,noexec,nosuid,size=64m`
  - Workspace volume: `-v {volume_name}:/workspace:rw` (ephemeral named volume)
  - Execution timeout: 3.0 seconds (10.0s for ML) enforced via subprocess timeout
  - Stdout/stderr cap: 64 KB (65,536 bytes)
- **Image Verification (`docker images` output):**
  - `bhasha2code-sandbox-python:1.0.0` (127 MB) — **Verified Present**
  - `bhasha2code-sandbox-python-ml:1.0.0` (485 MB) — **Verified Present**
  - `bhasha2code-sandbox-cpp:1.0.0` (278 MB) — **Verified Present**
  - `bhasha2code-sandbox-java:1.0.0` (364 MB) — **Verified Present**
  - `bhasha2code-sandbox-javascript:1.0.0` (136 MB) — **Verified Present**

---

### Claim 9: Study Mode Generation of Five Documented Sections
- **Source Files:**
  - Schema: [`backend/app/api/schemas.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/api/schemas.py#L117-L145) (`StudySectionResponse`)
  - Parser: [`backend/app/api/parsers.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/api/parsers.py#L535-L675)
- **Documented Sections:**
  1. `problem_understanding` (Prose explanation of the problem)
  2. `algorithm` (List of numbered/bulleted algorithmic steps)
  3. `flowchart` / `flowchart_nodes` (ASCII text & structured SVG flowchart nodes)
  4. `important_points` (Key takeaways and time/space complexity notes)
  5. `viva_questions` (List of `{question, answer}` pairs)
- **Technical Finding:**
  - The Pydantic schema and frontend renderer fully support all five sections.
  - However, small open-weights LLMs (1.5B/3B) frequently fail to generate all 5 headers deterministically or get truncated by token caps (`num_predict=600`).
  - To prevent frontend errors, [`backend/app/api/parsers.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/api/parsers.py) uses regex extraction and algorithmic fallback heuristics (e.g. for linear/binary search).
  - **Verdict:** **PARTIALLY VERIFIED**. The structured sections exist in the architecture, but end-to-end output relies on backend parsing and normalization fallbacks rather than raw LLM generation alone.

---

### Claim 10: Architecture Diagram Accuracy
- **Source Files:**
  - [`docs/presentation/architecture.mmd`](file:///home/tejas/Desktop/Bhasa2code/docs/presentation/architecture.mmd)
  - [`backend/app/main.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/main.py#L101-L106)
  - [`backend/app/api/routes/code.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/api/routes/code.py#L97)
  - [`backend/app/api/routes/chat_stream.py`](file:///home/tejas/Desktop/Bhasa2code/backend/app/api/routes/chat_stream.py#L280-L360)
- **Identified Discrepancies:**
  1. **WebSocket Route Prefix:** `architecture.mmd` line 62 labelled the WebSocket as `WebSocket /interactive-run`. The router is mounted with prefix `/code` under `/api/v1`, so the actual endpoint is `/api/v1/code/interactive-run`.
  2. **Streaming Pipeline Topology:** `architecture.mmd` lines 58–59 showed `OllamaDaemon --> RespValidator --> ChatUI` for streaming tokens. In reality, live tokens stream directly from Ollama to `ChatUI` via SSE `event: token`. `RespValidator` operates on the accumulated full text *after* generation completes, returning validated artifacts in the final `complete` event.
- **Verdict:** **PARTIALLY VERIFIED**. Updated `architecture.mmd` to reflect exact route prefixes and true streaming topology.

---

## 3. Safe Academic Wording for Presentation & Project Report

When presenting to faculty, evaluators, and project guides, replace absolute or ambiguous claims with precise, defensible formulations:

| Document / Topic | Previous Unsupported Phrasing | Recommended Academic Phrasing |
| :--- | :--- | :--- |
| **NLP Latency** | *"Our Scikit-Learn NLP pipeline runs in 3 milliseconds."* | *"Our complete 4-stage internal NLP pipeline executes in approximately 8 milliseconds on CPU, with individual classifier inferences taking 1.2 to 4.0 milliseconds."* |
| **Intent Accuracy** | *"92.59% accuracy on bilingual code-mixed input."* | *"92.59% accuracy and 92.39% macro F1 across 18 balanced classes on our 162-sample held-out benchmark split, with 100% accuracy on code-mixed test subsets."* |
| **Offline Claim** | *"100% offline from a clean setup."* | *"100% offline and air-gapped during runtime inference, eliminating recurring API costs. Initial dependency installation requires one-time downloads of models and packages."* |
| **Code Validation** | *"AST syntax validation for Python, JS, C, C++, and SQL."* | *"Native Python Abstract Syntax Tree (AST) validation with static ML consistency checks, complemented by compiler syntax checks for C, C++, and Java, and regex structural validation for SQL."* |
| **Streaming TTFT** | *"Sub-second response latency across all systems."* | *"Sub-second Time-to-First-Token (~290 ms) once the quantized model is resident in RAM, delivering immediate visual streaming via Server-Sent Events."* |
| **Study Mode** | *"The model reliably writes 5 distinct pedagogical sections."* | *"Structured educational scaffolding parses and normalizes five key learning artifacts (problem understanding, algorithm, SVG flowchart, key points, and viva Q&A) with deterministic backend fallbacks."* |

---

## 4. Five Core Facts You Must Personally Understand Before Your Viva

As an engineering student defending this project, you must be able to explain these five technical facts clearly:

1. **Two-Tier AI Architecture (Classifiers vs. Generative LLM):**  
   Bhasha2Code does *not* use a large transformer for intent or language detection. It uses lightweight, deterministic Scikit-Learn models (TF-IDF + Logistic Regression, <5 MB disk footprint) that run in ~8 ms on CPU to classify intent and tone. That classification is then used by `PromptBuilder` to steer the generative coding LLM (`Qwen2.5-Coder:1.5B` via Ollama) which writes the actual code.

2. **The Code Preservation Mandate:**  
   Because student queries are code-mixed (Marathi/Hindi/English), a naive LLM might translate code identifiers into transliterated words (e.g., `def sankhya_shodha()`). The `PromptBuilder` injects a strict system constraint: programming language keywords, variable names, and standard syntax MUST remain in standard English ASCII, while pedagogical explanations mirror the student's regional dialect.

3. **Static Syntax Validation vs. Dynamic Execution:**  
   Validation is *not* execution. Python code is parsed into an Abstract Syntax Tree via `ast.parse()`, detecting syntax and indentation errors in <1 ms without running code. Execution is dynamic and happens *only* after validation passes, inside an ephemeral Docker container.

4. **Container Isolation (cgroups & namespaces):**  
   Untrusted code is executed inside a container with `--network none` (zero internet or LAN access), `--cap-drop ALL`, `--user 1000:1000` (non-root), `--read-only` rootfs, and strict cgroup caps (256 MB RAM, 0.5 CPU cores, 64 PIDs, 3.0s hard timeout). This neutralizes infinite loops, fork bombs, and malicious filesystem deletion.

5. **Server-Sent Events (SSE) Streaming vs. Buffered Generation:**  
   Local LLM generation on consumer CPUs takes 8–15 seconds to complete. Without streaming, a student would stare at a frozen screen. By streaming tokens over SSE (`POST /api/v1/chat/stream`), the Time-to-First-Token (TTFT) is under 300 ms on a warm model. The student sees output immediately while post-processing and AST validation occur when generation finishes.
