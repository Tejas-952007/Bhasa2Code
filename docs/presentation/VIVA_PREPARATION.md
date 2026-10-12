# Bhasha2Code — Engineering Viva & Faculty Defense Master Guide

> **Candidate:** Tejas Ingle (PRN: `[Student PRN]`)  
> **Degree:** Bachelor of Engineering (B.E.), Third Year  
> **Department:** Department of Computer Engineering / AI & Data Science  
> **College:** Nutan Maharashtra Institute of Engineering & Technology (NMIET), Talegaon Dabhade, Pune  
> **Project Guide:** Prof. Gajanan Godage  

---

## The 90-Second Project Introduction Pitch (पाठ करण्यासाठी / To Memorize)

> *"Good morning, respected external examiner and faculty members.  
> My name is Tejas Ingle, and my mini-project is titled **Bhasha2Code: An Offline-First Multilingual Natural Language-to-Code Generation, Debugging, and Explanation Assistant**, developed under the guidance of Prof. Gajanan Godage.
> 
> In India, most engineering students think and conceptualize programming algorithms in their native language—such as Marathi or Hindi. When forced to translate their thoughts into formal English prompts for tools like ChatGPT, it creates cognitive friction. Furthermore, commercial tools require recurring subscription fees ($20/month), are 100% cloud-dependent, and lack educational scaffolding.
> 
> To solve this, we engineered **Bhasha2Code**. It runs completely offline on consumer hardware with zero API fees. It features a custom 4-stage NLP pipeline that detects code-mixed Marathi-English and Hinglish intents in just 3 milliseconds with 92.59% accuracy. We host a 4-bit quantized open-source Large Language Model—**Qwen2.5-Coder:1.5B**—locally via Ollama. 
> 
> To eliminate hallucinations, all generated code passes **Abstract Syntax Tree (AST)** validation before rendering. For execution, we provide an ephemeral **Docker sandbox** with zero network access and strict memory caps. Finally, our educational **Study Mode** automatically generates step-by-step algorithms, visual flowcharts, and curriculum viva questions.
> 
> Across 541 automated tests, our system achieves sub-second token streaming and complete offline privacy. I am ready to demonstrate the live project and answer your questions."*

---

## SECTION 1: Basic Project Questions (10 Questions)

### Q1. What is the core problem statement of your project?
* **English Answer:** *"Sir, our problem statement is to build an offline, zero-recurring-cost programming assistant that interprets code-mixed Indian vernacular prompts (Marathi, Hindi, Hinglish, Marathi-English), generates verified source code using local LLMs, and provides sandboxed runtime validation and educational scaffolding on consumer-grade hardware."*
* **Marathi-English Hint:** *"विद्यार्थ्यांच्या डोक्यात विचार मराठीत येतो पण कोड इंग्रजीत करावा लागतो. आमची सिस्टीम दोन्हीतलं अंतर मिटवते आणि पूर्णपणे ऑफलाइन चालते."*

### Q2. Why didn't you just use ChatGPT, Claude, or GitHub Copilot?
* **English Answer:** *"Sir, there are four key reasons:
  1. **Cost:** Commercial APIs cost $10–$20 per month, which is unaffordable for typical college students.
  2. **Internet Dependency:** Commercial tools fail in offline or air-gapped college laboratories.
  3. **Privacy:** Student code is transmitted to third-party offshore cloud servers.
  4. **Pedagogy:** Commercial assistants output raw code blocks without providing algorithmic breakdowns, flowcharts, or viva questions."*

### Q3. Who is the target user of Bhasha2Code?
* **English Answer:** *"Sir, our primary users are first- and second-year engineering students from non-metro and regional backgrounds who are learning programming and data structures, as well as educational institutions with air-gapped computer laboratories."*

### Q4. What programming languages does your system support?
* **English Answer:** *"Sir, Bhasha2Code supports code generation and validation for Python 3, C, C++, Java, JavaScript, and ANSI SQL. Python has native AST syntax parsing, while others utilize structured lexical validators and containerized compiler validation."*

### Q5. What is the difference between Developer Mode and Study Mode?
* **English Answer:** *"Sir, Developer Mode is optimized for compact, working code generation with minimal prose for rapid development. Study Mode is an educational scaffolding mode that deconstructs the solution into Problem Understanding, Algorithm Steps, Visual SVG Flowcharts, Complete Code, and Curriculum Viva Q&A pairs."*

### Q6. Does your project require an active internet connection to work?
* **English Answer:** *"No, sir. After the initial installation and downloading of the local model weights via Ollama, Bhasha2Code operates 100% offline. The NLP classifiers, local LLM, database, and Docker sandbox all run locally on localhost."*

### Q7. What hardware is required to run Bhasha2Code?
* **English Answer:** *"Sir, it runs on everyday consumer hardware: an Intel Core i5 or AMD Ryzen quad-core processor with 8GB to 16GB of RAM. It does not require any dedicated NVIDIA GPU because our Qwen2.5-Coder model is 4-bit quantized and consumes less than 1 GB of memory."*

### Q8. What is the Code Preservation Mandate in your system?
* **English Answer:** *"Sir, it is a strict prompt policy rule. It guarantees that all programming syntax, keywords (like `def`, `for`, `class`), and variable identifiers remain strictly in standard English ASCII characters, while the conversational explanations and comments mirror the student's regional language."*

### Q9. Is Bhasha2Code a simple wrapper around Ollama?
* **English Answer:** *"No, sir. Ollama is only the raw token generation engine. Bhasha2Code adds a custom 4-stage NLP classification pipeline, context management with sliding history, dynamic prompt policy engines, Abstract Syntax Tree validation, an ephemeral Docker sandbox, and an interactive React web workspace with visual flowchart rendering."*

### Q10. What are the key performance indicators (KPIs) of your project?
* **English Answer:** *"Our 4 verified KPIs are:
  1. **NLP Classification:** 92.59% intent accuracy and 97.78% tone accuracy with sub-10ms CPU latency (~8 ms full pipeline, 1.2–4.0 ms per classifier).
  2. **Generation Latency:** ~290–450 ms warm Time-to-First-Token and 22–27 tokens/second on consumer CPU.
  3. **Execution Safety:** Zero network access (`--network none`) and 256MB memory cap with automatic 3-second hard timeout.
  4. **Test Reliability:** 541 backend unit tests passing in pytest and 20 frontend integration tests passing with 0 failures."*

---

## SECTION 2: NLP, Machine Learning & LLM Questions (10 Questions)

### Q11. How does your 4-stage NLP pipeline work?
* **English Answer:** *"Sir, the pipeline runs sequentially in `backend/app/nlp/pipeline/nlp_pipeline.py`:
  - **Stage 1 (TextPreprocessor):** Applies Unicode NFC normalization and strips attached code blocks.
  - **Stage 2 (LanguageDetector):** Evaluates Devanagari script ratios and lexical dictionaries to identify 6 language variants.
  - **Stage 3 (ToneClassifier):** Predicts conversational style across 6 classes using TF-IDF and Logistic Regression.
  - **Stage 4 (IntentClassifier):** Maps user intent across 18 programming categories using TF-IDF and Logistic Regression."*

### Q12. Why did you choose TF-IDF and Logistic Regression over BERT or fine-tuned transformers?
* **English Answer:** *"Sir, deep transformer models like mBERT or XLM-RoBERTa require 500MB+ of RAM and introduce 50–150 ms of CPU latency. In contrast, our TF-IDF + Logistic Regression models occupy less than 5 MB of disk space, execute in approximately 8 milliseconds on CPU (1.2–4.0 ms per model), and achieved 92.59% accuracy across 18 intent classes on our held-out benchmark."*
* **Marathi-English Hint:** *"BERT खूप जड आहे आणि CPU वर स्लो चालतो. TF-IDF + Logistic Regression फक्त ८ मिलीसेकंदात चालतो आणि लॅपटॉपवर अजिबात लोड येत नाही."*

### Q13. How do you handle Romanized Marathi words that standard language libraries fail on?
* **English Answer:** *"Sir, standard libraries like `langdetect` assume Romanized words are English. We built a custom lexical dictionary containing unambiguous Marathi verb roots (e.g., `banav`, `kadh`, `samjav`) and post-positions (e.g., `madhe`, `sathi`, `cha`, `la`). Our LanguageDetector checks token intersections against these dictionaries and evaluates Devanagari Unicode blocks."*

### Q14. What are homographs and how does your LanguageDetector resolve them?
* **English Answer:** *"Sir, homographs are words with identical Latin spelling but different meanings across languages. For example, 'the' is an English article, but in Hindi, 'the' (थे) is an auxiliary verb. Similarly, 'me' is an English pronoun, but in Marathi, 'me' (मी) means 'I'. Our system checks for the presence of other unambiguous Indic tokens in the sentence: if present, the homograph resolves to Indic; otherwise, it defaults to English."*

### Q15. What features and n-gram ranges are used in your intent classifier?
* **English Answer:** *"Sir, as verified in `models/intent/metadata.json`, we use:
  - Word n-grams from 1 to 2 (unigrams and bigrams).
  - Character n-grams from 3 to 5 with `char_wb` (character n-grams inside word boundaries) to capture Indic inflectional suffixes.
  - Sublinear term frequency ($1 + \log(tf)$) to prevent high-frequency words from skewing vectors."*

### Q16. What is the mathematical formulation of your Logistic Regression classifier?
* **English Answer:** *"Sir, it is a multi-class linear model with a Softmax output layer:
  $$P(y = k \mid x) = \frac{\exp(w_k^T \cdot x + b_k)}{\sum_{j=1}^{K} \exp(w_j^T \cdot x + b_j)}$$
  We train it using the L-BFGS solver, an L2 regularization parameter $C = 3.0$, and balanced class weights to handle sample distributions across all 18 classes."*

### Q17. What LLM are you using, and what does 4-bit quantization mean?
* **English Answer:** *"Sir, we use **Qwen2.5-Coder:1.5B** (and 3B), an open-weights model trained on 5.5 trillion code tokens. Quantization reduces the precision of model weights from 16-bit floating point (FP16) down to 4-bit integers (Q4_K_M GGUF format). This reduces RAM usage from ~4 GB down to ~986 MB, allowing it to execute smoothly on a standard laptop CPU."*

### Q18. Why is low temperature (0.2) used during LLM inference?
* **English Answer:** *"Sir, temperature controls randomness in autoregressive next-token selection. In code generation, determinism and syntactic correctness are paramount. Setting `temperature=0.2` ensures the model selects high-probability, syntactically correct tokens and avoids creative hallucinations."*

### Q19. How do you prevent small models from hallucinating non-English keywords?
* **English Answer:** *"Sir, small models can be prone to instruction drift. Our `PromptBuilder` wraps user queries in strict system policies: explicitly specifying the target programming language, injecting the Code Preservation Mandate, and framing the user's regional query as input data rather than system instructions."*

### Q20. What is Time-to-First-Token (TTFT) and why is it important?
* **English Answer:** *"Sir, TTFT is the latency between the user submitting a prompt and the first generated token appearing on screen. In our system, warm TTFT is under 300 to 450 milliseconds once the model is resident in RAM. Thanks to Server-Sent Events (SSE), the student sees output begin almost immediately, rather than waiting 10 to 15 seconds for the entire response to complete."*

---

## SECTION 3: Backend, Database & API Questions (5 Questions)

### Q21. Why did you use Server-Sent Events (SSE) instead of WebSockets for the chat stream?
* **English Answer:** *"Sir, chat streaming is fundamentally unidirectional: the client sends a single HTTP POST request, and the server streams tokens back. Server-Sent Events operate over standard HTTP, support automatic reconnection, work effortlessly with standard proxies, and require less connection state overhead than bidirectional WebSockets."*

### Q22. How is session and conversation context maintained across turns?
* **English Answer:** *"Sir, our `ContextManager` uses SQLAlchemy to query the local SQLite database. It loads the last $N$ turns of message history and previously generated code artifacts for that session, injects them into the prompt specification, and updates the active programming language state in the `sessions` table."*

### Q23. What database are you using, and what is the database schema?
* **English Answer:** *"Sir, we use **SQLite 3** via **SQLAlchemy 2.0**. Our schema includes 7 tables: `users`, `sessions`, `messages`, `generated_codes`, `notes`, `saved_messages`, and `debug_histories`. Foreign key relationships link messages and generated code artifacts directly to active sessions."*

### Q24. How do you prevent duplicate submissions if a student clicks 'Send' multiple times?
* **English Answer:** *"Sir, the frontend generates a unique `client_turn_id` for every message submission. The backend checks if a user turn with that ID already exists in the database. If so, it returns an idempotent cached response stream without re-running LLM generation. Additionally, the frontend button has a concurrency lock."*

### Q25. How do you handle CORS and API security in local development?
* **English Answer:** *"Sir, FastAPI's `CORSMiddleware` explicitly permits requests only from the local Vite development origins (`http://localhost:5173` and `http://127.0.0.1:5173`). All API inputs are strictly validated through Pydantic v2 data models."*

---

## SECTION 4: Docker, Security & Testing Questions (5 Questions)

### Q26. What happens if a user submits malicious code like `os.system("rm -rf /")`?
* **English Answer:** *"Sir, our system uses **Defense-in-Depth**. Code never executes on the host machine. It executes inside an ephemeral Docker container (`b2c-run-*`) where:
  1. The root filesystem is mounted strictly read-only (`--read-only`).
  2. The process runs as an unprivileged user (`UID 1000`).
  3. The destructive command only affects the temporary virtual container filesystem, leaving the host operating system completely untouched."*
* **Marathi-English Hint:** *"हो सर, सिस्टीम १००% सुरक्षित आहे. कोड लॅपटॉपवर नाही तर डॉकर कंटेनरमध्ये चालतो. जर rm -rf / चालवला, तरी तो कंटेनरच्या आतच ब्लॉक होतो आणि लॅपटॉपला काहीही धोका नसतो."*

### Q27. How does the Docker sandbox handle infinite loops or fork bombs?
* **English Answer:** *"Sir, we enforce two kernel-level cgroup constraints:
  1. **Infinite Loops:** A hard wall-clock timeout of 3.0 seconds terminates the container via a background timer thread (`container.kill()`).
  2. **Fork Bombs:** We pass `--pids-limit 64`, which caps the total number of processes inside the container to 64. When a fork bomb tries to create more processes, the kernel immediately denies the system call."*

### Q28. Why does the container run with `--network none`?
* **English Answer:** *"Sir, `--network none` disables all virtual network interfaces inside the container. This prevents untrusted code from opening socket connections, downloading external payloads, exfiltrating student data, or executing reverse shells."*

### Q29. How does your Abstract Syntax Tree (AST) validator work?
* **English Answer:** *"Sir, for Python, we pass the extracted code string to Python's built-in `ast.parse()` module. If there is a syntax error (such as a missing colon or unmatched bracket), Python's AST compiler throws a `SyntaxError` with the exact line and column offset in under 1 millisecond. If invalid, the UI flags the error and disables the 'Run' button."*

### Q30. What automated testing have you conducted on this project?
* **English Answer:** *"Sir, we have two comprehensive automated test suites:
  1. **Backend Test Suite (Pytest):** 541 passing tests covering database repositories, API endpoints, NLP classification stages, prompt builders, AST validators, and Docker runner policies.
  2. **Frontend Test Suite (Node Native Test Runner):** 20 passing unit tests verifying diagnostic parsers, flowchart security, execution gating, debounce typing, and SSE event adaptation.
  Both test suites pass with 100% success rate on active tests."*

---

## Quick Reference: Faculty Keywords & Buzzwords

When answering questions, naturally weave in these technical terms:
- **"Deterministic 4-Stage NLP Pipeline"** (for language/intent)
- **"4-bit Quantized GGUF Model via Ollama"** (for local inference)
- **"Abstract Syntax Tree (AST) Compilation Validation"** (for code safety)
- **"Ephemeral Docker Sandbox with cgroup quotas"** (for isolated execution)
- **"Code Preservation Mandate"** (for keeping code in English ASCII)
- **"Server-Sent Events (SSE)"** (for real-time token streaming)
- **"Pedagogical Scaffolding & Study Mode"** (for flowcharts and viva Q&A)
