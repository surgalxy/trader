# Trader

A minimal project for experimenting with automated trading using a simple agent and a wrapper for the HyperLiquid API.

## Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure API keys

Set your Hyperliquid credentials in the environment before running the
agent:

```bash
export HYPERLIQUID_API_KEY="<your-api-key>"
export HYPERLIQUID_API_SECRET="<your-api-secret>"
```

An example configuration file is provided in `config.example.json`. Copy it to
`config.json` and adjust the values as needed.

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

### Running the trading agent

The repository includes an example configuration in `config.example.json`. To
run the agent repeatedly using this configuration:

```python
from trader import Agent

agent = Agent("config.json")
while True:
    agent.step()
```

Use the testnet API endpoint for paper trading and the main API for live
trading. Simply set the `base_url` field in your configuration file
accordingly.

## Testing

Run unit tests with:

```bash
pytest
```
