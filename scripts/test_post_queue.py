#!/usr/bin/env python3
"""Acceptance tests for the seven-post human-approval queue."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_post_queue", ROOT / "scripts" / "build_post_queue.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PostQueueTests(unittest.TestCase):
    def setUp(self):
        self.batch = MODULE.load_batch(ROOT / "distribution" / "post-queue.json")

    def test_batch_contains_seven_unique_reviewable_posts(self):
        self.assertEqual(len(self.batch["posts"]), 7)
        ids = [post["id"] for post in self.batch["posts"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(post["status"] == "awaiting_human_approval" for post in self.batch["posts"]))

    def test_every_post_has_https_sources(self):
        for post in self.batch["posts"]:
            self.assertGreaterEqual(len(post["source_urls"]), 1)
            self.assertTrue(all(url.startswith("https://") for url in post["source_urls"]))

    def test_non_reviewed_batch_cannot_enter_queue(self):
        candidate = copy.deepcopy(self.batch)
        candidate["status"] = "approved_for_publication"
        with self.assertRaisesRegex(ValueError, "awaiting_human_approval"):
            MODULE.validate_batch(candidate)

    def test_wrong_batch_size_is_rejected(self):
        candidate = copy.deepcopy(self.batch)
        candidate["posts"].pop()
        with self.assertRaisesRegex(ValueError, "exactly 7"):
            MODULE.validate_batch(candidate)

    def test_unapproved_post_cannot_be_promoted_silently(self):
        candidate = copy.deepcopy(self.batch)
        candidate["posts"][0]["status"] = "approved_for_publication"
        with self.assertRaisesRegex(ValueError, "awaiting_human_approval"):
            MODULE.validate_batch(candidate)

    def test_build_writes_mobile_readable_queue_and_non_delivery_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            receipt = MODULE.build(self.batch, Path(tmp))
            markdown = (Path(tmp) / "approval-queue.md").read_text(encoding="utf-8")
            queue = json.loads((Path(tmp) / "approval-queue.json").read_text(encoding="utf-8"))
            stored_receipt = json.loads((Path(tmp) / "receipts.json").read_text(encoding="utf-8"))
            self.assertEqual(markdown.count("**Review status:**"), 7)
            self.assertEqual(len(queue["posts"]), 7)
            self.assertTrue(receipt["human_approval_required"])
            self.assertFalse(receipt["publication_attempted"])
            self.assertEqual(receipt["delivery_status"], "not_sent")
            self.assertEqual(len(stored_receipt["posts"]), 7)
            self.assertTrue(all(item["published"] is False for item in stored_receipt["posts"]))
            self.assertTrue(all(item["delivery_status"] == "not_sent" for item in stored_receipt["posts"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
