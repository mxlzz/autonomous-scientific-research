#!/usr/bin/env python3
"""T0.24 minimal allowlist experiment; upstream SciResearch-Eval source left unmodified.

The gate here is PROTOTYPED in a trusted evaluator wrapper only.
It is NOT inserted into upstream agents/harness.py, so no actual LLM backend
is claimed secured. This script has no model/network/file tools for an actor.
"""
from __future__ import annotations
import hashlib
import json
import resource
import sys
import time
from pathlib import Path
from sciresearch_eval.agents.tools import AgentTools
from sciresearch_eval.env import ThermalEnv, ToolError
from sciresearch_eval.tasks.generator import public_id_for

SRC="9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0"
TASK="task_525abee377"
ROOT=Path("/project/tasks")
ALL=("A","B","C","D")
start=time.monotonic()

def m(k,v):print("T024_"+k+"="+str(v),flush=True)

def authorized_dispatch(tools: AgentTools,name: str,args: dict):
    # Minimal prototype of a conditional guard at trusted tool dispatch.
    allowed={spec["name"] for spec in tools.specs()}
    if name not in allowed:
        raise ToolError("tool not enabled in this condition")
    return tools.call(name,args)

def test():
    assert public_id_for("t3_coarse_mesh_2001",root=ROOT)==TASK
    out=[]
    denied=("read_file","exec","shell","filesystem","browser")
    for condition in ALL:
        t=AgentTools(ThermalEnv(TASK,ROOT,"dev"),condition)
        exposed={s["name"] for s in t.specs()}
        assert len(exposed)==len(t.specs())
        assert "budget_status" in exposed and "fit_parameters" in exposed
        assert ("update_state" in exposed)==(condition in "CD")
        assert ("recommend_experiment" in exposed)==(condition=="D")
        n=0
        for name in denied:
            try:authorized_dispatch(t,name,{})
            except ToolError:n+=1
            else:raise RuntimeError("unknown_tool_not_rejected")
        assert n==len(denied)
        for name in ("update_state","recommend_experiment"):
            if name in exposed:
                continue  # only test schema permission; expensive recommend is not executed
            try:authorized_dispatch(t,name,{})
            except ToolError:n+=1
            else:raise RuntimeError("unadvertised_tool_not_rejected")
        status=authorized_dispatch(t,"budget_status",{})
        assert set(status)=={"budget","used"}
        f=authorized_dispatch(t,"fit_parameters",{"data_ids":["d0"]})
        assert "fit_id" in f and "estimates" in f
        if condition in "CD":
            result=authorized_dispatch(t,"update_state",{
                "hypotheses":[],"evidence":[],"next_action":"test",
                "why":"condition permission regression"})
            assert result["recorded"] is True
        m("CONDITION_"+condition+"_ADVERTISED_COUNT",len(exposed))
        m("CONDITION_"+condition+"_DENIED_COUNT",n)
        m("CONDITION_"+condition+"_AUTHORIZED_FIT",True)
        m("CONDITION_"+condition+"_AUTHORIZED_UPDATE",condition in "CD")
        out.append({"condition":condition,"schema_names":sorted(exposed),
            "unauthorized_names_denied":n,"authorized_fit":True,
            "authorized_update":condition in "CD"})
    # Verify upstream dispatch is STILL defective on a separate unmodified object.
    original=AgentTools(ThermalEnv(TASK,ROOT,"dev"),"A")
    assert "update_state" not in {s["name"] for s in original.specs()}
    bypass=original.call("update_state",{"hypotheses":[],"evidence":[],
                                        "next_action":"negative_control","why":"audit"})
    assert bypass.get("recorded") is True
    m("UNMODIFIED_UPSTREAM_CONDITION_A_BYPASS_STILL_PRESENT",True)
    m("PROTOTYPE_ALLOWLIST_CONDITIONS_PASS",len(out))
    m("UPSTREAM_HARNESS_PATCH_APPLIED",False)
    m("LLM_BACKEND_END_TO_END_TESTED",False)
    m("PRIVATE_OS_FILE_ISOLATION",False)
    m("PAID_API_CALLS",0)
    m("MODEL_CALLS",0)
    obj={"upstream_commit":SRC,"task":TASK,"scope":"trusted wrapper prototype only",
         "conditions":out,"prototype_guard":"name in {spec['name'] for spec in tools.specs()}",
         "upstream_dispatch_bypass_still_present":True,
         "upstream_harness_patched":False,
         "actual_model_backend_tested":False,
         "os_private_file_isolation_proven":False,
         "model_calls":0,"paid_api_calls":0,
         "wall_sec":round(time.monotonic()-start,4),
         "process_maxrss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    raw=(json.dumps(obj,indent=2,sort_keys=True)+"\n").encode()
    Path("/results/t024_guard.json").write_bytes(raw)
    m("SUMMARY_SHA256",hashlib.sha256(raw).hexdigest())
    m("WALL_SEC",obj["wall_sec"])
    m("PROCESS_MAXRSS_KIB",obj["process_maxrss_kib"])
    m("PROTOTYPE_GATE_PASS",True)
if __name__=="__main__":
    try:test()
    except BaseException as e:
        m("TEST_FAILURE_CLASS",type(e).__name__)
        sys.exit(1)
