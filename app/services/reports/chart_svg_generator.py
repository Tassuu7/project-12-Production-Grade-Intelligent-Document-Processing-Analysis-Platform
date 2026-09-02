"""
Pure-Python SVG Vector Chart Generator.
"""
from typing import List, Dict, Any

class SVGChartGenerator:
    @staticmethod
    def generate_bar_chart(data: List[Dict[str, Any]], width: int = 500, height: int = 240) -> str:
        if not data:
            return f'<svg width="{width}" height="{height}"></svg>'

        max_val = max(d.get("value", 0) for d in data) or 1
        bar_width = (width - 80) / len(data)
        chart_height = height - 60

        bars_svg = []
        for i, item in enumerate(data):
            val = item.get("value", 0)
            label = item.get("label", "")
            color = item.get("color", "#3b82f6")
            
            b_height = (val / max_val) * chart_height
            x = 50 + i * bar_width + 10
            y = height - 40 - b_height

            bars_svg.append(f'<rect x="{x}" y="{y}" width="{bar_width - 15}" height="{b_height}" fill="{color}" rx="4" />')
            bars_svg.append(f'<text x="{x + (bar_width - 15)/2}" y="{height - 20}" font-size="11" text-anchor="middle" fill="#64748b">{label}</text>')
            bars_svg.append(f'<text x="{x + (bar_width - 15)/2}" y="{y - 5}" font-size="10" font-weight="bold" text-anchor="middle" fill="#1e293b">{val}</text>')

        return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <line x1="40" y1="{height - 40}" x2="{width - 20}" y2="{height - 40}" stroke="#e2e8f0" stroke-width="1.5" />
    {''.join(bars_svg)}
</svg>"""
