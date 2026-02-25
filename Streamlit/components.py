import streamlit as st
import config
from api_client import ApiClient
from helpers import coerce_date
import pandas as pd


def _render_connection_settings() -> ApiClient:
    """Hiển thị cài đặt kết nối ở Sidebar."""
    st.sidebar.header("Kết nối API")
    st.sidebar.caption("Chạy container và trỏ tới base URL của FastAPI")

    base_url = st.sidebar.text_input("API base URL", st.session_state["base_url"])
    timeout = st.sidebar.slider("Timeout (giây)", 5, 60, int(st.session_state["timeout"]))

    # Update Session State
    st.session_state["base_url"] = base_url
    st.session_state["timeout"] = float(timeout)

    client = ApiClient(base_url, float(timeout))

    if st.sidebar.button("Kiểm tra kết nối"):
        try:
            client.health()
            st.sidebar.success("API sẵn sàng")
        except Exception as exc:
            st.sidebar.error(f"Không thể kết nối: {exc}")

    return client

def _render_sampling_controls() -> tuple[int, str, str]:
    """Hiển thị các nút chọn số lượng và ngày tháng."""
    col1, col2, col3 = st.columns(3)
    limit = col1.slider("Số dòng", 10, config.MAX_SAMPLE_ROWS, 100, 10)
    start_val = col2.date_input("Từ ngày", value=None)
    end_val = col3.date_input("Đến ngày", value=None)

    return limit, coerce_date(start_val), coerce_date(end_val)

def _display_prediction_result(result_df: pd.DataFrame, count: int) -> None:
    """Hiển thị kết quả dự đoán thống nhất."""
    st.success(f"Đã dự đoán {count} dòng")
    st.dataframe(result_df, use_container_width=True)
