import logging
from web3 import Web3

# Define the ERC20 ABI
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

class HotWallet:
    def __init__(self, private_key, provider_url):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = self.web3.eth.account.from_key(private_key)
        self.balances = {
            'USDC': 0,  # Starting balance in USDC
            'USDT': 0   # Starting balance in USDT
        }
        self.update_balances()

    def update_balances(self):
        # Fetch balances from the blockchain
        self.balances['USDC'] = 100000000
        # self.balances['USDC'] = self.get_token_balance('0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238')  # Replace with actual USDC test contract address on Sepolia
        # self.balances['USDT'] = self.get_token_balance(Web3.to_checksum_address('0xaA8E23Fb1079EA71e0a56F48a2aA51851D8433D0'))
        self.balances['USDT'] = 00000000# Replace with actual USDT test contract address on Sepolia
        logging.info(f"Updated balances: USDC: {self.balances['USDC'] / 1e6:.4f}, USDT: {self.balances['USDT'] / 1e6:.4f}")

    def get_token_balance(self, token_address):
        # Implement ERC20 balanceOf call
        token_contract = self.web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI) 
        balance = token_contract.functions.balanceOf(self.account.address).call()
        logging.info(f"Fetched balance for {token_address}: {balance / 1e6:.4f}")  # Log balance in human-readable format
        return balance
