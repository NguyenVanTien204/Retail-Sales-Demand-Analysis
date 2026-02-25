"""Pydantic schemas used by the API."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    limit: Optional[int] = Field(
        default=200,
        ge=1,
        le=2000,
        description="Các hàng được lấy mẫu từ dữ liệu test khi không có bản ghi",
    )
    start_date: Optional[str] = Field(
        default=None, description="Giới hạn khi lấy mẫu dữ liệu"
    )
    end_date: Optional[str] = Field(
        default=None, description="Giới hạn khi lấy mẫu dữ liệu"
    )
    records: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Các hàng đặc trưng tùy chỉnh bao gồm mọi cột cần thiết",
    )


class PredictionResponse(BaseModel):
    rows: int
    model: str
    predictions: List[float]
