from __future__ import annotations

import pandas as pd
import streamlit as st

import config
from api_client import ApiClient
from helpers import coerce_date, dataframe_to_records
from service import _prepare_template_df, _fetch_api_data, _merge_predictions, _init_session_state
from components import _render_connection_settings, _render_sampling_controls, _display_prediction_result


# --- PAGE RENDERERS ---
def _render_overview(client: ApiClient) -> None:
    st.subheader("Tổng quan API")
    try:
        root_info = _fetch_api_data("root", client.base_url, client.timeout)
        summary = _fetch_api_data("summary", client.base_url, client.timeout)
    except Exception as exc:
        st.error(f"Không tải được thông tin: {exc}")
        return

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Model", root_info.get("model", "?"))
    c2.metric("Số cột", len(summary.get("columns", [])))
    c3.metric("Số dòng", summary.get("rows", 0))

    st.markdown("**Feature columns**")
    st.code(", ".join(summary.get("feature_columns", [])) or "(trống)")

    with st.expander("Chi tiết JSON"):
        st.json(root_info)
        st.json(summary)

def _render_quick_predict(client: ApiClient) -> None:
    st.subheader("Lấy mẫu & dự đoán nhanh")
    limit, start_date, end_date = _render_sampling_controls()

    # 1. Fetch Sample
    try:
        sample = _fetch_api_data("sample", client.base_url, client.timeout,
                                limit=limit, start_date=start_date, end_date=end_date)
        sample_df = pd.DataFrame(sample.get("data", []))
        st.caption(f"Hiển thị {len(sample_df)} dòng mẫu")
        st.dataframe(sample_df, use_container_width=True)
    except Exception as exc:
        st.error(f"Lỗi tải mẫu: {exc}")
        return

    # 2. Run Prediction
    if st.button("Chạy dự đoán"):
        try:
            payload = {"limit": limit, "start_date": start_date, "end_date": end_date}
            result = client.predict(payload)
            preds = result.get("predictions", [])

            merged_df = _merge_predictions(sample_df, preds)
            _display_prediction_result(merged_df, len(preds))
        except Exception as exc:
            st.error(f"Lỗi dự đoán: {exc}")

def _render_custom_predict(client: ApiClient) -> None:
    st.subheader("Tự nhập dữ liệu")

    # 1. Prepare Schema
    try:
        summary = _fetch_api_data("summary", client.base_url, client.timeout)
        seed = _fetch_api_data("sample", client.base_url, client.timeout, limit=5, start_date=None, end_date=None)

        feature_cols = summary.get("feature_columns", [])
        input_df = _prepare_template_df(feature_cols, seed)
    except Exception as exc:
        st.error(f"Lỗi tải schema: {exc}")
        return

    # 2. Data Editor
    editor_df = st.data_editor(input_df, num_rows="dynamic", use_container_width=True)

    # 3. Run Prediction
    if st.button("Dự đoán dữ liệu nhập"):
        records = dataframe_to_records(editor_df)
        if not records:
            st.warning("Vui lòng nhập dữ liệu")
            return

        try:
            result = client.predict({"records": records})
            preds = result.get("predictions", [])

            merged_df = _merge_predictions(editor_df, preds)
            _display_prediction_result(merged_df, len(preds))
        except Exception as exc:
            st.error(f"Lỗi dự đoán: {exc}")

# --- MAIN APP FLOW ---
def main() -> None:
    _init_session_state()

    # Sidebar Setup
    client = _render_connection_settings()
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Chức năng", ("Tổng quan", "Mẫu & dự đoán nhanh", "Tự nhập dữ liệu"))

    # Page Routing
    if page == "Tổng quan":
        _render_overview(client)
    elif page == "Mẫu & dự đoán nhanh":
        _render_quick_predict(client)
    else:
        _render_custom_predict(client)

if __name__ == "__main__":
    main()
