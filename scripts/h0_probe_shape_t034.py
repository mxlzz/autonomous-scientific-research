#!/usr/bin/env python3
"""T0.34 metadata-only classifier of original SciResearch Converse-style response.

DO NOT serialize raw responses, prompts, tool arguments, free-text content or reasoning.
Unknown tool names and finish reasons are reduced to 'other'.
"""
import json

ALLOWED_STOPS = frozenset(("tool_calls", "tool_use", "end_turn", "stop", "length", "max_tokens", "content_filter"))
KNOWN_NAME = "budget_status"

def summarize(response):
    body = response.get("output", {}).get("message", {}).get("content", [])
    if not isinstance(body, list):
        body = []
    uses = [part["toolUse"] for part in body
            if isinstance(part, dict) and isinstance(part.get("toolUse"), dict)]
    kinds = []
    names = []
    for use in uses:
        names.append("budget_status" if use.get("name") == KNOWN_NAME else "other")
        arg = use.get("input")
        if isinstance(arg, dict) and "_unparseable_arguments" in arg:
            kinds.append("invalid_json")
        elif isinstance(arg, dict):
            kinds.append("object")
        elif isinstance(arg, list):
            kinds.append("array")
        elif arg is None:
            kinds.append("missing")
        else:
            kinds.append("scalar")
    raw_stop = response.get("stopReason")
    stop = raw_stop if isinstance(raw_stop, str) and raw_stop in ALLOWED_STOPS else "other"
    usage = response.get("usage") or {}
    def count(key):
        v = usage.get(key, 0)
        if type(v) is int and 0 <= v <= 1000000:
            return v
        return None
    return {
        "probe_tool_count": len(uses),
        "probe_names": names,
        "probe_argument_kinds": kinds,
        "probe_finish_reason": stop,
        "probe_prompt_tokens": count("inputTokens"),
        "probe_completion_tokens": count("outputTokens"),
        "probe_reasoning_content_present": any(
            isinstance(p, dict) and "reasoningContent" in p for p in body),
        "probe_pass": len(uses) == 1 and names == ["budget_status"] and kinds == ["object"],
    }

def test_fixtures():
    secret = "DO_NOT_LOG_PRIVATE_TRUTH_OR_ARGUMENTS_K8FD"
    def fixture(uses, stop="tool_calls", extra=None, usage=None):
        content = ([{"text": secret}, {"reasoningContent": {"reasoningText": {"text": secret}}}]
                   if extra else [])
        content += [{"toolUse": use} for use in uses]
        return {"output": {"message": {"content": content}},
                "stopReason": stop, "usage": usage or {"inputTokens": 64, "outputTokens": 32}}
    trials = [
      ("no_call", fixture([], "stop"), False, 0),
      ("valid", fixture([{"name": "budget_status", "input": {}}]), True, 1),
      ("wrong_tool", fixture([{"name": secret, "input": {}}]), False, 1),
      ("two_calls", fixture([{"name": "budget_status", "input": {}},
                             {"name": "budget_status", "input": {}}]), False, 2),
      ("malformed_json", fixture([{"name": "budget_status", "input":
                                  {"_unparseable_arguments": secret}}]), False, 1),
      ("array_argument", fixture([{"name": "budget_status", "input": [secret]}]), False, 1),
      ("missing_argument", fixture([{"name": "budget_status"}]), False, 1),
      ("length_thinking", fixture([], "length", True), False, 0),
      ("unknown_stop", fixture([], secret), False, 0),
      ("malicious_text", fixture([], "stop", True), False, 0)
    ]
    for name, resp, valid, calls in trials:
        out = summarize(resp)
        assert out["probe_pass"] is valid, name
        assert out["probe_tool_count"] == calls, name
        assert secret not in json.dumps(out), name
        assert set(out) == {"probe_tool_count", "probe_names", "probe_argument_kinds",
                            "probe_finish_reason", "probe_prompt_tokens",
                            "probe_completion_tokens", "probe_reasoning_content_present",
                            "probe_pass"}
        if name == "malformed_json":
            assert out["probe_argument_kinds"] == ["invalid_json"]
        if name == "length_thinking":
            assert out["probe_reasoning_content_present"] is True
            assert out["probe_finish_reason"] == "length"
    print("T034_OFFLINE_SHAPE_FIXTURES_PASS=10", flush=True)
    print("T034_OFFLINE_NO_SECRET_LEAK_PASS=true", flush=True)

if __name__ == "__main__":
    test_fixtures()
