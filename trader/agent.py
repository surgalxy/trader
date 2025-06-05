"""Main trading agent."""

from typing import Any, Dict

from .api.hyperliquid import HyperLiquidAPI


class TradingAgent:
    """Simple trading agent using HyperLiquidAPI."""

    def __init__(self, api: HyperLiquidAPI):
        self.api = api

    def place_order(self, symbol: str, quantity: float, side: str) -> Dict[str, Any]:
        """Place an order via the HyperLiquid API.

        Parameters
        ----------
        symbol : str
            Trading symbol (e.g., 'ETH-USD').
        quantity : float
            Amount to buy or sell.
        side : str
            'buy' or 'sell'.
        Returns
        -------
        Dict[str, Any]
            API response payload.
        """
        order_data = {
            "symbol": symbol,
            "quantity": quantity,
            "side": side,
        }
        return self.api.post("/orders", json=order_data)
