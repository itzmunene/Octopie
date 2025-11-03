"""
Very small helper to save / load scikit-learn models.
"""
import joblib
from pathlib import Path

MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

def save_model(model, name: str):
    path = MODEL_DIR / f"{name}.joblib"
    joblib.dump(model, path)
    return path

def load_model(name: str):
    path = MODEL_DIR / f"{name}.joblib"
    if not path.exists():
        raise FileNotFoundError(f"Model {name} not found at {path}")
    return joblib.load(path)
