"""
Layer 2: Innate Detection - simple One-Class SVM prototype.
REVISED: Training now consumes data collected by Layer 1.
"""
import argparse
import time
import json
from pathlib import Path
import numpy as np
from sklearn.svm import OneClassSVM # type: ignore
# Assumed utility functions
from src.utils.feature_encoder import telemetry_to_vector, batch_to_dataframe
from src.utils.data_reader import read_telemetry_jsonl  # <--- NEW
from src.utils.telemetry_collectors import collect_basic_system_metrics # Keep this for live mode simplicity for now
from src.utils.model_loader import save_model, load_model
from src.utils.logging_manager import log_event

MODEL_NAME = "innate_ocsvm"
MODEL_PATH = Path("models") / f"{MODEL_NAME}.joblib"
# Update: Data file should be the primary Layer 1 output file
DATA_FILE = Path("data/telemetry.jsonl") 

# Function Removed: collect_baseline is no longer in Layer 2.

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Layer 2 - Innate Detection (One-Class SVM)")
    parser.add_argument("--train", action="store_true", help="Train model using data collected by Layer 1")
    # Removed: --samples and --interval arguments
    parser.add_argument("--live", action="store_true", help="Run live scoring loop")
    args = parser.parse_args()

    if args.train:
        train_oneclass_svm() # No more arguments needed
    elif args.live:
        live_mode()
    else:
        parser.print_help()