from typing import List, Pattern, Tuple

class UtilsForAnalyzer:
    
    @staticmethod
    def detect_patterns(content: str, patterns: List[Pattern]) -> Tuple[int, List[str]]:
        matches = []
        for pattern in patterns:
            for match in pattern.finditer(content):
                matches.append(match.group(0))
        return len(matches), matches
    
    @staticmethod
    def detect_count_patterns(content: str, patterns: List[Pattern]) -> int:
        return sum(1 for pattern in patterns for _ in pattern.finditer(content))