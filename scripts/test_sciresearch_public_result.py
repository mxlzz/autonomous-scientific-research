"""Exercise the public CLI with synthetic scored, unscored and broken records."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


EXPORTER = Path(__file__).with_name("sciresearch_public_result.py")
PRIVATE = "fixture-content-must-stay-private"


class PublicResultTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "result.json"
        self.grade = {
            "submitted": True, "param_interval_score": 0.5, "param_coverage": 0,
            "param_log10_error": 0.01, "target_interval_score": 6.0,
            "target_rel_interval_score": 0.2, "target_abs_error_over_sigma": 0.1,
            "compute_fraction": 0.01, "adequacy_correct": 0.5, "attribution_correct": 0,
            "target_covered": False, "checked_convergence": True, "final_fit_converged": None,
            "experiments_used": 0, "private_label": PRIVATE,
        }

    def invoke(self, payload=None):
        if payload is not None:
            self.path.write_text(json.dumps(payload), encoding="utf-8")
        result = subprocess.run([sys.executable, str(EXPORTER), str(self.path)],
                                capture_output=True, text=True, check=False)
        self.assertNotIn(PRIVATE, result.stdout + result.stderr)
        return result

    def test_scored(self):
        for final in (False, True, None):
            with self.subTest(final=final):
                self.grade["final_fit_converged"] = final
                result = self.invoke({"stop": "submitted", "grade": self.grade, "trace": PRIVATE})
                self.assertEqual(result.returncode, 0)
                public = json.loads(result.stdout)
                self.assertEqual(public["science_status"], "SCORED")
                self.assertIs(public["score"]["target_covered"], False)
                self.assertIs(public["score"]["checked_convergence"], True)
                self.assertIs(public["score"]["final_fit_converged"], final)
                self.assertEqual(public["score"]["experiments_used"], 0)

    def test_unscored(self):
        for stop, label in (("limit_turns_or_tokens", "limit_turns_or_tokens"),
                            ("error: " + PRIVATE, "error")):
            result = self.invoke({"grade": {"submitted": False}, "stop": stop})
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout),
                             {"science_status": "NO_SCORE", "stop": label, "score": None})

    def test_bad_measurements(self):
        for field, value in (("target_covered", 0.25), ("target_covered", "False"),
                             ("checked_convergence", None), ("param_coverage", True),
                             ("param_interval_score", float("nan")), ("experiments_used", -1)):
            with self.subTest(field=field, value=value):
                result = self.invoke({"stop": "submitted", "grade": {**self.grade, field: value}})
                self.assertEqual((result.returncode, result.stdout), (2, ""))

    def test_broken_records(self):
        for payload in (None, {}, {"stop": PRIVATE, "grade": self.grade},
                        {"stop": "submitted", "grade": {"submitted": True}},
                        {"stop": "submitted", "grade": {"submitted": False}},
                        {"stop": "no_tool_use", "grade": self.grade}):
            result = self.invoke(payload)
            self.assertEqual((result.returncode, result.stdout, result.stderr.strip()),
                             (2, "", "SCIRESEARCH_RECORD_UNAVAILABLE"))


if __name__ == "__main__":
    unittest.main()
