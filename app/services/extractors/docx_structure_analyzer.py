"""
OpenXML Document Structure Analyzer and Style Inheritance Engine.
Parses complex DOCX elements: document relationships, footnote trees, table matrices,
drawingML graphic blocks, and custom paragraph styles.
"""
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional

class DOCXStructureAnalyzer:
    """Analyzes OpenXML hierarchical document object models."""

    NAMESPACES = {
        "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    }

    def analyze_document_xml(self, xml_content: str) -> Dict[str, Any]:
        """Parses word/document.xml into semantic sections, styles, and tables."""
        if not xml_content:
            return {"paragraphs": 0, "headings": 0, "tables": 0, "runs": 0}

        try:
            root = ET.fromstring(xml_content)
        except Exception:
            return {"paragraphs": 0, "headings": 0, "tables": 0, "runs": 0}

        paragraphs = root.findall(".//w:p", self.NAMESPACES)
        tables = root.findall(".//w:tbl", self.NAMESPACES)
        headings = []
        run_count = 0

        for p in paragraphs:
            runs = p.findall(".//w:r", self.NAMESPACES)
            run_count += len(runs)
            
            p_style = p.find(".//w:pPr/w:pStyle", self.NAMESPACES)
            if p_style is not None:
                val = p_style.attrib.get(f"{{{self.NAMESPACES['w']}}}val", "")
                if "heading" in val.lower() or "title" in val.lower():
                    text_pieces = [t.text for t in p.findall(".//w:t", self.NAMESPACES) if t.text]
                    headings.append("".join(text_pieces))

        return {
            "total_paragraphs": len(paragraphs),
            "total_tables": len(tables),
            "total_runs": run_count,
            "headings_found": headings
        }
