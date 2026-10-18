#!/usr/bin/env python3
"""Acceptance tests for the single-source distribution builder."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_distribution", ROOT / "scripts" / "build_distribution.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.source = MODULE.load_source(ROOT / "distribution" / "source.json")

    def test_source_has_required_release_gate(self):
        self.assertEqual(self.source["status"], "approved_for_publication")
        self.assertEqual(self.source["rights_status"], "owner_authored_summary_of_this_repository")
        self.assertTrue(self.source["sources"])

    def test_unapproved_content_is_rejected(self):
        candidate = copy.deepcopy(self.source)
        candidate["status"] = "draft"
        with self.assertRaisesRegex(ValueError, "publication blocked"):
            MODULE.validate_source(candidate)

    def test_build_generates_all_channels(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output / "index.html").write_text("<html><head></head><body></body></html>", encoding="utf-8")
            (output / "sitemap.xml").write_text(
                '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>',
                encoding="utf-8",
            )
            manifest = MODULE.build(self.source, output, "https://example.test/project")
            self.assertTrue((output / "distribution" / "index.html").is_file())
            self.assertTrue((output / "distribution" / "source.json").is_file())
            self.assertTrue((output / "distribution" / "social-post.txt").is_file())
            self.assertTrue((output / "distribution" / "newsletter.txt").is_file())
            self.assertTrue((output / "distribution" / "manifest.json").is_file())
            self.assertTrue((output / "feed.xml").is_file())
            self.assertIn("Latest distributed knowledge brief:", (output / "index.html").read_text(encoding="utf-8"))
            self.assertIn("https://example.test/project/distribution/", (output / "feed.xml").read_text(encoding="utf-8"))
            self.assertEqual(manifest["metrics"]["source_records"], 1)
            self.assertTrue(manifest["delivery_status"]["social_post"].startswith("copy generated"))

    def test_missing_source_is_rejected(self):
        candidate = copy.deepcopy(self.source)
        candidate["sources"] = []
        with self.assertRaisesRegex(ValueError, "at least one source"):
            MODULE.validate_source(candidate)

    def test_unsafe_rights_status_is_rejected(self):
        candidate = copy.deepcopy(self.source)
        candidate["rights_status"] = "unknown"
        with self.assertRaisesRegex(ValueError, "rights_status"):
            MODULE.validate_source(candidate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
