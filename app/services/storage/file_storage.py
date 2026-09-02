"""
Local Filesystem Storage Manager for document storage, deduplication, and lifecycle management.
"""
import os
import shutil
import uuid
import logging
from pathlib import Path
from typing import Optional, BinaryIO
from app.core.config import settings
from app.core.security import calculate_file_hash, sanitize_filename
from app.core.exceptions import StorageException

logger = logging.getLogger("app.services.storage")

class FileStorageManager:
    """Manages physical document storage on local disk."""

    def __init__(self, base_upload_dir: Optional[Path] = None):
        self.upload_dir = base_upload_dir or settings.UPLOAD_DIR
        self.processed_dir = settings.PROCESSED_DIR
        self.reports_dir = settings.REPORTS_DIR
        
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(self, file_obj: BinaryIO, original_filename: str, user_id: int) -> dict:
        """
        Save an incoming uploaded stream to a secure user-partitioned directory.
        Returns metadata dict containing file_path, stored_filename, file_hash, and size.
        """
        try:
            user_folder = self.upload_dir / f"user_{user_id}"
            user_folder.mkdir(parents=True, exist_ok=True)
            
            clean_name = sanitize_filename(original_filename)
            unique_prefix = uuid.uuid4().hex[:12]
            stored_filename = f"{unique_prefix}_{clean_name}"
            target_path = user_folder / stored_filename
            
            # Stream to disk in 64KB chunks
            total_bytes = 0
            with open(target_path, "wb") as dest:
                while chunk := file_obj.read(65536):
                    dest.write(chunk)
                    total_bytes += len(chunk)
            
            file_hash = calculate_file_hash(str(target_path))
            
            logger.info(f"Saved file {stored_filename} ({total_bytes} bytes) for user {user_id}")
            
            return {
                "file_path": str(target_path),
                "stored_filename": stored_filename,
                "file_size_bytes": total_bytes,
                "file_hash_sha256": file_hash
            }
        except Exception as e:
            logger.error(f"Failed to save upload '{original_filename}': {str(e)}")
            raise StorageException(f"Failed to save uploaded file: {str(e)}")

    def delete_file(self, file_path: str) -> bool:
        """Safely remove file from disk."""
        try:
            p = Path(file_path)
            if p.exists() and p.is_file():
                p.unlink()
                logger.info(f"Deleted physical file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.warning(f"Could not delete physical file {file_path}: {e}")
            return False

    def get_file_bytes(self, file_path: str) -> bytes:
        """Read complete file bytes into memory."""
        p = Path(file_path)
        if not p.exists():
            raise StorageException(f"File not found: {file_path}")
        with open(p, "rb") as f:
            return f.read()

    def get_user_storage_usage(self, user_id: int) -> int:
        """Calculate total bytes consumed by a user's uploaded files."""
        user_folder = self.upload_dir / f"user_{user_id}"
        if not user_folder.exists():
            return 0
        total = 0
        for f in user_folder.glob("*"):
            if f.is_file():
                total += f.stat().st_size
        return total
