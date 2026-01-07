from typing import Dict
from models.composed_metrics import VersionMetrics, AggregateVersionMetrics
from utils import UtilsForComparator, synchronized_print
from models.change_detection.exfiltration_changes import ExfiltrationChanges
class DataExfiltrationComparator:
    """Obtain percentage differences for data exfiltration & command and control metrics between current version and previous versions' aggregate metrics"""
    def compare(self, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> ExfiltrationChanges:
        exfiltration = ExfiltrationChanges()
        if all_prev_tag_metrics.versions == "":
            # No comparison for first version - return blank differences
            '''
            return {
                'percent_difference_scan_functions': 0.0,
                'percent_difference_sensitive_elements': 0.0,
                'percent_difference_data_transmission': 0.0,
            }
            '''
            return exfiltration
        else:
            exfiltration.scan_functions = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.exfiltration.scan_functions_count,
                prev_value=all_prev_tag_metrics.exfiltration.avg_scan_functions_count
            )
            exfiltration.sensitive_elements = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.exfiltration.sensitive_elements_count,
                prev_value=all_prev_tag_metrics.exfiltration.avg_sensitive_elements_count
            )
            exfiltration.data_transmission = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.exfiltration.data_transmission_count,
                prev_value=all_prev_tag_metrics.exfiltration.avg_data_transmission_count
            )
            return exfiltration
            '''
            curr_scan = curr_tag_metrics.scan_functions_count
            all_prev_scan = all_prev_tag_metrics.avg_scan_functions_count

            curr_sens = curr_tag_metrics.sensitive_elements_count
            all_prev_sens = all_prev_tag_metrics.avg_sensitive_elements_count
            
            curr_data = curr_tag_metrics.data_transmission_count
            all_prev_data = all_prev_tag_metrics.avg_data_transmission_count

            return {
                'percent_difference_scan_functions': UtilsForComparator.calculate_percentage_difference(curr_scan, all_prev_scan),
                'percent_difference_sensitive_elements': UtilsForComparator.calculate_percentage_difference(curr_sens, all_prev_sens),
                'percent_difference_data_transmission': UtilsForComparator.calculate_percentage_difference(curr_data, all_prev_data),
            }
            '''