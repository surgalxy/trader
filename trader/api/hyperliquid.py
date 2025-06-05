"""HyperLiquid API wrapper."""

from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException


class APIError(Exception):
    """Raised when the HyperLiquid API returns an error response."""

    pass


class HyperLiquidAPI:
    """Minimal wrapper for HyperLiquid REST API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Perform a GET request and return the parsed JSON response."""

        try:
            response = requests.get(self._url(path), params=params or {})
            response.raise_for_status()
        except RequestException as exc:  # pragma: no cover - network failure branch
            raise ConnectionError(f"Failed to fetch {path}: {exc}") from exc

        data = response.json()
        if isinstance(data, dict) and data.get("error"):
            raise APIError(data["error"])
        return data

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform a POST request and return the parsed JSON response."""

        try:
            response = requests.post(self._url(path), json=json or {})
            response.raise_for_status()
        except RequestException as exc:  # pragma: no cover - network failure branch
            raise ConnectionError(f"Failed to fetch {path}: {exc}") from exc

        data = response.json()
        if isinstance(data, dict) and data.get("error"):
            raise APIError(data["error"])
        return data

    # Convenience higher level helpers -----------------------------------------------------

    def fetch_eth_market_data(self) -> Dict[str, Any]:
        """Return market data for ETH."""

        return self.get("/markets/ETH")

    def place_order(self, symbol: str, quantity: float, side: str) -> Dict[str, Any]:
        """Submit an order to the exchange."""

        payload = {"symbol": symbol, "quantity": quantity, "side": side}
        return self.post("/orders", json=payload)

    def get_account_balances(self) -> Dict[str, Any]:
        """Retrieve account balances."""

        return self.get("/balances")
