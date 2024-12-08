# Paper Trading Bot for Stablecoins

## Overview

This paper trading bot simulates a market-making strategy for trading stablecoins on a decentralized exchange (DEX). The bot automatically decides whether to buy or sell based on the current market price of stablecoins. It buys when the market price is below 1 and sells when the market price is above 1. The bot tracks profit and loss (P/L) to date, allowing users to evaluate the performance of their trading strategy without risking real funds.

## Features

2 Stables (i.e. USDC/USDT):
- Simulates buying stablecoins when the market price is less than 1 between the pair.
- Simulates selling stablecoins when the market price is greater than 1 between the pair.
- Executes trades based on 100% of available balance or portfolio amount.
- Tracks cumulative profit and loss over time.
- Outputs detailed trade information, including market prices, amounts traded, costs, revenues, and P/L.

3 Stables (i.e. USDC/USDT/DAI):
- Finds the biggest stable token amount in the wallet.
- Simulates finding the best market price at or greater than 1 between the pairs.
- Executes trades based on 100% of available balance amount.
- Tracks cumulative profit and loss over time.
- Outputs detailed trade information, including market prices, amounts traded, costs, revenues, and P/L.

## Requirements

- Python 3.x
- `random` library (included in Python standard library)
- `python-dotenv` library
- `web3` library

## Installation

### Clone the repository:
   ```bash
   git https://github.com/0xVampirot/Stables-Paper-Trading.git
   cd stables-paper-trading
   ```

### Run the bot:
Simply execute the Python script to start simulating trades:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python3 main.py
    ```

## Observe Output:
The bot will fetch simulated market prices and execute trades based on the defined strategy. You will see output indicating:
- Current market price.
- Actions taken (buy/sell).
- Amounts traded.
- Total costs and revenues.
- Cumulative profit and loss.

### Trading Strategy for 2 Stables:
- Buying: The bot will buy stablecoins when the market price is less than 1. It calculates the amount to buy as 80%/100% of the available balance divided by the current market price.
- Selling: The bot will sell stablecoins when the market price is greater than 1. It calculates the amount to sell as 80%/100% of USDT currently held in the portfolio.
- Profit and Loss Calculation: After each sell transaction, the bot calculates profit or loss based on the average cost of stablecoins sold compared to their selling price.

### Trading Strategy for 3+ Stables:
- Swapping: The bot will look at the highest balance stable coin existing in the wallet and fetch the market price of the two other stablecoins.If the market price is greater than 1, it will swap according to the better rate if both market prices are greater than 1. 
- Profit and Loss Calculation: After each swap, the bot calculates profit or loss based on the average cost of stablecoins sold compared to their selling price.

## Future Enhancements
- Use hot wallet to test with an Aggregator's API.

### License
This project is licensed under the MIT License - see the LICENSE file for details.