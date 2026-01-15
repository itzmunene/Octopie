"""
Layer 2: Innate Detection - simple One-Class SVM prototype.
REVISED: Training now consumes data collected by Layer 1.
"""
import argparse
import time
import json
from pathlib import Path
import joblib
import numpy as np
from sklearn.svm import OneClassSVM # type: ignore
# Assumed utility functions
from src.utils.feature_encoder import telemetry_to_vector, batch_to_dataframe
from src.utils.data_reader import read_telemetry_jsonl  # <--- NEW
from src.utils.telemetry_collectors import stream_system_metrics # Used for live mode data streaming
from src.utils.model_loader import save_model, load_model
from src.utils.logging_manager import log_event

MODEL_NAME = "innate_ocsvm"
MODEL_PATH = Path("models/innate_ocsvm.pkl")# Update: Data file should be the primary Layer 1 output file
DATA_FILE = Path("data/telemetry.jsonl") 

def load_innate_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Neural weights missing at {MODEL_PATH}")
    return joblib.load(MODEL_PATH)

def score_telemetry(model, sample):
    """Refactored to enforce feature alignment"""
    from src.utils.feature_encoder import batch_to_dataframe
    
    # 1. Convert the raw sample (6 features) to a DataFrame
    df_sample = batch_to_dataframe([sample])
    
    # 2. FILTER: Only keep the columns the model was trained on
    # This matches the ['cpu_percent', 'memory_percent'] used in Layer 5 training
    X_aligned = df_sample[['cpu_percent', 'memory_percent']]
    
    # 3. Score using only those 2 features
    score = model.decision_function(X_aligned.values)[0]
    pred = model.predict(X_aligned.values)[0]
    
    return score, "ANOMALY" if pred == -1 else "NORMAL"

def train_oneclass_svm(nu=0.05, kernel="rbf", gamma="scale"): # Removed 'records' argument
    # 1. Read the baseline data collected by Layer 1
    print(f"[layer2] Reading baseline data from {DATA_FILE}...")
    records = read_telemetry_jsonl(DATA_FILE) 
    
    if not records:
        raise SystemExit("No baseline data found. Run layer1_signal_acquisition.py first.")

    # 2. Train the model
    import pandas as pd
    df = batch_to_dataframe(records)
    X = df.values
    model = OneClassSVM(nu=nu, kernel=kernel, gamma=gamma) # type: ignore
    model.fit(X)
    save_model(model, MODEL_NAME)
    print(f"[layer2] Trained One-Class SVM on {len(records)} samples and saved as {MODEL_NAME}")
    return model

# ... (score_sample function remains the same) ...

# ... (live_mode function remains the same, still collecting data for PoC simplicity) ...
def live_mode():
    """
    Runs a live loop, collecting new metrics and scoring them instantly
    using the trained OCSVM model.
    """
    print(f"[layer2] Starting live detection using model: {MODEL_NAME}...")
    
    try:
        # Load the saved model
        model = load_model(MODEL_NAME)
    except FileNotFoundError:
        print(f"[ERROR] Model file not found at {MODEL_PATH}. Run with --train first.")
        return

    # Use the generator function imported from telemetry_collectors
    telemetry_stream = stream_system_metrics(poll_interval=1.0) 
    
    print("[layer2] Streaming and Scoring Live Data (Ctrl+C to stop)...")

    for sample in telemetry_stream:
        # 1. Convert the single sample to a feature vector (X)
        # FIX: Use the confirmed working batch_to_dataframe function
        # It handles converting a list of dicts ([sample]) into a DataFrame 
        # and then extracts the 2D numpy array required by Scikit-learn.
        df_sample = batch_to_dataframe([sample])
        X_sample = df_sample.values
        
        # 2. Score the sample using the OCSVM model
        score = model.decision_function(X_sample)[0]
        prediction = model.predict(X_sample)[0] # 1 (normal) or -1 (anomaly)
        
        # 3. Format and print the detection output
        status = "ANOMALY" if prediction == -1 else "NORMAL"
        
        output = {
            "timestamp": sample.get("timestamp"),
            "anomaly_score": round(float(score), 4),
            "prediction": status,
            "raw_prediction_value": int(prediction)
        }
        
        # Log and print the event
        print(json.dumps(output))


# ... (all imports, global variables, and function definitions: 
#      train_oneclass_svm and live_mode) ...

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Layer 2 - Innate Detection (One-Class SVM)")
    parser.add_argument("--train", action="store_true", help="Train model using data collected by Layer 1")
    parser.add_argument("--live", action="store_true", help="Run live scoring loop")
    args = parser.parse_args()
    
    # ------------------------------------------------
    # CORRECT CONTROL FLOW BLOCK
    # ------------------------------------------------
    if args.train:
        train_oneclass_svm() # No more arguments needed
    elif args.live:
        live_mode()  # type: ignore
    else:
        parser.print_help()