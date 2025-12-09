# src/layer3_contextual_detection.py

import argparse
import json
import time
from src.utils.telemetry_collectors import stream_system_metrics # type: ignore
from src.layer2_innate_detection import load_model, batch_to_dataframe # type: ignore

# Assume the OCSVM model name
MODEL_NAME = "innate_ocsvm"

def analyze_context(anomaly_data: dict) -> dict:
    """
    Layer 3: Provides contextual analysis (simple rule-based for PoC).
    Checks if an anomaly is associated with an immediate, short-lived high CPU spike.
    """
    score = anomaly_data.get("anomaly_score", 0)
    prediction = anomaly_data.get("prediction", "UNKNOWN")
    
    # Simple Contextual Rule: 
    # If Layer 2 flagged an anomaly BUT the raw CPU usage is still low (e.g., < 20%), 
    # we override the prediction to NORMAL, assuming the OCSVM threshold was too strict.
    # Otherwise, if the CPU is high AND it's an anomaly, we Escalate to Layer 4.
    
    cpu_percent = anomaly_data.get("cpu_percent", 0.0)

    if prediction == "ANOMALY":
        if cpu_percent < 20.0:
            # Low CPU, but OCSVM flagged it: Too strict threshold. Downgrade to 'NOISE'.
            contextual_status = "NOISE/TWEAK"
            escalation = False
        else:
            # High CPU AND OCSVM flagged: Potential threat. ESCALATE.
            contextual_status = "VIRAL_ALERT"
            escalation = True
    else:
        contextual_status = "NORMAL"
        escalation = False

    # Create the final, enriched output for Layer 4
    output = {
        "timestamp": anomaly_data["timestamp"],
        "L2_anomaly_score": round(float(score), 4),
        "L2_prediction": prediction,
        "L3_contextual_status": contextual_status,
        "L3_escalate_L4": escalation
    }
    return output


def live_context_detector():
    """
    Runs a live loop, streams data through L2, and applies L3 contextual rules.
    """
    print("[layer3] Starting contextual detection (L2 + L3)...")
    
    try:
        model = load_model(MODEL_NAME)
    except FileNotFoundError:
        print(f"[ERROR] Model file not found. Run layer2_innate_detection.py --train first.")
        return

    telemetry_stream = stream_system_metrics(poll_interval=1.0)
    print("[layer3] Streaming, Scoring (L2), and Contextualizing (L3)...")
    
    for sample in telemetry_stream:
        # --- L2 Processing ---
        df_sample = batch_to_dataframe([sample])
        X_sample = df_sample.values
        
        score = model.decision_function(X_sample)[0]
        prediction = model.predict(X_sample)[0] # 1 (normal) or -1 (anomaly)
        
        status = "ANOMALY" if prediction == -1 else "NORMAL"

        # Combine L1 raw data with L2 prediction for L3 analysis
        l2_output = {
            **sample, # Include all original metrics (including cpu_percent)
            "anomaly_score": score,
            "prediction": status
        }

        # --- L3 Processing ---
        l3_output = analyze_context(l2_output)
        
        # Log and print the final L3 decision
        print(json.dumps(l3_output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Layer 3 - Contextual Detection")
    parser.add_argument("--live", action="store_true", help="Run live contextual scoring loop")
    args = parser.parse_args()
    
    if args.live:
        live_context_detector()
    else:
        parser.print_help()