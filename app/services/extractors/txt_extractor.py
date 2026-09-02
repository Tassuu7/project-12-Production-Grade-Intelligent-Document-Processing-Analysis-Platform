"""
Plain Text (TXT) Document Extractor.
"""
import re
import logging
from typing import List
from app.services.extractors.base_extractor import (
    BaseDocumentExtractor,
    ExtractionResult,
    PageContent
)
from app.core.exceptions import ExtractionFailedException

logger = logging.getLogger("app.services.extractors.txt")

class TXTDocumentExtractor(BaseDocumentExtractor):
    """Plain text file extractor with encoding resilience."""

    def extract(self, filepath: str) -> ExtractionResult:
        try:
            raw_bytes = self._read_bytes(filepath)
            text, detected_encoding = self._decode_resilient(raw_bytes)
            
            normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
            normalized_text = re.sub(r'[ \t]+', ' ', normalized_text)
            
            lines = normalized_text.splitlines()
            paragraphs = [p.strip() for p in normalized_text.split("\n\n") if p.strip()]
            
            words = normalized_text.split()
            total_words = len(words)
            total_chars = len(normalized_text)
            total_lines = len(lines)
            
            chunk_size = 400
            pages: List[PageContent] = []
            for i in range(0, max(1, total_words), chunk_size):
                p_words = words[i:i + chunk_size]
                p_text = " ".join(p_words)
                page_num = (i // chunk_size) + 1
                pages.append(PageContent(
                    page_number=page_num,
                    text=p_text,
                    word_count=len(p_words),
                    character_count=len(p_text)
                ))
            
            headings = [p[:80] for p in paragraphs if len(p) < 100 and (p.isupper() or p.startswith("#"))]
            
            return ExtractionResult(
                file_type="txt",
                raw_text=normalized_text,
                page_count=len(pages),
                word_count=total_words,
                character_count=total_chars,
                line_count=total_lines,
                table_count=0,
                pages=pages,
                tables=[],
                metadata={"encoding": detected_encoding, "paragraph_count": len(paragraphs)},
                structural_headings=headings[:10]
            )
        except Exception as e:
            logger.error(f"TXT extraction failed on {filepath}: {str(e)}")
            raise ExtractionFailedException(filepath, str(e))

    def _read_bytes(self, filepath: str) -> bytes:
        with open(filepath, "rb") as f:
            return f.read()

    def _decode_resilient(self, raw_bytes: bytes) -> tuple[str, str]:
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "ascii", "utf-16"]
        for enc in encodings:
            try:
                return raw_bytes.decode(enc), enc
            except UnicodeDecodeError:
                continue
        return raw_bytes.decode("latin-1", errors="replace"), "latin-1-fallback"
