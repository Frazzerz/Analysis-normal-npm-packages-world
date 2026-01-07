from dataclasses import dataclass

@dataclass
class ExfiltrationVersion:
    """For a single version"""
    scan_functions_count: int = 0
    sensitive_elements_count: int = 0
    data_transmission_count: int = 0

@dataclass
class ExfiltrationAggregate:
    """For aggregate versions"""
    avg_scan_functions_count: int = 0
    avg_sensitive_elements_count: int = 0
    avg_data_transmission_count: int = 0