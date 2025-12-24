# src/layer5_memory_learning.py

import json
import pandas as pd
from sklearn.svm import OneClassSVM
import joblib

LEDGER_FILE = "logs/executive_audit_ledger.jsonl"
MODEL_PATH = "models/innate_ocsvm.pkl"

def evolutionary_update():
    """
    Layer 5: Memory & Learning.
    Consumes the ledger to refine the Innate Detection (L2) model.
    """
    print("[L5/LEARNING] Accessing Long-Term Memory (Ledger)...")
    
    events = []
    try:
        with open(LEDGER_FILE, "r") as f:
            for line in f:
                events.append(json.loads(line))
    except FileNotFoundError:
        print("[L5/LEARNING] No memory found. Evolution suspended.")
        return

    # Filter for events that were classified as 'NORMAL' or 'NOISE/TWEAK'
    # These are our 'New Truths' to learn from.
    df = pd.DataFrame(events)
    learning_pool = df[df['L3_contextual_status'].isin(['NORMAL', 'NOISE/TWEAK'])]

    if len(learning_pool) < 10:
        print("[L5/LEARNING] Insufficient new data to guarantee stable learning.")
        return

    print(f"[L5/LEARNING] Retraining Innate Model with {len(learning_pool)} new contextually-verified samples...")
    
    # Extract raw features used in L1/L2
    features = ['cpu_percent', 'memory_percent', 'net_io_sent', 'net_io_recv']
    X_new = learning_pool[features]

    # Federated/Incremental Update Logic (Simulated)
    # In a full implementation, we would use partial_fit or an Incremental Learner
    new_model = OneClassSVM(gamma='auto', nu=0.05)
    new_model.fit(X_new)

    # Save the evolved model
    joblib.dump(new_model, MODEL_PATH)
    print("[L5/LEARNING] Evolution complete. L2 model has been updated with new memory.")

if __name__ == "__main__":
    evolutionary_update()