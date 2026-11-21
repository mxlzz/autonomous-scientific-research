"""Export only public, typed metrics from an original SciResearch harness result."""
import argparse
import json
import math
from pathlib import Path
import sys


NUMBERS = (
    "param_interval_score", "param_coverage", "param_log10_error",
    "target_interval_score", "target_rel_interval_score", "target_abs_error_over_sigma",
    "compute_fraction", "adequacy_correct", "attribution_correct",
)
FLAGS = ("target_covered", "checked_convergence", "final_fit_converged")
NULLABLE = {"adequacy_correct", "attribution_correct", "final_fit_converged"}
STOPS = {"submitted", "limit_turns_or_tokens", "limit_tool_calls", "limit_cost", "no_tool_use"}


def public_result(result):
    grade = result["grade"]
    stop = result["stop"]
    if type(stop) is not str or type(grade) is not dict or type(grade["submitted"]) is not bool:
        raise ValueError("invalid episode")
    if stop.startswith("error:"):
        stop = "error"
    elif stop not in STOPS:
        raise ValueError("unknown stop")
    if grade["submitted"] != (stop == "submitted"):
        raise ValueError("inconsistent submission")

    if not grade["submitted"]:
        return {"science_status": "NO_SCORE", "stop": stop, "score": None}

    score = {}
    for key in (*NUMBERS, *FLAGS, "experiments_used"):
        value = grade[key]
        if value is None and key in NULLABLE:
            pass
        elif key in FLAGS:
            if type(value) is not bool:
                raise ValueError("expected a boolean")
        elif key == "experiments_used":
            if type(value) is not int or value < 0:
                raise ValueError("expected a count")
        elif type(value) not in (float, int) or not math.isfinite(value):
            raise ValueError("expected a finite number")
        score[key] = value
    return {"science_status": "SCORED", "stop": stop, "score": score}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path, help="evaluator-local result.json")
    args = parser.parse_args()
    try:
        record = public_result(json.loads(args.result.read_text(encoding="utf-8")))
    except (KeyError, TypeError, ValueError, OSError, OverflowError, RecursionError):
        # A missing, unreadable or inconsistent record is an instrument failure.
        # Source paths, exception messages and benchmark contents stay local.
        print("SCIRESEARCH_RECORD_UNAVAILABLE", file=sys.stderr)
        return 2
    print(json.dumps(record, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
