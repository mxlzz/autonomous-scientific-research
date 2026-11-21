#!/usr/bin/env python3
"""T0.36 trusted SciResearch evaluator controller, real Ollama tool-only actor.

No model filesystem tools: the Ollama server receives only prompt/tool schemas over
internal HTTP and lives in a separate container with weights only. All private task
data and original grader remain inside this trusted evaluator. Never print raw
task prompts, arguments, tool responses, transcripts or private truth.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
import types

ROOT=Path("/project")
RESULTS=Path("/results")
MODEL="qwen3:1.7b-q4_K_M"
UPSTREAM="9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0"
TASK="task_525abee377"
SERVER="http://ollama:11434/v1"
START=time.monotonic()
SCALAR_KEYS=("param_interval_score","param_coverage","param_log10_error",
    "target_interval_score","target_rel_interval_score","target_covered",
    "target_abs_error_over_sigma","adequacy_correct","attribution_correct",
    "compute_fraction","experiments_used")
STATS={"status":"STARTED","science_status":"NOT_STARTED","model":MODEL,
    "treatment":"reasoning_effort_none","preregister":"T0.36",
    "task":TASK,"upstream_commit":UPSTREAM,"model_calls":0,"api_paid_usd":0,
    "actor_has_evaluator_mount":None,"os_isolation_proven":False,
    "source_is_upstream_unmodified":True,"scientific_scorer_original":True,
    "score":None,"tool_names":[],"tool_statuses":[],"tool_error_kinds":[],"probe_pass":False,
    "guard_integrated_in_loaded_copy":False}
def marker(k,v):print("T036_"+k+"="+str(v),flush=True)
def gitblob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def read_pinned(relative, gitsha):
    data=(ROOT/relative).read_bytes()
    if gitblob(data)!=gitsha:
        raise RuntimeError("upstream_source_gitsha_mismatch")
    return data.decode("utf-8")
def replace_once(s, old, new):
    if s.count(old)!=1:raise RuntimeError("source_patching_unique_anchor_failed")
    return s.replace(old,new,1)
def fake_aws_import_only():
    # Scientific self-host mode never accesses AWS; explicitly prevent any client.
    boto=types.ModuleType("boto3")
    def forbidden(*a,**kw):raise RuntimeError("remote_aws_client_forbidden")
    boto.client=forbidden
    botocore=types.ModuleType("botocore")
    botoconfig=types.ModuleType("botocore.config")
    botoconfig.Config=type("Config",(),{"__init__":lambda self,*a,**kw:None})
    botoexceptions=types.ModuleType("botocore.exceptions")
    for n in ("ClientError","ConnectionClosedError","EndpointConnectionError","ReadTimeoutError"):
        setattr(botoexceptions,n,type(n,(Exception,),{}))
    sys.modules.update({"boto3":boto,"botocore":botocore,
        "botocore.config":botoconfig,"botocore.exceptions":botoexceptions})
def load_module(name,source):
    target=Path("/tmp")/(name.split(".")[-1]+"_t036.py")
    target.write_text(source,encoding="utf-8")
    spec=importlib.util.spec_from_file_location(name,str(target))
    module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

def setup():
    import numpy as np
    from sciresearch_eval.agents.tools import AgentTools
    from sciresearch_eval.env import ThermalEnv
    from sciresearch_eval.tasks.generator import public_id_for
    assert public_id_for("t3_coarse_mesh_2001",root=ROOT/"tasks")==TASK
    agent_src=read_pinned("src/sciresearch_eval/agents/openai_backend.py",
       "62226f9e814af28593763281ed8cf5e25dc6cc5d")
    harness_src=read_pinned("src/sciresearch_eval/agents/harness.py",
       "194a4b36caf4cd702caee34044ec457247644aee")
    read_pinned("src/sciresearch_eval/grader.py",
       "8194044d11b17b6d9d2b040a5115ff35bb798b64")
    read_pinned("src/sciresearch_eval/env.py",
       "ef080f18d9b509c5fc8192186c868265ed04613d")
    read_pinned("src/sciresearch_eval/agents/tools.py",
       "7f2c6e73e4872267ef8bded61880cf620d016c8b")
    src=replace_once(agent_src,
       '"tools": to_openai_tools(tools), "tool_choice": choice, "max_tokens": self.max_tokens',
       '"tools": to_openai_tools(tools), "max_tokens": self.max_tokens')
    # ONLY treatment delta from T0.32: add explicit non-thinking OpenAI field.
    src=replace_once(src,
        '"tools": to_openai_tools(tools), "max_tokens": self.max_tokens',
        '"tools": to_openai_tools(tools), "max_tokens": self.max_tokens, "reasoning_effort": "none"')
    src=replace_once(src,"timeout_s: float = 900.0","timeout_s: float = 90.0")
    src=replace_once(src,"for attempt in range(6):","for attempt in range(1):")
    src=replace_once(src,
        'if attempt == 5:\n                    raise RuntimeError(f"OpenAI-compatible endpoint failed: {exc}") from exc',
        'if attempt == 0:\n                    raise')
    ha=replace_once(harness_src,"MAX_TURNS = 80","MAX_TURNS = 8")
    ha=replace_once(ha,"MAX_TOOL_CALLS = 60","MAX_TOOL_CALLS = 4")
    ha=replace_once(ha,"MAX_OUTPUT_TOKENS_PER_TURN = 32000","MAX_OUTPUT_TOKENS_PER_TURN = 256")
    needle='                        payload, status = tools.call(use["name"], use.get("input") or {}), "success"'
    ha=replace_once(ha,needle,
        '                        if use["name"] not in {s["name"] for s in specs}:\n'
        '                            raise ToolError("tool name not announced for this condition")\n'
        +needle)
    fake_aws_import_only()
    a=load_module("sciresearch_eval.agents.openai_backend",src)
    h=load_module("sciresearch_eval.agents.harness",ha)
    STATS.update({"guard_integrated_in_loaded_copy":True,
                  "adapter_reasoning_effort_none":True,
                  "patched_harness_sha256":hashlib.sha256(ha.encode()).hexdigest(),
                  "patched_adapter_sha256":hashlib.sha256(src.encode()).hexdigest(),
                  "upstream_harness_sha256":hashlib.sha256(harness_src.encode()).hexdigest(),
                  "upstream_adapter_sha256":hashlib.sha256(agent_src.encode()).hexdigest(),
                  "tool_choice_omitted_in_copy":True,
                  "max_turns":4,"max_tool_calls":4,"max_output_tokens_per_turn":256})
    marker("SOURCE_PINS_AND_HARNESS_GUARD",True)
    return a,h,AgentTools(ThermalEnv(TASK,ROOT/"tasks","dev"),"A"),np

def scalar(v):
    if v is None:return None
    import numpy as np
    if isinstance(v,(bool,np.bool_)):return bool(v)
    if isinstance(v,(int,float,np.integer,np.floating)) and math.isfinite(float(v)):return float(v)
    raise ValueError("metric_unexpected_type")

def finish():
    STATS["wall_sec"]=round(time.monotonic()-START,3)
    STATS["process_maxrss_kib"]=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    data=(json.dumps(STATS,sort_keys=True,indent=2,allow_nan=False)+"\n").encode()
    p=RESULTS/"t036_summary.json"
    p.write_bytes(data)
    marker("SUMMARY_SHA256",hashlib.sha256(data).hexdigest())
    for k in ("status","science_status","probe_pass","model_calls",
              "actor_has_evaluator_mount","guard_integrated_in_loaded_copy","wall_sec"):
        marker(k.upper(),STATS[k])
    marker("SUMMARY_WRITTEN",True)

def run():
    a,h,tools,np=setup()
    if os.environ.get("T036_MOUNT_GATE_VERIFIED")!="yes":
        raise RuntimeError("mount_gate_not_verified")
    if os.environ.get("T036_RUNTIME_NO_THINK_VERIFIED")!="yes":
        STATS["status"]="NO_GO_RUNTIME_NO_THINK_UNVERIFIED"
        STATS["runtime_no_think_verified"]=False
        return
    STATS["runtime_no_think_verified"]=True
    STATS["actor_has_evaluator_mount"]=False
    STATS["docker_mount_check_pass"]=True
    if {"exec","read_file","shell"} & {t["name"] for t in tools.specs()}:
        raise RuntimeError("model_tools_expose_fs")
    # Probe the actual OpenAI-compatible endpoint using an original tool schema.
    probe_spec=[spec for spec in tools.specs() if spec["name"]=="budget_status"]
    assert len(probe_spec)==1
    model=a.OpenAICompatAgent(SERVER,MODEL,128,timeout_s=45)
    STATS["status"]="PROBE_REQUEST_SENT"
    try:
        response=model.converse(
           "You are testing a function-call API. Call the provided tool and no other.",
           [{"role":"user","content":[{"text":"/no_think Call budget_status now. Use the tool, no free text."}]}],
           probe_spec,False)
        STATS["model_calls"]+=1
    except BaseException as e:
        STATS["status"]="NO_GO_PROBE_TRANSPORT"
        STATS["probe_error_class"]=type(e).__name__
        marker("PROBE_TRANSPORT",type(e).__name__)
        return
    from probe_shape_t036 import summarize
    probe_shape=summarize(response)
    STATS.update(probe_shape)
    valid=probe_shape["probe_pass"]
    marker("PROBE_VALID_TOOL_CALL",valid)
    for k in ("probe_tool_count","probe_names","probe_argument_kinds",
              "probe_finish_reason","probe_prompt_tokens","probe_completion_tokens",
              "probe_reasoning_content_present"):
        marker(k.upper(),json.dumps(probe_shape[k],separators=(",",":")))
    if not valid:
        STATS["status"]="NO_GO_MODEL_TOOL_CALL"
        return
    # No shell, code execution tool, filesystem mount or oracle interface is
    # exposed to the model; native tools operate inside the evaluator only.
    STATS["status"]="SCIENCE_STARTED"
    begin=time.monotonic()
    try:
        result=h.run_episode("selfhost:"+MODEL,"A",TASK,0,RESULTS/"private",
            root=str(ROOT/"tasks"),split="dev",cache=False,max_usd=1.0,
            form="structured",base_url=SERVER,max_input_tokens=12000)
    except BaseException as e:
        STATS["status"]="SCIENCE_EXCEPTION"
        STATS["science_status"]="ERROR"
        STATS["science_error_class"]=type(e).__name__
        return
    STATS["science_wall_sec"]=round(time.monotonic()-begin,3)
    if result.get("skipped"):
        STATS["status"]="NO_GO_EPISODE_SKIPPED"
        return
    STATS["model_calls"]+=result["usage"].get("turns",0)
    stop_raw=str(result.get("stop","unknown"))
    STATS["science_stop"]=stop_raw.split(":",1)[0]
    if stop_raw.startswith("error: "):
        import re
        match=re.match(r"^error: ([A-Za-z_][A-Za-z0-9_]*)",stop_raw)
        STATS["science_exception_class"]=match.group(1) if match else "UnknownErrorClass"
    STATS["tool_calls"]=int(result["usage"].get("tool_calls",0))
    STATS["tool_errors"]=int(result["usage"].get("tool_errors",0))
    STATS["prompt_tokens"]=int(result["usage"].get("input_tokens",0))
    STATS["completion_tokens"]=int(result["usage"].get("output_tokens",0))
    # Sanitize transcript to names/statuses only; never include args/values.
    dirs=list((RESULTS/"private").glob("*/transcript.json"))
    if len(dirs)==1:
        STATS["private_transcript_sha256"]=hashlib.sha256(dirs[0].read_bytes()).hexdigest()
        transcript=json.loads(dirs[0].read_text())
        for entry in transcript:
            for item in entry.get("content",[]):
                if "toolUse" in item:
                    STATS["tool_names"].append(str(item["toolUse"].get("name","unknown")) if item["toolUse"].get("name") in {s["name"] for s in tools.specs()} else "other")
                if "toolResult" in item:
                    from tool_error_kind_t036 import category
                    raw_status=item["toolResult"].get("status")
                    status=raw_status if raw_status in ("success","error") else "other"
                    STATS["tool_statuses"].append(status)
                    if status=="error":
                        kind=category(item["toolResult"])
                        STATS["tool_error_kinds"].append(kind)
    grade=result.get("grade") or {}
    STATS["submitted"]=bool(grade.get("submitted"))
    if STATS["science_stop"]=="submitted" and STATS["submitted"]:
        STATS["score"]={k:scalar(grade.get(k)) for k in SCALAR_KEYS}
        STATS["science_status"]="SCORED"
        STATS["status"]="SCORED"
    else:
        STATS["science_status"]="NO_SCORE"
        STATS["status"]="SCIENCE_INCOMPLETE"
    marker("SCIENCE_STOP",STATS["science_stop"])
    if STATS.get("science_exception_class"):
        marker("SCIENCE_EXCEPTION_CLASS",STATS["science_exception_class"])
    marker("SCIENCE_SUBMITTED",STATS["submitted"])
    marker("SCIENCE_TOOL_CALLS",STATS["tool_calls"])
    marker("SCIENCE_TOOL_ERRORS",STATS["tool_errors"])
    marker("SCIENCE_ERROR_KINDS",json.dumps(STATS["tool_error_kinds"],separators=(",",":")))
    marker("SCIENCE_PROMPT_TOKENS",STATS["prompt_tokens"])
    marker("SCIENCE_COMPLETION_TOKENS",STATS["completion_tokens"])
    marker("SCIENCE_GRADE_OBSERVED",STATS["science_status"]=="SCORED")
    if STATS["score"]:
        for k,v in STATS["score"].items():marker("SCORE_"+k.upper(),v)

if __name__=="__main__":
    try:run()
    except BaseException as err:
        STATS["status"]="NO_GO_CONTROLLER"
        STATS["error_class"]=type(err).__name__
        marker("STOP_CLASS",type(err).__name__)
    finally:finish()
