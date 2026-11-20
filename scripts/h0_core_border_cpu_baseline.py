#!/usr/bin/env python3
"""T0.19 one optional baseline: CORE train capsule-2011424, adapted binary-wheel CPU environment.

Do not call this an exact environment reproduction or an autonomous agent.
Only static-validated MIT/CC0 capsule files enter a no-network scientific sandbox.
Gold and official scorer are fetched and used only after scientific sandbox exits.
"""
import ast
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tarfile
import time
import urllib.request

CAPSULE = "https://corebench.cs.princeton.edu/capsules/capsule-2011424.tar.gz"
EXPECTED_SHA = "012ff05f9c899452d95e279f1a3e59cffc3b660796645e893b56edf07dc05700"
TRAIN_SHA = "8ea09677fd4d98a4995144b959ba6f65bb2a85aa"
SCORER_SHA = "ecf1d77718c3a7e07bf48c37d7263656b5f7f06f"
COMMIT = "e32a2980e72fe6eb04ee04eb749458f570625663"
IMAGE = "python@sha256:a02e9c5406c416c504d6c9a1a306ff4080c3173f1008d192f953bd20382a2d5c"
REQS = ["numpy==1.26.2", "scipy==1.13.1", "scikit-fuzzy==0.5.0",
        "python-dateutil==2.8.0", "six==1.16.0", "networkx==3.2.1"]
BASE = Path(os.environ["RUNNER_TEMP"]) / "t019-baseline"
CODE, WHEELS, OUT, EVAL = (BASE / part for part in ("work", "wheels", "out", "eval"))
for p in (CODE, WHEELS, OUT, EVAL):
    p.mkdir(parents=True, exist_ok=True)
    p.chmod(0o777 if p in (WHEELS, OUT) else 0o755)


def log(name, value):
    print("T019_" + name + "=" + str(value), flush=True)


def fetch(url, max_bytes):
    with urllib.request.urlopen(urllib.request.Request(url, headers={
        "User-Agent": "ASR-T0.19-once/1"}), timeout=20) as r:
        data = r.read(max_bytes+1)
    if len(data)>max_bytes:
        raise ValueError("source size exceeded")
    return data


def gitblob(b):
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()


def step(label, args, limit):
    t=time.monotonic()
    try:
        out=subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           text=True, timeout=limit, check=False)
    except subprocess.TimeoutExpired:
        log(label+"_TIMEOUT",True)
        raise RuntimeError(label+"_timeout")
    log(label+"_WALL_SEC",round(time.monotonic()-t,3))
    # Only a strict controller-generated allowlist, no raw third-party output.
    for line in out.stdout.splitlines():
        if line.startswith("T019_"):
            log("CHILD_MARKER",line[:240])
    log(label+"_EXIT",out.returncode)
    if out.returncode:
        raise RuntimeError(label+"_exit_nonzero")
    return out


def mnt(p,dst,r=True):
    return ["--mount","type=bind,src="+str(p)+",dst="+dst+(",readonly" if r else "")]


def docker_spec(name, volumes, network="none", memory="3g"):
    return ["docker","run","--rm","--name",name,"--network",network,
            "--read-only","--cap-drop=ALL","--security-opt=no-new-privileges",
            "--pids-limit=96","--cpus=2","--memory="+memory,
            "--user=65534:65534",
            "--tmpfs","/tmp:rw,nosuid,nodev,size=768m,mode=1777",
            "--env","PYTHONDONTWRITEBYTECODE=1",
            "--env","OPENBLAS_NUM_THREADS=1",
            "--env","OMP_NUM_THREADS=1",
            *volumes,IMAGE]


def write_text(path,body):
    path.write_text(body,encoding="utf8")
    path.chmod(0o644)


def main():
    log("BASELINE_SCOPE","one_adapted_CPU_run_zero_LLM")
    log("ENVIRONMENT_DRIFT","Python3.9_numpy1.26_scikitfuzzy0.5_not_original_py3.7_numpy1.16_scfuzzy0.4.1")
    raw=fetch(CAPSULE,1_000_000)
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:
        raise ValueError("capsule SHA changed")
    log("CAPSULE_SHA_MATCH",True)
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as tf:
        members=tf.getmembers()
        if len(members)!=36 or sum(m.size for m in members if m.isfile())>5_000_000:
            raise ValueError("unexpected archive size")
        for m in members:
            p=PurePosixPath(m.name)
            if p.is_absolute() or ".." in p.parts or m.issym() or m.islnk() or m.isdev():
                raise ValueError("unsafe tar member")
        licenses=[m for m in members if m.isfile() and PurePosixPath(m.name).name=="LICENSE"]
        license_text=[tf.extractfile(m).read().decode("utf-8","replace").lower() for m in licenses]
        if len(licenses)!=2 or not any("mit license" in s for s in license_text) or not any("cc0 1.0 universal" in s for s in license_text):
            raise ValueError("license gate failed")
        log("LICENSE_GATE","MIT_and_CC0")
        script_candidates=[m for m in members if m.isfile() and m.name.endswith("/algorithms/border_tgraank.py")]
        if len(script_candidates)!=1 or script_candidates[0].size!=17876:
            raise ValueError("target script gate failed")
        origin=PurePosixPath(script_candidates[0].name)
        # Parent of Code Ocean's /code directory, so sibling /data is retained.
        if "code" in origin.parts:
            prefix=origin.parts[:origin.parts.index("code")]
        else:
            prefix=origin.parts[:-2]
        for m in members:
            if not m.isfile():continue
            p=PurePosixPath(m.name)
            if p.parts[:len(prefix)]!=prefix:continue
            relative=Path(*p.parts[len(prefix):])
            dest=CODE/relative
            if not str(dest.resolve()).startswith(str(CODE.resolve())+os.sep):
                raise ValueError("archive escape")
            dest.parent.mkdir(parents=True,exist_ok=True)
            if m.size>3_000_000:raise ValueError("large member")
            dest.write_bytes(tf.extractfile(m).read())
            dest.chmod(0o644)
        rel=Path(*origin.parts[len(prefix):])
        script=CODE/rel
        if not script.is_file():raise ValueError("script not staged")
        code=script.read_bytes()
        if hashlib.sha256(code).hexdigest()!="c2819e5914693614800c2e8bf88ec011237ef59813776ed206d1833058c402ec":
            raise ValueError("target hash changed")
        ast.parse(code.decode("utf8-sig"))
        log("TARGET_SHA_MATCH",True)
    # Original task says just Run algorithms/border_tgraank.py, with no user CLI flags.
    if rel.parts[-2:]!=("algorithms","border_tgraank.py"):
        raise ValueError("target relative location mismatch")
    log("RELATIVE_SCRIPT",str(rel))
    # Pin the base image to the tested digest. No build of original Dockerfile.
    step("IMAGE_PULL",["docker","pull",IMAGE],120)
    wheel_name="t019-wheels-"+os.getenv("GITHUB_RUN_ID","local")
    cmd=docker_spec(wheel_name,mnt(WHEELS,"/wheels",False),network="bridge",memory="2g")+[
        "python","-m","pip","download","--only-binary=:all:","--no-deps",
        "--disable-pip-version-check","-d","/wheels",*REQS]
    try: step("WHEEL_DOWNLOAD",cmd,120)
    finally:subprocess.run(["docker","rm","-f",wheel_name],capture_output=True)
    wheels=sorted(WHEELS.glob("*.whl"))
    if len(wheels)!=len(REQS):
        raise RuntimeError("binary-only dependency gate rejected packages")
    for w in wheels:
        log("WHEEL_SHA256",w.name+","+hashlib.sha256(w.read_bytes()).hexdigest())
    # Trusted wrapper runs target without passing scorer or gold; raw stdout/stderr not logged.
    runner='''import os,subprocess,re,json,time,resource
t=time.monotonic()
print("T019_BEFORE_IMPORTS=true",flush=True)
target=os.environ["CAPSULE_SCRIPT"]
cwd=os.environ["CAPSULE_CWD"]
try:
    p=subprocess.run(["python",target],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                     text=True,timeout=200,check=False)
except subprocess.TimeoutExpired:
    print("T019_SCRIPT_TIMEOUT=true",flush=True);raise SystemExit(124)
print("T019_SCIENTIFIC_PROCESS_EXIT="+str(p.returncode),flush=True)
if p.returncode:
    for name in ("ModuleNotFoundError","ImportError","FileNotFoundError","TypeError",
                 "ValueError","SyntaxError","AttributeError","RuntimeError","IndexError"):
        if name in p.stderr:
            print("T019_SCIENTIFIC_ERROR_CLASS="+name,flush=True);break
    raise SystemExit(2)
matches=re.findall(r"(?i)total\\s*:?\\s*(\\d+)\\s*ftgeps?\\s*found",p.stdout)
print("T019_OUTPUT_PATTERN_COUNT="+str(len(matches)),flush=True)
if len(matches)!=1:
    raise SystemExit(3)
value=int(matches[0])
with open("/out/report.json","w") as f:
    json.dump({"Report the number of FtGEPs found.":value},f)
with open("/out/resources.json","w") as f:
    json.dump({"wall_sec":round(time.monotonic()-t,3),
               "child_maxrss_kib":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "model_calls":0},f)
print("T019_REPORT_WRITTEN=true",flush=True)
'''
    launch=CODE/"runner_once.py"
    write_text(launch,runner)
    script_in="/work/"+str(rel)
    cwd_in="/work/"+str(rel.parent.parent)
    name="t019-science-"+os.getenv("GITHUB_RUN_ID","local")
    deps=" ".join(REQS)
    cmd=docker_spec(name,mnt(CODE,"/work")+mnt(WHEELS,"/wheels")+mnt(OUT,"/out",False))+[
        "sh","-c","python -m pip install --no-index --no-deps --find-links=/wheels --target=/tmp/site "+
        deps+" >/tmp/pip.log 2>&1; rc=$?; if [ $rc -ne 0 ]; then echo T019_INSTALL_EXIT=$rc; exit $rc; fi; "+
        "echo T019_INSTALL_PASS=true; "+
        "CAPSULE_SCRIPT='"+script_in+"' CAPSULE_CWD='"+cwd_in+"' PYTHONPATH=/tmp/site "+
        "python /work/runner_once.py; rc=$?; echo T019_RUNNER_EXIT=$rc; exit $rc"
    ]
    try:step("SCIENCE",cmd,240)
    finally:subprocess.run(["docker","rm","-f",name],capture_output=True)
    if not (OUT/"report.json").is_file() or not (OUT/"resources.json").is_file():
        raise RuntimeError("missing report")
    log("REPORT_SHA256",hashlib.sha256((OUT/"report.json").read_bytes()).hexdigest())
    res=json.loads((OUT/"resources.json").read_text())
    log("SCRIPT_WALL_SEC",res["wall_sec"])
    log("SCRIPT_CHILD_MAXRSS_KIB",res["child_maxrss_kib"])
    # Gold is not fetched or mounted until after scientific container is removed.
    base="https://raw.githubusercontent.com/siegelz/core-bench/"+COMMIT+"/benchmark/"
    train=fetch(base+"dataset/core_train.json",100000)
    scorer=fetch(base+"evaluations.py",50000)
    if gitblob(train)!=TRAIN_SHA or gitblob(scorer)!=SCORER_SHA:
        raise RuntimeError("eval source Git blob checksum mismatch")
    (EVAL/"train.json").write_bytes(train)
    (EVAL/"scorer.py").write_bytes(scorer)
    score_code='''import ast,json,math
import numpy as np
from scipy.stats import t
from pathlib import Path
src=ast.parse(Path("/eval/scorer.py").read_text())
f=next(n for n in src.body if isinstance(n,ast.FunctionDef) and n.name=="eval_result_json")
module=ast.fix_missing_locations(ast.Module(body=[f],type_ignores=[]))
scope={"Dict":dict,"np":np,"t":t,"math":math}
exec(compile(module,"CORE_original_eval_result_json","exec"),scope,scope)
task=next(x for x in json.loads(Path("/eval/train.json").read_text()) if x["capsule_id"]=="capsule-2011424")
result=json.loads(Path("/out/report.json").read_text())
if list(result)!=["Report the number of FtGEPs found."]:raise RuntimeError("unexpected report")
score=scope["eval_result_json"](task["results"],result)
print("T019_ORIGINAL_CORE_CORRECT="+str(score["correct_written_answers"]),flush=True)
print("T019_ORIGINAL_CORE_TOTAL="+str(score["total_written_questions"]),flush=True)
print("T019_GOLD_ISOLATED_POSTPROCESS=true",flush=True)
'''
    write_text(EVAL/"score_once.py",score_code)
    name="t019-score-"+os.getenv("GITHUB_RUN_ID","local")
    cmd=docker_spec(name,mnt(EVAL,"/eval")+mnt(OUT,"/out")+mnt(WHEELS,"/wheels"),memory="2g")+[
        "sh","-c",
        "python -m pip install --no-index --no-deps --find-links=/wheels --target=/tmp/site "+
        "numpy==1.26.2 scipy==1.13.1 >/tmp/pip.log 2>&1; rc=$?; "+
        "if [ $rc -ne 0 ]; then echo T019_SCORER_INSTALL_EXIT=$rc; exit $rc; fi; "+
        "PYTHONPATH=/tmp/site python /eval/score_once.py"
    ]
    try:step("EVALUATOR",cmd,80)
    finally:subprocess.run(["docker","rm","-f",name],capture_output=True)
    log("BASAL_SCORER_COMPLETE",True)
    log("NO_LLM_PAID_API_OR_GPU",True)


if __name__=="__main__":
    try: main()
    except Exception as e:
        log("STOP_REASON_TYPE",type(e).__name__)
        # Do not publish unreviewed exception messages or source values.
        log("STATUS","BLOCKED_OR_UNSCORED")
        sys.exit(1)
