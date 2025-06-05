import requests

from trader.api import HyperLiquidAPI


class DummyResponse:
    def __init__(self, payload=None):
        self.payload = payload or {}

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


def test_fetch_eth_market_data_makes_get_request(monkeypatch):
    called = {}

    def mock_get(url, params=None):
        called['url'] = url
        called['params'] = params
        return DummyResponse({'ok': True})

    monkeypatch.setattr(requests, 'get', mock_get)

    api = HyperLiquidAPI('https://api.test')
    resp = api.fetch_eth_market_data()

    assert resp == {'ok': True}
    assert called['url'] == 'https://api.test/markets/ETH'


def test_place_order_formatting(monkeypatch):
    called = {}

    def mock_post(url, json=None):
        called['url'] = url
        called['json'] = json
        return DummyResponse({'order': 'ok'})

    monkeypatch.setattr(requests, 'post', mock_post)

    api = HyperLiquidAPI('https://api.test')
    resp = api.place_order('ETH-USD', 1.5, 'buy')

    assert resp == {'order': 'ok'}
    assert called['url'] == 'https://api.test/orders'
    assert called['json'] == {'symbol': 'ETH-USD', 'quantity': 1.5, 'side': 'buy'}


def test_get_account_balances_makes_get_request(monkeypatch):
    called = {}

    def mock_get(url, params=None):
        called['url'] = url
        called['params'] = params
        return DummyResponse({'balances': []})

    monkeypatch.setattr(requests, 'get', mock_get)

    api = HyperLiquidAPI('https://api.test')
    resp = api.get_account_balances()

    assert resp == {'balances': []}
    assert called['url'] == 'https://api.test/balances'
