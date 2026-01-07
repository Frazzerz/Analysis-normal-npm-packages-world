from models.change_detection.change_metrics import ChangeMetric

class UtilsForComparator:
    """Utility functions for comparators"""
    
    @staticmethod
    def calculate_change_metric(curr_value: float, prev_value: float) -> ChangeMetric:
        """Calculate ChangeMetric between current and previous values"""
        if prev_value == 0 and curr_value > 0:
            # In this case, I return 'inf' as percentage change and i calculate absolute change
            return ChangeMetric(absolute=curr_value - prev_value, percentage="inf")
        else:
            # I don't return and calculate absolute change in this case
            percentage_change = ((curr_value - prev_value) / prev_value) * 100 if prev_value > 0 else 0.0
            return ChangeMetric(absolute=None, percentage=percentage_change)