#!/usr/bin/env python3
"""T0.29: zero-paid isolated real Ollama tool-calling gate and 1 SciResearch-Eval dev episode.

Trusted evaluator code only. It DOES have public+private dev data to run the upstream
scientific grader; the Ollama container has neither source nor data mounts.
Original code is SHA-verified. Only a COPY of harness/adapter is minimally changed.
No raw model text, data, prompts, transcript or private truth are printed or uploaded.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import sys
import time
import types
import urllib.error
import urllib.request

SRC=Path("/project/src/sciresearch_eval/agents")
OUT=Path("/summary")
PRIVATE=Path("/private-outputs")
MODEL="qwen3:0.6b"
URL="http://ollama:11434/v1"
TASK="task_525abee377"
START=time.monotonic()
records={"upstream_commit":"9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0",
         "public_task":TASK,"model":MODEL,"real_llm":True,
         "private_mounted_only_in_trusted_evaluator":True,
         "model_has_file_or_shell_tools":False,"paid_api_used":False,
         "max_turns":3,"max_tool_calls":4,"max_output_tokens_per_turn":192,
         "score":None,"status":"STARTED","gate":"startup"}

def note(key,value):
    print("T029_"+key+"="+str(value),flush=True)

def gitblob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def publish():
    records["controller_wall_sec"]=round(time.monotonic()-START,3)
    records["process_maxrss_kib"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    raw=(json.dumps(records,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    OUT.mkdir(parents=True,exist_ok=True)
    p=OUT/"t029_summary.json"
    p.write_bytes(raw)
    note("SUMMARY_SHA256",hashlib.sha256(raw).hexdigest())
    note("RESULT_STATUS",records["status"])
    note("RESULT_GATE",records["gate"])
    note("WALL_SEC",records["controller_wall_sec"])
    note("MAXRSS_PROCESS_KIB",records["process_maxrss_kib"])

def diagnostic_stop(stage,clazz):
    records["gate"]=stage
    records["status"]="NO_GO"
    records["stop_class"]=clazz
    note("GATE_STOP",stage)
    note("GATE_STOP_CLASS",clazz)

def import_patched_module(name,source,file):
    dest=Path("/scratch")/file
    dest.write_text(source,encoding="utf-8")
    s=importlib.util.spec_from_file_location(name,str(dest))
    mod=importlib.util.module_from_spec(s)
    sys.modules[name]=mod
    s.loader.exec_module(mod)
    return mod

def patch():
    pieces=[
     ("agents/openai_backend.py","62226f9e814af28593763281ed8cf5e25dc6cc5d"),
     ("agents/harness.py","194a4b36caf4cd702caee34044ec457247644aee")]
    source={}
    for item,digest in pieces:
        raw=(Path("/project/src/sciresearch_eval")/item).read_bytes()
        if gitblob(raw)!=digest:raise ValueError("original_source_sha_mismatch")
        source[item]=raw.decode("utf-8")
    adapter=source["agents/openai_backend.py"]
    for needle,repl in [
        ('"tool_choice": choice, ',''),
        ('timeout_s: float = 900.0','timeout_s: float = 50.0'),
        ('for attempt in range(6):','for attempt in range(1):'),
        ('if attempt == 5:','if attempt == 0:')]:
        if adapter.count(needle)!=1:raise ValueError("unrecognized_adapter_source")
        adapter=adapter.replace(needle,repl)
    harness=source["agents/harness.py"]
    mark='                        payload, status = tools.call(use["name"], use.get("input") or {}), "success"'
    if harness.count(mark)!=1:raise ValueError("dispatch_site_changed")
    harness=harness.replace(mark,
        '                        if use["name"] not in {s["name"] for s in specs}:\n'
        '                            raise ToolError("tool name not announced in this condition")\n'+mark)
    for needle,repl in [
        ("MAX_TURNS = 80","MAX_TURNS = 3"),
        ("MAX_TOOL_CALLS = 60","MAX_TOOL_CALLS = 4"),
        ("MAX_NUDGES = 3","MAX_NUDGES = 1"),
        ("MAX_OUTPUT_TOKENS_PER_TURN = 32000","MAX_OUTPUT_TOKENS_PER_TURN = 192")]:
        if harness.count(needle)!=1:raise ValueError("unrecognized_harness_limits")
        harness=harness.replace(needle,repl)
    # selfhost path should remain zero-billing, no fake scores.
    if "def _run_episode_locked(" not in harness or "grade(env)" not in harness:
        raise ValueError("original_grader_call_missing")
    original={"adapter":hashlib.sha256(source["agents/openai_backend.py"].encode()).hexdigest(),
              "harness":hashlib.sha256(source["agents/harness.py"].encode()).hexdigest()}
    changed={"adapter":hashlib.sha256(adapter.encode()).hexdigest(),
             "harness":hashlib.sha256(harness.encode()).hexdigest()}
    records["original_source_sha256"]=original
    records["patched_copy_sha256"]=changed
    # SciResearch-Eval's selfhost harness imports these modules by the exact name.
    import_patched_module("sciresearch_eval.agents.openai_backend",adapter,"openai_ollama_copy.py")
    return import_patched_module("t029_trusted_harness",harness,"harness_allowlist_copy.py")

def tools_probe():
    req_body={
      "model":MODEL,
      "messages":[{"role":"system","content":"Call only the supplied function."},
                  {"role":"user","content":"Call budget_status with an empty JSON object. Do not answer in text."}],
      "tools":[{"type":"function","function":{"name":"budget_status",
                "description":"Read current computational budget, no arguments.",
                "parameters":{"type":"object","properties":{},"additionalProperties":False}}}],
      "max_tokens":96,
    }
    req=urllib.request.Request(URL+"/chat/completions",data=json.dumps(req_body).encode(),
                               headers={"Content-Type":"application/json"})
    start=time.monotonic()
    try:
        with urllib.request.urlopen(req,timeout=60) as response:
            payload=response.read(131073)
            if len(payload)>131072:raise ValueError("response_too_large")
        data=json.loads(payload)
    except BaseException as e:
        diagnostic_stop("openai_toolcall_probe",type(e).__name__)
        return False
    usage=data.get("usage") or {}
    records["probe_prompt_tokens"]=int(usage.get("prompt_tokens") or 0)
    records["probe_completion_tokens"]=int(usage.get("completion_tokens") or 0)
    records["probe_wall_sec"]=round(time.monotonic()-start,3)
    calls=(data.get("choices") or [{}])[0].get("message",{}).get("tool_calls") or []
    records["probe_tool_calls"]=len(calls)
    if len(calls)!=1 or calls[0].get("function",{}).get("name")!="budget_status":
        diagnostic_stop("openai_toolcall_probe","NO_FUNCTION_TOOLCALL")
        return False
    try:
        args=json.loads(calls[0]["function"]["arguments"] or "{}")
    except (TypeError,ValueError,KeyError):
        diagnostic_stop("openai_toolcall_probe","INVALID_FUNCTION_ARGUMENTS")
        return False
    if args!={}:diagnostic_stop("openai_toolcall_probe","UNEXPECTED_FUNCTION_ARGUMENTS");return False
    note("OPENAI_TOOLCALL_PROBE_PASS",True)
    note("PROBE_PROMPT_TOKENS",records["probe_prompt_tokens"])
    note("PROBE_COMPLETION_TOKENS",records["probe_completion_tokens"])
    records["gate"]="model_toolcalls_verified"
    return True

def mock_bedrock_import_only():
    # Original SciResearch harness imports boto3 at module load even in selfhost mode.
    # Never expose real Bedrock/cloud client; only selfhost code path may be used.
    boto=types.ModuleType("boto3")
    def forbidden(*a,**kw):raise RuntimeError("paid_cloud_client_forbidden")
    boto.client=forbidden
    bc=types.ModuleType("botocore")
    cfg=types.ModuleType("botocore.config")
    cfg.Config=type("Config",(),{"__init__":lambda self,*a,**k:None})
    exc=types.ModuleType("botocore.exceptions")
    for n in ("ClientError","ConnectionClosedError","EndpointConnectionError","ReadTimeoutError"):
        setattr(exc,n,type(n,(Exception,),{}))
    sys.modules.update({"boto3":boto,"botocore":bc,
                        "botocore.config":cfg,"botocore.exceptions":exc})

def main():
    note("PHASE","evaluating_offline_toolonly_candidate")
    note("LLM_ID",MODEL)
    note("PUBLIC_TASK",TASK)
    note("MODEL_FILESYSTEM_ACCESS_TO_PRIVATE",False)
    note("SOURCE_SCIENTIFIC_GRADER_ORIGINAL",True)
    if not (Path("/project/tasks/dev/public")/(TASK+".json")).is_file():
        diagnostic_stop("task_public_exists","MISSING_PUBLIC_TASK");return
    if not (Path("/project/tasks/dev/private")/(TASK+".json")).is_file():
        diagnostic_stop("trusted_evaluator_private_exists","MISSING_PRIVATE_TASK");return
    from sciresearch_eval.tasks.generator import public_id_for
    if public_id_for("t3_coarse_mesh_2001",root=Path("/project/tasks"))!=TASK:
        diagnostic_stop("task_identity","TASK_CHANGED");return
    try:
        mock_bedrock_import_only()
        harness=patch()
    except BaseException as e:
        diagnostic_stop("source_patch_gate",type(e).__name__);return
    note("PATCHED_COPIES_SHA_VERIFIED",True)
    if not tools_probe():return
    records["gate"]="real_model_science_episode"
    t0=time.monotonic()
    try:
        result=harness.run_episode(
            "selfhost:"+MODEL,"A",TASK,0,PRIVATE/"runs",
            root="/project/tasks",split="dev",cache=False,max_usd=1.0,
            form="structured",base_url=URL,
            max_input_tokens=5000)
    except BaseException as e:
        diagnostic_stop("harness_episode",type(e).__name__);return
    records["episode_wall_sec"]=round(time.monotonic()-t0,3)
    if not isinstance(result,dict):
        diagnostic_stop("harness_episode","INVALID_RESULT");return
    stop=str(result.get("stop") or "none")
    # Never print raw stop string because it may contain third-party error texts.
    records["stop_category"]="submitted" if stop=="submitted" else "not_submitted"
    records["stop_error_prefix"]=bool(stop.startswith("error:"))
    usage=result.get("usage") or {}
    for k in ("input_tokens","output_tokens","turns","tool_calls","tool_errors","nudges"):
        records[k]=int(usage.get(k) or 0)
    envused=result.get("env_used") or {}
    records["simulated_experiments_used"]=int(envused.get("experiments") or 0)
    records["simulated_compute_units"]=int(envused.get("compute_units") or 0)
    records["model_paid_api_cost_usd"]=0
    gr=result.get("grade") or {}
    scored=stop=="submitted" and gr.get("submitted") is True
    records["original_scorer_submitted"]=scored
    if scored:
        fields=("param_interval_score","param_coverage","target_interval_score",
                "target_covered","adequacy_correct","attribution_correct","compute_fraction")
        score={}
        for k in fields:
            x=gr.get(k)
            if isinstance(x,(int,float,bool)) or x is None:
                score[k]=x
            else:raise ValueError("unexpected_grade_type")
        records["score"]=score
        records["status"]="SCORED_REAL_LLM_EPISODE"
    else:
        records["status"]="NO_SCORE_REAL_LLM_EPISODE"
    # The original transcript and tool traces remain on trusted private ephemeral disk.
    private_files=list((PRIVATE/"runs").glob("*/transcript.json"))
    if private_files:
        raw=private_files[0].read_bytes()
        records["transcript_sha256"]=hashlib.sha256(raw).hexdigest()
        records["transcript_raw_uploaded"]=False
        try:
            d=json.loads(raw)
            names=[]
            for msg in d:
                for x in msg.get("content",[]):
                    if "toolUse" in x:
                        names.append(x["toolUse"].get("name","unknown"))
            records["tool_names_only"]=names[:12]
        except (ValueError,TypeError,KeyError):
            records["transcript_parse_status"]="invalid_or_nonstandard"
    note("EPISODE_COMPLETED",True)
    note("EPISODE_SUBMITTED",scored)
    for k in ("turns","tool_calls","tool_errors","input_tokens","output_tokens"):
        note("EPISODE_"+k.upper(),records[k])
    if scored:
        for k,v in records["score"].items():
            note("SCORE_"+k.upper(),v)

if __name__=="__main__":
    try:main()
    except BaseException as e:
        diagnostic_stop("trusted_controller",type(e).__name__)
    finally:
        publish()
