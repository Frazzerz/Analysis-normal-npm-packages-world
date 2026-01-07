from models.composed_metrics import VersionMetrics, AggregateVersionMetrics
from models.change_detection import Flags
from .categories import GenericComparator, EvasionComparator, PayloadComparator, DataExfiltrationComparator, CryptojackingComparator, AccountComparator
from utils.logging_utils import synchronized_print

class VersionComparator:
    """Coordinate version comparison across all categories"""
    
    def __init__(self):
        self.generic_comparator = GenericComparator()
        self.evasion_comparator = EvasionComparator()
        self.payload_comparator = PayloadComparator()
        self.data_exfiltration_comparator = DataExfiltrationComparator()
        self.cryptojacking_comparator = CryptojackingComparator()
        self.account_comparator = AccountComparator()

    def compare_tags(self, all_prev_tag_metrics: AggregateVersionMetrics, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, package: str, version: str) -> Flags:
        flags = Flags(
            package=package,
            version=version
        )
        flags.generic = self.generic_comparator.compare(curr_tag_metrics, all_prev_tag_metrics)
        flags.evasion = self.evasion_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics)
        flags.payload = self.payload_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics)
        flags.exfiltration = self.data_exfiltration_comparator.compare(curr_tag_metrics, all_prev_tag_metrics)
        flags.crypto = self.cryptojacking_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics)
        flags.account = self.account_comparator.compare(prev_tag_metrics, curr_tag_metrics, all_prev_tag_metrics)
        return flags