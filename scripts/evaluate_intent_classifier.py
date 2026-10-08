#!/usr/bin/env python3
"""Evaluation and error analysis script for Bhasha2Code Intent Classifier (T13).

Loads the trained Intent Classifier pipeline and evaluates on the holdout test set
(data/datasets/intent/intent_test.csv).

Produces:
- Test Accuracy, Macro F1, Weighted F1
- Per-class Precision, Recall, F1, Support
- 18x18 Confusion Matrix
- Error analysis with diagnostic reasons for misclassifications
- Language-wise breakdown (Accuracy and Macro F1 per language variety)
- Confidence distribution analysis (<0.50, <0.60)
- Determinism check (10 repeated runs)
- Updates models/intent/metadata.json with final test results.
"""

import csv
import json
import os
import sys
from typing import Dict, List, Tuple

import joblib
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

TEST_CSV = os.path.join("data", "datasets", "intent", "intent_test.csv")
MODEL_DIR = os.path.join("models", "intent")
MODEL_PATH = os.path.join(MODEL_DIR, "intent_classifier.joblib")
METADATA_PATH = os.path.join(MODEL_DIR, "metadata.json")

EXPECTED_INTENTS = sorted(
    [
        "GENERATE_CODE",
        "DEBUG_CODE",
        "EXPLAIN_CODE",
        "OPTIMIZE_CODE",
        "CONVERT_CODE",
        "ALGORITHM",
        "CONCEPT",
        "CODE_REVIEW",
        "CODE_SUGGESTION",
        "PERFORMANCE_ANALYSIS",
        "ERROR_EXPLANATION",
        "APPROACH_SUGGESTION",
        "BEST_PRACTICE",
        "ARCHITECTURE_SUGGESTION",
        "FEATURE_SUGGESTION",
        "TEST_CASE_GENERATION",
        "SECURITY_ANALYSIS",
        "SEARCH",
    ]
)
EXPECTED_LANGUAGES = [
    "English",
    "Hindi",
    "Marathi",
    "Hinglish",
    "Marathi-English",
    "Hindi-English",
]

MIN_TEST_ACCURACY = 0.78
MIN_TEST_MACRO_F1 = 0.78


def load_test_split(filepath: str) -> Tuple[List[int], List[str], List[str], List[str]]:
    """Load IDs, texts, intent labels, and language varieties from test CSV."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Test CSV not found: '{filepath}'")

    ids: List[int] = []
    texts: List[str] = []
    intents: List[str] = []
    languages: List[str] = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            raw_id = row.get("id", "").strip()
            text = row.get("text", "").strip()
            intent = row.get("intent", "").strip()
            lang = row.get("language", "").strip()

            if not raw_id or not text or not intent or not lang:
                raise ValueError(f"File {filepath} row {idx}: missing required column")
            if intent not in EXPECTED_INTENTS:
                raise ValueError(f"File {filepath} row {idx}: unauthorized intent '{intent}'")

            ids.append(int(raw_id))
            texts.append(text)
            intents.append(intent)
            languages.append(lang)

    return ids, texts, intents, languages


def analyze_misclassification_reason(actual: str, pred: str, text: str) -> str:
    """Provide a linguistic or semantic hypothesis for the misclassification."""
    pair = {actual, pred}
    if pair == {"DEBUG_CODE", "ERROR_EXPLANATION"}:
        return "Boundary ambiguity: error keyword present without explicit command to fix vs understand."
    if pair == {"CODE_REVIEW", "CODE_SUGGESTION"}:
        return "Boundary ambiguity: review/critique overlaps with suggestion for function improvement."
    if pair == {"OPTIMIZE_CODE", "PERFORMANCE_ANALYSIS"}:
        return "Boundary overlap: performance diagnosis vs active speedup/efficiency request."
    if pair == {"ALGORITHM", "APPROACH_SUGGESTION"}:
        return "Methodology overlap: algorithmic choice framed as a solution approach."
    if pair == {"ALGORITHM", "CONCEPT"}:
        return "Theoretical overlap: algorithmic concept vs general computing principle."
    if pair == {"BEST_PRACTICE", "CODE_SUGGESTION"}:
        return "Normative overlap: general best practice vs code-specific tip."
    if pair == {"ARCHITECTURE_SUGGESTION", "FEATURE_SUGGESTION"}:
        return "Design overlap: structural project layout vs product capability proposal."
    if pair == {"EXPLAIN_CODE", "CONCEPT"}:
        return "Explanatory overlap: explanation of code construct vs theoretical concept definition."
    return f"Lexical feature overlap between {actual} and {pred}."


def main() -> int:
    print("=" * 60)
    print("Bhasha2Code Intent Classifier Test Evaluation (T13)")
    print("=" * 60)

    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at '{MODEL_PATH}'. Run train_intent_classifier.py first.")
        return 1

    pipeline = joblib.load(MODEL_PATH)
    print(f"Loaded pipeline from: {MODEL_PATH}")

    ids, texts, labels, langs = load_test_split(TEST_CSV)
    print(f"Loaded holdout test samples: {len(texts)}")

    # 1. Overall Metrics
    preds = pipeline.predict(texts)
    probs = pipeline.predict_proba(texts)

    acc = float(accuracy_score(labels, preds))
    macro_f1 = float(f1_score(labels, preds, average="macro"))
    weighted_f1 = float(f1_score(labels, preds, average="weighted"))

    print("\n--- Test Set Performance ---")
    print(f"Test Accuracy   : {acc:.4f} (target >= {MIN_TEST_ACCURACY})")
    print(f"Test Macro F1   : {macro_f1:.4f} (target >= {MIN_TEST_MACRO_F1})")
    print(f"Test Weighted F1: {weighted_f1:.4f}")

    # 2. Per-Class Metrics
    precision_cls, recall_cls, f1_cls, support_cls = precision_recall_fscore_support(
        labels, preds, labels=EXPECTED_INTENTS, zero_division=0
    )

    per_class = {}
    print("\n--- Per-Class Metrics ---")
    print(f"{'Intent':26} {'Precision':10} {'Recall':10} {'F1-Score':10} {'Support':8}")
    print("-" * 66)
    for idx, intent in enumerate(EXPECTED_INTENTS):
        p, r, f, s = (
            float(precision_cls[idx]),
            float(recall_cls[idx]),
            float(f1_cls[idx]),
            int(support_cls[idx]),
        )
        per_class[intent] = {
            "precision": round(p, 4),
            "recall": round(r, 4),
            "f1_score": round(f, 4),
            "support": s,
        }
        print(f"{intent:26} {p:10.4f} {r:10.4f} {f:10.4f} {s:8d}")

    # 3. Confusion Matrix
    cm = confusion_matrix(labels, preds, labels=EXPECTED_INTENTS).tolist()

    # 4. Error Analysis
    misclassifications = []
    for sample_id, text, actual, pred, prob, lang in zip(ids, texts, labels, preds, probs, langs):
        if actual != pred:
            conf = float(max(prob))
            reason = analyze_misclassification_reason(actual, pred, text)
            misclassifications.append(
                {
                    "id": sample_id,
                    "text": text,
                    "actual": actual,
                    "predicted": pred,
                    "confidence": round(conf, 4),
                    "language": lang,
                    "likely_reason": reason,
                }
            )

    print(f"\n--- Error Analysis ({len(misclassifications)} misclassifications / {len(texts)} total) ---")
    if misclassifications:
        for idx, err in enumerate(misclassifications, start=1):
            print(f"{idx}. [{err['language']}] \"{err['text']}\"")
            print(f"   Actual: {err['actual']} | Predicted: {err['predicted']} (Conf: {err['confidence']:.4f})")
            print(f"   Reason: {err['likely_reason']}")
    else:
        print("Zero misclassifications on holdout test set!")

    # 5. Language Breakdown
    print("\n--- Performance by Language Variety ---")
    lang_metrics = {}
    print(f"{'Language':18} {'Samples':8} {'Accuracy':10} {'Macro F1':10}")
    print("-" * 50)
    for target_lang in EXPECTED_LANGUAGES:
        lang_indices = [i for i, l in enumerate(langs) if l == target_lang]
        if not lang_indices:
            continue
        l_texts = [texts[i] for i in lang_indices]
        l_labels = [labels[i] for i in lang_indices]
        l_preds = [preds[i] for i in lang_indices]

        l_acc = float(accuracy_score(l_labels, l_preds))
        l_f1 = float(f1_score(l_labels, l_preds, average="macro", zero_division=0))
        lang_metrics[target_lang] = {
            "samples": len(lang_indices),
            "accuracy": round(l_acc, 4),
            "macro_f1": round(l_f1, 4),
        }
        print(f"{target_lang:18} {len(lang_indices):<8} {l_acc:10.4f} {l_f1:10.4f}")

    # 6. Confidence Analysis
    confidences = [float(max(p)) for p in probs]
    below_50 = sum(1 for c in confidences if c < 0.50)
    below_60 = sum(1 for c in confidences if c < 0.60)
    avg_conf = sum(confidences) / len(confidences)
    print("\n--- Confidence Analysis ---")
    print(f"Average confidence : {avg_conf:.4f}")
    print(f"Confidence < 0.50   : {below_50} ({below_50 / len(confidences) * 100:.1f}%)")
    print(f"Confidence < 0.60   : {below_60} ({below_60 / len(confidences) * 100:.1f}%)")

    # 7. Determinism Test
    test_sample = "mala linked list cha code debug karaycha aahe"
    runs = [str(pipeline.predict([test_sample])[0]) for _ in range(10)]
    assert all(r == runs[0] for r in runs), "Inference non-deterministic!"
    print(f"\nDeterminism check (10 runs on identical input): PASS (All predicted '{runs[0]}')")

    # 8. Update metadata.json with test metrics
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        metadata["test_metrics"] = {
            "accuracy": round(acc, 4),
            "macro_f1": round(macro_f1, 4),
            "weighted_f1": round(weighted_f1, 4),
            "per_class": per_class,
            "confusion_matrix": cm,
            "by_language": lang_metrics,
            "misclassification_count": len(misclassifications),
            "average_confidence": round(avg_conf, 4),
        }
        with open(METADATA_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"Updated metadata with test metrics at: {METADATA_PATH}")

    # Check targets
    if acc < MIN_TEST_ACCURACY or macro_f1 < MIN_TEST_MACRO_F1:
        print(f"\nFAIL: Test metrics below engineering targets (Acc >= {MIN_TEST_ACCURACY}, Macro F1 >= {MIN_TEST_MACRO_F1})")
        return 1

    print("\nIntent Classifier Evaluation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
