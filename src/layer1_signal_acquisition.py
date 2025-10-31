# Signal acquisition module for preprocessing system telemetry data
import psutil
import time
import json

def collect_system_metrics():
    """Collects basic system telemetry."""
    metrics = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "network_io": psutil.net_io_counters()._asdict()
    }
    return metrics

if __name__ == "__main__":
    while True:
        data = collect_system_metrics()
        print(json.dumps(data, indent=2))
        time.sleep(5)
