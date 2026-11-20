#!/usr/bin/env python3
"""T0.17: one bounded CPU-only scientific reproduction of CORE train capsule-5975162.

This is a trusted *pilot controller*, NOT an autonomous research agent.
Only the pinned capsule script and binary wheels enter the scientific container.
Gold and the original scorer are downloaded and mounted only after it exits.
No extra source is extracted from the original archive; no Code Ocean Dockerfile.
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

CAPSULE_URL = "https://corebench.cs.princeton.edu/capsules/capsule-5975162.tar.gz"
CAPSULE_SHA = "5668df380ab8b4f2cb7e3724d6fb2d6d2151714d7a571545e6c256c74b598e48"
CORE_COMMIT = "e32a2980e72fe6eb04ee04eb749458f570625663"
TRAIN_BLOB = "8ea09677fd4d98a4995144b959ba6f65bb2a85aa"
SCORER_BLOB = "ecf1d77718c3a7e07bf48c37d7263656b5f7f06f"
IMAGE_TAG = "python:3.9-slim-bookworm"
RUN_ID = os.getenv("GITHUB_RUN_ID", "local")
BASE = Path(os.environ["RUNNER_TEMP"]) / "t017-sandbox"
WORK, WHEELS, OUT, EVAL = (BASE / part for part in ("work", "wheels", "out", "evaluator"))
for folder in (WORK, WHEELS, OUT, EVAL):
    folder.mkdir(parents=True, exist_ok=True)
    folder.chmod(0o777 if folder in (WHEELS, OUT) else 0o755)


def fetch(url, limit):
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "ASR-T0.17-cpu-baseline/1"}),
        timeout=25,
    ) as response:
        b = response.read(limit + 1)
    if len(b) > limit:
        raise ValueError("download limit exceeded")
    return b


def gitblob(b):
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def run_step(stage, args, timeout=120):
    before = time.monotonic()
    try:
        result = subprocess.run(
            args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        print("T017_" + stage + "_TIMEOUT=true", flush=True)
        raise RuntimeError(stage + ": timeout")
    elapsed = time.monotonic() - before
    print("T017_" + stage + "_WALL_SEC=" + str(round(elapsed, 3)), flush=True)
    for line in result.stdout.splitlines():
        if line.startswith("T017_"):
            print(line[:350], flush=True)
    if result.returncode:
        print("T017_" + stage + "_EXIT=" + str(result.returncode), flush=True)
        # Do not copy unreviewed third-party output into public logs.
        raise RuntimeError(stage + ": nonzero exit")
    return result


def mount(path, target, readonly=True):
    return ["--mount", "type=bind,src=" + str(path) + ",dst=" + target + (",readonly" if readonly else "")]


def sandbox(name, image, extra, *, network="none", memory="3g"):
    return [
        "docker", "run", "--name", name, "--rm",
        "--network", network, "--read-only", "--cap-drop=ALL",
        "--security-opt=no-new-privileges", "--pids-limit=96",
        "--memory=" + memory, "--cpus=2", "--user=65534:65534",
        "--tmpfs", "/tmp:rw,nosuid,nodev,size=768m,mode=1777",
        "--env", "OPENBLAS_NUM_THREADS=1",
        "--env", "OMP_NUM_THREADS=1",
        "--env", "MKL_NUM_THREADS=1",
        "--env", "PYTHONDONTWRITEBYTECODE=1",
        *extra, image,
    ]


def write_file(path, text):
    path.write_text(text, encoding="utf-8")
    path.chmod(0o644)


def main():
    print("T017_CANDIDATE=train/capsule-5975162/codeocean_hard", flush=True)
    print("T017_BUDGET=one_script_run_cpu2_mem3g_timeout240s", flush=True)
    print("T017_ORIGINAL_DOCKERFILE_NOT_USED=true", flush=True)
    print("T017_ORIGINAL_HARNESS_NOT_USED=true", flush=True)
    package = fetch(CAPSULE_URL, 1024 * 1024)
    if hashlib.sha256(package).hexdigest() != CAPSULE_SHA:
        raise ValueError("capsule digest changed; stop")
    print("T017_CAPSULE_SHA256_MATCH=true", flush=True)
    with tarfile.open(fileobj=io.BytesIO(package), mode="r:gz") as tf:
        members = tf.getmembers()
        if len(members) != 47 or sum(m.size for m in members if m.isfile()) > 10_000_000:
            raise ValueError("unexpected archive structure")
        for member in members:
            p = PurePosixPath(member.name)
            if (p.is_absolute() or ".." in p.parts or member.issym()
                    or member.islnk() or member.isdev()):
                raise ValueError("unsafe archive member")
        candidates = [
            m for m in members
            if m.isfile() and m.name.rsplit("/", 1)[-1] == "ExPSOWithClassicalBenchmark02.py"
        ]
        if len(candidates) != 1 or candidates[0].size != 856:
            raise ValueError("wrong script")
        script = tf.extractfile(candidates[0]).read(2048)
    ast.parse(script.decode("utf-8"))
    (WORK / "ExPSOWithClassicalBenchmark02.py").write_bytes(script)
    (WORK / "ExPSOWithClassicalBenchmark02.py").chmod(0o644)
    print("T017_SCIENTIFIC_SCRIPT_SHA256=" + hashlib.sha256(script).hexdigest(), flush=True)

    run_step("PULL", ["docker", "pull", IMAGE_TAG], timeout=120)
    image_id = subprocess.check_output(
        ["docker", "image", "inspect", IMAGE_TAG, "--format", "{{index .RepoDigests 0}}"],
        text=True,
    ).strip()
    if "@sha256:" not in image_id:
        raise ValueError("unfrozen Docker image")
    print("T017_IMAGE_DIGEST=" + image_id, flush=True)

    # Dependency downloads are isolated from the runner. Binary wheels only, no builds.
    wheel_container = "t017-wheel-" + RUN_ID
    cmd = sandbox(
        wheel_container, image_id,
        mount(WHEELS, "/wheels", False), network="bridge", memory="2g",
    ) + [
        "python", "-m", "pip", "download", "--only-binary=:all:",
        "--no-deps", "--disable-pip-version-check", "-d", "/wheels",
        "ExPSO==0.1.4", "numpy==1.26.2", "scipy==1.13.1",
    ]
    try:
        run_step("WHEEL_DOWNLOAD", cmd, timeout=120)
    finally:
        subprocess.run(["docker", "rm", "-f", wheel_container], capture_output=True)
    wheel_files = sorted(WHEELS.glob("*.whl"))
    if len(wheel_files) != 3:
        raise ValueError("expected 3 pinned binary wheels")
    for wf in wheel_files:
        print("T017_WHEEL_SHA256=" + wf.name + "," + hashlib.sha256(wf.read_bytes()).hexdigest(), flush=True)

    runner = '''import contextlib, io, json, math, resource, runpy, time
import numpy as np
np.random.seed(0)
t0=time.monotonic()
with contextlib.redirect_stdout(io.StringIO()):
    record=runpy.run_path("/work/ExPSOWithClassicalBenchmark02.py",run_name="__main__")
metrics=record["best_solution"]["Metrics"]
mean=float(metrics["MEAN"])
fes=float(metrics["Avg_FES"])
if not math.isfinite(mean) or not math.isfinite(fes):
    raise ValueError("non-finite metric")
report={"Report the mean metric from the output.":mean,
        "Report the Avg FES from the output.":fes}
with open("/out/report.json","w") as f: json.dump(report,f)
with open("/out/resource.json","w") as f:
    json.dump({"wall_sec":round(time.monotonic()-t0,4),
               "process_maxrss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
               "seed":0,"model_calls":0},f)
print("T017_SCRIPT_FINISHED=true",flush=True)
print("T017_REPORT_FIELDS=2",flush=True)
'''
    write_file(WORK / "run_once.py", runner)
    run_container = "t017-science-" + RUN_ID
    cmd = sandbox(
        run_container, image_id,
        mount(WORK, "/work") + mount(WHEELS, "/wheels")
        + mount(OUT, "/out", False),
    ) + [
        "sh", "-c",
        "python -m pip install --no-index --find-links=/wheels --no-deps "
        "--target /tmp/site ExPSO==0.1.4 numpy==1.26.2 >/tmp/pip.log 2>&1 "
        "&& PYTHONPATH=/tmp/site python /work/run_once.py",
    ]
    try:
        run_step("SCIENCE", cmd, timeout=240)
    finally:
        subprocess.run(["docker", "rm", "-f", run_container], capture_output=True)
    if not (OUT / "report.json").is_file() or not (OUT / "resource.json").is_file():
        raise ValueError("missing scientific report/resource")
    report_raw = (OUT / "report.json").read_bytes()
    resource = json.loads((OUT / "resource.json").read_text())
    print("T017_REPORT_SHA256=" + hashlib.sha256(report_raw).hexdigest(), flush=True)
    print("T017_SCIENCE_WALL_SEC=" + str(resource["wall_sec"]), flush=True)
    print("T017_SCIENCE_MAXRSS_KIB=" + str(resource["process_maxrss_kib"]), flush=True)
    print("T017_SEED=0", flush=True)

    # Ground truth and scorer are fetched only AFTER the scientific container exits,
    # and are mounted ONLY in a second, independent read-only evaluator container.
    url_base = "https://raw.githubusercontent.com/siegelz/core-bench/" + CORE_COMMIT
    train = fetch(url_base + "/benchmark/dataset/core_train.json", 100_000)
    scorer = fetch(url_base + "/benchmark/evaluations.py", 50_000)
    if gitblob(train) != TRAIN_BLOB or gitblob(scorer) != SCORER_BLOB:
        raise ValueError("reference source SHA mismatch")
    (EVAL / "core_train.json").write_bytes(train)
    (EVAL / "evaluations.py").write_bytes(scorer)
    print("T017_EVALUATOR_AND_TRAIN_PINNED=true", flush=True)
    scorer_code = '''import ast, json, math
import numpy as np
from scipy.stats import t
from pathlib import Path
src=ast.parse(Path("/eval/evaluations.py").read_text())
fn=next(node for node in src.body if isinstance(node,ast.FunctionDef) and node.name=="eval_result_json")
obj=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]))
env={"Dict":dict,"np":np,"t":t,"math":math}
exec(compile(obj,"<original_CORE_eval_result_json>","exec"),env,env)
data=json.loads(Path("/eval/core_train.json").read_text())
task=next(item for item in data if item["capsule_id"]=="capsule-5975162")
report=json.loads(Path("/out/report.json").read_text())
assert set(report)==set(task["results"][0]),"report fields mismatch"
score=env["eval_result_json"](task["results"],report)
assert score["total_written_questions"]==2,score
print("T017_ORIGINAL_CORE_QUESTION_SCORE=%d/%d"%(score["correct_written_answers"],score["total_written_questions"]),flush=True)
print("T017_ORIGINAL_CORE_TASK_SUCCESS="+str(score["correct_written_answers"]==2),flush=True)
print("T017_ORACLE_SEPARATION=post_process_only",flush=True)
'''
    write_file(EVAL / "score_once.py", scorer_code)
    score_container = "t017-score-" + RUN_ID
    cmd = sandbox(
        score_container, image_id,
        mount(EVAL, "/eval") + mount(OUT, "/out") + mount(WHEELS, "/wheels"),
        memory="2g",
    ) + [
        "sh", "-c",
        "python -m pip install --no-index --find-links=/wheels --no-deps "
        "--target /tmp/site numpy==1.26.2 scipy==1.13.1 >/tmp/pip.log 2>&1 "
        "&& PYTHONPATH=/tmp/site python /eval/score_once.py",
    ]
    try:
        run_step("SCORER", cmd, timeout=90)
    finally:
        subprocess.run(["docker", "rm", "-f", score_container], capture_output=True)
    print("T017_COMPLETED_BASAL_REPRODUCTION=true", flush=True)
    print("T017_NO_LLM_OR_PAID_API=true", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("T017_RESULT=BLOCKED", flush=True)
        print("T017_FAILURE_CLASS=" + type(exc).__name__, flush=True)
        print("T017_FAILURE_REASON=" + str(exc)[:180], flush=True)
        sys.exit(1)
