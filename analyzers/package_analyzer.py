from pathlib import Path
from utils import NPMClient
from utils.logging_utils import OutputTarget
from .version_analyzer import VersionAnalyzer
from git import Repo
from utils import synchronized_print
from models import VersionEntry
from packaging.version import InvalidVersion
from analyzers.local_version_analyzer import LocalVersionAnalyzer
import re

class PackageAnalyzer:
    """Coordinator for analyzing Git and local versions of an npm package"""
    def __init__(self, include_local: bool = False, local_versions_dir: str = "./other_versions", workers: int = 1, package_name: str = "", output_dir: Path = Path(".")):
        self.pkg_name = package_name
        self.output_dir = output_dir
        self.npm_client = NPMClient(pkg_name=package_name)
        self.include_local = include_local
        self.local_versions_dir = local_versions_dir
        self.version_analyzer = VersionAnalyzer(
            max_processes=workers,
            include_local=include_local,
            local_versions_dir=local_versions_dir,
            package_name=package_name,
            output_dir=output_dir
        )
        
    def analyze_package(self) -> None:
        """Analyze all releases of a package"""
        '''
        repo = self.npm_client.clone_package_repo()
        if repo:
            self.analyze_git_and_local_versions(repo)
        else:
            print(f"Unable to analyze {self.pkg_name} - Git repository not available")
        '''
        entries = self.npm_client.download_package_versions_tarball()
        if not entries:
            synchronized_print(f"Unable to analyze {self.pkg_name} - No versions available")
            return
        if self.include_local:
            #synchronized_print(f"Including local versions in tarball analysis for {self.pkg_name}", target=OutputTarget.TERMINAL_ONLY)
            localversionanalyzer = LocalVersionAnalyzer(local_versions_dir=self.local_versions_dir, pkg_name=self.pkg_name)
            localversionanalyzer.setup_local_versions()
            entries = localversionanalyzer.unite_versions(entries)
        self.version_analyzer.entries = entries
        self.version_analyzer.analyze_versions()
        
    '''
    def analyze_git_and_local_versions(self, repo: Repo) -> None:
        """Analyze versions from Git tags and local versions"""

        # tags == [<git.TagReference "refs/tags/1.0.5">, <git.TagReference "refs/tags/posthog-node@5.18.0">, ...]
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        if not tags:
            synchronized_print(f"No tags found for {self.pkg_name}")
            return []
        synchronized_print(f"Found {len(tags)} Git tags")

        tags = self.filter_tags(tags)
        if not tags:
            synchronized_print(f"No valid tags found for package {self.pkg_name} after filtering")
            return []
        synchronized_print(f"Analyzing only the last {len(tags)} Git tags")

        entries = []
        for tag in tags:
            try:
                entries.append(VersionEntry(name=tag, source="git", ref=tag))
            except InvalidVersion as e:
                synchronized_print(f"Skipping tag, invalid version '{tag}': {e}")
            except Exception as e:
                synchronized_print(f"Skipping tag {tag} due to unexpected error: {e}")
            
        if self.include_local:
            synchronized_print(f"Including local versions in Git analysis for {self.pkg_name}")
            localversionanalyzer = LocalVersionAnalyzer(local_versions_dir=self.local_versions_dir, pkg_name=self.pkg_name)
            localversionanalyzer.setup_local_versions()
            entries = localversionanalyzer.unite_versions(entries)
        
        self.version_analyzer.entries = entries
        self.version_analyzer.repo = repo
        self.version_analyzer.analyze_versions()

    def filter_tags(self, tags: list) -> list:
        """Filter the tags that i'm looking for and take the last 50. The repo could be a monorepo containing multiple packages (that i don't care).
           I assume that inside the tag there is the exact name of the package I'm looking for. E.g. posthog-node@5.18.1
        """
        filtered_tags = []
        for tag in reversed(tags):
            if len(filtered_tags) >= 2: # Limit to last 2 tags
                break
            tag_name = tag.name
            # Tags that contain the package name
            if self.pkg_name in tag_name:
                # Check that there is also a version in the tag
                if re.search(r'\d+(\.\d+)*', tag_name):
                    filtered_tags.append(tag)
                    continue
            # Tags that are just version numbers
            if re.match(r'^v?\d+(\.\d+)*$', tag_name):
                filtered_tags.append(tag)
                continue
            
        filtered_tags.reverse()
        #synchronized_print(f"Filtered tags: {filtered_tags}")
        return filtered_tags
    '''