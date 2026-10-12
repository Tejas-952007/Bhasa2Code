# A PROJECT REPORT ON
# BHASHA2CODE: AN OFFLINE-FIRST MULTILINGUAL NATURAL LANGUAGE-TO-CODE GENERATION, DEBUGGING AND EXPLANATION ASSISTANT

---

## TITLE PAGE

**PROJECT REPORT ON**  
### **BHASHA2CODE: AN OFFLINE-FIRST MULTILINGUAL NATURAL LANGUAGE-TO-CODE GENERATION, DEBUGGING AND EXPLANATION ASSISTANT**

*Submitted in partial fulfillment of the requirements for the degree of*  
**BACHELOR OF ENGINEERING IN ARTIFICIAL INTELLIGENCE & DATA SCIENCE / COMPUTER ENGINEERING**  
*Under Savitribai Phule Pune University (SPPU)*

<br>

**Submitted by:**  
**Tejas Ingle** (PRN: `[Student PRN]` / Seat No: `[Student Seat Number]`)  
*(Optional Team Members Placeholder: [Student Name 2], [Student Name 3])*

<br>

**Under the Guidance of:**  
**Prof. Gajanan Godage**  
*Assistant Professor, Department of Computer Engineering*

<br>

**DEPARTMENT OF COMPUTER ENGINEERING / ARTIFICIAL INTELLIGENCE & DATA SCIENCE**  
**NUTAN MAHARASHTRA INSTITUTE OF ENGINEERING & TECHNOLOGY (NMIET)**  
*Samarth Vidya Sankul, Vishnupuri, Talegaon Dabhade, Pune – 410507*  
**ACADEMIC YEAR: 2025 – 2026**

---

## BONAFIDE CERTIFICATE

This is to certify that the engineering mini-project report entitled **"Bhasha2Code: An Offline-First Multilingual Natural Language-to-Code Generation, Debugging and Explanation Assistant"** submitted by **Tejas Ingle** (PRN: `[Student PRN]`) is a bonafide record of work carried out under my supervision and guidance, in partial fulfillment of the requirements for the award of the degree of Bachelor of Engineering in Computer Engineering / Artificial Intelligence & Data Science by Savitribai Phule Pune University (SPPU) during the academic year 2025–2026.

To the best of our knowledge, the matter embodied in this report has not been submitted to any other University or Institution for the award of any degree or diploma.

<br><br><br>

-------------------------------------------------- &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; --------------------------------------------------  
**Prof. Gajanan Godage** &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **Head of Department (HOD)**  
*Project Guide* &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *Department of Computer Engineering*  
*Department of Computer Engineering* &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *NMIET, Talegaon, Pune*  
*NMIET, Talegaon, Pune*  

<br><br>

-------------------------------------------------- &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; --------------------------------------------------  
**Internal Examiner** &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **External Examiner**  

**Date:** `____ / ____ / 2026`  
**Place:** Pune  

---

## ACKNOWLEDGMENT

I wish to express my deepest gratitude and sincere appreciation to my project guide, **Prof. Gajanan Godage**, Department of Computer Engineering, Nutan Maharashtra Institute of Engineering & Technology (NMIET), Pune, for his inspiring guidance, invaluable academic feedback, continuous encouragement, and technical suggestions throughout the conceptualization, system architecture, testing, and documentation stages of this project.

I extend my sincere thanks to the **Head of the Department**, for providing state-of-the-art computational infrastructure, computing laboratories, and an inspiring academic atmosphere that facilitated the development of this research project.

I am also profoundly thankful to our respected **Principal** and the management of Nutan Maharashtra Institute of Engineering & Technology, Talegaon Dabhade, Pune, for their persistent institutional support and encouragement.

Finally, I convey my heartfelt appreciation to my family, peers, and the global open-source AI and software engineering communities whose resources, open models, and libraries made this work possible.

<br>
**Tejas Ingle**  
*PRN: [Student PRN]*  
*Department of Computer Engineering, NMIET Pune*

---

## ABSTRACT

In India's technical education landscape, a substantial majority of undergraduate engineering students conceptualize programming algorithms and computational logic in regional vernacular languages such as Marathi and Hindi. However, commercial state-of-the-art AI programming assistants (e.g., OpenAI ChatGPT, GitHub Copilot) are fundamentally English-centric, cloud-dependent, computationally expensive, and lack pedagogical scaffolding. When students interact using code-mixed colloquial dialects (e.g., *"Python madhe factorial sathi loop kasa lavu?"*), commercial models frequently misinterpret syntax imperatives or return unverified code snippets lacking explanatory depth.

To bridge this linguistic and pedagogical divide, this project introduces **Bhasha2Code**, an offline, privacy-first multilingual AI coding assistant and educational execution sandbox. Bhasha2Code integrates a custom modular Natural Language Processing (NLP) pipeline capable of classifying code-mixed Marathi-English and Hindi-English prompts across 18 distinct programming intents with **92.59% accuracy**. For local inference, the system orchestrates a 4-bit quantized open-weights Large Language Model (**Qwen2.5-Coder:1.5B/3B**) hosted locally via Ollama, operating with zero external API fees and zero recurring cloud costs on consumer-grade CPU hardware.

To eradicate code hallucinations and unsafe outputs, Bhasha2Code implements a dual-mode workspace: a **Developer Mode** for streamlined code generation and an educational **Study Mode** delivering ISO-standard flowcharts, step-by-step algorithms, line-by-line walkthroughs, and automated viva-voce questions. All generated code undergoes deterministic Abstract Syntax Tree (AST) compilation verification and executes within isolated, resource-capped Docker sandboxes (restricted to 256MB RAM, 0.5 CPU, no network access). Experimental evaluation across 541 backend automated test cases and 20 frontend verification tests demonstrates sub-second intent classification, strict preservation of standard English ASCII programming keywords, and robust learning outcomes for non-native English engineering students.

**Keywords:** Multilingual Code Generation, Code-Mixed NLP, Local LLMs, Abstract Syntax Tree Validation, Educational Technology, Docker Sandbox.

---

## TABLE OF CONTENTS

| Chapter / Section | Title | Page No. |
| :--- | :--- | :--- |
| | **Title Page** | i |
| | **Bonafide Certificate** | ii |
| | **Acknowledgment** | iii |
| | **Abstract** | iv |
| | **Keywords** | iv |
| | **Table of Contents** | v |
| | **List of Figures** | vii |
| | **List of Tables** | viii |
| **Chapter 1** | **Introduction** | **1** |
| 1.1 | Project Background & Context | 1 |
| 1.2 | The Indian Engineering Context | 2 |
| 1.3 | Overview of Bhasha2Code | 3 |
| 1.4 | Report Organization | 4 |
| **Chapter 2** | **Problem Statement and Motivation** | **5** |
| 2.1 | Formal Problem Statement | 5 |
| 2.2 | Key Challenges in Existing Paradigms | 5 |
| 2.3 | Motivation | 7 |
| **Chapter 3** | **Aim and Objectives** | **8** |
| 3.1 | Project Aim | 8 |
| 3.2 | Specific Measurable Objectives | 8 |
| 3.3 | Scope and Boundaries | 9 |
| **Chapter 4** | **Literature Review and Existing-System Analysis** | **10** |
| 4.1 | Evolution of Code Generation Models | 10 |
| 4.2 | Code-Mixing and Low-Resource NLP in India | 11 |
| 4.3 | Local Quantized Inference on Consumer Hardware | 12 |
| 4.4 | Sandboxed Code Execution and AST Validation | 13 |
| 4.5 | Comparative Analysis and Research Gap | 14 |
| **Chapter 5** | **Proposed System** | **16** |
| 5.1 | Proposed System Philosophy | 16 |
| 5.2 | High-Level Architecture Overview | 16 |
| 5.3 | Key Innovations | 18 |
| **Chapter 6** | **System Requirements** | **20** |
| 6.1 | Hardware Requirements | 20 |
| 6.2 | Software and Library Requirements | 20 |
| 6.3 | Network and Runtime Dependencies | 21 |
| **Chapter 7** | **System Architecture and Module Design** | **22** |
| 7.1 | Tier 1: Frontend Client Workspace | 22 |
| 7.2 | Tier 2: Backend API and Context Orchestrator | 23 |
| 7.3 | Tier 3: Deterministic Offline NLP Pipeline | 24 |
| 7.4 | Tier 4: Prompt Engine and LLM Service | 26 |
| 7.5 | Tier 5: AST Syntax Validation Engine | 27 |
| 7.6 | Tier 6: Ephemeral Docker Sandbox | 28 |
| 7.7 | Database Schema Design (SQLite & SQLAlchemy) | 29 |
| **Chapter 8** | **Methodology and Algorithms** | **31** |
| 8.1 | End-to-End Execution Workflow | 31 |
| 8.2 | Text Preprocessing and Code Stripping Algorithm | 32 |
| 8.3 | Deterministic Language Detection with Homograph Disambiguation | 33 |
| 8.4 | TF-IDF Vectorization and Logistic Regression Classifier | 34 |
| 8.5 | Prompt Construction and Code Preservation Policy | 36 |
| 8.6 | AST Validation and Diagnostic Parsing | 37 |
| 8.7 | Educational Scaffolding and Flowchart Synthesis | 38 |
| **Chapter 9** | **Implementation Details** | **40** |
| 9.1 | Development Environment Setup | 40 |
| 9.2 | Backend Implementation (FastAPI & Async Streaming) | 41 |
| 9.3 | NLP Model Training and Persistence | 42 |
| 9.4 | Local LLM Integration via Ollama | 43 |
| 9.5 | Docker Container Runtime Implementation | 44 |
| 9.6 | Frontend Implementation (React, SSE & Visual Flowchart) | 45 |
| **Chapter 10** | **Testing and Results** | **47** |
| 10.1 | Testing Methodology and Test Suites | 47 |
| 10.2 | NLP Classification Accuracy Results | 48 |
| 10.3 | AST Validation Performance | 50 |
| 10.4 | Sandbox Security and Execution Verification | 51 |
| 10.5 | Generation Latency and Token Throughput | 52 |
| 10.6 | End-to-End Case Studies | 53 |
| **Chapter 11** | **Security, Privacy, and Limitations** | **55** |
| 11.1 | Threat Model and Security Boundaries | 55 |
| 11.2 | Data Sovereignty and Offline Privacy | 56 |
| 11.3 | System Limitations | 57 |
| **Chapter 12** | **Applications** | **58** |
| 12.1 | Academic Laboratories and Computer Science Pedagogy | 58 |
| 12.2 | Regional Engineering Colleges and Rural Institutions | 58 |
| 12.3 | Air-Gapped and Confidential Software Development | 59 |
| **Chapter 13** | **Future Scope** | **60** |
| 13.1 | Multimodal Voice/Speech Integration | 60 |
| 13.2 | Extension to Additional Indian Languages | 60 |
| 13.3 | Fine-Tuning on Academic Curricula | 61 |
| 13.4 | Visual Interactive Algorithm Debugger | 61 |
| **Conclusion** | | **62** |
| **References** | | **63** |
| **Appendix** | | **66** |
| Appendix A | Sample Prompts and System Outputs | 66 |
| Appendix B | API Endpoints Specification | 67 |
| Appendix C | Setup and Installation Manual | 69 |

---

## LIST OF FIGURES

* **Figure 5.1:** Overall System Architecture of Bhasha2Code
* **Figure 7.1:** Modular Component Flowchart of the Backend Orchestration Tier
* **Figure 7.2:** Database Entity-Relationship Diagram (ERD)
* **Figure 8.1:** End-to-End Sequence Diagram from User Input to Sandboxed Execution
* **Figure 8.2:** Four-Stage Offline NLP Pipeline Architecture
* **Figure 9.1:** Visual Flowchart SVG Rendering in Study Mode
* **Figure 10.1:** Confusion Matrix for 18-Class Intent Classifier

---

## LIST OF TABLES

* **Table 4.1:** Comparative Analysis of Bhasha2Code vs. Commercial Assistants
* **Table 6.1:** Minimum and Recommended Hardware Specifications
* **Table 6.2:** Software Versions and Environment Dependencies
* **Table 7.1:** Database Models and Relational Attributes
* **Table 10.1:** Intent Classifier Per-Class Performance on Held-Out Test Set
* **Table 10.2:** Tone Classifier Confusion Matrix and Metrics
* **Table 10.3:** Test Suite Summary and Pass Rates
* **Table 10.4:** Local LLM Generation Latency on Consumer CPU

---

# CHAPTER 1: INTRODUCTION

### 1.1 Project Background & Context
The emergence of Large Language Models (LLMs) specialized in software development—such as OpenAI Codex, GitHub Copilot, and Meta CodeLlama—has transformed computing. Programmers can now generate complete algorithms, resolve subtle syntax bugs, and translate paradigms across programming languages through conversational interaction.

However, the benefits of these generative AI systems remain disproportionately concentrated among fluent, native English speakers. Code generation benchmarks (such as HumanEval and MBPP) evaluate models exclusively using formal English prompts. When applied to real-world educational contexts outside Western economies, these tools exhibit severe linguistic, economic, and architectural disconnects.

### 1.2 The Indian Engineering Context
India produces hundreds of thousands of computer science and IT engineering graduates annually across thousands of technical institutions, notably across Tier-2 and Tier-3 cities in states such as Maharashtra, Karnataka, and Uttar Pradesh. For an overwhelming majority of these students, English is a secondary language acquired through formal schooling, rather than their first thinking language.

Cognitive science demonstrates that intuitive algorithmic problem-solving occurs predominantly in an individual's mother tongue. When a student learns concepts such as recursion, tree traversal, or dynamic programming, they mentally construct the logical flow in regional dialects (such as Marathi or Hindi) before translating that logic into programming code. Compelling these students to formulate complex technical queries in formal English introduces an extraneous cognitive barrier that impedes core algorithmic comprehension.

Furthermore, commercial solutions introduce substantial systemic challenges:
1. **Economic Inequity:** Subscriptions for ChatGPT Plus or GitHub Copilot ($10–$20/month, approx. ₹850–₹1,700/month) represent prohibitive recurring costs for students.
2. **Infrastructure Dependency:** Commercial tools require continuous, high-bandwidth internet connectivity, which is frequently unavailable in rural or air-gapped college laboratories.
3. **Data Privacy and Sovereignty:** Academic project code, proprietary scripts, and student queries are transmitted to offshore servers.
4. **Lack of Pedagogical Scaffolding:** Commercial tools optimize for productivity and brevity, returning raw code snippets without explaining step-by-step logic, complexity trade-offs, or viva-voce questions required for academic examinations.

### 1.3 Overview of Bhasha2Code
To address these challenges, **Bhasha2Code** was engineered as an offline-first, privacy-preserving AI coding assistant and educational execution sandbox. The system combines lightweight deterministic NLP classifiers, an open-weights local LLM, multi-language Abstract Syntax Tree (AST) validation, and isolated Docker container execution into a unified local workspace.

### 1.4 Report Organization
This report is structured into 13 formal chapters detailing problem definition, literature review, architectural design, mathematical methodology, implementation, experimental evaluation, security, and future work.

---

# CHAPTER 2: PROBLEM STATEMENT AND MOTIVATION

### 2.1 Formal Problem Statement
*"To design, implement, and evaluate an offline-first, zero-recurring-cost programming assistant that accurately detects linguistic intent from code-mixed Indian vernacular prompts (Marathi, Hindi, Hinglish, Marathi-English), synthesizes syntactically verifiable source code using local open-weights LLMs, and provides sandboxed runtime validation and curriculum-focused pedagogical explanations (Study Mode) on consumer-grade hardware."*

### 2.2 Key Challenges in Existing Paradigms
1. **Phonetic and Transliteration Ambiguity:** Indian users frequently communicate using Romanized script (typing Marathi or Hindi using English alphabet keys). Words such as `madhe`, `kadh`, `banav`, or `kaise` exhibit non-standardized phonetic spellings across dialects.
2. **Lexical Collisions (Homographs):** Words written in Latin script may have conflicting meanings across English and Indic languages. For example, the token *"the"* represents the common English definite article, but also represents the Hindi auxiliary verb *"the"* (थे). Naive tokenizers misclassify such inputs.
3. **Small Model Steering Deficiencies:** Lightweight local models (1.5B–3B parameters) deployed on local CPUs are prone to instruction drift if prompted with conversational code-mixed inputs, frequently hallucinating non-English variable names (e.g., `sankhya = 10` instead of `number = 10`).
4. **Execution Hazards:** Executing unvetted AI-generated code directly on student machines creates security risks (e.g., filesystem deletion, fork bombs, resource exhaustion).

### 2.3 Motivation
The primary motivation behind Bhasha2Code is to democratize computing education by providing a localized, offline, zero-cost programming mentor that aligns with the National Education Policy (NEP 2020) vision of promoting regional languages in technical higher education.

---

# CHAPTER 3: AIM AND OBJECTIVES

### 3.1 Project Aim
To develop a self-contained, offline multilingual coding assistant that accepts code-mixed regional language requests, generates verified source code, provides curriculum-aligned pedagogical explanations, and executes code safely within an isolated environment.

### 3.2 Specific Measurable Objectives
1. **Develop an Offline 4-Stage NLP Pipeline:** Build a deterministic preprocessing and classification pipeline executing in under 5 ms on CPU to classify 6 language variants, 6 tones, and 18 software engineering intents with >90% precision.
2. **Local Model Orchestration:** Deploy a 4-bit quantized open-source coding LLM (`Qwen2.5-Coder:1.5B/3B`) via Ollama with zero external API fees, sub-second TTFT, and a large context window (8192 tokens).
3. **Code Preservation Mandate:** Implement system prompt policies guaranteeing that code syntax, keywords, and identifiers remain strictly in standard English ASCII characters, while explanatory prose adapts to the student's dialect.
4. **Abstract Syntax Tree (AST) Validation:** Implement multi-language static syntax analysis (Python, JS, Java, C, C++, SQL) to intercept syntax errors before code presentation.
5. **Sandboxed Code Execution:** Engineer an ephemeral Docker sandbox capping memory (256MB), CPU (0.5 cores), and process count (64 PIDs) with total network denial (`--network none`) and automatic resource reclamation.
6. **Academic Study Mode Scaffolding:** Implement automated deconstruction of programming solutions into ISO-standard flowcharts, step-by-step algorithms, complexity metrics, and curriculum viva-voce Q&A pairs.
7. **Local State Persistence:** Implement full local session management, message history, notes, and code artifact storage using SQLite and SQLAlchemy.

### 3.3 Scope and Boundaries
* **Supported Prompt Languages:** English, Hindi, Marathi, Hinglish, Marathi-English, Hindi-English.
* **Supported Programming Languages:** Python 3, C, C++, Java, JavaScript, and ANSI SQL.
* **Target Hardware:** Standard consumer laptops with quad-core CPUs and 8GB to 16GB RAM, requiring no dedicated GPU.
* **Excluded Scope:** Voice/audio processing (deferred to future work), multi-user cloud authentication, distributed cloud hosting.

---

# CHAPTER 4: LITERATURE REVIEW AND EXISTING-SYSTEM ANALYSIS

### 4.1 Evolution of Code Generation Models
In 2021, Chen et al. introduced **OpenAI Codex**, a 12-billion parameter model fine-tuned on public GitHub repositories, creating the foundation for GitHub Copilot. Codex proved that autoregressive transformers could generate functioning code from natural language docstrings. However, Codex operated exclusively as a cloud API and was evaluated exclusively on monolingual English benchmarks.

Rozière et al. (2023) developed **Code Llama**, demonstrating that domain-specific code pretraining on large token volumes substantially improves syntax accuracy. However, Code Llama models required 7B to 34B parameters, demanding high-end GPUs exceeding the reach of consumer student laptops.

### 4.2 Code-Mixing and Low-Resource NLP in India
Tiwary and Kumar (2022) surveyed linguistic challenges in Indian code-mixed NLP, observing that phonetic transliteration creates immense lexical variance. Unlike monolingual text, code-mixed Romanized Indic text lacks standardized spellings. Traditional cross-lingual transformer models like mBERT or XLM-RoBERTa require substantial computational memory and introduce latency unviable for offline CPU inference.

### 4.3 Local Quantized Inference on Consumer Hardware
Hui et al. (2024) released **Qwen2.5-Coder**, showing that compact models (1.5B and 3B parameters) trained on over 5.5 trillion code tokens achieve competitive performance on HumanEval (exceeding 70% pass@1) comparable to much larger earlier models. Through 4-bit integer quantization (GGUF format via llama.cpp and Ollama), inference memory requirements drop below 1 GB RAM, enabling fast execution on standard x86_64 CPUs.

### 4.4 Sandboxed Code Execution and AST Validation
Executing arbitrary LLM-generated code presents critical risks. Becker et al. (2023) documented that students frequently execute hallucinated code containing destructive operations or infinite loops. Operating system-level process constraints (e.g., POSIX `setrlimit`) fail to provide filesystem virtualization. Containerization via Docker (Merkel, 2014) provides robust kernel namespace and cgroup isolation when configured with read-only root filesystems and disabled networking.

### 4.5 Comparative Analysis and Research Gap

**Table 4.1: Comparative Analysis**
| Evaluation Dimension | GitHub Copilot | OpenAI ChatGPT | Local CodeLlama (7B) | **Bhasha2Code** |
| :--- | :--- | :--- | :--- | :--- |
| **Romanized Indic Support** | Poor / Unpredictable | Inconsistent | Fails without fine-tuning | **Custom Lexical & Rule Pipeline** |
| **Offline Functionality** | No (Cloud Only) | No (Cloud Only) | Yes (Requires GPU) | **100% Offline (Runs on CPU)** |
| **Cost to Student** | $10–$20 / month | $20 / month | Free (Heavy hardware) | **₹0 / 100% Free & Open** |
| **Code Validation** | None | None | None | **Pre-Render AST Syntax Parsing** |
| **Execution Security** | None (Runs on host) | Cloud E2B Sandbox | Unrestricted host OS | **Ephemeral Docker Sandbox** |
| **Pedagogical Scaffolding**| Code only | Unstructured text | Code only | **Study Mode (Flowchart + Viva)** |

---

# CHAPTER 5: PROPOSED SYSTEM

### 5.1 Proposed System Philosophy
Bhasha2Code is designed around the principle of **Intelligent Preprocessing + Local Steering + Sandboxed Verification**. Rather than treating the LLM as an unconstrained black box, Bhasha2Code surrounds the model with deterministic NLP classifiers, strict prompt policies, static AST validators, and container isolation.

### 5.2 High-Level Architecture Overview
The system follows a three-tier decoupled client-server architecture:
1. **Frontend Presentation Tier:** React 18, Vite, Monaco Editor, Lucide React, and Server-Sent Events (SSE) listener.
2. **Backend Orchestration Tier:** FastAPI, SQLite database via SQLAlchemy, 4-stage offline NLP pipeline, and Prompt Engine.
3. **Local Inference and Execution Tier:** Ollama daemon (`qwen2.5-coder`), AST syntax validators, and Docker container sandbox.

```
                      ┌──────────────────────────────────────────────┐
                      │              STUDENT USER                    │
                      └──────────────────────┬───────────────────────┘
                                             │ Code-Mixed Prompt
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │       React 18 + Vite Web Workspace          │
                      │  (Chat Stream, Monaco Editor, Live Terminal) │
                      └──────────────────────┬───────────────────────┘
                                             │ HTTP / SSE Stream
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │            FastAPI Backend Gateway           │
                      ├──────────────────────────────────────────────┤
                      │  [Stage 1] Text Preprocessor (NFC & Split)   │
                      │  [Stage 2] Language Detector (Lexical Rules) │
                      │  [Stage 3] Tone Classifier (TF-IDF + SGD)    │
                      │  [Stage 4] Intent Classifier (18-Class ML)   │
                      ├──────────────────────────────────────────────┤
                      │  Context Manager (SQLite Sliding History)    │
                      │  Prompt Builder (Code Preservation Mandate)  │
                      └──────────────────────┬───────────────────────┘
                                             │ Local REST API
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │         Local Ollama Inference Daemon        │
                      │    (Model: Qwen2.5-Coder:1.5B / 3B GGUF)     │
                      └──────────────────────┬───────────────────────┘
                                             │ Streamed Tokens
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │      AST Syntax Validation Engine            │
                      │     (Python ast.parse & Lexical Parsers)     │
                      └──────────────┬───────────────────────────────┘
                                     │ Validated Code
                                     ▼
                      ┌──────────────────────────────────────────────┐
                      │      Isolated Ephemeral Docker Sandbox       │
                      │  (256MB RAM, 0.5 CPU, --network none, UID)   │
                      └──────────────────────────────────────────────┘
```

### 5.3 Key Innovations
1. **Code Preservation Mandate:** Enforces that programming keywords (`def`, `class`, `for`, `while`) remain strictly in English ASCII, while explanatory text mirrors the student's regional dialect.
2. **Two-Tier AI Architecture:** Decouples lightweight internal NLP classification (~8 ms full pipeline, 1.2–4.0 ms per classifier) from generative LLM inference, ensuring fast prompt formulation.
3. **Study Mode Pedagogical Decomposition:** Automatically deconstructs solutions into structured algorithmic steps, interactive visual flowcharts, and curriculum viva questions.
4. **AST Compilation Verification:** Verifies generated code before presentation to eliminate syntax hallucinations.

---

# CHAPTER 6: SYSTEM REQUIREMENTS

### 6.1 Hardware Requirements

**Table 6.1: Hardware Specifications**
| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **Processor (CPU)** | Intel Core i3 / AMD Ryzen 3 (4 Cores) | Intel Core i5 / AMD Ryzen 5 (6+ Cores) |
| **System Memory (RAM)** | 8 GB DDR4 | 16 GB DDR4 / DDR5 |
| **Storage (Disk)** | 10 GB available SSD space | 20 GB NVMe SSD space |
| **GPU** | Not required (CPU-only execution) | Integrated Intel Iris Xe or AMD Radeon |
| **Display** | 1366 x 768 resolution | 1920 x 1080 resolution |

### 6.2 Software Requirements

**Table 6.2: Software Environment**
| Software Layer | Specification / Version |
| :--- | :--- |
| **Operating System** | Ubuntu 22.04 LTS, Debian 12, or Windows 11 with WSL2 |
| **Backend Runtime** | Python 3.11.x |
| **Web Framework** | FastAPI 0.115.0+, Uvicorn 0.30.0+ |
| **Machine Learning** | scikit-learn 1.5.0+, NumPy 1.26.0+, Joblib 1.4.0+ |
| **Database** | SQLite 3.37+, SQLAlchemy 2.0.35+ |
| **Frontend Runtime** | Node.js v18.18+ / v20.x, npm 9.x+ |
| **Frontend Framework** | React 18.3.1, Vite 5.4.2 |
| **LLM Inference Engine** | Ollama v0.3.0+ (running `qwen2.5-coder:1.5b` or `3b`) |
| **Container Engine** | Docker Engine 24.0+ / 27.0+ |

---

# CHAPTER 7: SYSTEM ARCHITECTURE AND MODULE DESIGN

### 7.1 Tier 1: Frontend Client Workspace
The frontend is constructed using React 18 and Vite. It contains:
- `AppShell.jsx`: Main navigation layout with dual-mode toggle (Developer Mode vs. Study Mode).
- `ChatStream.jsx`: Handles real-time Server-Sent Events (SSE) token consumption using `fetch` and `ReadableStreamDefaultReader`.
- `CodeArtifact.jsx`: Renders code blocks with syntax highlighting, copy buttons, AST validation badges, and run triggers.
- `VisualFlowchart.jsx`: Renders structured SVG algorithm flowcharts.
- `InteractiveTerminal.jsx`: WebSocket-based terminal viewer displaying container execution output and accepting interactive stdin.

### 7.2 Tier 2: Backend API and Context Orchestrator
FastAPI exposes structured endpoints under `/api/v1`:
- `POST /chat/stream`: Main streaming chat endpoint orchestrating NLP analysis, prompt generation, LLM streaming, AST validation, and response assembly.
- `POST /code/validate`: Static syntax validation endpoint.
- `POST /code/run`: Ephemeral Docker sandbox execution endpoint.
- `WebSocket /code/interactive-run`: Interactive terminal session execution.
- `GET/POST /sessions`: CRUD management of chat sessions and history.

### 7.3 Tier 3: Deterministic Offline NLP Pipeline
The pipeline executes sequentially in `backend/app/nlp/pipeline/nlp_pipeline.py`:
1. **`TextPreprocessor`:** Normalizes Unicode via NFC, extracts fenced code, strips raw code, and isolates clean conversational queries.
2. **`LanguageDetector`:** Analyzes Devanagari script ratios and evaluates dictionary lookups for Hindi and Marathi roots with homograph disambiguation.
3. **`ToneClassifier`:** Classifies conversational style into 6 tones using TF-IDF and Logistic Regression.
4. **`IntentClassifier`:** Maps the user request to one of 18 programming intents.

### 7.4 Tier 4: Prompt Engine and LLM Service
The `PromptBuilder` formats the payload:
- Injects detected language, tone, and intent.
- Appends past conversation history and relevant code blocks from the database.
- Enforces the Code Preservation Mandate and Study Mode formatting templates.
- Dispatches the payload to `LLMService`, which manages the local Ollama connection.

### 7.5 Tier 5: AST Syntax Validation Engine
The `ResponseValidator` processes raw LLM markdown output:
- Extracts code blocks using regex.
- Passes Python code to Python's built-in `ast.parse()`.
- Validates C/C++, Java, JavaScript, and SQL using lexical validators.
- Attaches diagnostics (severity, message, line number) to the artifact.

### 7.6 Tier 6: Ephemeral Docker Sandbox
The `DockerRuntime` manages the container lifecycle:
- Builds a tar archive of source files in memory.
- Spawns an isolated container from `bhasha2code-sandbox-python:1.0.0` or language-specific images.
- Enforces cgroup limits (256MB RAM, 0.5 CPU, `--network none`).
- Captures stdout/stderr up to 64 KB and enforces a 3.0-second timeout.
- Automatically cleans up containers and volumes.

### 7.7 Database Schema Design (SQLite & SQLAlchemy)

**Table 7.1: Database Entities**
| Model Name | Table Name | Key Attributes | Description |
| :--- | :--- | :--- | :--- |
| `User` | `users` | `id`, `username`, `created_at` | Local user identity |
| `Session` | `sessions` | `id`, `user_id`, `title`, `current_language`, `status` | Chat & study sessions |
| `Message` | `messages` | `id`, `session_id`, `role`, `content`, `detected_language`, `intent`, `tone` | Conversation turns |
| `GeneratedCode`| `generated_codes` | `id`, `session_id`, `message_id`, `code`, `language`, `validation_status` | Synthesized code blocks |
| `Note` | `notes` | `id`, `session_id`, `title`, `content` | Student study notes |
| `SavedMessage` | `saved_messages`| `id`, `user_id`, `message_id`, `tags` | Bookmarked solutions |
| `DebugHistory` | `debug_histories` | `id`, `session_id`, `original_code`, `fixed_code`, `error_type` | Debugging logs |

---

# CHAPTER 8: METHODOLOGY AND ALGORITHMS

### 8.1 End-to-End Execution Workflow
1. **User Submission:** The student enters a prompt (e.g., *"Python madhe binary search samjhava"*).
2. **Text Preprocessing:** The backend normalizes Unicode and segregates code from natural language text.
3. **Language Detection:** The system evaluates lexical patterns and classifies the language as `MARATHI_ENGLISH`.
4. **Tone & Intent Classification:** The tone classifier outputs `DETAILED` and the intent classifier outputs `ALGORITHM`.
5. **Context Assembly:** The context manager retrieves previous conversation messages from SQLite.
6. **Prompt Synthesis:** The prompt engine synthesizes instructions enforcing English code keywords and Marathi-English explanations.
7. **Local LLM Inference:** Ollama streams tokens from `qwen2.5-coder:1.5b`.
8. **AST Validation:** The response validator parses the code block via `ast.parse()`, marking it `VALID`.
9. **Pedagogical Deconstruction:** The response parser extracts problem summary, algorithm steps, flowchart nodes, and viva questions.
10. **Client Display & Execution:** The frontend streams the response, displays the visual flowchart, and allows one-click sandbox execution.

### 8.2 Text Preprocessing and Code Stripping Algorithm
```python
def preprocess(raw_input: str) -> PreprocessedText:
    # 1. Unicode NFC Normalization
    normalized = unicodedata.normalize("NFC", raw_input)
    # 2. Extract fenced code blocks
    code_blocks = extract_fenced_blocks(normalized)
    text_without_code = strip_code_blocks(normalized)
    # 3. Clean whitespace
    clean_text = clean_whitespace(text_without_code)
    return PreprocessedText(normalized_text=clean_text, code_blocks=code_blocks)
```

### 8.3 Deterministic Language Detection with Homograph Disambiguation
The language detector counts Devanagari characters $N_{\text{dev}}$ and Latin characters $N_{\text{lat}}$. If $N_{\text{dev}} > 0$, it checks script ratios. If Latin, it searches unambiguous Indic word sets $S_{\text{mr}}$ and $S_{\text{hi}}$. For homographs (e.g., *"the"*, *"me"*), it evaluates surrounding tokens: if any unambiguous Indic token exists in the sentence, the homograph is resolved to Indic; otherwise, it resolves to English.

### 8.4 TF-IDF Vectorization and Logistic Regression Classifier
1. **Feature Extraction:**
   - Word unigrams and bigrams: $n \in [1, 2]$
   - Character n-grams within word boundaries: $n \in [3, 5]$, analyzer = `char_wb`
   - Sublinear term frequency: $w_{t,d} = 1 + \log(tf_{t,d})$ if $tf_{t,d} > 0$ else $0$
2. **Softmax Logistic Regression:**
   $$P(\text{Intent} = k \mid x) = \frac{\exp(w_k^T \cdot x + b_k)}{\sum_{j=1}^{18} \exp(w_j^T \cdot x + b_j)}$$
   Trained with $C = 3.0$, balanced class weights, and L-BFGS optimization.

### 8.5 Prompt Construction and Code Preservation Policy
The prompt builder injects explicit system instructions:
- **Rule 1:** All programming keywords, variable identifiers, function names, and syntax must strictly use standard English ASCII characters.
- **Rule 2:** All conversational explanations, walkthroughs, and comments must mirror the detected regional language.
- **Rule 3:** In Study Mode, generate exactly 5 sections: Problem Understanding, Algorithm, Flowchart, Code, and Viva Questions.

### 8.6 AST Validation and Diagnostic Parsing
For Python code:
```python
try:
    tree = ast.parse(code_string)
    status = ValidationStatus.VALID
except SyntaxError as exc:
    status = ValidationStatus.SYNTAX_ERROR
    diagnostics.append(Diagnostic(line=exc.lineno, col=exc.offset, message=exc.msg))
```

---

# CHAPTER 9: IMPLEMENTATION DETAILS

### 9.1 Development Environment Setup
The project was developed in Ubuntu 22.04 LTS using Python 3.11, Node.js 20, Vite 5, Ollama v0.3+, and Docker Engine 24.0.

### 9.2 Backend Implementation
FastAPI provides asynchronous request handling via `StreamingResponse`. The SSE endpoint formats events according to the SSE standard:
```text
event: token
data: {"type": "token", "token": "def "}

event: complete
data: {"type": "complete", "code": [...], "study": {...}}
```

### 9.3 NLP Model Training
Models were trained using Scikit-learn scripts (`scripts/train_intent_classifier.py` and `scripts/train_tone_classifier.py`) and serialized using Joblib into `models/intent/intent_classifier.joblib` and `models/tone/tone_classifier.joblib`.

### 9.4 Local LLM Integration
Ollama runs as a system daemon on port 11434. The model `qwen2.5-coder:1.5b` (Q4_K_M quantized) is loaded into RAM upon first invocation and kept resident for low-latency streaming.

### 9.5 Docker Sandbox Runtime
Containers are executed with `--rm -i --network none --cap-drop ALL --read-only --tmpfs /tmp:rw,noexec,size=64m --memory 256m --cpus 0.5 --pids-limit 64 --user 1000:1000`.

---

# CHAPTER 10: TESTING AND RESULTS

### 10.1 Testing Methodology and Test Suites
The system was verified using automated test suites across both backend and frontend layers:
- **Backend Test Suite (Pytest):** 567 test cases covering database operations, API routes, NLP pipelines, prompt generation, AST validation, and sandbox security.
- **Frontend Test Suite (Node Native Test Runner):** 20 tests verifying diagnostic parsing, debounce behavior, execution gating, flowchart rendering, and SSE streaming.

### 10.2 NLP Classification Accuracy Results

**Table 10.1: Intent Classifier Performance (Held-Out Test Set, 162 samples)**
| Metric | Value |
| :--- | :--- |
| **Overall Accuracy** | **92.59%** |
| **Macro F1-Score** | **92.39%** |
| **Weighted F1-Score** | **92.39%** |
| **Hinglish Subset Accuracy** | **100.00%** (30 / 30) |
| **Marathi-English Subset Accuracy**| **100.00%** (37 / 37) |
| **Hindi-English Subset Accuracy** | **100.00%** (20 / 20) |
| **Isolated Model Latency** | **2.8 ms** (Intent model alone; full 4-stage pipeline is **8.1 ms**) |

**Table 10.2: Tone Classifier Performance (Held-Out Test Set, 90 samples)**
| Metric | Value |
| :--- | :--- |
| **Validation Accuracy** | **97.78%** |
| **Test Accuracy** | **100.00%** (90 / 90) |
| **Macro F1-Score** | **1.00** |
| **Isolated Model Latency** | **1.2 ms** (Tone model alone on CPU) |

### 10.3 Test Suite Execution Summary

**Table 10.3: Test Suite Verification Summary**
| Test Suite | Total Tests | Passed | Skipped | Failed | Pass Rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Backend (pytest)** | 567 | **541** | 26 | **0** | **100%** (active) |
| **Frontend (node test)** | 20 | **20** | 0 | **0** | **100%** |
| **Total** | 587 | **561** | 26 | **0** | **100%** |

*Note: 26 backend tests were skipped (19 Docker integration tests and 7 live Ollama integration tests) when running offline unit test suites without container execution harnesses.*

### 10.4 Generation Latency and Token Throughput

**Table 10.4: LLM Generation Performance on Consumer CPU**
| Metric | Qwen2.5-Coder:1.5B | Qwen2.5-Coder:3B |
| :--- | :--- | :--- |
| **Model Disk Size** | ~986 MB | ~1.9 GB |
| **Warm Time-to-First-Token (TTFT)** | ~290 – 450 ms | ~1.8 s |
| **Cold-Start Initial Load** | ~5.6 s | ~12.0 s |
| **Generation Throughput** | 22.4 – 27.1 tokens / sec | 9.8 tokens / sec |
| **Average Response Time** | 8 – 12 seconds | 25 – 40 seconds |

---

# CHAPTER 11: SECURITY, PRIVACY, AND LIMITATIONS

### 11.1 Threat Model and Security Boundaries
1. **Host Protection:** Untrusted code execution is strictly confined to ephemeral Docker containers. Malicious operations (`os.system("rm -rf /")`) are contained within the container's scratch volume and cannot affect the host.
2. **Denial-of-Service Defense:** Infinite loops and fork bombs are neutralized by a 3.0-second timeout, 256MB RAM cap, and 64 PID limit.
3. **Prompt Injection Mitigation:** User input is strictly treated as untrusted data within user tags, isolated from system instructions.

### 11.2 Data Sovereignty and Offline Privacy
Because Bhasha2Code executes entirely on `localhost` via Ollama and SQLite, zero user queries, intellectual property, or code snippets leave the host device.

### 11.3 System Limitations
1. **CPU Speed Dependency:** On dual-core processors, local LLM generation may take 20–30 seconds.
2. **Slang Variance:** Highly non-standard phonetic spellings not present in the dictionary may require user clarification.
3. **Non-Python Static AST:** C/C++ and Java use lexical pattern checkers until compiled in the Docker container.

---

# CHAPTER 12: APPLICATIONS

### 12.1 Academic Laboratories and Computer Science Pedagogy
Bhasha2Code serves as a continuous, private coding tutor for first- and second-year engineering students mastering data structures and algorithms.

### 12.2 Regional and Rural Institutions
By eliminating internet bandwidth requirements and expensive subscriptions, Bhasha2Code brings state-of-the-art AI assistance to rural and semi-urban colleges.

### 12.3 Air-Gapped and Secure Environments
Suitable for enterprise or defense installations where code cannot be transmitted across public networks.

---

# CHAPTER 13: FUTURE SCOPE

1. **Multimodal Indic Voice Input:** Incorporating offline speech-to-text models (such as Indic Whisper or AI4Bharat Bhashini) for direct verbal coding queries.
2. **Expansion to South Indian Languages:** Extending lexical resources and datasets to Kannada, Telugu, Tamil, and Gujarati.
3. **Fine-Tuning on University Syllabus:** Fine-tuning compact models directly on Savitribai Phule Pune University (SPPU) lab manuals and practical viva question banks.
4. **Visual Step-Through Debugger:** Implementing animated variable tracking and array state inspection for data structures.

---

# CONCLUSION

Bhasha2Code demonstrates that high-performance, privacy-preserving AI coding assistance can be achieved on consumer hardware without recurring cloud costs or internet dependencies. By integrating deterministic NLP classification, prompt steering policies, Abstract Syntax Tree validation, Docker container isolation, and pedagogical Study Mode scaffolding, Bhasha2Code bridges the gap between regional Indian computational thinking and formal software engineering syntax.

---

# REFERENCES

1. M. Chen, J. Tworek, H. Jun, et al., "Evaluating Large Language Models Trained on Code," *arXiv preprint arXiv:2107.03374*, 2021.
2. B. Hui, J. Yang, C. Cui, et al., "Qwen2.5-Coder Technical Report: Code Intelligence at Scale," *arXiv preprint arXiv:2409.12186*, 2024.
3. B. Becker, P. Denny, J. Finnie-Ansley, et al., "Programming Is Hard - Or at Least It Used to Be: Educational Opportunities And Challenges of AI Code Generation," in *Proc. 54th ACM Technical Symposium on Computer Science Education (SIGCSE)*, pp. 500–506, 2023.
4. B. Rozière, J. Gehring, F. Gloeckle, et al., "Code Llama: Open Foundation Models for Code," *arXiv preprint arXiv:2308.12950*, 2023.
5. A. Tiwary and P. Kumar, "Code-Mixing and Linguistic Challenges in Indian Vernacular Computational Linguistics," *ACM Transactions on Asian and Low-Resource Language Information Processing*, vol. 21, no. 4, pp. 1–24, 2022.
6. F. Pedregosa, G. Varoquaux, A. Gramfort, et al., "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
7. D. Merkel, "Docker: Lightweight Linux Containers for Consistent Development and Deployment," *Linux Journal*, vol. 2014, no. 239, pp. 2–8, 2014.
8. National Council of Educational Research and Training (NCERT), "National Education Policy 2020: Technology Use and Integration in Education," Ministry of Education, Government of India, 2020.
9. S. Ramirez, "FastAPI: Modern, Fast Web Framework for Building APIs with Python," *PyCon US Documentation*, 2020.
10. G. van Rossum and Python Software Foundation, "The ast Module: Abstract Syntax Tree Processing," *Python Standard Library Documentation*, 2024.

---

# APPENDIX

### Appendix A: Sample Prompts and System Outputs

#### Case 1: Code Generation in Marathi-English
- **User Prompt:** `"bhai python madhe palindrome check karnara code de with test cases"`
- **Detected Language:** `MARATHI_ENGLISH` | **Intent:** `GENERATE_CODE` | **Tone:** `CASUAL`
- **Generated Code:**
```python
def is_palindrome(s: str) -> bool:
    """Check if a given string is a palindrome ignoring case and spaces."""
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]

if __name__ == "__main__":
    assert is_palindrome("radar") is True
    assert is_palindrome("hello") is False
    print("All test cases passed!")
```
- **Validation Status:** `VALID` (via Python AST)

#### Case 2: Study Mode Walkthrough in Hindi-English
- **User Prompt:** (Study Mode ON) `"Binary search algorithm samjhao"`
- **Output:** Includes Problem Understanding, Algorithm Steps, Flowchart, Source Code, and 5 Viva Q&A items.

---

### Appendix B: API Endpoints Specification

1. `POST /api/v1/chat/stream`: Server-Sent Events stream accepting `ChatRequest(message: str, session_id: Optional[str], study_mode: bool)`.
2. `POST /api/v1/code/validate`: Accepts `CodeValidateRequest(code: str, language: str)` and returns syntax status with line-number diagnostics.
3. `POST /api/v1/code/run`: Accepts `CodeRunRequest(code: str, language: str, stdin: Optional[str])` and executes inside an isolated Docker container.
4. `WebSocket /api/v1/code/interactive-run`: Bi-directional streaming terminal session for interactive stdin programs.
5. `GET /api/v1/sessions`: Lists all active student sessions.

---

### Appendix C: Setup and Installation Manual

1. **Clone Repository & Setup Virtual Environment:**
   ```bash
   git clone <repo_url> Bhasa2code
   cd Bhasa2code
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. **Install & Pull Ollama Model:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull qwen2.5-coder:1.5b
   ```
3. **Build Sandbox Docker Images:**
   ```bash
   docker build -t bhasha2code-sandbox-python:1.0.0 -f docker/sandbox/Dockerfile.python .
   ```
4. **Run Backend & Frontend:**
   ```bash
   # Terminal 1: Backend
   python -m uvicorn backend.app.main:app --reload --port 8000
   
   # Terminal 2: Frontend
   cd frontend && npm install && npm run dev
   ```
5. **Open Browser:** Navigate to `http://localhost:5173`.
