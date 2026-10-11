"""The machine-readable catalog must follow CODE_OF_CONDUCT.md section 3 exactly."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "research" / "agent-self-report" / "error-classes.json"
CONDUCT = ROOT / "CODE_OF_CONDUCT.md"
CLAIMS = ROOT / "traceweave" / "claims.py"

ROW = re.compile(r"\|\s*\**(E\d\d)\**\s*\|\s*\**(.+?)\**\s*\|")


class TestErrorClassCatalog(unittest.TestCase):

    def setUp(self):
        self.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    def test_same_classes_in_same_order_as_code_of_conduct(self):
        table = [m.groups() for m in map(ROW.match, CONDUCT.read_text(encoding="utf-8").splitlines()) if m]
        self.assertEqual([(c["id"], c["name"]) for c in self.catalog["classes"]], table)

    def test_automated_checks_exist_in_claims_module(self):
        source = CLAIMS.read_text(encoding="utf-8")
        for cls in self.catalog["classes"]:
            for check in cls["automated_checks"]:
                self.assertIn(f'"{check}", "{cls["id"]}"', source, f"{check} is not emitted as {cls['id']}")


if __name__ == "__main__":
    unittest.main()
