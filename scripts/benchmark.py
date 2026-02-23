"""Benchmark runner for Sudoku puzzle corpora."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# Ensure local benchmark runs import solver code from this workspace checkout.
_WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
_WORKSPACE_ROOT_STR = str(_WORKSPACE_ROOT)
if _WORKSPACE_ROOT_STR in sys.path:
    sys.path.remove(_WORKSPACE_ROOT_STR)
sys.path.insert(0, _WORKSPACE_ROOT_STR)

from sudoku_solver.solver import solve_from_string  # noqa: E402
from sudoku_solver.types import SolveStatus  # noqa: E402


@dataclass(slots=True)
class BenchmarkEntry:
    line_number: int
    status: SolveStatus
    elapsed_seconds: float


@dataclass(slots=True)
class TechniqueProfileEntry:
    calls: int = 0
    hits: int = 0
    elapsed_seconds: float = 0.0


def workspace_import_root() -> Path:
    """Return the workspace path that benchmark import resolution is pinned to."""
    return _WORKSPACE_ROOT


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
    parser.add_argument(
        "--allow-fallback-search",
        action="store_true",
        help="Allow fallback search after human techniques stall",
    )
    parser.add_argument(
        "--profile-techniques",
        action="store_true",
        help="Collect per-technique call/hit/runtime profiling information",
    )
    parser.add_argument(
        "--top-techniques",
        type=int,
        default=15,
        help="Print top N techniques by aggregate runtime when profiling",
    )
    parser.add_argument(
        "--output-json",
        default=None,
        help="Write machine-readable benchmark summary to this JSON file",
    )
    parser.add_argument(
        "--output-csv",
        default=None,
        help="Write per-puzzle benchmark rows to this CSV file",
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
    if args.top_techniques < 0:
        raise ValueError("--top-techniques must be >= 0")

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
    technique_profile: dict[str, TechniqueProfileEntry] = {}

    run_start = time.perf_counter()
    for line_number, raw_line in enumerate(lines, start=1):
        puzzle = raw_line.strip()
        if not puzzle or puzzle.startswith("#"):
            continue
        if args.limit is not None and len(entries) >= args.limit:
            break

        start = time.perf_counter()
        try:
            technique_attempt_hook = None
            if args.profile_techniques:
                technique_attempt_hook = _build_technique_attempt_hook(technique_profile)
            result = solve_from_string(
                puzzle,
                allow_fallback_search=args.allow_fallback_search,
                technique_attempt_hook=technique_attempt_hook,
            )
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

    if args.profile_techniques and technique_profile:
        print("technique_profile:")
        for name, metrics in sorted(
            technique_profile.items(),
            key=lambda item: item[1].elapsed_seconds,
            reverse=True,
        )[: args.top_techniques]:
            hit_rate = 0.0 if metrics.calls == 0 else (metrics.hits / metrics.calls) * 100.0
            avg_attempt_ms = (
                0.0 if metrics.calls == 0 else metrics.elapsed_seconds * 1000 / metrics.calls
            )
            print(
                f"- name={name} calls={metrics.calls} hits={metrics.hits} "
                f"hit_rate_pct={hit_rate:.2f} elapsed_seconds={metrics.elapsed_seconds:.4f} "
                f"time_ms_avg_attempt={avg_attempt_ms:.4f}"
            )

    if args.output_json is not None:
        json_path = Path(args.output_json)
        payload = _build_json_payload(
            path=path,
            entries=entries,
            solved=solved,
            stalled=stalled,
            invalid=invalid,
            elapsed_total=elapsed_total,
            technique_profile=technique_profile,
        )
        try:
            json_path.write_text(
                f"{json.dumps(payload, indent=2, sort_keys=True)}\n",
                encoding="utf-8",
            )
        except OSError as exc:
            print(f"error: unable to write JSON output: {exc}")
            return 2

    if args.output_csv is not None:
        csv_path = Path(args.output_csv)
        try:
            _write_csv_entries(csv_path, entries)
        except OSError as exc:
            print(f"error: unable to write CSV output: {exc}")
            return 2

    return 0


def _build_technique_attempt_hook(
    profile: dict[str, TechniqueProfileEntry],
):
    def _hook(name: str, elapsed_seconds: float, applied: bool) -> None:
        metrics = profile.setdefault(name, TechniqueProfileEntry())
        metrics.calls += 1
        if applied:
            metrics.hits += 1
        metrics.elapsed_seconds += elapsed_seconds

    return _hook


def _build_json_payload(
    *,
    path: Path,
    entries: list[BenchmarkEntry],
    solved: int,
    stalled: int,
    invalid: int,
    elapsed_total: float,
    technique_profile: dict[str, TechniqueProfileEntry],
) -> dict[str, object]:
    processed = len(entries)
    durations_ms = [entry.elapsed_seconds * 1000.0 for entry in entries]
    throughput = 0.0 if elapsed_total <= 0 else processed / elapsed_total
    techniques = []
    for name, metrics in sorted(
        technique_profile.items(),
        key=lambda item: item[1].elapsed_seconds,
        reverse=True,
    ):
        calls = metrics.calls
        hit_rate_pct = 0.0 if calls == 0 else (metrics.hits / calls) * 100.0
        avg_attempt_ms = 0.0 if calls == 0 else metrics.elapsed_seconds * 1000.0 / calls
        techniques.append(
            {
                "name": name,
                "calls": calls,
                "hits": metrics.hits,
                "hit_rate_pct": hit_rate_pct,
                "elapsed_seconds": metrics.elapsed_seconds,
                "time_ms_avg_attempt": avg_attempt_ms,
            }
        )

    return {
        "file": str(path),
        "processed": processed,
        "solved": solved,
        "stalled": stalled,
        "invalid": invalid,
        "elapsed_seconds_total": elapsed_total,
        "throughput_puzzles_per_second": throughput,
        "time_ms_avg": statistics.mean(durations_ms),
        "time_ms_median": statistics.median(durations_ms),
        "time_ms_p95": percentile(durations_ms, 95),
        "entries": [
            {
                "line_number": entry.line_number,
                "status": entry.status.value,
                "elapsed_seconds": entry.elapsed_seconds,
            }
            for entry in entries
        ],
        "techniques": techniques,
    }


def _write_csv_entries(path: Path, entries: list[BenchmarkEntry]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["line_number", "status", "elapsed_seconds"])
        for entry in entries:
            writer.writerow([entry.line_number, entry.status.value, f"{entry.elapsed_seconds:.9f}"])


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
