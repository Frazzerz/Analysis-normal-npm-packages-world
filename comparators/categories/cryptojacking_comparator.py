from typing import Dict
from models.composed_metrics import VersionMetrics, AggregateVersionMetrics
from utils import UtilsForComparator, synchronized_print
from models.change_detection.crypto_changes import CryptoChanges
class CryptojackingComparator:
    """Obtain percentage differences and introductions features for cryptojacking metrics between current version and previous versions' aggregate metrics (and previous version)"""
    def compare(self, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> CryptoChanges:
        crypto = CryptoChanges()
        if all_prev_tag_metrics.versions == "":
            '''
            # No comparison for first version - return blank differences
            return {
                'percent_difference_crypto_addresses': 0.0,
                'change_crypto_addresses': False,
                'percent_difference_cryptocurrency_name': 0.0,
                'percent_difference_wallet_checks': 0.0,
                'percent_difference_replaced_crypto_addresses': 0.0,
                'percent_difference_hook_provider': 0.0
            }
            '''
            return crypto
        else:
            crypto.crypto_addresses = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.crypto.crypto_addresses,
                prev_value=all_prev_tag_metrics.crypto.avg_crypto_addresses
            )
            crypto.change_crypto_addresses = prev_tag_metrics.crypto.crypto_addresses == curr_tag_metrics.crypto.crypto_addresses and prev_tag_metrics.crypto.list_crypto_addresses != curr_tag_metrics.crypto.list_crypto_addresses and prev_tag_metrics.crypto.crypto_addresses > 0
            crypto.cryptocurrency_name = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.crypto.cryptocurrency_name,
                prev_value=all_prev_tag_metrics.crypto.avg_cryptocurrency_name
            )
            crypto.wallet_checks = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.crypto.wallet_detection,
                prev_value=all_prev_tag_metrics.crypto.avg_wallet_detection
            )
            crypto.replaced_crypto_addresses = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.crypto.replaced_crypto_addresses,
                prev_value=all_prev_tag_metrics.crypto.avg_replaced_crypto_addresses
            )
            crypto.hook_provider = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.crypto.hook_provider,
                prev_value=all_prev_tag_metrics.crypto.avg_hook_provider
            )
            return crypto
            '''
            curr_crypto = curr_tag_metrics.crypto_addresses
            all_prev_crypto = all_prev_tag_metrics.avg_crypto_addresses
            prev_crypto = prev_tag_metrics.crypto_addresses
            curr_list_crypto = curr_tag_metrics.list_crypto_addresses
            prev_list_crypto = prev_tag_metrics.list_crypto_addresses

            curr_cryptocurrency = curr_tag_metrics.cryptocurrency_name
            all_prev_cryptocurrency = all_prev_tag_metrics.avg_cryptocurrency_name
            
            curr_wallet = curr_tag_metrics.wallet_detection
            all_prev_wallet = all_prev_tag_metrics.avg_wallet_detection
            
            curr_replaced = curr_tag_metrics.replaced_crypto_addresses
            all_prev_replaced = all_prev_tag_metrics.avg_replaced_crypto_addresses
            
            curr_hook = curr_tag_metrics.hook_provider
            all_prev_hook = all_prev_tag_metrics.avg_hook_provider
            
            return {
                'percent_difference_crypto_addresses': UtilsForComparator.calculate_percentage_difference(curr_crypto, all_prev_crypto),
                'change_crypto_addresses': prev_crypto == curr_crypto and prev_list_crypto != curr_list_crypto and prev_crypto > 0,
                'percent_difference_cryptocurrency_name': UtilsForComparator.calculate_percentage_difference(curr_cryptocurrency, all_prev_cryptocurrency),
                'percent_difference_wallet_checks': UtilsForComparator.calculate_percentage_difference(curr_wallet, all_prev_wallet),
                'percent_difference_replaced_crypto_addresses': UtilsForComparator.calculate_percentage_difference(curr_replaced, all_prev_replaced),
                'percent_difference_hook_provider': UtilsForComparator.calculate_percentage_difference(curr_hook, all_prev_hook)
            }
            '''