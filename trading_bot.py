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
            amount_received = amount * price  # Simulate receiving USDC
        elif from_token == 'DAI':
            amount_received = amount * price  # Simulate receiving DAI
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
            logging.error(f"Gas is too high to trade.Gas cost: {gas_cost_eth:.4f} ETH ({gas_cost_usdc:.4f} USDC)")
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
        # Log ending wallet balances
        logging.info(f"Ending Wallet Balance: USDC: {self.wallet.balances['USDC'] / 1e6:.4f}, USDT: {self.wallet.balances['USDT'] / 1e6:.4f}, DAI: {self.wallet.balances['DAI'] / 1e6:.4f}\n")
    
    
    def simulate_trade(self):
        # Constants for trading conditions
        MIN_BALANCE = 1.00
        PRICE_THRESHOLD = 1.0000
        funding_token = None

        highest_balance_token = max(self.wallet.balances, key=lambda k: self.wallet.balances[k])  # Get the token with the highest balance
        logging.info(f"Highest balance token: {highest_balance_token} ")
        
        # Log starting wallet balances
        logging.info(f"Starting Wallet Balance: USDC: {self.wallet.balances['USDC'] / 1e6:.4f}, USDT: {self.wallet.balances['USDT'] / 1e6:.4f}, DAI: {self.wallet.balances['DAI'] / 1e6:.4f}")

        # Fetch market prices based on the highest balance token
        if highest_balance_token == 'USDC':
            funding_token = 'USDC'
            price_usdt = fetch_market_price("USDC/USDT")
            price_dai = fetch_market_price("USDC/DAI")
            if price_usdt >= PRICE_THRESHOLD or price_dai >= PRICE_THRESHOLD:
                best_price = max(price_usdt, price_dai)
                logging.info(f"Market prices fetched: {funding_token}/USDT: {price_usdt:.4f}, {funding_token}/DAI: {price_dai:.4f}")
            else:
                logging.info(f"No favorable prices for swapping {funding_token}. Market prices fetched: {funding_token}/USDT: {price_usdt:.4f}, {funding_token}/DAI: {price_dai:.4f}")
                return  # Exit if no favorable prices

        elif highest_balance_token == 'USDT':
            funding_token = 'USDT'
            price_usdc = fetch_market_price("USDT/USDC")
            price_dai = fetch_market_price("USDT/DAI")
            if price_usdc >= PRICE_THRESHOLD or price_dai >= PRICE_THRESHOLD:
                best_price = max(price_usdc, price_dai)
                logging.info(f"Market prices fetched: {funding_token}/USDC: {price_usdc:.4f}, {funding_token}/DAI: {price_dai:.4f}")
            else:
                logging.info(f"No favorable prices for swapping {funding_token}. Market prices fetched: {funding_token}/USDC: {price_usdc:.4f}, {funding_token}/DAI: {price_dai:.4f}")
                return  # Exit if no favorable prices

        elif highest_balance_token == 'DAI':
            funding_token = 'DAI'
            price_usdt = fetch_market_price("DAI/USDT")
            price_usdc = fetch_market_price("DAI/USDC")
            if price_usdt >= PRICE_THRESHOLD or price_usdc >= PRICE_THRESHOLD:
                best_price = max(price_usdt, price_usdc)
                logging.info(f"Market prices fetched: {funding_token}/USDT: {price_usdt:.4f}, {funding_token}/USDC: {price_usdc:.4f}")
            else:
                logging.info(f"No favorable prices for swapping {funding_token}. Market prices fetched: {funding_token}/USDT: {price_usdt:.4f}, {funding_token}/USDC: {price_usdc:.4f}\n")
                return  # Exit if no favorable prices

        else:
            logging.error("No valid tokens available for trading.")
            return  # Exit if no valid tokens

        # Check if the best price is greater than 1.0000 before proceeding with the swap
        if best_price <= PRICE_THRESHOLD:
            logging.info("Best price is not favorable for trading. No trades will take place.")
            return  # Exit the method to prevent any trades

        logging.info(f"Using funding token: {funding_token}")

        # Check if the funding token balance is sufficient
        if self.wallet.balances[funding_token] < MIN_BALANCE * 1e6:  # Adjust minimum balance check
            logging.warning(f"Insufficient balance in {funding_token}. Minimum required is {MIN_BALANCE:.4f}. No trade will take place.")
            return  # Exit the method to prevent any trades

        # Trading logic based on the funding token
        if funding_token == 'USDC':
            # Swap 100% of USDC to USDT or DAI based on best price
            amount_to_sell = self.wallet.balances[funding_token] / 1e6 
            self.simulate_swap('USDC', 'USDT' if price_usdt > price_dai else 'DAI', amount_to_sell, best_price)  # Simulate the swap

        elif funding_token == 'USDT':
            # Swap 100% of USDT to USDC or DAI based on best price
            amount_to_sell = self.wallet.balances[funding_token] / 1e6 
            self.simulate_swap('USDT', 'USDC' if price_usdc > price_dai else 'DAI', amount_to_sell, best_price)  # Simulate the swap

        elif funding_token == 'DAI':
            # Swap 100% of DAI to USDT or USDC based on best price
            amount_to_sell = self.wallet.balances[funding_token] / 1e6 
            self.simulate_swap('DAI', 'USDT' if price_usdt > price_usdc else 'USDC', amount_to_sell, best_price)  # Simulate the swap
            return

        # Randomize gas price for this transaction
        self.gas_price_per_transaction = fetch_gas_price()  # Get a new random gas price

