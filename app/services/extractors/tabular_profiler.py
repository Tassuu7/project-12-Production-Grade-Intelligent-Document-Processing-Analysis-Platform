"""
Comprehensive Tabular Statistical Profiling Engine.
"""
import math
from typing import Dict, List, Any

class TabularProfiler:
    def profile(self, headers: List[str], rows: List[List[str]]) -> Dict[str, Any]:
        if not headers or not rows:
            return {"columns": {}, "total_rows": 0, "total_columns": 0}

        col_profiles: Dict[str, Any] = {}
        total_rows = len(rows)

        for col_idx, name in enumerate(headers):
            values = []
            for r in rows:
                if col_idx < len(r):
                    values.append(r[col_idx].strip())
                else:
                    values.append("")

            non_empty = [v for v in values if v != ""]
            missing_count = total_rows - len(non_empty)

            num_vals: List[float] = []
            for v in non_empty:
                try:
                    num_vals.append(float(v.replace(",", "")))
                except ValueError:
                    pass

            is_numeric = len(num_vals) == len(non_empty) and len(non_empty) > 0

            profile_data = {
                "name": name,
                "data_type": "number" if is_numeric else "string",
                "total_count": total_rows,
                "missing_count": missing_count,
                "missing_percentage": round((missing_count / max(1, total_rows)) * 100, 2),
                "unique_count": len(set(non_empty))
            }

            if is_numeric and num_vals:
                n = len(num_vals)
                mean_val = sum(num_vals) / n
                variance = sum((x - mean_val) ** 2 for x in num_vals) / max(1, n - 1)
                std_dev = math.sqrt(variance)

                profile_data.update({
                    "min": min(num_vals),
                    "max": max(num_vals),
                    "mean": round(mean_val, 4),
                    "std_dev": round(std_dev, 4)
                })

            col_profiles[name] = profile_data

        return {
            "columns": col_profiles,
            "total_rows": total_rows,
            "total_columns": len(headers)
        }
