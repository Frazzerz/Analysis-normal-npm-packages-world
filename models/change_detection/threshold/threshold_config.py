from dataclasses import dataclass
from typing import Optional
from ...symbol import Symbol

@dataclass
class ThresholdConfig:
    """Configuration for a specific metric threshold"""
    percentage: Optional[float] = None      # For ChangeMetric with percentage
    absolute: Optional[float] = None        # For ChangeMetric with absolute
    boolean: Optional[bool] = None          # For boolean metrics, e.g., obfuscated code introduced. If set, indicates the expected boolean value to trigger
    symbol: Optional[Symbol] = Symbol.NONE  # Symbol to indicate comparison type e.g., greater than, less than
    description: str = ""