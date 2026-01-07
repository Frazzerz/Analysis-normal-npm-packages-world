from models.change_detection.change_metrics import ChangeMetric
from .threshold_config import ThresholdConfig
from typing import Any
from utils import synchronized_print
from ...symbol import Symbol

class ThresholdEvaluator:

    @staticmethod
    def get_value(flag: Any, path: str):
        for part in path.split("."):
            flag = getattr(flag, part)
        return flag

    @staticmethod
    def is_triggered(value: ChangeMetric, config: ThresholdConfig) -> bool:
        #synchronized_print(f"Evaluating value: {value} with config: {config}")
        #if value is None:
        #        synchronized_print("Value is None case")
        #        return False
        if config.boolean:
                # In this case, value is expected to be a boolean
                if not isinstance(value, bool):
                        #synchronized_print(f"Expected boolean value for threshold evaluation, got: {value}")
                        return False
                #synchronized_print("bool case")
                return value == config.boolean
        
        if config.symbol == Symbol.NONE or (value.percentage is None and value.absolute is None):
                #synchronized_print("No symbol or no value case")
                return False
        
        if value.percentage != 'inf' and value.percentage is not None and config.percentage is not None:
                #synchronized_print("Common case")
                return config.symbol.value(value.percentage, config.percentage)
        elif value.absolute is not None and config.absolute is not None:
                #synchronized_print("Rare case")
                return config.symbol.value(value.absolute, config.absolute)
        else:
                #synchronized_print("Here value and config absolute must be present")
                return False