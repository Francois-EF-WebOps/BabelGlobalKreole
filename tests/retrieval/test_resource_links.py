import unittest

from scripts.check_resource_links import strip_tracking


class ResourceLinkCheckTests(unittest.TestCase):
    def test_tracking_parameters_are_removed_without_changing_other_query_values(self):
        self.assertEqual(
            strip_tracking("https://example.org/path?utm_source=feed&lang=fr&page=2"),
            "https://example.org/path?lang=fr&page=2",
        )

    def test_url_without_tracking_parameters_is_stable(self):
        url = "https://example.org/path?lang=fr#section"
        self.assertEqual(strip_tracking(url), url)


if __name__ == "__main__":
    unittest.main()
