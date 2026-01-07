from dataclasses import dataclass
from .change_metrics import ChangeMetric
from .threshold import ThresholdConfig, GenericThresholdRule
from ..symbol import Symbol
@dataclass
class ExfiltrationChanges:
    scan_functions: ChangeMetric = ChangeMetric(None, None)
    sensitive_elements: ChangeMetric = ChangeMetric(None, None)
    data_transmission: ChangeMetric = ChangeMetric(None, None)

    THRESHOLDS = [
        GenericThresholdRule(
            name="Increase scan functions",          # See better later
            metric_path="exfiltration.scan_functions",
            config=ThresholdConfig(
                absolute=100.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Scan functions increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Increase sensitive elements",      # See better later
            metric_path="exfiltration.sensitive_elements",
            config=ThresholdConfig(
                absolute=50.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Sensitive elements increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Increase data transmission",       # See better later
            metric_path="exfiltration.data_transmission",
            config=ThresholdConfig(
                absolute=200.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Data transmission increased significantly",
            ),
        )
    ]