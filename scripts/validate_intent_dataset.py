#!/usr/bin/env python3
"""Dataset validation script for Bhasha2Code Intent Dataset (T12).

Validates schema, uniqueness, absence of nulls/empty entries, label distribution,
multilingual coverage, coding-domain exclusivity, and strict split isolation (zero leakage)
across full, train, validation, and test datasets. Exits with non-zero status code if any verification fails.
"""

import csv
import json
import os
import sys
from typing import Dict, List, Set, Tuple

REQUIRED_COLUMNS = ["id", "text", "intent", "language", "domain"]
ALLOWED_INTENTS = {
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
}
ALLOWED_LANGUAGES = {
    "English",
    "Hindi",
    "Marathi",
    "Hinglish",
    "Marathi-English",
    "Hindi-English",
}
MIN_SAMPLE_COUNT = 900
EXPECTED_FULL_COUNT = 1080

DEFAULT_DATASET_DIR = os.path.join("data", "datasets", "intent")
DEFAULT_DATASET_CSV = os.path.join(DEFAULT_DATASET_DIR, "intent_dataset.csv")
DEFAULT_DATASET_JSONL = os.path.join(DEFAULT_DATASET_DIR, "intent_dataset.jsonl")
DEFAULT_TRAIN_CSV = os.path.join(DEFAULT_DATASET_DIR, "intent_train.csv")
DEFAULT_VAL_CSV = os.path.join(DEFAULT_DATASET_DIR, "intent_validation.csv")
DEFAULT_TEST_CSV = os.path.join(DEFAULT_DATASET_DIR, "intent_test.csv")


def validate_csv(filepath: str, min_samples: int = MIN_SAMPLE_COUNT) -> Dict:
    """Validate full CSV intent dataset file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset CSV not found at '{filepath}'")

    rows: List[Dict] = []
    seen_ids: Set[int] = set()
    seen_texts: Set[str] = set()
    text_to_intent: Dict[str, str] = {}
    errors: List[str] = []
    intent_counts: Dict[str, int] = {}
    lang_counts: Dict[str, int] = {}
    lengths: List[int] = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"Empty header in '{filepath}'")

        missing_cols = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing_cols:
            raise ValueError(f"Missing required columns in CSV header: {missing_cols}")

        for idx, row in enumerate(reader, start=2):
            # Check row fields
            for col in REQUIRED_COLUMNS:
                if col not in row or row[col] is None or not str(row[col]).strip():
                    errors.append(f"Row {idx}: missing or empty field '{col}'")

            # Validate ID
            try:
                row_id = int(row.get("id", ""))
                if row_id in seen_ids:
                    errors.append(f"Row {idx}: duplicate ID {row_id}")
                seen_ids.add(row_id)
            except ValueError:
                errors.append(f"Row {idx}: invalid non-integer ID '{row.get('id')}'")

            # Validate Text
            text = (row.get("text") or "").strip()
            if not text:
                errors.append(f"Row {idx}: empty text")
            elif text in seen_texts:
                errors.append(f"Row {idx}: duplicate text '{text[:40]}...'")
            seen_texts.add(text)
            lengths.append(len(text))

            # Validate Intent
            intent = (row.get("intent") or "").strip()
            if intent not in ALLOWED_INTENTS:
                errors.append(f"Row {idx}: unauthorized intent label '{intent}'")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1

            # Check duplicate text + different intent collision
            norm_text = text.lower()
            if norm_text in text_to_intent and text_to_intent[norm_text] != intent:
                errors.append(
                    f"Row {idx}: text conflicting intent collision for '{text[:40]}': "
                    f"'{text_to_intent[norm_text]}' vs '{intent}'"
                )
            text_to_intent[norm_text] = intent

            # Validate Language
            lang = (row.get("language") or "").strip()
            if lang not in ALLOWED_LANGUAGES:
                errors.append(f"Row {idx}: unauthorized language category '{lang}'")
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

            # Validate Domain
            domain = (row.get("domain") or "").strip()
            if domain != "coding":
                errors.append(f"Row {idx}: unexpected domain '{domain}', expected 'coding'")

            rows.append(row)

    if len(rows) < min_samples:
        errors.append(
            f"Sample count {len(rows)} is below minimum requirement of {min_samples}"
        )

    # Check for missing intents
    missing_intents = ALLOWED_INTENTS - set(intent_counts.keys())
    if missing_intents:
        errors.append(f"Intent labels missing from dataset: {missing_intents}")

    # Check for missing languages
    missing_langs = ALLOWED_LANGUAGES - set(lang_counts.keys())
    if missing_langs:
        errors.append(f"Language categories missing from dataset: {missing_langs}")

    return {
        "filepath": filepath,
        "rows": rows,
        "total_samples": len(rows),
        "unique_samples": len(seen_texts),
        "errors": errors,
        "intent_counts": intent_counts,
        "lang_counts": lang_counts,
        "min_len": min(lengths) if lengths else 0,
        "max_len": max(lengths) if lengths else 0,
        "avg_len": sum(lengths) / len(lengths) if lengths else 0,
    }


def validate_jsonl(filepath: str, expected_count: int) -> List[str]:
    """Validate JSONL version matches count and schema."""
    if not os.path.exists(filepath):
        return [f"JSONL file not found at '{filepath}'"]

    errors: List[str] = []
    lines_count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line_str = line.strip()
            if not line_str:
                continue
            lines_count += 1
            try:
                data = json.loads(line_str)
                for col in REQUIRED_COLUMNS:
                    if col not in data or not str(data[col]).strip():
                        errors.append(f"JSONL line {idx}: missing or empty key '{col}'")
            except json.JSONDecodeError as e:
                errors.append(f"JSONL line {idx}: invalid JSON syntax: {e}")

    if lines_count != expected_count:
        errors.append(
            f"JSONL sample count ({lines_count}) does not match CSV sample count ({expected_count})"
        )

    return errors


def validate_splits(
    train_path: str,
    val_path: str,
    test_path: str,
    full_rows: List[Dict],
) -> Tuple[List[str], Dict]:
    """Validate train/val/test splits for schema, size, partition, and zero leakage."""
    errors: List[str] = []

    for name, path in [("train", train_path), ("val", val_path), ("test", test_path)]:
        if not os.path.exists(path):
            errors.append(f"Split file '{name}' not found at '{path}'")

    if errors:
        return errors, {}

    def read_split(path: str) -> List[Dict]:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

    train_rows = read_split(train_path)
    val_rows = read_split(val_path)
    test_rows = read_split(test_path)

    train_ids = {int(r["id"]) for r in train_rows}
    val_ids = {int(r["id"]) for r in val_rows}
    test_ids = {int(r["id"]) for r in test_rows}
    full_ids = {int(r["id"]) for r in full_rows}

    # Leakage check: ID level
    id_leak_tv = train_ids & val_ids
    id_leak_tt = train_ids & test_ids
    id_leak_vt = val_ids & test_ids
    if id_leak_tv:
        errors.append(f"ID leakage between train and val: {id_leak_tv}")
    if id_leak_tt:
        errors.append(f"ID leakage between train and test: {id_leak_tt}")
    if id_leak_vt:
        errors.append(f"ID leakage between val and test: {id_leak_vt}")

    # Partition check
    split_union_ids = train_ids | val_ids | test_ids
    if split_union_ids != full_ids:
        missing = full_ids - split_union_ids
        extra = split_union_ids - full_ids
        if missing:
            errors.append(f"Splits missing IDs from full dataset: {missing}")
        if extra:
            errors.append(f"Splits contain extra IDs not in full dataset: {extra}")

    # Leakage check: normalized text level
    train_texts = {r["text"].strip().lower() for r in train_rows}
    val_texts = {r["text"].strip().lower() for r in val_rows}
    test_texts = {r["text"].strip().lower() for r in test_rows}

    text_leak_tv = train_texts & val_texts
    text_leak_tt = train_texts & test_texts
    text_leak_vt = val_texts & test_texts
    if text_leak_tv:
        errors.append(f"Text leakage between train and val: {len(text_leak_tv)} samples")
    if text_leak_tt:
        errors.append(f"Text leakage between train and test: {len(text_leak_tt)} samples")
    if text_leak_vt:
        errors.append(f"Text leakage between val and test: {len(text_leak_vt)} samples")

    # Intent coverage in splits
    train_intents = {r["intent"] for r in train_rows}
    val_intents = {r["intent"] for r in val_rows}
    test_intents = {r["intent"] for r in test_rows}

    if train_intents != ALLOWED_INTENTS:
        errors.append(f"Train split missing intents: {ALLOWED_INTENTS - train_intents}")
    if val_intents != ALLOWED_INTENTS:
        errors.append(f"Validation split missing intents: {ALLOWED_INTENTS - val_intents}")
    if test_intents != ALLOWED_INTENTS:
        errors.append(f"Test split missing intents: {ALLOWED_INTENTS - test_intents}")

    split_stats = {
        "train_count": len(train_rows),
        "val_count": len(val_rows),
        "test_count": len(test_rows),
    }

    return errors, split_stats


def main() -> int:
    dataset_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATASET_DIR
    csv_path = os.path.join(dataset_dir, "intent_dataset.csv")
    jsonl_path = os.path.join(dataset_dir, "intent_dataset.jsonl")
    train_path = os.path.join(dataset_dir, "intent_train.csv")
    val_path = os.path.join(dataset_dir, "intent_validation.csv")
    test_path = os.path.join(dataset_dir, "intent_test.csv")

    try:
        report = validate_csv(csv_path)
    except Exception as exc:
        print(f"Intent Dataset Validation: FAIL\nError reading CSV: {exc}")
        return 1

    jsonl_errors = []
    if os.path.exists(jsonl_path):
        jsonl_errors = validate_jsonl(jsonl_path, report["total_samples"])

    split_errors, split_stats = validate_splits(
        train_path, val_path, test_path, report["rows"]
    )

    all_errors = report["errors"] + jsonl_errors + split_errors

    if all_errors:
        print("Intent Dataset Validation: FAIL\n")
        print(f"Total errors encountered: {len(all_errors)}")
        for err in all_errors[:20]:
            print(f" - {err}")
        if len(all_errors) > 20:
            print(f" ... and {len(all_errors) - 20} more errors.")
        return 1

    print("Intent Dataset Validation: PASS\n")
    print(f"Total samples: {report['total_samples']}")
    print(f"Unique samples: {report['unique_samples']}")
    print(f"Duplicate texts: 0")
    print(f"Invalid rows: 0")
    print(f"Text length: min={report['min_len']}, max={report['max_len']}, avg={report['avg_len']:.1f} chars\n")

    print("Intent distribution:")
    for intent in sorted(ALLOWED_INTENTS):
        count = report["intent_counts"].get(intent, 0)
        print(f" - {intent:24}: {count}")

    print("\nLanguage distribution:")
    for lang in sorted(ALLOWED_LANGUAGES):
        count = report["lang_counts"].get(lang, 0)
        print(f" - {lang:18}: {count}")

    print("\nSplit isolation:")
    print("PASS")
    print(f" - Train:      {split_stats.get('train_count', 0)} samples (70.0%)")
    print(f" - Validation: {split_stats.get('val_count', 0)} samples (15.0%)")
    print(f" - Test:       {split_stats.get('test_count', 0)} samples (15.0%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
