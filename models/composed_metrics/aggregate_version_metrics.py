from dataclasses import dataclass, field
from .aggregate_metrics.generic_aggregate import GenericAggregate
from .aggregate_metrics.evasion_aggregate import EvasionAggregate
from .aggregate_metrics.payload_aggregate import PayloadAggregate
from .aggregate_metrics.exfiltration_aggregate import ExfiltrationAggregate
from .aggregate_metrics.crypto_aggregate import CryptoAggregate
from .aggregate_metrics.account import AccountAggregate

@dataclass
class AggregateVersionMetrics:
    """Aggregated metrics across multiple package versions"""
    package: str = ""
    versions: str = ""
    generic: GenericAggregate = field(default_factory=GenericAggregate)
    evasion: EvasionAggregate = field(default_factory=EvasionAggregate)
    payload: PayloadAggregate = field(default_factory=PayloadAggregate)
    exfiltration: ExfiltrationAggregate = field(default_factory=ExfiltrationAggregate)
    crypto: CryptoAggregate = field(default_factory=CryptoAggregate)
    account: AccountAggregate = field(default_factory=AccountAggregate)