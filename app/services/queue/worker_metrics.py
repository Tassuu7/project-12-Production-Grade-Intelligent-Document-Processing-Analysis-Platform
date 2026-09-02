"""
Worker Telemetry and Latency Percentile Profiler.
Monitors p50, p95, and p99 processing durations and queue throughput metrics.
"""
import time
from typing import List, Dict, Any

class WorkerMetricsCollector:
    """Tracks latency percentiles and throughput counters for document processing workers."""

    def __init__(self, window_size: int = 500):
        self.window_size = window_size
        self.latencies: List[float] = []
        self.total_processed_count: int = 0
        self.total_failed_count: int = 0
        self.start_timestamp: float = time.time()

    def record_job_completion(self, duration_ms: float, success: bool = True) -> None:
        if success:
            self.total_processed_count += 1
            self.latencies.append(duration_ms)
            if len(self.latencies) > self.window_size:
                self.latencies.pop(0)
        else:
            self.total_failed_count += 1

    def get_summary_metrics(self) -> Dict[str, Any]:
        if not self.latencies:
            return {
                "total_completed": self.total_processed_count,
                "total_failed": self.total_failed_count,
                "p50_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "p99_latency_ms": 0.0,
                "avg_latency_ms": 0.0
            }

        sorted_lat = sorted(self.latencies)
        n = len(sorted_lat)

        p50 = sorted_lat[int(0.50 * n)]
        p95 = sorted_lat[min(n - 1, int(0.95 * n))]
        p99 = sorted_lat[min(n - 1, int(0.99 * n))]
        avg = sum(sorted_lat) / n

        return {
            "total_completed": self.total_processed_count,
            "total_failed": self.total_failed_count,
            "p50_latency_ms": round(p50, 2),
            "p95_latency_ms": round(p95, 2),
            "p99_latency_ms": round(p99, 2),
            "avg_latency_ms": round(avg, 2)
        }

worker_metrics = WorkerMetricsCollector()
