"""
Simple telemetry collectors that read basic system metrics.
Extend these to add OS-specific telemetry or kernel hooks.
"""
import psutil # type: ignore
import time
from typing import Dict

def collect_basic_system_metrics() -> Dict:
    """Collect a basic snapshot of system telemetry."""
    net = psutil.net_io_counters()
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": mem.percent,
        "disk_percent": disk.percent,
        "num_processes": len(psutil.pids()),
        "net_bytes_sent": net.bytes_sent,
        "net_bytes_recv": net.bytes_recv,
        "timestamp": time.time()
    }

def stream_system_metrics(poll_interval: float = 1.0):
    """Generator that yields telemetry dictionaries every poll_interval seconds."""
    while True:
        yield collect_basic_system_metrics()
        time.sleep(poll_interval)

