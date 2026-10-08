#!/usr/bin/env python3
"""Training script for Bhasha2Code Intent Classifier (T13).

Loads T12 dataset splits, validates data isolation (leakage check),
trains hybrid TF-IDF (word + char) with Logistic Regression,
evaluates on validation set, performs boundary and tone-independence checks,
and persists model and metadata to models/intent/.
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

TRAIN_CSV = os.path.join("data", "datasets", "intent", "intent_train.csv")
VAL_CSV = os.path.join("data", "datasets", "intent", "intent_validation.csv")
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
RANDOM_STATE = 42

MIN_VAL_ACCURACY = 0.80
MIN_VAL_MACRO_F1 = 0.80


def load_split(filepath: str) -> Tuple[List[int], List[str], List[str], List[str]]:
    """Load IDs, texts, intent labels, and language categories from CSV split."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Split file not found: '{filepath}'")

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
                raise ValueError(f"File {filepath} line {idx}: empty id, text, intent, or language")
            if intent not in EXPECTED_INTENTS:
                raise ValueError(f"File {filepath} line {idx}: unauthorized intent '{intent}'")

            ids.append(int(raw_id))
            texts.append(text)
            intents.append(intent)
            languages.append(lang)

    return ids, texts, intents, languages


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
    train_text_set = {t.strip().lower() for t in train_texts}
    val_text_set = {t.strip().lower() for t in val_texts}
    test_text_set = {t.strip().lower() for t in test_texts}

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
    """Build the hybrid TF-IDF (word + char) + Logistic Regression classification pipeline."""
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

    precision_cls, recall_cls, f1_cls, support_cls = precision_recall_fscore_support(
        labels, preds, labels=EXPECTED_INTENTS, zero_division=0
    )

    per_class = {}
    for idx, intent in enumerate(EXPECTED_INTENTS):
        per_class[intent] = {
            "precision": float(round(precision_cls[idx], 4)),
            "recall": float(round(recall_cls[idx], 4)),
            "f1_score": float(round(f1_cls[idx], 4)),
            "support": int(support_cls[idx]),
        }

    cm = confusion_matrix(labels, preds, labels=EXPECTED_INTENTS).tolist()

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


def evaluate_boundary_cases(pipeline: Pipeline) -> List[Dict]:
    """Test critical ambiguous intent boundaries."""
    boundary_cases = [
        # DEBUG_CODE vs ERROR_EXPLANATION
        ("Why does this IndexError occur?", "ERROR_EXPLANATION"),
        ("Fix this IndexError in my Python script.", "DEBUG_CODE"),
        ("Explain why this KeyError happens and fix the code.", "DEBUG_CODE"),
        # DEBUG_CODE vs CODE_REVIEW
        ("Fix this bug in my binary search implementation.", "DEBUG_CODE"),
        ("Review this binary search code and check overall quality.", "CODE_REVIEW"),
        # CODE_SUGGESTION vs OPTIMIZE_CODE
        ("What improvements can I make to this function?", "CODE_SUGGESTION"),
        ("Make this function execute faster and reduce memory.", "OPTIMIZE_CODE"),
        # PERFORMANCE_ANALYSIS vs OPTIMIZE_CODE
        ("Why is this code slow? Profile the execution.", "PERFORMANCE_ANALYSIS"),
        ("Optimize this code to run faster.", "OPTIMIZE_CODE"),
        # ALGORITHM vs CONCEPT
        ("How does Dijkstra's algorithm work?", "ALGORITHM"),
        ("What is polymorphism in object oriented programming?", "CONCEPT"),
        # APPROACH_SUGGESTION vs ALGORITHM
        ("What approach should I use to solve this two-sum problem?", "APPROACH_SUGGESTION"),
        ("Which sorting algorithm is best for small arrays?", "ALGORITHM"),
        # ARCHITECTURE_SUGGESTION vs FEATURE_SUGGESTION
        ("How should I structure the microservices backend?", "ARCHITECTURE_SUGGESTION"),
        ("What features should I add to my coding assistant app?", "FEATURE_SUGGESTION"),
        # BEST_PRACTICE vs CODE_SUGGESTION
        ("What is the best practice for exception handling in Python?", "BEST_PRACTICE"),
        ("How can I improve this specific function implementation?", "CODE_SUGGESTION"),
        # SEARCH vs CONCEPT
        ("What is recursion?", "CONCEPT"),
        ("Find my previous Python script where we discussed recursion.", "SEARCH"),
    ]

    results = []
    for text, expected in boundary_cases:
        pred = str(pipeline.predict([text])[0])
        prob = float(max(pipeline.predict_proba([text])[0]))
        results.append(
            {
                "text": text,
                "expected": expected,
                "predicted": pred,
                "confidence": round(prob, 4),
                "match": pred == expected,
            }
        )
    return results


def evaluate_tone_independence(pipeline: Pipeline) -> List[Dict]:
    """Verify that intent prediction remains robust across different conversational tones."""
    tone_variations = [
        # EXPLAIN_CODE across tones
        ("Please explain this Python function.", "EXPLAIN_CODE", "FORMAL"),
        ("bro ha code samjhav na", "EXPLAIN_CODE", "CASUAL"),
        ("simple language madhe ha code explain kar", "EXPLAIN_CODE", "SIMPLE"),
        ("give a detailed step by step explanation of this code", "EXPLAIN_CODE", "DETAILED"),
        # GENERATE_CODE across tones
        ("Kindly write a Python program for calculator.", "GENERATE_CODE", "FORMAL"),
        ("bro calculator cha code de na", "GENERATE_CODE", "CASUAL"),
        ("only give the calculator code, nothing else", "GENERATE_CODE", "SHORT"),
        # DEBUG_CODE across tones
        ("Please debug this function and resolve the exception.", "DEBUG_CODE", "FORMAL"),
        ("yaar ye code fix kar de crash ho raha hai", "DEBUG_CODE", "CASUAL"),
        ("fakt ha error fix karun de", "DEBUG_CODE", "SHORT"),
    ]

    results = []
    for text, expected_intent, tone_desc in tone_variations:
        pred = str(pipeline.predict([text])[0])
        prob = float(max(pipeline.predict_proba([text])[0]))
        results.append(
            {
                "text": text,
                "expected_intent": expected_intent,
                "tone_style": tone_desc,
                "predicted_intent": pred,
                "confidence": round(prob, 4),
                "match": pred == expected_intent,
            }
        )
    return results


def main() -> int:
    print("=" * 60)
    print("Bhasha2Code Intent Classifier Training (T13)")
    print("=" * 60)

    # 1. Load data
    train_ids, train_texts, train_intents, train_langs = load_split(TRAIN_CSV)
    val_ids, val_texts, val_intents, val_langs = load_split(VAL_CSV)
    test_ids, test_texts, test_intents, test_langs = load_split(TEST_CSV)

    print(f"Loaded train samples     : {len(train_texts)}")
    print(f"Loaded validation samples: {len(val_texts)}")
    print(f"Loaded test samples      : {len(test_texts)}")

    # 2. Leakage checks
    check_leakage(train_ids, train_texts, val_ids, val_texts, test_ids, test_texts)
    print("Leakage verification passed: zero overlap across train, val, and test splits.")

    # 3. Train model
    pipeline = build_pipeline()
    print("Fitting hybrid TF-IDF (word + char) + LogisticRegression pipeline...")
    pipeline.fit(train_texts, train_intents)

    # 4. Evaluate Validation split
    val_metrics = evaluate_split(pipeline, val_texts, val_intents, "validation")
    print("\n--- Validation Evaluation ---")
    print(f"Validation Accuracy: {val_metrics['accuracy']:.4f} (target >= {MIN_VAL_ACCURACY})")
    print(f"Validation Macro F1: {val_metrics['macro_f1']:.4f} (target >= {MIN_VAL_MACRO_F1})")
    print(f"Validation Weighted F1: {val_metrics['weighted_f1']:.4f}")

    if val_metrics["accuracy"] < MIN_VAL_ACCURACY or val_metrics["macro_f1"] < MIN_VAL_MACRO_F1:
        print(f"\nERROR: Validation targets not met (Accuracy >= {MIN_VAL_ACCURACY}, Macro F1 >= {MIN_VAL_MACRO_F1})")
        return 1

    # 5. Evaluate boundary and tone independence cases
    boundary_results = evaluate_boundary_cases(pipeline)
    boundary_passes = sum(1 for b in boundary_results if b["match"])
    print(f"\nBoundary tests: {boundary_passes}/{len(boundary_results)} passed")

    tone_results = evaluate_tone_independence(pipeline)
    tone_passes = sum(1 for t in tone_results if t["match"])
    print(f"Tone independence tests: {tone_passes}/{len(tone_results)} passed")

    # 6. Persist model and metadata
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"\nModel saved:\n{MODEL_PATH}")

    metadata = {
        "task": "intent_classification",
        "model": "tfidf_logistic_regression",
        "model_version": "1.0.0",
        "num_classes": len(EXPECTED_INTENTS),
        "labels": EXPECTED_INTENTS,
        "train_samples": len(train_texts),
        "validation_samples": len(val_texts),
        "test_samples": len(test_texts),
        "random_state": RANDOM_STATE,
        "features": {
            "word_ngram_range": [1, 2],
            "char_ngram_range": [3, 5],
            "char_analyzer": "char_wb",
            "sublinear_tf": True,
        },
        "hyperparameters": {
            "C": 3.0,
            "class_weight": "balanced",
            "max_iter": 1000,
            "solver": "lbfgs",
            "random_state": RANDOM_STATE,
        },
        "dataset_paths": {
            "train": TRAIN_CSV,
            "validation": VAL_CSV,
            "test": TEST_CSV,
        },
        "validation_metrics": {
            "accuracy": val_metrics["accuracy"],
            "macro_f1": val_metrics["macro_f1"],
            "weighted_f1": val_metrics["weighted_f1"],
            "per_class": val_metrics["per_class"],
        },
        "boundary_tests_pass_rate": round(boundary_passes / len(boundary_results), 4),
        "tone_independence_pass_rate": round(tone_passes / len(tone_results), 4),
        "scikit_learn_version": sklearn.__version__,
        "trained_at": datetime.now(timezone.utc).isoformat(),
    }

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Metadata saved:\n{METADATA_PATH}")

    print("\nIntent Classifier Training: SUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
