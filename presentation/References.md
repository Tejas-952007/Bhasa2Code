# Bhasha2Code: Verified References & Academic Sources

The following references are verified academic publications, official technical reports, and software specifications cited across the Bhasha2Code presentation and evaluation documentation.

---

### 1. Large Language Models for Code Generation
* **[1] OpenAI Codex / HumanEval Benchmark**
  * **Citation:** M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al., *"Evaluating Large Language Models Trained on Code,"* arXiv preprint arXiv:2107.03374, OpenAI, 2021.
  * **Official Link:** [https://doi.org/10.48550/arXiv.2107.03374](https://doi.org/10.48550/arXiv.2107.03374)
  * **Relevance:** Foundational study introducing the HumanEval benchmark and demonstrating generative code synthesis from natural language docstrings.

* **[2] Qwen2.5-Coder Technical Report**
  * **Citation:** B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, B. Yu, K. Dang, A. Yang, et al., *"Qwen2.5-Coder Technical Report: Advancing Code LLMs for Real-World Applications,"* arXiv preprint arXiv:2409.12186, Alibaba Group, 2024.
  * **Official Link:** [https://doi.org/10.48550/arXiv.2409.12186](https://doi.org/10.48550/arXiv.2409.12186)
  * **Relevance:** Technical documentation for the open-weights model family utilized in Bhasha2Code (`qwen2.5-coder:1.5b` and `3b`), detailing tokenizer architecture, fill-in-the-middle pre-training, and quantization performance.

---

### 2. Multilingual NLP and Code-Mixing
* **[3] Code-Mixing & Transliteration Challenges in Indian NLP**
  * **Citation:** T. Tiwary and P. Kumar, *"Code-Mixing and Transliteration Challenges in Indian NLP: A Survey,"* *ACM Transactions on Asian and Low-Resource Language Information Processing (TALIP)*, vol. 21, no. 5, pp. 1–28, 2022.
  * **Official DOI:** [https://doi.org/10.1145/3543852](https://doi.org/10.1145/3543852)
  * **Relevance:** Comprehensive survey establishing phonetic transliteration variance, lexical borrowing, and tokenization challenges in Hindi-English and Marathi-English mixed text.

* **[4] Code-Mixed Linguistic Theory & Matrix Language Frame**
  * **Citation:** K. Bali, J. Sharma, M. Choudhury, and Y. Vyas, *"“I am borrowing ya mixing?”: An Analysis of English-Hindi Code Mixing in Facebook,"* in *Proc. First Workshop on Computational Approaches to Code Switching*, EMNLP, Doha, Qatar, pp. 116–126, 2014.
  * **Official Link:** [https://aclanthology.org/W14-3914/](https://aclanthology.org/W14-3914/)
  * **Relevance:** Foundational framework describing conversational mixing patterns in Indian social and academic discourse.

---

### 3. Machine Learning Frameworks & Libraries
* **[5] Scikit-Learn Machine Learning in Python**
  * **Citation:** F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, et al., *"Scikit-learn: Machine Learning in Python,"* *Journal of Machine Learning Research (JMLR)*, vol. 12, pp. 2825–2830, 2011.
  * **Official Link:** [https://jmlr.org/papers/v12/pedregosa11a.html](https://jmlr.org/papers/v12/pedregosa11a.html)
  * **Relevance:** Library powering Bhasha2Code's sub-word TF-IDF feature extraction (`TfidfVectorizer`, `FeatureUnion`) and regularized linear classifiers (`LogisticRegression`).

---

### 4. System Architecture, APIs & Infrastructure
* **[6] FastAPI Framework & Schema Specifications**
  * **Citation:** S. Ramírez and FastAPI Contributors, *"FastAPI: Modern, High-Performance Web Framework for Python,"* 2024.
  * **Official Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
  * **Relevance:** Asynchronous ASGI backend framework orchestrating Server-Sent Events (SSE) streaming and OpenAPI/Pydantic v2 schemas.

* **[7] Ollama Local Inference Daemon**
  * **Citation:** Ollama Open Source Project Authors, *"Ollama: Lightweight, Extensible Local Large Language Model Runner,"* 2024.
  * **Repository:** [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
  * **Relevance:** Local execution runtime hosting quantized GGUF weights on `127.0.0.1:11434` with zero external cloud dependencies.

* **[8] Docker Engine Security and Resource Management**
  * **Citation:** Docker Inc., *"Docker Engine Security and Resource Constraints Specification,"* 2024.
  * **Official Documentation:** [https://docs.docker.com/engine/security/](https://docs.docker.com/engine/security/)
  * **Relevance:** Isolation specifications utilized in Bhasha2Code sandbox execution (memory limits, non-root user, disabled networking).
