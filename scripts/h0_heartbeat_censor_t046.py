#!/usr/bin/env python3
"""T0.46 offline-only source instrumentation and private-safe progress classifier.

No execution of the SciResearch harness, no private data, no LLM.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

FIXES={
 "            force = \"submit\" if (final_turn or usage[\"nudges\"] >= 2) else None\n            try:\n":
 """            force = "submit" if (final_turn or usage["nudges"] >= 2) else None
            _heartbeat_request_started = time.monotonic()
            print("T047_HEARTBEAT_REQUEST_START_TURN="+str(usage["turns"]+1),flush=True)
            try:
""",
 '            usage["turns"] += 1\n':
 """            print("T047_HEARTBEAT_REQUEST_END_SECONDS="+format(time.monotonic()-_heartbeat_request_started, ".3f"),flush=True)
            usage["turns"] += 1
""",
 '            content = resp["output"]["message"]["content"]\n':
 """            print("T047_HEARTBEAT_PROGRESS="+json.dumps({
                "turns":usage["turns"],"tool_calls":usage["tool_calls"],
                "tool_errors":usage["tool_errors"],"input_tokens":usage["input_tokens"],
                "cache_read_tokens":usage["cache_read_tokens"],
                "cache_write_tokens":usage["cache_write_tokens"],
                "output_tokens":usage["output_tokens"]},
                separators=(",",":"),sort_keys=True),flush=True)
            content = resp["output"]["message"]["content"]
""",
 '                usage["tool_calls"] += 1\n':
 """                usage["tool_calls"] += 1
                print("T047_HEARTBEAT_TOOL_START_COUNT="+str(usage["tool_calls"]),flush=True)
""",
 '            messages.append({"role": "user", "content": results})\n':
 """            messages.append({"role": "user", "content": results})
            print("T047_HEARTBEAT_TOOL_END_COUNT="+str(usage["tool_calls"]),flush=True)
""",
 '    graded = grade(env)\n':
 """    print("T047_HEARTBEAT_SCORER_START=true",flush=True)
    graded = grade(env)
    print("T047_HEARTBEAT_SCORER_SUBMITTED="+str(bool(graded.get("submitted"))).lower(),flush=True)
"""
}
PROGRESS_KEYS=frozenset(("turns","tool_calls","tool_errors",
    "input_tokens","cache_read_tokens","cache_write_tokens","output_tokens"))
COUNT_MARKERS=frozenset(("REQUEST_START_TURN","TOOL_START_COUNT","TOOL_END_COUNT"))
BOOL_MARKERS=frozenset(("SCORER_START","SCORER_SUBMITTED"))
CENSORS={"FINISHED":"COMPLETED","SCIENCE_TIMEOUT":"CENSORED_TIMEOUT",
  "OOM_KILL":"CENSORED_MEMORY","MEMORY_PRESSURE":"CENSORED_MEMORY",
  "MEMORY_METRICS_UNVERIFIED":"CENSORED_UNVERIFIED"}
ACCEPTED_CAUSES=frozenset(("COMPLETED","CENSORED_TIMEOUT","CENSORED_MEMORY",
 "CENSORED_UNVERIFIED","CENSORED_CONTROLLER"))

def instrument_harness(source):
    out=source
    for old,new in FIXES.items():
        if out.count(old)!=1:
            raise ValueError("harness anchor changed; do not patch")
        out=out.replace(old,new)
    compile(out,"<pinned_harness_heartbeat_copy>","exec")
    if out.count("tools.call(")!=source.count("tools.call("):
        raise ValueError("tool dispatch modified")
    if out.count("grade(env)")!=source.count("grade(env)"):
        raise ValueError("grader invocation modified")
    if out.count("agent.converse(")!=source.count("agent.converse("):
        raise ValueError("converse invocation modified")
    if out.count('stop = "limit_turns_or_tokens"')!=source.count('stop = "limit_turns_or_tokens"'):
        raise ValueError("stop modified")
    return out

def censor_reason(reason):
    return CENSORS.get(reason,"CENSORED_CONTROLLER")

def classify_heartbeat(line):
    m=re.fullmatch(r"T047_HEARTBEAT_([A-Z_]+)=(.{1,600})",line)
    if not m:
        return None
    key,raw=m.group(1),m.group(2)
    if key in COUNT_MARKERS:
        if not re.fullmatch("[0-9]{1,9}",raw):
            return None
        return {key:int(raw)}
    if key=="REQUEST_END_SECONDS":
        if not re.fullmatch(r"[0-9]{1,4}\.[0-9]{1,3}",raw):
            return None
        value=float(raw)
        return {key:value} if 0<=value<=3600 else None
    if key in BOOL_MARKERS:
        if raw not in ("true","false"):
            return None
        return {key:raw=="true"}
    if key=="PROGRESS":
        try: value=json.loads(raw)
        except (json.JSONDecodeError,TypeError):return None
        if not isinstance(value,dict) or set(value)!=PROGRESS_KEYS:
            return None
        if any(type(v) is not int or not 0<=v<=1_000_000_000 for v in value.values()):
            return None
        return {key:value}
    return None

def offline_fixtures():
    secret="T046_FORBIDDEN_RAW_PRIVATE_TOOLARGUMENT_NEVER_LOG"
    valid=[
     "T047_HEARTBEAT_REQUEST_START_TURN=1",
     "T047_HEARTBEAT_REQUEST_END_SECONDS=90.001",
     "T047_HEARTBEAT_TOOL_START_COUNT=3",
     "T047_HEARTBEAT_TOOL_END_COUNT=3",
     "T047_HEARTBEAT_SCORER_START=true",
     "T047_HEARTBEAT_SCORER_SUBMITTED=false",
     "T047_HEARTBEAT_PROGRESS="+json.dumps({k:4 for k in PROGRESS_KEYS},separators=(",",":"))
    ]
    for item in valid:
        out=classify_heartbeat(item)
        assert out is not None and secret not in json.dumps(out),item
    invalid=[
     "T047_HEARTBEAT_REQUEST_START_TURN="+secret,
     "T047_HEARTBEAT_REQUEST_START_TURN=-1",
     "T047_HEARTBEAT_REQUEST_START_TURN=1.5",
     "T047_HEARTBEAT_REQUEST_END_SECONDS="+secret,
     "T047_HEARTBEAT_REQUEST_END_SECONDS=nan",
     "T047_HEARTBEAT_SCORER_SUBMITTED="+secret,
     "T047_HEARTBEAT_PROGRESS="+json.dumps({**{k:4 for k in PROGRESS_KEYS},"raw":secret}),
     "T047_HEARTBEAT_PROGRESS="+json.dumps({k:(secret if k=="turns" else 1) for k in PROGRESS_KEYS}),
     "T047_HEARTBEAT_UNKNOWN="+secret,
     "T047_HEARTBEAT_PROGRESS={",
     secret
    ]
    for item in invalid:
        assert classify_heartbeat(item) is None,item
    assert censor_reason("SCIENCE_TIMEOUT")=="CENSORED_TIMEOUT"
    assert censor_reason("FINISHED")=="COMPLETED"
    assert censor_reason("MEMORY_PRESSURE")=="CENSORED_MEMORY"
    assert censor_reason("OOM_KILL")=="CENSORED_MEMORY"
    assert censor_reason("MEMORY_METRICS_UNVERIFIED")=="CENSORED_UNVERIFIED"
    assert censor_reason("bogus")=="CENSORED_CONTROLLER"
    assert censor_reason("SCIENCE_TIMEOUT")!="CENSORED_MEMORY"
    assert secret not in json.dumps([classify_heartbeat(x) for x in valid])
    print("T046_OFFLINE_HEARTBEAT_FIXTURES_PASS=18",flush=True)
    print("T046_CENSOR_CLASSIFICATION_FIXTURES_PASS=7",flush=True)
    print("T046_NO_PRIVATE_MARKER_LEAK=true",flush=True)

def verify_source(path):
    source=Path(path).read_text()
    updated=instrument_harness(source)
    assert updated.count("T047_HEARTBEAT_")>=7
    print("T046_PINNED_HARNESS_HEARTBEAT_PATCH_COMPILES=true",flush=True)
    print("T046_TOOL_DISPATCH_AND_GRADER_UNCHANGED=true",flush=True)
    print("T046_REQUEST_PROGRESS_AND_SCORER_MARKERS_PRESENT=true",flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--offline-test",action="store_true")
    p.add_argument("--source")
    args=p.parse_args()
    if not args.offline_test:
        p.error("offline-only; --offline-test required")
    offline_fixtures()
    if args.source:
        verify_source(args.source)

if __name__=="__main__":
    main()
