"""Unit tests for spreadsheet formula engine."""
from app.services.extractors.spreadsheet_formula_engine import SpreadsheetFormulaEngine

def test_formula_sum():
    sheets = {"Sheet1": [[10, 20, 30], [5, 15, 25]]}
    engine = SpreadsheetFormulaEngine(sheets)
    res = engine.evaluate_formula("=SUM(A1:C1)", "Sheet1")
    assert res == 60.0

def test_formula_average():
    sheets = {"Sheet1": [[10, 20, 30]]}
    engine = SpreadsheetFormulaEngine(sheets)
    res = engine.evaluate_formula("=AVERAGE(A1:C1)", "Sheet1")
    assert res == 20.0

def test_formula_min_max():
    sheets = {"Sheet1": [[10, 50, 5]]}
    engine = SpreadsheetFormulaEngine(sheets)
    assert engine.evaluate_formula("=MIN(A1:C1)", "Sheet1") == 5.0
    assert engine.evaluate_formula("=MAX(A1:C1)", "Sheet1") == 50.0
