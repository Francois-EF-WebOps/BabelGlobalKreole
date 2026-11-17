import tempfile
import unittest
from pathlib import Path

from scripts.validation_checks import (
    check_draft_content,
    check_jsonl_text,
    check_repository_files,
    should_scan_draft_content,
)


class DraftMarkerTests(unittest.TestCase):
    def test_github_issue_form_placeholder_is_not_content_marker(self):
        path = ".github/ISSUE_TEMPLATE/bounded-contribution.yml"
        self.assertFalse(should_scan_draft_content(path))
        self.assertEqual(
            check_draft_content([(path, "placeholder: One task, one outcome.")]), []
        )

    def test_genuine_marker_in_project_docs_fails(self):
        self.assertTrue(should_scan_draft_content("docs/draft.md"))
        self.assertTrue(check_draft_content([("docs/draft.md", "TODO: add evidence")]))


class JsonlIntegrityTests(unittest.TestCase):
    def test_valid_record_passes(self):
        self.assertEqual(
            check_jsonl_text(
                "data/example.jsonl",
                '{"record_status":"draft","source_ids":[],"name":"Example"}',
            ),
            [],
        )

    def test_malformed_json_fails(self):
        self.assertTrue(check_jsonl_text("data/example.jsonl", '{"broken":'))

    def test_accepted_record_without_provenance_fails(self):
        errors = check_jsonl_text(
            "data/example.jsonl",
            '{"record_status":"accepted","source_ids":[],"name":"Example"}',
        )
        self.assertTrue(any("accepted record has empty source_ids" in e for e in errors))

    def test_empty_object_fails(self):
        self.assertTrue(check_jsonl_text("data/example.jsonl", "{}"))

    def test_blank_line_fails(self):
        content = '{"name":"x"}\n\n{"name":"y"}'
        self.assertTrue(check_jsonl_text("data/example.jsonl", content))


class RepositoryIntegrityTests(unittest.TestCase):
    def test_missing_tracked_file_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = check_repository_files(Path(directory), ["missing.md"])
        self.assertTrue(any("tracked path is missing" in error for error in errors))

    def test_zero_byte_tracked_file_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "empty.md").write_text("")
            errors = check_repository_files(Path(directory), ["empty.md"])
        self.assertTrue(any("zero-byte tracked file" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
