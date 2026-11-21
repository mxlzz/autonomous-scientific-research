#!/usr/bin/env python3
"""T0.52: allowlisted Linux cgroup v2 telemetry for one synthetic Qwen4B probe.

No raw model output, free-text errors, private files, prompts or gold are printed.
"""
import argparse
import json
import re
import subprocess
import sys
import time

ROOT="/sys/fs/cgroup/"
EVENT_KEYS=("max","oom","oom_kill")
STAT_KEYS=("anon","file","kernel")
MODEL_OUTPUT_KEYS=frozenset((
    "PINNED_RUNTIME_GATE","INFERENCE_REQUEST_COUNT","TOOL_COUNT","TOOL_NAMES",
    "ARGUMENT_KINDS","FINISH_REASON","PROMPT_TOKENS","COMPLETION_TOKENS",
    "REASONING_CONTENT_PRESENT","PROBE_PASS","ELAPSED_SECONDS",
    "DECISION","TRANSPORT_ERROR_CLASS"
))

def number(text, max_allowed=False):
    if text is None:
        return None
    x=text.strip()
    if max_allowed and x=="max":
        return "max"
    if not re.fullmatch(r"[0-9]{1,20}",x):
        return None
    val=int(x)
    return val if 0 <= val <= 10**15 else None

def pairs(text, keys):
    out={k:None for k in keys}
    seen=set()
    if not isinstance(text,str):
        return out
    for line in text.splitlines():
        parts=line.split()
        if len(parts)!=2 or parts[0] not in out:
            continue
        key=parts[0]
        if key in seen:
            out[key]=None
        else:
            out[key]=number(parts[1])
        seen.add(key)
    return out

def pressure(text):
    out={"some":None,"full":None}
    if not isinstance(text,str):
        return out
    for line in text.splitlines():
        head=line.split(" ",1)
        if len(head)!=2 or head[0] not in out:
            continue
        m=re.search(r"(?:^|\s)total=([0-9]+)(?:\s|$)",head[1])
        out[head[0]]=number(m.group(1)) if m else None
    return out

def snapshot_from_text(source):
    # Controlled file set; none of this content is printed directly.
    events=source.get("memory.events.local")
    scope="local"
    if events is None:
        events=source.get("memory.events")
        scope="hierarchical" if events is not None else "unverified"
    stat=pairs(source.get("memory.stat"),STAT_KEYS)
    e=pairs(events,EVENT_KEYS)
    p=pressure(source.get("memory.pressure"))
    return {
        "memory_current_bytes":number(source.get("memory.current")),
        "memory_peak_bytes":number(source.get("memory.peak")),
        "memory_max_bytes":number(source.get("memory.max"),True),
        "events_scope":scope,
        "events_max":e["max"],"events_oom":e["oom"],"events_oom_kill":e["oom_kill"],
        "stat_anon_bytes":stat["anon"],"stat_file_bytes":stat["file"],
        "stat_kernel_bytes":stat["kernel"],
        "swap_current_bytes":number(source.get("memory.swap.current")),
        "swap_max_bytes":number(source.get("memory.swap.max"),True),
        "psi_some_total_us":p["some"],"psi_full_total_us":p["full"]
    }

def read_file(container, filename):
    proc=subprocess.run(["docker","exec",container,"cat",ROOT+filename],
                       stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                       text=True,timeout=3,check=False)
    if proc.returncode!=0 or len(proc.stdout)>25000:
        return None
    return proc.stdout

def sample(container):
    names=("memory.current","memory.peak","memory.max","memory.events.local",
           "memory.stat","memory.swap.current","memory.swap.max","memory.pressure")
    raw={}
    for name in names:
        try:raw[name]=read_file(container,name)
        except (subprocess.TimeoutExpired,OSError):
            raw[name]=None
    if raw["memory.events.local"] is None:
        try:raw["memory.events"]=read_file(container,"memory.events")
        except (subprocess.TimeoutExpired,OSError):raw["memory.events"]=None
    return snapshot_from_text(raw)

def safe_print(marker,value):
    print("T052_"+marker+"="+json.dumps(value,separators=(",",":"),sort_keys=True),flush=True)

def deltas(before,after):
    out={}
    for key in ("events_max","events_oom","events_oom_kill","swap_current_bytes"):
        a,b=before.get(key),after.get(key)
        out[key+"_delta"]=(b-a if type(a) is int and type(b) is int and b>=a else None)
    out["events_scope_consistent"]=(before.get("events_scope")==after.get("events_scope") and
                                    before.get("events_scope")!="unverified")
    return out

def tests():
    sentinel="PRIVATE_GOLD_MODEL_RAW_TXT_NEVER_LEAK_ZK13"
    src={"memory.current":"100","memory.peak":"120",
         "memory.max":"5368709120","memory.events.local":"max 2\noom 1\noom_kill 0",
         "memory.stat":"anon 70\nfile 25\nkernel 5\nsensitive "+sentinel,
         "memory.swap.current":"0","memory.swap.max":"max",
         "memory.pressure":"some avg10=0.00 avg60=0.00 total=55\nfull avg10=0.00 total=0"}
    out=snapshot_from_text(src)
    assert out["memory_peak_bytes"]==120 and out["memory_max_bytes"]==5368709120
    assert out["events_max"]==2 and out["events_oom"]==1 and out["events_oom_kill"]==0
    assert out["stat_anon_bytes"]==70 and out["stat_file_bytes"]==25
    assert out["psi_some_total_us"]==55 and out["swap_max_bytes"]=="max"
    assert sentinel not in json.dumps(out)
    b={**src,"memory.events.local":"max 3\noom 1\noom_kill 0","memory.swap.current":"4"}
    delta=deltas(out,snapshot_from_text(b))
    assert delta["events_max_delta"]==1 and delta["swap_current_bytes_delta"]==4
    assert delta["events_oom_delta"]==0 and delta["events_scope_consistent"] is True
    missing=snapshot_from_text({"memory.events":"max 5\noom 0\noom_kill 0"})
    assert missing["events_scope"]=="hierarchical" and missing["stat_anon_bytes"] is None
    invalid=snapshot_from_text({"memory.current":sentinel,"memory.max":"-1",
                                "memory.events.local":"max -2\noom xyz\noom_kill 5",
                                "memory.stat":"anon 1\nanon 2\nfile "+sentinel})
    assert invalid["memory_current_bytes"] is None and invalid["memory_max_bytes"] is None
    assert invalid["events_max"] is None and invalid["events_oom_kill"]==5
    assert invalid["stat_anon_bytes"] is None and invalid["stat_file_bytes"] is None
    assert sentinel not in json.dumps(invalid)
    assert number("True") is None and number("1.5") is None and number("max") is None
    assert number("max",True)=="max"
    assert pressure("some garbage").get("some") is None
    empty=snapshot_from_text({})
    assert empty["events_scope"]=="unverified" and empty["memory_current_bytes"] is None
    uncapped=snapshot_from_text({"memory.max":"max"})
    assert uncapped["memory_max_bytes"]=="max"
    zero_events=snapshot_from_text({"memory.events.local":"max 0\noom 0\noom_kill 0"})
    assert zero_events["events_max"]==0 and zero_events["events_oom"]==0
    duplicate=snapshot_from_text({"memory.events.local":"max 1\nmax 2\noom 0\noom_kill 0"})
    assert duplicate["events_max"] is None
    stat_only=snapshot_from_text({"memory.stat":"anon 3\nfile 2\nkernel 1"})
    assert stat_only["stat_anon_bytes"]==3 and stat_only["stat_file_bytes"]==2
    psi_only=snapshot_from_text({"memory.pressure":"some avg10=0.00 total=23\nfull avg10=0.00 total=0"})
    assert psi_only["psi_some_total_us"]==23 and psi_only["psi_full_total_us"]==0
    back=deltas(out,snapshot_from_text({**src,"memory.events.local":"max 1\noom 0\noom_kill 0"}))
    assert back["events_max_delta"] is None
    print("T052_OFFLINE_CGROUP_FIXTURES_PASS=15",flush=True)
    print("T052_OFFLINE_PRIVATE_LEAK_CHECK=true",flush=True)

def monitor(container):
    before=sample(container)
    safe_print("CGROUP_BEFORE_REQUEST",before)
    cmd=[sys.executable,"scripts/h0_qwen4b_tool_probe_t041.py","--run-one"]
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                          text=True)
    records=[]
    deadline=time.monotonic()+105
    timed_out=False
    while proc.poll() is None:
        records.append(sample(container))
        if time.monotonic()>=deadline:
            timed_out=True
            proc.kill()
            break
        time.sleep(1.5)
    stdout,_=proc.communicate(timeout=10)
    for line in stdout.splitlines():
        match=re.fullmatch(r"T041_([A-Z_]+)=(.{1,256})",line)
        if match and match.group(1) in MODEL_OUTPUT_KEYS:
            # Existing probe generates only author-controlled allowlisted values.
            # Drop any unexpected strings/characters to ensure no raw leakage.
            if re.fullmatch(r"[A-Za-z0-9_.,\[\]\" :+-]+",match.group(2)):
                print("T052_PROBE_"+match.group(1)+"="+match.group(2),flush=True)
    after=sample(container)
    safe_print("CGROUP_AFTER_REQUEST",after)
    d=deltas(before,after)
    safe_print("EVENTS_AND_SWAP_DELTA",d)
    currents=[s["memory_current_bytes"] for s in [before,*records,after]
              if type(s["memory_current_bytes"]) is int]
    safe_print("SAMPLED_CURRENT_MAX_BYTES",max(currents) if currents else None)
    safe_print("CGROUP_SAMPLE_COUNT",len(records))
    safe_print("PROBE_EXIT_CODE",proc.returncode)
    safe_print("PROBE_MONITOR_TIMEOUT",timed_out)
    good=(d["events_scope_consistent"] and all(d[k] is not None for k in
         ("events_max_delta","events_oom_delta","events_oom_kill_delta"))
          and type(after["memory_max_bytes"]) is int)
    safe_print("MEMORY_OBSERVABILITY_VERIFIED",good)
    pressure=(d["events_max_delta"] or 0)>0 or (d["events_oom_delta"] or 0)>0 or (
        d["swap_current_bytes_delta"] is not None and d["swap_current_bytes_delta"]>0)
    if d["events_oom_kill_delta"] is not None and d["events_oom_kill_delta"]>0:
        result="NO_GO_OOM_KILL"
    elif timed_out or proc.returncode!=0:
        result="NO_GO_PROBE_OR_TIMEOUT"
    elif not good:
        result="NO_GO_MEM_METRICS_UNVERIFIED"
    elif pressure:
        result="MEMORY_PRESSURE_DIAGNOSTIC_REQUIRED"
    else:
        result="ONLY_SHORT_PROBE_PASS_LONG_SCIENCE_UNVERIFIED"
    safe_print("MEMORY_DECISION",result)
    return 0

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--offline-test",action="store_true")
    p.add_argument("--snapshot-stage",choices=("before_pull","after_pull"))
    p.add_argument("--monitor",action="store_true")
    p.add_argument("--container")
    a=p.parse_args()
    if a.offline_test:tests()
    if a.snapshot_stage or a.monitor:
        if not a.container or not re.fullmatch(r"h0t052-prep-[0-9]+",a.container):
            p.error("expected isolated T0.52 prep name")
        if a.snapshot_stage:safe_print("CGROUP_"+a.snapshot_stage.upper(),sample(a.container))
        elif a.monitor:return monitor(a.container)
    return 0

if __name__=="__main__":
    sys.exit(main())
