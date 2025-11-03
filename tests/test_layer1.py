import pytest
from src.utils.telemetry_collectors import collect_basic_system_metrics

def test_collect_metrics_returns_dict():
    out = collect_basic_system_metrics()
    assert isinstance(out, dict)
    assert "cpu_percent" in out
    assert "memory_percent" in out
