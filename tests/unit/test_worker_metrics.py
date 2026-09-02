"""Unit tests for Worker Metrics."""
from app.services.queue.worker_metrics import WorkerMetricsCollector

def test_worker_metrics_recording():
    collector = WorkerMetricsCollector()
    collector.record_job_completion(duration_ms=45.0, success=True)
    collector.record_job_completion(duration_ms=55.0, success=True)
    metrics = collector.get_summary_metrics()
    assert metrics["total_completed"] == 2
    assert metrics["avg_latency_ms"] == 50.0
