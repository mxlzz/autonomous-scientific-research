#!/usr/bin/env python3
"""T0.45: monitor science actor cgroup while ONE original evaluator episode runs.

No raw evaluator stdout, tool arguments, prompts, private traces or model text printed.
Stop evaluator at first observed memory-limit/oom/swap-growth event or deadline.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from h0_cgroup_pressure_t045 import sample,deltas,safe_print

STAT_KEYS={"SCIENCE_TURNS","SCIENCE_TOOL_CALLS","SCIENCE_TOOL_ERRORS",
 "SCIENCE_PROMPT_TOKENS","SCIENCE_CACHE_READ_TOKENS","SCIENCE_CACHE_WRITE_TOKENS",
 "SCIENCE_TOTAL_INPUT_TOKENS","SCIENCE_MAX_TURNS","SCIENCE_MAX_TOOL_CALLS",
 "SCIENCE_COMPLETION_TOKENS","MODEL_CALLS","WALL_SEC"}
BOOL_KEYS={"SOURCE_PINS_AND_HARNESS_GUARD","PREP_PROBE_GATE_VERIFIED",
 "SCIENCE_SUBMITTED","SCIENCE_GRADE_OBSERVED","PROBE_PASS",
 "ACTOR_HAS_EVALUATOR_MOUNT","GUARD_INTEGRATED_IN_LOADED_COPY","SUMMARY_WRITTEN"}
STATE_VALUES={"STARTED","SCIENCE_STARTED","NO_GO_CONTROLLER","NO_GO_PREP_GATE_NOT_VERIFIED",
 "SCIENCE_EXCEPTION","SCIENCE_INCOMPLETE","SCORED","NO_SCORE","NOT_STARTED",
 "ERROR","NO_GO_EPISODE_SKIPPED","SKIPPED","SCORED"}
LIMITS={"turns_only","tokens_only","both","None"}
ERROR_KINDS={"final_turn_non_submit","tool_limit","invalid_arguments","tool_error","other"}

def classified_lines(log):
    allowed={}
    for line in log.splitlines():
        m=re.fullmatch(r"T045_([A-Z0-9_]+)=(.{1,3000})",line)
        if not m:
            continue
        name,raw=m.group(1),m.group(2)
        value=None
        if name in STAT_KEYS:
            try:
                num=float(raw)
                if 0<=num<=1e9 and num==num and num!=float("inf"):
                    value=num
            except ValueError:pass
        elif name.startswith("SCORE_") and re.fullmatch("[A-Z0-9_]{1,80}",name):
            try:
                num=float(raw)
                if abs(num)<=1e9 and num==num and num!=float("inf") and num!=float("-inf"):
                    value=num
            except ValueError:pass
        elif name in BOOL_KEYS and raw in ("True","False"):
            value=(raw=="True")
        elif name in ("STATUS","SCIENCE_STATUS") and raw in STATE_VALUES:
            value=raw
        elif name=="SCIENCE_STOP" and raw in ("submitted","limit_turns_or_tokens",
           "limit_tool_calls","no_tool_use","limit_cost","error"):
            value=raw
        elif name=="SCIENCE_LIMIT_TRIGGER" and raw in LIMITS:
            value=raw
        elif name=="SCIENCE_ERROR_KINDS":
            try:
                x=json.loads(raw)
                if isinstance(x,list) and len(x)<=40 and all(y in ERROR_KINDS for y in x):
                    value=x
            except (ValueError,TypeError):pass
        elif name=="SUMMARY_SHA256" and re.fullmatch("[a-f0-9]{64}",raw):
            value=raw
        elif name in ("SCIENCE_EXCEPTION_CLASS","STOP_CLASS") and re.fullmatch("[A-Za-z_]{1,60}",raw):
            value=raw
        if value is not None:
            allowed[name]=value
    return allowed

def fixtures():
    secret="NO_RAW_GOLD_OR_PROMPT_SHOULD_LEAK_SC045"
    x="\n".join([
     "T045_SCIENCE_STOP=limit_turns_or_tokens",
     "T045_SCIENCE_ERROR_KINDS=[\"tool_limit\",\"tool_error\"]",
     "T045_SCORE_PARAM_INTERVAL_SCORE=0.25",
     "T045_SCIENCE_TOTAL_INPUT_TOKENS=12222",
     "T045_STATUS=SCIENCE_INCOMPLETE",
     "T045_SCIENCE_EXCEPTION_CLASS=ValueError",
     "T045_UNKNOWN="+secret,
     "T045_SCIENCE_STOP="+secret,
     "T045_SCIENCE_ERROR_KINDS=[\""+secret+"\"]",
     "T045_SCORE_TARGET_INTERVAL_SCORE="+secret,
     secret])
    out=classified_lines(x)
    assert out["SCIENCE_STOP"]=="limit_turns_or_tokens"
    assert out["SCIENCE_ERROR_KINDS"]==["tool_limit","tool_error"]
    assert out["SCORE_PARAM_INTERVAL_SCORE"]==.25
    assert out["SCIENCE_TOTAL_INPUT_TOKENS"]==12222
    assert "UNKNOWN" not in out and secret not in json.dumps(out)
    safe_print("OFFLINE_SCIENCE_MONITOR_FIXTURES_PASS",8)
    safe_print("OFFLINE_SCIENCE_MONITOR_PRIVACY_PASS",True)

def run(actor,evaluator,deadline_s):
    before=sample(actor)
    safe_print("SCIENCE_CGROUP_BEFORE",before)
    proc=subprocess.Popen(["docker","start","-a",evaluator],
        stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
    began=time.monotonic()
    records=[]
    reason="FINISHED"
    while proc.poll() is None:
        status=sample(actor)
        records.append(status)
        delta=deltas(before,status)
        if not delta["events_scope_consistent"] or any(delta[k] is None for k in
          ("events_max_delta","events_oom_delta","events_oom_kill_delta","swap_current_bytes_delta")):
            reason="MEMORY_METRICS_UNVERIFIED"
        elif delta["events_oom_kill_delta"]>0:
            reason="OOM_KILL"
        elif delta["events_max_delta"]>0 or delta["events_oom_delta"]>0 or delta["swap_current_bytes_delta"]>0:
            reason="MEMORY_PRESSURE"
        elif time.monotonic()-began>deadline_s:
            reason="SCIENCE_TIMEOUT"
        if reason!="FINISHED":
            subprocess.run(["docker","kill",evaluator],stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,timeout=10,check=False)
            break
        time.sleep(2)
    try:
        output,_=proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        output,_=proc.communicate()
        reason="SCIENCE_TIMEOUT"
    for name,value in classified_lines(output).items():
        safe_print("EVALUATOR_"+name,value)
    after=sample(actor)
    delta=deltas(before,after)
    safe_print("SCIENCE_CGROUP_AFTER",after)
    safe_print("SCIENCE_CGROUP_DELTA",delta)
    safe_print("SCIENCE_CGROUP_SAMPLE_COUNT",len(records))
    safe_print("SCIENCE_MONITOR_ELAPSED_SEC",round(time.monotonic()-began,3))
    safe_print("SCIENCE_MONITOR_REASON",reason)
    safe_print("EVALUATOR_EXIT_CODE",proc.returncode)
    safe_print("SCIENCE_SCORE_CENSORED_BY_MEMORY",reason!="FINISHED")
    return 0

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--offline-test",action="store_true")
    p.add_argument("--actor")
    p.add_argument("--evaluator")
    p.add_argument("--deadline-sec",type=int,default=360)
    args=p.parse_args()
    if args.offline_test:fixtures()
    if args.actor or args.evaluator:
        if not args.actor or not re.fullmatch(r"h0t045-actor-[0-9]+",args.actor):
            p.error("actor must be ephemeral isolated 4B container")
        if not args.evaluator or not re.fullmatch(r"h0t045-evaluator-[0-9]+",args.evaluator):
            p.error("evaluator must be ephemeral private container")
        if not 1<=args.deadline_sec<=360:
            p.error("max science time 360 seconds")
        return run(args.actor,args.evaluator,args.deadline_sec)
    return 0

if __name__=="__main__":
    sys.exit(main())
