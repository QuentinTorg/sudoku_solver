"""Benchmark runner for Sudoku puzzle corpora."""

from __future__ import annotations

import argparse
import statistics
import time
from dataclasses import dataclass
from pathlib import Path

from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import SolveStatus


@dataclass(slots=True)
class BenchmarkEntry:
    line_number: int
    status: SolveStatus
    elapsed_seconds: float


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="benchmark")
    parser.add_argument("puzzle_file", help="Path to newline-separated puzzle file")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of non-comment puzzles to process",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=1000,
        help="Print progress every N processed puzzles (0 disables)",
    )
    parser.add_argument(
        "--top-slowest",
        type=int,
        default=5,
        help="Print the N slowest puzzles by solve time",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.limit is not None and args.limit <= 0:
        raise ValueError("--limit must be > 0 when provided")
    if args.progress_every < 0:
        raise ValueError("--progress-every must be >= 0")
    if args.top_slowest < 0:
        raise ValueError("--top-slowest must be >= 0")

    path = Path(args.puzzle_file)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"error: unable to read puzzle file: {exc}")
        return 2

    entries: list[BenchmarkEntry] = []
    solved = 0
    stalled = 0
    invalid = 0

    run_start = time.perf_counter()
    for line_number, raw_line in enumerate(lines, start=1):
        puzzle = raw_line.strip()
        if not puzzle or puzzle.startswith("#"):
            continue
        if args.limit is not None and len(entries) >= args.limit:
            break

        start = time.perf_counter()
        try:
            result = solve_from_string(puzzle)
            status = result.status
        except ValueError:
            status = SolveStatus.INVALID
        elapsed_seconds = time.perf_counter() - start

        entries.append(
            BenchmarkEntry(
                line_number=line_number,
                status=status,
                elapsed_seconds=elapsed_seconds,
            )
        )

        if status is SolveStatus.SOLVED:
            solved += 1
        elif status is SolveStatus.STALLED:
            stalled += 1
        else:
            invalid += 1

        if args.progress_every > 0 and len(entries) % args.progress_every == 0:
            print(
                "progress: "
                f"processed={len(entries)} solved={solved} stalled={stalled} invalid={invalid}"
            )

    elapsed_total = time.perf_counter() - run_start
    processed = len(entries)

    if processed == 0:
        print("error: no puzzles processed")
        return 2

    durations_ms = [entry.elapsed_seconds * 1000.0 for entry in entries]
    print(f"file: {path}")
    print(f"processed: {processed}")
    print(f"solved: {solved}")
    print(f"stalled: {stalled}")
    print(f"invalid: {invalid}")
    print(f"elapsed_seconds_total: {elapsed_total:.4f}")
    print(f"throughput_puzzles_per_second: {processed / elapsed_total:.2f}")
    print(f"time_ms_avg: {statistics.mean(durations_ms):.3f}")
    print(f"time_ms_median: {statistics.median(durations_ms):.3f}")
    print(f"time_ms_p95: {percentile(durations_ms, 95):.3f}")

    if args.top_slowest > 0:
        print("slowest:")
        for entry in sorted(entries, key=lambda item: item.elapsed_seconds, reverse=True)[
            : args.top_slowest
        ]:
            print(
                f"- line={entry.line_number} status={entry.status.value} "
                f"time_ms={entry.elapsed_seconds * 1000.0:.3f}"
            )

    return 0


def percentile(values: list[float], rank: int) -> float:
    if not values:
        msg = "values must not be empty"
        raise ValueError(msg)
    if not 0 <= rank <= 100:
        msg = "rank must be in [0, 100]"
        raise ValueError(msg)
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * (rank / 100)
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(ordered) - 1)
    fraction = position - lower_index
    lower = ordered[lower_index]
    upper = ordered[upper_index]
    return lower + (upper - lower) * fraction


if __name__ == "__main__":
    raise SystemExit(main())
