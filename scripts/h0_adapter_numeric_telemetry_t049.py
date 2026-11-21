#!/usr/bin/env python3
"""T0.49 offline-only synthetic test + patch for private-safe request metrics.

Emits numeric sizes/counts, a fixed success boolean, elapsed seconds and exception class.
Never emits request bytes, text, prompts, response, headers, tool names or raw errors.
"""
import argparse
import contextlib
import io
import json
import re
from pathlib import Path
import urllib.request

ANCHORS=(
 ('        body = json.dumps(req_body).encode()\n',
  '        body = json.dumps(req_body).encode()\n'
  '        print("T049_REQUEST_BODY_BYTES="+str(len(body)),flush=True)\n'
  '        print("T049_REQUEST_MESSAGE_COUNT="+str(len(req_body["messages"])),flush=True)\n'
  '        print("T049_REQUEST_TOOL_SCHEMA_COUNT="+str(len(req_body["tools"])),flush=True)\n'),
 ('        for attempt in range(1):\n',
  '        for attempt in range(1):\n'
  '            _t049_started_at=time.monotonic()\n'
  '            print("T049_REQUEST_ATTEMPT_COUNT=1",flush=True)\n'),
 ('                    return from_openai_response(json.loads(r.read()))\n',
  '                    _t049_response=from_openai_response(json.loads(r.read()))\n'
  '                    print("T049_REQUEST_ELAPSED_SECONDS="+format(time.monotonic()-_t049_started_at,".3f"),flush=True)\n'
  '                    print("T049_REQUEST_COMPLETED=true",flush=True)\n'
  '                    return _t049_response\n'),
 ('            except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:\n',
  '            except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:\n'
  '                print("T049_REQUEST_ELAPSED_SECONDS="+format(time.monotonic()-_t049_started_at,".3f"),flush=True)\n'
  '                print("T049_REQUEST_EXCEPTION_CLASS="+type(exc).__name__,flush=True)\n')
)
NUM_FIELDS=frozenset(("REQUEST_BODY_BYTES","REQUEST_MESSAGE_COUNT","REQUEST_TOOL_SCHEMA_COUNT","REQUEST_ATTEMPT_COUNT"))
ALLOWED_EXC=frozenset(("TimeoutError","URLError","ConnectionError"))

def patch_adapter(source):
    out=source
    for old,new in ANCHORS:
        if out.count(old)!=1:
            raise ValueError("source anchor missing/nonunique; stop rather than patch")
        out=out.replace(old,new)
    compile(out,"<patched-openai-adapter>","exec")
    if out.count("urllib.request.urlopen(req, timeout=self.timeout_s)")!=source.count("urllib.request.urlopen(req, timeout=self.timeout_s)"):
        raise ValueError("transport changed")
    if out.count("req_body =")!=source.count("req_body =") or out.count("body = json.dumps(req_body).encode()")!=source.count("body = json.dumps(req_body).encode()"):
        raise ValueError("request body builder changed")
    return out

def parse_metric(line):
    m=re.fullmatch(r"T049_(REQUEST_[A-Z_]+)=(.{1,160})",line)
    if not m:return None
    k,v=m.group(1),m.group(2)
    if k in NUM_FIELDS:
        if not re.fullmatch("[0-9]{1,10}",v):return None
        n=int(v)
        return {k:n} if 0<=n<=2_000_000_000 else None
    if k=="REQUEST_ELAPSED_SECONDS":
        if not re.fullmatch(r"[0-9]{1,5}\.[0-9]{1,3}",v):return None
        n=float(v)
        return {k:n} if 0<=n<=10000 else None
    if k=="REQUEST_EXCEPTION_CLASS":
        return {k:v} if v in ALLOWED_EXC else None
    if k=="REQUEST_COMPLETED":
        return {k:True} if v=="true" else None
    return None

def test_synthetic_adapter(source):
    patched=patch_adapter(source)
    env={"__name__":"h0_t049_synthetic_adapter"}
    exec(compile(patched,"<t049mock>","exec"),env,env)
    fake_secret="PRIVATE_GOLD_RAW_PROMPT_NEVER_LEAK_T049_U2F"
    class Fake:
        status=200
        def __enter__(self):return self
        def __exit__(self,*args):return False
        def read(self):
            return json.dumps({"choices":[{"message":{"content":"synthetic not private","tool_calls":[]},"finish_reason":"stop"}],
                               "usage":{"prompt_tokens":10,"completion_tokens":1}}).encode()
    original=urllib.request.urlopen
    try:
        urllib.request.urlopen=lambda req,timeout:Fake()
        b=io.StringIO()
        with contextlib.redirect_stdout(b):
            a=env["OpenAICompatAgent"]("http://127.0.0.1:11434/v1","mock:synthetic",128,timeout_s=180)
            r=a.converse(fake_secret,[{"role":"user","content":[{"text":fake_secret}]}],[],False)
        lines=b.getvalue().splitlines()
        metrics=[parse_metric(x) for x in lines]
        assert r["usage"]["inputTokens"]==10
        assert all(x is not None for x in metrics)
        assert any("REQUEST_COMPLETED" in x for x in metrics)
        assert fake_secret not in b.getvalue()
        urllib.request.urlopen=lambda req,timeout: (_ for _ in ()).throw(TimeoutError(fake_secret))
        b2=io.StringIO()
        with contextlib.redirect_stdout(b2):
            try:a.converse(fake_secret,[],[],False)
            except TimeoutError:pass
            else:raise AssertionError("expected timeout")
        lines=b2.getvalue().splitlines()
        metrics=[parse_metric(x) for x in lines]
        assert all(x is not None for x in metrics)
        assert any(x.get("REQUEST_EXCEPTION_CLASS")=="TimeoutError" for x in metrics)
        assert not any("REQUEST_COMPLETED" in x for x in metrics)
        assert fake_secret not in b2.getvalue()
    finally:
        urllib.request.urlopen=original
    print("T049_OFFLINE_MOCK_ADAPTER_SUCCESS_AND_TIMEOUT_PASS=true",flush=True)
    print("T049_OFFLINE_ADAPTER_NO_PRIVATE_LEAK=true",flush=True)

def fixtures():
    valid=["T049_REQUEST_BODY_BYTES=220","T049_REQUEST_MESSAGE_COUNT=1",
           "T049_REQUEST_TOOL_SCHEMA_COUNT=9","T049_REQUEST_ATTEMPT_COUNT=1",
           "T049_REQUEST_ELAPSED_SECONDS=90.125",
           "T049_REQUEST_EXCEPTION_CLASS=TimeoutError",
           "T049_REQUEST_COMPLETED=true"]
    assert all(parse_metric(x) is not None for x in valid)
    bad=["T049_REQUEST_BODY_BYTES=-1","T049_REQUEST_MESSAGE_COUNT=inf",
         "T049_REQUEST_TOOL_SCHEMA_COUNT=secret","T049_REQUEST_ATTEMPT_COUNT=2e3",
         "T049_REQUEST_ELAPSED_SECONDS=nan",
         "T049_REQUEST_EXCEPTION_CLASS=RuntimeError",
         "T049_REQUEST_COMPLETED=false",
         "T049_REQUEST_RAW=PRIVATE_CONTENT",
         "T049_REQUEST_BODY_BYTES=999999999999999",
         "PRIVATE_CONTENT"]
    assert all(parse_metric(x) is None for x in bad)
    print("T049_OFFLINE_NUMERIC_ALLOWLIST_FIXTURES_PASS=17",flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--offline-test",action="store_true")
    p.add_argument("--adapter-source")
    a=p.parse_args()
    if not a.offline_test:p.error("offline-only")
    fixtures()
    if a.adapter_source:
        source=Path(a.adapter_source).read_text()
        if 'timeout_s: float = 900.0' not in source:
            raise ValueError("expected original upstream adapter")
        # Apply exactly the prior T0.47 modifications, except timeout 180 not 90.
        old=source
        for before,after in (
          ('"tools": to_openai_tools(tools), "tool_choice": choice, "max_tokens": self.max_tokens',
           '"tools": to_openai_tools(tools), "max_tokens": self.max_tokens, "reasoning_effort": "none"'),
          ("timeout_s: float = 900.0","timeout_s: float = 180.0"),
          ("for attempt in range(6):","for attempt in range(1):"),
          ('if attempt == 5:\n                    raise RuntimeError(f"OpenAI-compatible endpoint failed: {exc}") from exc',
           'if attempt == 0:\n                    raise')):
            if old.count(before)!=1:raise ValueError("original adapter patch prerequisite")
            old=old.replace(before,after)
        test_synthetic_adapter(old)
        print("T049_ORIGINAL_ADAPTER_PIN_PATCH_COMPILES=true",flush=True)
        print("T049_REQUEST_BODY_TRANSPORT_AND_SCORER_UNCHANGED=true",flush=True)

if __name__=="__main__":
    main()
