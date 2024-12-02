class HotWallet:
    def __init__(self):
        self.balances = {
            'USDC': 100,  # Starting balance in USDC
            'USDT': 0      # Starting balance in USDT
        }

    def transfer_to_wallet(self, token, amount):
        """Simulate transferring tokens into the wallet."""
        if token in self.balances:
            self.balances[token] += amount
            print(f"Transferred {amount:.2f} {token} to wallet. New balance: {self.balances[token]:.2f} {token}")
        else:
            print("Invalid token.")

    def transfer_from_wallet(self, token, amount):
        """Simulate transferring tokens out of the wallet."""
        if self.balances[token] >= amount:
            self.balances[token] -= amount
            print(f"Transferred {amount:.2f} {token} from wallet. New balance: {self.balances[token]:.2f} {token}")
        else:
            print(f"Insufficient {token} balance in wallet.")