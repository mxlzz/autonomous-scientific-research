#!/usr/bin/env python3
"""Offline-only SciResearch source-patch and strict privacy-safe tool category validation.

The output is only {category, outcome}; never raw tool name, prompt, result or error.
"""
import argparse
import json
import re
from pathlib import Path

GROUPS={
  "run_simulation":"simulation",
  "fit_parameters":"fitting",
  "request_measurement":"measurement",
  "analyze":"analysis",
  "recommend_experiment":"analysis",
  "get_readings":"reading",
  "get_residuals":"reading",
  "budget_status":"status",
  "update_state":"state",
  "submit":"submission",
}
CATEGORIES=frozenset((*GROUPS.values(),"other"))
OUTCOMES=frozenset(("success","error"))
PATCH_SOURCE_ANCHOR='from sciresearch_eval.grader import grade\n'
PATCH_EVENT_ANCHOR='                if status == "error":\n                    usage["tool_errors"] += 1\n'
PATCH_EVENT_APPEND=(
 '                print("T052_TOOL_EVENT="+json.dumps({"category":_t051_tool_group(use.get("name")),'
 ' "outcome":status},separators=(",",":"),sort_keys=True),flush=True)\n'
)

def tool_group(name):
    # Only fixed public tool categories; model text cannot survive to the output.
    return GROUPS.get(name,"other") if isinstance(name,str) else "other"

def parse_event(line):
    m=re.fullmatch(r"T052_TOOL_EVENT=(.{1,160})",line)
    if not m:return None
    try:v=json.loads(m.group(1))
    except (ValueError,TypeError):return None
    if not isinstance(v,dict) or set(v)!={"category","outcome"}:return None
    if type(v["category"]) is not str or v["category"] not in CATEGORIES:return None
    if type(v["outcome"]) is not str or v["outcome"] not in OUTCOMES:return None
    return v

def patch_harness(source):
    if source.count(PATCH_SOURCE_ANCHOR)!=1 or source.count(PATCH_EVENT_ANCHOR)!=1:
        raise ValueError("source pin/anchor mismatch, do not patch")
    out=source.replace(PATCH_SOURCE_ANCHOR,
       PATCH_SOURCE_ANCHOR+"from h0_tool_categories_t051 import tool_group as _t051_tool_group\n")
    out=out.replace(PATCH_EVENT_ANCHOR,PATCH_EVENT_ANCHOR+PATCH_EVENT_APPEND)
    compile(out,"<t051-tool-categories-verified-copy>","exec")
    for key in ("tools.call(","agent.converse(","grade(env)","if tools.submitted:","stop = \"submitted\""):
        if out.count(key)!=source.count(key):raise ValueError("science control changed: "+key)
    return out

def fixtures():
    secret="PRIVATE_TRUTH_TOOL_ARGUMENT_NEVER_LEAK_T051"
    expected={v for v in GROUPS.values()}
    assert expected|{"other"}==CATEGORIES
    for name,group in GROUPS.items():
        assert tool_group(name)==group
        for outcome in OUTCOMES:
            line="T052_TOOL_EVENT="+json.dumps({"category":tool_group(name),"outcome":outcome},separators=(",",":"))
            got=parse_event(line)
            assert got=={"category":group,"outcome":outcome}
            assert name not in line and secret not in line
    for x in (secret,None,123,{},[]):
        assert tool_group(x)=="other"
    failures=[
      "T052_TOOL_EVENT="+secret,
      "T052_TOOL_EVENT="+json.dumps({"category":"measurement","outcome":"error","args":secret}),
      "T052_TOOL_EVENT="+json.dumps({"category":secret,"outcome":"success"}),
      "T052_TOOL_EVENT="+json.dumps({"category":"analysis","outcome":secret}),
      "T052_TOOL_EVENT="+json.dumps({"category":"request_measurement","outcome":"success"}),
      "T052_TOOL_EVENT="+json.dumps(["measurement","success"]),
      "T052_TOOL_EVENT={",
      "T052_TOOL_EVENT="+json.dumps({"category":True,"outcome":"error"}),
      "T052_TOOL_EVENT="+json.dumps({"category":"other","outcome":True}),
      "T052_TOOL_EVENT="+json.dumps({"category":"submission"}),
      secret
    ]
    assert all(parse_event(x) is None for x in failures)
    assert secret not in json.dumps([parse_event(x) for x in failures])
    print("T051_TOOL_CATEGORY_VALID_FIXTURES_PASS="+str(len(GROUPS)*len(OUTCOMES)),flush=True)
    print("T051_TOOL_CATEGORY_REJECTED_FIXTURES_PASS="+str(len(failures)),flush=True)
    print("T051_TOOL_CATEGORY_PRIVATE_LEAK=false",flush=True)

def test_source(path,tools_path=None):
    source=Path(path).read_text()
    patched=patch_harness(source)
    assert patched.count("T052_TOOL_EVENT=")==1
    assert 'tools.call(use["name"], use.get("input") or {})' in patched
    if tools_path:
        raw=Path(tools_path).read_text()
        assert 'if self.condition in ("C", "D"):' in raw
        assert 'tools.append(STATE_TOOL)' in raw
        assert 'if self.condition == "D":' in raw
        for tool in ("run_simulation","fit_parameters","request_measurement",
                     "analyze","get_readings","get_residuals","budget_status","submit"):
            assert ('"name": "'+tool+'"') in raw
        print("T051_CONDITION_A_BASE_TOOLS_NO_STATE_TOOL_SOURCE_CHECK=true",flush=True)
    print("T051_PINNED_HARNESS_CATEGORY_PATCH_COMPILES=true",flush=True)
    print("T051_SCIENCE_DISPATCH_AND_GRADER_CALLS_UNCHANGED=true",flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--offline-test",action="store_true")
    p.add_argument("--harness")
    p.add_argument("--tools")
    a=p.parse_args()
    if not a.offline_test:p.error("offline-only")
    fixtures()
    if a.harness:test_source(a.harness,a.tools)

if __name__=="__main__":
    main()
