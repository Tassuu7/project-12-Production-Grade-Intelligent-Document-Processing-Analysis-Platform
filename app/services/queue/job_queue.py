"""
Thread-safe Priority In-Memory and Persistent Background Processing Queue.
"""
import queue
import threading
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("app.services.queue")

class DocumentJobQueue:
    """Thread-safe FIFO/Priority Job Queue for background processing tasks."""
    
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DocumentJobQueue, cls).__new__(cls)
                cls._instance._queue = queue.PriorityQueue()
                cls._instance._running_jobs = {}
                cls._instance._jobs_lock = threading.Lock()
        return cls._instance

    def enqueue(self, job_id: int, document_id: int, user_id: int, priority: int = 0) -> None:
        """Push new job to processing queue (lower number = higher priority)."""
        # Invert priority so higher number = runs first in priority queue
        item = (-priority, job_id, {"document_id": document_id, "user_id": user_id})
        self._queue.put(item)
        logger.info(f"Enqueued Job ID {job_id} for Document ID {document_id}")

    def dequeue(self, timeout: float = 1.0) -> Optional[tuple[int, Dict[str, Any]]]:
        """Pop next available job item."""
        try:
            priority_val, job_id, payload = self._queue.get(timeout=timeout)
            with self._jobs_lock:
                self._running_jobs[job_id] = payload
            return job_id, payload
        except queue.Empty:
            return None

    def mark_completed(self, job_id: int) -> None:
        with self._jobs_lock:
            self._running_jobs.pop(job_id, None)
        self._queue.task_done()

    def get_queue_size(self) -> int:
        return self._queue.qsize()

    def get_running_count(self) -> int:
        with self._jobs_lock:
            return len(self._running_jobs)

job_queue = DocumentJobQueue()
