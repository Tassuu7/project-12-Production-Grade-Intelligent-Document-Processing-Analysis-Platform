"""
Domain-specific custom application exceptions.
"""
from typing import Any, Dict, Optional

class AppBaseException(Exception):
    def __init__(self, message: str, status_code: int = 400, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class AuthenticationException(AppBaseException):
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=401, details=details)

class AuthorizationException(AppBaseException):
    def __init__(self, message: str = "You do not have permission to perform this action", details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=403, details=details)

class DocumentNotFoundException(AppBaseException):
    def __init__(self, document_id: Any, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=f"Document with ID {document_id} was not found", status_code=404, details=details)

class ExtractionFailedException(AppBaseException):
    def __init__(self, filename: str, reason: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=f"Extraction failed for {filename}: {reason}", status_code=422, details=details)

class ValidationException(AppBaseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=422, details=details)

class DuplicateDocumentException(AppBaseException):
    def __init__(self, filename: str, existing_id: Any, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Duplicate file {filename} already exists with document ID {existing_id}",
            status_code=409,
            details=details or {"existing_document_id": existing_id}
        )

class StorageException(AppBaseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=500, details=details)

class JobQueueException(AppBaseException):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, status_code=500, details=details)
