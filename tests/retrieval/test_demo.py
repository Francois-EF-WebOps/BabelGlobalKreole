import json
import unittest

from demo.retrieval.demo import build_answer


class RetrievalDemoTests(unittest.TestCase):
    def test_draft_without_sources_abstains_and_cites_nothing(self):
        records = [
            {"language_id": "lng-test", "name": "Test Language", "record_status": "draft", "source_ids": []}
        ]
        answer = build_answer("Test Language", records, "test-version")
        self.assertEqual(answer["answer_status"], "abstained")
        self.assertEqual(answer["claims"], [])
        self.assertEqual(answer["sources"], [])

    def test_accepted_record_cites_resolved_source_metadata(self):
        records = [
            {"language_id": "lng-test", "name": "Test Language", "record_status": "accepted", "source_ids": ["src-test"], "evidence_status": "scholarly_analysis"},
            {"source_id": "src-test", "title": "Test source", "canonical_url": "https://example.org/source", "relevant_location": "section 2", "accessed_date": "2026-10-17"},
        ]
        answer = build_answer("lng-test", records, "test-version")
        self.assertEqual(answer["answer_status"], "partial")
        self.assertEqual(answer["claims"][0]["record_ids"], ["lng-test"])
        self.assertEqual(answer["sources"][0]["source_id"], "src-test")
        self.assertEqual(answer["sources"][0]["location"], "section 2")

    def test_accepted_record_with_source_missing_access_date_abstains(self):
        records = [
            {"language_id": "lng-test", "name": "Test Language", "record_status": "accepted", "source_ids": ["src-test"], "evidence_status": "scholarly_analysis"},
            {"source_id": "src-test", "title": "Source without access date", "canonical_url": "https://example.org/source", "relevant_location": "section 2"},
        ]
        answer = build_answer("lng-test", records, "test-version")
        self.assertEqual(answer["answer_status"], "abstained")
        self.assertEqual(answer["claims"], [])
        self.assertEqual(answer["sources"], [])

    def test_accepted_record_with_source_without_location_abstains(self):
        records = [
            {"language_id": "lng-test", "name": "Test Language", "record_status": "accepted", "source_ids": ["src-test"], "evidence_status": "scholarly_analysis"},
            {"source_id": "src-test", "title": "Source with no location"},
        ]
        answer = build_answer("lng-test", records, "test-version")
        self.assertEqual(answer["answer_status"], "abstained")
        self.assertEqual(answer["claims"], [])
        self.assertEqual(answer["sources"], [])

    def test_lexical_entry_id_uses_schema_field_entry_id(self):
        records = [
            {"entry_id": "lex-test", "lemma": "test-form", "record_status": "draft", "source_ids": []}
        ]
        answer = build_answer("lex-test", records, "test-version")
        self.assertEqual(answer["answer_status"], "abstained")
        self.assertIn("test-form", answer["answer"])
        self.assertEqual(answer["claims"], [])

    def test_variety_id_is_not_shadowed_by_parent_language_id(self):
        records = [
            {"variety_id": "var-test", "language_id": "lng-test", "name": "Test Variety", "record_status": "draft", "source_ids": [], "retrieval_status": "non-retrievable"}
        ]
        answer = build_answer("var-test", records, "test-version")
        self.assertEqual(answer["answer_status"], "abstained")
        self.assertIn("Test Variety", answer["answer"])
        self.assertEqual(answer["claims"], [])
        self.assertEqual(answer["sources"], [])

    def test_unknown_query_abstains(self):
        answer = build_answer("no-such-record", [], "test-version")
        self.assertEqual(answer["answer_status"], "abstained")
        self.assertEqual(answer["claims"], [])


if __name__ == "__main__":
    unittest.main()
