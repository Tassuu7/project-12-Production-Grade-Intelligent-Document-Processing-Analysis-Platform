"""Unit tests for Dead Letter Queue."""
from app.services.queue.dead_letter_queue import DeadLetterQueueManager

def test_dlq_recording():
    dlq = DeadLetterQueueManager()
    dlq.record_failure(job_id=1, document_id=10, user_id=2, error_message="Extraction crash")
    failed = dlq.get_failed_jobs()
    assert len(failed) == 1
    assert failed[0]["job_id"] == 1
