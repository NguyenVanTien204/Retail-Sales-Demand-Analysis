"""Utility helpers for parsing dates and shaping tabular data."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


def ensure_artifact(path: Path) -> None:
    """Đảm bảo artifact cần thiết tồn tại trên đĩa."""
    if not path.exists():
        raise FileNotFoundError(f"không thể tìm thấy artifact tại {path}")


def parse_date(value: Optional[str]) -> Optional[pd.Timestamp]:
    """Convert date strig sang pd.Timestamp, hoặc None nếu value là None."""
    if value is None:
        return None
    dt = pd.to_datetime(value, errors="coerce")
    if isinstance(dt, pd.Series):
        dt = dt.iloc[0]
    if pd.isna(dt):
        raise ValueError(f"Giá trị ngày không hợp lệ: {value}")
    if isinstance(dt, pd.Timestamp) and dt.tzinfo is not None:
        dt = dt.tz_convert(None)
    return dt


def filter_by_date(
    df: pd.DataFrame,
    start: Optional[pd.Timestamp],
    end: Optional[pd.Timestamp],
) -> pd.DataFrame:
    """Áp dụng bộ lọc bắt đầu/kết thúc tùy chọn trên cột date_id."""
    if "date_id" not in df.columns or (start is None and end is None):
        return df
    result = df
    if start is not None:
        result = result[result["date_id"] >= start]
    if end is not None:
        result = result[result["date_id"] <= end]
    return result


def frame_to_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Chuyển một dataframe thành dict thân thiện với JSON."""
    if df.empty:
        return []
    serialized = df.copy()
    if "date_id" in serialized.columns and pd.api.types.is_datetime64_any_dtype(
        serialized["date_id"]
    ):
        serialized["date_id"] = serialized["date_id"].dt.strftime("%Y-%m-%d")
    serialized = serialized.where(pd.notna(serialized), None)
    return serialized.to_dict(orient="records")


def records_to_dataframe(records: List[Dict[str, Any]]) -> pd.DataFrame:
    """Xây dựng dataframe từ các bản ghi JSON do người dùng cung cấp."""
    if not records:
        raise ValueError("Không có bản ghi được cung cấp")
    df = pd.DataFrame.from_records(records)
    if "date_id" in df.columns:
        df["date_id"] = pd.to_datetime(df["date_id"], errors="coerce")
    return df
