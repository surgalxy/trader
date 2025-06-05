# Trader

A minimal project for experimenting with automated trading using a simple agent and a wrapper for the HyperLiquid API.

## Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Instantiate the `TradingAgent` with a configured `HyperLiquidAPI` instance and place orders programmatically:

```python
from trader import TradingAgent
from trader.api import HyperLiquidAPI

api = HyperLiquidAPI(base_url="https://api.hyperliquid.xyz")
agent = TradingAgent(api)
response = agent.place_order("ETH-USD", quantity=1.0, side="buy")
print(response)
```

## Testing

Run unit tests with:

```bash
pytest
```
