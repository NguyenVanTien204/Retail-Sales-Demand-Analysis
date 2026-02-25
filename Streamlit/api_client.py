from __future__ import annotations

"""Lightweight HTTP client for the forecasting API."""
from typing import Any, Dict, Optional

import requests


class ApiClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.request(method=method, url=url, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response.json()

    def root(self) -> Dict[str, Any]:
        return self._request("get", "/")

    def health(self) -> Dict[str, Any]:
        return self._request("get", "/health")

    def summary(self) -> Dict[str, Any]:
        return self._request("get", "/data/summary")

    def sample(
        self,
        *,
        limit: int = 100,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        params = {"limit": limit}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._request("get", "/data/sample", params=params)

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("post", "/predict", json=payload)
