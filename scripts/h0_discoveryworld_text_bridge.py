#!/usr/bin/env python3
"""H0 T0.11: bounded, text-only DiscoveryWorld adapter. NOT a scientific baseline.

Only the trusted controller imports DiscoveryWorld. Untrusted Ollama output is a
single JSON action, not Python, shell, method names, or tool invocations.
No hidden world state or scorer is exposed to model.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import time
import urllib.request

SCENARIO = "Plant Nutrients"
DIFFICULTY = "Normal"
SEED = 0
MAX_ACTIONS = 4
MAX_CALLS = 6
MAX_NEW_TOKENS = 256
MAX_MODEL_BYTES = 2048
MAX_OBSERVATION_CHARS = 7500

# Deliberately restricted for instrumental smoke; not equal tools to official baselines.
ACTIONS = {
    "ROTATE_DIRECTION": ("direction",),
    "MOVE_DIRECTION": ("direction",),
    "READ": ("uuid",),
    "PICKUP": ("uuid",),
    "OPEN": ("uuid",),
    "USE": ("uuid", "uuid"),
    "TALK": ("uuid",),
}
DIRECTIONS = {"north", "east", "south", "west"}
SCORE_KEYS = {"scoreNormalized", "scoreCard", "maxScore", "criticalQuestions", "criticalHypotheses"}
UI_ALLOWED = {"taskProgress", "agentLocation", "accessibleEnvironmentObjects", "inventoryObjects", "nearbyObjects", "dialog_box"}


def reject_duplicates(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate_json_field")
        out[key] = value
    return out


def parse_action(text, known_names):
    if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_MODEL_BYTES:
        raise ValueError("output_size_or_type")
    obj = json.loads(text, object_pairs_hook=reject_duplicates)
    if not isinstance(obj, dict) or not set(obj).issubset({"action", "arg1", "arg2"}):
        raise ValueError("not_single_allowed_action_object")
    a = obj.get("action")
    if not isinstance(a, str) or a not in ACTIONS or a not in known_names:
        raise ValueError("action_denied")
    kinds = ACTIONS[a]
    expected = {"action"} | ({"arg1"} if len(kinds) >= 1 else set()) | ({"arg2"} if len(kinds) >= 2 else set())
    if set(obj) != expected:
        raise ValueError("action_argument_fields")
    for ix, kind in enumerate(kinds):
        value = obj["arg" + str(ix + 1)]
        if kind == "direction" and (not isinstance(value, str) or value not in DIRECTIONS):
            raise ValueError("direction_denied")
        if kind == "uuid" and (type(value) is not int or value < 0):
            raise ValueError("uuid_denied")
    return obj


def observation_for_model(obs):
    if not isinstance(obs, dict) or obs.get("errors") or not isinstance(obs.get("ui"), dict):
        raise ValueError("invalid_observation")
    ui = obs["ui"]
    projected = {k: ui[k] for k in UI_ALLOWED if k in ui}
    # taskProgress is player-visible, unlike full scorecard; expose description/completed only.
    if isinstance(projected.get("taskProgress"), list):
        projected["taskProgress"] = [
            {"description": str(t.get("description", ""))[:500], "completed": bool(t.get("completed", False))}
            for t in projected["taskProgress"] if isinstance(t, dict)
        ]
    serialized = json.dumps(projected, sort_keys=True, ensure_ascii=True, default=str)
    if any(k in serialized for k in SCORE_KEYS):
        raise ValueError("observation_contains_oracle_field")
    # Truncate text (never JSON-decoded by controller, only prompt); no output to public logs.
    return serialized[:MAX_OBSERVATION_CHARS]


def self_test():
    known = set(ACTIONS)
    positives = [
        '{"action":"ROTATE_DIRECTION","arg1":"north"}',
        '{"action":"MOVE_DIRECTION","arg1":"east"}',
        '{"action":"USE","arg1":3,"arg2":8}',
    ]
    for raw in positives:
        assert parse_action(raw, known)
    negatives = [
        '{"action":"getTaskScorecard"}',
        '{"action":"__class__"}',
        '{"action":"READ","arg1":true}',
        '{"action":"MAGIC"}',
        '{"action":"ROTATE_DIRECTION","arg1":"north","__class__":"oracle"}',
        '{"action":"ROTATE_DIRECTION","arg1":"north","arg1":"east"}',
        '{"action":"ROTATE_DIRECTION","arg1":"up"}',
        '{"action":"USE","arg1":1,"arg2":2,"eval":"yes"}',
        '[{"action":"ROTATE_DIRECTION","arg1":"north"}]',
    ]
    for raw in negatives:
        try:
            parse_action(raw, known)
        except (ValueError, json.JSONDecodeError):
            pass
        else:
            raise AssertionError("rejected_action_was_accepted")
    assert observation_for_model({"errors": [], "ui": {"taskProgress": [{"description": "public task", "completed": False}], "agentLocation": {"x": 1}, "scoreCard": {"hidden": 9}}})
    try:
        observation_for_model({"errors": [], "ui": {"nearbyObjects": [{"scoreNormalized": 0.8}]}})
    except ValueError:
        pass
    else:
        raise AssertionError("hidden_score_field_was_accepted")
    print("T011_NEGATIVE_ACTION_TESTS=" + str(len(negatives)))
    print("T011_POSITIVE_ACTION_TESTS=" + str(len(positives)))
    print("T011_ORACLE_FIELD_TEST=pass")
    print("T011_VALIDATOR_GATE=pass")


def ask_local_model(prompt):
    payload = {
        "model": "qwen3:0.6b",
        "stream": False,
        "format": "json",
        "think": False,
        "messages": [
            {"role": "system", "content": "You are a scientist exploring a simulated world. Pick ONE allowed world action per turn, using only JSON with keys action, arg1, arg2 as needed. Never request code execution, secrets, scores, or evaluation information. Reply with one JSON object and no prose."},
            {"role": "user", "content": prompt},
        ],
        "options": {"temperature": 0, "seed": 0, "num_predict": MAX_NEW_TOKENS, "num_ctx": 4096},
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=55) as response:
        answer = json.load(response)
    message = answer.get("message", {})
    return message.get("content", ""), int(answer.get("prompt_eval_count") or 0), int(answer.get("eval_count") or 0)


def run():
    from discoveryworld.DiscoveryWorldAPI import DiscoveryWorldAPI
    start = time.monotonic()
    api = DiscoveryWorldAPI(threadID=11019)
    if not api.loadScenario(SCENARIO, DIFFICULTY, randomSeed=SEED, numUserAgents=1):
        raise RuntimeError("scenario_could_not_load")
    known = set(api.listKnownActions(limited=False))
    if not set(ACTIONS).issubset(known):
        raise RuntimeError("upstream_action_schema_changed")
    stats = {"llm_calls": 0, "valid_actions": 0, "invalid_actions": 0, "prompt_tokens": 0, "completion_tokens": 0}
    invalid_in_row = 0
    reasons = []
    while stats["valid_actions"] < MAX_ACTIONS and stats["llm_calls"] < MAX_CALLS:
        if time.monotonic() - start > 240:
            reasons.append("timeout_budget")
            break
        obs = api.getAgentObservation(agentIdx=0)
        projected = observation_for_model(obs)
        prompt = ("Scenario: Plant Nutrients, Normal difficulty. Discover useful evidence through permitted observations and experiments. "
                  "You have no access to the evaluator. Allowed actions (args UUID are integers): "
                  + json.dumps(ACTIONS, sort_keys=True) + ". World observation: " + projected)
        if invalid_in_row:
            prompt += " Previous JSON action was invalid; choose a valid JSON action from allowed set."
        stats["llm_calls"] += 1
        raw, tokens_in, tokens_out = ask_local_model(prompt)
        stats["prompt_tokens"] += tokens_in
        stats["completion_tokens"] += tokens_out
        try:
            action = parse_action(raw, known)
        except (ValueError, json.JSONDecodeError):
            stats["invalid_actions"] += 1
            invalid_in_row += 1
            reasons.append("invalid_model_action")
            if invalid_in_row >= 2:
                reasons.append("two_invalid_in_row")
                break
            continue
        invalid_in_row = 0
        result = api.performAgentAction(agentIdx=0, actionJSON=action)
        api.tick()
        # Action valid in schema, but world may legitimately reject it. Distinguish.
        if result.get("success") is True:
            stats["valid_actions"] += 1
        else:
            stats["invalid_actions"] += 1
            reasons.append("world_action_unsuccessful")
            # Count world actions towards budget (never unlimited retries).
            if stats["llm_calls"] >= MAX_CALLS:
                break
    # Trusted evaluator ONLY, after model loop has terminated. Do not send scorecard to model.
    scorecard = api.getTaskScorecard()
    if not isinstance(scorecard, list) or not scorecard:
        raise RuntimeError("scorer_unavailable")
    score = scorecard[0]
    value = float(score["scoreNormalized"])
    if not 0 <= value <= 1:
        raise RuntimeError("invalid_scorer_range")
    record = {
        "source_commit": "fd591323920be0d3786ef350955de1945aa571e5",
        "model_digest": "7df6b6e09427a769808717c0a93cadc4ae99ed4eb8bf5ca557c90846becea435",
        "scenario": SCENARIO, "difficulty": DIFFICULTY, "seed": SEED,
        "max_actions": MAX_ACTIONS, "max_calls": MAX_CALLS, "max_generated_tokens": MAX_NEW_TOKENS,
        "stats": stats, "failure_categories": sorted(set(reasons)),
        "score_normalized": value, "completed_successfully": bool(score["completedSuccessfully"]),
        "elapsed_seconds": round(time.monotonic()-start, 3),
        "maxrss_kb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "llm_has_code_tools": False,
        "oracle_read_only_after_stop": True,
        "trajectory_audit": "unavailable",
    }
    p = Path(os.environ["RUNNER_TEMP"]) / "t011-private" / "summary.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(record, sort_keys=True))
    # Source engine can print full internal state; STDOUT redirected to private file by workflow.


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--run", action="store_true")
    a = p.parse_args()
    if a.self_test and not a.run:
        self_test()
    elif a.run and not a.self_test:
        run()
    else:
        p.error("select exactly one mode")
