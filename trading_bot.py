import random
import logging
from hot_wallet import HotWallet
from utils import fetch_market_price, fetch_eth_price_in_usdc, fetch_gas_price  # Import fetch_gas_price

class StableTradingBot:
    def __init__(self, wallet):
        self.wallet = wallet
        self.trade_history = []  # To store trade history for P/L calculation
        self.total_profit_loss = 0.0  # Cumulative profit/loss
        self.successful_trades_count = 0  # Count of successful trades
        self.gas_price_per_transaction = fetch_gas_price()  # Randomized gas price in Gwei

    def simulate_swap(self, from_token, to_token, amount, price):
        # Calculate the amount of tokens received based on the simulated market price
        if from_token == 'USDC':
            amount_received = amount * price  # Simulate receiving USDT
        elif from_token == 'USDT':
            amount_received = amount / price  # Simulate receiving USDC
        else:
            raise ValueError("Invalid token for swap simulation.")

        # Calculate gas cost
        gas_cost_eth = self.gas_price_per_transaction / 1e9  # Convert Gwei to ETH
        eth_price_usdc = fetch_eth_price_in_usdc()  # Fetch current ETH price in USDC
        gas_cost_usdc = gas_cost_eth * eth_price_usdc  # Calculate gas cost in USDC

        # Estimate the amount after gas costs
        estimated_amount_after_gas = amount_received - gas_cost_usdc

        # Check if the estimated amount after gas costs is beneficial
        if estimated_amount_after_gas <= 0:
            logging.error("Swap not initiated due to high gas costs.")
            return  # Exit the method without performing the swap

        # Check if the gain is less than the gas cost
        gain = estimated_amount_after_gas - amount  # Gain calculated as the amount received minus the amount swapped
        if gain < gas_cost_usdc:
            logging.error("Gas is too high to trade.")
            return  # Exit the method without performing the swap

        # Update the wallet balances
        self.wallet.balances[from_token] -= amount * 1e6  # Deduct the amount being swapped
        self.wallet.balances[to_token] += estimated_amount_after_gas * 1e6  # Add the received amount after gas

        # Log the gas costs and gain
        logging.info(f"Gas used: {gas_cost_eth:.4f} ETH ({gas_cost_usdc:.4f} USDC) | Gain: {gain:.4f} {to_token}")

        # Calculate P/L (including gas costs)
        profit_loss = gain - gas_cost_usdc
        self.total_profit_loss += profit_loss  # Update total profit/loss
        self.successful_trades_count += 1  # Increment successful trades count

        # Log the simulated swap
        logging.info(f"Simulated swap: {amount:.4f} {from_token} to {estimated_amount_after_gas:.4f} {to_token} at price {price:.4f}")
        logging.info(f"Profit/Loss from swap: {profit_loss:.4f} ({gain:.4f} - {gas_cost_usdc:.4f})")
        logging.info(f"Total Profit/Loss: {self.total_profit_loss:.4f} USDT | Successful Trades: {self.successful_trades_count}")  # Log total profit/loss and successful trades count

    def simulate_trade(self):
        # Constants for trading conditions
        MIN_BALANCE = 1.00
        PRICE_THRESHOLD = 1.00

        # Determine which market pair to fetch based on balances
        market_pair = "USDC/USDT"
        price = fetch_market_price(market_pair)  # Use the imported function
        logging.info(f"Fetching market price for {market_pair}: {price:.4f}")
        logging.info(f"Starting Wallet Balance: USDT: {self.wallet.balances['USDT'] / 1e6:.4f}, USDC: {self.wallet.balances['USDC'] / 1e6:.4f}")

        # Check if the price is exactly 1.00
        if round(price, 4) == PRICE_THRESHOLD:
            logging.info("Price is exactly 1.0000. No trades will take place.")
            return  # Exit the method to prevent any trades

        # Determine the funding token based on the price
        if price > PRICE_THRESHOLD:
            funding_token = 'USDC'  # Swap USDC to USDT
        else:
            funding_token = 'USDT'  # Swap USDT to USDC

        logging.info(f"Using funding token: {funding_token}")

        # Check if the funding token balance is sufficient
        if self.wallet.balances[funding_token] < MIN_BALANCE * 1e6:  # Adjust minimum balance check
            logging.warning(f"Insufficient balance in {funding_token}. Minimum required is {MIN_BALANCE:.4f}. No trade will take place.")
            return  # Exit the method to prevent any trades

        # Trading logic based on the funding token
        if funding_token == 'USDC':
            # Swap 80% of USDC to USDT
            amount_to_buy = self.wallet.balances[funding_token] / 1e6 
            self.simulate_swap('USDC', 'USDT', amount_to_buy, price)  # Simulate the swap

        elif funding_token == 'USDT':
            # Swap 80% of USDT to USDC
            amount_to_sell = self.wallet.balances[funding_token] / 1e6 
            self.simulate_swap('USDT', 'USDC', amount_to_sell, price)  # Simulate the swap

        # Randomize gas price for this transaction
        self.gas_price_per_transaction = fetch_gas_price()  # Get a new random gas price

