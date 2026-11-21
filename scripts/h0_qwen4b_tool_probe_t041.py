#!/usr/bin/env python3
"""One public synthetic tool-call probe, never benchmark science or raw output.

Strictly one OpenAI-compatible inference request. No retries or tool execution.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request

from h0_qwen4b_preflight_t040 import get_json, inspect, MODEL

DIGEST="0edcdef34593eac1aa2be9c7d06c432dcf81945adca5eca2f27662c18f168ba0"
REQUIRED_VERSION="0.40.16"
ALLOW_FINISH={"tool_calls","stop","length","content_filter"}
PUBLIC_PROMPT="/no_think Call budget_status now. Use the tool, no free text."
TOOL_SCHEMA={"type":"function","function":{"name":"budget_status",
    "description":"Remaining experiment and compute budget.",
    "parameters":{"type":"object","properties":{}}}}

def classify_response(raw):
    choices=raw.get("choices")
    choice=choices[0] if isinstance(choices,list) and choices and isinstance(choices[0],dict) else {}
    message=choice.get("message") if isinstance(choice.get("message"),dict) else {}
    calls=message.get("tool_calls")
    calls=calls if isinstance(calls,list) else []
    names=[]
    kinds=[]
    for item in calls:
        item=item if isinstance(item,dict) else {}
        fn=item.get("function") if isinstance(item.get("function"),dict) else {}
        names.append("budget_status" if fn.get("name")=="budget_status" else "other")
        arg=fn.get("arguments")
        if isinstance(arg,str):
            try: parsed=json.loads(arg or "{}")
            except json.JSONDecodeError: kind="invalid_json"
            else: kind=("object" if isinstance(parsed,dict) else
                        "array" if isinstance(parsed,list) else "other")
        else: kind="missing"
        kinds.append(kind)
    finish=choice.get("finish_reason")
    finish=finish if isinstance(finish,str) and finish in ALLOW_FINISH else "other"
    usage=raw.get("usage")
    usage=usage if isinstance(usage,dict) else {}
    def tokens(key):
        value=usage.get(key)
        return value if type(value) is int and 0<=value<=1000000 else None
    return {"tool_count":len(calls),"tool_names":names,"argument_kinds":kinds,
        "finish_reason":finish,"prompt_tokens":tokens("prompt_tokens"),
        "completion_tokens":tokens("completion_tokens"),
        "reasoning_content_present":bool(message.get("reasoning_content")),
        "probe_pass":len(calls)==1 and names==["budget_status"] and
                      kinds==["object"] and finish=="tool_calls"}

def fixtures():
    secret="SENSITIVE_PRIVATE_ARGUMENT_UNLOGGED_UX40"
    def fake(calls,finish="tool_calls",extra=None):
        return {"choices":[{"finish_reason":finish,
              "message":{"tool_calls":calls,"content":secret,"reasoning_content":extra}}],
              "usage":{"prompt_tokens":160,"completion_tokens":17}}
    def call(name="budget_status",arguments="{}"):
        return {"type":"function","function":{"name":name,"arguments":arguments}}
    cases=[
      ("valid",fake([call()]),True,"object"),
      ("no_call",fake([],finish="stop"),False,None),
      ("wrong_name",fake([call(secret)]),False,"object"),
      ("multiple",fake([call(),call()]),False,"object"),
      ("invalid_json",fake([call(arguments="{")]),False,"invalid_json"),
      ("array",fake([call(arguments="[1]")]),False,"array"),
      ("missing",fake([call(arguments=None)]),False,"missing"),
      ("length",fake([],finish="length"),False,None),
      ("text_only",fake([],finish="stop",extra=secret),False,None)
    ]
    for name,raw,ok,kind in cases:
        out=classify_response(raw)
        assert out["probe_pass"] is ok,name
        assert secret not in json.dumps(out),name
        if kind is not None: assert out["argument_kinds"][0]==kind,name
    print("T041_OFFLINE_SHAPE_FIXTURES_PASS=9",flush=True)
    print("T041_NO_PRIVATE_OUTPUT_EXPOSURE=true",flush=True)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--offline-test",action="store_true")
    parser.add_argument("--run-one",action="store_true")
    args=parser.parse_args()
    if args.offline_test:
        fixtures()
    if not args.run_one:
        return 0
    info=inspect(get_json("/api/tags"),get_json("/api/show",{"model":MODEL}),get_json("/api/version"))
    correct=info["metadata_gate_pass"] and info["full_manifest_digest"]==DIGEST and info["ollama_version"]==REQUIRED_VERSION
    print("T041_PINNED_RUNTIME_GATE="+str(correct).lower(),flush=True)
    if not correct:
        print("T041_DECISION=NO_GO_RUNTIME_OR_MODEL",flush=True)
        return 3
    body={"model":MODEL,
        "messages":[{"role":"system","content":"Use the provided function when directly requested."},
                    {"role":"user","content":PUBLIC_PROMPT}],
        "tools":[TOOL_SCHEMA],
        "max_tokens":128,"stream":False,"reasoning_effort":"none"}
    req=urllib.request.Request(
        "http://127.0.0.1:11434/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json"},method="POST")
    print("T041_INFERENCE_REQUEST_COUNT=1",flush=True)
    start=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=90) as r:
            raw=json.load(r)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,ValueError,KeyError) as exc:
        elapsed=round(time.monotonic()-start,3)
        print("T041_TRANSPORT_ERROR_CLASS="+type(exc).__name__,flush=True)
        print("T041_ELAPSED_SECONDS="+str(elapsed),flush=True)
        print("T041_DECISION=NO_GO_TRANSPORT",flush=True)
        return 2
    elapsed=round(time.monotonic()-start,3)
    classified=classify_response(raw)
    for k,v in classified.items():
        print("T041_"+k.upper()+"="+json.dumps(v,separators=(",",":")),flush=True)
    print("T041_ELAPSED_SECONDS="+str(elapsed),flush=True)
    print("T041_DECISION="+("PASS_ONE_TOOL_PROBE" if classified["probe_pass"] else "NO_GO_TOOL_PROBE"),flush=True)
    return 0 if classified["probe_pass"] else 1

if __name__=="__main__":
    sys.exit(main())
