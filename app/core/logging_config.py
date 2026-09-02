"""
Logging configuration with JSON telemetry and colored console handlers.
"""
import logging
import sys
import json
from datetime import datetime, timezone
from typing import Any, Dict
from app.core.config import settings

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "process": record.process,
            "thread": record.threadName
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logging() -> None:
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    try:
        file_handler = logging.FileHandler(settings.LOG_FILE_PATH, encoding="utf-8")
        file_handler.setFormatter(JSONFormatter())
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create file handler: {e}")
    
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
