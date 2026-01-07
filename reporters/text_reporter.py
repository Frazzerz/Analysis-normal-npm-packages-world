from pathlib import Path
from models.change_detection import Flags
from models.change_detection.threshold.threshold_evaluator import ThresholdEvaluator
from utils import synchronized_print
class TextReporter:
    """Generate flag text report considering all flag fields"""

    @staticmethod
    def initialize_report(output_dir: Path, package: str) -> None:
        with open(output_dir, "w", encoding="utf-8") as f:
            f.write(f"FLAGS REPORT - Package: {package}\n")
            f.write("=" * 60 + "\n\n")
    
    @staticmethod
    def generate_report(output_dir: Path, flag: Flags) -> None:
        with open(output_dir, "a", encoding="utf-8") as f:
            bullets = []

            for rule in flag.iterate_thresholds():
                value = ThresholdEvaluator.get_value(flag, rule.metric_path)

                if value is None:
                    continue
                if not ThresholdEvaluator.is_triggered(value, rule.config):
                    continue

                base = f"  • {rule.name} ({rule.config.description})."
                if (getattr(value, "percentage", None) is not None and not value.percentage == 'inf'):
                    detail = f"     Value percentage: {value.percentage:.2f}%.  Threshold: {rule.config.percentage:.2f}%."
                elif getattr(value, "absolute", None) is not None:
                    detail = f"     Value absolute: {value.absolute:.2f}.   Threshold: {rule.config.absolute:.2f}."
                else:
                    detail = f"     Value: {value}."
                bullets.append(f"{base}\n{detail}")

            if bullets:
                f.write(f"Version: {flag.version}. Find {len(bullets)} flags\n")
                f.write("\n".join(bullets))
                f.write("\n\n")

    @staticmethod
    def finish_report(output_dir: Path) -> None:
        with open(output_dir, "r+", encoding="utf-8") as f:
            content = f.read()
            if "Version:" not in content:
                f.write("No flags found.\n")

    @staticmethod
    def generate_log_txt(pkg_dir: Path, package: str, output_buffer: str) -> None:
        """Generate log file with the captured output during analysis"""
        pkg_output_file = pkg_dir / f"{package.replace('/', '_')}.txt"
        captured_output = output_buffer.getvalue()

        with open(pkg_output_file, 'w', encoding='utf-8') as f:
            f.write(f"=== Analysis of {package} ===\n")
            f.write(captured_output)

    '''
    @staticmethod
    def generate_report(output_dir: Path, flag: Flags) -> None:
        with open(output_dir, "a", encoding="utf-8") as f:
            bullets = [
                f"  • {rule.name} ({rule.config.description})."
                f"    Value per: {value}"
                for rule in flag.iterate_thresholds()
                if ThresholdEvaluator.is_triggered(
                    value := ThresholdEvaluator.get_value(flag, rule.metric_path),
                    rule.config,
                )
            ]
            if bullets:
                f.write(f"Version: {flag.version}\n")
                f.write("\n".join(bullets))
                f.write("\n\n")
    '''