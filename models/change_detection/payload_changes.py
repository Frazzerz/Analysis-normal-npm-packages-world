from dataclasses import dataclass
from .change_metrics import ChangeMetric
from .threshold import ThresholdConfig, GenericThresholdRule
from ..symbol import Symbol
@dataclass
class PayloadChanges:
    timing_delays: ChangeMetric = ChangeMetric(None, None)
    eval_function: ChangeMetric = ChangeMetric(None, None)
    shell_commands: ChangeMetric = ChangeMetric(None, None)
    preinstall_scripts_introduced: bool = False
    preinstall_scripts_change: bool = False

    THRESHOLDS = [
        GenericThresholdRule(
            name="Increase timing delays",          # See better later
            metric_path="payload.timing_delays",
            config=ThresholdConfig(
                absolute=500.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Timing delays increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Increase eval function usage",    # See better later
            metric_path="payload.eval_function",
            config=ThresholdConfig(
                absolute=100.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Eval function usage increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Increase shell commands",        # See better later
            metric_path="payload.shell_commands",
            config=ThresholdConfig(
                absolute=50.0,
                percentage=50.0,
                symbol=Symbol.GREATER_THAN,
                description="Shell commands usage increased significantly",
            ),
        ),
        GenericThresholdRule(
            name="Preinstall scripts introduced",
            metric_path="payload.preinstall_scripts_introduced",
            config=ThresholdConfig(
                boolean=True,
                description="Preinstall scripts were introduced in this version",
            ),
        ),
        GenericThresholdRule(
            name="Preinstall scripts changed",
            metric_path="payload.preinstall_scripts_change",
            config=ThresholdConfig(
                boolean=True,
                description="Preinstall scripts were changed in this version",
            ),
        )
    ]