from pathlib import Path
import json

# Define the base data directory here (or ensure it's imported)
DATA_DIR = Path("data") 

def log_event(record: dict, filename: str):
    """
    Writes a single record as a JSON line to the specified file in the DATA_DIR.
    """
    # 1. Construct the full path: data/telemetry.jsonl
    file_path = DATA_DIR / filename
    
    # 2. Open the file in APPEND mode ('a') and ensure it uses UTF-8 encoding
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            # 3. Dump the record as a JSON string and add a NEWLINE character
            json_line = json.dumps(record)
            f.write(json_line + '\n')
    except Exception as e:
        print(f"[ERROR: logging_manager] Failed to write to {file_path}. Error: {e}")