import random
from hot_wallet import HotWallet

class StableTradingBot:
    def __init__(self, wallet):
        self.wallet = wallet
        self.trade_history = []  # To store trade history for P/L calculation
        self.total_profit_loss = 0.0  # Cumulative profit/loss

    def simulate_trade(self):
    # Constants for trading conditions
        MIN_BALANCE = 10.0
        PRICE_THRESHOLD = 1.00

        # Determine which market pair to fetch based on balances
        market_pair = "USDC/USDT"
        price = self.fetch_market_price(market_pair)
        print(f"Fetching market price for {market_pair}: {price:.2f}")
        print(f"Starting Wallet Balance: {self.wallet.balances['USDT']:.2f} USDT, {self.wallet.balances['USDC']:.2f} USDC")

        # Check if the price is exactly 1.00
        if round(price, 2) == PRICE_THRESHOLD:
            print("Price is exactly 1.00. No trades will take place.\n")
            return  # Exit the method to prevent any trades

        # Determine the funding token based on the price
        funding_token = 'USDC' if price < PRICE_THRESHOLD else 'USDT'
        print(f"Using funding token: {funding_token}")

        # Check if the funding token balance is sufficient
        if self.wallet.balances[funding_token] < MIN_BALANCE:
            print(f"Insufficient balance in {funding_token}. Minimum required is {MIN_BALANCE}. No trade will take place.\n")
            return  # Exit the method to prevent any trades

        # Trading logic based on the funding token
        if funding_token == 'USDC':
            # Swap 80% of USDC to USDT
            amount_to_buy = self.wallet.balances[funding_token] * 0.8  # Use 80% of USDC
            cost = amount_to_buy * price
            
            # Ensure sufficient balance for the trade
            if cost <= self.wallet.balances[funding_token]:
                self.wallet.transfer_from_wallet(funding_token, cost)
                self.wallet.transfer_to_wallet('USDT', amount_to_buy / price)  # Calculate amount to buy
                self.trade_history.append({'action': 'buy', 'amount': amount_to_buy / price, 'price': price})
                print(f"Swapped {amount_to_buy:.2f} {funding_token} to {amount_to_buy / price:.2f} USDT at {price:.2f} each.")
            else:
                print(f"Insufficient balance in {funding_token} for purchase.")
        
        elif funding_token == 'USDT':
            # Swap 80% of USDT to USDC
            amount_to_sell = self.wallet.balances[funding_token] * 0.8  # Use 80% of USDT
            
            if amount_to_sell > 0:
                revenue = amount_to_sell * price
                self.wallet.transfer_from_wallet(funding_token, amount_to_sell)
                self.wallet.transfer_to_wallet('USDC', revenue)
                
                # Calculate total cost of the tokens being sold
                total_cost = sum(trade['amount'] * trade['price'] for trade in self.trade_history if trade['action'] == 'buy')
                
                # Calculate P/L for this trade
                total_bought = sum(trade['amount'] for trade in self.trade_history if trade['action'] == 'buy')
                average_cost_per_unit = total_cost / total_bought if total_bought > 0 else 0
                profit_loss = revenue - (average_cost_per_unit * amount_to_sell)
                
                # Update cumulative P/L
                self.total_profit_loss += profit_loss
                
                print(f"Swapped {amount_to_sell:.2f} {funding_token} to {revenue:.2f} USDC at {price:.2f} each. P/L: {profit_loss:.2f} USDT")
                print(f"Cumulative P/L to date: {self.total_profit_loss:.2f} USDT")
            else:
                print(f"Insufficient {funding_token} in portfolio.")

        # Display current wallet balances after each trade
        print(f"Wallet: {self.wallet.balances['USDT']:.2f} USDT, {self.wallet.balances['USDC']:.2f} USDC\n")
    def fetch_market_price(self, market_pair):
        """Simulate fetching market prices based on the trading pair."""
        return random.uniform(0.95, 1.05)  # Example range for stablecoin prices

# Initialize the hot wallet and trading bot
if __name__ == "__main__":
    wallet = HotWallet()
    bot = StableTradingBot(wallet)

    # Simulate trading loop
    for _ in range(10):
        print("Fetching market price...")
        bot.simulate_trade()