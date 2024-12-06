from typing import Final

# Trading Constants
MIN_BALANCE: Final[float] = 1.00
PRICE_THRESHOLD: Final[float] = 1.0000
DECIMAL_PLACES: Final[int] = 4

# Token Decimals
TOKEN_DECIMALS: Final[int] = 6  # For USDC, USDT, DAI

# Contract Addresses (example testnet addresses)
USDC_ADDRESS: Final[str] = "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238"
USDT_ADDRESS: Final[str] = "0xaA8E23Fb1079EA71e0a56F48a2aA51851D8433D0"
DAI_ADDRESS: Final[str] = "0x1234567890123456789012345678901234567890"  # Example

# Logging
LOG_DIRECTORY: Final[str] = "logs"
LOG_FORMAT: Final[str] = "%(asctime)s - %(levelname)s - %(message)s"