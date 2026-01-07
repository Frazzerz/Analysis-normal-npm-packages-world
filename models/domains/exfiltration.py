from dataclasses import dataclass, field
from typing import List

@dataclass
class ExfiltrationMetrics:
    scan_functions_count: int = 0
    list_scan_functions: List[str] = field(default_factory=list)
    sensitive_elements_count: int = 0
    list_sensitive_elements: List[str] = field(default_factory=list)
    data_transmission_count: int = 0
    list_data_transmissions: List[str] = field(default_factory=list)