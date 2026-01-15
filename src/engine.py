# src/engine.py
import time
from src.utils.telemetry_collectors import stream_system_metrics
from src.layer2_innate_detection import load_innate_model, score_telemetry
from src.layer3_contextual_detection import analyze_context
from src.layer4_response_containment import take_protective_action
from src.layer5_memory_learning import record_enterprise_state
from src.database.hybrid_store import store

def run_autonomous_engine():
    print("--- [OCTOPIE] AUTONOMOUS ENGINE STARTING ---")
    
    # 1. Initialize the Neural Weights (L2)
    try:
        model = load_innate_model()
    except Exception as e:
        print(f"[ERROR] Engine could not load L2 model: {e}")
        return

    # 2. Start the Sensory Stream (L1)
    telemetry_stream = stream_system_metrics(poll_interval=1.0)

    for sample in telemetry_stream:
        # A. Instinct Phase (L2)
        score, prediction = score_telemetry(model, sample)
        
        # B. Reasoning Phase (L3)
        l2_data = {**sample, "anomaly_score": score, "prediction": prediction}
        l3_report = analyze_context(l2_data)
        
        # C. Reflex Phase (L4)
        response = take_protective_action(l3_report["L3_contextual_status"])
        
        # D. Memory Phase (L5)
        # This populates the SQLite DB that the FastAPI Synapse reads
        record_enterprise_state(l3_report, response)
        
        # Pulse check for terminal
        print(f"[HEARTBEAT] Score: {round(score, 2)} | Status: {l3_report['L3_contextual_status']}")

if __name__ == "__main__":
    run_autonomous_engine()

def record_enterprise_state(l3_context, l4_response):
    event_packet = {
        **l3_context,
        "action_taken": l4_response # Maps L4 reflex to the ledger
    }
    store.commit_event(event_packet)
    print(f"📖 [L5] Event Archived to Ledger.")