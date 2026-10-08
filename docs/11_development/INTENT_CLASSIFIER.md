# Intent Classifier Development & Evaluation Guide (T13)

## 1. Problem Statement

Bhasha2Code is an intelligent coding assistant that empowers developers to interact using natural English, Hindi, Marathi, and code-mixed phrasing (Hinglish, Marathi-English, Hindi-English). While **Language Detection** (T09) identifies the linguistic variety and **Tone Classification** (T11) identifies the desired communication style, the **Intent Classifier** (T13) determines:

> **What does the user want the system to do or provide?**

The Intent Classifier classifies user queries into exactly one of **18 operational intent classes**:
- `GENERATE_CODE`: Create new code or scripts.
- `DEBUG_CODE`: Fix failing, buggy, or throwing code.
- `EXPLAIN_CODE`: Explain mechanics, logic, or flow of existing code.
- `OPTIMIZE_CODE`: Improve execution speed, memory footprint, or algorithmic complexity.
- `CONVERT_CODE`: Translate code from one language or framework to another.
- `ALGORITHM`: Ask about algorithm mechanics, design, or algorithmic selection.
- `CONCEPT`: Understand general computing, data structure, or programming principles.
- `CODE_REVIEW`: Holistic evaluation of code quality, readability, and maintainability.
- `CODE_SUGGESTION`: Incremental tips and improvements for a specific function or block.
- `PERFORMANCE_ANALYSIS`: Profiling, bottleneck analysis, and execution diagnostics.
- `ERROR_EXPLANATION`: Meaning and root cause of an error, exception, or traceback.
- `APPROACH_SUGGESTION`: Conceptual strategy or solution methodology before writing code.
- `BEST_PRACTICE`: Recommended conventions, standards, and idiomatic idioms.
- `ARCHITECTURE_SUGGESTION`: System architecture, multi-tier layout, or database design.
- `FEATURE_SUGGESTION`: Functional feature additions and project enhancements.
- `TEST_CASE_GENERATION`: Unit tests, test suites, edge cases, or test code.
- `SECURITY_ANALYSIS`: Vulnerability detection, injection threats, or security audits.
- `SEARCH`: Search previous conversation history, notes, or saved code snippets.

---

## 2. Dataset Source & Partitions

The classifier is trained on the T12 curated dataset located in `data/datasets/intent/`:
- **Training Set** (`intent_train.csv`): 756 samples (42 per intent, exactly 70.0%)
- **Validation Set** (`intent_validation.csv`): 162 samples (9 per intent, exactly 15.0%)
- **Test Set** (`intent_test.csv`): 162 samples (9 per intent, exactly 15.0%) — untouched holdout

The dataset features 100% coding-domain queries evenly distributed across 6 language varieties (English, Hindi, Marathi, Hinglish, Marathi-English, Hindi-English).

---

## 3. Model Architecture & Feature Engineering

### Classical Hybrid NLP
We employ a classical, fully offline machine-learning architecture:
- **TF-IDF Word Features**: $n$-gram range `(1, 2)` with `sublinear_tf=True` and `min_df=1`, capturing key operational phrases and keywords.
- **TF-IDF Character Features**: $n$-gram range `(3, 5)` with boundary-aware `char_wb` analyzer, sublinear term frequency scaling, and `min_df=1`. This captures subword roots, affixes, and transliterated Indian-language particles (e.g., `samjhav`, `samjhao`, `banav`, `banao`, `shodh`, `dhoondho`).
- **Feature Union**: Concatenates word and character TF-IDF representations into a unified sparse feature matrix.
- **Classifier**: Multi-class `LogisticRegression` with:
  - Inverse regularization parameter $C = 3.0$
  - `class_weight="balanced"`
  - Solver: `lbfgs`
  - Maximum iterations: `1000`
  - Fixed `random_state = 42`

### Why Classical ML?
- **100% Offline & Deterministic**: Zero cloud API dependencies, zero network requests, zero LLM latency.
- **Lightweight**: Model artifact size is 3.9 MB on disk.
- **Ultra-Fast Inference**: Evaluates queries in ~1.5 milliseconds per prediction on CPU.
- **Clean Baseline**: Only `text` is consumed during inference. Ground-truth `language` and `tone` labels are never used as model inputs, preventing data leakage and circular dependencies.
- **Calibrated Softmax Probabilities**: Directly provides probabilities across all 18 classes for downstream thresholding and confidence inspection.

---

## 4. Evaluation Results

### Validation Split (162 samples)
- **Accuracy**: `91.36%` (target $\ge 80.0\%$)
- **Macro F1**: `0.9114` (target $\ge 0.8000$)
- **Weighted F1**: `0.9114`

### Holdout Test Split (162 samples)
- **Accuracy**: `92.59%` (target $\ge 78.0\%$)
- **Macro F1**: `0.9239` (target $\ge 0.7800$)
- **Weighted F1**: `0.9239`

### Per-Class Test Metrics:
| Intent | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| `ALGORITHM` | 0.8571 | 0.6667 | 0.7500 | 9 |
| `APPROACH_SUGGESTION` | 1.0000 | 1.0000 | 1.0000 | 9 |
| `ARCHITECTURE_SUGGESTION` | 0.9000 | 1.0000 | 0.9474 | 9 |
| `BEST_PRACTICE` | 1.0000 | 0.8889 | 0.9412 | 9 |
| `CODE_REVIEW` | 0.9000 | 1.0000 | 0.9474 | 9 |
| `CODE_SUGGESTION` | 1.0000 | 1.0000 | 1.0000 | 9 |
| `CONCEPT` | 0.8889 | 0.8889 | 0.8889 | 9 |
| `CONVERT_CODE` | 0.8182 | 1.0000 | 0.9000 | 9 |
| `DEBUG_CODE` | 0.9000 | 1.0000 | 0.9474 | 9 |
| `ERROR_EXPLANATION` | 1.0000 | 0.8889 | 0.9412 | 9 |
| `EXPLAIN_CODE` | 0.8000 | 0.8889 | 0.8421 | 9 |
| `FEATURE_SUGGESTION` | 1.0000 | 1.0000 | 1.0000 | 9 |
| `GENERATE_CODE` | 0.8889 | 0.8889 | 0.8889 | 9 |
| `OPTIMIZE_CODE` | 1.0000 | 0.6667 | 0.8000 | 9 |
| `PERFORMANCE_ANALYSIS` | 0.9000 | 1.0000 | 0.9474 | 9 |
| `SEARCH` | 1.0000 | 1.0000 | 1.0000 | 9 |
| `SECURITY_ANALYSIS` | 0.8889 | 0.8889 | 0.8889 | 9 |
| `TEST_CASE_GENERATION` | 1.0000 | 1.0000 | 1.0000 | 9 |

---

## 5. Multilingual Performance Breakdown

Performance on the holdout test set grouped by linguistic variety:

| Language Variety | Samples | Accuracy | Macro F1 |
|---|---|---|---|
| `Hinglish` | 30 | **100.0%** (1.0000) | **1.0000** |
| `Marathi-English` | 37 | **100.0%** (1.0000) | **1.0000** |
| `Hindi-English` | 20 | **100.0%** (1.0000) | **1.0000** |
| `English` | 27 | **85.19%** (0.8519) | **0.7738** |
| `Marathi` (Devanagari) | 25 | **84.00%** (0.8400) | **0.7059** |
| `Hindi` (Devanagari) | 23 | **82.61%** (0.8261) | **0.8118** |

**Observation**: Code-mixed transliterated queries (Hinglish, Marathi-English, Hindi-English) achieved 100% accuracy due to highly informative subword combinations between regional grammatical indicators and English technical terminology. Devanagari queries and English queries both exceeded the 82% benchmark.

---

## 6. Error Analysis

Out of 162 holdout test samples, exactly 12 misclassifications were observed. Every misclassification occurred with low model confidence ($\le 0.4055$), indicating appropriate calibration:

1. **Query**: `"बायनरी सर्च अल्गोरिदमचा संपूर्ण जावा कोड लिहून दे."`
   - *Actual*: `GENERATE_CODE` | *Predicted*: `ALGORITHM` (Confidence: 0.4055)
   - *Cause*: Algorithmic keyword `बायनरी सर्च अल्गोरिदम` competed with generation directive `कोड लिहून दे`.
2. **Query**: `"इस कोड में यह लैम्ब्डा फंक्शन क्या कर रहा है?"`
   - *Actual*: `EXPLAIN_CODE` | *Predicted*: `DEBUG_CODE` (Confidence: 0.2042)
   - *Cause*: Query phrasing resembles debugging inquiry ("what is this doing wrong").
3. **Query**: `"Improve the runtime efficiency of this recursive Fibonacci calculation."`
   - *Actual*: `OPTIMIZE_CODE` | *Predicted*: `EXPLAIN_CODE` (Confidence: 0.1542)
   - *Cause*: Low confidence distribution across optimization and explanation.
4. **Query**: `"या एसक्यूएल क्वेरीचा एक्झिक्युशन वेळ कमी करण्यासाठी बदल करा."`
   - *Actual*: `OPTIMIZE_CODE` | *Predicted*: `CONVERT_CODE` (Confidence: 0.1014)
   - *Cause*: Marathi phrasing `बदल करा` (make change) has high overlap with transformation terms.
5. **Query**: `"या पायथन स्क्रिप्टचा परफॉर्मन्स वाढवण्यासाठी कोड सुधारा."`
   - *Actual*: `OPTIMIZE_CODE` | *Predicted*: `PERFORMANCE_ANALYSIS` (Confidence: 0.1727)
   - *Cause*: Explicit boundary overlap between performance diagnosis and code optimization.
6. **Query**: `"Explain the difference between depth-first search and breadth-first search."`
   - *Actual*: `ALGORITHM` | *Predicted*: `CONCEPT` (Confidence: 0.2728)
   - *Cause*: "Explain the difference" closely mirrors conceptual definitions.
7. **Query**: `"Explain the working principle of the A* search heuristic function."`
   - *Actual*: `ALGORITHM` | *Predicted*: `EXPLAIN_CODE` (Confidence: 0.3916)
   - *Cause*: "Explain the working principle" keyword overlap with code explanation.
8. **Query**: `"बाइनरी सर्च की टाइम कॉम्प्लेक्सिटी क्या होती है?"`
   - *Actual*: `ALGORITHM` | *Predicted*: `GENERATE_CODE` (Confidence: 0.1461)
   - *Cause*: Low confidence dispersion across algorithmic queries.
9. **Query**: `"What is the difference between monolithic and microservices architecture?"`
   - *Actual*: `CONCEPT` | *Predicted*: `ARCHITECTURE_SUGGESTION` (Confidence: 0.3067)
   - *Cause*: Architecture terminology pulled prediction toward architectural suggestions.
10. **Query**: `"एसक्यूएल में 'foreign key constraint fails' का क्या मतलब है?"`
    - *Actual*: `ERROR_EXPLANATION` | *Predicted*: `SECURITY_ANALYSIS` (Confidence: 0.1835)
    - *Cause*: Low confidence token overlap.
11. **Query**: `"पायथन में लॉगिंग सेटअप करने के मानक तरीके क्या हैं?"`
    - *Actual*: `BEST_PRACTICE` | *Predicted*: `CONVERT_CODE` (Confidence: 0.1057)
    - *Cause*: Low confidence token dispersion.
12. **Query**: `"या वेब ॲप्लिकेशनमधील कोर्स आणि सीएसआरएफ सुरक्षेचे परीक्षण करा."`
    - *Actual*: `SECURITY_ANALYSIS` | *Predicted*: `CODE_REVIEW` (Confidence: 0.2126)
    - *Cause*: Marathi `परीक्षण करा` (review/inspect) shared with code review vocabulary.

---

## 7. Inference Usage

```python
from backend.app.nlp.intent_classification import IntentClassifier, predict_intent

# 1. Using convenience function (uses cached singleton)
result = predict_intent("ha code debug kar na")
print(result.intent)         # "DEBUG_CODE"
print(result.confidence)     # 0.8842
print(result.probabilities)  # {"DEBUG_CODE": 0.8842, ...}

# 2. Loading explicitly from disk
classifier = IntentClassifier.load("models/intent/intent_classifier.joblib")
result = classifier.predict("Please explain this function")
print(result.to_dict())
```

### Edge-Case Behavior:
- **Empty or Whitespace-only string**: Returns neutral fallback (`CONCEPT`, confidence `0.0`, uniform probability distribution).
- **None**: Safely returns fallback with confidence `0.0`.
- **PreprocessedText**: Automatically extracts text segments and executes prediction seamlessly.

---

## 8. Limitations & Future Improvements

1. **Curated Dataset Scale**: Trained on 756 samples (1,080 total); live user chatter may exhibit heavier spelling corruption or mixed-intent compound sentences (e.g. *"explain this code and then optimize it"*).
2. **Boundary Disambiguation**: When queries combine diagnostic keywords (`"why is this slow"`) with optimization requests (`"make it faster"`), the classifier relies on dominant term frequencies.
3. **Future Step (T14)**: Orchestrate Intent Classification with Language Detection (T09) and Tone Classification (T11) inside a unified NLP Orchestrator.
