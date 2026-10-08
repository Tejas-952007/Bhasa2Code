#!/usr/bin/env python3
"""Training script for Bhasha2Code Tone Classifier (T11).

Loads T10 dataset splits, validates data isolation (leakage check),
trains hybrid TF-IDF (word + char) with Logistic Regression,
evaluates on validation and final test sets, performs error analysis,
and persists model and metadata.
"""

import csv
from datetime import datetime, timezone
import json
import os
import sys
from typing import Dict, List, Set, Tuple

import joblib
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from sklearn.pipeline import FeatureUnion, Pipeline

TRAIN_CSV = os.path.join("data", "datasets", "tone", "tone_train.csv")
VAL_CSV = os.path.join("data", "datasets", "tone", "tone_validation.csv")
TEST_CSV = os.path.join("data", "datasets", "tone", "tone_test.csv")

MODEL_DIR = os.path.join("models", "tone")
MODEL_PATH = os.path.join(MODEL_DIR, "tone_classifier.joblib")
METADATA_PATH = os.path.join(MODEL_DIR, "metadata.json")

EXPECTED_TONES = sorted(["CASUAL", "FORMAL", "SIMPLE", "TECHNICAL", "SHORT", "DETAILED"])
RANDOM_STATE = 42

MIN_VAL_ACCURACY = 0.80
MIN_VAL_MACRO_F1 = 0.80
MIN_TEST_ACCURACY = 0.78
MIN_TEST_MACRO_F1 = 0.78


def load_split(filepath: str) -> Tuple[List[int], List[str], List[str]]:
    """Load IDs, texts, and tone labels from CSV split."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Split file not found: '{filepath}'")

    ids: List[int] = []
    texts: List[str] = []
    labels: List[str] = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            raw_id = row.get("id", "").strip()
            text = row.get("text", "").strip()
            tone = row.get("tone", "").strip()

            if not raw_id or not text or not tone:
                raise ValueError(f"File {filepath} line {idx}: empty id, text, or tone")
            if tone not in EXPECTED_TONES:
                raise ValueError(f"File {filepath} line {idx}: unauthorized tone '{tone}'")

            ids.append(int(raw_id))
            texts.append(text)
            labels.append(tone)

    return ids, texts, labels


def check_leakage(
    train_ids: List[int],
    train_texts: List[str],
    val_ids: List[int],
    val_texts: List[str],
    test_ids: List[int],
    test_texts: List[str],
) -> None:
    """Ensure strict isolation across train, validation, and test splits."""
    train_id_set, val_id_set, test_id_set = set(train_ids), set(val_ids), set(test_ids)
    train_text_set, val_text_set, test_text_set = set(train_texts), set(val_texts), set(test_texts)

    # Check ID overlaps
    if not train_id_set.isdisjoint(val_id_set):
        raise ValueError(f"Data leakage: train and val share IDs: {train_id_set & val_id_set}")
    if not train_id_set.isdisjoint(test_id_set):
        raise ValueError(f"Data leakage: train and test share IDs: {train_id_set & test_id_set}")
    if not val_id_set.isdisjoint(test_id_set):
        raise ValueError(f"Data leakage: val and test share IDs: {val_id_set & test_id_set}")

    # Check text overlaps
    if not train_text_set.isdisjoint(val_text_set):
        raise ValueError(f"Data leakage: train and val share texts: {train_text_set & val_text_set}")
    if not train_text_set.isdisjoint(test_text_set):
        raise ValueError(f"Data leakage: train and test share texts: {train_text_set & test_text_set}")
    if not val_text_set.isdisjoint(test_text_set):
        raise ValueError(f"Data leakage: val and test share texts: {val_text_set & test_text_set}")


def build_pipeline() -> Pipeline:
    """Build the hybrid TF-IDF + Logistic Regression classification pipeline."""
    feature_union = FeatureUnion(
        [
            (
                "word_tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=1,
                    sublinear_tf=True,
                ),
            ),
            (
                "char_tfidf",
                TfidfVectorizer(
                    analyzer="char_wb",
                    ngram_range=(3, 5),
                    min_df=1,
                    sublinear_tf=True,
                ),
            ),
        ]
    )

    clf = LogisticRegression(
        C=3.0,
        max_iter=1000,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        solver="lbfgs",
    )

    return Pipeline([("features", feature_union), ("classifier", clf)])


def evaluate_split(
    pipeline: Pipeline, texts: List[str], labels: List[str], split_name: str
) -> Dict:
    """Evaluate pipeline on a dataset split and return metrics dict."""
    preds = pipeline.predict(texts)
    probs = pipeline.predict_proba(texts)

    acc = float(accuracy_score(labels, preds))
    macro_f1 = float(f1_score(labels, preds, average="macro"))
    weighted_f1 = float(f1_score(labels, preds, average="weighted"))

    # Per-class metrics
    precision_cls, recall_cls, f1_cls, support_cls = precision_recall_fscore_support(
        labels, preds, labels=EXPECTED_TONES, zero_division=0
    )

    per_class = {}
    for idx, tone in enumerate(EXPECTED_TONES):
        per_class[tone] = {
            "precision": float(round(precision_cls[idx], 4)),
            "recall": float(round(recall_cls[idx], 4)),
            "f1_score": float(round(f1_cls[idx], 4)),
            "support": int(support_cls[idx]),
        }

    cm = confusion_matrix(labels, preds, labels=EXPECTED_TONES).tolist()

    # Find misclassifications for error analysis
    misclassified = []
    for text, actual, pred, prob in zip(texts, labels, preds, probs):
        if actual != pred:
            misclassified.append(
                {
                    "text": text,
                    "actual": actual,
                    "predicted": pred,
                    "confidence": float(round(max(prob), 4)),
                }
            )

    return {
        "split": split_name,
        "sample_count": len(texts),
        "accuracy": round(acc, 4),
        "macro_f1": round(macro_f1, 4),
        "weighted_f1": round(weighted_f1, 4),
        "per_class": per_class,
        "confusion_matrix": cm,
        "misclassified": misclassified,
    }


def main() -> int:
    print("=" * 60)
    print("Bhasha2Code Tone Classifier Training (T11)")
    print("=" * 60)

    # 1. Load data
    train_ids, train_texts, train_labels = load_split(TRAIN_CSV)
    val_ids, val_texts, val_labels = load_split(VAL_CSV)
    test_ids, test_texts, test_labels = load_split(TEST_CSV)

    print(f"Loaded train samples     : {len(train_texts)}")
    print(f"Loaded validation samples: {len(val_texts)}")
    print(f"Loaded test samples      : {len(test_texts)}")

    # 2. Leakage checks
    check_leakage(train_ids, train_texts, val_ids, val_texts, test_ids, test_texts)
    print("Leakage verification passed: zero overlap across train, val, and test splits.")

    # 3. Train model
    pipeline = build_pipeline()
    print("Fitting hybrid TF-IDF + LogisticRegression pipeline...")
    pipeline.fit(train_texts, train_labels)

    # 4. Evaluate Validation split
    val_metrics = evaluate_split(pipeline, val_texts, val_labels, "validation")
    print("\n--- Validation Evaluation ---")
    print(f"Validation Accuracy: {val_metrics['accuracy']:.4f} (target >= {MIN_VAL_ACCURACY})")
    print(f"Validation Macro F1: {val_metrics['macro_f1']:.4f} (target >= {MIN_VAL_MACRO_F1})")
    print(f"Validation Weighted F1: {val_metrics['weighted_f1']:.4f}")

    if val_metrics["accuracy"] < MIN_VAL_ACCURACY or val_metrics["macro_f1"] < MIN_VAL_MACRO_F1:
        print("FAIL: Validation metrics did not meet required thresholds!")
        return 1

    # 5. Evaluate Test split
    test_metrics = evaluate_split(pipeline, test_texts, test_labels, "test")
    print("\n--- Test Evaluation (Final Untouched Holdout) ---")
    print(f"Test Accuracy: {test_metrics['accuracy']:.4f} (target >= {MIN_TEST_ACCURACY})")
    print(f"Test Macro F1: {test_metrics['macro_f1']:.4f} (target >= {MIN_TEST_MACRO_F1})")
    print(f"Test Weighted F1: {test_metrics['weighted_f1']:.4f}")

    if test_metrics["accuracy"] < MIN_TEST_ACCURACY or test_metrics["macro_f1"] < MIN_TEST_MACRO_F1:
        print("FAIL: Test metrics did not meet required thresholds!")
        return 1

    print("\nPer-Class Metrics (Test):")
    print(f"{'Tone':12} {'Precision':10} {'Recall':10} {'F1-Score':10} {'Support':8}")
    print("-" * 52)
    for tone, m in test_metrics["per_class"].items():
        print(f"{tone:12} {m['precision']:<10.4f} {m['recall']:<10.4f} {m['f1_score']:<10.4f} {m['support']:<8}")

    print("\nConfusion Matrix (Test):")
    print("Labels:", EXPECTED_TONES)
    for row in test_metrics["confusion_matrix"]:
        print(row)

    # 6. Error Analysis
    print("\n--- Error Analysis ---")
    all_misclassified = val_metrics["misclassified"] + test_metrics["misclassified"]
    print(f"Total validation misclassifications: {len(val_metrics['misclassified'])}")
    print(f"Total test misclassifications      : {len(test_metrics['misclassified'])}")
    for item in all_misclassified:
        print(
            f" - text='{item['text']}' | actual={item['actual']} | predicted={item['predicted']} | conf={item['confidence']:.4f}"
        )

    # 7. Persist Model and Metadata
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nModel artifact saved to: {MODEL_PATH}")

    metadata = {
        "task": "tone_classification",
        "model": "tfidf_logistic_regression",
        "model_version": "1.0.0",
        "labels": EXPECTED_TONES,
        "train_samples": len(train_texts),
        "validation_samples": len(val_texts),
        "test_samples": len(test_texts),
        "random_state": RANDOM_STATE,
        "features": {
            "word_ngram_range": [1, 2],
            "char_ngram_range": [3, 5],
            "sublinear_tf": True,
        },
        "classifier_params": {
            "C": 3.0,
            "max_iter": 1000,
            "solver": "lbfgs",
            "class_weight": "balanced",
        },
        "dependencies": {
            "scikit-learn": sklearn.__version__,
            "joblib": joblib.__version__,
        },
        "training_timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": {
            "validation": {
                "accuracy": val_metrics["accuracy"],
                "macro_f1": val_metrics["macro_f1"],
                "weighted_f1": val_metrics["weighted_f1"],
                "per_class": val_metrics["per_class"],
                "confusion_matrix": val_metrics["confusion_matrix"],
            },
            "test": {
                "accuracy": test_metrics["accuracy"],
                "macro_f1": test_metrics["macro_f1"],
                "weighted_f1": test_metrics["weighted_f1"],
                "per_class": test_metrics["per_class"],
                "confusion_matrix": test_metrics["confusion_matrix"],
            },
        },
        "dataset_sources": {
            "train": TRAIN_CSV,
            "validation": VAL_CSV,
            "test": TEST_CSV,
        },
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Metadata saved to      : {METADATA_PATH}")

    print("\nTone Classifier Training: SUCCESS (ALL TARGETS MET)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
