"""Unit tests for SVG Chart Generator."""
from app.services.reports.chart_svg_generator import SVGChartGenerator

def test_svg_bar_chart_generation():
    data = [{"label": "Invoices", "value": 15}, {"label": "Resumes", "value": 8}]
    svg = SVGChartGenerator.generate_bar_chart(data)
    assert "<svg" in svg
    assert "</svg>" in svg
    assert "Invoices" in svg
