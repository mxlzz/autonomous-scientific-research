#!/usr/bin/env python3
"""T0.40: check Ollama 4B tag metadata only. NEVER request inference.

Only allowlisted metrics are printed. No prompts, weights, template text, private task
data or full /api/show payload leave this ephemeral process.
"""
import argparse
import json
import re
import sys
import urllib.request

MODEL="qwen3:4b-instruct-2507-q4_K_M"
PREFIX="0edcdef34593"
VERSION_RE=re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.\-]+)?$")
SHA_RE=re.compile(r"^[0-9a-f]{64}$")

def inspect(tag_data, show_data, version_data):
    models=tag_data.get("models", [])
    chosen=[m for m in models if isinstance(m,dict) and m.get("name")==MODEL]
    name_unique=(len(chosen)==1)
    manifest=chosen[0].get("digest") if name_unique else ""
    digest_ok=isinstance(manifest,str) and bool(SHA_RE.fullmatch(manifest)) and manifest.startswith(PREFIX)
    version=version_data.get("version")
    version_ok=isinstance(version,str) and bool(VERSION_RE.fullmatch(version))
    template=show_data.get("template", "")
    if not isinstance(template,str):
        template=""
    caps=show_data.get("capabilities", [])
    tools_ok=isinstance(caps,list) and "tools" in caps
    template_ok=("<tool_call>" in template and "Tools" in template)
    thinking=show_data.get("thinking")
    # In non-thinking Instruct the 'thinking' field may be omitted legitimately.
    thinking_values=thinking.get("values") if isinstance(thinking,dict) else None
    thinking_false_only=isinstance(thinking_values,list) and len(thinking_values)==1 and thinking_values[0] is False
    size=chosen[0].get("size") if name_unique else None
    if type(size) is not int or size<0 or size>100_000_000_000:
        size=None
    details=chosen[0].get("details") if name_unique else None
    quant=details.get("quantization_level") if isinstance(details,dict) else None
    quant_ok=(quant=="Q4_K_M")
    model_dir=show_data.get("details")
    show_quant=model_dir.get("quantization_level") if isinstance(model_dir,dict) else None
    show_quant_ok=(show_quant=="Q4_K_M")
    info=show_data.get("model_info")
    info_family=info.get("general.architecture") if isinstance(info,dict) else None
    arch_ok=isinstance(info_family,str) and bool(re.fullmatch("[a-zA-Z0-9_-]{1,40}",info_family))
    out={
        "tag_name_unique":name_unique,"manifest_digest_prefix_ok":digest_ok,
        "full_manifest_digest":manifest if digest_ok else None,
        "model_size_bytes":size,"ollama_version":version if version_ok else None,
        "model_tools_capability":tools_ok,"template_tool_call_supported":template_ok,
        "thinking_metadata_present":isinstance(thinking,dict),
        "thinking_false_only_metadata":thinking_false_only,
        "tag_quantization_q4_k_m":quant_ok,
        "show_quantization_q4_k_m":show_quant_ok,
        "model_architecture_known":arch_ok
    }
    out["metadata_gate_pass"]=(name_unique and digest_ok and version_ok and tools_ok and
                               template_ok and quant_ok and show_quant_ok and size is not None)
    return out

def fixture_tests():
    secret="FORBIDDEN_PROMPT_OR_PRIVATE_OR_TEMPLATE_X8340"
    d={ "models":[{"name":MODEL,"digest":PREFIX+"a"*(64-len(PREFIX)),
                   "size":2500000000,"details":{"quantization_level":"Q4_K_M"}}]}
    sh={"template":"{{ if .Tools }} <tool_call>"+secret+"</tool_call>{{end}}",
        "details":{"quantization_level":"Q4_K_M"},
        "model_info":{"general.architecture":"qwen3"},
        "capabilities":["completion","tools"]}
    ver={"version":"0.40.16"}
    out=inspect(d,sh,ver)
    assert out["metadata_gate_pass"] is True
    assert secret not in json.dumps(out)
    assert out["thinking_metadata_present"] is False
    tests=[(d,{"template":secret},ver),(d,sh,{"version":secret}),
           ({"models":[]},sh,ver),
           ({"models":[{"name":MODEL,"digest":secret,"size":0}]},sh,ver),
           ({"models":[d["models"][0],d["models"][0]]},sh,ver),
           (d,{**sh,"capabilities":["completion"]},ver),
           (d,{**sh,"details":{"quantization_level":"Q8_0"}},ver)]
    for x,y,z in tests:
        val=inspect(x,y,z)
        assert val["metadata_gate_pass"] is False
        assert secret not in json.dumps(val)
    print("T040_OFFLINE_META_FIXTURES_PASS=8",flush=True)
    print("T040_OFFLINE_NO_RAW_TEMPLATE_LEAK=true",flush=True)

def get_json(path,payload=None):
    url="http://127.0.0.1:11434"+path
    data=json.dumps(payload).encode() if payload is not None else None
    headers={"Content-Type":"application/json"} if data is not None else {}
    req=urllib.request.Request(url,data=data,headers=headers)
    with urllib.request.urlopen(req,timeout=12) as response:
        assert response.status==200
        return json.load(response)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--offline-test",action="store_true")
    p.add_argument("--inspect-runtime",action="store_true")
    args=p.parse_args()
    if args.offline_test:
        fixture_tests()
    if args.inspect_runtime:
        data=inspect(get_json("/api/tags"),get_json("/api/show",{"model":MODEL}),get_json("/api/version"))
        for name,value in data.items():
            print("T040_"+name.upper()+"="+(str(value).lower() if isinstance(value,bool) else str(value)),flush=True)
        if not data["metadata_gate_pass"]:
            print("T040_DECISION=NO_GO_METADATA_GATE",flush=True)
            return 2
        print("T040_DECISION=GO_METADATA_ONLY_NO_INFERENCE",flush=True)
    return 0

if __name__=="__main__":
    sys.exit(main())
