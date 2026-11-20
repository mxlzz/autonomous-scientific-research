#!/usr/bin/env python3
"""T0.22 — fixed single-dev paired deterministic policies, original upstream scientific scorer.

This script is a trusted evaluator-side controller; it is NOT an autonomous agent,
nor an operating-system isolation of the task's private truth.
Only filtered metrics (not private labels, source data or full traces) are public.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import sys
import time

import numpy as np

from sciresearch_eval.baselines.scripted import naive, heuristic
from sciresearch_eval.env import ThermalEnv
from sciresearch_eval.grader import grade, interval_score
from sciresearch_eval.tasks.generator import public_id_for

UPSTREAM = "9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0"
TASK = "task_525abee377"
ROOT = Path("/project/tasks")
EXPECTED_NAIVE = {
    "param_interval_score": 0.3617342985371508,
    "param_coverage": 0.0,
    "target_interval_score": 6.0,
    "target_covered": True,
    "adequacy_correct": 1.0,
    "attribution_correct": 0.0,
}
SCALAR_FIELDS = (
    "param_interval_score", "param_coverage", "param_log10_error",
    "target_interval_score", "target_rel_interval_score", "target_covered",
    "target_abs_error_over_sigma", "adequacy_correct", "attribution_correct",
    "stop_correct", "experiment_selection", "proposal_score",
    "compute_fraction", "experiments_used",
)
start = time.monotonic()

def log(key: str, val) -> None:
    print("T022_" + key + "=" + str(val), flush=True)

def filter_metric(key, value):
    if value is None:
        return None
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (float, int, np.floating, np.integer)):
        v = float(value)
        if not math.isfinite(v):
            raise ValueError("nonfinite_" + key)
        return v
    raise ValueError("unexpected_type_" + key)

def execute(name, policy):
    np.random.seed(0)
    env = ThermalEnv(TASK, ROOT, "dev")
    if env.trace or env.used != {"experiments": 0, "compute_units": 0}:
        raise RuntimeError("environment_not_fresh")
    begin = time.monotonic()
    try:
        policy(env)
    except BaseException as e:
        log(name.upper() + "_POLICY_ERROR", type(e).__name__)
        raise
    elapsed = time.monotonic() - begin
    if env.submission is None:
        raise RuntimeError("no_submission_" + name)
    try:
        scored = grade(env)
    except BaseException as e:
        log(name.upper() + "_GRADE_ERROR", type(e).__name__)
        raise
    if not scored.get("submitted"):
        raise RuntimeError("not_graded_" + name)
    metrics = {k: filter_metric(k, scored.get(k)) for k in SCALAR_FIELDS}
    observations = {
        "policy": name,
        "score": metrics,
        "actions": len(env.trace),
        "experiments_used": env.used["experiments"],
        "compute_units": env.used["compute_units"],
        "compute_budget": env.budget["compute_units"],
        "experiment_budget": env.budget["experiments"],
        "policy_wall_sec": round(elapsed, 4),
    }
    # Do not print private data or task family, regime, labels, trace arguments,
    # dataset readings or submitted parameter values.
    log(name.upper() + "_ACTION_COUNT", observations["actions"])
    log(name.upper() + "_EXPERIMENTS", observations["experiments_used"])
    log(name.upper() + "_COMPUTE_UNITS", observations["compute_units"])
    log(name.upper() + "_POLICY_WALL_SEC", observations["policy_wall_sec"])
    for key, val in metrics.items():
        log(name.upper() + "_SCORE_" + key.upper(), val)
    return observations

def test_contract():
    spec = importlib.util.spec_from_file_location(
        "original_env_grader_tests", "/project/tests/test_env_grader.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for n in ("test_interval_score", "test_tool_outputs_never_contain_private_fields"):
        getattr(module, n)()
        log("ORIGINAL_TEST_PASS", n)
    if interval_score(1, 2, 3) != 41:
        raise RuntimeError("interval_score_contract")
    log("ORIGINAL_TEST_COUNT", 2)

def main():
    log("UPSTREAM_COMMIT", UPSTREAM)
    log("TASK_ID", TASK)
    log("PAIR", "naive_versus_heuristic_same_public_dev_task")
    log("SEED", 0)
    log("LLM_CALLS", 0)
    log("SECRET_FILES_IN_EVALUATOR", True)
    log("ACTOR_FS_PRIVATE_ISOLATION", False)
    log("PAID_API", False)
    if public_id_for("t3_coarse_mesh_2001", root=ROOT) != TASK:
        raise RuntimeError("task_identity_changed")
    test_contract()
    a = execute("naive", naive)
    b = execute("heuristic", heuristic)
    # The naive baseline is expected to match T0.21 within tolerances.
    # Environment/versions and seed are pinned; mismatch is a failed control.
    for key, expected in EXPECTED_NAIVE.items():
        actual = a["score"][key]
        matched = actual == expected if isinstance(expected, bool) else math.isclose(
            actual, expected, rel_tol=1e-8, abs_tol=1e-8
        )
        log("NAIVE_REPLICATION_" + key.upper(), matched)
        if not matched:
            raise RuntimeError("naive_baseline_not_replicated")
    changes = {}
    for key in ("param_interval_score", "param_coverage", "target_interval_score",
                "compute_fraction"):
        v0 = a["score"][key]
        v1 = b["score"][key]
        changes[key] = v1 - v0 if v0 is not None and v1 is not None else None
        log("HEURISTIC_MINUS_NAIVE_" + key.upper(), changes[key])
    stats = {
        "task": TASK, "upstream": UPSTREAM, "seed": 0,
        "kind": "one_paired_dev_task_non_LLM_not_heldout",
        "grader": "original_sciresearch_eval.grader.grade",
        "naive": a, "heuristic": b, "paired_difference": changes,
        "tests": ["test_interval_score", "test_tool_outputs_never_contain_private_fields"],
        "model_calls": 0, "api_paid": False,
        "os_private_file_isolation": False,
        "privacy_note": "trusted evaluator calls original scripted policies in same process; "
                        "separate LLM restricted to AgentTools needed before any model experiment",
        "wrapper_wall_sec": round(time.monotonic() - start, 4),
        "controller_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    dest = Path("/results/t022_pair.json")
    raw = (json.dumps(stats, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    dest.write_bytes(raw)
    log("PAIR_JSON_SHA256", hashlib.sha256(raw).hexdigest())
    log("WRAPPER_WALL_SEC", stats["wrapper_wall_sec"])
    log("CONTROLLER_MAXRSS_KIB", stats["controller_maxrss_kib"])
    log("PAIR_GRADED", True)

if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        log("STOP_CLASS", type(e).__name__)
        log("STATUS", "UNSCORED_OR_PARTIAL")
        sys.exit(1)
