import csv
from datetime import datetime
import logging
import os
from typing import Dict, Optional
from config.settings import LOG_DIRECTORY


class TradeLogger:
    def __init__(self):
        self.log_directory = LOG_DIRECTORY
        os.makedirs(self.log_directory, exist_ok=True)
        self.current_date = datetime.now().strftime('%Y%m%d')
        self.log_file_path = self._create_log_file()
        self.logger = logging.getLogger(__name__)

    def _create_log_file(self) -> str:
        log_file_name = f"trade_log_{self.current_date}.csv"
        log_file_path = os.path.join(self.log_directory, log_file_name)
        
        if not os.path.isfile(log_file_path):
            with open(log_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Date", "Time", "Status", "Reason", 
                    "Funding Token", "Funding Amount",
                    "Market Price USDC", "Market Price USDT", "Market Price DAI",
                    "Swapped To Token", "Swap Price", "Gas Cost in Gwei", "Gas Cost in USD",
                    "Ending Token", "Ending Amount",
                    "PNL from Swap", "Cumulative PNL", "Success Rate"
                ])
        return log_file_path

    def _check_new_day(self) -> None:
        current_date = datetime.now().strftime('%Y%m%d')
        if current_date != self.current_date:
            self.current_date = current_date
            self.log_file_path = self._create_log_file()

    def log_trade(self, status: str, funding_token: str, funding_amount: float,
              market_prices: Dict[str, float], swapped_to_token: Optional[str],
              swap_price: float, gas_cost: float, gas_cost_gwei: float,
              ending_token: str, ending_amount: float, pnl_from_swap: float,
              cumulative_pnl: float, successful_trades_count: int,
              total_trades_count: int, failure_reason: str = "") -> None:
        
        self._check_new_day()
        
        self.logger.info(
            f"Trade Status: {status}\n"
            f"From: {funding_token} ({funding_amount:.4f})\n"
            f"To: {swapped_to_token or 'N/A'}\n"
            f"Market Prices: {market_prices}\n"
            f"Swap Price: {swap_price:.4f}\n"
            f"Gas Cost: {gas_cost:.4f} USDC ({gas_cost_gwei:.2f} Gwei)\n"
            f"Ending Balance: {ending_amount:.4f} {ending_token}\n"
            f"PnL from Swap: {pnl_from_swap:.4f}\n"
            f"Cumulative PnL: {cumulative_pnl:.4f}\n"
            f"Success Rate: {successful_trades_count}/{total_trades_count}"
        )
    
        if failure_reason:
            self.logger.warning(f"Trade failed: {failure_reason}")
            
        self._log_csv_entry(status, funding_token, funding_amount, market_prices,
                        swapped_to_token, swap_price, gas_cost_gwei, gas_cost, ending_token,
                        ending_amount, pnl_from_swap, cumulative_pnl,
                        successful_trades_count, total_trades_count, failure_reason)

    def _log_csv_entry(self, *args) -> None:
        status, funding_token, funding_amount, market_prices, swapped_to_token, \
        swap_price, gas_cost_gwei, gas_cost, ending_token, ending_amount, pnl_from_swap, \
        cumulative_pnl, successful_trades_count, total_trades_count, failure_reason = args

        # Calculate success rate
        success_rate = f"{successful_trades_count}/{total_trades_count}"

        now = datetime.now()
        with open(self.log_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                status,
                failure_reason if status == "Failed" else "",  # Add failure reason
                funding_token,
                f"{funding_amount:.4f}",
                f"{market_prices.get('USDC', 0):.4f}",
                f"{market_prices.get('USDT', 0):.4f}",
                f"{market_prices.get('DAI', 0):.4f}",
                swapped_to_token or "N/A",
                f"{swap_price:.4f}" if swap_price else "N/A",
                f"{gas_cost_gwei:.2f}",
                f"{gas_cost:.4f}",
                ending_token,
                f"{ending_amount:.4f}",
                f"{pnl_from_swap:.4f}",
                f"{cumulative_pnl:.4f}",
                success_rate
            ])