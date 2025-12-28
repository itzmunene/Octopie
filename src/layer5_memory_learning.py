# src/layer5_memory_learning.py (Refined for Hybrid DB)

import pandas as pd
from sklearn.svm import OneClassSVM
import joblib
from src.database.hybrid_store import store

MODEL_PATH = "models/innate_ocsvm.pkl"

def evolve_from_memory():
    print("[L5/EVOLUTION] Querying hybrid database for verified benign patterns...")
    
    # Query the store for the latest 500 'Normal' events
    batch = store.get_learning_batch(limit=500)
    
    if len(batch) < 20:
        print("[L5/EVOLUTION] Memory too shallow. Need more experience to evolve.")
        return

    # Convert to DataFrame for training
    df_learning = pd.DataFrame(batch, columns=['cpu_percent', 'memory_percent'])
    
    print(f"[L5/EVOLUTION] Integrating {len(df_learning)} experiences into the Innate Model...")
    
    # Retrain (or adapt) the model
    new_model = OneClassSVM(gamma='auto', nu=0.05)
    new_model.fit(df_learning)
    
    # Update the 'Nervous System'
    joblib.dump(new_model, MODEL_PATH)
    print("[L5/EVOLUTION] System has evolved. New neural weights deployed to L2.")

if __name__ == "__main__":
    evolve_from_memory()