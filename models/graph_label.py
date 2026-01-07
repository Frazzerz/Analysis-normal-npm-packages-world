from dataclasses import dataclass

@dataclass
class GraphLabel:
    """Class containing labels and titles for graphing metrics evolution"""
    # Structure: category -> metrics
    # Each metric: (version_column, aggregate_column, display_label)
    METRICS = {
        'GENERIC_METRICS': {
            'title': 'Generic metrics',
            'metrics': {
                'generic.total_files': (
                    'generic.total_files',
                    'generic.avg_total_files',
                    'Total files'
                ),
                'generic.total_size_bytes': (
                    'generic.total_size_bytes',
                    'generic.avg_total_size_bytes',
                    'Total size (bytes)'
                ),
                'generic.weighted_avg_blank_space_and_character_ratio': (
                    'generic.weighted_avg_blank_space_and_character_ratio',
                    'generic.weighted_avg_blank_space_and_character_ratio',
                    'Weighted avg blank space ratio'
                ),
                'generic.weighted_avg_shannon_entropy': (
                    'generic.weighted_avg_shannon_entropy',
                    'generic.weighted_avg_shannon_entropy',
                    'Weighted avg Shannon entropy'
                ),
                'generic.longest_line_length': (
                    'generic.longest_line_length',
                    'generic.avg_longest_line_length',
                    'Longest line length'
                ),
            }
        },
        'EVASION_TECHNIQUES': {
            'title': 'Evasion techniques metrics',
            'metrics': {
                'evasion.obfuscation_patterns_count': (
                    'evasion.obfuscation_patterns_count',
                    'evasion.avg_obfuscation_patterns_count',
                    'Total count obfuscation patterns'
                ),
                'evasion.platform_detections_count': (
                    'evasion.platform_detections_count',
                    'evasion.avg_platform_detections_count',
                    'Total count platform detections'
                ),
            }
        },
        'PAYLOAD_DELIVERY_EXECUTION': {
            'title': 'Payload delivery & Execution metrics',
            'metrics': {
                'payload.timing_delays_count': (
                    'payload.timing_delays_count',
                    'payload.avg_timing_delays_count',
                    'Total count timing delays'
                ),
                'payload.eval_count': (
                    'payload.eval_count',
                    'payload.avg_eval_count',
                    'Total count eval calls'
                ),
                'payload.shell_commands_count': (
                    'payload.shell_commands_count',
                    'payload.avg_shell_commands_count',
                    'Total count shell commands'
                ),
            }
        },
        'DATA_EXFILTRATION_C2': {
            'title': 'Data exfiltration & C2 metrics',
            'metrics': {
                'exfiltration.scan_functions_count': (
                    'exfiltration.scan_functions_count',
                    'exfiltration.avg_scan_functions_count',
                    'Total count scan functions'
                ),
                'exfiltration.sensitive_elements_count': (
                    'exfiltration.sensitive_elements_count',
                    'exfiltration.avg_sensitive_elements_count',
                    'Total count sensitive elements'
                ),
                'exfiltration.data_transmission_count': (
                    'exfiltration.data_transmission_count',
                    'exfiltration.avg_data_transmission_count',
                    'Total count data transmissions'
                ),
            }
        },
        'CRYPTOJACKING_WALLET_THEFT': {
            'title': 'Cryptojacking & Wallet theft metrics',
            'metrics': {
                'crypto.crypto_addresses': (
                    'crypto.crypto_addresses',
                    'crypto.avg_crypto_addresses',
                    'Total count crypto addresses'
                ),
                'crypto.cryptocurrency_name': (
                    'crypto.cryptocurrency_name',
                    'crypto.avg_cryptocurrency_name',
                    'Total count cryptocurrency names'
                ),
                'crypto.wallet_detection': (
                    'crypto.wallet_detection',
                    'crypto.avg_wallet_detection',
                    'Total count wallet detections'
                ),
                'crypto.replaced_crypto_addresses': (
                    'crypto.replaced_crypto_addresses',
                    'crypto.avg_replaced_crypto_addresses',
                    'Total count replaced addresses'
                ),
                'crypto.hook_provider': (
                    'crypto.hook_provider',
                    'crypto.avg_hook_provider',
                    'Total count hook providers'
                ),
            }
        },
        'ACCOUNT_COMPROMISE': {
            'title': 'Account compromise & Integrity anomalies',
            'metrics': {
                'account.npm_maintainers': (
                    'account.npm_maintainers',
                    'account.avg_npm_maintainers',
                    'Total count NPM maintainers'
                ),
            }
        },
    }