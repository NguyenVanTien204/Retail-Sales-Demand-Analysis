"""Minimal route definitions for the forecasting API demo."""
from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from Dashboard.services import predictor

from . import dependencies as deps
from .schemas import PredictionRequest, PredictionResponse
from .utils import filter_by_date, frame_to_records, parse_date, records_to_dataframe

router = APIRouter()


def _build_features_for_inference(df: pd.DataFrame) -> pd.DataFrame:
    """Xây dựng ma trận đặc trưng từ dataframe đầu vào."""
    mapping = deps.get_encoding_mapping()
    try:
        return predictor.build_feature_matrix_for_inference(df, mapping)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _build_features_with_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Xây dựng ma trận đặc trưng và chuỗi mục tiêu từ dataframe đầu vào."""
    mapping = deps.get_encoding_mapping()
    try:
        return predictor.build_feature_matrix(df, mapping)
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _select_dataframe(payload: PredictionRequest) -> pd.DataFrame:
    """Chọn dataframe để sử dụng cho dự đoán dựa trên payload đầu vào."""
    if payload.records:
        try:
            return records_to_dataframe(payload.records)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    try:
        start = parse_date(payload.start_date)
        end = parse_date(payload.end_date)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    df = filter_by_date(deps.get_test_dataframe(), start, end)
    if payload.limit is not None:
        df = df.tail(payload.limit)
    if df.empty:
        raise HTTPException(status_code=400, detail="No rows available for prediction")
    return df



# route chính
@router.get("/")
def root() -> Dict[str, Any]:
    return {
        "message": "Welcome to the Retail Demand Forecasting API",
        "docs": "/docs",
        "model": deps.MODEL_VARIANT,
    }

# route kiểm tra kết nối
@router.get("/health")
def healthcheck() -> Dict[str, Any]:
    return {"status": "ok"}

# route tóm tắt dữ liệu
@router.get("/data/summary")
def data_summary() -> Dict[str, Any]:
    """Trả về tóm tắt dữ liệu test bao gồm số hàng, cột và phạm vi ngày."""
    try:
        df = deps.get_test_dataframe()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    date_min: Optional[pd.Timestamp] = df["date_id"].min() if "date_id" in df.columns else None
    date_max: Optional[pd.Timestamp] = df["date_id"].max() if "date_id" in df.columns else None
    return {
        "rows": int(df.shape[0]),
        "columns": df.columns.tolist(),
        "date_min": date_min.isoformat() if pd.notna(date_min) else None,
        "date_max": date_max.isoformat() if pd.notna(date_max) else None,
        "feature_columns": predictor.FEATURE_COLUMNS,
        "target_column": predictor.TARGET_COLUMN,
    }

# route lấy mẫu dữ liệu
@router.get("/data/sample")
def data_sample(
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
) -> Dict[str, Any]:
    """Trả về mẫu dữ liệu test với các bộ lọc tùy chọn."""
    try:
        df = deps.get_test_dataframe()
    except:
        print("Loi chuyen doi dataframe")
    try:
        start = parse_date(start_date)
        end = parse_date(end_date)
    except:
        print("Loi ngay thang")

    filtered = filter_by_date(df, start, end)
    sample_df = filtered.tail(limit)
    return {"rows": int(sample_df.shape[0]), "data": frame_to_records(sample_df)}


# route dự đoán
@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    """Thực hiện dự đoán dựa trên payload đầu vào."""
    df = _select_dataframe(payload)
    features = _build_features_for_inference(df)
    model = deps.get_model()
    predictions = model.predict(features)
    return PredictionResponse(
        rows=int(features.shape[0]),
        model=deps.MODEL_VARIANT,
        predictions=predictions.tolist(),
    )
