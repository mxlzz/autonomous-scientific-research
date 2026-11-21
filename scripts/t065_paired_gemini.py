#!/usr/bin/env python3
"""T0.65: bounded exploratory 2-model x 2-original-task Gemini Free study.

No SciResearch or other benchmark data. No paid endpoints, search grounding,
model fallback or result-driven retries. Output is ONLY typed scientific summaries.
"""
import hashlib
import json
import os
import sys
import time

from t061_gemini_identifiability import BASE_URL, request_json
from t064_cases import CASES, SYSTEM, check_x, measure, score, tools_for

MODELS = ("gemini-3.5-flash-lite", "gemini-3.8-flash")
# Preregistered, preserve order to avoid selecting based on scores.
ORDER = (
    ("mechanisms", "gemini-3.5-flash-lite"),
    ("mechanisms", "gemini-3.8-flash"),
    ("outlier", "gemini-3.8-flash"),
    ("outlier", "gemini-3.5-flash-lite"),
)
MAX_MODEL_REQUESTS = 3
MAX_MEASUREMENTS = 2
MAX_OUTPUT_TOKENS = 1536
SAFE_NETWORK_ERRORS = {
    "socket_timeout", "dns_error", "tls_error", "connection_error",
    "url_error", "invalid_json_response", "oversized_response",
}
def safe_error(error):
    text = str(error)
    if text in SAFE_NETWORK_ERRORS or (text.startswith("http_") and text[5:].isdigit()):
        return text
    return "unexpected_error"

def episode(task, model, send):
    """Transport injection supports offline mock tests with NO secrets or HTTP calls."""
    if task not in CASES or model not in MODELS:
        raise ValueError("unapproved_task_or_model")
    started = time.monotonic()
    history = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": CASES[task]["question"]},
    ]
    observed_x = []
    reqs = replies = n_measures = tool_errors = 0
    tokens_in = tokens_out = 0
    def result(status, submitted=False, **other):
        return {"task": task, "model": model, "science_status": status,
                "submitted": submitted, "requests_started": reqs,
                "responses_received": replies, "measurements": n_measures,
                "observed_x": observed_x.copy(), "tool_errors": tool_errors,
                "input_tokens_reported": tokens_in, "output_tokens_reported": tokens_out,
                "wall_seconds": round(time.monotonic()-started, 3), **other}
    for _ in range(MAX_MODEL_REQUESTS):
        request = {"model": model, "messages": history, "tools": tools_for(task),
                   "tool_choice": "auto", "temperature": 0,
                   "max_tokens": MAX_OUTPUT_TOKENS}
        reqs += 1
        try:
            data = send(request)
        except RuntimeError as exc:
            return result("NO_SCORE", error_stage="model_request", error_category=safe_error(exc))
        except Exception:
            return result("NO_SCORE", error_stage="model_request", error_category="unexpected_error")
        replies += 1
        try:
            usage = data.get("usage") or {}
            tokens_in += int(usage.get("prompt_tokens") or 0)
            tokens_out += int(usage.get("completion_tokens") or 0)
            message = data["choices"][0]["message"]
            calls = message.get("tool_calls") or []
            if not isinstance(calls,list) or not calls or len(calls) > 3:
                raise ValueError("no_or_invalid_tool_calls")
        except (ValueError, TypeError, KeyError, IndexError):
            return result("NO_SCORE", error_stage="response_parse",
                          error_category="no_or_invalid_tool_calls")
        names = [str((c.get("function") or {}).get("name") or "") for c in calls]
        if "submit" in names and len(calls) != 1:
            return result("GRADED_FAIL", error_stage="protocol",
                          error_category="submit_in_parallel")
        history.append({"role": "assistant", "content": message.get("content"),
                        "tool_calls": calls})
        for c in calls:
            function = c.get("function") or {}
            name = function.get("name")
            try:
                args = json.loads(function.get("arguments") or "{}")
            except (TypeError, ValueError):
                args = {}
            if name == "submit":
                grade = score(task, args, observed_x)
                rationale = args.get("rationale") if isinstance(args,dict) else None
                if type(rationale) is str and len(rationale) <= 2000:
                    grade["rationale_sha256"] = hashlib.sha256(
                        rationale.encode("utf-8")).hexdigest()
                    grade["rationale_char_count"] = len(rationale)
                return result(grade.pop("science_status"), **grade)
            if name == "measure":
                if not check_x(task, args):
                    # Invalid measure / holdout probe is a scientifically invalid action.
                    return result("GRADED_FAIL", error_stage="protocol",
                                  error_category="forbidden_or_invalid_measurement")
                x = args["x"]
                if n_measures >= MAX_MEASUREMENTS or x in observed_x:
                    return result("GRADED_FAIL", error_stage="protocol",
                                  error_category="measurement_limit_or_duplicate")
                value = measure(task, x)
                observed_x.append(x)
                n_measures += 1
                answer = value
            else:
                tool_errors += 1
                answer = {"error": "unknown_tool"}
            history.append({"role": "tool", "tool_call_id": str(c.get("id","")),
                            "content": json.dumps(answer)})
    return result("NO_SCORE", error_stage="agent_delivery",
                  error_category="no_submit_within_budget")

def fake_tool_response(name, arguments, ident):
    return {"choices": [{"message": {"role": "assistant", "content": None,
               "tool_calls": [{"id": ident, "type": "function",
                   "function": {"name": name, "arguments": json.dumps(arguments)}}]}}],
            "usage": {"prompt_tokens": 80, "completion_tokens": 30}}
def self_test():
    for task in CASES:
        good_measure = 3 if task=="mechanisms" else 5
        good_submit = ({"model_choice":"B","predicted_y":20.8,"rationale":"sensor at 3 distinguishes"}
                if task=="mechanisms" else {"a":2,"b":3,"outlier_x":3,"predicted_y":20,
                                      "lower":19.5,"upper":20.5,"rationale":"remove outlier"})
        messages = [fake_tool_response("measure", {"x":good_measure}, "t1"),
                    fake_tool_response("submit", good_submit, "t2")]
        def send(payload):
            assert payload["tools"]==tools_for(task)
            assert payload["temperature"]==0
            assert payload["max_tokens"]==MAX_OUTPUT_TOKENS
            return messages.pop(0)
        for model in MODELS:
            messages[:] = [fake_tool_response("measure", {"x":good_measure}, "t1"),
                           fake_tool_response("submit", good_submit, "t2")]
            good = episode(task, model, send)
            assert good["science_status"]=="GRADED_PASS", good
            assert good["requests_started"]==2 and good["responses_received"]==2, good
            assert good["measurements"]==1 and good["submitted"],good
        target = CASES[task]["target"]
        bad=episode(task, MODELS[0], lambda payload:fake_tool_response("measure",{"x":target},"t3"))
        assert bad["science_status"]=="GRADED_FAIL" and bad["requests_started"]==1,bad
        def timeout(payload):raise RuntimeError("socket_timeout")
        lost=episode(task, MODELS[0], timeout)
        assert lost["science_status"]=="NO_SCORE" and lost["responses_received"]==0,lost
    assert len(ORDER)==4 and len(set(ORDER))==4
    print("T065_OFFLINE_PAIR_MOCK=PASS; four cells, positive, target violation, transport no-score")

def run_all(key):
    if not key or key.isspace():
        return {"status":"BLOCKED","reason":"missing_free_project_secret"}, 2
    # Get model visibility, NOT quota evidence, without inferential token usage.
    available = {}
    for model in MODELS:
        try:
            item = request_json(BASE_URL+"/models/"+model, key, timeout=15)
            model_ref = str(item.get("id") or item.get("name") or "")
            available[model] = "MODEL_VISIBLE" if model in model_ref else "MODEL_NOT_VISIBLE"
        except RuntimeError as exc:
            available[model] = "NO_SCORE_"+safe_error(exc)
        except Exception:
            available[model] = "NO_SCORE_unexpected_error"
    result = []
    catastrophic_auth_error = False
    for task, model in ORDER:
        if catastrophic_auth_error:
            result.append({"task":task,"model":model,"science_status":"NO_SCORE",
                           "error_category":"auth_stop"})
            continue
        if available.get(model)!="MODEL_VISIBLE":
            result.append({"task":task,"model":model,"science_status":"NO_SCORE",
                           "error_category":"model_preflight_unavailable"})
            continue
        item = episode(task, model, lambda payload: request_json(
            BASE_URL+"/chat/completions", key, payload, timeout=75))
        if item.get("error_category") in {"http_401","http_403"}:
            catastrophic_auth_error=True
        result.append(item)
    scores = {"GRADED_PASS":0, "GRADED_FAIL":0, "NO_SCORE":0}
    for item in result:
        scores[item["science_status"]] += 1
    return {"protocol":"T0.65", "mode":"FREE_ONLY_ORIGINAL_SYNTHETIC",
            "model_visibility":available, "episode_count":len(result),
            "result_counts":scores, "order":[{"task":t,"model":m} for t,m in ORDER],
            "episodes":result}, 0

if __name__=="__main__":
    if sys.argv[1:]==["--self-test"]:
        self_test()
    elif sys.argv[1:]==["--run"]:
        summary, exit_status=run_all(os.getenv("GEMINI_API_KEY",""))
        # No raw model messages, prompts, request bodies, bearer token or exception text.
        print(json.dumps(summary, separators=(",",":"), sort_keys=True))
        sys.exit(exit_status)
    else:
        sys.exit(2)
