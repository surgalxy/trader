"""Trading agents and strategies."""

import json
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Optional

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


class Strategy:
    """Trading strategy interface."""

    def generate_signal(self, prices: Iterable[float]) -> str:
        """Return ``'buy'``, ``'sell'`` or ``'hold'`` for the given prices."""

        raise NotImplementedError


class MovingAverageCrossStrategy(Strategy):
    """Simple moving average crossover strategy."""

    def __init__(self, short_window: int = 5, long_window: int = 20) -> None:
        self.short_window = short_window
        self.long_window = long_window
        self._last_signal = "hold"

    def generate_signal(self, prices: Iterable[float]) -> str:
        prices = list(prices)
        if len(prices) < self.long_window:
            return "hold"

        short_avg = mean(prices[-self.short_window :])
        long_avg = mean(prices[-self.long_window :])

        if short_avg > long_avg and self._last_signal != "buy":
            self._last_signal = "buy"
            return "buy"
        if short_avg < long_avg and self._last_signal != "sell":
            self._last_signal = "sell"
            return "sell"
        return "hold"


class Agent:
    """Trading agent that uses a strategy to decide when to trade."""

    def __init__(
        self,
        config: Mapping[str, Any] | str,
        api: Optional[HyperLiquidAPI] = None,
        strategy: Optional[Strategy] = None,
    ) -> None:
        if isinstance(config, str):
            with open(config, "r", encoding="utf-8") as fh:
                config = json.load(fh)

        self.config = dict(config)
        base_url = self.config.get("base_url", "https://api.hyperliquid.xyz")
        self.api = api or HyperLiquidAPI(base_url)

        self.symbol = self.config.get("symbol", "ETH")
        self.quantity = float(self.config.get("quantity", 1.0))

        self.strategy = strategy or MovingAverageCrossStrategy(
            short_window=int(self.config.get("short_window", 5)),
            long_window=int(self.config.get("long_window", 20)),
        )

        self._prices: List[float] = []

    def step(self) -> Optional[Dict[str, Any]]:
        """Fetch market data, evaluate the strategy and place orders if needed."""

        data = self.api.fetch_eth_market_data()
        price = float(data.get("price"))
        self._prices.append(price)
        signal = self.strategy.generate_signal(self._prices)
        if signal in {"buy", "sell"}:
            return self.api.place_order(self.symbol, self.quantity, signal)
        return None
