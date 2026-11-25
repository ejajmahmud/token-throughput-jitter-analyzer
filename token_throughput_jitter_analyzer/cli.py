"""CLI for Token Throughput Jitter Analyzer."""
import argparse
import json
from .core import TokenJitterAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Token Throughput Jitter Analyzer CLI")
    parser.add_argument("--stall-ms", type=float, default=200.0, help="Stall threshold in ms")
    args = parser.parse_args()

    analyzer = TokenJitterAnalyzer(stall_threshold_ms=args.stall_ms)
    res = analyzer.analyze(0.0, [0.10, 0.12, 0.14, 0.16, 0.52, 0.54, 0.56])
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
