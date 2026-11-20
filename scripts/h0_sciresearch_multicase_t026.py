#!/usr/bin/env python3
"""T0.26: preregistered four public dev SciResearch-Eval tasks, paired scripted policies.

No LLM, no shell/file actor, and no new evaluation logic. The ORIGINAL ThermalEnv and
grade run inside a trusted evaluator, which may read private truth. Report only scalar
grade metrics, task public IDs and resource counts. Child watchdog censors timeouts.
"""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import statistics
import subprocess
import sys
import time

import numpy as np

from sciresearch_eval.baselines.scripted import heuristic, naive
from sciresearch_eval.env import ThermalEnv
from sciresearch_eval.grader import grade
ROOT=Path("/project/tasks")
RESULTS=Path("/results")
UPSTREAM="9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0"
TASKS=[
    ("task_525abee377",39,4,"slab1"),
    ("task_907a7c179a",14,20,"slab1"),
    ("task_b402d13dd9",7,40,"slab1"),
    ("task_147ad98b9e",45,60,"slab1_kT"),
]
POLICIES={"naive":naive,"heuristic":heuristic}
METRICS=("param_interval_score","param_coverage","param_log10_error",
         "target_interval_score","target_covered","target_abs_error_over_sigma",
         "adequacy_correct","attribution_correct","experiments_used","compute_fraction")

def note(k,v):print("T026_"+k+"="+str(v),flush=True)
def metric_value(v):
    if v is None:return None
    if isinstance(v,(bool,np.bool_)):return bool(v)
    if isinstance(v,(float,int,np.floating,np.integer)) and math.isfinite(float(v)):return float(v)
    raise ValueError("unexpected_metric_kind")

def episode(tid,policy):
    start=time.monotonic()
    record={"task":tid,"policy":policy,"status":"INCOMPLETE","score":None}
    try:
        np.random.seed(0)
        env=ThermalEnv(tid,ROOT,"dev")
        POLICIES[policy](env)
        if env.submission is None:raise RuntimeError("no_submission")
        g=grade(env)
        if not g.get("submitted"):raise RuntimeError("grader_not_submitted")
        record.update({"status":"SCORED",
              "score":{k:metric_value(g.get(k)) for k in METRICS},
              "actions":len(env.trace),"compute_units":env.used["compute_units"],
              "experiments":env.used["experiments"],
              "compute_budget":env.budget["compute_units"],
              "wall_sec":round(time.monotonic()-start,4),
              "process_maxrss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    except BaseException as e:
        record.update({"status":"ERROR","error_class":type(e).__name__,
                       "wall_sec":round(time.monotonic()-start,4)})
    dest=RESULTS/(tid+"_"+policy+".json")
    dest.write_text(json.dumps(record,sort_keys=True,allow_nan=False)+"\n")
    if record["status"]!="SCORED":sys.exit(2)

def run_tests():
    spec=importlib.util.spec_from_file_location("original_test_env_grader","/project/tests/test_env_grader.py")
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for n in ("test_interval_score","test_tool_outputs_never_contain_private_fields"):
        getattr(m,n)()
        note("ORIGINAL_TEST_PASS",n)

def run_all():
    started=time.monotonic()
    manifest=json.loads((ROOT/"dev/manifest.json").read_text())
    if len(manifest["tasks"])!=47:raise RuntimeError("dev_manifest_size_mismatch")
    import hashlib
    expected={
       "task_525abee377":39,
       "task_907a7c179a":14,
       "task_b402d13dd9":7,
       "task_147ad98b9e":45,
    }
    for tid,idx,cells,model in TASKS:
        if manifest["tasks"][idx]!=tid:raise RuntimeError("manifest_task_id_mismatch")
        pub=json.loads((ROOT/"dev/public"/(tid+".json")).read_text())
        if pub["default_solver_settings"]["cells_per_layer"]!=cells or pub["supplied_model"]["name"]!=model:
            raise RuntimeError("preregistered_public_fields_changed")
    run_tests()
    note("UPSTREAM",UPSTREAM)
    note("TASK_IDS",",".join(t[0] for t in TASKS))
    note("NO_LLM",True)
    note("OS_PRIVATE_ACTOR_ISOLATION",False)
    observations=[]
    for tid,idx,cells,model in TASKS:
        for name in ("naive","heuristic"):
            limit=15 if name=="naive" else 60
            begin=time.monotonic()
            cmd=[sys.executable,"/controller/t026.py","--episode",tid,name]
            try:
                p=subprocess.run(cmd,capture_output=True,text=True,timeout=limit)
                path=RESULTS/(tid+"_"+name+".json")
                if path.exists():
                    data=json.loads(path.read_text())
                    if data.get("task")!=tid or data.get("policy")!=name:
                        raise RuntimeError("child_result_identity_mismatch")
                    if p.returncode!=0 and data.get("status")=="SCORED":
                        raise RuntimeError("score_from_failed_process")
                else:
                    data={"task":tid,"policy":name,"status":"NO_REPORT","score":None}
                if p.returncode and data["status"]=="NO_REPORT":
                    data["status"]="ERROR_NO_REPORT"
                    data["returncode"]=p.returncode
            except subprocess.TimeoutExpired:
                data={"task":tid,"policy":name,"status":"CENSORED_TIMEOUT",
                      "score":None,"timeout_sec":limit}
            except BaseException as e:
                data={"task":tid,"policy":name,"status":"CONTROLLER_ERROR",
                      "score":None,"error_class":type(e).__name__}
            data["elapsed_parent_wall_sec"]=round(time.monotonic()-begin,4)
            data["cutoff_sec"]=limit
            observations.append(data)
            # All reported information is only PUBLIC ID and scalar scores computed by original grader.
            note("EPISODE_JSON",json.dumps(data,sort_keys=True,separators=(",",":")))
    pairs=[]
    for tid,_,_,_ in TASKS:
        x=next(r for r in observations if r["task"]==tid and r["policy"]=="naive")
        y=next(r for r in observations if r["task"]==tid and r["policy"]=="heuristic")
        pair={"task":tid,"pair_scored":x["status"]==y["status"]=="SCORED"}
        if pair["pair_scored"]:
            a,b=x["score"],y["score"]
            pair.update({"delta_heuristic_minus_naive_param_score":b["param_interval_score"]-a["param_interval_score"],
                         "delta_coverage":b["param_coverage"]-a["param_coverage"],
                         "delta_target_score":b["target_interval_score"]-a["target_interval_score"],
                         "compute_ratio_heuristic_over_naive":(y["compute_units"]/x["compute_units"] if x["compute_units"] else None)})
        pairs.append(pair)
    valid=[p for p in pairs if p["pair_scored"]]
    summary={"source_commit":UPSTREAM,"split":"dev","sampling":"fixed_nonrandom_public_model_and_mesh_bins",
        "task_ids":[t[0] for t in TASKS],"seed":0,"original_policies":["naive","heuristic"],
        "original_grader":"sciresearch_eval.grader.grade","tests_original_passed_count":2,
        "observations":observations,"pairs":pairs,"complete_pairs":len(valid),
        "censored_episodes":sum(r["status"]=="CENSORED_TIMEOUT" for r in observations),
        "failed_other_episodes":sum(r["status"] not in ("SCORED","CENSORED_TIMEOUT") for r in observations),
        "model_calls":0,"paid_api_calls":0,"os_actor_private_isolation":False,
        "wall_sec":round(time.monotonic()-started,3),
        "controller_maxrss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if valid:
        summary["paired_summary"]={
            "param_score_delta_mean":statistics.mean(x["delta_heuristic_minus_naive_param_score"] for x in valid),
            "param_score_delta_median":statistics.median(x["delta_heuristic_minus_naive_param_score"] for x in valid),
            "coverage_delta_mean":statistics.mean(x["delta_coverage"] for x in valid),
            "compute_ratio_median":statistics.median(x["compute_ratio_heuristic_over_naive"] for x in valid if x["compute_ratio_heuristic_over_naive"] is not None),
        }
    raw=(json.dumps(summary,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    (RESULTS/"t026_summary.json").write_bytes(raw)
    note("COMPLETE_PAIRS",summary["complete_pairs"])
    note("CENSORED_EPISODES",summary["censored_episodes"])
    note("FAILED_OTHER_EPISODES",summary["failed_other_episodes"])
    note("SUMMARY_SHA256",hashlib.sha256(raw).hexdigest())
    note("TOTAL_WALL_SEC",summary["wall_sec"])
    note("MAXRSS_CONTROLLER_KIB",summary["controller_maxrss_kib"])
    note("MULTICASE_EXECUTED",True)
    if summary["complete_pairs"]<1:sys.exit(3)

if __name__=="__main__":
    try:
        if len(sys.argv)==4 and sys.argv[1]=="--episode":
            if sys.argv[2] not in {v[0] for v in TASKS} or sys.argv[3] not in POLICIES:
                raise RuntimeError("bad_child_arguments")
            episode(sys.argv[2],sys.argv[3])
        elif len(sys.argv)==1:
            run_all()
        else:raise RuntimeError("invalid_arguments")
    except BaseException as e:
        note("STOP_CLASS",type(e).__name__)
        sys.exit(1)
