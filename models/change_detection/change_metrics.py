from dataclasses import dataclass
from typing import Optional

@dataclass
class ChangeMetric:
    absolute: Optional[float]
    percentage: Optional[float]