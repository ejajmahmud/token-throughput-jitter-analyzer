"""Tests for Token Throughput Jitter Analyzer."""
import unittest
from token_throughput_jitter_analyzer.core import TokenJitterAnalyzer


class TestTokenJitterAnalyzer(unittest.TestCase):
    def test_computes_ttft_percentiles_and_stalls(self):
        analyzer = TokenJitterAnalyzer(stall_threshold_ms=200.0)
        res = analyzer.analyze(10.0, [10.10, 10.12, 10.14, 10.50, 10.52])
        self.assertAlmostEqual(res["ttft_ms"], 100.0, places=1)
        self.assertEqual(res["stall_count"], 1)
        self.assertAlmostEqual(res["itl_p50_ms"], 20.0, places=1)
        self.assertGreater(res["itl_p99_ms"], 300.0)

    def test_empty_timestamps_raises(self):
        with self.assertRaises(ValueError):
            TokenJitterAnalyzer().analyze(0.0, [])
