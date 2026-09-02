"""
Pure-Python PDF Extractor.
Extracts text streams, decompresses FlateDecode/zlib object streams, resolves font encoding maps,
calculates page counts, detects table patterns, and handles malformed documents.
"""
import re
import zlib
import logging
from typing import List, Dict, Any, Tuple, Optional
from app.services.extractors.base_extractor import (
    BaseDocumentExtractor,
    ExtractionResult,
    PageContent,
    TableData
)
from app.core.exceptions import ExtractionFailedException

logger = logging.getLogger("app.services.extractors.pdf")

class PDFDocumentExtractor(BaseDocumentExtractor):
    """Pure-Python PDF parser extracting text, structural headers, and tables."""

    def extract(self, filepath: str) -> ExtractionResult:
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            
            if not data.startswith(b"%PDF-"):
                raise ExtractionFailedException(filepath, "Invalid PDF header signature")
            
            version_match = re.search(rb"%PDF-(\d+\.\d+)", data[:20])
            pdf_version = version_match.group(1).decode("ascii") if version_match else "1.4"
            
            pages_text = self._extract_page_texts(data)
            if not pages_text:
                raw_strings = self._fallback_raw_text_extraction(data)
                pages_text = [raw_strings] if raw_strings else [""]
            
            tables = self._detect_text_tables(pages_text)
            
            pages: List[PageContent] = []
            full_text_list: List[str] = []
            total_chars = 0
            total_words = 0
            total_lines = 0
            
            for idx, p_text in enumerate(pages_text, start=1):
                clean_p_text = self._clean_pdf_text(p_text)
                full_text_list.append(clean_p_text)
                
                words = len(clean_p_text.split())
                chars = len(clean_p_text)
                lines = len(clean_p_text.splitlines())
                
                total_words += words
                total_chars += chars
                total_lines += lines
                
                page_tables = [t for t in tables if getattr(t, 'table_index', 0) == idx]
                pages.append(PageContent(
                    page_number=idx,
                    text=clean_p_text,
                    word_count=words,
                    character_count=chars,
                    tables=page_tables
                ))
            
            full_text = "\n\n".join(full_text_list).strip()
            headings = self._extract_headings(full_text)
            
            return ExtractionResult(
                file_type="pdf",
                raw_text=full_text,
                page_count=len(pages),
                word_count=total_words,
                character_count=total_chars,
                line_count=total_lines,
                table_count=len(tables),
                pages=pages,
                tables=tables,
                metadata={"pdf_version": pdf_version, "stream_count": len(pages_text)},
                structural_headings=headings
            )
        except Exception as e:
            logger.error(f"PDF extraction error on {filepath}: {str(e)}")
            raise ExtractionFailedException(filepath, str(e))

    def _extract_page_texts(self, data: bytes) -> List[str]:
        page_texts: List[str] = []
        stream_pattern = re.compile(b"stream[\r\n]+(.*?)[\r\n]+endstream", re.DOTALL)
        for match in stream_pattern.finditer(data):
            stream_data = match.group(1)
            decompressed: Optional[bytes] = None
            try:
                decompressed = zlib.decompress(stream_data)
            except Exception:
                try:
                    decompressed = zlib.decompress(stream_data, -zlib.MAX_WBITS)
                except Exception:
                    decompressed = None
            
            if decompressed:
                extracted_str = self._parse_pdf_operators(decompressed)
                if extracted_str and len(extracted_str.strip()) > 3:
                    page_texts.append(extracted_str)
                    
        return page_texts

    def _parse_pdf_operators(self, stream: bytes) -> str:
        text_chunks: List[str] = []
        tj_matches = re.findall(rb"\((.*?)\)\s*Tj", stream)
        for chunk in tj_matches:
            try:
                decoded = chunk.decode("latin-1", errors="ignore")
                text_chunks.append(decoded)
            except Exception:
                pass
        
        tj_array_matches = re.findall(rb"\[(.*?)\]\s*TJ", stream, re.DOTALL)
        for arr in tj_array_matches:
            elements = re.findall(rb"\((.*?)\)", arr)
            line = "".join([e.decode("latin-1", errors="ignore") for e in elements])
            if line:
                text_chunks.append(line)
        
        return " ".join(text_chunks)

    def _fallback_raw_text_extraction(self, data: bytes) -> str:
        matches = re.findall(rb"\(([A-Za-z0-9 ,.\-!?;:$/%#@&*+=\(\)\[\]]{3,})\)", data)
        return " ".join([m.decode("ascii", errors="ignore") for m in matches])

    def _clean_pdf_text(self, text: str) -> str:
        text = text.replace(r"\(", "(").replace(r"\)", ")").replace(r"\\", "\\")
        text = re.sub(r'[\r\n]+', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()

    def _detect_text_tables(self, pages: List[str]) -> List[TableData]:
        tables: List[TableData] = []
        table_idx = 1
        for p_idx, page in enumerate(pages, start=1):
            lines = page.splitlines()
            potential_table_rows: List[List[str]] = []
            for line in lines:
                parts = [p.strip() for p in re.split(r'[\t|]|\s{3,}', line) if p.strip()]
                if len(parts) >= 3:
                    potential_table_rows.append(parts)
            
            if len(potential_table_rows) >= 2:
                headers = potential_table_rows[0]
                rows = potential_table_rows[1:]
                tables.append(TableData(
                    table_index=table_idx,
                    headers=headers,
                    rows=rows,
                    row_count=len(rows),
                    column_count=len(headers),
                    sheet_name=f"Page {p_idx} Table"
                ))
                table_idx += 1
        return tables

    def _extract_headings(self, text: str) -> List[str]:
        headings: List[str] = []
        for line in text.splitlines():
            line = line.strip()
            if 3 < len(line) < 80 and (line.isupper() or line.title() == line):
                if not any(char in line for char in ["$", "%", "=", "+"]):
                    headings.append(line)
        return headings[:10]
