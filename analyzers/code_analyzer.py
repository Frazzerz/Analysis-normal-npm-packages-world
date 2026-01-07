from pathlib import Path
from typing import Dict
from .categories import EvasionAnalyzer, PayloadAnalyzer, DataExfiltrationAnalyzer, CryptojackingAnalyzer, GenericAnalyzer
from models.composed_metrics import FileMetrics
from utils import FileHandler, synchronized_print
class CodeAnalyzer:
    """Coordinates analysis across all categories"""
    
    def __init__(self):
        self.generic_analyzer = GenericAnalyzer()
        self.evasion_analyzer = EvasionAnalyzer()
        self.payload_analyzer = PayloadAnalyzer()
        self.data_exfiltration_analyzer = DataExfiltrationAnalyzer()
        self.cryptojacking_analyzer = CryptojackingAnalyzer()

    def analyze_file(self, file_path: Path, package_info: Dict) -> FileMetrics:
        """Analyze a single file and return all metrics"""
        metrics = FileMetrics(
            package=package_info['name'],
            version=package_info['version'],
            file_path=package_info['file_name'],
        )
        content = FileHandler().read_file(file_path)
        metrics.generic = self.generic_analyzer.analyze(content)
        metrics.evasion = self.evasion_analyzer.analyze(content, package_info)
        metrics.payload = self.payload_analyzer.analyze(content, package_info)
        metrics.exfiltration = self.data_exfiltration_analyzer.analyze(content)
        metrics.crypto = self.cryptojacking_analyzer.analyze(content)
        return metrics