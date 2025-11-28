"""
Layer 1: Signal Acquisition & Preprocessing
Basic CLI: either stream to stdout or write to data/telemetry.jsonl
"""
import argparse
import json
from pathlib import Path
from src.utils.telemetry_collectors import stream_system_metrics
from src.utils.logging_manager import log_event

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def run_collector(poll_interval: float = 1.0, write_file: bool = True):
    gen = stream_system_metrics(poll_interval=poll_interval)
    for i, sample in enumerate(gen):
        # write to file for downstream consumption
        if write_file:
            log_event(sample, filename="telemetry.jsonl")
        print(json.dumps(sample))
        if i and i >= 9999:
            break  # safety guard

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run telemetry collector (Layer 1)")
    parser.add_argument("--interval", type=float, default=1.0, help="poll interval in seconds")
    parser.add_argument("--no-write", dest="write_file", action="store_false", help="do not write to data file")
    args = parser.parse_args()
    run_collector(poll_interval=args.interval, write_file=args.write_file)

# Conceptual function to be used by layer2_innate_detection.py
def read_telemetry_jsonl(file_path: Path):
    """Reads records from a JSON Lines file."""
    records = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                records.append(json.loads(line))
    except FileNotFoundError:
        print(f"Error: Telemetry file not found at {file_path}")
    return records