from dataclasses import dataclass

@dataclass
class GenericVersion:
    """For a single version"""
    total_files: int = 0
    total_size_bytes: bytes = 0
    total_size_chars: int = 0
    weighted_avg_blank_space_and_character_ratio: float = 0
    weighted_avg_shannon_entropy: float = 0
    longest_line_length: int = 0
    
@dataclass
class GenericAggregate:
    """For aggregate versions"""
    avg_total_files: int = 0
    avg_total_size_bytes: bytes = 0
    avg_total_size_chars: int = 0
    weighted_avg_blank_space_and_character_ratio: float = 0
    weighted_avg_shannon_entropy: float = 0
    avg_longest_line_length: int = 0