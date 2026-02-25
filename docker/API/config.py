"""Static paths shared across the FastAPI service."""
from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "Dashboard" / "data"
MODEL_DIR = ROOT_DIR / "model"

TEST_DATA_PATH = DATA_DIR / "test_data.parquet"
ENCODING_PATH = DATA_DIR / "target_encoding_mapping.json"
LGBM_PATH = MODEL_DIR / "lgbm_model.joblib"
XGB_PATH = MODEL_DIR / "xgboost_model.joblib"
