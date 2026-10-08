import csv
import json
import os
import pytest
from typing import Dict, List, Set

DATASET_DIR = os.path.join("data", "datasets", "tone")
DATASET_CSV = os.path.join(DATASET_DIR, "tone_dataset.csv")
DATASET_JSONL = os.path.join(DATASET_DIR, "tone_dataset.jsonl")
TRAIN_CSV = os.path.join(DATASET_DIR, "tone_train.csv")
VAL_CSV = os.path.join(DATASET_DIR, "tone_validation.csv")
TEST_CSV = os.path.join(DATASET_DIR, "tone_test.csv")

ALLOWED_TONES = {"CASUAL", "FORMAL", "SIMPLE", "TECHNICAL", "SHORT", "DETAILED"}
ALLOWED_LANGUAGES = {
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


class TestToneDatasetFilesExist:
    def test_all_expected_dataset_files_exist(self) -> None:
        assert os.path.exists(DATASET_CSV)
        assert os.path.exists(DATASET_JSONL)
        assert os.path.exists(TRAIN_CSV)
        assert os.path.exists(VAL_CSV)
        assert os.path.exists(TEST_CSV)
        readme_path = os.path.join(DATASET_DIR, "README.md")
        assert os.path.exists(readme_path)


class TestToneDatasetSchema:
    def test_csv_columns(self, dataset_rows: List[Dict[str, str]]) -> None:
        expected_columns = {"id", "text", "tone", "language", "domain"}
        assert len(dataset_rows) >= 300
        for row in dataset_rows:
            assert expected_columns.issubset(set(row.keys()))

    def test_jsonl_keys_match_csv(
        self, dataset_rows: List[Dict[str, str]], jsonl_rows: List[Dict]
    ) -> None:
        assert len(dataset_rows) == len(jsonl_rows)
        for csv_row, json_row in zip(dataset_rows, jsonl_rows):
            assert int(csv_row["id"]) == int(json_row["id"])
            assert csv_row["text"] == json_row["text"]
            assert csv_row["tone"] == json_row["tone"]
            assert csv_row["language"] == json_row["language"]
            assert csv_row["domain"] == json_row["domain"]


class TestToneDatasetNoNullsOrEmpty:
    def test_no_null_or_empty_fields(self, dataset_rows: List[Dict[str, str]]) -> None:
        for idx, row in enumerate(dataset_rows, start=1):
            assert row["id"].strip(), f"Row {idx} has empty id"
            assert row["text"].strip(), f"Row {idx} has empty text"
            assert row["tone"].strip(), f"Row {idx} has empty tone"
            assert row["language"].strip(), f"Row {idx} has empty language"
            assert row["domain"].strip(), f"Row {idx} has empty domain"


class TestToneDatasetUniqueness:
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


class TestToneDatasetLabelsAndLanguages:
    def test_only_allowed_tone_labels(self, dataset_rows: List[Dict[str, str]]) -> None:
        found_tones = set()
        for row in dataset_rows:
            tone = row["tone"]
            assert tone in ALLOWED_TONES, f"Unexpected tone: {tone}"
            found_tones.add(tone)
        assert found_tones == ALLOWED_TONES, "Not all 6 tone classes are represented"

    def test_all_six_languages_present(self, dataset_rows: List[Dict[str, str]]) -> None:
        found_langs = set()
        for row in dataset_rows:
            lang = row["language"]
            assert lang in ALLOWED_LANGUAGES, f"Unexpected language: {lang}"
            found_langs.add(lang)
        assert found_langs == ALLOWED_LANGUAGES, "Not all 6 language categories are represented"

    def test_coding_domain_exclusivity(self, dataset_rows: List[Dict[str, str]]) -> None:
        for row in dataset_rows:
            assert row["domain"] == "coding"


class TestToneDatasetBalance:
    def test_tone_label_distribution_balanced(
        self, dataset_rows: List[Dict[str, str]]
    ) -> None:
        counts: Dict[str, int] = {}
        for row in dataset_rows:
            counts[row["tone"]] = counts.get(row["tone"], 0) + 1

        for tone in ALLOWED_TONES:
            assert counts.get(tone, 0) >= 50, f"Tone {tone} under-represented: {counts.get(tone, 0)}"
            # In our 600-sample dataset, exactly 100 per tone
            assert counts.get(tone, 0) == 100


class TestToneDatasetSplits:
    def test_splits_are_disjoint_and_partition_full_dataset(
        self, dataset_rows: List[Dict[str, str]]
    ) -> None:
        def load_ids(path: str) -> Set[int]:
            with open(path, "r", encoding="utf-8") as f:
                return {int(r["id"]) for r in csv.DictReader(f)}

        train_ids = load_ids(TRAIN_CSV)
        val_ids = load_ids(VAL_CSV)
        test_ids = load_ids(TEST_CSV)
        full_ids = {int(r["id"]) for r in dataset_rows}

        # No leakage across splits
        assert train_ids.isdisjoint(val_ids), "Train and validation overlap"
        assert train_ids.isdisjoint(test_ids), "Train and test overlap"
        assert val_ids.isdisjoint(test_ids), "Validation and test overlap"

        # Complete union
        assert train_ids | val_ids | test_ids == full_ids

        # Proportions: 70% train (420), 15% val (90), 15% test (90)
        assert len(train_ids) == 420
        assert len(val_ids) == 90
        assert len(test_ids) == 90


class TestToneDatasetValidationScript:
    def test_validator_script_succeeds(self) -> None:
        from scripts.validate_tone_dataset import validate_csv, validate_jsonl

        csv_report = validate_csv(DATASET_CSV)
        assert len(csv_report["errors"]) == 0
        assert csv_report["total_samples"] == 600
        assert csv_report["unique_samples"] == 600

        jsonl_errors = validate_jsonl(DATASET_JSONL, csv_report["total_samples"])
        assert len(jsonl_errors) == 0
