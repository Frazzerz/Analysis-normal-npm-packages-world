from dataclasses import dataclass
from .change_metrics import ChangeMetric
from .threshold import ThresholdConfig, GenericThresholdRule
from ..symbol import Symbol
@dataclass
class EvasionChanges:
    obfuscated_code_introduced: bool = False
    minified_code_introduced: bool = False
    hex_obfuscation_patterns: ChangeMetric = ChangeMetric(None, None)
    platform_detections: ChangeMetric = ChangeMetric(None, None)

    THRESHOLDS = [
        GenericThresholdRule(
            name="Obfuscated code introduced",
            metric_path="evasion.obfuscated_code_introduced",
            config=ThresholdConfig(
                boolean=True,
                description="Obfuscated code was introduced in this version",
            ),
        ),
        GenericThresholdRule(
            name="Minified code introduced",
            metric_path="evasion.minified_code_introduced",
            config=ThresholdConfig(
                boolean=True,
                description="Minified code was introduced in this version",
            ),
        ),
        GenericThresholdRule(
            name="Increase hex obfuscation patterns",
            metric_path="evasion.hex_obfuscation_patterns",
            config=ThresholdConfig(
                percentage=1000.0,
                symbol=Symbol.GREATER_THAN,
                description="Hex obfuscation patterns increased significantly",
            ),
        ),
        GenericThresholdRule(                           # to understand
            name="Remove all hex obfuscation patterns",
            metric_path="evasion.hex_obfuscation_patterns",
            config=ThresholdConfig(
                percentage=-100.0,
                symbol=Symbol.LESS_THAN,
                description="Hex obfuscation patterns removed completely in this version",
            ),
        ),
        GenericThresholdRule(
            name="Increase platform detections",        # See better later
            metric_path="evasion.platform_detections",
            config=ThresholdConfig(
                absolute=10.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Platform detections increased significantly",
            ),
        )
    ]