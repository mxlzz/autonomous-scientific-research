#!/usr/bin/env python3
"""Allowlisted error-category extractor; never serialize tool responses or private values."""
import json

ALLOWED=frozenset(("final_turn_non_submit","tool_limit","invalid_arguments",
                   "tool_error","other"))

def category(tool_result):
    if not isinstance(tool_result,dict) or tool_result.get("status")!="error":
        return None
    blocks=tool_result.get("content") or []
    payload=blocks[0].get("json") if isinstance(blocks,list) and blocks and isinstance(blocks[0],dict) else None
    msg=payload.get("error") if isinstance(payload,dict) else None
    if not isinstance(msg,str):
        return "other"
    if msg.startswith("turn or token limit reached; only submit"):
        return "final_turn_non_submit"
    if msg.startswith("tool-call limit reached"):
        return "tool_limit"
    if msg.startswith("invalid arguments:"):
        return "invalid_arguments"
    return "tool_error"

def test_fixtures():
    secret="RAW_PRIVATE_TRUTH_AND_TOOL_ARGUMENT_SHOULD_NEVER_LOG_QT41"
    def tool(status, error=None):
        return {"status":status,"content":[{"json":{"error":error}}]}
    fixtures=(
        ("success",tool("success",secret),None),
        ("final",tool("error","turn or token limit reached; only submit is allowed now"),"final_turn_non_submit"),
        ("toolbudget",tool("error","tool-call limit reached; call submit now"),"tool_limit"),
        ("invalid_args",tool("error","invalid arguments: TypeError: "+secret),"invalid_arguments"),
        ("toolerror",tool("error","unknown source_id "+secret),"tool_error"),
        ("missing_error",{"status":"error","content":[{"json":{}}]},"other"),
        ("wrong_content",{"status":"error","content":[{"text":secret}]},"other"),
        ("bad_status",{"status":"success","content":[{"json":{"error":secret}}]},None),
        ("empty",{"status":"error"}, "other")
    )
    for name,x,want in fixtures:
        got=category(x)
        assert got==want,(name,got,want)
        assert got is None or got in ALLOWED
        assert secret not in json.dumps({"category":got}),name
    print("T036_OFFLINE_ERROR_TAXONOMY_FIXTURES_PASS=9",flush=True)
    print("T036_OFFLINE_NO_PRIVATE_STRING_LEAK_PASS=true",flush=True)

if __name__=="__main__":
    test_fixtures()
