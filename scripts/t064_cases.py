#!/usr/bin/env python3
"""T0.64: original fictional scientific cases. No network, no third-party benchmark data."""
import math
import sys

SYSTEM = (
    "You are an experimental scientist working with a wholly fictional numerical instrument. "
    "The specified deterministic measurement tool is your only source of new data. "
    "Choose informative interventions, then call submit. Do not guess when the observations "
    "are ambiguous. At most 2 measurements and 3 responses per episode. "
    "No web browsing, external datasets, or code execution is available."
)
CASES = {
    "mechanisms": {
        "question": (
            "Two rival mechanisms predict response y for integer x 0..4: "
            "model A: y=4+3*x, model B: y=4+3*x+0.4*x*(x-1). "
            "Any sensor reading may deviate by at most 0.5 from its mechanism's predicted value. "
            "Initial readings are x=0 -> 4.0, x=1 -> 7.0. "
            "Use measure(x) at a permitted point to distinguish which mechanism produced the readings. "
            "Predict y at the reserved x=4 without measuring x=4. "
            "Submit model_choice ('A' or 'B'), predicted_y and rationale."
        ),
        "allowed_measurements": (2, 3),
        "target": 4,
        "measurements": {2: 10.4, 3: 15.4},
        "submit_schema": {
            "model_choice": {"type": "string", "enum": ["A", "B"]},
            "predicted_y": {"type": "number"},
            "rationale": {"type": "string"}
        },
    },
    "outlier": {
        "question": (
            "A fictional instrument follows an underlying linear law y=a+b*x. "
            "Every good sensor reading deviates by at most 0.2 from the true line. "
            "Exactly one of the initial readings is grossly corrupted. "
            "Initial readings (x,y): (0,2.1),(1,4.9),(2,8.0),(3,23.1),(4,13.9). "
            "Use measure(x) at a permitted validation point to verify your calibration. "
            "Predict the underlying true y at reserved x=6 (cannot measure it). "
            "Report a narrow interval containing your predicted true value. "
            "Submit estimated coefficients a,b, anomalous outlier_x, predicted_y, lower, upper, rationale."
        ),
        "allowed_measurements": (5, 7),
        "target": 6,
        "measurements": {5: 17.1, 7: 23.0},
        "submit_schema": {
            "a": {"type": "number"}, "b": {"type": "number"},
            "outlier_x": {"type": "integer"}, "predicted_y": {"type": "number"},
            "lower": {"type": "number"}, "upper": {"type": "number"},
            "rationale": {"type": "string"}
        },
    },
}

def tools_for(case_name):
    case = CASES[case_name]
    submit_fields = case["submit_schema"]
    return [
        {"type": "function", "function": {
            "name": "measure", "description": "Get a synthetic sensor reading for a permitted integer x.",
            "parameters": {"type": "object", "properties": {
                "x": {"type": "integer", "enum": list(case["allowed_measurements"])}
            }, "required": ["x"], "additionalProperties": False}
        }},
        {"type": "function", "function": {
            "name": "submit", "description": "Submit your scientific conclusion and reserved prediction.",
            "parameters": {"type": "object", "properties": submit_fields,
                           "required": list(submit_fields), "additionalProperties": False}
        }}
    ]

def check_x(case_name, arguments):
    return (isinstance(arguments, dict) and set(arguments) == {"x"}
            and type(arguments["x"]) is int
            and arguments["x"] in CASES[case_name]["allowed_measurements"])

def measure(case_name, x):
    if x not in CASES[case_name]["allowed_measurements"]:
        raise ValueError("forbidden_measurement")
    return {"value": CASES[case_name]["measurements"][x]}

def is_number(value):
    return type(value) in (float, int) and math.isfinite(value)

def score(case_name, args, observed_x, forbidden_attempt=False):
    """Independent deterministic grader; only called after structured submit, never in actor prompt."""
    base = {"submitted": True, "science_status": "GRADED_FAIL", "pass": False,
            "criterion": "MECHANISM_SELECTION" if case_name == "mechanisms" else "ROBUST_CALIBRATION",
            "method_review": "NOT_REVIEWED"}
    if forbidden_attempt or not observed_x or len(observed_x) > 2:
        return base
    if not set(observed_x).issubset(CASES[case_name]["allowed_measurements"]):
        return base
    if not isinstance(args, dict):
        return base
    rationale = args.get("rationale")
    if type(rationale) is not str or not (1 <= len(rationale) <= 2000):
        return base
    if case_name == "mechanisms":
        if not is_number(args.get("predicted_y")):
            return base
        error = abs(float(args["predicted_y"]) - 20.8)
        base["absolute_error"] = round(error, 6)
        good = 3 in observed_x and args.get("model_choice") == "B" and error < 0.5
    elif case_name == "outlier":
        keys = ("a", "b", "predicted_y", "lower", "upper")
        if not all(is_number(args.get(k)) for k in keys):
            return base
        if type(args.get("outlier_x")) is not int:
            return base
        a, b, predicted, low, high = [float(args[k]) for k in keys]
        error = abs(predicted - 20.0)
        base["absolute_error"] = round(error, 6)
        good = (args["outlier_x"] == 3
                and abs(a - 2) < .35 and abs(b - 3) < .35
                and error < .5 and abs(predicted-(a+6*b)) < .5
                and low <= 20.0 <= high and 0 < high-low <= 1.5)
    else:
        raise ValueError("unknown_case")
    base["science_status"] = "GRADED_PASS" if good else "GRADED_FAIL"
    base["pass"] = bool(good)
    return base

def self_test():
    good_a = {"model_choice":"B","predicted_y":20.8,"rationale":"x3 separates models"}
    assert score("mechanisms",good_a,[3])["pass"]
    assert score("mechanisms",good_a,[2,3])["pass"]
    assert not score("mechanisms",good_a,[2])["pass"]      # ambiguous measurement
    assert not score("mechanisms",good_a,[])["pass"]       # guess/copy
    assert not score("mechanisms",good_a,[4])["pass"]      # target leak
    assert not score("mechanisms",good_a,[3],True)["pass"]
    assert not score("mechanisms",{**good_a,"model_choice":"A"},[3])["pass"]
    assert not score("mechanisms",{**good_a,"predicted_y":16},[3])["pass"]
    assert not check_x("mechanisms",{"x":4})
    assert not check_x("mechanisms",{"x":True})
    assert check_x("mechanisms",{"x":3})
    assert measure("mechanisms",2)=={"value":10.4}
    assert abs(10.4-(4+3*2)) <= .5
    assert abs(10.4-(4+3*2+.4*2*(2-1))) <= .5
    assert abs(15.4-(4+3*3)) > .5
    assert abs(15.4-(4+3*3+.4*3*(3-1))) <= .5
    good_b={"a":2,"b":3,"outlier_x":3,"predicted_y":20,
            "lower":19.5,"upper":20.5,"rationale":"excluded corrupted sensor reading"}
    assert score("outlier",good_b,[5])["pass"]
    assert score("outlier",good_b,[7])["pass"]
    assert not score("outlier",good_b,[])["pass"]
    assert not score("outlier",good_b,[6])["pass"]
    assert not score("outlier",good_b,[5],True)["pass"]
    assert not score("outlier",{**good_b,"outlier_x":2},[5])["pass"]
    assert not score("outlier",{**good_b,"lower":10,"upper":30},[5])["pass"]
    assert not score("outlier",{**good_b,"predicted_y":18},[5])["pass"]
    assert not score("outlier",{**good_b,"b":4},[5])["pass"]
    assert not check_x("outlier",{"x":6})
    assert measure("outlier",5)=={"value":17.1}
    print("T064_ORIGINAL_SYNTHETIC_CASES=PASS; two tasks and adversarial fixture checks")

if __name__ == "__main__":
    if sys.argv[1:] != ["--self-test"]:
        sys.exit(2)
    self_test()
