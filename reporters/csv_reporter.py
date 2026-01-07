import csv
import json
from dataclasses import is_dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Union
from datetime import datetime
from utils import synchronized_print

class CSVReporter:
    """Generate CSV files with analysis results"""

    @staticmethod
    def save_csv(output_path: Path, data: Union[Any, List[Any]], append: bool = True) -> None:
        items = data if isinstance(data, list) else [data]

        if not items:
            synchronized_print(f"No data to save in {output_path}")
            return

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            flattened_items = [CSVReporter.flatten(item) for item in items]

            fieldnames = []
            for item in flattened_items:
                for key in item.keys():
                    if key not in fieldnames:
                        fieldnames.append(key)

            file_exists = output_path.exists()
            mode = "a" if append else "w"

            with open(output_path, mode, newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                if not append or not file_exists:
                    writer.writeheader()

                for item in flattened_items:
                    writer.writerow(item)

        except Exception as e:
            synchronized_print(f"Error saving CSV to {output_path}: {e}")


    @staticmethod
    def flatten(obj: Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
        items = {}

        obj = CSVReporter.normalize_value(obj)

        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                items.update(CSVReporter.flatten(v, new_key, sep))

        elif isinstance(obj, list):
            # list -> secure JSON string
            items[parent_key] = json.dumps(obj, ensure_ascii=False)

        else:
            items[parent_key] = obj

        return items

    @staticmethod
    def normalize_value(value):
        if isinstance(value, Enum):
            return value.value
        elif isinstance(value, datetime):
            return value.isoformat()
        elif is_dataclass(value):
            return asdict(value)
        elif isinstance(value, list):
            return [CSVReporter.normalize_value(v) for v in value]
        elif isinstance(value, dict):
            return {k: CSVReporter.normalize_value(v) for k, v in value.items()}
        else:
            return value