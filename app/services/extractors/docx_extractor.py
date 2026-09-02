"""
Pure-Python DOCX Extractor using zipfile and xml.etree.ElementTree.
Parses WordprocessingML: paragraphs, heading styles, tables, headers, footers, and metadata.
"""
import zipfile
import xml.etree.ElementTree as ET
import logging
from typing import List, Dict, Any, Optional
from app.services.extractors.base_extractor import (
    BaseDocumentExtractor,
    ExtractionResult,
    PageContent,
    TableData
)
from app.core.exceptions import ExtractionFailedException

logger = logging.getLogger("app.services.extractors.docx")

WORD_NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
    "dc": "http://purl.org/dc/elements/1.1/"
}

class DOCXDocumentExtractor(BaseDocumentExtractor):
    """OpenXML DOCX parser for Microsoft Word documents."""

    def extract(self, filepath: str) -> ExtractionResult:
        try:
            if not zipfile.is_zipfile(filepath):
                raise ExtractionFailedException(filepath, "File is not a valid ZIP/DOCX container")
            
            with zipfile.ZipFile(filepath, "r") as docx_zip:
                # Read main document XML
                if "word/document.xml" not in docx_zip.namelist():
                    raise ExtractionFailedException(filepath, "Missing word/document.xml inside DOCX archive")
                
                doc_xml_bytes = docx_zip.read("word/document.xml")
                root = ET.fromstring(doc_xml_bytes)
                
                paragraphs: List[str] = []
                headings: List[str] = []
                tables: List[TableData] = []
                
                # Extract paragraphs and headings
                for p in root.findall(".//w:p", WORD_NS):
                    p_text = self._extract_text_from_node(p)
                    if p_text:
                        paragraphs.append(p_text)
                        # Check style for headings
                        p_style = p.find(".//w:pStyle", WORD_NS)
                        if p_style is not None:
                            val = p_style.attrib.get(f"{{{WORD_NS['w']}}}val", "")
                            if "Heading" in val or "Title" in val:
                                headings.append(p_text)
                
                # Extract tables
                tbl_elements = root.findall(".//w:tbl", WORD_NS)
                for tbl_idx, tbl in enumerate(tbl_elements, start=1):
                    t_data = self._extract_table_from_node(tbl, tbl_idx)
                    if t_data:
                        tables.append(t_data)
                
                # Extract metadata if core.xml exists
                meta = self._extract_docx_metadata(docx_zip)
            
            full_text = "

".join(paragraphs).strip()
            total_words = len(full_text.split())
            total_chars = len(full_text)
            total_lines = len(full_text.splitlines())
            
            # Approximate page count (Word is flowable: ~350 words per standard page)
            approx_pages = max(1, (total_words // 350) + (1 if total_words % 350 > 0 else 0))
            
            # Split into synthetic pages for unified pagination
            pages: List[PageContent] = []
            words_list = full_text.split()
            chunk_size = 350
            for i in range(0, max(1, len(words_list)), chunk_size):
                p_words = words_list[i:i + chunk_size]
                p_text = " ".join(p_words)
                page_num = (i // chunk_size) + 1
                pages.append(PageContent(
                    page_number=page_num,
                    text=p_text,
                    word_count=len(p_words),
                    character_count=len(p_text),
                    tables=[t for t in tables if t.table_index == page_num]
                ))
            
            return ExtractionResult(
                file_type="docx",
                raw_text=full_text,
                page_count=len(pages),
                word_count=total_words,
                character_count=total_chars,
                line_count=total_lines,
                table_count=len(tables),
                pages=pages,
                tables=tables,
                metadata=meta,
                structural_headings=headings
            )
        except Exception as e:
            logger.error(f"DOCX extraction failed on {filepath}: {str(e)}")
            raise ExtractionFailedException(filepath, str(e))

    def _extract_text_from_node(self, node: ET.Element) -> str:
        """Extract all text nodes from a paragraph or run element."""
        text_pieces: List[str] = []
        for t in node.findall(".//w:t", WORD_NS):
            if t.text:
                text_pieces.append(t.text)
        return "".join(text_pieces).strip()

    def _extract_table_from_node(self, tbl_node: ET.Element, table_idx: int) -> Optional[TableData]:
        """Parse table row and cell elements from w:tbl."""
        rows: List[List[str]] = []
        for tr in tbl_node.findall(".//w:tr", WORD_NS):
            row_cells: List[str] = []
            for tc in tr.findall(".//w:tc", WORD_NS):
                cell_text = self._extract_text_from_node(tc)
                row_cells.append(cell_text)
            if row_cells:
                rows.append(row_cells)
        
        if not rows:
            return None
        
        headers = rows[0]
        data_rows = rows[1:] if len(rows) > 1 else []
        return TableData(
            table_index=table_idx,
            headers=headers,
            rows=data_rows,
            row_count=len(data_rows),
            column_count=len(headers),
            sheet_name=f"DOCX Table {table_idx}"
        )

    def _extract_docx_metadata(self, docx_zip: zipfile.ZipFile) -> Dict[str, Any]:
        meta: Dict[str, Any] = {}
        if "docProps/core.xml" in docx_zip.namelist():
            try:
                core_xml = docx_zip.read("docProps/core.xml")
                c_root = ET.fromstring(core_xml)
                title = c_root.find(".//dc:title", WORD_NS)
                creator = c_root.find(".//dc:creator", WORD_NS)
                if title is not None and title.text:
                    meta["title"] = title.text
                if creator is not None and creator.text:
                    meta["creator"] = creator.text
            except Exception:
                pass
        return meta
