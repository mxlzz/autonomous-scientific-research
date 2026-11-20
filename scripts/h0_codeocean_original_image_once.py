#!/usr/bin/env python3
"""T0.20: one frozen Code Ocean image attempt with strict sandbox and original CORE scorer.

No Dockerfile build, no adaptation of published scientific dependencies, no LLM.
Only the original capsule and its published preserved Code Ocean image are used.
The answer key/scorer are downloaded only after the scientific container exits.
"""
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request

CAPSULE_URL="https://corebench.cs.princeton.edu/capsules/capsule-2011424.tar.gz"
CAPSULE_SHA="012ff05f9c899452d95e279f1a3e59cffc3b660796645e893b56edf07dc05700"
IMAGE="registry.codeocean.com/published/31650577-0a26-4f81-974b-6c5912a14301:v1"
CORE_COMMIT="e32a2980e72fe6eb04ee04eb749458f570625663"
TRAIN_BLOB="8ea09677fd4d98a4995144b959ba6f65bb2a85aa"
SCORER_BLOB="ecf1d77718c3a7e07bf48c37d7263656b5f7f06f"
ROOT=Path(os.environ["RUNNER_TEMP"])/"asr-t020-preserved"
CODE,DATA,RESULTS=(ROOT/n for n in ("code","data","results"))
for d in (CODE,DATA,RESULTS):
    d.mkdir(parents=True,exist_ok=True)
    d.chmod(0o777 if d==RESULTS else 0o755)

def mark(k,v):
    print("T020_"+k+"="+str(v),flush=True)

def fetch(url,max_bytes):
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"ASR-T0.20-one-science/1"}),timeout=20) as r:
        body=r.read(max_bytes+1)
    if len(body)>max_bytes:raise ValueError("source_size_cap")
    return body

def gitblob(body):
    return hashlib.sha1(b"blob "+str(len(body)).encode()+b"\0"+body).hexdigest()

def cmd(label,args,limit=120):
    start=time.monotonic()
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=limit,check=False)
    except subprocess.TimeoutExpired:
        mark(label+"_TIMEOUT",True)
        raise RuntimeError(label+"_timeout")
    mark(label+"_WALL_SEC",round(time.monotonic()-start,3))
    mark(label+"_EXIT",p.returncode)
    if p.returncode:raise RuntimeError(label+"_exit"+str(p.returncode))
    return p.stdout

def mount(src,dst,readonly=True):
    return ["--mount","type=bind,src="+str(src)+",dst="+dst+(",readonly" if readonly else "")]

def main():
    mark("TASK","CORE_train_capsule-2011424")
    mark("BUDGET","CPU2_RAM3GiB_PIDs96_SCIENCE240sec")
    mark("NO_GOLD_AND_NO_SECRETS_IN_SCIENCE",True)
    mark("SOURCE_DEPENDENCIES","original_published_preserved_image_no_rebuild")
    raw=fetch(CAPSULE_URL,1_000_000)
    if hashlib.sha256(raw).hexdigest()!=CAPSULE_SHA:raise ValueError("capsule_hash_mismatch")
    mark("ARCHIVE_SHA256_MATCH",True)
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as tar:
        ms=tar.getmembers()
        if len(ms)!=36 or sum(m.size for m in ms if m.isfile())>5_000_000:
            raise ValueError("archive_member_gate")
        for m in ms:
            p=PurePosixPath(m.name)
            if m.issym() or m.islnk() or m.isdev() or p.is_absolute() or ".." in p.parts:
                raise ValueError("archive_unsafe_member")
        files=[m for m in ms if m.isfile()]
        target=[m for m in files if m.name.endswith("/code/algorithms/border_tgraank.py")]
        if len(target)!=1 or hashlib.sha256(tar.extractfile(target[0]).read()).hexdigest()!="c2819e5914693614800c2e8bf88ec011237ef59813776ed206d1833058c402ec":
            raise ValueError("target_script_gate")
        licenses=[m for m in files if PurePosixPath(m.name).name=="LICENSE"]
        ltext=[tar.extractfile(m).read().decode("utf-8","replace").lower() for m in licenses]
        if len(licenses)!=2 or not any("mit license" in x for x in ltext) or not any("cc0 1.0 universal" in x for x in ltext):
            raise ValueError("license_markers_not_found")
        docs=[m for m in files if PurePosixPath(m.name).name=="REPRODUCING.md"]
        if len(docs)!=1:raise ValueError("reproduction_instructions_missing")
        doc=tar.extractfile(docs[0]).read().decode("utf-8","replace")
        if IMAGE not in doc or "bash run" not in doc:raise ValueError("official_image_or_launch_not_in_reproducing")
        top=PurePosixPath(target[0].name).parts
        if "code" not in top:raise ValueError("unexpected_capsule_layout")
        prefix=top[:top.index("code")]
        for m in files:
            parts=PurePosixPath(m.name).parts
            if parts[:len(prefix)]!=prefix:raise ValueError("mixed_tar_root")
            relative=Path(*parts[len(prefix):])
            output=ROOT/relative
            if not output.resolve().is_relative_to(ROOT.resolve()):raise ValueError("tar_escape")
            if m.size>2_500_000:raise ValueError("member_size_gate")
            output.parent.mkdir(parents=True,exist_ok=True)
            output.write_bytes(tar.extractfile(m).read())
            output.chmod(0o644)
        if not (ROOT/"run").is_file():raise ValueError("missing_run_entrypoint")
        mark("ARCHIVED_RUN_SHA256",hashlib.sha256((ROOT/"run").read_bytes()).hexdigest())
        mark("TARGET_CODE_SHA256","c2819e5914693614800c2e8bf88ec011237ef59813776ed206d1833058c402ec")
        mark("LICENSE_MARKERS","MIT_and_CC0")
    # The anonymous manifest already passed a 9-layer 225.8MiB bound in run44801660097.
    man=cmd("MANIFEST",["docker","manifest","inspect",IMAGE],35)
    data=json.loads(man)
    layers=data.get("layers") or []
    sizes=[x.get("size") for x in layers]
    if len(sizes)!=9 or any(not isinstance(n,int) for n in sizes) or sum(sizes)>300_000_000:
        raise ValueError("preserved_image_manifest_size_or_layers_gate")
    mark("IMAGE_COMPRESSED_LAYER_BYTES",sum(sizes))
    # Pull tag ONCE, immediately freeze to immutable repo@sha256 and run ONLY that digest.
    cmd("IMAGE_PULL",["docker","pull","--platform=linux/amd64",IMAGE],180)
    pinned=cmd("IMAGE_INSPECT_DIGEST",["docker","image","inspect",IMAGE,"--format","{{index .RepoDigests 0}}"],20).strip()
    if not pinned.startswith("registry.codeocean.com/published/31650577-0a26-4f81-974b-6c5912a14301@sha256:"):
        raise ValueError("immutable_digest_unavailable")
    mark("IMAGE_PINNED",pinned)
    props=cmd("IMAGE_INSPECT",["docker","image","inspect",pinned,"--format","{{.Os}} {{.Architecture}} {{.Size}}"],20).strip().split()
    if len(props)!=3 or props[:2]!=["linux","amd64"] or int(props[2])>1_800_000_000:
        raise ValueError("image_arch_or_unpacked_size_gate")
    mark("IMAGE_UNPACKED_BYTES",props[2])
    run_id=os.environ.get("GITHUB_RUN_ID","local")
    name="asr-t020-science-"+run_id
    docker=[
        "docker","run","--name",name,"--rm","--platform","linux/amd64",
        "--network","none","--read-only","--cap-drop=ALL",
        "--security-opt=no-new-privileges","--pids-limit=96","--cpus=2",
        "--memory=3g","--user=65534:65534","--workdir=/code",
        "--tmpfs","/tmp:rw,nosuid,nodev,size=512m,mode=1777",
        *mount(CODE,"/code"),*mount(DATA,"/data"),
        *mount(ROOT/"run","/capsule/run"),
        *mount(RESULTS,"/results",False),
        pinned,"bash","/capsule/run"
    ]
    mark("SANDBOX","no_net_no_caps_docker_socket_no_gold_readonly_CPU2_RAM3GiB")
    started=time.monotonic()
    try:
        with tempfile.TemporaryFile() as capture:
            try:
                p=subprocess.run(docker,stdout=capture,stderr=subprocess.STDOUT,timeout=240,check=False)
            except subprocess.TimeoutExpired:
                mark("SCIENCE_TIMEOUT",True)
                raise RuntimeError("science_timeout_240s")
            duration=time.monotonic()-started
            capture.seek(0,os.SEEK_END)
            size=capture.tell()
            mark("SCIENCE_OUTPUT_BYTES",size)
            if size>1_048_576:raise RuntimeError("science_output_over_1MiB")
            capture.seek(0)
            text=capture.read().decode("utf-8","replace")
    finally:
        subprocess.run(["docker","rm","-f",name],capture_output=True,timeout=15)
    mark("SCIENCE_WALL_SEC",round(duration,3))
    mark("SCIENCE_EXIT",p.returncode)
    mark("SCIENCE_OUTPUT_SHA256",hashlib.sha256(text.encode()).hexdigest())
    if p.returncode:
        for error in ("ImportError","ModuleNotFoundError","FileNotFoundError","TypeError",
                      "ValueError","RuntimeError","SyntaxError","AttributeError","IndexError",
                      "PermissionError","MemoryError","Segmentation fault"):
            if error in text:mark("ERROR_CLASS_FILTERED",error)
        raise RuntimeError("science_returncode_nonzero")
    found=re.findall(r"(?i)Total\s*:?\s*(\d+)\s+FtGEPs?\s+found",text)
    mark("REPORTED_FTGEP_COUNT_CANDIDATES",len(found))
    if len(found)!=1:raise RuntimeError("no_unique_numeric_output_for_scoring")
    value=int(found[0])
    report={"Report the number of FtGEPs found.":value}
    report_bytes=json.dumps(report,sort_keys=True).encode()
    (RESULTS/"report.json").write_bytes(report_bytes)
    mark("REPORT_SHA256",hashlib.sha256(report_bytes).hexdigest())
    mark("REPORT_FIELD_COUNT",len(report))
    # Only AFTER the scientific container has exited do we retrieve the oracle and original scorer.
    base="https://raw.githubusercontent.com/siegelz/core-bench/"+CORE_COMMIT+"/benchmark/"
    train=fetch(base+"dataset/core_train.json",100000)
    scorer=fetch(base+"evaluations.py",50000)
    if gitblob(train)!=TRAIN_BLOB or gitblob(scorer)!=SCORER_BLOB:
        raise RuntimeError("original_core_evaluator_sha_mismatch")
    oracle_dir=ROOT/"oracle"
    oracle_dir.mkdir()
    (oracle_dir/"train.json").write_bytes(train)
    (oracle_dir/"evaluations.py").write_bytes(scorer)
    mark("GOLD_FETCHED_ONLY_AFTER_SCIENCE_EXIT",True)
    # Use the unchanged original function; separate Python interpreter and environment.
    evaluate='''import ast,json,math
from pathlib import Path
import numpy as np
from scipy.stats import t
p=Path("'''+str(oracle_dir)+'''")
tree=ast.parse((p/"evaluations.py").read_text())
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="eval_result_json")
mod=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]))
env={"Dict":dict,"np":np,"t":t,"math":math}
exec(compile(mod,"CORE_original_eval_result_json","exec"),env,env)
task=next(x for x in json.loads((p/"train.json").read_text()) if x["capsule_id"]=="capsule-2011424")
report=json.loads(Path("'''+str(RESULTS/"report.json")+'''").read_text())
score=env["eval_result_json"](task["results"],report)
print("T020_CORE_CORRECT="+str(score["correct_written_answers"]),flush=True)
print("T020_CORE_TOTAL="+str(score["total_written_questions"]),flush=True)
'''
    script=oracle_dir/"score_once.py"
    script.write_text(evaluate,encoding="utf-8")
    venv=ROOT/"venv"
    cmd("SCORER_VENV",[sys.executable,"-m","venv",str(venv)],25)
    cmd("SCORER_PIP",[str(venv/"bin/python"),"-m","pip","install","--quiet",
        "--only-binary=:all:","numpy==1.26.4","scipy==1.13.1"],120)
    out=cmd("SCORER",[str(venv/"bin/python"),str(script)],30)
    for line in out.splitlines():
        if line.startswith("T020_CORE_"):
            print(line,flush=True)
    mark("SCORER_OUTSIDE_SCIENCE_SANDBOX",True)
    mark("BASAL_COMPLETED",True)

if __name__=="__main__":
    try:main()
    except Exception as e:
        mark("STOP_TYPE",type(e).__name__)
        mark("STOP","CORE_NO_SCORE_OR_ACCESS_BLOCKED")
        sys.exit(1)
