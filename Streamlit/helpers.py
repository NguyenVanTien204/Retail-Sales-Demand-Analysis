from __future__ import annotations

from typing import Iterable, List, Optional

import pandas as pd


def coerce_date(value: Optional[pd.Timestamp | str]) -> Optional[str]:
    """Chuyển đổi giá trị ngày tháng sang chuỗi 'YYYY-MM-DD' hoặc None."""
    if value in (None, ""):
        return None
    ts = pd.to_datetime(value, errors="coerce")
    if isinstance(ts, pd.Series):
        ts = ts.iloc[0]
    if pd.isna(ts):
        return None
    if getattr(ts, "tzinfo", None):
        ts = ts.tz_convert(None)
    return ts.strftime("%Y-%m-%d")


def dataframe_to_records(df: pd.DataFrame, date_columns: Iterable[str] = ("date_id",)) -> List[dict]:
    """Chuyển dataframe thành danh sách các dict, định dạng lại các cột ngày tháng."""
    if df is None or df.empty:
        return []
    data = df.copy()
    for col in date_columns:
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors="coerce").dt.strftime("%Y-%m-%d")
    data = data.where(pd.notna(data), None)
    return data.to_dict(orient="records")
