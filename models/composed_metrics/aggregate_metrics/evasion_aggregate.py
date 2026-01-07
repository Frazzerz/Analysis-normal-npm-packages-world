from typing import List
from dataclasses import dataclass, field

@dataclass
class EvasionVersion:
    """For a single version"""
    code_types: List[str] = field(default_factory=list)
    obfuscation_patterns_count: int = 0
    platform_detections_count: int = 0

@dataclass
class EvasionAggregate:
    """For aggregate versions"""
    avg_obfuscation_patterns_count: int = 0
    avg_platform_detections_count: int = 0