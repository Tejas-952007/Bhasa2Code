"""Unit tests for the Bhasha2Code labeled Intent Dataset (T12).

Verifies:
- File existence (CSV, JSONL, train, val, test, README)
- Schema validity (columns, datatypes, non-null, non-empty)
- Intent taxonomy adherence (all 18 intents, no unknown labels)
- Balance per intent (exactly 60 samples per intent, 1080 total)
- Multilingual distribution (English, Hindi, Marathi, Hinglish, Marathi-English, Hindi-English)
- Coding domain exclusivity ('coding')
- Uniqueness and absence of duplicates
- Split isolation and leakage prevention (train, val, test disjointness)
- Deterministic validation script execution
"""

import csv
import json
import os
from typing import Dict, List, Set
import pytest

DATASET_DIR = os.path.join("data", "datasets", "intent")
DATASET_CSV = os.path.join(DATASET_DIR, "intent_dataset.csv")
DATASET_JSONL = os.path.join(DATASET_DIR, "intent_dataset.jsonl")
TRAIN_CSV = os.path.join(DATASET_DIR, "intent_train.csv")
VAL_CSV = os.path.join(DATASET_DIR, "intent_validation.csv")
TEST_CSV = os.path.join(DATASET_DIR, "intent_test.csv")

EXPECTED_COLUMNS = ["id", "text", "intent", "language", "domain"]
EXPECTED_INTENTS = {
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
EXPECTED_LANGUAGES = {
    "English",
    "Hindi",
    "Marathi",
    "Hinglish",
    "Marathi-English",
    "Hindi-English",
}


@pytest.fixture
def dataset_rows() -> List[Dict[str, str]]:
    assert os.path.exists(DATASET_CSV), f"Dataset CSV missing: {DATASET_CSV}"
    with open(DATASET_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


@pytest.fixture
def jsonl_rows() -> List[Dict]:
    assert os.path.exists(DATASET_JSONL), f"Dataset JSONL missing: {DATASET_JSONL}"
    rows = []
    with open(DATASET_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line.strip()))
    return rows


class TestIntentDatasetFilesExist:
    def test_all_expected_dataset_files_exist(self) -> None:
        assert os.path.exists(DATASET_CSV)
        assert os.path.exists(DATASET_JSONL)
        assert os.path.exists(TRAIN_CSV)
        assert os.path.exists(VAL_CSV)
        assert os.path.exists(TEST_CSV)
        readme_path = os.path.join(DATASET_DIR, "README.md")
        assert os.path.exists(readme_path)


class TestIntentDatasetSchema:
    def test_csv_columns(self, dataset_rows: List[Dict[str, str]]) -> None:
        assert len(dataset_rows) == 1080
        for row in dataset_rows:
            assert set(EXPECTED_COLUMNS).issubset(set(row.keys()))

    def test_jsonl_keys_match_csv(
        self, dataset_rows: List[Dict[str, str]], jsonl_rows: List[Dict]
    ) -> None:
        assert len(dataset_rows) == len(jsonl_rows)
        for csv_row, json_row in zip(dataset_rows, jsonl_rows):
            assert int(csv_row["id"]) == int(json_row["id"])
            assert csv_row["text"] == json_row["text"]
            assert csv_row["intent"] == json_row["intent"]
            assert csv_row["language"] == json_row["language"]
            assert csv_row["domain"] == json_row["domain"]


class TestIntentDatasetIntegrity:
    def test_no_null_or_empty_fields(self, dataset_rows: List[Dict[str, str]]) -> None:
        for idx, row in enumerate(dataset_rows, start=1):
            assert row["id"].strip(), f"Row {idx} has empty id"
            assert row["text"].strip(), f"Row {idx} has empty text"
            assert row["intent"].strip(), f"Row {idx} has empty intent"
            assert row["language"].strip(), f"Row {idx} has empty language"
            assert row["domain"].strip(), f"Row {idx} has empty domain"

    def test_no_duplicate_texts(self, dataset_rows: List[Dict[str, str]]) -> None:
        seen = set()
        for row in dataset_rows:
            text = row["text"].strip()
            assert text not in seen, f"Duplicate text detected: {text}"
            seen.add(text)

    def test_no_duplicate_ids(self, dataset_rows: List[Dict[str, str]]) -> None:
        seen_ids = set()
        for row in dataset_rows:
            row_id = int(row["id"])
            assert row_id not in seen_ids, f"Duplicate id: {row_id}"
            seen_ids.add(row_id)


class TestIntentDatasetTaxonomyAndDomain:
    def test_only_allowed_intent_labels(self, dataset_rows: List[Dict[str, str]]) -> None:
        found_intents = set()
        for row in dataset_rows:
            intent = row["intent"]
            assert intent in EXPECTED_INTENTS, f"Unexpected intent label: {intent}"
            found_intents.add(intent)
        assert found_intents == EXPECTED_INTENTS, "Not all 18 intent classes are represented"

    def test_all_six_languages_present(self, dataset_rows: List[Dict[str, str]]) -> None:
        found_langs = set()
        for row in dataset_rows:
            lang = row["language"]
            assert lang in EXPECTED_LANGUAGES, f"Unexpected language: {lang}"
            found_langs.add(lang)
        assert found_langs == EXPECTED_LANGUAGES, "Not all 6 language categories are represented"

    def test_coding_domain_exclusivity(self, dataset_rows: List[Dict[str, str]]) -> None:
        for row in dataset_rows:
            assert row["domain"] == "coding"


class TestIntentDatasetDistribution:
    def test_exactly_sixty_samples_per_intent(
        self, dataset_rows: List[Dict[str, str]]
    ) -> None:
        counts: Dict[str, int] = {}
        for row in dataset_rows:
            counts[row["intent"]] = counts.get(row["intent"], 0) + 1

        for intent in EXPECTED_INTENTS:
            assert counts.get(intent, 0) == 60, f"Intent {intent} count != 60: {counts.get(intent, 0)}"

    def test_language_distribution_balance(
        self, dataset_rows: List[Dict[str, str]]
    ) -> None:
        lang_counts: Dict[str, int] = {}
        for row in dataset_rows:
            lang_counts[row["language"]] = lang_counts.get(row["language"], 0) + 1

        for lang in EXPECTED_LANGUAGES:
            assert lang_counts.get(lang, 0) == 180, f"Language {lang} count != 180: {lang_counts.get(lang, 0)}"

    def test_each_intent_has_all_languages(
        self, dataset_rows: List[Dict[str, str]]
    ) -> None:
        matrix: Dict[str, Dict[str, int]] = {i: {} for i in EXPECTED_INTENTS}
        for row in dataset_rows:
            matrix[row["intent"]][row["language"]] = (
                matrix[row["intent"]].get(row["language"], 0) + 1
            )

        for intent, langs in matrix.items():
            for lang in EXPECTED_LANGUAGES:
                assert langs.get(lang, 0) == 10, f"{intent} missing balanced count for {lang}: {langs.get(lang, 0)}"


class TestIntentDatasetSplits:
    def test_splits_are_disjoint_and_partition_full_dataset(
        self, dataset_rows: List[Dict[str, str]]
    ) -> None:
        def load_split(path: str) -> List[Dict[str, str]]:
            with open(path, "r", encoding="utf-8") as f:
                return list(csv.DictReader(f))

        train_rows = load_split(TRAIN_CSV)
        val_rows = load_split(VAL_CSV)
        test_rows = load_split(TEST_CSV)

        train_ids = {int(r["id"]) for r in train_rows}
        val_ids = {int(r["id"]) for r in val_rows}
        test_ids = {int(r["id"]) for r in test_rows}
        full_ids = {int(r["id"]) for r in dataset_rows}

        # ID disjointness
        assert train_ids.isdisjoint(val_ids), "Train and validation overlap by ID"
        assert train_ids.isdisjoint(test_ids), "Train and test overlap by ID"
        assert val_ids.isdisjoint(test_ids), "Validation and test overlap by ID"

        # Complete partition
        assert train_ids | val_ids | test_ids == full_ids

        # Size assertions
        assert len(train_ids) == 756
        assert len(val_ids) == 162
        assert len(test_ids) == 162

        # Text disjointness (normalized)
        train_texts = {r["text"].strip().lower() for r in train_rows}
        val_texts = {r["text"].strip().lower() for r in val_rows}
        test_texts = {r["text"].strip().lower() for r in test_rows}

        assert train_texts.isdisjoint(val_texts), "Train and validation overlap by text"
        assert train_texts.isdisjoint(test_texts), "Train and test overlap by text"
        assert val_texts.isdisjoint(test_texts), "Validation and test overlap by text"

    def test_all_intents_represented_in_all_splits(self) -> None:
        for split_path in [TRAIN_CSV, VAL_CSV, TEST_CSV]:
            with open(split_path, "r", encoding="utf-8") as f:
                intents = {r["intent"] for r in csv.DictReader(f)}
                assert intents == EXPECTED_INTENTS


class TestIntentDatasetValidationScript:
    def test_validator_script_succeeds(self) -> None:
        from scripts.validate_intent_dataset import validate_csv, validate_jsonl, validate_splits

        csv_report = validate_csv(DATASET_CSV)
        assert len(csv_report["errors"]) == 0
        assert csv_report["total_samples"] == 1080
        assert csv_report["unique_samples"] == 1080

        jsonl_errors = validate_jsonl(DATASET_JSONL, csv_report["total_samples"])
        assert len(jsonl_errors) == 0

        split_errors, split_stats = validate_splits(
            TRAIN_CSV, VAL_CSV, TEST_CSV, csv_report["rows"]
        )
        assert len(split_errors) == 0
        assert split_stats["train_count"] == 756
        assert split_stats["val_count"] == 162
        assert split_stats["test_count"] == 162
