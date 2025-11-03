"""
Feature encoder: converts raw telemetry dicts into numeric features (numpy/pandas friendly).
Keep it small and explicit for easy unit testing.
"""
from typing import Dict, List
import numpy as np
import pandas as pd

DEFAULT_FEATURE_ORDER = [
    "cpu_percent",
    "memory_percent",
    "disk_percent",
    "num_processes",
    "net_bytes_sent",
    "net_bytes_recv"
]

def telemetry_to_vector(record: Dict, feature_order: List[str] = DEFAULT_FEATURE_ORDER) -> np.ndarray:
    """Return a 1D numpy array of features in the specified order."""
    return np.array([float(record.get(k, 0.0)) for k in feature_order], dtype=float)

def batch_to_dataframe(records: List[Dict], feature_order: List[str] = DEFAULT_FEATURE_ORDER) -> pd.DataFrame:
    """Convert a list of telemetry dicts to a pandas DataFrame of features."""
    vectors = [telemetry_to_vector(r, feature_order) for r in records]
    return pd.DataFrame(vectors, columns=feature_order)
