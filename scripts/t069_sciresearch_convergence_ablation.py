#!/usr/bin/env python3
"""Original SciResearch one-factor convergence ablation; no LLM or private data outputs."""
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

PIN = "9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0"
ORDER = (
    ("task_525abee377", "original"),
    ("task_525abee377", "without_convergence"),
    ("task_b402d13dd9", "without_convergence"),
    ("task_b402d13dd9", "original"),
)
FIELDS = ("target_interval_score", "target_abs_error_over_sigma", "target_covered",
          "param_interval_score", "param_coverage", "adequacy_correct",
          "attribution_correct", "experiments_used", "checked_convergence",
          "final_fit_converged")

def scalar(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    try:
        v = float(value)
        return round(v, 9) if math.isfinite(v) else None
    except (ValueError, TypeError):
        return None

def self_test():
    import numpy as np
    import sciresearch_eval.baselines.scripted as scripted
    import sciresearch_eval.grader as grader
    assert grader.grade.__module__ == "sciresearch_eval.grader"
    assert grader.interval_score(1, 3, 2) == 2
    old = scripted._converge
    stub = lambda env, task, fit: (None, False, fit)
    dummy = {"estimates": {"a": 1.0}}
    try:
        scripted._converge = stub
        a, b, c = scripted._converge(None, {}, dummy)
        assert a is None and b is False and c is dummy
    finally:
        scripted._converge = old
    assert scripted._converge is old
    root = Path(os.environ["SCIRESEARCH_ROOT"])
    assert root.exists() and (root / "tasks" / "dev" / "manifest.json").exists()
    public_dir = root / "tasks" / "dev" / "public"
    for case, _ in ORDER:
        assert (public_dir / (case + ".json")).is_file()
    # No case text or original private data printed.
    print("T069_OFFLINE_GATE=PASS; grader unchanged, convergence patch isolated, cases present")

def child(case, arm):
    import numpy as np
    import sciresearch_eval.baselines.scripted as scripted
    from sciresearch_eval.env import ThermalEnv
    from sciresearch_eval.grader import grade
    if case not in {x[0] for x in ORDER} or arm not in {"original", "without_convergence"}:
        return 2
    original = scripted._converge
    if arm == "without_convergence":
        scripted._converge = lambda env, task, fit: (None, False, fit)
    start = time.perf_counter()
    try:
        np.random.seed(0)
        root = Path(os.environ["SCIRESEARCH_ROOT"]) / "tasks"
        env = ThermalEnv(case, root=root, split="dev")
        scripted.heuristic(env)
        before_grade_compute = int(env.used["compute_units"])
        before_grade_measurements = int(env.used["experiments"])
        sc = grade(env) if env.submission is not None else {"submitted": False}
        result = {
            "task": case, "arm": arm,
            "science_status": "SCORED" if sc.get("submitted") else "NO_SCORE",
            "submitted": bool(sc.get("submitted", False)),
            "compute_units_before_grade": before_grade_compute,
            "measurements": before_grade_measurements,
            "action_trace_length": len(env.trace),
            "wall_seconds": round(time.perf_counter() - start, 4),
            "scores": {k: scalar(sc.get(k)) for k in FIELDS},
        }
        print("T069_CHILD_RESULT=" + json.dumps(result, allow_nan=False, sort_keys=True))
        return 0
    except Exception:
        # Never print raw exceptions, private case/seed details or task content.
        print("T069_CHILD_STATUS=policy_or_grader_exception")
        return 1
    finally:
        scripted._converge = original

def run():
    t0 = time.perf_counter()
    root = Path(os.environ["SCIRESEARCH_ROOT"])
    subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                   capture_output=True, text=True, check=True)
    actual_pin = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"],
                                         text=True).strip()
    if actual_pin != PIN:
        raise RuntimeError("upstream_commit_mismatch")
    cases = []
    for case, arm in ORDER:
        t = time.perf_counter()
        args = [sys.executable, str(Path(__file__).resolve()), "--episode", case, arm]
        try:
            pr = subprocess.run(args, text=True, capture_output=True, timeout=90,
                                env=os.environ.copy(), check=False)
            lines = [line.split("=", 1)[1] for line in pr.stdout.splitlines()
                     if line.startswith("T069_CHILD_RESULT=")]
            if pr.returncode != 0 or len(lines) != 1:
                row = {"task": case, "arm": arm, "science_status": "NO_SCORE",
                       "error_category": "child_failed"}
            else:
                row = json.loads(lines[0])
        except subprocess.TimeoutExpired:
            row = {"task": case, "arm": arm, "science_status": "NO_SCORE",
                   "error_category": "episode_timeout_90s"}
        except Exception:
            row = {"task": case, "arm": arm, "science_status": "NO_SCORE",
                   "error_category": "parent_or_parse_error"}
        row["parent_elapsed_seconds"] = round(time.perf_counter()-t, 4)
        cases.append(row)
        # Progress markers, no raw data; all four episodes are preregistered once only.
        print("T069_EPISODE=" + json.dumps(row, sort_keys=True, separators=(",", ":")), flush=True)
    pairs = []
    for case in dict.fromkeys(case for case, _ in ORDER):
        rows = {r["arm"]: r for r in cases if r["task"] == case}
        a = rows["original"]; b = rows["without_convergence"]
        paired = a["science_status"] == "SCORED" and b["science_status"] == "SCORED"
        out = {"task": case, "paired_scored": paired}
        if paired:
            out["target_interval_delta_A_minus_B"] = round(
                a["scores"]["target_interval_score"] - b["scores"]["target_interval_score"], 7)
            out["target_abs_error_sigma_delta_A_minus_B"] = round(
                a["scores"]["target_abs_error_over_sigma"] - b["scores"]["target_abs_error_over_sigma"], 7)
            ua = a["compute_units_before_grade"]; ub = b["compute_units_before_grade"]
            out["compute_ratio_A_over_B"] = round(ua/ub, 5) if ub > 0 else None
        pairs.append(out)
    summary = {"protocol": "T0.69", "upstream_pin": PIN, "mode": "NO_LLM_CPU_ORIGINAL_GRADER",
               "episode_count": len(cases), "scored_count": sum(x["science_status"] == "SCORED" for x in cases),
               "pairs": pairs, "total_parent_seconds": round(time.perf_counter()-t0, 3)}
    print("T069_SUMMARY=" + json.dumps(summary, sort_keys=True, separators=(",", ":")), flush=True)
    return 0 if len(cases) == 4 else 1

def main():
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return 0
    if len(sys.argv) == 4 and sys.argv[1] == "--episode":
        return child(sys.argv[2], sys.argv[3])
    if sys.argv[1:] == ["--run"]:
        return run()
    return 2

if __name__ == "__main__":
    sys.exit(main())
