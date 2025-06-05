"""HyperLiquid API wrapper."""

from typing import Any, Dict, Optional

import requests


class HyperLiquidAPI:
    """Minimal wrapper for HyperLiquid REST API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.post(self._url(path), json=json or {})
        response.raise_for_status()
        return response.json()
