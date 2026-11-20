#!/usr/bin/env python3
"""T0.25: actual original SciResearch-Eval harness tool-use receiving path with fake backend.

Uses source from the pinned checkout. One line-of-defense is added to a TEMP COPY
of harness.py, NOT the upstream or scientific grader. The mock is trusted test code
in the evaluator process and does NOT establish an OS isolation of private truth.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time
import types

ORIGINAL=Path("/project/src/sciresearch_eval/agents/harness.py")
TID="task_525abee377"
start=time.monotonic()

def note(k,v): print("T025_"+k+"="+str(v),flush=True)
def gitblob(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

class MockOpenAICompatAgent:
    """Deterministic responder of four toolUses, no model, network or credentials."""
    def __init__(self,*args,**kwargs):
        self.pos=0
    def converse(self,system,messages,specs,cache,force_tool=None):
        self.pos+=1
        if self.pos==1:
            name="update_state"  # unadvertised in A; original accepts, guarded rejects
            arg={"hypotheses":[],"evidence":[],"next_action":"fake","why":"test"}
        elif self.pos==2:
            name="budget_status"
            arg={}
        elif self.pos==3:
            name="read_file"
            arg={}
        elif self.pos==4:
            name="submit"
            first=messages[0]["content"][0]["text"]
            public=json.loads(first.split("Task (JSON):\n",1)[1].split("\n\nBegin your investigation.",1)[0])
            params={p:{"estimate":1.0,"ci95":[0.5,2.0]}
                    for p in public["supplied_model"]["free_parameters"]}
            arg={"parameters":params,
                 "hidden_target_prediction":{"estimate":300.0,"ci95":[250.0,350.0]},
                 "model_adequate":"uncertain","misfit_cause":"unknown",
                 "stop_reason":"insufficient_evidence"}
        else:
            raise AssertionError("mock called unexpectedly")
        return {"usage":{"inputTokens":1,"outputTokens":1},
                "output":{"message":{"content":[{"toolUse":{
                  "toolUseId":"mock-"+str(self.pos),"name":name,"input":arg}}]}},
                "stopReason":"tool_use"}

def fake_modules():
    # Avoid installing boto3 or contacting any AWS/OpenAI service.
    boto=types.ModuleType("boto3")
    def fail_client(*a,**kw): raise RuntimeError("paid/network client is forbidden")
    boto.client=fail_client
    bc=types.ModuleType("botocore")
    cfg=types.ModuleType("botocore.config")
    cfg.Config=type("Config",(),{"__init__":lambda self,*a,**k:None})
    exc=types.ModuleType("botocore.exceptions")
    for name in ("ClientError","ConnectionClosedError","EndpointConnectionError","ReadTimeoutError"):
        setattr(exc,name,type(name,(Exception,),{}))
    oc=types.ModuleType("sciresearch_eval.agents.openai_backend")
    oc.OpenAICompatAgent=MockOpenAICompatAgent
    sys.modules.update({"boto3":boto,"botocore":bc,
                        "botocore.config":cfg,"botocore.exceptions":exc,
                        "sciresearch_eval.agents.openai_backend":oc})

def load(source,path):
    dest=Path("/results")/path
    dest.write_text(source,encoding="utf-8")
    spec=importlib.util.spec_from_file_location("harness_test_"+path.replace(".","_"),str(dest))
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m,dest

def run_harness(m, label):
    outdir=Path("/results")/("episodes_"+label)
    result=m.run_episode("selfhost:mock-offline","A",TID,0,outdir,
          root="/project/tasks",split="dev",max_usd=1.0,cache=False,
          form="structured",base_url="offline://mock",
          max_input_tokens=1000)
    assert result["stop"]=="submitted",result["stop"]
    assert result["usage"]["tool_calls"]==4
    assert result["usage"]["turns"]==4
    transcripts=list(outdir.glob("*/transcript.json"))
    states=list(outdir.glob("*/state_log.json"))
    assert len(transcripts)==len(states)==1
    conversation=json.loads(transcripts[0].read_text())
    statuses=[x["toolResult"]["status"] for entry in conversation
              for x in entry.get("content",[]) if "toolResult" in x]
    state_entries=json.loads(states[0].read_text())
    assert len(statuses)==4
    note(label.upper()+"_STATUSES",",".join(statuses))
    note(label.upper()+"_UNADVERTISED_STATE_RECORDS",len(state_entries))
    note(label.upper()+"_MODEL_CALLS_REAL",0)
    return {"statuses":statuses,"state_entries":len(state_entries),
            "stopped":result["stop"],
            "mock_backend_turns":result["usage"]["turns"],
            "mock_tool_calls":result["usage"]["tool_calls"],
            "original_grader_ran":result["grade"].get("submitted",False)}

def main():
    raw=ORIGINAL.read_bytes()
    expected="194a4b36caf4cd702caee34044ec457247644aee"
    if gitblob(raw)!=expected: raise RuntimeError("harness_git_blob_changed")
    note("UPSTREAM_HARNESS_GIT_BLOB_MATCH",True)
    original=raw.decode("utf-8")
    needle='                        payload, status = tools.call(use["name"], use.get("input") or {}), "success"'
    if original.count(needle)!=1:raise RuntimeError("unique_dispatch_site_not_found")
    guarded=original.replace(needle,
       '                        if use["name"] not in {s["name"] for s in specs}:\n'
       '                            raise ToolError("tool name not announced for this condition")\n'
       +needle)
    note("ORIGINAL_SOURCE_SHA256",hashlib.sha256(raw).hexdigest())
    note("PATCHED_SOURCE_SHA256",hashlib.sha256(guarded.encode()).hexdigest())
    fake_modules()
    old,oldfile=load(original,"harness_original_copy.py")
    new,newfile=load(guarded,"harness_guard_copy.py")
    # No LLM calls, and private gold remains inside evaluator.
    unchanged=run_harness(old,"original")
    fixed=run_harness(new,"guarded")
    assert unchanged["statuses"]==["success","success","error","success"]
    assert fixed["statuses"]==["error","success","error","success"]
    assert unchanged["state_entries"]==1 and fixed["state_entries"]==0
    note("UNPATCHED_HARNESS_CONFIRMS_BYPASS",True)
    note("PATCHED_HARNESS_DISPATCH_BLOCKS_UNADVERTISED",True)
    note("VALID_TOOLS_STILL_WORK",True)
    note("UPSTREAM_REPO_MODIFIED",False)
    note("MODEL_REAL_CALLS",0)
    note("BACKEND_MOCK_CALLS_PER_EPISODE",4)
    note("ACTOR_PRIVATE_OS_ISOLATION_PROVEN",False)
    note("COST_USD_PAID_API",0)
    obj={"source_repo":"Btwestyo/sciresearch-eval",
         "source_commit":"9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0",
         "upstream_harness_sha":hashlib.sha256(raw).hexdigest(),
         "patched_copy_sha":hashlib.sha256(guarded.encode()).hexdigest(),
         "source_code_modified_upstream":False,
         "model_real_calls":0,"fake_backend_tool_uses_per_run":4,
         "scorer_original":True,
         "unpatched_harness":unchanged,"patched_harness":fixed,
         "scope":"real harness receiving loop using offline fake selfhosted agent; no OS isolation",
         "actor_private_os_isolation":False,
         "wall_sec":round(time.monotonic()-start,4),
         "process_maxrss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    dest=Path("/results/t025_summary.json")
    data=(json.dumps(obj,indent=2,sort_keys=True)+"\n").encode()
    dest.write_bytes(data)
    note("SUMMARY_SHA256",hashlib.sha256(data).hexdigest())
    note("WALL_SEC",obj["wall_sec"])
    note("MAXRSS_KIB",obj["process_maxrss_kib"])
    note("HARNESS_PATCHED_COPY_GATE_PASS",True)

if __name__=="__main__":
    try:main()
    except BaseException as e:
        note("STOP_EXCEPTION_CLASS",type(e).__name__)
        note("STATUS","INCOMPLETE_OR_FAILED")
        sys.exit(1)
