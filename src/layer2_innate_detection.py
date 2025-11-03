"""
Layer 2: Innate Detection - simple One-Class SVM prototype.
This script demonstrates:
 - building a small baseline (collect N samples)
 - training a one-class SVM on baseline
 - scoring new samples and flagging anomalies
"""
import argparse
import time
import json
from pathlib import Path
import numpy as np
from sklearn.svm import OneClassSVM # type: ignore
from src.utils.feature_encoder import telemetry_to_vector, batch_to_dataframe
from src.utils.telemetry_collectors import collect_basic_system_metrics
from src.utils.model_loader import save_model, load_model
from src.utils.logging_manager import log_event

MODEL_NAME = "innate_ocsvm"
MODEL_PATH = Path("models") / f"{MODEL_NAME}.joblib"
DATA_FILE = Path("data/telemetry_baseline.jsonl")
DATA_FILE.parent.mkdir(exist_ok=True)

def collect_baseline(n: int = 50, interval: float = 0.5):
    print(f"[layer2] Collecting baseline ({n} samples)...")
    samples = []
    for _ in range(n):
        s = collect_basic_system_metrics()
        samples.append(s)
        # persist
        with open(DATA_FILE, "a") as f:
            f.write(json.dumps(s) + "\n")
        time.sleep(interval)
    print("[layer2] Baseline collection complete.")
    return samples

def train_oneclass_svm(records, nu=0.05, kernel="rbf", gamma="scale"):
    import pandas as pd
    df = batch_to_dataframe(records)
    X = df.values
    model = OneClassSVM(nu=nu, kernel=kernel, gamma=gamma) # type: ignore
    model.fit(X)
    save_model(model, MODEL_NAME)
    print(f"[layer2] Trained One-Class SVM and saved as {MODEL_NAME}")
    return model

def score_sample(model, sample):
    vec = telemetry_to_vector(sample).reshape(1, -1)
    pred = model.predict(vec)  # +1 normal, -1 outlier
    score = float(model.decision_function(vec).ravel()[0])
    return {"prediction": int(pred[0]), "score": score}

def live_mode(poll_interval: float = 1.0):
    if not MODEL_PATH.exists():
        raise SystemExit("Model not found. Run --train to create baseline model first.")
    model = load_model(MODEL_NAME)
    print("[layer2] Running live scoring. Press Ctrl+C to stop.")
    try:
        while True:
            sample = collect_basic_system_metrics()
            res = score_sample(model, sample)
            out = {"sample": sample, "detection": res}
            print(json.dumps(out))
            log_event(out, filename="innate_detections.log")
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("[layer2] Stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Layer 2 - Innate Detection (One-Class SVM)")
    parser.add_argument("--train", action="store_true", help="Collect baseline and train model")
    parser.add_argument("--samples", type=int, default=60, help="Baseline sample count")
    parser.add_argument("--interval", type=float, default=0.5, help="Baseline sample interval")
    parser.add_argument("--live", action="store_true", help="Run live scoring loop")
    args = parser.parse_args()

    if args.train:
        recs = collect_baseline(args.samples, args.interval)
        train_oneclass_svm(recs)
    elif args.live:
        live_mode()
    else:
        parser.print_help()
