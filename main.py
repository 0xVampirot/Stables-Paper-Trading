import os
import logging
from dotenv import load_dotenv
from models.hot_wallet import HotWallet
from services.trading_bot import StableTradingBot
from config.settings import LOG_FORMAT

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT
    )

def main():
    # Load environment variables
    load_dotenv()

    # Setup logging
    setup_logging()

    # Initialize wallet and trading bot
    try:
        private_key = os.getenv("PRIVATE_KEY")
        provider_url = os.getenv("PROVIDER_URL")
        
        if not private_key or not provider_url:
            raise ValueError("Missing required environment variables")

        wallet = HotWallet(private_key, provider_url)
        bot = StableTradingBot(wallet)

        # Simulate trading loop (24 hours * 60 minutes)
        for i in range(1440):
            logging.info(f"Starting trade simulation {i + 1}/1440")
            bot.simulate_trade()

    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()