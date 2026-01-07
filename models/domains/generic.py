from dataclasses import dataclass

@dataclass
class GenericMetrics:
    size_bytes: int = 0
    size_chars: int = 0
    blank_space_and_character_ratio: float = 0.0
    shannon_entropy: float = 0.0
    longest_line_length: int = 0