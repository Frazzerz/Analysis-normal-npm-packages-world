import math
from typing import Tuple
from models.domains import GenericMetrics
from models import CodeType
import jsbeautifier
class GenericAnalyzer:
    """Obtain generic metrics from files"""

    def pre_analyze_js(self, content: str) -> Tuple[int, int, float, float, int, int]:
        """Pre-analyze JavaScript code to get basic metrics"""
        num_chars = len(content)
        num_lines = self._count_non_blank_lines(content)
        entropy = self._calculate_shannon_entropy(content)
        ws_ratio, num_ws, num_printable = self._w_p_ratio(content)
        return num_chars, num_lines, entropy, ws_ratio, num_ws, num_printable

    def analyze(self, content: str, num_chars: int, num_lines: int, 
                num_comments: int, entropy_orig: float, ws_ratio_orig: float,
                num_ws: int, num_printable: int) -> GenericMetrics:
        """Analyze content and return generic metrics"""
        metrics = GenericMetrics()
        
        # Calculate metrics (with or without pre-computed values)
        metrics.number_of_characters = num_chars if num_chars > 0 else len(content)
        metrics.number_of_characters_no_comments = len(content)
        
        metrics.total_number_of_non_blank_lines = num_lines if num_lines > 0 else self._count_non_blank_lines(content)
        metrics.number_of_non_blank_lines_no_comments = self._count_non_blank_lines(content)
        
        metrics.number_of_comments = num_comments
        
        # Entropy metrics
        if entropy_orig > 0:
            metrics.shannon_entropy_original = entropy_orig
            metrics.shannon_entropy_no_comments = self._calculate_shannon_entropy(content)
        else:
            metrics.shannon_entropy_original = self._calculate_shannon_entropy(content)
            metrics.shannon_entropy_no_comments = metrics.shannon_entropy_original
        
        # Whitespace ratio metrics
        if ws_ratio_orig > 0:
            metrics.blank_space_and_character_ratio_original = ws_ratio_orig
            ws_ratio_nc, num_ws_nc, num_p_nc = self._w_p_ratio(content)
            metrics.blank_space_and_character_ratio_no_comments = ws_ratio_nc
            
            metrics.number_of_whitespace_characters = num_ws
            metrics.number_of_whitespace_characters_no_comments = num_ws_nc
            metrics.number_of_printable_characters = num_printable
            metrics.number_of_printable_characters_no_comments = num_p_nc
        else:
            ws_ratio, ws_count, p_count = self._w_p_ratio(content)
            metrics.blank_space_and_character_ratio_original = ws_ratio
            metrics.blank_space_and_character_ratio_no_comments = ws_ratio
            
            metrics.number_of_whitespace_characters = ws_count
            metrics.number_of_whitespace_characters_no_comments = ws_count
            metrics.number_of_printable_characters = p_count
            metrics.number_of_printable_characters_no_comments = p_count
        
        metrics.longest_line_length_no_comments = max((len(line) for line in content.splitlines()), default=0)
        
        minified = self._detect_minified_code(metrics.longest_line_length_no_comments, metrics.number_of_whitespace_characters_no_comments, metrics.number_of_non_blank_lines_no_comments)
        metrics.code_type = CodeType.MINIFIED if minified else CodeType.CLEAR

        if metrics.code_type == CodeType.MINIFIED:
            unminified_content = self.unminify_code(content)
            metrics.number_of_characters_no_comments_unminified = len(unminified_content)
            metrics.shannon_entropy_no_comments_unminified = self._calculate_shannon_entropy(unminified_content)
            metrics.blank_space_and_character_ratio_no_comments_unminified, metrics.number_of_whitespace_characters_no_comments_minified, _ = self._w_p_ratio(unminified_content)
        else:
            metrics.number_of_characters_no_comments_unminified = 0
            metrics.shannon_entropy_no_comments_unminified = 0.0
            metrics.blank_space_and_character_ratio_no_comments_unminified = 0.0
            metrics.number_of_whitespace_characters_no_comments_minified = 0

        metrics.is_plain_text_file = True
        
        return metrics

    def _count_non_blank_lines(self, content: str) -> int:
        """Count non-blank lines"""
        return len([line for line in content.splitlines() if line.strip()])

    def _calculate_shannon_entropy(self, content: str) -> float:
        """Calculate Shannon entropy of the content"""
        if not content:
            return 0.0
        
        freq = {}
        for char in content:
            freq[char] = freq.get(char, 0) + 1
        
        entropy = 0.0
        length = len(content)
        for count in freq.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _w_p_ratio(self, content: str) -> Tuple[float, int, int]:
        """Calculate the whitespace to printable character ratio"""
        w = sum(1 for c in content if c.isspace())
        p = len(content) - w
        w_p_ratio = w / p if p > 0 else float("inf")
        return w_p_ratio, w, p
    
    def _detect_minified_code(self, longest_line: int, number_of_whitespace_characters: int, num_lines: int) -> bool:
        """Detect if code is minified"""
        return (longest_line > 500 or number_of_whitespace_characters == 0) and num_lines < 2
    
    def unminify_code(self, content: str) -> str:
        """Attempt to unminify code"""
        return jsbeautifier.beautify(content)