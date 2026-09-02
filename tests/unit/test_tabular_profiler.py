"""Unit tests for tabular profiler."""
from app.services.extractors.tabular_profiler import TabularProfiler

def test_tabular_profiler():
    headers = ["Age", "Salary", "Department"]
    rows = [
        ["25", "50000", "Sales"],
        ["30", "60000", "Engineering"],
        ["40", "80000", "Management"]
    ]
    profiler = TabularProfiler()
    profile = profiler.profile(headers, rows)
    assert profile["total_rows"] == 3
    assert profile["columns"]["Salary"]["mean"] == 63333.3333
