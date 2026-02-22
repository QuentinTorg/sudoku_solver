"""Main solver orchestration loop."""

from sudoku_solver.candidates import get_candidates
from sudoku_solver.grid import format_grid, parse_grid
from sudoku_solver.techniques import (
    apply_hidden_pair,
    apply_hidden_single,
    apply_hidden_triple,
    apply_locked_candidates,
    apply_naked_pair,
    apply_naked_single,
    apply_naked_triple,
    apply_xyz_wing,
)
from sudoku_solver.types import (
    DifficultyRating,
    Grid,
    SolveResult,
    SolveStatus,
    Step,
    TechniqueName,
)


def solve(grid: Grid, *, techniques: list[str] | None = None) -> SolveResult:
    """Solve a Sudoku grid using configured human techniques."""
    technique_order = _resolve_techniques(techniques)
    cells = list(grid.cells)
    steps: list[Step] = []

    if 0 not in cells:
        solved_grid = Grid(cells=tuple(cells))
        return SolveResult(
            status=SolveStatus.SOLVED,
            grid=solved_grid,
            grid_string=format_grid(solved_grid),
            steps=[],
            message="Puzzle is already solved.",
            technique_counts={},
            difficulty=DifficultyRating.EASY,
        )

    candidates = get_candidates(Grid(cells=tuple(cells)))
    while True:
        current_grid = Grid(cells=tuple(cells))
        candidates = _normalize_candidates(current_grid, candidates)
        contradiction = _find_contradiction(cells, candidates)
        if contradiction is not None:
            return SolveResult(
                status=SolveStatus.INVALID,
                grid=current_grid,
                grid_string=format_grid(current_grid),
                steps=steps,
                message=contradiction,
                technique_counts=_count_techniques(steps),
                difficulty=DifficultyRating.UNSOLVED,
            )

        if 0 not in cells:
            solved_grid = Grid(cells=tuple(cells))
            return SolveResult(
                status=SolveStatus.SOLVED,
                grid=solved_grid,
                grid_string=format_grid(solved_grid),
                steps=steps,
                message="Puzzle solved with configured techniques.",
                technique_counts=_count_techniques(steps),
                difficulty=_classify_difficulty(steps, used_fallback=False),
            )

        progress = False
        for technique in technique_order:
            step = technique(current_grid, candidates)
            if step is None:
                continue

            changed, error = _apply_step(cells, candidates, step)
            if error is not None:
                invalid_grid = Grid(cells=tuple(cells))
                return SolveResult(
                    status=SolveStatus.INVALID,
                    grid=invalid_grid,
                    grid_string=format_grid(invalid_grid),
                    steps=steps,
                    message=error,
                    technique_counts=_count_techniques(steps),
                    difficulty=DifficultyRating.UNSOLVED,
                )
            if not changed:
                continue

            updated_grid = Grid(cells=tuple(cells))
            step.grid_snapshot_after = format_grid(updated_grid)
            steps.append(step)
            progress = True
            break

        if not progress:
            unique_solution, solution_count = _find_unique_solution(cells)
            if unique_solution is not None:
                solved_grid = Grid(cells=unique_solution)
                return SolveResult(
                    status=SolveStatus.SOLVED,
                    grid=solved_grid,
                    grid_string=format_grid(solved_grid),
                    steps=steps,
                    message="Puzzle solved with fallback search.",
                    technique_counts=_count_techniques(steps),
                    difficulty=_classify_difficulty(steps, used_fallback=True),
                )
            if solution_count == 0:
                invalid_grid = Grid(cells=tuple(cells))
                return SolveResult(
                    status=SolveStatus.INVALID,
                    grid=invalid_grid,
                    grid_string=format_grid(invalid_grid),
                    steps=steps,
                    message="No valid solution exists for current grid state.",
                    technique_counts=_count_techniques(steps),
                    difficulty=DifficultyRating.UNSOLVED,
                )

            stalled_grid = Grid(cells=tuple(cells))
            return SolveResult(
                status=SolveStatus.STALLED,
                grid=stalled_grid,
                grid_string=format_grid(stalled_grid),
                steps=steps,
                message="No further v1 moves were applied.",
                technique_counts=_count_techniques(steps),
                difficulty=DifficultyRating.UNSOLVED,
            )


def solve_from_string(puzzle: str, *, techniques: list[str] | None = None) -> SolveResult:
    """Parse and solve from puzzle string input."""
    grid = parse_grid(puzzle)
    return solve(grid, techniques=techniques)


def _resolve_techniques(
    techniques: list[str] | None,
) -> tuple:
    available = {
        "naked_single": apply_naked_single,
        "hidden_single": apply_hidden_single,
        "locked_candidates": apply_locked_candidates,
        "naked_pair": apply_naked_pair,
        "hidden_pair": apply_hidden_pair,
        "naked_triple": apply_naked_triple,
        "hidden_triple": apply_hidden_triple,
        "xyz_wing": apply_xyz_wing,
    }
    default_order = (
        apply_naked_single,
        apply_hidden_single,
        apply_locked_candidates,
        apply_naked_pair,
        apply_hidden_pair,
        apply_naked_triple,
        apply_hidden_triple,
        apply_xyz_wing,
    )

    if techniques is None:
        return default_order

    resolved = []
    for name in techniques:
        if name not in available:
            msg = f"Unknown technique: {name}"
            raise ValueError(msg)
        resolved.append(available[name])
    return tuple(resolved)


def _normalize_candidates(grid: Grid, candidates: dict[int, set[int]]) -> dict[int, set[int]]:
    base_candidates = get_candidates(grid)
    normalized: dict[int, set[int]] = {}

    for cell_index, base_options in base_candidates.items():
        retained_options = candidates.get(cell_index, set(base_options))
        normalized[cell_index] = set(base_options) & set(retained_options)

    return normalized


def _find_contradiction(cells: list[int], candidates: dict[int, set[int]]) -> str | None:
    for index, value in enumerate(cells):
        if value != 0:
            continue
        if index not in candidates or len(candidates[index]) == 0:
            return f"Cell {index} has no valid candidates."
    return None


def _apply_step(
    cells: list[int],
    candidates: dict[int, set[int]],
    step: Step,
) -> tuple[bool, str | None]:
    changed = False

    for cell_index, digit in step.placements:
        if not 0 <= cell_index < 81:
            return False, f"Invalid placement index: {cell_index}"
        if not 1 <= digit <= 9:
            return False, f"Invalid placement digit: {digit}"

        current_value = cells[cell_index]
        if current_value not in (0, digit):
            return False, f"Conflicting placement at cell {cell_index}."
        if current_value == 0 and digit not in candidates.get(cell_index, set()):
            return False, f"Placement digit {digit} is not valid for cell {cell_index}."
        if current_value == 0:
            cells[cell_index] = digit
            changed = True

    for cell_index, digit in step.eliminations:
        if not 0 <= cell_index < 81:
            return False, f"Invalid elimination index: {cell_index}"
        if not 1 <= digit <= 9:
            return False, f"Invalid elimination digit: {digit}"
        if cells[cell_index] != 0:
            continue

        options = candidates.setdefault(cell_index, set(range(1, 10)))
        if digit in options:
            options.remove(digit)
            changed = True

    for index, value in enumerate(cells):
        if value != 0 and index in candidates:
            del candidates[index]

    return changed, None


def _find_unique_solution(cells: list[int]) -> tuple[tuple[int, ...] | None, int]:
    state = list(cells)
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for index, value in enumerate(state):
        if value == 0:
            continue
        row = index // 9
        col = index % 9
        box = (row // 3) * 3 + (col // 3)
        if value in rows[row] or value in cols[col] or value in boxes[box]:
            return None, 0
        rows[row].add(value)
        cols[col].add(value)
        boxes[box].add(value)

    solutions: list[tuple[int, ...]] = []

    def backtrack() -> None:
        if len(solutions) >= 2:
            return

        best_index = -1
        best_options: list[int] | None = None
        for index, value in enumerate(state):
            if value != 0:
                continue
            row = index // 9
            col = index % 9
            box = (row // 3) * 3 + (col // 3)
            options = [
                digit
                for digit in range(1, 10)
                if digit not in rows[row] and digit not in cols[col] and digit not in boxes[box]
            ]
            if len(options) == 0:
                return
            if best_options is None or len(options) < len(best_options):
                best_index = index
                best_options = options
                if len(best_options) == 1:
                    break

        if best_index == -1:
            solutions.append(tuple(state))
            return

        row = best_index // 9
        col = best_index % 9
        box = (row // 3) * 3 + (col // 3)
        assert best_options is not None
        for digit in best_options:
            state[best_index] = digit
            rows[row].add(digit)
            cols[col].add(digit)
            boxes[box].add(digit)

            backtrack()

            state[best_index] = 0
            rows[row].remove(digit)
            cols[col].remove(digit)
            boxes[box].remove(digit)

            if len(solutions) >= 2:
                return

    backtrack()
    if len(solutions) == 1:
        return solutions[0], 1
    return None, len(solutions)


def _count_techniques(steps: list[Step]) -> dict[TechniqueName, int]:
    counts: dict[TechniqueName, int] = {}
    for step in steps:
        counts[step.technique] = counts.get(step.technique, 0) + 1
    return counts


def _classify_difficulty(
    steps: list[Step],
    *,
    used_fallback: bool,
) -> DifficultyRating:
    if used_fallback:
        return DifficultyRating.EXPERT
    if not steps:
        return DifficultyRating.EASY

    techniques_used = {step.technique for step in steps}
    if TechniqueName.XYZ_WING in techniques_used:
        return DifficultyRating.EXPERT
    if (
        TechniqueName.NAKED_TRIPLE in techniques_used
        or TechniqueName.HIDDEN_TRIPLE in techniques_used
    ):
        return DifficultyRating.HARD
    if (
        TechniqueName.LOCKED_CANDIDATES in techniques_used
        or TechniqueName.NAKED_PAIR in techniques_used
        or TechniqueName.HIDDEN_PAIR in techniques_used
    ):
        return DifficultyRating.MEDIUM
    return DifficultyRating.EASY
