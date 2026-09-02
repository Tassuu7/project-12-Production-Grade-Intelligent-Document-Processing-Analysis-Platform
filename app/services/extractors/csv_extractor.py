"""
CSV Extractor with Auto-Dialect Sniffing, Type Inference, and Statistical Profiling.
"""
import csv
import io
import logging
from typing import List, Dict, Any, Optional
from app.services.extractors.base_extractor import (
    BaseDocumentExtractor,
    ExtractionResult,
    PageContent,
    TableData
)
from app.core.exceptions import ExtractionFailedException

logger = logging.getLogger("app.services.extractors.csv")

class CSVDocumentExtractor(BaseDocumentExtractor):
    """CSV data extractor providing structural tables, schema profiling, and text representations."""

    def extract(self, filepath: str) -> ExtractionResult:
        try:
            with open(filepath, "rb") as f:
                raw = f.read()
            
            # Decode content
            text, enc = self._decode_content(raw)
            
            # Detect dialect / delimiter
            sample = text[:4096]
            try:
                dialect = csv.Sniffer().sniff(sample)
                delimiter = dialect.delimiter
            except Exception:
                delimiter = ","
            
            reader = csv.reader(io.StringIO(text), delimiter=delimiter)
            rows: List[List[str]] = [row for row in reader if any(cell.strip() for cell in row)]
            
            if not rows:
                raise ExtractionFailedException(filepath, "CSV file is empty or contains only blank rows")
            
            headers = rows[0]
            data_rows = rows[1:] if len(rows) > 1 else []
            
            # Generate text representation for NLP downstream processing
            text_lines: List[str] = [f"CSV Table with Columns: {', '.join(headers)}"]
            for idx, r in enumerate(data_rows[:100], start=1):
                row_str = " | ".join([f"{h}: {v}" for h, v in zip(headers, r) if v.strip()])
                text_lines.append(f"Row {idx}: {row_str}")
            
            full_text = "
".join(text_lines)
            
            # Profile statistics
            stats = self._calculate_column_stats(headers, data_rows)
            
            table = TableData(
                table_index=1,
                headers=headers,
                rows=data_rows[:200],  # cap table display matrix at 200 rows
                row_count=len(data_rows),
                column_count=len(headers),
                sheet_name="Main CSV Data"
            )
            
            page = PageContent(
                page_number=1,
                text=full_text,
                word_count=len(full_text.split()),
                character_count=len(full_text),
                tables=[table]
            )
            
            return ExtractionResult(
                file_type="csv",
                raw_text=full_text,
                page_count=1,
                word_count=len(full_text.split()),
                character_count=len(full_text),
                line_count=len(rows),
                table_count=1,
                pages=[page],
                tables=[table],
                metadata={
                    "encoding": enc,
                    "delimiter": delimiter,
                    "total_rows": len(data_rows),
                    "total_columns": len(headers)
                },
                structural_headings=headers[:10],
                tabular_statistics=stats
            )
        except Exception as e:
            logger.error(f"CSV extraction failed on {filepath}: {str(e)}")
            raise ExtractionFailedException(filepath, str(e))

    def _decode_content(self, raw: bytes) -> tuple[str, str]:
        for enc in ["utf-8", "utf-8-sig", "latin-1", "cp1252"]:
            try:
                return raw.decode(enc), enc
            except UnicodeDecodeError:
                continue
        return raw.decode("latin-1", errors="replace"), "latin-1"

    def _calculate_column_stats(self, headers: List[str], rows: List[List[str]]) -> Dict[str, Any]:
        stats: Dict[str, Any] = {"columns": {}, "total_rows": len(rows), "missing_values_count": 0}
        total_missing = 0
        
        for col_idx, col_name in enumerate(headers):
            col_values = []
            for r in rows:
                if col_idx < len(r):
                    val = r[col_idx].strip()
                    if val != "":
                        col_values.append(val)
                    else:
                        total_missing += 1
                else:
                    total_missing += 1
            
            # Check if numerical
            numeric_vals = []
            for v in col_values:
                try:
                    numeric_vals.append(float(v.replace(",", "")))
                except ValueError:
                    pass
            
            is_numeric = len(numeric_vals) == len(col_values) and len(col_values) > 0
            
            col_stat = {
                "name": col_name,
                "data_type": "number" if is_numeric else "string",
                "non_empty_count": len(col_values),
                "missing_count": len(rows) - len(col_values)
            }
            
            if is_numeric and numeric_vals:
                col_stat["min"] = min(numeric_vals)
                col_stat["max"] = max(numeric_vals)
                col_stat["mean"] = sum(numeric_vals) / len(numeric_vals)
            
            stats["columns"][col_name] = col_stat
            
        stats["missing_values_count"] = total_missing
        return stats
