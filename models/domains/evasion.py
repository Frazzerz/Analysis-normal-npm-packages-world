from dataclasses import dataclass, field
from typing import List
from ..code_type import CodeType
@dataclass
class EvasionMetrics:
    code_type: CodeType = CodeType.NONE
    obfuscation_patterns_count: int = 0
    list_obfuscation_patterns: List[str] = field(default_factory=list)
    platform_detections_count: int = 0
    list_platform_detections: List[str] = field(default_factory=list)
