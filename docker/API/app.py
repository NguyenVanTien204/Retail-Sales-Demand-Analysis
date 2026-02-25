"""FastAPI entrypoint that wires routers together."""
from __future__ import annotations

from fastapi import FastAPI

from .routes import router

app = FastAPI(
    title="API du bao units_sold",
    version="1.0.0",
    summary="bao gom LightGBM (CPU) va XGBoost (GPU-trained) du bao units_sold.",
)

app.include_router(router)
