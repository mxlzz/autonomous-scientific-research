#!/usr/bin/env python3
"""T0.47: memory abort + live private-safe stream of SciResearch evaluator progress.

Never forward raw model/evaluator stdout. Reader threads only queue allowlisted metrics.
"""
from __future__ import annotations
import argparse
import json
import queue
import re
import subprocess
import threading
import time
from h0_cgroup_pressure_t045 import sample, deltas
from h0_heartbeat_censor_t046 import classify_heartbeat, censor_reason

STATS={"SCIENCE_TURNS","SCIENCE_TOOL_CALLS","SCIENCE_TOOL_ERRORS",
 "SCIENCE_PROMPT_TOKENS","SCIENCE_CACHE_READ_TOKENS","SCIENCE_CACHE_WRITE_TOKENS",
 "SCIENCE_TOTAL_INPUT_TOKENS","SCIENCE_MAX_TURNS","SCIENCE_MAX_TOOL_CALLS",
 "SCIENCE_COMPLETION_TOKENS","MODEL_CALLS","WALL_SEC"}
BOOLS={"SOURCE_PINS_AND_HARNESS_GUARD","PREP_PROBE_GATE_VERIFIED",
 "SCIENCE_SUBMITTED","SCIENCE_GRADE_OBSERVED","PROBE_PASS",
 "ACTOR_HAS_EVALUATOR_MOUNT","GUARD_INTEGRATED_IN_LOADED_COPY",
 "HEARTBEAT_INTEGRATED_IN_LOADED_COPY","SUMMARY_WRITTEN"}
STATES={"STARTED","SCIENCE_STARTED","NO_GO_CONTROLLER","NO_GO_PREP_GATE_NOT_VERIFIED",
 "SCIENCE_EXCEPTION","SCIENCE_INCOMPLETE","SCORED","NO_SCORE","NOT_STARTED",
 "ERROR","NO_GO_EPISODE_SKIPPED","SKIPPED"}
STOPS={"submitted","limit_turns_or_tokens","limit_tool_calls","no_tool_use",
 "limit_cost","error"}
ERROR_KINDS={"final_turn_non_submit","tool_limit","invalid_arguments","tool_error","other"}

def safe_print(name,value):
    assert re.fullmatch("[A-Z_]{1,80}",name)
    print("T047_"+name+"="+json.dumps(value,separators=(",",":"),sort_keys=True),flush=True)

def classify_result_line(line):
    m=re.fullmatch(r"T047_([A-Z0-9_]+)=(.{1,3000})",line)
    if not m:
        return None
    name,raw=m.group(1),m.group(2)
    value=None
    if name in STATS:
        try:
            n=float(raw)
            if 0<=n<=1e9 and n==n and n not in (float("inf"),float("-inf")):
                value=n
        except ValueError:pass
    elif name.startswith("SCORE_") and re.fullmatch("SCORE_[A-Z0-9_]{1,75}",name):
        try:
            n=float(raw)
            if abs(n)<=1e9 and n==n and n not in (float("inf"),float("-inf")):
                value=n
        except ValueError:pass
    elif name in BOOLS and raw in ("True","False"):
        value=(raw=="True")
    elif name in ("STATUS","SCIENCE_STATUS") and raw in STATES:
        value=raw
    elif name=="SCIENCE_STOP" and raw in STOPS:
        value=raw
    elif name=="SCIENCE_LIMIT_TRIGGER" and raw in ("turns_only","tokens_only","both","None"):
        value=raw
    elif name=="SCIENCE_ERROR_KINDS":
        try:
            arr=json.loads(raw)
            if isinstance(arr,list) and len(arr)<=40 and all(type(x) is str and x in ERROR_KINDS for x in arr):
                value=arr
        except (ValueError,TypeError):pass
    elif name=="SUMMARY_SHA256" and re.fullmatch("[a-f0-9]{64}",raw):
        value=raw
    elif name in ("SCIENCE_EXCEPTION_CLASS","STOP_CLASS") and re.fullmatch("[A-Za-z_]{1,60}",raw):
        value=raw
    if value is None:
        return None
    return {name:value}

def classify_stream_line(line):
    line=line.rstrip("\r\n")
    heartbeat=classify_heartbeat(line)
    if heartbeat is not None:
        return "HEARTBEAT",heartbeat
    result=classify_result_line(line)
    if result is not None:
        return "EVALUATOR",result
    return None

def stream_thread(pipe,events,statistics):
    try:
        for line in pipe:
            classified=classify_stream_line(line)
            if classified is None:
                statistics["rejected_lines"]+=1
                continue
            try:
                events.put_nowait(classified)
            except queue.Full:
                statistics["dropped_allowlisted"]+=1
    finally:
        pipe.close()

def flush_events(q,last):
    count=0
    while True:
        try:kind,record=q.get_nowait()
        except queue.Empty:break
        if kind=="HEARTBEAT":
            last.update(record)
        safe_print("STREAM_"+kind,record)
        count+=1
    return count

def fixtures():
    secret="T047_RAW_PRIVATE_DONT_PRINT_ARG_SECRET"
    items=[
     "T047_HEARTBEAT_REQUEST_START_TURN=1",
     "T047_HEARTBEAT_REQUEST_END_SECONDS=90.125",
     "T047_HEARTBEAT_TOOL_START_COUNT=2",
     "T047_HEARTBEAT_SCORER_SUBMITTED=false",
     "T047_SCIENCE_TOTAL_INPUT_TOKENS=1000",
     "T047_SCIENCE_TOOL_CALLS=5",
     "T047_SCIENCE_STOP=limit_turns_or_tokens",
     "T047_SCIENCE_ERROR_KINDS=[\"invalid_arguments\"]",
     "T047_SUMMARY_SHA256="+"a"*64,
     "T047_SCORE_PARAM_INTERVAL_SCORE=0.25"
    ]
    result=[classify_stream_line(x) for x in items]
    assert all(x is not None for x in result)
    assert result[0][0]=="HEARTBEAT" and result[-1][0]=="EVALUATOR"
    malformed=[
     "T047_HEARTBEAT_PROGRESS="+json.dumps({"turns":1,"prompt":secret}),
     "T047_HEARTBEAT_TOOL_START_COUNT="+secret,
     "T047_SCIENCE_STOP="+secret,
     "T047_SCIENCE_TOOL_CALLS="+secret,
     "T047_SCIENCE_ERROR_KINDS=[\""+secret+"\"]",
     "T047_SCORE_PARAM_INTERVAL_SCORE=nan",
     "T047_SCORE_PARAM_INTERVAL_SCORE="+secret,
     "T047_SUMMARY_SHA256="+secret,
     "T047_MODEL_RAW="+secret,secret
    ]
    for line in malformed:
        assert classify_stream_line(line) is None,line
    assert secret not in json.dumps(result)
    for cause,result in (("SCIENCE_TIMEOUT","CENSORED_TIMEOUT"),
                         ("MEMORY_PRESSURE","CENSORED_MEMORY"),
                         ("OOM_KILL","CENSORED_MEMORY"),
                         ("MEMORY_METRICS_UNVERIFIED","CENSORED_UNVERIFIED"),
                         ("FINISHED","COMPLETED"),
                         ("unknown","CENSORED_CONTROLLER")):
        assert censor_reason(cause)==result
    assert censor_reason("SCIENCE_TIMEOUT")!="CENSORED_MEMORY"
    safe_print("OFFLINE_STREAM_VALID_FIXTURES_PASS",len(items))
    safe_print("OFFLINE_STREAM_REJECTED_FIXTURES_PASS",len(malformed))
    safe_print("OFFLINE_CENSOR_CLASSES_PASS",7)
    safe_print("OFFLINE_PRIVATE_STRING_LEAK",False)

def run(actor,evaluator,limit):
    before=sample(actor)
    safe_print("SCIENCE_CGROUP_BEFORE",before)
    proc=subprocess.Popen(["docker","start","-a",evaluator],stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL,text=True,bufsize=1)
    q=queue.Queue(maxsize=512)
    stats={"rejected_lines":0,"dropped_allowlisted":0}
    reader=threading.Thread(target=stream_thread,args=(proc.stdout,q,stats),daemon=True)
    reader.start()
    began=time.monotonic()
    reason="FINISHED"
    n=0
    last={}
    while proc.poll() is None:
        n+=1
        flush_events(q,last)
        stat=sample(actor)
        delta=deltas(before,stat)
        if not delta["events_scope_consistent"] or any(delta[k] is None for k in
           ("events_max_delta","events_oom_delta","events_oom_kill_delta","swap_current_bytes_delta")):
            reason="MEMORY_METRICS_UNVERIFIED"
        elif delta["events_oom_kill_delta"]>0:
            reason="OOM_KILL"
        elif delta["events_max_delta"]>0 or delta["events_oom_delta"]>0 or delta["swap_current_bytes_delta"]>0:
            reason="MEMORY_PRESSURE"
        elif time.monotonic()-began>limit:
            reason="SCIENCE_TIMEOUT"
        if reason!="FINISHED":
            subprocess.run(["docker","kill",evaluator],stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,timeout=10,check=False)
            break
        time.sleep(2)
    try:proc.wait(timeout=12)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)
        reason="SCIENCE_TIMEOUT"
    reader.join(timeout=6)
    flush_events(q,last)
    after=sample(actor)
    safe_print("SCIENCE_CGROUP_AFTER",after)
    safe_print("SCIENCE_CGROUP_DELTA",deltas(before,after))
    safe_print("SCIENCE_CGROUP_SAMPLE_COUNT",n)
    safe_print("SCIENCE_MONITOR_ELAPSED_SEC",round(time.monotonic()-began,3))
    if reason=="FINISHED" and proc.returncode!=0:
        reason="CONTROLLER_EXIT_ERROR"
    classified=censor_reason(reason)
    safe_print("SCIENCE_MONITOR_REASON",reason)
    safe_print("SCIENCE_CENSOR_CLASS",classified)
    safe_print("SCIENCE_SCORE_CENSORED_BY_MEMORY",classified=="CENSORED_MEMORY")
    safe_print("SCIENCE_SCORE_CENSORED_BY_TIMEOUT",classified=="CENSORED_TIMEOUT")
    safe_print("EVALUATOR_EXIT_CODE",proc.returncode)
    safe_print("LAST_ALLOWLIST_HEARTBEAT",last)
    safe_print("REJECTED_RAW_STDOUT_LINE_COUNT",stats["rejected_lines"])
    safe_print("DROPPED_ALLOWLISTED_EVENT_COUNT",stats["dropped_allowlisted"])
    safe_print("STDOUT_READER_DRAINED",not reader.is_alive())
    return 0

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--offline-test",action="store_true")
    p.add_argument("--actor")
    p.add_argument("--evaluator")
    p.add_argument("--deadline-sec",type=int,default=600)
    a=p.parse_args()
    if a.offline_test:fixtures()
    if a.actor or a.evaluator:
        if not a.actor or not re.fullmatch(r"h0t047-actor-[0-9]+",a.actor):
            p.error("actor identifier mismatch")
        if not a.evaluator or not re.fullmatch(r"h0t047-evaluator-[0-9]+",a.evaluator):
            p.error("evaluator identifier mismatch")
        if not 1<=a.deadline_sec<=600:
            p.error("science deadline exceeds prereg cap600")
        return run(a.actor,a.evaluator,a.deadline_sec)
    return 0

if __name__=="__main__":
    main()
