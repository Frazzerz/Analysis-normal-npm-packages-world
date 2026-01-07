from pathlib import Path
from typing import List
import json
import shutil
import os

class FileHandler:
    """Handles file and directory operations"""
    
    @staticmethod
    def load_packages_from_json(path: str) -> List[str]:
        """Load package names from a JSON file"""        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [data] if isinstance(data, str) else data
        except Exception as e:
            raise SystemExit(f"Error reading JSON {path}: {e}")
    
    @staticmethod
    def get_all_files(directory: Path) -> List[Path]:
        """Find all files in directory (recursive) excluding certain directories, files and extensions."""
        '''
         Excluded: Also auto-generated file (like yarn.lock)
         not excluded: README.md, package.json, all .js .mjs .ts .cjs .js.map files
        exclude_dirs = {'.git', 'node_modules', '.github', '__tests__', 'test', 'tests'}
        exclude_files = {
            'LICENSE', '.npmrc', '.editorconfig', '.gitattributes', 'license',
            '.eslintrc', '.prettierrc', 'CHANGELOG.md', '.eslintignore', 'yarn.lock', '.gitignore', '.prettierignore'
        }
        exclude_suffixes = ('d.ts', '.d.ts.map', '.png', '.jpg', '.jpeg', '.ai', '.svg', '.gif', 'ico', '.eot', '.ttf',
                             '.woff', '.woff2', '.mp4', '.mp3', '.mov', '.map')
        '''
        files: List[Path] = []
        directory_str = str(directory)
        for root, dirs, filenames in os.walk(directory_str):
            #dirs[:] = [d for d in dirs if d not in exclude_dirs]   # dirs contains names (not full paths)
            for name in filenames:
                '''
                if name in exclude_files:
                    continue
                if name.endswith(exclude_suffixes):
                    continue
                '''
                files.append(Path(root) / name)
        return files
    
    @staticmethod
    def read_file(file_path: Path) -> str:
        """Read file content and remove comments"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                '''
                js_extensions = {'.js', '.mjs', '.cjs', '.ts', '.jsx', '.tsx'}
                if file_path.suffix.lower() in js_extensions:
                    content = FileHandler.remove_js_comments_easy(content)
                '''    
                return content
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

    @staticmethod
    def delete_previous_analysis() -> None:
        """Delete all results from previous analysis (repos, other_versions/extracted, log file, output directory) #deobfuscated_files"""
        dirs_to_delete = ['other_versions/extracted', 'analysis_results']    # tarballs, deobfuscated_files, repos,  other_versions/extracted
        for dir_name in dirs_to_delete:
            dir_path = Path(dir_name)
            if dir_path.exists() and dir_path.is_dir():
                shutil.rmtree(dir_path)
                #print(f"Deleted directory: {dir_path}")

        log_file = Path('log.txt')
        if log_file.exists() and log_file.is_file():
            log_file.unlink()
            #print(f"Deleted log file: {log_file}")
    
    @staticmethod
    def delete_tarballs(package: str) -> None:
        """Delete downloaded tarballs for a specific package"""
        tarball_dir = Path("tarballs") / package.replace('/', '_')
        if tarball_dir.exists() and tarball_dir.is_dir():
            shutil.rmtree(tarball_dir)
            #print(f"Deleted tarballs directory: {tarball_dir}")

    '''
    # Too fragile, better to use a proper JS parser
    @staticmethod
    def remove_js_comments_easy(content: str) -> str:
        """Remove JavaScript comments from content, only if starting at the beginning of the line"""
        out = []
        in_block = False

        for line in content.splitlines():
            stripped = line.lstrip()

            # inside /* ... */
            if in_block:
                if "*/" in stripped:
                    in_block = False
                    # preserve any code after */
                    after = stripped.split("*/", 1)[1]
                    if after.strip():
                        out.append(after)
                continue

            # comment //
            if stripped.startswith("//"):
                continue

            # comment /* */
            if stripped.startswith("/*"):
                if "*/" not in stripped:
                    in_block = True
                # preserve any code after */
                after = stripped.split("*/", 1)[1] if "*/" in stripped else ""
                if after.strip():
                    out.append(after)
                continue

            out.append(line)

        return "\n".join(out)
    '''