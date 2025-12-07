"""
Layer 1: Signal Acquisition & Preprocessing
Basic CLI: either stream to stdout or write to data/telemetry.jsonl
"""
import argparse
import json
from numpy import record
import pandas as pd
from ydata_profiling import ProfileReport
from pathlib import Path
from src.utils.telemetry_collectors import stream_system_metrics # type: ignore 
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
    

# Conceptual function to be used by layer2_innate_detection.py
def read_telemetry_jsonl(file_path: Path):
    """Reads records from a JSON Lines file, safely skipping corrupted lines."""
    records = [] 
    try:
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                try:
                    # Attempt to load the JSON line
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    # If a line is corrupted, print a warning and skip it
                    print(f"[data_reader] Skipping corrupted line {i+1} in {file_path}. Error: {e}")
                    continue # Skip to the next line
    except FileNotFoundError:
        print(f"[data_reader] Error: Telemetry file not found at {file_path}")
    return records

def run_profiler():
    """Reads the collected telemetry data and generates a detailed HTML profile report."""
    file_path = DATA_DIR / "telemetry.jsonl"
    print(f"[profiler] Reading data from {file_path} for profiling...")
    
    # Use the utility function to load records
    records = read_telemetry_jsonl(file_path)
    
    if not records:
        print("[profiler] Error: No data found to profile. Run acquisition first.")
        return

    # Convert records to a DataFrame
    # Note: Using pandas DataFrame conversion requires the 'telemetry' data to be consistent.
    df = pd.DataFrame(records)
    
    # Drop timestamp for profiling to avoid high cardinality warnings
    df = df.drop(columns=['timestamp'])
    
    print(f"[profiler] Generating profile report on {len(df)} samples...")
    profile = ProfileReport(df, title="Telemetry Baseline Profile", minimal=True)
    
    output_path = DATA_DIR / "telemetry_profile.html"
    profile.to_file(output_path)
    print(f"[profiler] Report saved successfully to {output_path.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run telemetry collector (Layer 1)")
    parser.add_argument("--interval", type=float, default=1.0, help="poll interval in seconds")
    parser.add_argument("--no-write", dest="write_file", action="store_false", help="do not write to data file")
    
        # NEW ARGUMENT: --profile
    parser.add_argument("--profile", action="store_true", help="Generate ydata-profiling report on baseline data and exit")
    
    args = parser.parse_args()

    if args.profile:
        run_profiler() # Call the new profiler function
    else:
        # This is your existing run_collector logic
        run_collector(poll_interval=args.interval, write_file=args.write_file)
