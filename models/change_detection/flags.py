from dataclasses import asdict, dataclass, field, fields
from .account_changes import AccountChanges
from .crypto_changes import CryptoChanges
from .exfiltration_changes import ExfiltrationChanges
from .evasion_changes import EvasionChanges
from .generic_changes import GenericChanges
from .payload_changes import PayloadChanges
from utils import synchronized_print

@dataclass
class Flags:
    """Flags indicating percentage differences or introductions across various metrics between versions
        (current vs all previous versions (or in some cases only previous version))"""
    package: str
    version: str

    generic: GenericChanges = field(default_factory=GenericChanges)
    evasion: EvasionChanges = field(default_factory=EvasionChanges)
    payload: PayloadChanges = field(default_factory=PayloadChanges)
    exfiltration: ExfiltrationChanges = field(default_factory=ExfiltrationChanges)
    crypto: CryptoChanges = field(default_factory=CryptoChanges)
    account: AccountChanges = field(default_factory=AccountChanges)

    def iterate_thresholds(self):
        """Iterate over all ThresholdRules defined in Changes"""
        for field_info in fields(self):
            name = field_info.name
            
            if name in ("package", "version"):
                continue

            changes_obj = getattr(self, name)
            thresholds = getattr(changes_obj, "THRESHOLDS", [])

            for rule in thresholds:
                yield rule

    @staticmethod
    def _iterate(d, prefix):
        for k, v in d.items():
                if isinstance(v, dict):
                    yield from Flags._iterate(v, f"{prefix}{k}.")
                else:
                    yield prefix + k, v

    def iterate_changes(self):
        """Iterate only the 6 Changes sections"""
        for field_info in fields(self):
            name = field_info.name
            if name in ("package", "version"):
                continue
            yield name, asdict(getattr(self, name))

    def iterate_changes_flat(self):
        for name, section in self.iterate_changes():
            yield from Flags._iterate(section, f"{name}.")