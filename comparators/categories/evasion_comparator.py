from typing import Dict
from models.composed_metrics import VersionMetrics, AggregateVersionMetrics
from utils import UtilsForComparator, synchronized_print
from models.change_detection.evasion_changes import EvasionChanges
from models import CodeType
class EvasionComparator:
    """Obtain percentage differences and introductions features for evasion techniques metrics between current version and previous versions' aggregate metrics (and previous version)"""
    def compare(self, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> EvasionChanges:
        evasion = EvasionChanges()
        if all_prev_tag_metrics.versions == "":
            # No comparison for first version - return blank differences
            '''
            return {
                'obfuscated_code_introduced': False,
                'minified_code_introduced': False,
                'percent_difference_hex_obfuscation_patterns': 0.0,
                'percent_difference_platform_detections': 0.0,
            }
            '''
            return evasion
        else:
            evasion.obfuscated_code_introduced = CodeType.OBFUSCATED in curr_tag_metrics.evasion.code_types and CodeType.OBFUSCATED not in prev_tag_metrics.evasion.code_types
            evasion.minified_code_introduced = CodeType.MINIFIED in curr_tag_metrics.evasion.code_types and CodeType.MINIFIED not in prev_tag_metrics.evasion.code_types
            evasion.hex_obfuscation_patterns = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.evasion.obfuscation_patterns_count,
                prev_value=all_prev_tag_metrics.evasion.avg_obfuscation_patterns_count
            )
            evasion.platform_detections = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.evasion.platform_detections_count,
                prev_value=all_prev_tag_metrics.evasion.avg_platform_detections_count
            )
            return evasion
            '''
            curr_code_types = curr_tag_metrics.code_types            
            prev_code_types = prev_tag_metrics.code_types

            curr_obfuscation = curr_tag_metrics.obfuscation_patterns_count
            all_prev_obfuscation = all_prev_tag_metrics.avg_obfuscation_patterns_count

            curr_platform = curr_tag_metrics.platform_detections_count
            all_prev_platform = all_prev_tag_metrics.avg_platform_detections_count

            return {
                'obfuscated_code_introduced': 'Obfuscated' in curr_code_types and 'Obfuscated' not in prev_code_types,
                'minified_code_introduced': 'Minified' in curr_code_types and 'Minified' not in prev_code_types,
                'percent_difference_hex_obfuscation_patterns': UtilsForComparator.calculate_percentage_difference(curr_obfuscation, all_prev_obfuscation),
                'percent_difference_platform_detections': UtilsForComparator.calculate_percentage_difference(curr_platform, all_prev_platform),
            }
            '''