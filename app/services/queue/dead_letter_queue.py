"""
Dead Letter Queue (DLQ) and Incident Recovery Management.
Tracks failed processing tasks, calculates exponential backoff retry schedules,
and maintains an audit trail of persistent processing anomalies.
"""
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from collections import deque

class DeadLetterQueueManager:
    """Manages poisoned or persistently failing document jobs."""

    def __init__(self, max_capacity: int = 1000):
        self.max_capacity = max_capacity
        self.dlq_records: deque = deque(maxlen=max_capacity)

    def record_failure(self, job_id: int, document_id: int, user_id: int, error_message: str, stack_trace: Optional[str] = None) -> Dict[str, Any]:
        entry = {
            "job_id": job_id,
            "document_id": document_id,
            "user_id": user_id,
            "error_message": error_message,
            "stack_trace": stack_trace,
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "retry_count": 3
        }
        self.dlq_records.append(entry)
        return entry

    def get_failed_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        return list(self.dlq_records)[-limit:]

    def clear_dlq(self) -> None:
        self.dlq_records.clear()

dead_letter_queue = DeadLetterQueueManager()
