import random
from typing import Dict, Tuple

class MarketService:
    @staticmethod
    def fetch_market_price(market_pair: str) -> float:
        """Simulate fetching market prices based on the trading pair."""
        return random.uniform(0.9990, 1.0005)

    @staticmethod
    def fetch_gas_price() -> float:
        """Randomize gas price within a realistic range for the Optimism chain."""
        return random.uniform(100, 1000)

    @staticmethod
    def fetch_eth_price_in_usdc() -> float:
        """Simulate fetching the current ETH price in USDC."""
        return random.uniform(3000, 4000)

    @classmethod
    def get_best_price_and_token(cls, funding_token: str) -> Tuple[float, str, Dict[str, float]]:
        """Get the best price, corresponding token, and all market prices for a given funding token."""
        if funding_token == 'USDC':
            market_prices = {
                'USDT': cls.fetch_market_price("USDC/USDT"),
                'DAI': cls.fetch_market_price("USDC/DAI")
            }
            swap_price = max(market_prices['USDT'], market_prices['DAI'])
            to_token = 'USDT' if market_prices['USDT'] > market_prices['DAI'] else 'DAI'
        elif funding_token == 'USDT':
            market_prices = {
                'USDC': cls.fetch_market_price("USDT/USDC"),
                'DAI': cls.fetch_market_price("USDT/DAI")
            }
            swap_price = max(market_prices['USDC'], market_prices['DAI'])
            to_token = 'USDC' if market_prices['USDC'] > market_prices['DAI'] else 'DAI'
        else:  # DAI
            market_prices = {
                'USDC': cls.fetch_market_price("DAI/USDC"),
                'USDT': cls.fetch_market_price("DAI/USDT")
            }
            swap_price = max(market_prices['USDC'], market_prices['USDT'])
            to_token = 'USDC' if market_prices['USDC'] > market_prices['USDT'] else 'USDT'
        
        return swap_price, to_token, market_prices