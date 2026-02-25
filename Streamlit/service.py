from __future__ import annotations

import pandas as pd
import streamlit as st

import config
from api_client import ApiClient


st.set_page_config(page_title="Retail Forecast UI", page_icon="📈", layout="wide")

def _init_session_state() -> None:
    """Khởi tạo các biến session mặc định."""
    st.session_state.setdefault("base_url", config.DEFAULT_API_BASE_URL)
    st.session_state.setdefault("timeout", config.REQUEST_TIMEOUT)


@st.cache_data(show_spinner=False)
def _fetch_api_data(method_name: str, base_url: str, timeout: float, **kwargs) -> dict:
    """Hàm wrapper chung để gọi các phương thức GET của API."""
    client = ApiClient(base_url, timeout)
    method = getattr(client, method_name)
    return method(**kwargs)


def _merge_predictions(original_df: pd.DataFrame, predictions: list) -> pd.DataFrame:
    """Ghép cột dự đoán vào dataframe gốc."""
    result_df = original_df.copy()
    if not result_df.empty and len(predictions) == len(result_df):
        result_df["prediction"] = predictions
        return result_df
    # Fallback nếu không khớp độ dài
    return pd.DataFrame({"prediction": predictions})

def _prepare_template_df(columns: list, seed_data: dict) -> pd.DataFrame:
    """Tạo dataframe mẫu với đúng các cột feature cần thiết."""
    df = pd.DataFrame(seed_data.get("data", []))
    for col in columns:
        if col not in df.columns:
            df[col] = None
    return df[columns]
