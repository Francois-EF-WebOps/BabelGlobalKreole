import unittest

from scripts.record_integrity import extract_record_id, register_record_id


class RecordIntegrityTests(unittest.TestCase):
    def test_variety_id_precedes_parent_language_id(self):
        self.assertEqual(
            extract_record_id({"variety_id": "var-test", "language_id": "lng-test"}),
            "var-test",
        )

    def test_lexical_entry_uses_schema_id_field(self):
        self.assertEqual(extract_record_id({"entry_id": "lex-test", "language_id": "lng-test"}), "lex-test")

    def test_duplicate_id_returns_first_location(self):
        seen = {}
        self.assertIsNone(register_record_id({"source_id": "src-test"}, seen, "data/sources.jsonl", 1))
        self.assertEqual(
            register_record_id({"source_id": "src-test"}, seen, "other.jsonl", 9),
            ("data/sources.jsonl", 1),
        )


if __name__ == "__main__":
    unittest.main()
