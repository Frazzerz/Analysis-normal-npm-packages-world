from dataclasses import dataclass
from .change_metrics import ChangeMetric
from .threshold import ThresholdConfig, GenericThresholdRule
from ..symbol import Symbol
@dataclass
class CryptoChanges:
    crypto_addresses: ChangeMetric = ChangeMetric(None, None)
    change_crypto_addresses: bool = False
    cryptocurrency_name: ChangeMetric = ChangeMetric(None, None)
    wallet_checks: ChangeMetric = ChangeMetric(None, None)
    replaced_crypto_addresses: ChangeMetric = ChangeMetric(None, None)
    hook_provider: ChangeMetric = ChangeMetric(None, None)

    THRESHOLDS = [
        GenericThresholdRule(
            name="Increase crypto addresses",
            metric_path="crypto.crypto_addresses",
            config=ThresholdConfig(
                absolute=50.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Crypto addresses increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Remove all crypto addresses",             # to understand
            metric_path="crypto.crypto_addresses",
            config=ThresholdConfig(
                percentage=-100.0,
                symbol=Symbol.LESS_THAN,
                description="All crypto addresses were removed in this version",
            ),
        ),
        GenericThresholdRule(
            name="Cryptocurrency name changed",
            metric_path="crypto.change_crypto_addresses",
            config=ThresholdConfig(
                boolean=True,
                description="Cryptocurrency name was changed in this version",
            ),
        ),
        GenericThresholdRule(
            name="Increase cryptocurrency name occurrences",
            metric_path="crypto.cryptocurrency_name",
            config=ThresholdConfig(
                absolute=50.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Cryptocurrency name occurrences increased significantly",
            ),
        ),
        GenericThresholdRule(                               # to understand
            name="Remove all cryptocurrency name occurrences",
            metric_path="crypto.cryptocurrency_name",
            config=ThresholdConfig(
                percentage=-100.0,
                symbol=Symbol.LESS_THAN,
                description="All cryptocurrency name occurrences were removed in this version",
            ),
        ),
        GenericThresholdRule(
            name="Increase wallet checks",
            metric_path="crypto.wallet_checks",
            config=ThresholdConfig(
                absolute=1,
                symbol=Symbol.GREATER_THAN,
                description="Wallet checks increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Increase replaced crypto addresses",
            metric_path="crypto.replaced_crypto_addresses",
            config=ThresholdConfig(
                absolute=1,
                symbol=Symbol.GREATER_THAN,
                description="Replaced crypto addresses increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Increase hook provider usage",
            metric_path="crypto.hook_provider",
            config=ThresholdConfig(
                absolute=1,
                symbol=Symbol.GREATER_THAN,
                description="Hook provider usage increased significantly",
            ),
        ),
    ]