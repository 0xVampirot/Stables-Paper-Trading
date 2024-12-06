from typing import Dict
import logging
from web3 import Web3
from config.settings import (
    TOKEN_DECIMALS,
    USDC_ADDRESS,
    USDT_ADDRESS,
    DAI_ADDRESS
)

class HotWallet:
    # ERC20 ABI for the required functions
    ERC20_ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "payable": False,
            "stateMutability": "view",
            "type": "function",
        },
        {
            "constant": False,
            "inputs": [
                {"name": "_to", "type": "address"},
                {"name": "_value", "type": "uint256"},
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        },
    ]

    def __init__(self, private_key: str, provider_url: str):
        """Initialize the hot wallet with Web3 connection and account."""
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = self.web3.eth.account.from_key(private_key)
        self.token_addresses = {
            'USDC': USDC_ADDRESS,
            'USDT': USDT_ADDRESS,
            'DAI': DAI_ADDRESS
        }
        self.balances: Dict[str, int] = {
            'USDC': 0,
            'USDT': 0,
            'DAI': 0
        }
        self.update_balances()

    def update_balances(self) -> None:
        """Update token balances from the blockchain."""
        # For testing/development, using mock balances
        self.balances['USDC'] = 100_000_000  # 100 USDC
        self.balances['USDT'] = 0
        self.balances['DAI'] = 0

        # Uncomment for production use
        # for token, address in self.token_addresses.items():
        #     self.balances[token] = self.get_token_balance(address)
        
        self._log_balances()

    def get_token_balance(self, token_address: str) -> int:
        """Fetch token balance from the blockchain."""
        try:
            token_contract = self.web3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=self.ERC20_ABI
            )
            balance = token_contract.functions.balanceOf(self.account.address).call()
            return balance
        except Exception as e:
            logging.error(f"Error fetching balance for {token_address}: {str(e)}")
            return 0

    def _log_balances(self) -> None:
        """Log current balances in human-readable format."""
        balance_str = ", ".join(
            f"{token}: {balance / 10**TOKEN_DECIMALS:.4f}"
            for token, balance in self.balances.items()
        )
        logging.info(f"Current balances: {balance_str}")