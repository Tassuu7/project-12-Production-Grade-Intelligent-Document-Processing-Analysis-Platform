"""
Document Quality and Structural Anomaly Detection Engine.
Identifies empty files, extreme repetition, abnormal character distributions,
missing standard sections, numerical outliers in tabular datasets, and encoding glitches.
"""
import re
from typing import List, Dict, Any
from app.core.constants import AnomalyType
from app.services.extractors.base_extractor import ExtractionResult

class QualityAnomalyDetector:
    """Audits document structure and extraction characteristics for quality anomalies."""

    def analyze(self, doc_record, extraction: ExtractionResult, cleaned_text: str) -> List[Dict[str, Any]]:
        """Audit document extraction and return structured list of detected anomalies."""
        anomalies: List[Dict[str, Any]] = []
        
        # 1. Empty or Near-Empty Document
        if len(cleaned_text.strip()) == 0:
            anomalies.append({
                "type": AnomalyType.EMPTY_DOCUMENT.value,
                "description": "The document contains zero extractable text.",
                "severity": "HIGH",
                "location": "Global"
            })
            return anomalies
        
        if len(cleaned_text.strip()) < 50:
            anomalies.append({
                "type": AnomalyType.VERY_SHORT_CONTENT.value,
                "description": f"Extracted text is unusually short ({len(cleaned_text.strip())} characters).",
                "severity": "MEDIUM",
                "location": "Global"
            })
        
        # 2. Excessive Repetition Detection
        words = cleaned_text.lower().split()
        if len(words) > 30:
            unique_words = set(words)
            diversity_ratio = len(unique_words) / len(words)
            if diversity_ratio < 0.25:
                anomalies.append({
                    "type": AnomalyType.EXCESSIVE_REPETITION.value,
                    "description": f"High lexical repetition detected ({diversity_ratio*100:.1f}% unique vocabulary). Potential boilerplate.",
                    "severity": "MEDIUM",
                    "location": "Global"
                })
        
        # 3. Abnormal Character / Symbol Ratios
        non_alphanumeric = re.findall(r'[^a-zA-Z0-9\s.,;:!?-]', cleaned_text)
        if len(cleaned_text) > 100:
            symbol_ratio = len(non_alphanumeric) / len(cleaned_text)
            if symbol_ratio > 0.20:
                anomalies.append({
                    "type": AnomalyType.MALFORMED_ENCODING.value,
                    "description": f"Unusual character symbol density ({symbol_ratio*100:.1f}%). Possible font encoding distortion or OCR noise.",
                    "severity": "LOW",
                    "location": "Text Body"
                })
        
        # 4. Tabular Data Anomalies for CSV / XLSX
        if extraction.tabular_statistics:
            missing_cnt = extraction.tabular_statistics.get("missing_values_count", 0)
            total_rows = extraction.tabular_statistics.get("total_rows", 1)
            columns = extraction.tabular_statistics.get("columns", {})
            
            total_cells = total_rows * max(1, len(columns))
            missing_rate = missing_cnt / total_cells if total_cells > 0 else 0
            
            if missing_rate > 0.35:
                anomalies.append({
                    "type": AnomalyType.HIGH_MISSING_VALUE_RATE.value,
                    "description": f"Tabular matrix has high missing value rate ({missing_rate*100:.1f}% empty cells).",
                    "severity": "MEDIUM",
                    "location": "Tabular Schema"
                })
            
            # Numeric Outlier Check
            for col_name, stats in columns.items():
                if stats.get("data_type") == "number":
                    col_min = stats.get("min", 0)
                    col_max = stats.get("max", 0)
                    col_mean = stats.get("mean", 0)
                    if col_max > 0 and col_mean > 0 and (col_max / col_mean) > 100:
                        anomalies.append({
                            "type": AnomalyType.NUMERICAL_OUTLIER.value,
                            "description": f"Column '{col_name}' exhibits extreme numerical outliers (max: {col_max}, mean: {col_mean:.1f}).",
                            "severity": "LOW",
                            "location": f"Column '{col_name}'"
                        })
        
        return anomalies
