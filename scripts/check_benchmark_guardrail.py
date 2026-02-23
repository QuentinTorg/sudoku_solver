"""Validate benchmark summary metrics against configured thresholds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="check-benchmark-guardrail")
    parser.add_argument("benchmark_json", help="Path to benchmark JSON summary file")
    parser.add_argument(
        "--max-avg-ms",
        type=float,
        default=700.0,
        help="Maximum allowed average solve time in milliseconds",
    )
    parser.add_argument(
        "--max-p95-ms",
        type=float,
        default=2500.0,
        help="Maximum allowed p95 solve time in milliseconds",
    )
    parser.add_argument(
        "--min-throughput",
        type=float,
        default=2.5,
        help="Minimum required puzzles/second throughput",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.max_avg_ms <= 0:
        raise ValueError("--max-avg-ms must be > 0")
    if args.max_p95_ms <= 0:
        raise ValueError("--max-p95-ms must be > 0")
    if args.min_throughput <= 0:
        raise ValueError("--min-throughput must be > 0")

    path = Path(args.benchmark_json)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"error: unable to read benchmark JSON: {exc}")
        return 2
    except json.JSONDecodeError as exc:
        print(f"error: invalid benchmark JSON: {exc}")
        return 2

    try:
        avg_ms = float(payload["time_ms_avg"])
        p95_ms = float(payload["time_ms_p95"])
        throughput = float(payload["throughput_puzzles_per_second"])
    except (KeyError, TypeError, ValueError) as exc:
        print(f"error: benchmark JSON missing or invalid required fields: {exc}")
        return 2

    violations: list[str] = []
    if avg_ms > args.max_avg_ms:
        violations.append(f"time_ms_avg {avg_ms:.3f} exceeded max {args.max_avg_ms:.3f}")
    if p95_ms > args.max_p95_ms:
        violations.append(f"time_ms_p95 {p95_ms:.3f} exceeded max {args.max_p95_ms:.3f}")
    if throughput < args.min_throughput:
        violations.append(
            f"throughput_puzzles_per_second {throughput:.3f} below min {args.min_throughput:.3f}"
        )

    if violations:
        print("benchmark guardrail failed:")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print(
        "benchmark guardrail passed: "
        f"avg_ms={avg_ms:.3f} p95_ms={p95_ms:.3f} throughput={throughput:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
