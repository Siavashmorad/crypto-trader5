from __future__ import annotations

import requests


class TabdealAPI:
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get(self, path: str, params: dict | None = None):
        response = requests.get(self.base_url + path, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def ping(self):
        return self._get("/r/api/v1/ping")

    def server_time(self):
        return self._get("/r/api/v1/time")

    def exchange_info(self):
        return self._get("/r/api/v1/exchangeInfo")

    def trades(self, symbol: str, limit: int | None = None):
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        return self._get("/r/api/v1/trades", params)

    def depth(self, symbol: str, limit: int | None = None):
        params = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        return self._get("/r/api/v1/depth", params)
