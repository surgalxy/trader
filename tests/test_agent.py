import types

import pytest

from trader import TradingAgent
from trader.api import HyperLiquidAPI


class DummyAPI(HyperLiquidAPI):
    def __init__(self):
        pass

    def post(self, path: str, json=None):
        return {"path": path, "json": json}


def test_place_order_returns_response_dict():
    api = DummyAPI()
    agent = TradingAgent(api)
    resp = agent.place_order("ETH-USD", 1.0, "buy")
    assert isinstance(resp, dict)
    assert resp["path"] == "/orders"
    assert resp["json"]["symbol"] == "ETH-USD"
