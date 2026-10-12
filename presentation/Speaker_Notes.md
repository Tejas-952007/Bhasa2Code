# Bhasha2Code: 12-Slide Speaker Notes & Viva Delivery Guide

> **Presenter:** Tejas Ingle (PRN: `[Student PRN]`)  
> **Institution:** Nutan Maharashtra Institute of Engineering & Technology (NMIET), Talegaon, Pune  
> **Project Guide:** Prof. Gajanan Godage  
> **Audience:** Faculty Reviewers & Technical Viva Examiners  

---

### Slide 1 — Title Slide
* **What to say:**  
  *"Good morning/afternoon respected Guide and Examiners. My name is Tejas Ingle, from the Department of Computer Engineering, NMIET Pune. Today, I am presenting my NLP and Machine Learning Mini-Project titled **Bhasha2Code: A Multilingual AI Coding Assistant and Educational Sandbox**, developed under the guidance of Prof. Gajanan Godage."*
* **Key highlight:** Emphasize that this is an offline, privacy-first NLP system designed to bridge the linguistic barrier in computer science education.

---

### Slide 2 — Abstract & Project Overview
* **What to say:**  
  *"To give a quick overview: In India, a majority of students think and conceptualize programming logic in regional languages like Marathi or Hindi. When they try to express complex coding queries in formal English, they face significant friction. Commercial tools like ChatGPT or Copilot charge subscriptions, require constant internet, and send student code to foreign cloud servers.*  
  *Bhasha2Code solves this by integrating an offline, modular **NLP classification pipeline** with a quantized local LLM (**Qwen2.5-Coder** via Ollama), automated **AST syntax validation**, and an isolated **Docker execution sandbox** at zero recurring cost."*

---

### Slide 3 — Problem Statement & Objectives
* **What to say:**  
  *"Our problem statement targets the linguistic divide, high cloud costs, and lack of code verification in technical education. We established four measurable objectives:*  
  1. *Build an offline NLP classifier to recognize code-mixed Marathi-English queries across 18 programming intents with >90% accuracy.*  
  2. *Design a deterministic prompt engine enforcing standard English syntax while keeping explanations in the user's regional dialect.*  
  3. *Deploy open-weights quantized models locally on consumer CPU hardware with zero API billing.*  
  4. *Implement an automated AST syntax verification pipeline and safe Docker sandbox to eliminate syntax hallucinations."*

---

### Slide 4 — Literature Survey
* **What to say:**  
  *"In our literature survey, we analyzed four foundational works:*  
  * *First, **Chen et al. (OpenAI Codex, 2021)** established the HumanEval code synthesis benchmark, but assumed English prompts and heavy cloud compute.*  
  * *Second, **Hui et al. (Qwen2.5-Coder, 2024)** demonstrated state-of-the-art open-source code generation in compact sizes like 1.5B, but lacked localized dialect prompt wrappers.*  
  * *Third, **Tiwary & Kumar (ACM, 2022)** surveyed Indian code-mixing and transliteration challenges, identifying the phonetic patterns we leveraged.*  
  * *Fourth, **Pedregosa et al. (Scikit-learn, 2011)** provided the fast, sub-millisecond TF-IDF and linear classification algorithms powering our offline intent classifier."*

---

### Slide 5 — Research Gap & Proposed Solution
* **What to say:**  
  *"The research gap is clear: Existing commercial tools are cloud-dependent, English-centric, expensive, and unverified. General LLMs hallucinate syntax on incomplete outputs and provide no educational structure.*  
  *Bhasha2Code bridges this gap through four contributions: an offline bilingual NLP pipeline, local zero-cost CPU inference, compiler-level AST verification, and an educational **Study Mode** providing algorithms, ASCII flowcharts, and viva questions alongside code."*

---

### Slide 6 — Proposed System & Major Features
* **What to say:**  
  *"The system delivers six core functional capabilities:*  
  * *1. Code-Mixed chat handling queries like 'Python madhye factorial kadha'.*  
  * *2. Dual Pedagogical Modes: Normal Mode for fast code generation, and Study Mode for exam/concept preparation.*  
  * *3. Automated AST Syntax Validation badging code as 'Validated' before rendering.*  
  * *4. Ephemeral Docker Sandbox execution capping memory to 512MB and disabling network access.*  
  * *5. Multi-turn context memory retaining historical code artifacts in SQLite.*  
  * *6. Fast asynchronous REST and SSE streaming APIs with complete OpenAPI documentation."*

---

### Slide 7 — System Architecture
* **What to say (Point to the 4 tiers):**  
  *"Looking at our system architecture:*  
  * *In the **Presentation Tier**, the React 18 SPA communicates over HTTP and Server-Sent Events (SSE) for real-time token streaming.*  
  * *In the **NLP & Gateway Tier**, FastAPI routes the input through Unicode NFC preprocessing, language detection, and our 18-class intent classifier. The Prompt Builder then structures the prompt according to strict safety and code-preservation policies.*  
  * *In the **Inference Tier**, the local Ollama daemon streams tokens from the quantized Qwen2.5-Coder:1.5B model.*  
  * *Finally, in the **Validation & Sandbox Tier**, our AST engine verifies syntax, and if the user clicks 'Run', an isolated Docker container executes the code safely, returning output to the terminal."*

---

### Slide 8 — NLP Methodology
* **What to say:**  
  *"This slide details our core NLP methodology in five sequential stages:*  
  * *1. Preprocessing: Unicode NFC normalization harmonizes Devanagari and Latin characters while separating natural language text from code blocks.*  
  * *2. Language Detection: Evaluates Devanagari script ratios and sub-word n-grams for Romanized Marathi patterns.*  
  * *3. Feature Extraction: We use a Feature Union combining word n-grams (1,2) and character n-grams (3,5) with sublinear TF scaling, creating a 496-dimensional sparse matrix.*  
  * *4. Multi-Class Classification: A calibrated Logistic Regression model classifies 18 intents and 4 pragmatic tones.*  
  * *5. Prompt Synthesis: Enforces the 'Code Preservation Mandate', ensuring keywords remain in ASCII English while explanations match the detected regional dialect."*

---

### Slide 9 — Technology Stack & Implementation
* **What to say:**  
  *"Our entire technology stack is 100% open-source and locally hosted:*  
  * *Frontend: React 18, Vite, and Tailwind CSS with Monaco/Prism syntax highlighting.*  
  * *Backend: Python 3.11 with FastAPI and Pydantic v2 schemas for strict data contracts.*  
  * *NLP: Scikit-learn and joblib for fast sub-millisecond intent classification.*  
  * *LLM: Ollama running Qwen2.5-Coder:1.5B (986 MB).*  
  * *Storage & Security: SQLite 3 for sessions and Docker for sandbox containment.*  
  * *Every technology shown here is verified and actively running in the project."*

---

### Slide 10 — Experimental Results, KPIs & Verification
* **What to say (Direct attention to the Confusion Matrix):**  
  *"Here are our verified empirical results:*  
  * *1. **NLP Evaluation:** Evaluated on 162 unseen test samples from our 1,080-sample dataset, our intent classifier achieved **92.59% Test Accuracy**, with a **Macro Precision of 0.9301**, **Macro Recall of 0.9259**, and **Macro F1-Score of 0.9239**.*  
  * *2. **Throughput:** On consumer CPU hardware, the 1.5B model achieves **16.54 tokens/sec** with response latency between 12–15 seconds, representing a 2.3x speedup over the 3B model.*  
  * *3. **AST Validity:** 93.2% of generated Python code blocks passed AST parsing without syntax errors.*  
  * *4. **Software Tests:** All **490 out of 490 backend tests** passed via pytest, and 15 out of 15 frontend tests passed via vitest."*

---

### Slide 11 — Conclusion, Limitations & Future Scope
* **What to say:**  
  *"In conclusion, Bhasha2Code proves that offline NLP pipelines combined with compact quantized LLMs can successfully democratize coding education for bilingual students at zero recurring cost.*  
  *Regarding current limitations: CPU inference latency takes 12–15 seconds, and token budget is capped at 8,192 tokens.*  
  *For future work, we plan to integrate open-source Speech-to-Text (such as AI4Bharat Bhashini or Whisper) for voice coding, expand lexical dictionaries to south Indian languages, and build interactive algorithmic animation tools."*

---

### Slide 12 — References
* **What to say:**  
  *"Finally, here are our verified academic references cited in IEEE format, including the OpenAI Codex benchmark, the Qwen2.5-Coder technical report, ACM surveys on code-mixing, Scikit-learn documentation, and FastAPI specifications.*  
  *Thank you, respected examiners. I am now ready for the technical viva and live demonstration."*
