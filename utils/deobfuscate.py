from pathlib import Path
import subprocess
from utils import synchronized_print, OutputTarget
from shutil import copy2
class Deobfuscator:

    @staticmethod
    def deobfuscate(path_original_file: Path, package_name: str, version: str, file_name: str) -> bool:
        """Deobfuscates a JavaScript file using the obfuscator-io-deobfuscator tool, saves the output to a structured directory, and returns True if successful."""
        synchronized_print(f"    Try to deobfuscate file: {file_name}, version {version}", target=OutputTarget.FILE_ONLY)
        
        file_path = Path(file_name)  # es: src/index.js
        # base dir: deobfuscated_files/pkg/version/
        base_dir = Path("deobfuscated_files") / package_name.replace('/', '_') / version
        base_dir.mkdir(parents=True, exist_ok=True)

        # destination of the original file (with subfolders)
        dest_original_file = base_dir / file_path
        dest_original_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            copy2(path_original_file, dest_original_file)
        except Exception as e:
            synchronized_print(f"    Failed to copy original file to {dest_original_file}: {e}", target=OutputTarget.FILE_ONLY)
            return False

        # output in the same folder
        output_file = dest_original_file.with_name(f"{dest_original_file.stem}-deobfuscated.js")

        if output_file.exists():
            synchronized_print(f"    Deobfuscated file already exists: {output_file}. Skipping.", target=OutputTarget.FILE_ONLY)
            return True

        command = ['obfuscator-io-deobfuscator', str(dest_original_file), '-o', str(output_file)]

        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)    
            if result.returncode == 0:
                synchronized_print(f"    Success! Deobfuscated file saved to: {output_file}", target=OutputTarget.FILE_ONLY)
                return True
                
        except Exception as e:
            error_msg = str(e).lower()
            if 'timed out' in error_msg:
                synchronized_print(f"    Deobfuscation process timed out for file: {file_name}", target=OutputTarget.FILE_ONLY)
            else:
                synchronized_print(f"    An error occurred during deobfuscation of file {file_name}: {e}", target=OutputTarget.FILE_ONLY)
        return False