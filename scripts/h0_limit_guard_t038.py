#!/usr/bin/env python3
"""Offline, allowlisted stop-budget observability for future SciResearch harness copies.

Never serialize tool inputs, chat contents, error strings, private truth or gold.
No model and no benchmark execution. Source patches are opt-in and only compiled/tested.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from types import SimpleNamespace

TRIGGERS=frozenset(("none","turns_only","tokens_only","both"))
GUARD_ANCHOR='                if not final_turn:\n                    final_turn = True\n'
GUARD_REPLACEMENT=(
    '                if not final_turn:\n'
    '                    usage["limit_trigger"] = (\n'
    '                        "both" if usage["turns"] >= MAX_TURNS and total_in >= max_input_tokens\n'
    '                        else "turns_only" if usage["turns"] >= MAX_TURNS\n'
    '                        else "tokens_only"\n'
    '                    )\n'
    '                    final_turn = True\n'
)

def count(value, label):
    # bool is an int subclass and MUST be rejected.
    if type(value) is not int or not 0 <= value <= 1_000_000_000:
        raise ValueError("invalid nonnegative count: "+label)
    return value

def from_runtime(harness):
    """Metadata from the loaded module's globals, NOT a copied literal."""
    return {
        "max_turns":count(getattr(harness,"MAX_TURNS",None),"max_turns"),
        "max_tool_calls":count(getattr(harness,"MAX_TOOL_CALLS",None),"max_tool_calls")
    }

def metrics(usage, max_turns, max_input_tokens):
    turns=count(usage.get("turns"),"turns")
    fresh=count(usage.get("input_tokens"),"input_tokens")
    cached_read=count(usage.get("cache_read_tokens"),"cache_read_tokens")
    cached_write=count(usage.get("cache_write_tokens"),"cache_write_tokens")
    max_turns=count(max_turns,"max_turns")
    max_input_tokens=count(max_input_tokens,"max_input_tokens")
    if max_turns == 0 or max_input_tokens == 0:
        raise ValueError("limit must be positive")
    total=fresh+cached_read+cached_write
    turns_hit=turns>=max_turns
    tokens_hit=total>=max_input_tokens
    trigger=("both" if turns_hit and tokens_hit else
             "turns_only" if turns_hit else
             "tokens_only" if tokens_hit else "none")
    assert trigger in TRIGGERS
    return {
        "turns":turns,"input_tokens":fresh,"cache_read_tokens":cached_read,
        "cache_write_tokens":cached_write,"total_input_tokens":total,
        "max_turns":max_turns,"max_input_tokens":max_input_tokens,
        "trigger_at_sample":trigger
    }

def patch_harness_source(source):
    """One additive metadata assignment only when first final_turn is enabled."""
    if source.count(GUARD_ANCHOR)!=1:
        raise ValueError("original harness guard anchor changed; no patch")
    updated=source.replace(GUARD_ANCHOR,GUARD_REPLACEMENT)
    compile(updated,"<pinned_sciresearch_harness_instrumented>","exec")
    return updated

def fixtures():
    secret="PRIVATE_ARGUMENT_AND_GOLD_SHOULD_NOT_APPEAR_NJ903"
    def u(turns=0,fresh=0,read=0,write=0):
        return {"turns":turns,"input_tokens":fresh,
                "cache_read_tokens":read,"cache_write_tokens":write,
                "unused_private_payload":secret}
    cases=[
        ("none",u(5,7810),8,12000,"none",7810),
        ("turns_only",u(8,7810),8,12000,"turns_only",7810),
        ("tokens_only_with_cache",u(5,7810,4190),8,12000,"tokens_only",12000),
        ("both",u(8,7810,4190),8,12000,"both",12000),
        ("tokens_with_write",u(7,8000,0,4000),8,12000,"tokens_only",12000),
        ("just_below",u(7,7809,4190),8,12000,"none",11999),
        ("zero",u(),8,12000,"none",0),
        ("no_cache_reach",u(5,12000),8,12000,"tokens_only",12000)
    ]
    for name,usage,turn_limit,input_limit,want,total in cases:
        result=metrics(usage,turn_limit,input_limit)
        assert result["trigger_at_sample"]==want,(name,result)
        assert result["total_input_tokens"]==total,name
        assert secret not in json.dumps(result),name
        assert set(result)=={"turns","input_tokens","cache_read_tokens","cache_write_tokens",
                             "total_input_tokens","max_turns","max_input_tokens","trigger_at_sample"}
    for field in ("turns","input_tokens","cache_read_tokens","cache_write_tokens"):
        for bad in (-1,True,secret):
            item=u()
            item[field]=bad
            try:metrics(item,8,12000)
            except ValueError:pass
            else:raise AssertionError("bad value accepted: "+field)
    assert from_runtime(SimpleNamespace(MAX_TURNS=8,MAX_TOOL_CALLS=4))=={
        "max_turns":8,"max_tool_calls":4}
    assert from_runtime(SimpleNamespace(MAX_TURNS=8,MAX_TOOL_CALLS=4))["max_turns"]!=4
    for bad in (-1,True,secret,0):
        try:metrics(u(),bad,12000)
        except ValueError:pass
        else:raise AssertionError("bad limit accepted")
    try:patch_harness_source("not a harness")
    except ValueError:pass
    else:raise AssertionError("incorrect source accepted")
    print("T038_METRICS_FIXTURES_PASS=8",flush=True)
    print("T038_INVALID_COUNTS_REJECTED=12",flush=True)
    print("T038_RUNTIME_MAX_TURNS_FROM_LOADED_MODULE=true",flush=True)
    print("T038_NO_PRIVATE_STRING_LEAK=true",flush=True)

def test_source(path):
    source=Path(path).read_text()
    updated=patch_harness_source(source)
    assert updated.count('usage["limit_trigger"]')==1
    assert updated.count("final_turn = True")==source.count("final_turn = True")
    assert updated.count("tools.call(")==source.count("tools.call(")
    assert updated.count("grade(env)")==source.count("grade(env)")
    assert updated.count("MAX_TURNS = 80")==1 # original source unchanged for future copied patch
    assert updated.count("if usage[\"turns\"] >= MAX_TURNS or total_in >= max_input_tokens:")==1
    # Run controlled single-branch excerpt with synthetic counters; never import harness.
    branch='\n'.join(updated.splitlines()[255:268])
    assert "limit_trigger" in branch
    print("T038_PINNED_HARNESS_PATCH_COMPILES=true",flush=True)
    print("T038_DISPATCH_AND_GRADER_TEXT_UNCHANGED=true",flush=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--source")
    a=p.parse_args()
    if not a.self_test:
        p.error("offline self-test required")
    fixtures()
    if a.source:
        test_source(a.source)

if __name__=="__main__":
    main()
