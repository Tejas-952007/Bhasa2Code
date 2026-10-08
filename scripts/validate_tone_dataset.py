#!/usr/bin/env python3
"""Dataset validation script for Bhasha2Code Tone Dataset (T10).

Validates schema, uniqueness, absence of nulls/empty entries, label distribution,
and language distribution across both CSV and JSONL formats. Exits with non-zero
status code if any verification fails.
"""

import csv
import json
import os
import sys
from typing import Dict, List, Set

REQUIRED_COLUMNS = ["id", "text", "tone", "language", "domain"]
ALLOWED_TONES = {"CASUAL", "FORMAL", "SIMPLE", "TECHNICAL", "SHORT", "DETAILED"}
ALLOWED_LANGUAGES = {
    "English",
    "Hindi",
    "Marathi",
    "Hinglish",
    "Marathi-English",
    "Hindi-English",
}
MIN_SAMPLE_COUNT = 300
DEFAULT_DATASET_CSV = os.path.join("data", "datasets", "tone", "tone_dataset.csv")
DEFAULT_DATASET_JSONL = os.path.join("data", "datasets", "tone", "tone_dataset.jsonl")


def validate_csv(filepath: str, min_samples: int = MIN_SAMPLE_COUNT) -> Dict:
    """Validate CSV tone dataset file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset CSV not found at '{filepath}'")

    rows: List[Dict] = []
    seen_ids: Set[int] = set()
    seen_texts: Set[str] = set()
    errors: List[str] = []
    tone_counts: Dict[str, int] = {}
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

            # Validate Tone
            tone = (row.get("tone") or "").strip()
            if tone not in ALLOWED_TONES:
                errors.append(f"Row {idx}: unauthorized tone label '{tone}'")
            tone_counts[tone] = tone_counts.get(tone, 0) + 1

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

    # Check for missing tones
    missing_tones = ALLOWED_TONES - set(tone_counts.keys())
    if missing_tones:
        errors.append(f"Tone labels missing from dataset: {missing_tones}")

    return {
        "filepath": filepath,
        "total_samples": len(rows),
        "unique_samples": len(seen_texts),
        "errors": errors,
        "tone_counts": tone_counts,
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


def main() -> int:
    csv_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DATASET_CSV
    jsonl_path = (
        sys.argv[2]
        if len(sys.argv) > 2
        else DEFAULT_DATASET_JSONL
    )

    try:
        report = validate_csv(csv_path)
    except Exception as exc:
        print(f"Tone Dataset Validation: FAIL\nError reading CSV: {exc}")
        return 1

    jsonl_errors = []
    if os.path.exists(jsonl_path):
        jsonl_errors = validate_jsonl(jsonl_path, report["total_samples"])

    all_errors = report["errors"] + jsonl_errors

    if all_errors:
        print("Tone Dataset Validation: FAIL\n")
        print(f"Total errors encountered: {len(all_errors)}")
        for err in all_errors[:20]:
            print(f" - {err}")
        if len(all_errors) > 20:
            print(f" ... and {len(all_errors) - 20} more errors.")
        return 1

    print("Tone Dataset Validation: PASS\n")
    print(f"Total samples: {report['total_samples']}")
    print(f"Unique samples: {report['unique_samples']}")
    print(f"Duplicate texts: 0")
    print(f"Invalid rows: 0")
    print(f"Text length: min={report['min_len']}, max={report['max_len']}, avg={report['avg_len']:.1f} chars\n")

    print("Samples Per Tone:")
    for tone in sorted(ALLOWED_TONES):
        count = report["tone_counts"].get(tone, 0)
        print(f" - {tone:12}: {count}")

    print("\nSamples Per Language:")
    for lang in sorted(ALLOWED_LANGUAGES):
        count = report["lang_counts"].get(lang, 0)
        print(f" - {lang:16}: {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
