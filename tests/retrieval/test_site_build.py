import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_site import build


class SiteBuildTests(unittest.TestCase):
    def test_site_contains_jsonld_absolute_sitemap_and_robot_rules(self):
        base_url = "https://github.com/Francois-EF-WebOps/BabelGlobalKreole"
        with tempfile.TemporaryDirectory() as temp:
            build(base_url, temp)
            root = Path(temp)
            page = (root / "index.html").read_text(encoding="utf-8")
            robots = (root / "robots.txt").read_text(encoding="utf-8")
            sitemap = (root / "sitemap.xml").read_text(encoding="utf-8")
            catalog = json.loads((root / "catalog.json").read_text(encoding="utf-8"))
            self.assertIn('application/ld+json', page)
            self.assertIn('"@type":"Dataset"', page)
            self.assertIn(base_url + "/sitemap.xml", robots)
            self.assertIn(base_url + "/llms.txt", sitemap)
            self.assertEqual(catalog["record_counts"]["language_records"], 24)
            self.assertTrue((root / "llms.txt").is_file())


if __name__ == "__main__":
    unittest.main()
