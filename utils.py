import random

def fetch_market_price(market_pair):
    """Simulate fetching market prices based on the trading pair."""
    return random.uniform(0.9990, 1.0005)  # Example range for stablecoin prices

def fetch_gas_price():
    """Randomize gas price within a realistic range for the Optimism chain."""
    return random.uniform(100, 1000)  # Random gas price between 10 and 100 Gwei

def fetch_eth_price_in_usdc():
    """Simulate fetching the current ETH price in USDC."""
    return random.uniform(3000, 4000)  # Example range for ETH price in USDC