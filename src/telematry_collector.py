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
    
    