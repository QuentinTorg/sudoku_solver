"""Command-line interface for sudoku_solver."""

import argparse
from pathlib import Path

from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import SolveStatus

PROGRESS_INTERVAL = 1000


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="sudoku_solver")
    parser.add_argument("puzzle", nargs="?", help="81-character Sudoku puzzle string")
    parser.add_argument(
        "--puzzle-file",
        help="Path to newline-separated puzzle file (one 81-char puzzle per line)",
    )
    parser.add_argument(
        "--max-failures",
        type=int,
        default=50,
        help="Stop file-mode run after this many failed puzzles",
    )
    parser.add_argument("--show-steps", action="store_true", help="Print step trace")
    parser.add_argument("--max-steps", type=int, default=None, help="Maximum steps to emit")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the sudoku_solver CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.max_failures is not None and args.max_failures < 0:
        parser.error("--max-failures must be >= 0")

    if args.puzzle_file:
        if args.puzzle is not None:
            parser.error("Use either a puzzle string or --puzzle-file, not both.")
        return _run_puzzle_file(
            Path(args.puzzle_file),
            max_failures=args.max_failures,
            show_steps=args.show_steps,
            max_steps=args.max_steps,
        )

    if args.puzzle is None:
        parser.error("Provide a puzzle string or use --puzzle-file.")

    result = solve_from_string(args.puzzle)
    _print_single_result(result)

    if args.show_steps:
        for step in result.steps[: args.max_steps]:
            print(
                f"- {step.technique.value} "
                f"placements={step.placements} eliminations={step.eliminations}"
            )

    if result.status is SolveStatus.INVALID:
        return 2
    return 0


def _print_single_result(result) -> None:
    print(f"status: {result.status.value}")
    print(f"grid: {result.grid_string}")
    if result.message:
        print(f"message: {result.message}")


def _run_puzzle_file(
    path: Path,
    *,
    max_failures: int | None,
    show_steps: bool,
    max_steps: int | None,
) -> int:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"error: unable to read puzzle file: {exc}")
        return 2

    total = 0
    solved = 0
    stalled = 0
    invalid = 0
    failures: list[tuple[int, str, str, str | None]] = []
    stopped_early = False

    for line_number, raw_line in enumerate(lines, start=1):
        puzzle = raw_line.strip()
        if not puzzle or puzzle.startswith("#"):
            continue

        total += 1
        try:
            result = solve_from_string(puzzle)
        except ValueError as exc:
            invalid += 1
            failures.append((line_number, "invalid", str(exc), None))
            _maybe_print_progress(total, solved, stalled, invalid)
            continue

        if result.status is SolveStatus.SOLVED:
            solved += 1
            _maybe_print_progress(total, solved, stalled, invalid)
            continue

        if result.status is SolveStatus.STALLED:
            stalled += 1
            failures.append((line_number, "stalled", result.message, result.grid_string))
            if show_steps and result.steps:
                _print_file_steps(line_number, result, max_steps)
            _maybe_print_progress(total, solved, stalled, invalid)
            if max_failures is not None and len(failures) >= max_failures:
                stopped_early = True
                break
            continue

        invalid += 1
        failures.append((line_number, "invalid", result.message, result.grid_string))
        if show_steps and result.steps:
            _print_file_steps(line_number, result, max_steps)
        _maybe_print_progress(total, solved, stalled, invalid)
        if max_failures is not None and len(failures) >= max_failures:
            stopped_early = True
            break

    print(f"file: {path}")
    print(f"total: {total}")
    print(f"solved: {solved}")
    print(f"stalled: {stalled}")
    print(f"invalid: {invalid}")
    if stopped_early:
        print(f"stopped_early: reached max_failures={max_failures}")

    if failures:
        print(f"failures: {len(failures)}")
        for line_number, status, message, grid_string in failures:
            print(f"- line {line_number}: {status} ({message})")
            if status == "stalled" and grid_string is not None:
                print(f"  ending_grid: {grid_string}")
        return 1

    return 0


def _print_file_steps(line_number: int, result, max_steps: int | None) -> None:
    print(f"steps line {line_number}:")
    for step in result.steps[:max_steps]:
        print(
            f"- {step.technique.value} "
            f"placements={step.placements} eliminations={step.eliminations}"
        )


def _maybe_print_progress(total: int, solved: int, stalled: int, invalid: int) -> None:
    if total % PROGRESS_INTERVAL != 0:
        return
    print(
        f"progress: processed={total} solved={solved} stalled={stalled} invalid={invalid}",
        flush=True,
    )
