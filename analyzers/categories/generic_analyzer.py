import math
from models.domains import GenericMetrics
from utils import synchronized_print

class GenericAnalyzer:
    """Obtain generic metrics from files"""

    def analyze(self, content: str) -> GenericMetrics:
        generic = GenericMetrics()

        if not content:
            return generic
        
        generic.size_bytes = len(content.encode("utf-8"))
        generic.size_chars = len(content)
        whitespace_count = sum(1 for c in content if c.isspace())
        generic.blank_space_and_character_ratio = whitespace_count / generic.size_chars if content else 0.0
        generic.shannon_entropy = self._calculate_shannon_entropy(content)
        ##no_empty_lines = len([r for r in content.splitlines() if r.strip()])

        generic.longest_line_length = max(len(r) for r in content.splitlines()) if content.splitlines() else 0
        return generic

    def _calculate_shannon_entropy(self, content: str) -> float:
        """Calculate Shannon entropy of the content"""
        if not content:
            return 0.0

        # Calculate frequency of each character in the content
        freq = {}
        for char in content:
            freq[char] = freq.get(char, 0) + 1

        # Calculate the Shannon entropy
        entropy = 0.0
        length = len(content)
        for count in freq.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        return entropy