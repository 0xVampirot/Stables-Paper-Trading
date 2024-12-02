# Paper Trading Bot for Stablecoins

## Overview

This paper trading bot simulates a market-making strategy for trading stablecoins on a decentralized exchange (DEX). The bot automatically decides whether to buy or sell based on the current market price of stablecoins. It buys when the market price is below 1 and sells when the market price is above 1. The bot tracks profit and loss (P/L) to date, allowing users to evaluate the performance of their trading strategy without risking real funds.

## Features

- Simulates buying stablecoins when the market price is less than 1.
- Simulates selling stablecoins when the market price is greater than 1.
- Executes trades based on 80% of available balance or portfolio amount.
- Tracks cumulative profit and loss over time.
- Outputs detailed trade information, including market prices, amounts traded, costs, revenues, and P/L.

## Requirements

- Python 3.x
- `random` library (included in Python standard library)

## Installation

### Clone the repository:
   ```bash
   git clone https://github.com/yourusername/paper-trading-bot.git
   cd paper-trading-bot
   ```

### Run the bot:
Simply execute the Python script to start simulating trades:
    ```bash
    python paper_trading_bot.py
    ```

## Observe Output:
The bot will fetch simulated market prices and execute trades based on the defined strategy. You will see output indicating:
- Current market price.
- Actions taken (buy/sell).
- Amounts traded.
- Total costs and revenues.
- Cumulative profit and loss.

### Trading Strategy
- Buying: The bot will buy stablecoins when the market price is less than 1. It calculates the amount to buy as 80% of the available balance divided by the current market price.
- Selling: The bot will sell stablecoins when the market price is greater than 1. It calculates the amount to sell as 80% of USDT currently held in the portfolio.
- Profit and Loss Calculation: After each sell transaction, the bot calculates profit or loss based on the average cost of stablecoins sold compared to their selling price.

## Future Enhancements
- Integrate real-time market data from a DEX API.
- Implement more advanced trading strategies.
- Add logging functionality for better tracking of trades and performance.
- reate a user interface for easier interaction with the bot.

### License
This project is licensed under the MIT License - see the LICENSE file for details.