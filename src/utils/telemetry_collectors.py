import psutil # type: ignore
import time
from datetime import datetime
import json

def collect_resource_telemetry(interval=5):
    """
    Collects system-wide CPU and Memory usage.
    """
    # 1. Collect System-wide Metrics
    cpu_percent = psutil.cpu_percent(interval=None) # Non-blocking call for immediate data
    mem_percent = psutil.virtual_memory().percent
    
    # 2. Collect Process-specific Metrics (Top 5 CPU users)
    process_data = []
    pids = psutil.pids()
    processes = []
    for pid in pids:
        try:
            p = psutil.Process(pid)
            processes.append({
                'pid': p.pid,
                'name': p.name(),
                'cpu_percent': p.cpu_percent(interval=None),
                'memory_percent': p.memory_percent(),
                'status': p.status()
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort and take the top 5 processes by CPU usage for context
    top_processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    
# 3. Create the Telemetry Data Object
    telemetry_record = {
        'timestamp': datetime.now().isoformat(),
        'system_cpu_total_percent': cpu_percent,
        'system_memory_used_percent': mem_percent,
        'process_count_total': len(pids),
        'top_processes': top_processes
    }
    
    return telemetry_record

# live data streaming generator for Layer 1 testing
def stream_system_metrics(poll_interval=1.0):
    """
    A generator that continuously collects telemetry and yields it.
    This is what Layer 1 uses to stream data.
    """
    while True:
        # Use the single-shot collector function you defined
        record = collect_resource_telemetry()
        
        # Log and yield the record
        # Note: We are using a simplified version of the data structure 
        # that was in the Layer 1 run output for now.
        simplified_record = {
            "cpu_percent": record["system_cpu_total_percent"],
            "memory_percent": record["system_memory_used_percent"],
            "num_processes": record["process_count_total"],
            "timestamp": time.time() # Use simple time.time() for faster serialization
        }
        
        yield simplified_record
        time.sleep(poll_interval)