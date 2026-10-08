# Tone Classifier Development & Evaluation Guide (T11)

## 1. Problem Statement

Bhasha2Code is an intelligent coding assistant that adapts not only to programming language and natural language, but also to user communication style (tone). Different users require different response formats:
- A beginner needs a gentle, intuitive analogy (**SIMPLE**).
- An experienced engineer debugging in a rush needs direct code (**SHORT**).
- A student preparing for an exam needs a complete step-by-step walkthrough (**DETAILED**).
- An architect needs formal Big-O proofs and memory tradeoffs (**TECHNICAL**).
- A colleague asking casually needs conversational peer dialogue (**CASUAL**).
- An enterprise user needs polite, professional phrasing (**FORMAL**).

The Tone Classifier is the first machine learning model in the Bhasha2Code NLP pipeline. It deterministically classifies conversational input into one of these six primary operational tones.

---

## 2. Dataset Source

The classifier is trained on the T10 curated dataset located in `data/datasets/tone/`:
- **Training Set** (`tone_train.csv`): 420 samples (70 per tone)
- **Validation Set** (`tone_validation.csv`): 90 samples (15 per tone)
- **Test Set** (`tone_test.csv`): 90 samples (15 per tone) — final untouched holdout

The dataset spans 6 multilingual varieties: English, Hindi, Marathi, Hinglish, Marathi-English, and Hindi-English, all strictly within the coding domain.

---

## 3. Model Architecture & Feature Engineering

### Classical Hybrid NLP
We employ a classical, fully offline machine-learning architecture:
- **TF-IDF Word Features**: $n$-gram range `(1, 2)` capturing lexical phrasing, keywords, and tone particles. Sublinear term frequency scaling is enabled.
- **TF-IDF Character Features**: $n$-gram range `(3, 5)` with boundary-aware `char_wb` analyzer. This captures subword roots, spelling variants, and transliteration patterns in Marathi/Hindi/Hinglish (e.g. `samjhav`, `samjhao`, `samajh`, `madhe`, `fakt`, `bus`).
- **Feature Union**: Concatenates word and character TF-IDF representations into a combined sparse feature matrix.
- **Classifier**: Multi-class `LogisticRegression` with:
  - Inverse regularization parameter $C = 3.0$
  - `class_weight="balanced"`
  - Solver: `lbfgs`
  - Fixed `random_state = 42`

### Why This Model?
- **100% Offline & Lightweight**: Requires zero internet connection, cloud credentials, or GPU hardware. Artifact size is only 1.3 MB.
- **Fast Training & Inference**: Trains in < 2 seconds on a standard laptop CPU; inference takes < 2 milliseconds per query.
- **Calibrated Probabilities**: Softmax output yields genuine probability distributions across all 6 classes without fabricated confidence scores.
- **Explainability**: Logistic regression coefficients provide direct inspectability of feature weights.

---

## 4. Training & Evaluation Pipeline

The training script `scripts/train_tone_classifier.py` executes:
1. **Data Leakage Verification**: Rigorously verifies that train, validation, and test sample IDs and texts are completely disjoint before training begins.
2. **Model Training**: Fits the pipeline solely on `tone_train.csv`.
3. **Validation Evaluation**: Assesses performance against engineering thresholds ($\ge 0.80$ Accuracy and Macro F1).
4. **Final Test Evaluation**: Evaluates on untouched `tone_test.csv` against targets ($\ge 0.78$ Accuracy and Macro F1).
5. **Artifact Persistence**: Saves model to `models/tone/tone_classifier.joblib` and comprehensive metadata to `models/tone/metadata.json`.

---

## 5. Evaluation Results

### Validation Split (90 samples)
- **Accuracy**: `97.78%` (0.9778)
- **Macro F1**: `0.9778`
- **Weighted F1**: `0.9778`

### Final Test Split (90 samples)
- **Accuracy**: `100.0%` (1.0000)
- **Macro F1**: `1.0000`
- **Weighted F1**: `1.0000`

### Per-Class Test Metrics:
| Tone | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| `CASUAL` | 1.0000 | 1.0000 | 1.0000 | 15 |
| `DETAILED` | 1.0000 | 1.0000 | 1.0000 | 15 |
| `FORMAL` | 1.0000 | 1.0000 | 1.0000 | 15 |
| `SHORT` | 1.0000 | 1.0000 | 1.0000 | 15 |
| `SIMPLE` | 1.0000 | 1.0000 | 1.0000 | 15 |
| `TECHNICAL` | 1.0000 | 1.0000 | 1.0000 | 15 |

### Confusion Matrix (Test Split):
```text
Labels: ['CASUAL', 'DETAILED', 'FORMAL', 'SHORT', 'SIMPLE', 'TECHNICAL']
[15,  0,  0,  0,  0,  0]  (CASUAL)
[ 0, 15,  0,  0,  0,  0]  (DETAILED)
[ 0,  0, 15,  0,  0,  0]  (FORMAL)
[ 0,  0,  0, 15,  0,  0]  (SHORT)
[ 0,  0,  0,  0, 15,  0]  (SIMPLE)
[ 0,  0,  0,  0,  0, 15]  (TECHNICAL)
```

---

## 6. Error Analysis

Across validation and test sets (180 evaluation samples), only 2 misclassifications occurred (both on the validation set):

1. **Text**: `"एसक्यूएल और नोएसक्यूएल का अंतर बिल्कुल सरल और आम बोलचाल में बताओ।"`
   - **Actual**: `SIMPLE`
   - **Predicted**: `SHORT` (confidence: `0.4201`)
   - **Root Cause**: `"बिल्कुल"` and short sentence structure resembled concise query phrasing, causing slight ambiguity between simplicity and brevity.
2. **Text**: `"ek line me explain karo ye error"`
   - **Actual**: `SHORT`
   - **Predicted**: `DETAILED` (confidence: `0.2651`)
   - **Root Cause**: The presence of `"explain"` strongly triggered detailed explanation features. The low confidence (`0.2651`) appropriately reflects uncertainty.

---

## 7. Model Artifacts

- **Model Binary**: `models/tone/tone_classifier.joblib` (1.3 MB)
- **Model Metadata**: `models/tone/metadata.json` (4.0 KB)

---

## 8. Python Inference API

```python
from backend.app.nlp.tone_classification import ToneClassifier, predict_tone

# Method 1: Using singleton convenience helper
result = predict_tone("bro ha code check kar na")
print(result.tone)          # "CASUAL"
print(result.confidence)    # e.g. 0.3515
print(result.probabilities) # {'CASUAL': 0.35, ...}

# Method 2: Explicit class instantiation
classifier = ToneClassifier.load("models/tone/tone_classifier.joblib")
result = classifier.predict("Please explain the architecture of this module.")
print(result.tone)          # "FORMAL"
```

Edge case behavior:
- `""`, `"   "`, or `None`: Returns fallback with `confidence=0.0` and uniform class probabilities.
- Unsupported data types: Raises `TypeError`.

---

## 9. Known Limitations & Future Improvements

1. **Curated Baseline**: The dataset is relatively clean; real-world developer queries may contain more extreme typos, noisy punctuation, or mixed code snippets.
2. **Auxiliary Feature Integration**: In future tasks, the output of T09 (Language Detection) can optionally be passed as a secondary metadata prior to calibrate confidence on rare code-mixed phrases.
3. **Fine-Tuning**: If greater nuance or multi-label tone classification is required, a lightweight local multilingual transformer (e.g. MiniLM or IndicBERT) can be introduced without changing the `ToneClassifier` interface.
