# Bhasha2Code Labeled Intent Dataset (T12)

## Purpose

The Bhasha2Code Intent Dataset provides a high-quality, multilingual, coding-domain labeled dataset designed to train and evaluate an offline Intent Classifier (Task T13).

### Core Principle: Orthogonality of Intent and Tone
- **Intent** answers: *"What does the user want the system to do or provide?"*
- **Tone** answers: *"How does the user want the response to sound or be presented?"*

```text
"bro ha code debug kar na"
Tone   = CASUAL
Intent = DEBUG_CODE

"Please explain this algorithm in detail."
Tone   = DETAILED
Intent = ALGORITHM

"simple language madhe ha code samjhav"
Tone   = SIMPLE
Intent = EXPLAIN_CODE
```

The dataset keeps these two concepts completely independent. Every intent appears across varied tones (casual, formal, simple, technical, short, detailed).

---

## Dataset Schema

The dataset is stored in CSV (`intent_dataset.csv`, `intent_train.csv`, `intent_validation.csv`, `intent_test.csv`) and JSON Lines (`intent_dataset.jsonl`) formats:

| Column | Type | Description |
|---|---|---|
| `id` | Integer | Unique sample identifier (1-indexed) |
| `text` | String | Raw conversational coding query |
| `intent` | String | Primary intent class (one of 18 allowed labels) |
| `language` | String | Language style (`English`, `Hindi`, `Marathi`, `Hinglish`, `Marathi-English`, `Hindi-English`) |
| `domain` | String | Context domain (fixed to `coding`) |

### Example Records:

```csv
id,text,intent,language,domain
1,"mala calculator cha code de",GENERATE_CODE,Marathi-English,coding
2,"ya code madhe error aahe fix kar",DEBUG_CODE,Marathi-English,coding
3,"explain this Python function",EXPLAIN_CODE,English,coding
4,"mujhe binary search ka approach batao",APPROACH_SUGGESTION,Hinglish,coding
5,"find my previous SQL code",SEARCH,English,coding
```

---

## Intent Taxonomy & Operational Definitions

The dataset uses exactly 18 intent labels:

### 1. `GENERATE_CODE`
User wants new code or an implementation to be created from scratch.
- **Primary Signal**: Create, generate, or produce implementation.
- **Examples**:
  - `Write a Python program to calculate the factorial of a number.`
  - `दो मैट्रिक्स को जोड़ने का सी भाषा में कोड बनाओ।`
  - `दिलेल्या संख्येचा फॅक्टोरियल काढणारा पायथन कोड तयार कर.`
  - `calculator ka program bana do python me`

### 2. `DEBUG_CODE`
User provides code or describes a malfunctioning program and explicitly requests a bug fix or resolution.
- **Primary Signal**: Fix broken implementation or solve run-time error in provided code.
- **Examples**:
  - `Fix this Python script because it throws an IndexError on empty lists.`
  - `या कोडमध्ये येणारा एरर फिक्स करून दे.`
  - `ye code crash ho raha hai isko fix kar do`

### 3. `EXPLAIN_CODE`
User wants an existing code snippet or construct explained to understand how it functions.
- **Primary Signal**: Explain behavior, logic, or line-by-line mechanics of code.
- **Examples**:
  - `Explain line by line how this Python recursive function works.`
  - `हा कोड कसा काम करतो ते समजावून सांग.`
  - `mujhe is code ka logic step by step samjhao`

### 4. `OPTIMIZE_CODE`
User wants an existing working code modified to be faster, cleaner, use less memory, or use better idioms.
- **Primary Signal**: Modify/rewrite implementation for efficiency, speed, or memory savings.
- **Examples**:
  - `Optimize this nested loop to improve execution time.`
  - `हा कोड अजून फास्ट कसा करता येईल?`
  - `is code ka memory usage optimize karke do`

### 5. `CONVERT_CODE`
User wants code translated from one programming language or framework representation into another.
- **Primary Signal**: Re-implement identical solution in a different target language.
- **Examples**:
  - `Convert this JavaScript Promise chain to equivalent Python async await.`
  - `हा पायथन कोड सी++ मध्ये कन्व्हर्ट करून दे.`
  - `is java code ko python me convert kar do`

### 6. `ALGORITHM`
User inquires about an algorithmic technique, algorithm behavior, complexity, or algorithm choice rather than inspecting a particular code snippet.
- **Primary Signal**: Algorithmic methodology, step mechanisms, or selection between algorithms.
- **Examples**:
  - `How does Dijkstra's shortest path algorithm work on weighted graphs?`
  - `बायनरी सर्च अल्गोरिदम कसा काम करतो?`
  - `quick sort algorithm kaise kaam karta hai explain karo`

### 7. `CONCEPT`
User asks to understand a general computing, software engineering, or computer science concept.
- **Primary Signal**: Theoretical understanding of a technical concept or paradigm.
- **Examples**:
  - `What is polymorphism in object-oriented programming?`
  - `एनकॅप्स्युलेशन म्हणजे काय आणि ते का वापरतात?`
  - `dependency injection concept kya hota hai samjhao`

### 8. `CODE_REVIEW`
User requests an overall evaluation, stylistic critique, maintainability check, or holistic review of written code.
- **Primary Signal**: Broad assessment of code quality, cleanliness, and maintainability.
- **Examples**:
  - `Review this pull request code for readability and edge cases.`
  - `माझ्या कोडची क्वालिटी तपासून रिव्ह्यू दे.`
  - `is implementation ka thorough code review karke do`

### 9. `CODE_SUGGESTION`
User asks for incremental coding-level tips or suggestions to improve a specific function or script without necessarily requesting complete re-engineering.
- **Primary Signal**: Actionable recommendations for a specific code fragment.
- **Examples**:
  - `What improvements can I make to this Python function?`
  - `या फंक्शनमध्ये काय सुधारणा करता येतील ते सुचव.`
  - `is function ko better banane ke liye suggestions do`

### 10. `PERFORMANCE_ANALYSIS`
User wants to diagnose performance characteristics, identify bottlenecks, measure profiling metrics, or understand why an application is slow.
- **Primary Signal**: Profiling, bottleneck identification, and latency diagnosis.
- **Examples**:
  - `Why is this Pandas DataFrame merge taking so long to complete?`
  - `हा प्रोग्राम इतका स्लो का चालतोय ते ॲनालाइज कर.`
  - `is function me bottleneck kahan hai analyze karo`

### 11. `ERROR_EXPLANATION`
User wants to understand the underlying cause or meaning of an error message or exception trace, without explicitly commanding an immediate fix.
- **Primary Signal**: Interpretation and root-cause education for an error or exception.
- **Examples**:
  - `What does AttributeError: 'NoneType' object has no attribute 'split' mean?`
  - `हा KeyError का येतो आणि त्याचा अर्थ काय?`
  - `mujhe samjhao ye null pointer exception kyun aata hai`

### 12. `APPROACH_SUGGESTION`
User asks for high-level strategy, algorithmic approach, or problem-solving plan before writing any code.
- **Primary Signal**: Conceptual plan or methodology to tackle a programming challenge.
- **Examples**:
  - `What approach should I take to solve the two-sum problem efficiently?`
  - `हा प्रोग्रॅमिंग प्रॉब्लेम सोडवण्यासाठी कोणता अप्रोच योग्य ठरेल?`
  - `is problem ko solve karne ke liye kya approach follow karein`

### 13. `BEST_PRACTICE`
User seeks industry standards, official conventions, idiomatic guidelines, or design principles.
- **Primary Signal**: Industry-standard conventions or idiomatic coding rules.
- **Examples**:
  - `What are the best practices for handling database sessions in FastAPI?`
  - `पायथनमध्ये एरर हँडलिंगसाठी बेस्ट प्रॅक्टिस कोणती आहे?`
  - `rest api designing me best practices kya hoti hain`

### 14. `ARCHITECTURE_SUGGESTION`
User asks for system-level design, component boundaries, multi-tier layout, or database integration patterns.
- **Primary Signal**: Multi-component or macro-system structural architecture.
- **Examples**:
  - `How should I design the microservices architecture for an e-commerce platform?`
  - `या ॲप्लिकेशनसाठी स्वच्छ आणि स्केलेबल आर्किटेक्चर सुचव.`
  - `is full stack project ka clean architecture suggest karo`

### 15. `FEATURE_SUGGESTION`
User asks for creative ideas, new functionality, or capability expansions for a software project.
- **Primary Signal**: Product capability and feature additions.
- **Examples**:
  - `What features should I add to my CLI expense tracker project?`
  - `या कोडिंग असिस्टंट ॲपमध्ये अजून कोणती नवीन फीचर्स ॲड करू शकतो?`
  - `apne portfolio project me aur kya cool features add karu`

### 16. `TEST_CASE_GENERATION`
User wants test suites, unit tests, mock scenarios, edge cases, or test code.
- **Primary Signal**: Test fixtures, unit test functions, or edge-case validation suites.
- **Examples**:
  - `Generate pytest test cases for this string validation function.`
  - `या फंक्शनसाठी युनिट टेस्ट्स आणि एज केसेस तयार कर.`
  - `is class ke liye comprehensive test cases generate karo`

### 17. `SECURITY_ANALYSIS`
User asks for vulnerability discovery, injection risks, authentication evaluation, or secure coding audits.
- **Primary Signal**: Threat assessment, security vulnerability scan, or hardened coding review.
- **Examples**:
  - `Scan this SQL query construction for potential SQL injection vulnerabilities.`
  - `या ऑथेंटिकेशन कोडमध्ये काही सिक्युरिटी रिस्क आहेत का ते तपास.`
  - `is api endpoint me security flaws check karke batao`

### 18. `SEARCH`
User asks to locate, retrieve, or reference previously saved code, conversation history, notes, or indexed session data.
- **Primary Signal**: Querying past session context or stored workspace artifacts.
- **Examples**:
  - `Find my previous Python script where we implemented Dijkstra's algorithm.`
  - `आपल्या आधीच्या चॅटमधील कॅल्क्युलेटरचा कोड शोधून दाखव.`
  - `humne pehle jo jwt token ka code discuss kiya tha wo dhoondho`

---

## Critical Boundary Rules

To resolve edge-case queries deterministically, annotations strictly follow these boundary rules:

1. **`DEBUG_CODE` vs `ERROR_EXPLANATION`**:
   - *"Why does this error occur?"* $\rightarrow$ `ERROR_EXPLANATION`
   - *"Fix this error in my code."* $\rightarrow$ `DEBUG_CODE`
   - *"Explain this error and fix the code."* $\rightarrow$ `DEBUG_CODE` (Actionable fixing overrides explanation).

2. **`DEBUG_CODE` vs `CODE_REVIEW`**:
   - *"Fix this specific bug."* $\rightarrow$ `DEBUG_CODE`
   - *"Review this code and evaluate its overall quality."* $\rightarrow$ `CODE_REVIEW`

3. **`CODE_SUGGESTION` vs `OPTIMIZE_CODE`**:
   - *"Any suggestions to make this code cleaner?"* $\rightarrow$ `CODE_SUGGESTION`
   - *"Make this code faster / reduce memory usage."* $\rightarrow$ `OPTIMIZE_CODE`

4. **`PERFORMANCE_ANALYSIS` vs `OPTIMIZE_CODE`**:
   - *"Why is this code running so slow? Profile the execution."* $\rightarrow$ `PERFORMANCE_ANALYSIS`
   - *"Make this code faster."* $\rightarrow$ `OPTIMIZE_CODE`
   - *"Analyze performance and optimize it."* $\rightarrow$ `OPTIMIZE_CODE`

5. **`ALGORITHM` vs `CONCEPT`**:
   - *"How does binary search / quicksort work?"* $\rightarrow$ `ALGORITHM`
   - *"What is polymorphism / encapsulation / REST API?"* $\rightarrow$ `CONCEPT`

6. **`APPROACH_SUGGESTION` vs `ALGORITHM`**:
   - *"What approach should I take to solve this problem?"* $\rightarrow$ `APPROACH_SUGGESTION`
   - *"Which sorting algorithm should I pick?"* $\rightarrow$ `ALGORITHM`

7. **`ARCHITECTURE_SUGGESTION` vs `FEATURE_SUGGESTION`**:
   - *"How should I organize microservices and database layers?"* $\rightarrow$ `ARCHITECTURE_SUGGESTION`
   - *"What interesting features can I add to my application?"* $\rightarrow$ `FEATURE_SUGGESTION`

8. **`BEST_PRACTICE` vs `CODE_SUGGESTION`**:
   - *"What is the standard best practice for error handling in Python?"* $\rightarrow$ `BEST_PRACTICE`
   - *"What should I change in this specific function?"* $\rightarrow$ `CODE_SUGGESTION`

9. **`SEARCH` vs `CONCEPT`**:
   - *"What is binary search?"* $\rightarrow$ `CONCEPT`
   - *"Find our previous discussion about binary search in my notes."* $\rightarrow$ `SEARCH` (Internal history search).

---

## Multilingual Coverage

The dataset features balanced distribution across 6 linguistic styles:
1. **English**: Standard English developer queries.
2. **Hindi**: Devanagari Hindi technical phrasing.
3. **Marathi**: Devanagari Marathi technical phrasing.
4. **Hinglish**: Latin-script transliterated Hindi with English technical nouns.
5. **Marathi-English**: Latin-script transliterated Marathi with English technical nouns.
6. **Hindi-English**: Hybrid mixed queries combining Hindi sentence structures and English keywords.

Both native Devanagari scripts and Latin transliterations are fully supported:
- `मला` / `mala`
- `मला कोड दे` / `mala code de`
- `मुझे` / `mujhe`

---

## Dataset Statistics

- **Total Samples**: 1080 unique queries
- **Unique Samples**: 1080 (0 duplicates)
- **Invalid Rows**: 0
- **Domain**: 100% `coding`
- **Text Length**:
  - Minimum: 35 characters
  - Maximum: 100 characters
  - Average: 59.3 characters

### Intent Distribution (Exact Balance):
| Intent | Count | Percentage |
|---|---|---|
| `GENERATE_CODE` | 60 | 5.56% |
| `DEBUG_CODE` | 60 | 5.56% |
| `EXPLAIN_CODE` | 60 | 5.56% |
| `OPTIMIZE_CODE` | 60 | 5.56% |
| `CONVERT_CODE` | 60 | 5.56% |
| `ALGORITHM` | 60 | 5.56% |
| `CONCEPT` | 60 | 5.56% |
| `CODE_REVIEW` | 60 | 5.56% |
| `CODE_SUGGESTION` | 60 | 5.56% |
| `PERFORMANCE_ANALYSIS` | 60 | 5.56% |
| `ERROR_EXPLANATION` | 60 | 5.56% |
| `APPROACH_SUGGESTION` | 60 | 5.56% |
| `BEST_PRACTICE` | 60 | 5.56% |
| `ARCHITECTURE_SUGGESTION` | 60 | 5.56% |
| `FEATURE_SUGGESTION` | 60 | 5.56% |
| `TEST_CASE_GENERATION` | 60 | 5.56% |
| `SECURITY_ANALYSIS` | 60 | 5.56% |
| `SEARCH` | 60 | 5.56% |
| **Total** | **1080** | **100%** |

### Language Distribution (Exact Balance):
| Language Category | Count | Percentage |
|---|---|---|
| `English` | 180 | 16.67% |
| `Hindi` | 180 | 16.67% |
| `Marathi` | 180 | 16.67% |
| `Hinglish` | 180 | 16.67% |
| `Marathi-English` | 180 | 16.67% |
| `Hindi-English` | 180 | 16.67% |
| **Total** | **1080** | **100%** |

---

## Deterministic Split Strategy

The dataset is partitioned deterministically using `random_state = 42`:
- **Train Set** (70%): 756 samples (42 per intent)
- **Validation Set** (15%): 162 samples (9 per intent)
- **Test Set** (15%): 162 samples (9 per intent)

### Split Isolation & Zero Leakage:
- $\text{Train} \cap \text{Validation} = \emptyset$ (Disjoint IDs & normalized texts)
- $\text{Train} \cap \text{Test} = \emptyset$ (Disjoint IDs & normalized texts)
- $\text{Validation} \cap \text{Test} = \emptyset$ (Disjoint IDs & normalized texts)
- $\text{Train} \cup \text{Validation} \cup \text{Test} = \text{Full Dataset}$

---

## Limitations

1. **Synthetic Curation**: Queries were curated specifically for Bhasha2Code's taxonomy; live production chatter may contain more shorthand or typographical errors.
2. **Search Scope**: `SEARCH` queries are restricted to searching previous session context, local notes, or workspace artifacts, not broad web crawling.
3. **No Multimodal Inputs**: Audio, image diagrams, and raw file uploads are not represented in this text-based intent corpus.

---

## Future Classifier Usage (Task T13)

The dataset will be utilized in Task T13 to train an offline Intent Classifier:
- Feature extraction using n-gram TF-IDF vectorization with multilingual subword/character tokenization.
- Classical supervised classification (Logistic Regression / Linear SVM) for low-latency, deterministic offline prediction.
- Evaluation on the holdout `intent_test.csv` test set against accuracy, macro F1 score, and per-intent precision/recall.
