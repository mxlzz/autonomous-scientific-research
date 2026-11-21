#!/usr/bin/env python3
"""T0.58: ONE original synthetic confounding episode. No benchmark data or raw model logs."""
import json
import os
import sys
import time
import urllib.error
import urllib.request

MODEL_ALLOWLIST = {"gemini-3.8-flash", "gemini-3.5-flash-lite"}
URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
TARGET = 11.0
MAX_REQUESTS = 3
MAX_MEASUREMENTS = 2
TOOLS = [
    {"type": "function", "function": {
        "name": "measure", "description": "Measure stable temperature of a fictional apparatus at selected integer controls.",
        "parameters": {"type": "object", "properties": {
            "heater": {"type": "integer", "minimum": 0, "maximum": 3},
            "fan": {"type": "integer", "minimum": 0, "maximum": 3}},
            "required": ["heater", "fan"], "additionalProperties": False}}},
    {"type": "function", "function": {
        "name": "submit", "description": "Submit your final numerical prediction and short explanation of experimental identifiability.",
        "parameters": {"type": "object", "properties": {
            "predicted_temperature": {"type": "number"},
            "rationale": {"type": "string"}},
            "required": ["predicted_temperature", "rationale"], "additionalProperties": False}}}
]
SYSTEM = ("Study a fictional deterministic lab with two independent controls, heater and fan. "
          "Use available measurement tools if needed. Explain why the initial data may not identify "
          "separate effects. Complete with the submit function, not ordinary text. "
          "You have up to two measurements; prioritize a scientifically informative intervention.")
QUESTION = ("Measurements (heater,fan,temperature C): (0,0,5.0), (1,1,10.0), (2,2,15.0). "
            "Controls are integer 0..3. Predict temperature at heater=3, fan=0; "
            "measure if needed. No assumptions about the formula beyond observed data.")

def valid_controls(args):
    return (isinstance(args, dict) and set(args) == {"heater", "fan"}
            and all(type(args[x]) is int and 0 <= args[x] <= 3 for x in ("heater", "fan")))

def grade(predicted, interventions):
    valid_number = type(predicted) in (int, float) and not isinstance(predicted, bool)
    if not valid_number or not (-10000 < predicted < 10000):
        return {"submitted": True, "science_status": "GRADED_INVALID", "pass": False,
                "absolute_error_c": None, "off_diagonal_measured": any(h != f for h, f in interventions)}
    err = round(abs(predicted - TARGET), 6)
    discriminant = any(h != f for h, f in interventions)
    return {"submitted": True, "science_status": "GRADED", "pass": bool(err <= 0.25 and discriminant),
            "absolute_error_c": err, "off_diagonal_measured": discriminant}

def post(payload, key):
    req = urllib.request.Request(URL, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read(250001)
        if len(data) > 250000:
            raise ValueError("response_too_large")
        return json.loads(data)
    except urllib.error.HTTPError as exc:
        raise RuntimeError("http_" + str(exc.code)) from None
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError("transport_error") from None
    except (ValueError, KeyError, TypeError):
        raise RuntimeError("response_parse_error") from None

def run(model, key, transport=post):
    if model not in MODEL_ALLOWLIST:
        raise RuntimeError("model_not_in_free_allowlist")
    if not key:
        raise RuntimeError("missing_secret")
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": QUESTION}]
    measurements = []
    count = 0
    input_tokens = 0
    output_tokens = 0
    tool_errors = 0
    result = {"science_status": "NO_SCORE", "submitted": False, "pass": None,
              "absolute_error_c": None, "off_diagonal_measured": False}
    started = time.monotonic()
    for _ in range(MAX_REQUESTS):
        payload = {"model": model, "messages": messages, "tools": TOOLS, "tool_choice": "auto",
                   "max_tokens": 900, "temperature": 0}
        response = transport(payload, key)
        count += 1
        usage = response.get("usage") or {}
        input_tokens += int(usage.get("prompt_tokens") or 0)
        output_tokens += int(usage.get("completion_tokens") or 0)
        choices = response.get("choices") or []
        if not choices:
            raise RuntimeError("no_model_choice")
        choice = choices[0]
        message = choice.get("message") or {}
        calls = message.get("tool_calls") or []
        if not calls:
            break
        if not isinstance(calls, list) or len(calls) > 3:
            raise RuntimeError("invalid_tool_batch")
        names = [((c.get("function") or {}).get("name")) for c in calls]
        # Prevent parallel measure+submit: the answer must incorporate the experiment.
        if "measure" in names and "submit" in names:
            raise RuntimeError("parallel_submit_measure")
        messages.append({"role": "assistant", "content": message.get("content"), "tool_calls": calls})
        for call in calls:
            func = call.get("function") or {}
            name = func.get("name")
            try:
                args = json.loads(func.get("arguments") or "{}")
            except (TypeError, ValueError):
                args = {}
            if name == "measure":
                if not valid_controls(args) or len(measurements) >= MAX_MEASUREMENTS:
                    tool_response = {"error": "invalid_measure_or_limit"}
                    tool_errors += 1
                else:
                    h, f = args["heater"], args["fan"]
                    measurements.append((h, f))
                    tool_response = {"temperature_c": float(5 + 2*h + 3*f)}
            elif name == "submit":
                if not isinstance(args, dict) or type(args.get("rationale")) is not str:
                    result["science_status"] = "GRADED_INVALID"
                    result["submitted"] = True
                    result["pass"] = False
                else:
                    result.update(grade(args.get("predicted_temperature"), measurements))
                    # Not a second LLM verdict. Method text requires later human/same-agent audit.
                    result["method_review"] = "PENDING_INDEPENDENT_REVIEW"
                tool_response = {"received": True}
            else:
                tool_response = {"error": "unknown_tool"}
                tool_errors += 1
            messages.append({"role": "tool", "tool_call_id": str(call.get("id", "")),
                             "content": json.dumps(tool_response)})
        if result["submitted"]:
            break
    # Publish only a typed summary; NEVER raw prompts/replies, arguments or auth.
    return {"protocol": "T0.58", "model": model, "requests": count,
            "measurements": len(measurements), "tool_errors": tool_errors,
            "input_tokens_reported": input_tokens, "output_tokens_reported": output_tokens,
            "wall_s": round(time.monotonic() - started, 2), **result}

def self_test():
    assert valid_controls({"heater": 0, "fan": 3})
    assert not valid_controls({"heater": True, "fan": 1})
    assert not valid_controls({"heater": -1, "fan": 1})
    assert not valid_controls({"heater": 1, "fan": 1, "extra": 0})
    assert grade(11, [(0, 1)])["pass"] is True
    assert grade(11, [(1, 1)])["pass"] is False
    assert grade(9, [(0, 1)])["pass"] is False
    assert grade(True, [(0, 1)])["pass"] is False
    assert grade(11, [])["pass"] is False
    def fake_transport(payload, key):
        calls = payload["messages"]
        if len(calls) == 2:
            return {"choices": [{"message": {"tool_calls": [{
                "id": "fake1", "type": "function", "function": {
                    "name": "measure", "arguments": '{"heater":0,"fan":1}'}}]}}],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 10}}
        return {"choices": [{"message": {"tool_calls": [{
            "id": "fake2", "type": "function", "function": {
                "name": "submit", "arguments": '{"predicted_temperature":11.0,"rationale":"The original factors are confounded."}'}}]}}],
                "usage": {"prompt_tokens": 120, "completion_tokens": 20}}
    got = run("gemini-3.8-flash", "TEST_ONLY", transport=fake_transport)
    assert got["pass"] is True and got["requests"] == 2 and got["measurements"] == 1
    assert got["input_tokens_reported"] == 220 and got["method_review"] == "PENDING_INDEPENDENT_REVIEW"
    print("T058_OFFLINE_SCORER_AND_TOOL_FLOW=PASS")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
    elif len(sys.argv) == 2 and sys.argv[1] == "--run":
        model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        # Free-only allowlist even if a repository variable is misconfigured.
        if model not in MODEL_ALLOWLIST:
            print(json.dumps({"protocol":"T0.58","status":"BLOCKED_MODEL_NOT_FREE_ALLOWLIST"}))
            sys.exit(2)
        key = os.getenv("GEMINI_API_KEY", "")
        if not key:
            print(json.dumps({"protocol":"T0.58","status":"BLOCKED_SECRET_MISSING"}))
            sys.exit(2)
        try:
            print(json.dumps(run(model, key), sort_keys=True))
        except RuntimeError as exc:
            # Only bounded internal error codes (never echo HTTP response, header or request).
            msg = str(exc)
            allowed = {"transport_error", "response_parse_error", "no_model_choice",
                       "invalid_tool_batch", "parallel_submit_measure", "model_not_in_free_allowlist"}
            code = msg if msg in allowed or (msg.startswith("http_") and msg[5:].isdigit()) else "unexpected_runtime_error"
            print(json.dumps({"protocol":"T0.58","model":model,"status":"NO_SCORE","error_category":code}))
            sys.exit(1)
    else:
        print("usage: t058_gemini_synthetic.py --self-test | --run", file=sys.stderr)
        sys.exit(2)
