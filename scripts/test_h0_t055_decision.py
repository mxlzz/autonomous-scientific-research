"""T0.55 fixtures only: no private benchmark inputs, model or paid API."""
import unittest

from h0_t055_decision import summarize, quality_screen


def episode(name, started, public=None, review=None, cpu=1, tokens=100, minutes=0):
    return {"id": name, "science_started": started, "public": public,
            "review_valid": review,
            "cost": {"cpu_seconds": cpu, "input_tokens": tokens, "review_minutes": minutes}}


def scored(error=1, interval=6, covered=True, conv=None, checked=False):
    return {"science_status": "SCORED", "stop": "submitted",
            "score": {"target_abs_error_over_sigma": error,
                      "target_interval_score": interval,
                      "target_covered": covered,
                      "checked_convergence": checked,
                      "final_fit_converged": conv}}


class AccountingFixtures(unittest.TestCase):
    def test_quality_and_types(self):
        self.assertTrue(quality_screen(scored()))
        for x in (scored(error=4), scored(interval=13),
                  scored(covered=False), scored(conv=False, checked=True)):
            self.assertFalse(quality_screen(x))
        self.assertTrue(quality_screen(scored(conv=True, checked=True)))
        for x in (scored(covered=1), scored(error="bad"),
                  scored(conv=1, checked=True)):
            with self.assertRaises(ValueError):
                quality_screen(x)

    def test_five_distinct_outcomes_and_cost_gap(self):
        rows = [
            episode("valid", True, scored(), True, cpu=10, tokens=100, minutes=2),
            episode("invalid", True, scored(error=500), False, cpu=20, tokens=200, minutes=1),
            episode("no-submit", True, {"science_status": "NO_SCORE", "score": None},
                    cpu=30, tokens=300),
            episode("pre-science", False, cpu=4, tokens=0),
            episode("unreviewed", True, scored(), cpu=None, tokens=400),
        ]
        result = summarize(rows)
        self.assertEqual((result["attempts"], result["pre_science"],
                          result["started"], result["valid"], result["unknown_validity"]),
                         (5, 1, 4, 1, 1))
        self.assertEqual((result["valid_rate"], result["valid_rate_upper"]), (.25, .5))
        self.assertEqual(result["cost_total"],
                         {"cpu_seconds": None, "input_tokens": 1000., "review_minutes": 3.})
        self.assertEqual(result["cost_known_lower_bound"]["cpu_seconds"], 64.)
        self.assertEqual(result["cost_per_valid"],
                         {"cpu_seconds": None, "input_tokens": 1000., "review_minutes": 3.})
        self.assertIs(result["episodes"][2]["science_valid"], False)

    def test_zero_valid_and_zero_started(self):
        result = summarize([
            episode("bad", True, scored(error=4), False, cpu=2),
            episode("missing", True, {"science_status": "NO_SCORE", "score": None}, cpu=4),
        ])
        self.assertEqual(result["valid_rate"], 0)
        self.assertEqual(result["cost_total"]["cpu_seconds"], 6)
        self.assertIsNone(result["cost_per_valid"]["cpu_seconds"])
        no_start = summarize([episode("pre", False, cpu=3)])
        self.assertIsNone(no_start["valid_rate"])
        self.assertEqual(no_start["pre_science"], 1)

    def test_bad_accounting_rejected(self):
        invalid_groups = [
            [episode("dup", True, scored(), True), episode("dup", True, scored(), True)],
            [episode("bad-pre", False, scored(), True)],
            [episode("bad-review", True, scored(error=4), True)],
            [episode("bad-submit", True, {"science_status": "NO_SCORE", "score": None}, True)],
            [episode("bad-unknown", True, None, True)],
        ]
        for rows in invalid_groups:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                summarize(rows)


if __name__ == "__main__":
    unittest.main()
