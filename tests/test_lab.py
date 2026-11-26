import tempfile
import unittest
from pathlib import Path
from lab import Lab

class LabTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.lab = Lab(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_has_three_fictional_endpoints(self):
        self.assertEqual(len(self.lab.clients), 3)

    def test_demo_creates_six_events(self):
        self.assertTrue(self.lab.add_demo_events("LAB-001"))
        self.assertEqual(len(self.lab.events), 6)

    def test_unknown_endpoint_rejected(self):
        self.assertFalse(self.lab.add_demo_events("UNKNOWN"))

    def test_detection_rules_return_findings(self):
        self.lab.add_demo_events("LAB-001")
        self.assertGreaterEqual(len(self.lab.detect()), 6)

if __name__ == "__main__":
    unittest.main()
