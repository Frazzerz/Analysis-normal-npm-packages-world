from pathlib import Path
import time
import contextlib
from io import StringIO
from analyzers import PackageAnalyzer
from reporters import TextReporter, GraphReporter
from utils import FileHandler

def analyze_single_package(package, out_dir, package_index, total_packages, include_local, local_dir, workers) -> None:
    """Analyzing a single npm package with optional local versions"""
    pkg_dir = Path(out_dir) / package.replace('/', '_')
    pkg_dir.mkdir(parents=True, exist_ok=True)

    start_time = time.time()
    print(f"[{package_index}/{total_packages}] Analyzing {package}...")
    analyzer = PackageAnalyzer(include_local=include_local, local_versions_dir=local_dir, workers=workers, package_name=package, output_dir=pkg_dir)

    txt_flags_summary_path = pkg_dir / f"{package.replace('/', '_')}_flags_summary.txt"
    TextReporter.initialize_report(txt_flags_summary_path, package)

    # Capture the output of analyze_package
    output_buffer = StringIO()
    with contextlib.redirect_stdout(output_buffer):
        analyzer.analyze_package()

    TextReporter().generate_log_txt(pkg_dir, package, output_buffer)
    TextReporter().finish_report(txt_flags_summary_path)
    GraphReporter().generate_graphs(pkg_dir, package)
    #FileHandler().delete_tarballs(package)

    elapsed_time = time.time() - start_time
    print(f"[{package_index}/{total_packages}] Completed: {package} ({elapsed_time:.1f}s)")