"""Command-line interface for sudoku_solver."""

import argparse

from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import SolveStatus


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(prog="sudoku_solver")
    parser.add_argument("puzzle", help="81-character Sudoku puzzle string")
    parser.add_argument("--show-steps", action="store_true", help="Print step trace")
    parser.add_argument("--max-steps", type=int, default=None, help="Maximum steps to emit")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the sudoku_solver CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    result = solve_from_string(args.puzzle)

    print(f"status: {result.status.value}")
    print(f"grid: {result.grid_string}")
    if result.message:
        print(f"message: {result.message}")

    if args.show_steps:
        for step in result.steps[: args.max_steps]:
            print(
                f"- {step.technique.value} "
                f"placements={step.placements} eliminations={step.eliminations}"
            )

    if result.status is SolveStatus.INVALID:
        return 2
    return 0
