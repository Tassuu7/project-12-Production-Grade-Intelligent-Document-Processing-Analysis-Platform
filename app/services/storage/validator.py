"""
Document File Validation, Magic Byte Verification, Size Checking, and Path Sanitization.
"""
import os
import re
from typing import Tuple, Optional, Dict
from app.core.constants import (
    ALLOWED_FILE_EXTENSIONS,
    MAX_UPLOAD_SIZE_BYTES,
    MAGIC_SIGNATURES,
    MIME_TYPE_MAP
)
from app.core.exceptions import ValidationException

class DocumentValidator:
    """Validates uploaded file properties, security constraints, and content integrity."""

    @staticmethod
    def validate_file_extension(filename: str) -> str:
        """Extract and validate file extension against allowed types."""
        if not filename or "." not in filename:
            raise ValidationException("File has no extension or invalid filename")
        
        ext = filename.rsplit(".", 1)[1].lower().strip()
        if ext not in ALLOWED_FILE_EXTENSIONS:
            allowed_list = ", ".join(sorted(ALLOWED_FILE_EXTENSIONS))
            raise ValidationException(
                f"Unsupported file extension '.{ext}'. Supported formats: {allowed_list}"
            )
        return ext

    @staticmethod
    def validate_file_size(size_bytes: int) -> None:
        """Ensure file size is within limits (> 0 and <= MAX_UPLOAD_SIZE_BYTES)."""
        if size_bytes <= 0:
            raise ValidationException("File is empty (0 bytes)")
        if size_bytes > MAX_UPLOAD_SIZE_BYTES:
            max_mb = MAX_UPLOAD_SIZE_BYTES / (1024 * 1024)
            actual_mb = size_bytes / (1024 * 1024)
            raise ValidationException(
                f"File size ({actual_mb:.1f} MB) exceeds maximum allowed size ({max_mb:.0f} MB)"
            )

    @classmethod
    def validate_file_content(cls, filepath: str, declared_ext: str) -> Tuple[bool, str]:
        """
        Verify actual file byte signatures match the declared file extension.
        Returns (is_valid, mime_type).
        """
        if not os.path.exists(filepath):
            raise ValidationException(f"File not found on disk: {filepath}")
        
        file_size = os.path.getsize(filepath)
        cls.validate_file_size(file_size)
        
        expected_mime = MIME_TYPE_MAP.get(declared_ext, "application/octet-stream")
        
        # Read header bytes for magic signature checks
        with open(filepath, "rb") as f:
            header = f.read(512)
        
        signatures = MAGIC_SIGNATURES.get(declared_ext, [])
        if signatures:
            matched = any(header.startswith(sig) for sig in signatures)
            if not matched:
                raise ValidationException(
                    f"File content signature does not match declared extension '.{declared_ext}'. Possible file corruption or spoofing."
                )
        
        # Text and CSV encoding validation
        if declared_ext in ("txt", "csv"):
            cls._validate_text_encoding(filepath)
            
        return True, expected_mime

    @staticmethod
    def _validate_text_encoding(filepath: str) -> None:
        """Attempt reading text/csv with multiple standard encodings to ensure readability."""
        encodings = ["utf-8", "latin-1", "cp1252", "ascii", "utf-16"]
        success = False
        with open(filepath, "rb") as f:
            raw = f.read(4096)
        
        for enc in encodings:
            try:
                raw.decode(enc)
                success = True
                break
            except (UnicodeDecodeError, Exception):
                continue
        
        if not success:
            raise ValidationException("Text file contains unreadable or corrupted character encodings.")

    @staticmethod
    def sanitize_title(title: str, max_len: int = 150) -> str:
        """Clean human-readable title string."""
        cleaned = re.sub(r'[\r\n\t]+', ' ', title).strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned[:max_len] if cleaned else "Untitled Document"
