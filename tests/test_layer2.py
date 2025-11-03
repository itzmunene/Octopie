import os
import json
import tempfile
from src.utils.feature_encoder import telemetry_to_vector
from src.layer2_innate_detection import train_oneclass_svm, collect_baseline
from src.utils.telemetry_collectors import collect_basic_system_metrics

def test_feature_encoder_vector_shape():
    sample = collect_basic_system_metrics()
    vec = telemetry_to_vector(sample)
    assert vec.shape[0] >= 1

def test_training_runs(tmp_path):
    # collect a few synthetic baseline samples (use local collector)
    recs = [collect_basic_system_metrics() for _ in range(10)]
    model = train_oneclass_svm(recs, nu=0.1)
    # basic smoke test: model has fit method
    assert hasattr(model, "predict")
