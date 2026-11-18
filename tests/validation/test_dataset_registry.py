import json
import tempfile
import unittest
from pathlib import Path

from scripts.dataset_registry import discover_jsonl_paths, load_dataset_registry


class DatasetRegistryTests(unittest.TestCase):
    def test_current_manifest_registers_every_canonical_jsonl(self):
        root = Path(__file__).resolve().parents[2]
        manifest, datasets, errors = load_dataset_registry(root)
        self.assertEqual(errors, [])
        self.assertEqual(
            {entry["path"] for entry in datasets},
            discover_jsonl_paths(root),
        )
        self.assertEqual(manifest["source_dataset_id"], "sources")

    def test_unregistered_jsonl_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "registry").mkdir()
            (root / "data" / "known").mkdir(parents=True)
            (root / "data" / "unknown").mkdir()
            (root / "schemas").mkdir()
            (root / "data" / "known" / "records.jsonl").write_text("{}\n", encoding="utf-8")
            (root / "data" / "unknown" / "new.jsonl").write_text("{}\n", encoding="utf-8")
            (root / "schemas" / "record.schema.json").write_text("{}", encoding="utf-8")
            manifest = {
                "registry_version": 1,
                "source_dataset_id": "records",
                "catalog_paths": {"records": "data/known/"},
                "datasets": [{
                    "id": "records",
                    "path": "data/known/records.jsonl",
                    "schema": "schemas/record.schema.json",
                    "record_family": "record",
                    "catalog_key": "records",
                    "quality_checks": True,
                    "retrieval": True,
                }],
            }
            (root / "registry" / "datasets.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            _, _, errors = load_dataset_registry(root)
            self.assertTrue(any("not registered" in error for error in errors))

    def test_missing_registered_dataset_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "registry").mkdir()
            (root / "schemas").mkdir()
            (root / "schemas" / "record.schema.json").write_text("{}", encoding="utf-8")
            manifest = {
                "registry_version": 1,
                "source_dataset_id": "records",
                "catalog_paths": {"records": "data/"},
                "datasets": [{
                    "id": "records",
                    "path": "data/missing.jsonl",
                    "schema": "schemas/record.schema.json",
                    "record_family": "record",
                    "catalog_key": "records",
                    "quality_checks": True,
                    "retrieval": True,
                }],
            }
            (root / "registry" / "datasets.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            _, _, errors = load_dataset_registry(root)
            self.assertTrue(any("dataset file is missing" in error for error in errors))

    def test_duplicate_dataset_path_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "registry").mkdir()
            (root / "data").mkdir()
            (root / "schemas").mkdir()
            (root / "data" / "records.jsonl").write_text("{}\n", encoding="utf-8")
            (root / "schemas" / "record.schema.json").write_text("{}", encoding="utf-8")
            entry = {
                "id": "records",
                "path": "data/records.jsonl",
                "schema": "schemas/record.schema.json",
                "record_family": "record",
                "catalog_key": "records",
                "quality_checks": True,
                "retrieval": True,
            }
            manifest = {
                "registry_version": 1,
                "source_dataset_id": "records",
                "catalog_paths": {"records": "data/"},
                "datasets": [entry, dict(entry, id="records-copy")],
            }
            (root / "registry" / "datasets.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            _, _, errors = load_dataset_registry(root)
            self.assertTrue(any("duplicate dataset path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
