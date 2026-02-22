"""Main solver orchestration loop."""

from sudoku_solver.candidates import get_candidates
from sudoku_solver.grid import format_grid, parse_grid
from sudoku_solver.techniques import (
    apply_hidden_pair,
    apply_hidden_single,
    apply_locked_candidates,
    apply_naked_pair,
    apply_naked_single,
)
from sudoku_solver.types import Grid, SolveResult, SolveStatus, Step


def solve(grid: Grid, *, techniques: list[str] | None = None) -> SolveResult:
    """Solve a Sudoku grid using configured human techniques."""
    _ = techniques  # Extension point for custom ordering in later iterations.
    grid_string = format_grid(grid)

    if 0 not in grid.cells:
        return SolveResult(
            status=SolveStatus.SOLVED,
            grid=grid,
            grid_string=grid_string,
            steps=[],
            message="Puzzle is already solved.",
        )

    candidates = get_candidates(grid)
    if any(len(options) == 0 for options in candidates.values()):
        return SolveResult(
            status=SolveStatus.INVALID,
            grid=grid,
            grid_string=grid_string,
            steps=[],
            message="At least one unsolved cell has no valid candidates.",
        )

    step = _first_applicable_step(grid, candidates)
    steps: list[Step] = []
    if step is not None:
        steps.append(step)

    return SolveResult(
        status=SolveStatus.STALLED,
        grid=grid,
        grid_string=grid_string,
        steps=steps,
        message="No further v1 moves were applied.",
    )


def solve_from_string(puzzle: str, *, techniques: list[str] | None = None) -> SolveResult:
    """Parse and solve from puzzle string input."""
    grid = parse_grid(puzzle)
    return solve(grid, techniques=techniques)


def _first_applicable_step(grid: Grid, candidates: dict[int, set[int]]) -> Step | None:
    for technique in (
        apply_naked_single,
        apply_hidden_single,
        apply_locked_candidates,
        apply_naked_pair,
        apply_hidden_pair,
    ):
        step = technique(grid, candidates)
        if step is not None:
            return step
    return None
