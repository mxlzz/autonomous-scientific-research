#!/usr/bin/env python3
"""T0.23: exact upstream tool API capability gate, no model and no private truth output.

The evaluator retains private task files. This tests the API dispatcher only, NOT OS
isolation. This script does not alter the upstream SciResearch-Eval repository.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time

from sciresearch_eval.agents.tools import AgentTools
from sciresearch_eval.env import ThermalEnv, ToolError
from sciresearch_eval.tasks.generator import public_id_for

UPSTREAM = "9d391b3aa8daf8d0b944acda12c7f8b089a1d8e0"
ROOT = Path("/project/tasks")
TASK = "task_525abee377"
PRIVATE_KEYS = (
    "truth_spec","true_free_params","labels","hidden_target_true_K",
    "severity","regime","converged_settings","truth_settings"
)
start = time.monotonic()
def mark(k, v):
    print("T023_" + k + "=" + str(v), flush=True)

def native_tests():
    for f, tests in (
        ("test_env_grader.py", ("test_interval_score", "test_tool_outputs_never_contain_private_fields")),
        ("test_agent_tools.py", ("test_task_view_is_summarized_and_leak_free",
                                 "test_fit_then_fetch_residuals_and_readings",
                                 "test_condition_c_requires_state_update_between_actions")),
    ):
        spec=importlib.util.spec_from_file_location(
            "original_" + f.replace(".","_"),"/project/tests/" + f)
        m=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for name in tests:
            getattr(m,name)()
            mark("ORIGINAL_TEST_PASS", f + "::" + name)
    mark("ORIGINAL_TESTS_PASS", 5)

def main():
    mark("UPSTREAM", UPSTREAM)
    mark("TASK", TASK)
    mark("LLM_CALLS", 0)
    mark("PAID_APIS", False)
    mark("PRIVATE_FILES_IN_EVALUATOR", True)
    mark("ACTOR_OS_FS_ISOLATION", False)
    assert public_id_for("t3_coarse_mesh_2001",root=ROOT)==TASK
    native_tests()
    tools=AgentTools(ThermalEnv(TASK,ROOT,"dev"),"A")
    specs=tools.specs()
    advertised=[x["name"] for x in specs]
    assert len(advertised)==len(set(advertised)), "duplicate tool schema names"
    assert not {"exec","shell","read_file","filesystem","browser"} & set(advertised)
    mark("CONDITION_A_ADVERTISED_TOOLS", ",".join(advertised))
    mark("CONDITION_A_ADVERTISED_TOOL_COUNT", len(advertised))
    mark("FILE_SHELL_TOOLS_IN_SPECS", False)
    task=tools.task_view()
    b=json.dumps(task)
    assert "summary" in b and len(b)<20000
    if any(key in b for key in PRIVATE_KEYS):
        raise RuntimeError("private_key_in_task_view")
    mark("TASK_VIEW_PRIVATE_KEY_SCAN", "PASS")
    observed_rejections={}
    for name in ("read_file","exec","shell","filesystem","browser"):
        try:
            tools.call(name,{})
        except ToolError:
            observed_rejections[name]=True
        else:
            observed_rejections[name]=False
        mark("UNKNOWN_" + name.upper() + "_REJECTED", observed_rejections[name])
    assert all(observed_rejections.values()), "dangerous tool name allowed"
    allowed=tools.call("budget_status",{})
    assert set(allowed)=={"budget","used"}
    mark("ADVERTISED_BUDGET_STATUS", "PASS")
    state_name="update_state"
    mark("CONDITION_A_UPDATE_STATE_IN_SPECS", state_name in advertised)
    # The condition A schema deliberately excludes update_state, which belongs
    # only to condition C/D. A robust dispatcher must reject this request.
    if state_name in advertised:
        raise RuntimeError("unexpected advertised update_state for condition A")
    bypass=False
    try:
        response=tools.call(state_name, {
            "hypotheses":[],"evidence":[],
            "next_action":"controlled_interface_test","why":"security check"
        })
    except ToolError:
        pass
    else:
        bypass=response.get("recorded") is True
    mark("UNADVERTISED_CONDITION_A_UPDATE_STATE_ACCEPTED",bypass)
    mark("UNADVERTISED_RECOMMEND_HANDLER_EXISTS",hasattr(tools,"_t_recommend_experiment"))
    # No unadvertised recommend_experiment call is made: it can consume compute.
    # No private values are returned, only class and action capability flags.
    gate="FAIL_SCHEMA_ALLOWLIST_DISPATCH" if bypass else "PASS_SCHEMA_ALLOWLIST_DISPATCH"
    mark("TOOL_DISPATCH_GATE",gate)
    mark("DATA_LEAK_OBSERVED",False)
    mark("ACTOR_WITH_FILE_TOOLS_SAFE",False)
    mark("GATE_NOT_OS_ISOLATION",True)
    summary={
       "source":UPSTREAM,"task_public_id":TASK,"split":"dev",
       "scope":"API tool interface only; no LLM or OS actor separation",
       "advertised_tools_condition_A":advertised,
       "original_tests_passed_count":5,
       "unknown_file_shell_tool_names_rejected":observed_rejections,
       "task_view_scanned_for_private_field_names":True,
       "unadvertised_update_state_accepted_in_A":bypass,
       "unadvertised_recommend_handler_present":hasattr(tools,"_t_recommend_experiment"),
       "dispatcher_gate":gate,
       "leak_of_private_values_observed":False,
       "private_files_mounted_in_evaluator":True,
       "actor_os_fs_isolation_proven":False,
       "model_calls":0,"paid_apis":False,
       "wall_sec":round(time.monotonic()-start,4),
       "controller_maxrss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    }
    output=Path("/results/t023_api_gate.json")
    data=(json.dumps(summary,sort_keys=True,indent=2)+"\n").encode()
    output.write_bytes(data)
    mark("SUMMARY_SHA256",hashlib.sha256(data).hexdigest())
    mark("WALL_SEC",summary["wall_sec"])
    mark("RSS_PROCESS_KIB",summary["controller_maxrss_kib"])
    mark("GATE_TEST_EXECUTED",True)
    # Return success for a *correctly observed security finding*, not a PASS gate.
    # Consumers MUST examine T023_TOOL_DISPATCH_GATE.
if __name__=="__main__":
    try: main()
    except BaseException as exc:
        mark("STOP_EXCEPTION_CLASS",type(exc).__name__)
        mark("TEST_RESULT","INCOMPLETE")
        sys.exit(1)
