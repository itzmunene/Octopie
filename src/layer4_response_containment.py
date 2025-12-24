# src/layer4_response_containment.py (Updated with Cooldown)

import argparse
import json
import time
from src.utils.telemetry_collectors import stream_system_metrics
from src.layer2_innate_detection import load_model, batch_to_dataframe 
from src.layer3_contextual_detection import analyze_context

MODEL_NAME = "innate_ocsvm"

# State tracking for cooldown
last_action_time = 0
COOLDOWN_SECONDS = 10 # Only act once every 10 seconds for the same threat

def take_protective_action(contextual_status: str):
    global last_action_time
    current_time = time.time()
    
    if contextual_status == "VIRAL_ALERT":
        # Check if we are in cooldown
        if current_time - last_action_time < COOLDOWN_SECONDS:
            return "COOLDOWN_ACTIVE"
            
        print(f"\n[L4/RESPONSE] !!! HIGH SEVERITY: VIRAL_ALERT !!!")
        print("[L4/RESPONSE] ACTION: Initiating sandboxing and isolation...")
        time.sleep(0.1) 
        print("[L4/RESPONSE] STATUS: Containment completed.")
        
        last_action_time = current_time
        return "ACTION_TAKEN"
    
    return "NO_ACTION_REQUIRED"

def live_response_system():
    print("[layer4] Starting refined detection & response (Cooldown Enabled)...")
    
    try:
        model = load_model(MODEL_NAME)
    except FileNotFoundError:
        print(f"[ERROR] Model file not found.")
        return

    telemetry_stream = stream_system_metrics(poll_interval=1.0)
    
    for sample in telemetry_stream:
        # L2 & L3 Logic
        df_sample = batch_to_dataframe([sample])
        score = model.decision_function(df_sample.values)[0]
        prediction = model.predict(df_sample.values)[0] 
        l2_output = {**sample, "anomaly_score": score, "prediction": "ANOMALY" if prediction == -1 else "NORMAL"}
        l3_output = analyze_context(l2_output)
        
        # L4 Refined Response
        response_result = take_protective_action(l3_output["L3_contextual_status"])
        
        # Enrich log
        l3_output["L4_response_result"] = response_result
        print(json.dumps(l3_output))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    if args.live: live_response_system()