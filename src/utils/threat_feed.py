# src/utils/threat_feed.py

import requests
from src.database.hybrid_store import store

def update_threat_signatures():
    """
    Simulated Threat Feed. In production, this fetches from 
    external APIs (e.g., MalwareBazaar, Abuse.ch).
    """
    print("[L0/FEED] Syncing with global threat intelligence...")
    
    # Mock data for testing (Replace with API call)
    mock_threats = [
        {"hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "name": "EmptyFile_Test"},
        {"hash": "cf23df2207d99a74fbe169e3eba035e633b65d94", "name": "Mock_Exploit_X"}
    ]
    
    for threat in mock_threats:
        store.add_malware_hash(threat['hash'], threat['name'], "Octopie_Global_Feed")
    
    print(f"[L0/FEED] Sync complete. {len(mock_threats)} signatures added/verified.")

if __name__ == "__main__":
    update_threat_signatures()