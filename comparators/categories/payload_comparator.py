from typing import Dict
from models.composed_metrics import VersionMetrics, AggregateVersionMetrics
from utils import UtilsForComparator, synchronized_print
from models.change_detection.payload_changes import PayloadChanges
class PayloadComparator:
    """Obtain percentage differences and introductions features for payload delivery and execution metrics between current version and previous versions' aggregate metrics (and previous version)"""
    def compare(self, prev_tag_metrics: VersionMetrics, curr_tag_metrics: VersionMetrics, all_prev_tag_metrics: AggregateVersionMetrics) -> PayloadChanges:
        payload = PayloadChanges()
        if all_prev_tag_metrics.versions == "":
            # No comparison for first version - return blank differences
            '''
            return {
                'percent_difference_timing_delays': 0.0,
                'percent_difference_eval_function': 0.0,
                'percent_difference_shell_commands': 0.0,
                'preinstall_scripts_introduced': False,
                'preinstall_scripts_change': False,
            }
            '''
            return payload
        else:
            payload.timing_delays = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.payload.timing_delays_count,
                prev_value=all_prev_tag_metrics.payload.avg_timing_delays_count
            )
            payload.eval_function = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.payload.eval_count,
                prev_value=all_prev_tag_metrics.payload.avg_eval_count
            )
            payload.shell_commands = UtilsForComparator.calculate_change_metric(
                curr_value=curr_tag_metrics.payload.shell_commands_count,
                prev_value=all_prev_tag_metrics.payload.avg_shell_commands_count
            )
            payload.preinstall_scripts_introduced = bool(curr_tag_metrics.payload.preinstall_scripts) and not bool(prev_tag_metrics.payload.preinstall_scripts)
            payload.preinstall_scripts_change = bool(curr_tag_metrics.payload.preinstall_scripts) != bool(prev_tag_metrics.payload.preinstall_scripts) and bool(curr_tag_metrics.payload.preinstall_scripts) and bool(prev_tag_metrics.payload.preinstall_scripts)
            return payload
        '''
            curr_timing = curr_tag_metrics.timing_delays_count
            all_prev_timing = all_prev_tag_metrics.avg_timing_delays_count

            curr_eval = curr_tag_metrics.eval_count
            all_prev_eval = all_prev_tag_metrics.avg_eval_count

            curr_shell = curr_tag_metrics.shell_commands_count
            all_prev_shell = all_prev_tag_metrics.avg_shell_commands_count

            prev_preinstall = prev_tag_metrics.preinstall_scripts
            curr_preinstall = curr_tag_metrics.preinstall_scripts
            prev_has_preinstall = bool(prev_preinstall)
            curr_has_preinstall = bool(curr_preinstall)

            return {
                'percent_difference_timing_delays': UtilsForComparator.calculate_percentage_difference(curr_timing, all_prev_timing),
                'percent_difference_eval_function': UtilsForComparator.calculate_percentage_difference(curr_eval, all_prev_eval),
                'percent_difference_shell_commands': UtilsForComparator.calculate_percentage_difference(curr_shell, all_prev_shell),
                'preinstall_scripts_introduced': not prev_has_preinstall and curr_has_preinstall,
                'preinstall_scripts_change': prev_has_preinstall != curr_has_preinstall and prev_has_preinstall and curr_has_preinstall,
            }
        '''