from dataclasses import dataclass
from .threshold_config import ThresholdConfig

@dataclass
class GenericThresholdRule:
    name: str                       # e.g. increase_total_files
    metric_path: str                # e.g. generic.total_files.percentage
    config: ThresholdConfig
