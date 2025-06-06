"""Wrapper for the hyperliquid-python-sdk."""

from typing import Any

from hyperliquid.info import Info
from hyperliquid.utils import constants


class HyperLiquidSDK:
    """Small convenience wrapper around :class:`hyperliquid.info.Info`."""

    def __init__(self, account_address: str, secret_key: str, testnet: bool = True) -> None:
        self.account_address = account_address
        self.secret_key = secret_key
        api_url = constants.TESTNET_API_URL if testnet else constants.MAINNET_API_URL
        self._info = Info(api_url, skip_ws=True)

    def user_state(self) -> Any:
        """Return the user state for ``account_address``."""
        return self._info.user_state(self.account_address)

