# src/layer4_response_and_containment.py

import argparse
import json
import time
from src.utils.telemetry_collectors import stream_system_metrics
# We import L2 functions and L3 logic directly
from src.layer2_innate_detection import load_model, batch_to_dataframe 
from src.layer3_contextual_detection import analyze_context

MODEL_NAME = "innate_ocsvm"

def take_protective_action(contextual_status: str):
    """
    Layer 4: Simulates a response based on the L3 contextual status.
    """
    if contextual_status == "VIRAL_ALERT":
        # Viral-like threat requires rapid containment (sandboxing)
        print(f"\n[L4/RESPONSE] !!! HIGH SEVERITY: VIRAL_ALERT !!!")
        print("[L4/RESPONSE] ACTION: Initiating sandboxing and isolation of suspicious process...")
        time.sleep(0.1) # Simulate action
        print("[L4/RESPONSE] STATUS: Containment (Sandboxing) completed.")
        return True
    
    # Noise and NORMAL status require no action
    return False

def live_response_system():
    """
    Runs a live pipeline (L2, L3) and applies L4 response logic.
    """
    print("[layer4] Starting full detection & response system (L2, L3, L4)...")
    
    try:
        model = load_model(MODEL_NAME)
    except FileNotFoundError:
        print(f"[ERROR] Model file not found. Run layer2_innate_detection.py --train first.")
        return

    telemetry_stream = stream_system_metrics(poll_interval=1.0)
    print("[layer4] Monitoring system state... (L4 response logic armed)")
    
    for sample in telemetry_stream:
        # --- L2 Processing (Innate Detection) ---
        df_sample = batch_to_dataframe([sample])
        X_sample = df_sample.values
        score = model.decision_function(X_sample)[0]
        prediction = model.predict(X_sample)[0] 
        status = "ANOMALY" if prediction == -1 else "NORMAL"

        l2_output = {
            **sample, 
            "anomaly_score": score,
            "prediction": status
        }

        # --- L3 Processing (Contextual Analysis) ---
        l3_output = analyze_context(l2_output)
        
        # --- L4 Processing (Response and Containment) ---
        action_taken = take_protective_action(l3_output["L3_contextual_status"])
        
        # Add L4 status to output
        l3_output["L4_action_taken"] = action_taken
        
        # Print final status
        print(json.dumps(l3_output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Layer 4 - Response and Containment")
    parser.add_argument("--live", action="store_true", help="Run live detection and containment loop")
    args = parser.parse_args()
    
    if args.live:
        live_response_system()
    else:
        parser.print_help()