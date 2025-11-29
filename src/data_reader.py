import json
from pathlib import Path

def read_telemetry_jsonl(file_path: Path) -> list:
    """
    Reads records from a JSON Lines (.jsonl) file, where each line is a JSON object.
    This is used to load data saved by Layer 1.
    """
    records = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Safely parse each line as a JSON object
                records.append(json.loads(line))
        print(f"[data_reader] Loaded {len(records)} records from {file_path}")
    except FileNotFoundError:
        print(f"[data_reader] Error: Telemetry file not found at {file_path}")
    except json.JSONDecodeError as e:
        print(f"[data_reader] Error decoding JSON line: {e}")
    return records
