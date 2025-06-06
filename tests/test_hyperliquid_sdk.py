from trader.api.hyperliquid_sdk import HyperLiquidSDK


class DummyInfo:
    def __init__(self, *args, **kwargs):
        self.called_with = None

    def user_state(self, address):
        self.called_with = address
        return {"user": address}


def test_user_state_uses_info(monkeypatch):
    dummy = DummyInfo()
    monkeypatch.setattr("trader.api.hyperliquid_sdk.Info", lambda *a, **k: dummy)
    sdk = HyperLiquidSDK("0xabc", "secret", testnet=True)
    data = sdk.user_state()
    assert data == {"user": "0xabc"}
    assert dummy.called_with == "0xabc"

