"""
Background Worker Thread Pool executing document processing tasks asynchronously.
"""
import threading
import time
import logging
from typing import List
from app.core.config import settings
from app.services.queue.job_queue import job_queue

logger = logging.getLogger("app.services.queue.worker")

class BackgroundWorkerPool:
    """Manages worker threads pulling document processing jobs from the queue."""

    def __init__(self, concurrency: int = 4):
        self.concurrency = concurrency
        self.workers: List[threading.Thread] = []
        self.is_running = False
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Spawn worker daemon threads."""
        if self.is_running:
            return
        
        self.is_running = True
        self._stop_event.clear()
        
        for i in range(self.concurrency):
            thread = threading.Thread(
                target=self._worker_loop,
                name=f"DocProcessor-Worker-{i+1}",
                daemon=True
            )
            thread.start()
            self.workers.append(thread)
        
        logger.info(f"Started {self.concurrency} document processing background worker threads.")

    def stop(self) -> None:
        """Signal workers to gracefully stop."""
        self.is_running = False
        self._stop_event.set()
        for t in self.workers:
            t.join(timeout=2.0)
        self.workers.clear()
        logger.info("Stopped background worker pool.")

    def _worker_loop(self) -> None:
        from app.services.queue.task_runner import execute_processing_job
        
        while not self._stop_event.is_set():
            job_item = job_queue.dequeue(timeout=0.5)
            if not job_item:
                continue
            
            job_id, payload = job_item
            logger.info(f"Worker {threading.current_thread().name} picking up Job {job_id}")
            try:
                execute_processing_job(job_id, payload["document_id"], payload["user_id"])
            except Exception as e:
                logger.exception(f"Unhandled error in worker processing job {job_id}: {str(e)}")
            finally:
                job_queue.mark_completed(job_id)

worker_pool = BackgroundWorkerPool(concurrency=settings.WORKER_CONCURRENCY)
