import types

import pytest

from trader import Agent, TradingAgent
from trader.api import HyperLiquidAPI


class DummyAPI(HyperLiquidAPI):
    def __init__(self):
        pass

    def post(self, path: str, json=None):
        return {"path": path, "json": json}


class AgentDummyAPI(HyperLiquidAPI):
    def __init__(self, prices):
        self.prices = list(prices)
        self.orders = []

    def fetch_eth_market_data(self):
        return {"price": self.prices.pop(0)}

    def place_order(self, symbol: str, quantity: float, side: str):
        order = {"symbol": symbol, "quantity": quantity, "side": side}
        self.orders.append(order)
        return order


def test_place_order_returns_response_dict():
    api = DummyAPI()
    agent = TradingAgent(api)
    resp = agent.place_order("ETH-USD", 1.0, "buy")
    assert isinstance(resp, dict)
    assert resp["path"] == "/orders"
    assert resp["json"]["symbol"] == "ETH-USD"


def test_agent_moving_average_strategy():
    prices = [100, 100, 100, 100, 100, 105, 110, 90, 80]
    api = AgentDummyAPI(prices)
    agent = Agent(
        config={"symbol": "ETH", "quantity": 1.0, "short_window": 3, "long_window": 5},
        api=api,
    )

    while api.prices:
        agent.step()

    assert len(api.orders) == 2
    assert api.orders[0]["side"] == "buy"
    assert api.orders[1]["side"] == "sell"
