"""The public demo must keep catching every planted lie (examples/lie-detection/demo.py)."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

DEMO = Path(__file__).resolve().parent.parent / "examples" / "lie-detection" / "demo.py"


def load_demo():
    spec = importlib.util.spec_from_file_location("lie_detection_demo", DEMO)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestLieDetectionDemo(unittest.TestCase):

    def test_honest_passes_and_every_lie_is_caught(self):
        rows = load_demo().run()
        claim, structural, reality = rows[0]
        self.assertTrue(structural and reality, "the honest checkpoint must pass both checks")
        self.assertEqual(len(rows), 5)
        for claim, _structural, reality in rows[1:]:
            self.assertFalse(reality, f"not caught: {claim}")

    def test_record_time_lies_need_the_repository(self):
        rows = load_demo().run()
        # Lies 1 and 2 are well-formed: structural verify alone accepts them.
        self.assertTrue(rows[1][1])
        self.assertTrue(rows[2][1])


if __name__ == "__main__":
    unittest.main()
