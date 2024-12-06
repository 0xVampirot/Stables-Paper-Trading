import os
import logging
from dotenv import load_dotenv
from hot_wallet import HotWallet
from trading_bot import StableTradingBot

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

private_key = os.getenv("PRIVATE_KEY")  # Get the private key from the environment
provider_url = os.getenv("PROVIDER_URL")  # Get the provider URL
wallet = HotWallet(private_key, provider_url)
bot = StableTradingBot(wallet)

# Simulate trading loop
for _ in range(1440): #60 mins * 24 hrs > assuming 1 trade per min = 1440
    logging.info("Fetching market price...")
    bot.simulate_trade()