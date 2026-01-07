from typing import Dict
from models.composed_metrics import VersionMetrics, AggregateVersionMetrics
from utils import UtilsForComparator, synchronized_print
from models.change_detection.generic_changes import GenericChanges
class GenericComparator:
    """Obtain percentage differences for generic metrics between current version and previous versions' aggregate metrics"""
    def compare(self, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> GenericChanges:
            generic = GenericChanges()
            if all_prev_tag_metrics.versions == "":
                # No comparison for the first version - return blank differences
                '''
                return {
                    'percent_difference_total_files': 0.0,
                    'percent_difference_size_bytes': 0.0,
                    'percent_difference_weighted_avg_blank_space_and_character_ratio': 0.0,
                    'percent_difference_weighted_avg_shannon_entropy': 0.0,
                    'percent_difference_longest_line_length': 0.0
                }
                '''
                return generic
            else:
                generic.total_files = UtilsForComparator.calculate_change_metric(
                    curr_value=curr_tag_metrics.generic.total_files,
                    prev_value=all_prev_tag_metrics.generic.avg_total_files
                )
                generic.size_bytes = UtilsForComparator.calculate_change_metric(
                    curr_value=curr_tag_metrics.generic.total_size_bytes,
                    prev_value=all_prev_tag_metrics.generic.avg_total_size_bytes
                )
                generic.weighted_avg_blank_space_and_character_ratio = UtilsForComparator.calculate_change_metric(
                    curr_value=curr_tag_metrics.generic.weighted_avg_blank_space_and_character_ratio,
                    prev_value=all_prev_tag_metrics.generic.weighted_avg_blank_space_and_character_ratio
                )
                generic.weighted_avg_shannon_entropy = UtilsForComparator.calculate_change_metric(
                    curr_value=curr_tag_metrics.generic.weighted_avg_shannon_entropy,
                    prev_value=all_prev_tag_metrics.generic.weighted_avg_shannon_entropy
                )
                generic.longest_line_length = UtilsForComparator.calculate_change_metric(
                    curr_value=curr_tag_metrics.generic.longest_line_length,
                    prev_value=all_prev_tag_metrics.generic.avg_longest_line_length
                )
                
                return generic
            '''
            else:
                curr_total_files = curr_tag_metrics.total_files
                all_prev_total_files = all_prev_tag_metrics.avg_total_files
                #synchronized_print(f"    Previous Total Files: {all_prev_total_files}, Current Total Files: {curr_total_files}")
                #synchronized_print(f"    Result:{((curr_total_files - all_prev_total_files) / all_prev_total_files) * 100 if all_prev_total_files > 0 else 0.0}")
                
                curr_size_bytes = curr_tag_metrics.total_size_bytes
                all_prev_size_bytes = all_prev_tag_metrics.avg_total_size_bytes
                #synchronized_print(f"    Generic Comparison: Previous Size Bytes: {all_prev_size_bytes}, Current Size Bytes: {curr_size_bytes}")
                #synchronized_print(f"    Result:{((curr_size_bytes - all_prev_size_bytes) / all_prev_size_bytes) * 100 if all_prev_size_bytes > 0 else 0.0}")
                
                curr_BSCR = curr_tag_metrics.weighted_avg_blank_space_and_character_ratio
                all_prev_BSCR = all_prev_tag_metrics.weighted_avg_blank_space_and_character_ratio

                curr_SE = curr_tag_metrics.weighted_avg_shannon_entropy
                all_prev_SE = all_prev_tag_metrics.weighted_avg_shannon_entropy

                curr_LLL = curr_tag_metrics.longest_line_length
                all_prev_LLL = all_prev_tag_metrics.avg_longest_line_length

                return {
                    'percent_difference_total_files': UtilsForComparator.calculate_percentage_difference(curr_total_files, all_prev_total_files),
                    'percent_difference_size_bytes': UtilsForComparator.calculate_percentage_difference(curr_size_bytes, all_prev_size_bytes),
                    'percent_difference_weighted_avg_blank_space_and_character_ratio': UtilsForComparator.calculate_percentage_difference(curr_BSCR, all_prev_BSCR),
                    'percent_difference_weighted_avg_shannon_entropy': UtilsForComparator.calculate_percentage_difference(curr_SE, all_prev_SE),
                    'percent_difference_longest_line_length': UtilsForComparator.calculate_percentage_difference(curr_LLL, all_prev_LLL),
                }
            '''