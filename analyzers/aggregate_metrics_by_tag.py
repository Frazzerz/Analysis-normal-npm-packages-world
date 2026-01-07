from zipfile import Path
from models.composed_metrics import FileMetrics, VersionMetrics, AggregateVersionMetrics
from typing import List
from analyzers.categories import AccountAnalyzer
from utils import synchronized_print
from models import CodeType, SourceType

class AggregateMetricsByTag:

    @staticmethod
    def aggregate_metrics_by_tag(metrics_list: List[FileMetrics], repo_path: Path, source: SourceType) -> VersionMetrics:
        """Aggregation of all metrics from the all files in the current version into a single VersionMetrics object"""

        if not metrics_list:
            synchronized_print("Warning: Empty metrics list provided to aggregate_metrics_by_tag")
            return None

        version_metrics = VersionMetrics()
        version_metrics.package = metrics_list[0].package
        #version_metrics.version = str(metrics_list[0].version) # Ensure it's a string, not a git.refs.tag.TagReference
        version_metrics.version = metrics_list[0].version # Ensure it's a string, not a git.refs.tag.TagReference


        # Calculate metrics for account categories
        account = AccountAnalyzer(pkg_name=version_metrics.package)
        account_metrics = account.analyze(version_metrics.version, repo_path, source)
        version_metrics.account.npm_maintainers = account_metrics.npm_maintainers
        version_metrics.account.npm_hash_commit = account_metrics.npm_hash_commit
        #version_metrics.account.github_hash_commit = account_metrics.github_hash_commit
        version_metrics.account.npm_release_date = account_metrics.npm_release_date
    
        # Calculate total file sizes for weighted averages
        for fm in metrics_list:
                # Filter for deobfuscated files, I don't consider the deobfuscated files for these metrics below
                if fm.evasion.code_type != CodeType.DEOBFUSCATED:
                    version_metrics.generic.total_size_chars += fm.generic.size_chars
                    version_metrics.evasion.code_types.append(fm.evasion.code_type)
                    version_metrics.generic.total_files += 1
                    version_metrics.generic.total_size_bytes += fm.generic.size_bytes
                    version_metrics.generic.longest_line_length = max(version_metrics.generic.longest_line_length, fm.generic.longest_line_length)

        for fm in metrics_list:
            version_metrics.evasion.obfuscation_patterns_count += fm.evasion.obfuscation_patterns_count
            version_metrics.evasion.platform_detections_count += fm.evasion.platform_detections_count
            
            version_metrics.payload.timing_delays_count += fm.payload.timing_delays_count
            version_metrics.payload.eval_count += fm.payload.eval_count
            version_metrics.payload.shell_commands_count += fm.payload.shell_commands_count
            version_metrics.payload.preinstall_scripts.extend(fm.payload.preinstall_scripts)

            version_metrics.exfiltration.scan_functions_count += fm.exfiltration.scan_functions_count
            version_metrics.exfiltration.sensitive_elements_count += fm.exfiltration.sensitive_elements_count
            version_metrics.exfiltration.data_transmission_count += fm.exfiltration.data_transmission_count

            version_metrics.crypto.crypto_addresses += fm.crypto.crypto_addresses
            version_metrics.crypto.list_crypto_addresses.extend(fm.crypto.list_crypto_addresses)
            version_metrics.crypto.cryptocurrency_name += fm.crypto.cryptocurrency_name
            version_metrics.crypto.wallet_detection += fm.crypto.wallet_detection
            version_metrics.crypto.replaced_crypto_addresses += fm.crypto.replaced_crypto_addresses
            version_metrics.crypto.hook_provider += fm.crypto.hook_provider
            
            # weighted averages
            if fm.evasion.code_type != CodeType.DEOBFUSCATED:
                # To calculate the average blank space ratio for the version, we need to calculate the weighted average based on character size,
                # so a larger file will have a larger weight on average
                version_metrics.generic.weighted_avg_blank_space_and_character_ratio += fm.generic.blank_space_and_character_ratio * fm.generic.size_chars / version_metrics.generic.total_size_chars if version_metrics.generic.total_size_chars > 0 else 0.0
                # To calculate the shannon entropy of the version, we need to calculate the weighted average based on character size,
                # represent the average information content per character in the version
                version_metrics.generic.weighted_avg_shannon_entropy += fm.generic.shannon_entropy * fm.generic.size_chars / version_metrics.generic.total_size_chars if version_metrics.generic.total_size_chars > 0 else 0.0

        # Remove duplicates in lists (set function)
        version_metrics.evasion.code_types = list(set(version_metrics.evasion.code_types))

        return version_metrics

    @staticmethod
    def aggregate_metrics_incremental(all_previous_metrics: AggregateVersionMetrics, current_metrics: VersionMetrics, count_versions: int, last_version: str) -> AggregateVersionMetrics:
        
        if not current_metrics:
            synchronized_print("Warning: Empty current metrics provided to aggregate_metrics_incremental")
            return None

        c = current_metrics
        # First version case
        if count_versions == 0:
            all_previous_metrics.package = c.package
            all_previous_metrics.versions = c.version

            all_previous_metrics.evasion.avg_obfuscation_patterns_count = c.evasion.obfuscation_patterns_count
            all_previous_metrics.evasion.avg_platform_detections_count = c.evasion.platform_detections_count
            
            all_previous_metrics.payload.avg_timing_delays_count = c.payload.timing_delays_count
            all_previous_metrics.payload.avg_eval_count = c.payload.eval_count
            all_previous_metrics.payload.avg_shell_commands_count = c.payload.shell_commands_count
            
            all_previous_metrics.exfiltration.avg_scan_functions_count = c.exfiltration.scan_functions_count
            all_previous_metrics.exfiltration.avg_sensitive_elements_count = c.exfiltration.sensitive_elements_count
            all_previous_metrics.exfiltration.avg_data_transmission_count = c.exfiltration.data_transmission_count
            
            all_previous_metrics.crypto.avg_crypto_addresses = c.crypto.crypto_addresses
            all_previous_metrics.crypto.avg_cryptocurrency_name = c.crypto.cryptocurrency_name
            all_previous_metrics.crypto.avg_wallet_detection = c.crypto.wallet_detection
            all_previous_metrics.crypto.avg_replaced_crypto_addresses = c.crypto.replaced_crypto_addresses
            all_previous_metrics.crypto.avg_hook_provider = c.crypto.hook_provider
            
            all_previous_metrics.account.avg_npm_maintainers = c.account.npm_maintainers
            
            all_previous_metrics.generic.avg_total_files = c.generic.total_files
            all_previous_metrics.generic.avg_total_size_bytes = c.generic.total_size_bytes
            all_previous_metrics.generic.avg_total_size_chars = c.generic.total_size_chars
            all_previous_metrics.generic.weighted_avg_blank_space_and_character_ratio = c.generic.weighted_avg_blank_space_and_character_ratio
            all_previous_metrics.generic.weighted_avg_shannon_entropy = c.generic.weighted_avg_shannon_entropy
            all_previous_metrics.generic.avg_longest_line_length = c.generic.longest_line_length
            
            return all_previous_metrics

        # General case: aggregate previous and current metrics
        n = count_versions

        all_previous_metrics.versions = f"all up to {last_version} (included) + {c.version} (included)"

        all_previous_metrics.evasion.avg_obfuscation_patterns_count = all_previous_metrics.evasion.avg_obfuscation_patterns_count + (c.evasion.obfuscation_patterns_count - all_previous_metrics.evasion.avg_obfuscation_patterns_count) / (n + 1)
        all_previous_metrics.evasion.avg_platform_detections_count = all_previous_metrics.evasion.avg_platform_detections_count + (c.evasion.platform_detections_count - all_previous_metrics.evasion.avg_platform_detections_count) / (n + 1)

        all_previous_metrics.payload.avg_timing_delays_count = all_previous_metrics.payload.avg_timing_delays_count + (c.payload.timing_delays_count - all_previous_metrics.payload.avg_timing_delays_count) / (n + 1)
        all_previous_metrics.payload.avg_eval_count = all_previous_metrics.payload.avg_eval_count + (c.payload.eval_count - all_previous_metrics.payload.avg_eval_count) / (n + 1)
        all_previous_metrics.payload.avg_shell_commands_count = all_previous_metrics.payload.avg_shell_commands_count + (c.payload.shell_commands_count - all_previous_metrics.payload.avg_shell_commands_count) / (n + 1)

        all_previous_metrics.exfiltration.avg_scan_functions_count = all_previous_metrics.exfiltration.avg_scan_functions_count + (c.exfiltration.scan_functions_count - all_previous_metrics.exfiltration.avg_scan_functions_count) / (n + 1)
        all_previous_metrics.exfiltration.avg_sensitive_elements_count = all_previous_metrics.exfiltration.avg_sensitive_elements_count + (c.exfiltration.sensitive_elements_count - all_previous_metrics.exfiltration.avg_sensitive_elements_count) / (n + 1)
        all_previous_metrics.exfiltration.avg_data_transmission_count = all_previous_metrics.exfiltration.avg_data_transmission_count + (c.exfiltration.data_transmission_count - all_previous_metrics.exfiltration.avg_data_transmission_count) / (n + 1)
        
        all_previous_metrics.crypto.avg_crypto_addresses = all_previous_metrics.crypto.avg_crypto_addresses + (c.crypto.crypto_addresses - all_previous_metrics.crypto.avg_crypto_addresses) / (n + 1)
        all_previous_metrics.crypto.avg_cryptocurrency_name = all_previous_metrics.crypto.avg_cryptocurrency_name + (c.crypto.cryptocurrency_name - all_previous_metrics.crypto.avg_cryptocurrency_name) / (n + 1)
        all_previous_metrics.crypto.avg_wallet_detection = all_previous_metrics.crypto.avg_wallet_detection + (c.crypto.wallet_detection - all_previous_metrics.crypto.avg_wallet_detection) / (n + 1)
        all_previous_metrics.crypto.avg_replaced_crypto_addresses = all_previous_metrics.crypto.avg_replaced_crypto_addresses + (c.crypto.replaced_crypto_addresses - all_previous_metrics.crypto.avg_replaced_crypto_addresses) / (n + 1)
        all_previous_metrics.crypto.avg_hook_provider = all_previous_metrics.crypto.avg_hook_provider + (c.crypto.hook_provider - all_previous_metrics.crypto.avg_hook_provider) / (n + 1)

        all_previous_metrics.account.avg_npm_maintainers = all_previous_metrics.account.avg_npm_maintainers + (c.account.npm_maintainers - all_previous_metrics.account.avg_npm_maintainers) / (n + 1)
        
        all_previous_metrics.generic.avg_total_files = all_previous_metrics.generic.avg_total_files + (c.generic.total_files - all_previous_metrics.generic.avg_total_files) / (n + 1)
        all_previous_metrics.generic.avg_total_size_chars = all_previous_metrics.generic.avg_total_size_chars + (c.generic.total_size_chars - all_previous_metrics.generic.avg_total_size_chars) / (n + 1)
        all_previous_metrics.generic.avg_total_size_bytes = all_previous_metrics.generic.avg_total_size_bytes + (c.generic.total_size_bytes - all_previous_metrics.generic.avg_total_size_bytes) / (n + 1)
        all_previous_metrics.generic.weighted_avg_blank_space_and_character_ratio = all_previous_metrics.generic.weighted_avg_blank_space_and_character_ratio + (c.generic.weighted_avg_blank_space_and_character_ratio - all_previous_metrics.generic.weighted_avg_blank_space_and_character_ratio) / (n + 1)
        all_previous_metrics.generic.avg_longest_line_length = all_previous_metrics.generic.avg_longest_line_length + (c.generic.longest_line_length - all_previous_metrics.generic.avg_longest_line_length) / (n + 1)
        all_previous_metrics.generic.weighted_avg_shannon_entropy = all_previous_metrics.generic.weighted_avg_shannon_entropy + (c.generic.weighted_avg_shannon_entropy - all_previous_metrics.generic.weighted_avg_shannon_entropy) / (n + 1)

        return all_previous_metrics