from typing import Dict, Optional
from decimal import Decimal
from logger.trade_logger import TradeLogger
from models.hot_wallet import HotWallet
from services.market_service import MarketService
from config.settings import MIN_BALANCE, PRICE_THRESHOLD, TOKEN_DECIMALS

class StableTradingBot:
    def __init__(self, wallet: HotWallet):
        self.wallet = wallet
        self.trade_logger = TradeLogger()
        self.market_service = MarketService()
        self.total_profit_loss: float = 0.0
        self.successful_trades_count: int = 0
        self.total_trades_count: int = 0  # Add this line
        self.gas_price_per_transaction: float = self.market_service.fetch_gas_price()

    def simulate_trade(self) -> None:
        """Execute a single trading simulation."""
        # Get starting balances and find highest balance token
        starting_balances = self._get_normalized_balances()
        funding_token = max(self.wallet.balances, key=lambda k: self.wallet.balances[k])
        
        # Get market prices and best trading pair
        swap_price, to_token, market_prices = self.market_service.get_best_price_and_token(funding_token)
        
        self.total_trades_count += 1 

        if not market_prices:
            self._log_failed_trade(starting_balances, market_prices, None, 
                                 funding_token, "Failed to fetch market prices")
            return
        
        # Validate trade conditions
        if not self._validate_trade_conditions(funding_token, swap_price):
            self._log_failed_trade(starting_balances, market_prices, to_token, 
                                 funding_token, "Trade conditions not met")
            return

        # Execute the trade
        self._execute_trade(funding_token, to_token, swap_price, starting_balances, 
                          market_prices)
        

    def _log_failed_trade(self, starting_balances: Dict[str, float], 
                     market_prices: Optional[Dict[str, float]], 
                     to_token: Optional[str], 
                     funding_token: str,
                     reason: str) -> None:
        """Log information about a failed trade attempt."""
        self.trade_logger.log_trade(
            status="Failed",
            funding_token=funding_token,
            funding_amount=starting_balances.get(funding_token, 0),
            market_prices=market_prices or {},
            swapped_to_token=to_token,
            swap_price=0.0,
            gas_cost=0.0,
            gas_cost_gwei=0.0,  # Add this line
            ending_token=funding_token,
            ending_amount=starting_balances.get(funding_token, 0),
            pnl_from_swap=0.0,
            cumulative_pnl=self.total_profit_loss,
            successful_trades_count=self.successful_trades_count,
            total_trades_count=self.total_trades_count,
            failure_reason=reason
        )
    def _get_normalized_balances(self) -> Dict[str, float]:
        """Get token balances normalized to standard units."""
        return {
            token: balance / 10**TOKEN_DECIMALS
            for token, balance in self.wallet.balances.items()
        }

    def _fetch_market_prices(self, funding_token: str) -> Optional[Dict[str, float]]:
        """Fetch market prices for the given funding token."""
        market_prices = {}
        try:
            if funding_token == 'USDC':
                market_prices = {
                    'USDT': self.market_service.fetch_market_price("USDC/USDT"),
                    'DAI': self.market_service.fetch_market_price("USDC/DAI")
                }
            elif funding_token == 'USDT':
                market_prices = {
                    'USDC': self.market_service.fetch_market_price("USDT/USDC"),
                    'DAI': self.market_service.fetch_market_price("USDT/DAI")
                }
            else:  # DAI
                market_prices = {
                    'USDC': self.market_service.fetch_market_price("DAI/USDC"),
                    'USDT': self.market_service.fetch_market_price("DAI/USDT")
                }
            return market_prices
        except Exception as e:
            self.trade_logger.logger.error(f"Error fetching market prices: {str(e)}")
            return None

    def _validate_trade_conditions(self, funding_token: str, swap_price: float) -> bool:
        """Validate if trade conditions are met."""
        if self.wallet.balances[funding_token] < MIN_BALANCE * 10**TOKEN_DECIMALS:
            # Replace logger.warning with log_trade
            self._log_failed_trade(
                self._get_normalized_balances(),
                None,
                None,
                funding_token,
                f"Insufficient balance in {funding_token}. Minimum required is {MIN_BALANCE:.4f}"
            )
            return False

        if swap_price < PRICE_THRESHOLD:
            # Replace logger.info with log_trade
            self._log_failed_trade(
                self._get_normalized_balances(),
                None,
                None,
                funding_token,
                "Market price is not favorable for trading."
            )
            return False

        return True

    def _validate_swap_profitability(self, estimated_amount_after_gas: float,
                                amount_to_sell: float, gas_cost: float) -> bool:
        """Validate if the swap would be profitable after gas costs."""
        if estimated_amount_after_gas <= 0:
            self._log_failed_trade(
                self._get_normalized_balances(),
                None,
                None,
                None,
                "Swap not initiated due to high gas costs."
            )
            return False

        gain = estimated_amount_after_gas - amount_to_sell
        if gain < gas_cost:
            self._log_failed_trade(
                self._get_normalized_balances(),
                None,
                None,
                None,
                f"Gas is too high to trade. Gas cost: {gas_cost:.4f} USDC"
            )
            return False

        return True

    def _execute_trade(self, funding_token: str, to_token: str, swap_price: float,
                      starting_balances: Dict[str, float], market_prices: Dict[str, float]) -> None:
        """Execute the trade with the given parameters."""
        amount_to_sell = self.wallet.balances[funding_token] / 10**TOKEN_DECIMALS
        gas_cost = self._calculate_gas_cost()

        # Simulate the swap
        estimated_amount = amount_to_sell * swap_price
        estimated_amount_after_gas = estimated_amount - gas_cost

        if not self._validate_swap_profitability(estimated_amount_after_gas, amount_to_sell, gas_cost):
            return

        # Execute the swap
        self._perform_swap(funding_token, to_token, amount_to_sell, 
                          estimated_amount_after_gas)

        # Log the successful trade
        ending_balances = self._get_normalized_balances()
        pnl_from_swap = sum(ending_balances.values()) - sum(starting_balances.values()) - gas_cost
        self.total_profit_loss += pnl_from_swap
        self.successful_trades_count += 1

        self.trade_logger.log_trade(
            status="Success",
            funding_token=funding_token,
            funding_amount=amount_to_sell,
            market_prices=market_prices,
            swapped_to_token=to_token,
            swap_price=swap_price,
            gas_cost=gas_cost,
            gas_cost_gwei=self.gas_price_per_transaction,  # Add this line
            ending_token=to_token,
            ending_amount=estimated_amount_after_gas,
            pnl_from_swap=pnl_from_swap,
            cumulative_pnl=self.total_profit_loss,
            successful_trades_count=self.successful_trades_count,
            total_trades_count=self.total_trades_count
        )

    def _calculate_gas_cost(self) -> float:
        """Calculate the gas cost in USDC."""
        gas_cost_eth = self.gas_price_per_transaction / 1e9
        eth_price_usdc = self.market_service.fetch_eth_price_in_usdc()
        return gas_cost_eth * eth_price_usdc

    def _validate_swap_profitability(self, estimated_amount_after_gas: float,
                                   amount_to_sell: float, gas_cost: float) -> bool:
        """Validate if the swap would be profitable after gas costs."""
        if estimated_amount_after_gas <= 0:
            self.trade_logger.logger.error("Swap not initiated due to high gas costs.")
            return False

        gain = estimated_amount_after_gas - amount_to_sell
        if gain < gas_cost:
            self.trade_logger.logger.error(
                f"Gas is too high to trade. "
                f"Gas cost: {gas_cost:.4f} USDC"
            )
            return False

        return True

    def _perform_swap(self, from_token: str, to_token: str, 
                     amount: float, amount_after_gas: float) -> None:
        """Perform the actual token swap."""
        # Deduct from source token
        self.wallet.balances[from_token] -= int(amount * 10**TOKEN_DECIMALS)
        # Add to destination token
        self.wallet.balances[to_token] += int(amount_after_gas * 10**TOKEN_DECIMALS)