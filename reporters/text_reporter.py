from pathlib import Path
from utils import synchronized_print
class TextReporter:
    """Generate flag text report considering all flag fields"""

    @staticmethod
    def generate_log_txt(pkg_dir: Path, package: str, output_buffer: str) -> None:
        """Generate log file with the captured output during analysis"""
        pkg_output_file = pkg_dir / f"{package.replace('/', '_')}.txt"
        captured_output = output_buffer.getvalue()

        with open(pkg_output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== Analysis of {package} ===\n")
            f.write(captured_output)