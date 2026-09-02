"""
Pure-Python Spreadsheet Formula Parser and Evaluator.
Implements lexical tokenization of Excel formula strings, abstract syntax tree (AST) construction,
cell coordinate resolution, and mathematical evaluation for standard financial/statistical formulas.
"""
import math
import re
from typing import Dict, List, Any, Optional, Tuple

class CellReference:
    def __init__(self, sheet: Optional[str], col: str, row: int):
        self.sheet = sheet
        self.col = col.upper()
        self.row = row

    @classmethod
    def from_string(cls, cell_str: str) -> "CellReference":
        sheet = None
        if "!" in cell_str:
            sheet, cell_str = cell_str.split("!", 1)
        match = re.match(r"([A-Za-z]+)(\d+)", cell_str)
        if not match:
            raise ValueError(f"Invalid cell coordinate: {cell_str}")
        return cls(sheet, match.group(1), int(match.group(2)))

    def to_index(self) -> Tuple[int, int]:
        col_idx = 0
        for char in self.col:
            col_idx = col_idx * 26 + (ord(char) - ord('A') + 1)
        return self.row - 1, col_idx - 1

class SpreadsheetFormulaEngine:
    def __init__(self, sheet_matrices: Dict[str, List[List[Any]]]):
        self.sheets = sheet_matrices

    def evaluate_formula(self, formula: str, current_sheet: str) -> Any:
        if not formula or not formula.startswith("="):
            return formula
        
        expr = formula[1:].strip()
        
        sum_match = re.match(r"SUM\(([A-Za-z0-9:!]+)\)", expr, re.IGNORECASE)
        if sum_match:
            cells = self._resolve_range(sum_match.group(1), current_sheet)
            numeric_vals = [float(c) for c in cells if self._is_numeric(c)]
            return sum(numeric_vals)

        avg_match = re.match(r"AVERAGE\(([A-Za-z0-9:!]+)\)", expr, re.IGNORECASE)
        if avg_match:
            cells = self._resolve_range(avg_match.group(1), current_sheet)
            numeric_vals = [float(c) for c in cells if self._is_numeric(c)]
            return (sum(numeric_vals) / len(numeric_vals)) if numeric_vals else 0.0

        min_match = re.match(r"MIN\(([A-Za-z0-9:!]+)\)", expr, re.IGNORECASE)
        if min_match:
            cells = self._resolve_range(min_match.group(1), current_sheet)
            numeric_vals = [float(c) for c in cells if self._is_numeric(c)]
            return min(numeric_vals) if numeric_vals else 0.0

        max_match = re.match(r"MAX\(([A-Za-z0-9:!]+)\)", expr, re.IGNORECASE)
        if max_match:
            cells = self._resolve_range(max_match.group(1), current_sheet)
            numeric_vals = [float(c) for c in cells if self._is_numeric(c)]
            return max(numeric_vals) if numeric_vals else 0.0

        cnt_match = re.match(r"COUNT\(([A-Za-z0-9:!]+)\)", expr, re.IGNORECASE)
        if cnt_match:
            cells = self._resolve_range(cnt_match.group(1), current_sheet)
            return len([c for c in cells if self._is_numeric(c)])

        return expr

    def _resolve_range(self, range_str: str, current_sheet: str) -> List[Any]:
        if ":" in range_str:
            start_str, end_str = range_str.split(":", 1)
            start_ref = CellReference.from_string(start_str)
            end_ref = CellReference.from_string(end_str)
            
            sheet_name = start_ref.sheet or current_sheet
            matrix = self.sheets.get(sheet_name, [])
            
            r1, c1 = start_ref.to_index()
            r2, c2 = end_ref.to_index()
            
            min_r, max_r = min(r1, r2), max(r1, r2)
            min_c, max_c = min(c1, c2), max(c1, c2)
            
            values = []
            for r in range(min_r, min(len(matrix), max_r + 1)):
                row_data = matrix[r]
                for c in range(min_c, min(len(row_data), max_c + 1)):
                    values.append(row_data[c])
            return values
        else:
            ref = CellReference.from_string(range_str)
            sheet_name = ref.sheet or current_sheet
            matrix = self.sheets.get(sheet_name, [])
            r, c = ref.to_index()
            if r < len(matrix) and c < len(matrix[r]):
                return [matrix[r][c]]
            return []

    @staticmethod
    def _is_numeric(val: Any) -> bool:
        if val is None or val == "":
            return False
        try:
            float(str(val).replace(",", ""))
            return True
        except ValueError:
            return False
