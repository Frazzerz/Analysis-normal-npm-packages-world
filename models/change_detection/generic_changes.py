from dataclasses import dataclass
from .change_metrics import ChangeMetric
from .threshold import ThresholdConfig, GenericThresholdRule
from ..symbol import Symbol

@dataclass
class GenericChanges:
    total_files: ChangeMetric = ChangeMetric(None, None)
    size_bytes: ChangeMetric = ChangeMetric(None, None)
    weighted_avg_blank_space_and_character_ratio: ChangeMetric = ChangeMetric(None, None)
    weighted_avg_shannon_entropy: ChangeMetric = ChangeMetric(None, None)
    longest_line_length: ChangeMetric = ChangeMetric(None, None)

    THRESHOLDS = [
        GenericThresholdRule(
            name="Increase total files",            # normal rule
            metric_path="generic.total_files",
            config=ThresholdConfig(
                percentage=100.0,
                symbol=Symbol.GREATER_THAN,
                description="Number of files increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Decrease total files",            # normal rule
            metric_path="generic.total_files",
            config=ThresholdConfig(
                percentage=-100.0,
                symbol=Symbol.LESS_THAN,
                description="Number of files decreased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Increase package size",
            metric_path="generic.size_bytes",
            config=ThresholdConfig(
                percentage=200.0,
                symbol=Symbol.GREATER_THAN,
                description="Package size increased significantly",
            ),
        ),
        GenericThresholdRule(                       # to understand
            name="Decrease package size",
            metric_path="generic.size_bytes",
            config=ThresholdConfig(
                percentage=-100.0,
                symbol=Symbol.LESS_THAN,
                description="Package size decreased significantly",
            ),
        ),
        GenericThresholdRule(                       # to understand
            name="Increase weighted average blank space and character ratio",
            metric_path="generic.weighted_avg_blank_space_and_character_ratio",
            config=ThresholdConfig(
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Significant increase in blank space and character ratio",
            ),
        ),
        GenericThresholdRule(
            name="Decrease weighted average blank space and character ratio",
            metric_path="generic.weighted_avg_blank_space_and_character_ratio",
            config=ThresholdConfig(
                percentage=-50.0,
                symbol=Symbol.LESS_THAN,
                description="Significant decrease in blank space and character ratio",
            ),
        ),
        GenericThresholdRule(
            name="Increase weighted average Shannon entropy",
            metric_path="generic.weighted_avg_shannon_entropy",
            config=ThresholdConfig(
                percentage=5.0,
                symbol=Symbol.GREATER_THAN,
                description="Significant increase in Shannon entropy",
            ),
        ),
        GenericThresholdRule(                       # to understand
            name="Decrease weighted average Shannon entropy",
            metric_path="generic.weighted_avg_shannon_entropy",
            config=ThresholdConfig(
                percentage=-0.5,
                symbol=Symbol.LESS_THAN,
                description="Significant decrease in Shannon entropy",
            ),
        ),
        GenericThresholdRule(
            name="Increase longest line length",
            metric_path="generic.longest_line_length",
            config=ThresholdConfig(
                percentage=10000,
                symbol=Symbol.GREATER_THAN,
                description="Significant increase in longest line length",
            ),
        ),
    ]
