from dataclasses import dataclass, field
from typing import List

@dataclass
class CryptoVersion:
    """For a single version"""
    crypto_addresses: int = 0
    list_crypto_addresses: List[str] = field(default_factory=list)
    cryptocurrency_name: int = 0
    wallet_detection: int = 0
    replaced_crypto_addresses: int = 0
    hook_provider: int = 0

@dataclass
class CryptoAggregate:
    """For aggregate versions"""
    avg_crypto_addresses: int = 0
    avg_cryptocurrency_name: int = 0
    avg_wallet_detection: int = 0
    avg_replaced_crypto_addresses: int = 0
    avg_hook_provider: int = 0