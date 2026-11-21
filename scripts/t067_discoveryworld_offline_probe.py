#!/usr/bin/env python3
"""T0.67 pinned DiscoveryWorld read-only/offline engine probe. NO Gemini/API."""
import json
import os
import shutil
import sys
import time

SCENARIO = "Small Skills: Instrument Measurement Test"
DIFFICULTY = "Normal"
SEED = 0

def deep_keys(obj, seen):
    if isinstance(obj, dict):
        for key, value in obj.items():
            seen.add(str(key))
            deep_keys(value, seen)
    elif isinstance(obj, list):
        for value in obj:
            deep_keys(value, seen)

def main():
    start=time.monotonic()
    api=None
    os.environ["SDL_VIDEODRIVER"]="dummy"
    os.environ["SDL_AUDIODRIVER"]="dummy"
    try:
        from discoveryworld.DiscoveryWorldAPI import DiscoveryWorldAPI
        api=DiscoveryWorldAPI(threadID=67)
        ok=api.loadScenario(scenarioName=SCENARIO,difficultyStr=DIFFICULTY,
                            randomSeed=SEED,numUserAgents=1)
        if not ok:
            raise RuntimeError("scenario_load_rejected")
        t_obs=time.monotonic()
        observation=api.getAgentObservation(agentIdx=0)
        observation_duration=time.monotonic()-t_obs
        ui=observation.get("ui")
        vision=observation.get("vision")
        errors=observation.get("errors")
        if not isinstance(ui,dict) or not isinstance(vision,dict):
            raise RuntimeError("observation_shape")
        if errors:
            raise RuntimeError("observation_errors")
        keys=set()
        deep_keys(ui,keys)
        leaked=bool(keys & {"scoreCard","criticalQuestions","criticalHypotheses",
                            "scoreNormalized","completedSuccessfully","gold"})
        score=api.getTaskScorecard()
        if score is None:
            raise RuntimeError("missing_scorecard")
        size=len(json.dumps(ui,separators=(",",":"),default=str))
        image_lengths=[len(v) for v in vision.values() if isinstance(v,str)]
        result={"protocol":"T0.67", "status":"PASS" if not leaked else "FAIL",
                "scenario":"unit_instrument_measurement","difficulty":DIFFICULTY,"seed":SEED,
                "ui_keys_count":len(keys),"ui_json_bytes":size,
                "task_progress_present":"taskProgress" in keys,
                "oracle_keys_leaked_to_ui":leaked,
                "scorecard_available":True,
                "vision_base64_fields":len(image_lengths),
                "vision_base64_total_chars":sum(image_lengths),
                "first_observation_seconds":round(observation_duration,3),
                "start_to_observation_seconds":round(time.monotonic()-start,3)}
        print(json.dumps(result,separators=(",",":"),sort_keys=True))
        return 0 if result["status"]=="PASS" and result["task_progress_present"] else 1
    except ModuleNotFoundError:
        print('{"protocol":"T0.67","status":"FAIL","category":"missing_dependency"}')
        return 1
    except Exception:
        # No raw exception from third-party data (avoid exposing task/gold/content).
        print('{"protocol":"T0.67","status":"FAIL","category":"runtime_or_observation_error"}')
        return 1
    finally:
        if api is not None:
            shutil.rmtree(api.FRAME_DIR,ignore_errors=True)

if __name__=="__main__":
    sys.exit(main())
