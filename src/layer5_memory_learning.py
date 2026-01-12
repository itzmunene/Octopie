# src/layer5_memory_learning.py

import pandas as pd
from sklearn.svm import OneClassSVM
import joblib
from src.database.hybrid_store import store

MODEL_PATH = "models/innate_ocsvm.pkl"

def evolve_from_memory():
    # Only pull the specific features the SVM understands
    batch = store.get_learning_batch(limit=500) 
    
    if not batch or len(batch) < 20:
        return "[L5] Not enough data."

    # Force feature alignment
    df_learning = pd.DataFrame(batch)[['cpu_percent', 'memory_percent']]
    
    new_model = OneClassSVM(gamma='auto', nu=0.05)
    new_model.fit(df_learning.values)
    
    # Save using the unified .pkl path variable
    joblib.dump(new_model, MODEL_PATH) 
    print(f"[L5] Neural Evolution Complete. Weights saved to {MODEL_PATH}")

if __name__ == "__main__":
    evolve_from_memory()


from src.database.hybrid_store import store

def record_enterprise_state(l3_context, l4_response):
    """
    This is the function that POPULATES the DB.
    It takes the contextual status and the response taken to create a record.
    """
    # Create the final payload for the database
    # l3_context usually contains: cpu_percent, memory_percent, anomaly_score, context_status
    
    event_packet = {
        **l3_context,
        "L4_response_status": l4_response
    }
    
    # COMMIT to the Hybrid Store
    store.commit_event(event_packet) # type: ignore
    
    # Visual feedback in the terminal
    status = l3_context.get('L3_contextual_status', 'UNKNOWN')
    print(f"[L5/LEDGER] Experience Archived: {status} | Action: {l4_response}")

# Example usage in the live loop:
# record_enterprise_state(context_results, "SANDBOX_INITIATED")