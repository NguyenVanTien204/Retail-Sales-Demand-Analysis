from __future__ import annotations

"""Centralized Streamlit configuration for the API frontend."""
import os

DEFAULT_API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
REQUEST_TIMEOUT = float(os.getenv("API_TIMEOUT", "10"))
MAX_SAMPLE_ROWS = 500
