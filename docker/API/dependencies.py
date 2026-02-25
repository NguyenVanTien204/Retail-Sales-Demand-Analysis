"""Cached loaders for artifacts and prepared data."""
from __future__ import annotations

import json
import os
from contextlib import suppress
from functools import lru_cache
from typing import Any, Dict

import joblib
import pandas as pd

from .API import config
from .utils import ensure_artifact

MODEL_VARIANT = os.getenv("MODEL_VARIANT", "lightgbm").lower()
SUPPORTED_MODELS = {"lightgbm", "xgboost"}


@lru_cache()
def get_test_dataframe() -> pd.DataFrame:
    """tải dataframe test đã được chuẩn bị trước từ đĩa."""
    ensure_artifact(config.TEST_DATA_PATH)
    df = pd.read_parquet(config.TEST_DATA_PATH)
    if "date_id" in df.columns:
        df["date_id"] = pd.to_datetime(df["date_id"], errors="coerce")
    return df.sort_values("date_id").reset_index(drop=True)


@lru_cache()
def get_encoding_mapping() -> Dict[str, Any]:
    """Tải encoding từ đĩa."""
    ensure_artifact(config.ENCODING_PATH)
    with config.ENCODING_PATH.open("r", encoding="utf-8") as source:
        return json.load(source)


@lru_cache()
def _load_lightgbm_model() -> Any:
    """Tải mô hình LightGBM từ đĩa."""
    ensure_artifact(config.LGBM_PATH)
    return joblib.load(config.LGBM_PATH)


@lru_cache()
def _load_xgboost_model() -> Any:
    """Tải mô hình XGBoost từ đĩa và cấu hình để sử dụng CPU predictor."""
    ensure_artifact(config.XGB_PATH)
    model = joblib.load(config.XGB_PATH)
    with suppress(Exception):
        import xgboost as xgb

        if hasattr(model, "set_params"):
            with suppress(TypeError, ValueError):
                model.set_params(predictor="cpu_predictor")
            with suppress(TypeError, ValueError):
                model.set_params(device="cpu")
        booster = None
        if hasattr(model, "get_booster"):
            booster = model.get_booster()
        if booster is None and isinstance(model, xgb.Booster):
            booster = model
        if booster is not None:
            booster.set_param({"predictor": "cpu_predictor", "device": "cpu"})
    return model


@lru_cache()
def get_model() -> Any:
    if MODEL_VARIANT not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported MODEL_VARIANT: {MODEL_VARIANT}")
    if MODEL_VARIANT == "lightgbm":
        return _load_lightgbm_model()
    return _load_xgboost_model()
