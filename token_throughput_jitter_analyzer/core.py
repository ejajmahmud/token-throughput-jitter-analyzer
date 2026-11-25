"""Core TTFT, ITL percentile, and stall-burst profiler for streaming LLMs."""
from typing import Any, Dict, List


def _percentile(sorted_vals: List[float], pct: float) -> float:
    if not sorted_vals:
        return 0.0
    idx = min(len(sorted_vals) - 1, max(0, int(round((pct / 100.0) * (len(sorted_vals) - 1)))))
    return sorted_vals[idx]


class TokenJitterAnalyzer:
    """Analyzes streaming token timestamps for TTFT, ITL percentiles, and stall bursts."""

    def __init__(self, stall_threshold_ms: float = 250.0):
        self.stall_threshold_ms = stall_threshold_ms

    def analyze(self, start_ts: float, token_timestamps: List[float]) -> Dict[str, Any]:
        if not token_timestamps:
            raise ValueError("token_timestamps must contain at least one timestamp")

        ttft_ms = max(0.0, (token_timestamps[0] - start_ts) * 1000.0)
        itls_ms = sorted(
            max(0.0, (token_timestamps[i] - token_timestamps[i - 1]) * 1000.0)
            for i in range(1, len(token_timestamps))
        )
        stalls = [gap for gap in itls_ms if gap > self.stall_threshold_ms]
        total_sec = max(1e-6, token_timestamps[-1] - start_ts)
        tps = len(token_timestamps) / total_sec

        return {
            "token_count": len(token_timestamps),
            "ttft_ms": round(ttft_ms, 2),
            "itl_p50_ms": round(_percentile(itls_ms, 50), 2),
            "itl_p95_ms": round(_percentile(itls_ms, 95), 2),
            "itl_p99_ms": round(_percentile(itls_ms, 99), 2),
            "stall_count": len(stalls),
            "tokens_per_sec": round(tps, 2),
        }
