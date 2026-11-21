"""T0.55: accounting of synthetic, public typed SciResearch episode outputs.

Review of the original private scientific trace is separate from scoring; do not
infer scientific validity from the public scorer alone.
"""
import math

# Explicit exploratory gates, NOT general scientific truth.
MAX_ERROR_SIGMA = 3.0
MAX_INTERVAL_SCORE_SIGMA = 12.0
COST_FIELDS = ("cpu_seconds", "input_tokens", "review_minutes")


def quality_screen(public):
    if public is None or public.get("science_status") != "SCORED":
        return False
    s = public.get("score")
    if type(s) is not dict:
        raise ValueError("typed score missing")
    for name in ("target_abs_error_over_sigma", "target_interval_score"):
        v = s.get(name)
        if type(v) not in (float, int) or not math.isfinite(v) or v < 0:
            raise ValueError("invalid numeric score")
    for name in ("target_covered", "checked_convergence"):
        if type(s.get(name)) is not bool:
            raise ValueError("invalid boolean score")
    conv = s.get("final_fit_converged")
    if conv is not None and type(conv) is not bool:
        raise ValueError("invalid convergence field")
    return (
        s["target_abs_error_over_sigma"] <= MAX_ERROR_SIGMA
        and s["target_covered"]
        and s["target_interval_score"] <= MAX_INTERVAL_SCORE_SIGMA
        and (conv is None or (s["checked_convergence"] and conv))
    )


def summarize(rows):
    """One row per launch, including preparation failures.

    Row fields: id, science_started (bool), public (typed export or None),
    review_valid (bool or None), cost (all COST_FIELDS, number or None).
    Unknown audit status stays unknown; cost gaps never silently become zero.
    """
    seen = set()
    started = valid = unknown = pre_science = 0
    costs = {f: 0.0 for f in COST_FIELDS}
    missing = {f: False for f in COST_FIELDS}
    episodes = []
    for row in rows:
        key = row["id"]
        began = row["science_started"]
        public = row["public"]
        review = row["review_valid"]
        if key in seen or type(began) is not bool or type(review) not in (bool, type(None)):
            raise ValueError("invalid or duplicate episode")
        seen.add(key)
        if not began:
            if public is not None or review is not None:
                raise ValueError("pre-science episode cannot be scored")
            pre_science += 1
            status, screen, result = "PRE_SCIENCE", None, None
        else:
            started += 1
            if public is None:
                if review is not None:
                    raise ValueError("missing score with known review status")
                status, screen, result = "UNKNOWN", None, None
                unknown += 1
            else:
                status = public.get("science_status")
                if status not in ("SCORED", "NO_SCORE"):
                    raise ValueError("unknown scientific status")
                if status == "NO_SCORE":
                    if public.get("score") is not None or review is True:
                        raise ValueError("unscored result cannot be valid")
                    screen, result = False, False
                else:
                    screen = quality_screen(public)
                    if review is True and not screen:
                        raise ValueError("scientific review contradicts failed quality gate")
                    result = review if screen else False
                    if result is None:
                        unknown += 1
                if result is True:
                    valid += 1
        cost = row["cost"]
        if type(cost) is not dict or set(cost) != set(COST_FIELDS):
            raise ValueError("incomplete cost structure")
        for field in COST_FIELDS:
            v = cost[field]
            if v is None:
                missing[field] = True
            elif type(v) not in (float, int) or not math.isfinite(v) or v < 0:
                raise ValueError("invalid cost value")
            else:
                costs[field] += v
        episodes.append({"id": key, "status": status,
                         "quality_screen": screen, "science_valid": result})
    totals = {f: None if missing[f] else costs[f] for f in COST_FIELDS}
    per_valid = {f: None if valid == 0 or totals[f] is None else totals[f] / valid
                 for f in COST_FIELDS}
    return {
        "attempts": len(rows), "pre_science": pre_science,
        "started": started, "valid": valid, "unknown_validity": unknown,
        "valid_rate": None if started == 0 else valid / started,
        "valid_rate_upper": None if started == 0 else (valid + unknown) / started,
        "cost_total": totals, "cost_known_lower_bound": costs,
        "cost_per_valid": per_valid, "episodes": episodes,
    }
