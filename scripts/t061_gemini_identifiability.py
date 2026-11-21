#!/usr/bin/env python3
"""T0.61: ONE authorized original synthetic tool-use calibration, no other benchmark."""
import hashlib
import json
import math
import os
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request

MODEL = "gemini-3.5-flash-lite"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai"
TARGET = (3, 0)
MAX_MODEL_CALLS = 3
MAX_MEASUREMENTS = 2
OBSERVATIONS = [[0, 0, 5.0], [1, 1, 10.0], [2, 2, 15.0]]

SYSTEM = (
    "You are examining a fictional noiseless apparatus. The temperature is EXACTLY "
    "additive-linear: T(h,f)=a+b*h+c*f for h,f integers from 0 to 3. "
    "The unknown coefficients are constant. Choose informative measurements to identify "
    "a,b,c, then submit numerical coefficients, the prediction, and a brief explanation. "
    "You may use at most two measurements. Never measure the reserved target (h=3,f=0). "
    "You must use the submit tool to finish. No other outside information is available."
)
USER = (
    "Initial observations (heater,fan,temperature Celsius): "
    "(0,0,5.0); (1,1,10.0); (2,2,15.0). "
    "Predict T(heater=3, fan=0), without measuring that point."
)
TOOLS = [
    {"type": "function", "function": {
        "name": "measure",
        "description": "Measure fictional T(h,f), except target (3,0). At most two measurements.",
        "parameters": {
            "type": "object", "properties": {
                "heater": {"type": "integer", "minimum": 0, "maximum": 3},
                "fan": {"type": "integer", "minimum": 0, "maximum": 3}
            }, "required": ["heater", "fan"], "additionalProperties": False
        }
    }},
    {"type": "function", "function": {
        "name": "submit",
        "description": "Submit estimated coefficients a,b,c and prediction T(3,0) with an explanation.",
        "parameters": {
            "type": "object", "properties": {
                "a": {"type": "number"}, "b": {"type": "number"},
                "c": {"type": "number"}, "predicted_temperature": {"type": "number"},
                "rationale": {"type": "string"}
            }, "required": ["a", "b", "c", "predicted_temperature", "rationale"],
            "additionalProperties": False
        }
    }}
]

def numeric(value):
    return type(value) in (int, float) and math.isfinite(value)

def controls(args):
    return (isinstance(args, dict) and set(args) == {"heater", "fan"}
            and all(type(args[v]) is int and 0 <= args[v] <= 3
                    for v in ("heater", "fan")))

def oracle(h, f):
    return float(5 + 2*h + 3*f)

def score(args, observations, direct_target_attempt):
    result = {
        "science_status": "GRADED_FAIL", "pass": False,
        "absolute_error_c": None, "coefficients_correct": False,
        "off_diagonal_measured": any(h != f for h, f in observations),
        "target_probe_attempted": bool(direct_target_attempt),
        "method_review": "NOT_REVIEWED"
    }
    if not isinstance(args, dict) or not all(numeric(args.get(k))
            for k in ("a", "b", "c", "predicted_temperature")):
        return result
    rationale = args.get("rationale")
    if type(rationale) is not str or len(rationale) > 2000:
        return result
    a, b, c, pred = (float(args[k]) for k in ("a", "b", "c", "predicted_temperature"))
    result["rationale_sha256"] = hashlib.sha256(rationale.encode("utf-8")).hexdigest()
    result["rationale_char_count"] = len(rationale)
    result["absolute_error_c"] = round(abs(pred - 11.0), 6)
    good_coeffs = all(abs(x-y) < 0.25 for x,y in zip((a,b,c),(5.,2.,3.)))
    result["coefficients_correct"] = bool(good_coeffs)
    consistency = (abs(pred - (a + 3*b)) < 0.25 and
                   all(abs(oracle(h,f) - (a+b*h+c*f)) < 0.25 for h,f in observations))
    valid_measurements = bool(observations) and all(h != f and (h,f) != TARGET for h,f in observations)
    passed = (not direct_target_attempt and valid_measurements and good_coeffs
              and abs(pred - 11.0) < 0.25 and consistency)
    result.update({"science_status": "GRADED_PASS" if passed else "GRADED_FAIL", "pass": bool(passed)})
    return result

def categorize_network_error(exc):
    # Deliberately avoid printing exception text (may contain auth or request details).
    underlying = exc.reason if isinstance(exc, urllib.error.URLError) else exc
    if isinstance(underlying, (TimeoutError, socket.timeout)):
        return "socket_timeout"
    if isinstance(underlying, socket.gaierror):
        return "dns_error"
    if isinstance(underlying, ssl.SSLError):
        return "tls_error"
    if isinstance(underlying, ConnectionError):
        return "connection_error"
    return "url_error"

def request_json(url, key, payload=None, timeout=75):
    body = json.dumps(payload, separators=(",", ":")).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url, data=body,
        headers={"Authorization": "Bearer " + key,
                 "Accept": "application/json",
                 **({"Content-Type": "application/json"} if body is not None else {})},
        method="POST" if body is not None else "GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read(250001)
        if len(raw) > 250000:
            raise RuntimeError("oversized_response")
        return json.loads(raw)
    except urllib.error.HTTPError as exc:
        raise RuntimeError("http_" + str(exc.code)) from None
    except (urllib.error.URLError, TimeoutError, ssl.SSLError, socket.timeout) as exc:
        raise RuntimeError(categorize_network_error(exc)) from None
    except (ValueError, TypeError):
        raise RuntimeError("invalid_json_response") from None

def run(key, preflight=None, transport=None):
    if not key or key.isspace():
        raise RuntimeError("missing_secret")
    preflight = preflight or (lambda: request_json(BASE_URL + "/models/" + MODEL, key, timeout=15))
    transport = transport or (lambda payload: request_json(BASE_URL + "/chat/completions", key, payload, timeout=75))
    started = time.monotonic()
    counts = {"model_requests_started": 0, "model_responses_received": 0,
              "measurements": 0, "tool_errors": 0}
    measures = []
    common = {"protocol": "T0.61", "model": MODEL, "preflight": "PENDING",
              "input_tokens_reported": 0, "output_tokens_reported": 0}
    def summary(result):
        return {**common, **counts, "observed_controls": [list(x) for x in measures],
                "wall_s": round(time.monotonic() - started, 3), **result}

    try:
        preflight_result = preflight()
        if not isinstance(preflight_result, dict):
            raise RuntimeError("invalid_model_metadata")
        model_id = str(preflight_result.get("id") or preflight_result.get("name") or "")
        if MODEL not in model_id:
            raise RuntimeError("model_not_visible_in_project")
        common["preflight"] = "MODEL_VISIBLE_NOT_QUOTA_VERIFIED"
    except RuntimeError as exc:
        return summary({"science_status":"NO_SCORE", "pass":None, "submitted":False,
                        "error_stage":"metadata_preflight", "error_category":str(exc)})
    except Exception:
        return summary({"science_status":"NO_SCORE", "pass":None, "submitted":False,
                        "error_stage":"metadata_preflight", "error_category":"unexpected_error"})

    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}]
    attempted_target = False
    for _ in range(MAX_MODEL_CALLS):
        payload = {"model": MODEL, "messages": messages, "tools": TOOLS,
                   "tool_choice": "auto", "max_tokens": 1024, "temperature": 0}
        counts["model_requests_started"] += 1
        try:
            response = transport(payload)
        except RuntimeError as exc:
            return summary({"science_status":"NO_SCORE", "pass":None, "submitted":False,
                            "error_stage":"model_request", "error_category":str(exc)})
        except Exception:
            return summary({"science_status":"NO_SCORE", "pass":None, "submitted":False,
                            "error_stage":"model_request", "error_category":"unexpected_error"})
        counts["model_responses_received"] += 1
        try:
            usage = response.get("usage") or {}
            common["input_tokens_reported"] += int(usage.get("prompt_tokens") or 0)
            common["output_tokens_reported"] += int(usage.get("completion_tokens") or 0)
            choices = response.get("choices") or []
            message = choices[0]["message"]
            calls = message.get("tool_calls") or []
            if not isinstance(calls, list) or len(calls) > 3:
                raise ValueError("invalid_tool_batch")
        except (KeyError, IndexError, TypeError, ValueError):
            return summary({"science_status":"NO_SCORE", "pass":None, "submitted":False,
                            "error_stage":"response_parse", "error_category":"invalid_response_shape"})
        if not calls:
            return summary({"science_status":"NO_SCORE", "pass":None, "submitted":False,
                            "error_stage":"agent_delivery", "error_category":"no_tool_submit"})
        names = [str((v.get("function") or {}).get("name") or "") for v in calls]
        if "submit" in names and (len(calls) != 1 or "measure" in names):
            return summary({"science_status":"GRADED_FAIL", "pass":False, "submitted":False,
                            "error_stage":"protocol", "error_category":"parallel_submit"})
        messages.append({"role":"assistant", "content": message.get("content"),
                         "tool_calls": calls})
        for call in calls:
            func = call.get("function") or {}
            name = func.get("name")
            try:
                args = json.loads(func.get("arguments") or "{}")
            except (ValueError, TypeError):
                args = {}
            if name == "measure":
                if not controls(args):
                    counts["tool_errors"] += 1
                    tool_answer = {"error":"invalid_controls"}
                else:
                    h, f = args["heater"], args["fan"]
                    if (h,f) == TARGET:
                        attempted_target = True
                        return summary({"science_status":"GRADED_FAIL", "pass":False, "submitted":False,
                                        "target_probe_attempted":True,
                                        "error_stage":"protocol", "error_category":"target_probe_forbidden"})
                    if counts["measurements"] >= MAX_MEASUREMENTS:
                        counts["tool_errors"] += 1
                        tool_answer = {"error":"measurement_limit"}
                    else:
                        counts["measurements"] += 1
                        measures.append((h,f))
                        tool_answer = {"temperature_c": oracle(h,f)}
            elif name == "submit":
                report = score(args, measures, attempted_target)
                return summary({"submitted":True, **report})
            else:
                counts["tool_errors"] += 1
                tool_answer = {"error":"unknown_function"}
            messages.append({"role":"tool", "tool_call_id": str(call.get("id","")),
                             "content": json.dumps(tool_answer)})
    return summary({"science_status":"NO_SCORE", "pass":None, "submitted":False,
                    "error_stage":"agent_delivery", "error_category":"max_model_calls_no_submit"})

def offline_tests():
    assert score({"a":5,"b":2,"c":3,"predicted_temperature":11,"rationale":"confounding"},[(0,1)],False)["pass"]
    assert not score({"a":5,"b":2,"c":3,"predicted_temperature":11,"rationale":"x"},[(3,0)],True)["pass"]
    assert not score({"a":5,"b":3,"c":2,"predicted_temperature":11,"rationale":"x"},[(0,1)],False)["pass"]
    assert not score({"a":5,"b":2,"c":3,"predicted_temperature":12,"rationale":"x"},[(0,1)],False)["pass"]
    assert not score({"a":5,"b":2,"c":3,"predicted_temperature":11,"rationale":"x"},[],False)["pass"]
    assert not score({"a":5,"b":2,"c":3,"predicted_temperature":11,"rationale":"x"},[(1,1)],False)["pass"]
    assert not controls({"heater":True,"fan":0})
    assert not controls({"heater":-1,"fan":0})
    assert controls({"heater":0,"fan":1})
    a={"name":"models/"+MODEL}
    def fake_preflight():return a
    answer1={"choices":[{"message":{"tool_calls":[{"id":"fake1","type":"function","function":{"name":"measure","arguments":json.dumps({"heater":0,"fan":1})}}]}}],"usage":{"prompt_tokens":90,"completion_tokens":15}}
    answer2={"choices":[{"message":{"tool_calls":[{"id":"fake2","type":"function","function":{"name":"submit","arguments":json.dumps({"a":5,"b":2,"c":3,"predicted_temperature":11,"rationale":"diagonal observations confound both effects; off-diagonal separates them"})}}]}}],"usage":{"prompt_tokens":95,"completion_tokens":22}}
    responses=[answer1,answer2]
    def fake_post(payload):
        assert payload["model"]==MODEL and len(payload["messages"])>=2
        return responses.pop(0)
    got=run("FAKE_KEY_NEVER_USED",preflight=fake_preflight,transport=fake_post)
    assert got["science_status"]=="GRADED_PASS" and got["model_requests_started"]==2 and got["measurements"]==1 and got["model_responses_received"]==2,got
    def target_post(payload):
        return {"choices":[{"message":{"tool_calls":[{"id":"x","type":"function","function":{"name":"measure","arguments":'{"heater":3,"fan":0}'}}]}}]}
    forbidden=run("FAKE_KEY_NEVER_USED",preflight=fake_preflight,transport=target_post)
    assert forbidden["science_status"]=="GRADED_FAIL" and forbidden["target_probe_attempted"] and forbidden["model_requests_started"]==1
    def timed_out(_):raise RuntimeError("socket_timeout")
    timeout=run("FAKE_KEY_NEVER_USED",preflight=fake_preflight,transport=timed_out)
    assert timeout["science_status"]=="NO_SCORE" and timeout["model_requests_started"]==1 and timeout["model_responses_received"]==0
    print("T061_OFFLINE_TESTS=PASS; scored valid/invalid; tool target isolation; mock episode; timeout counters")

def main():
    if sys.argv[1:]==["--self-test"]:
        offline_tests()
        return 0
    if sys.argv[1:]!=["--run"]:
        return 2
    # Must remain fixed to the verified Free Tier model. Never select a paid-only alternative dynamically.
    if os.getenv("GEMINI_MODEL", MODEL)!=MODEL:
        print(json.dumps({"protocol":"T0.61","science_status":"BLOCKED","error_category":"unapproved_model"}))
        return 2
    key=os.getenv("GEMINI_API_KEY","")
    if not key:
        print(json.dumps({"protocol":"T0.61","science_status":"BLOCKED","error_category":"secret_missing"}))
        return 2
    result=run(key)
    print(json.dumps(result, sort_keys=True, separators=(",",":")))
    # Non-passing science or infra counts as failure; no automated reruns.
    return 0 if result["science_status"]=="GRADED_PASS" else 1

if __name__=="__main__":
    sys.exit(main())
