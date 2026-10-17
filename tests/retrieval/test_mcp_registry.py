import unittest

from mcp_server.registry import evidence_eligibility, get_record, safe_record_view, search_records


class MCPRegistryTests(unittest.TestCase):
    def test_draft_records_are_not_evidence(self):
        record = {"language_id": "lng-test", "name": "Test", "record_status": "draft", "source_ids": []}
        eligible, _ = evidence_eligibility(record, {})
        self.assertFalse(eligible)

    def test_accepted_record_requires_resolved_source_location(self):
        record = {"language_id": "lng-test", "record_status": "accepted", "source_ids": ["src-test"]}
        eligible, reason = evidence_eligibility(record, {"src-test": {"canonical_url": "https://github.com/Francois-EF-WebOps/BabelGlobalKreole", "accessed_date": "2026-10-17"}})
        self.assertFalse(eligible)
        self.assertIn("precise location", reason)

    def test_content_is_withheld_without_explicit_retrieval_permission(self):
        record = {"entry_id": "lex-test", "form": "secret-example", "definition": "example", "record_status": "draft", "source_ids": [], "ai_use": {"retrieval": "unknown"}}
        view = safe_record_view(record, {})
        self.assertTrue(view["content_withheld"])
        self.assertNotIn("form", view)
        self.assertNotIn("definition", view)

    def test_search_abstains_on_draft_matches(self):
        records = [{"language_id": "lng-test", "name": "Test Language", "record_status": "draft", "source_ids": []}]
        result = search_records("Test Language", records=records)
        self.assertTrue(result["abstained"])
        self.assertFalse(result["results"][0]["record"]["evidence_eligible"])

    def test_search_does_not_match_content_when_retrieval_is_not_allowed(self):
        records = [
            {"entry_id": "lex-test", "form": "secret-form", "record_status": "draft", "source_ids": [], "ai_use": {"retrieval": "unknown"}}
        ]
        result = search_records("secret-form", records=records)
        self.assertEqual(result["results"], [])
        self.assertTrue(result["abstained"])

    def test_eligible_evidence_is_prioritized_over_draft_matches(self):
        source = {"source_id": "src-test", "canonical_url": "https://github.com/Francois-EF-WebOps/BabelGlobalKreole", "accessed_date": "2026-10-17", "relevant_location": "README scope paragraph"}
        records = [
            {"language_id": "lng-draft", "name": "shared term", "record_status": "draft", "source_ids": []},
            {"language_id": "lng-accepted", "name": "shared term", "record_status": "accepted", "source_ids": ["src-test"]},
            source,
        ]
        result = search_records("shared term", records=records, limit=1)
        self.assertEqual(result["results"][0]["record_id"], "lng-accepted")
        self.assertFalse(result["abstained"])

    def test_missing_record_is_explicit(self):
        self.assertFalse(get_record("lng-missing", records=[])["found"])


if __name__ == "__main__":
    unittest.main()
