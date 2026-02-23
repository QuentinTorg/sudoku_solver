"""Main solver orchestration loop."""

from sudoku_solver.candidates import get_candidates
from sudoku_solver.grid import format_grid, parse_grid
from sudoku_solver.techniques import (
    apply_als_xz,
    apply_bug_plus_one,
    apply_empty_rectangle,
    apply_finned_swordfish,
    apply_finned_x_wing,
    apply_hidden_pair,
    apply_hidden_quad,
    apply_hidden_single,
    apply_hidden_triple,
    apply_jellyfish,
    apply_locked_candidates,
    apply_naked_pair,
    apply_naked_quad,
    apply_naked_single,
    apply_naked_triple,
    apply_remote_pairs,
    apply_simple_coloring,
    apply_skyscraper,
    apply_sue_de_coq,
    apply_swordfish,
    apply_two_string_kite,
    apply_unique_rectangle,
    apply_w_wing,
    apply_x_cycles,
    apply_x_wing,
    apply_xy_chain,
    apply_xy_wing,
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

_HIGH_RISK_TECHNIQUES = {
    TechniqueName.XY_WING,
    TechniqueName.XYZ_WING,
    TechniqueName.W_WING,
    TechniqueName.FINNED_X_WING,
    TechniqueName.FINNED_SWORDFISH,
    TechniqueName.EMPTY_RECTANGLE,
    TechniqueName.REMOTE_PAIRS,
    TechniqueName.TWO_STRING_KITE,
    TechniqueName.SKYSCRAPER,
    TechniqueName.UNIQUE_RECTANGLE,
    TechniqueName.SIMPLE_COLORING,
    TechniqueName.X_CYCLES,
    TechniqueName.XY_CHAIN,
    TechniqueName.ALS_XZ,
    TechniqueName.SUE_DE_COQ,
}


def solve(
    grid: Grid,
    *,
    techniques: list[str] | None = None,
    allow_fallback_search: bool = False,
) -> SolveResult:
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
            used_fallback_search=False,
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
                used_fallback_search=False,
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
                used_fallback_search=False,
            )

        progress = False
        for technique in technique_order:
            step = technique(current_grid, candidates)
            if step is None:
                continue

            if step.technique in _HIGH_RISK_TECHNIQUES and not _step_preserves_solution(
                cells, candidates, step
            ):
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
                    used_fallback_search=False,
                )
            if not changed:
                continue

            updated_grid = Grid(cells=tuple(cells))
            step.grid_snapshot_after = format_grid(updated_grid)
            steps.append(step)
            progress = True
            break

        if not progress:
            if not allow_fallback_search:
                stalled_grid = Grid(cells=tuple(cells))
                return SolveResult(
                    status=SolveStatus.STALLED,
                    grid=stalled_grid,
                    grid_string=format_grid(stalled_grid),
                    steps=steps,
                    message=(
                        "No further human-technique moves were applied. "
                        "Fallback search is disabled."
                    ),
                    technique_counts=_count_techniques(steps),
                    difficulty=DifficultyRating.UNSOLVED,
                    used_fallback_search=False,
                )

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
                    used_fallback_search=True,
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
                    used_fallback_search=False,
                )

            stalled_grid = Grid(cells=tuple(cells))
            return SolveResult(
                status=SolveStatus.STALLED,
                grid=stalled_grid,
                grid_string=format_grid(stalled_grid),
                steps=steps,
                message="No further human-technique moves were applied.",
                technique_counts=_count_techniques(steps),
                difficulty=DifficultyRating.UNSOLVED,
                used_fallback_search=False,
            )


def solve_from_string(
    puzzle: str,
    *,
    techniques: list[str] | None = None,
    allow_fallback_search: bool = False,
) -> SolveResult:
    """Parse and solve from puzzle string input."""
    grid = parse_grid(puzzle)
    return solve(
        grid,
        techniques=techniques,
        allow_fallback_search=allow_fallback_search,
    )


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
        "naked_quad": apply_naked_quad,
        "hidden_quad": apply_hidden_quad,
        "xy_wing": apply_xy_wing,
        "xyz_wing": apply_xyz_wing,
        "x_wing": apply_x_wing,
        "finned_x_wing": apply_finned_x_wing,
        "swordfish": apply_swordfish,
        "finned_swordfish": apply_finned_swordfish,
        "jellyfish": apply_jellyfish,
        "simple_coloring": apply_simple_coloring,
        "x_cycles": apply_x_cycles,
        "xy_chain": apply_xy_chain,
        "als_xz": apply_als_xz,
        "sue_de_coq": apply_sue_de_coq,
        "bug_plus_one": apply_bug_plus_one,
        "empty_rectangle": apply_empty_rectangle,
        "remote_pairs": apply_remote_pairs,
        "unique_rectangle": apply_unique_rectangle,
        "skyscraper": apply_skyscraper,
        "two_string_kite": apply_two_string_kite,
        "w_wing": apply_w_wing,
    }
    default_order = (
        apply_naked_single,
        apply_hidden_single,
        apply_locked_candidates,
        apply_naked_pair,
        apply_hidden_pair,
        apply_naked_triple,
        apply_hidden_triple,
        apply_naked_quad,
        apply_hidden_quad,
        apply_xy_wing,
        apply_xyz_wing,
        apply_x_wing,
        apply_w_wing,
        apply_swordfish,
        apply_jellyfish,
        apply_bug_plus_one,
        apply_simple_coloring,
        apply_x_cycles,
        apply_xy_chain,
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
    return _find_unique_solution_limited(cells, max_solutions=2)


def _find_unique_solution_limited(
    cells: list[int],
    *,
    max_solutions: int,
) -> tuple[tuple[int, ...] | None, int]:
    if max_solutions <= 0:
        msg = "max_solutions must be >= 1"
        raise ValueError(msg)
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
        if len(solutions) >= max_solutions:
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

            if len(solutions) >= max_solutions:
                return

    backtrack()
    if len(solutions) == 1:
        return solutions[0], 1
    return None, len(solutions)


def _step_preserves_solution(
    cells: list[int],
    candidates: dict[int, set[int]],
    step: Step,
) -> bool:
    for cell_index, digit in step.placements:
        if not _assignment_has_solution(cells, cell_index, digit):
            return False

    for cell_index, digit in step.eliminations:
        if cells[cell_index] != 0:
            continue
        # Conservative guard: only eliminate a digit when that assignment
        # cannot participate in any valid completion of the current grid.
        if _assignment_has_solution(cells, cell_index, digit):
            return False

    test_cells = list(cells)
    test_candidates = {cell_index: set(options) for cell_index, options in candidates.items()}

    changed, error = _apply_step(test_cells, test_candidates, step)
    if error is not None or not changed:
        return False

    test_grid = Grid(cells=tuple(test_cells))
    normalized_candidates = _normalize_candidates(test_grid, test_candidates)
    if _find_contradiction(test_cells, normalized_candidates) is not None:
        return False
    if 0 not in test_cells:
        return True

    _, solution_count = _find_unique_solution_limited(test_cells, max_solutions=1)
    return solution_count > 0


def _assignment_has_solution(cells: list[int], cell_index: int, digit: int) -> bool:
    if not 0 <= cell_index < 81:
        return False
    if not 1 <= digit <= 9:
        return False
    if cells[cell_index] not in (0, digit):
        return False

    constrained = list(cells)
    constrained[cell_index] = digit
    _, solution_count = _find_unique_solution_limited(constrained, max_solutions=1)
    return solution_count > 0


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
        TechniqueName.JELLYFISH in techniques_used
        or TechniqueName.FINNED_SWORDFISH in techniques_used
        or TechniqueName.FINNED_X_WING in techniques_used
        or TechniqueName.SIMPLE_COLORING in techniques_used
        or TechniqueName.X_CYCLES in techniques_used
        or TechniqueName.XY_CHAIN in techniques_used
        or TechniqueName.ALS_XZ in techniques_used
        or TechniqueName.SUE_DE_COQ in techniques_used
    ):
        return DifficultyRating.EXPERT
    if (
        TechniqueName.X_WING in techniques_used
        or TechniqueName.XY_WING in techniques_used
        or TechniqueName.W_WING in techniques_used
        or TechniqueName.SWORDFISH in techniques_used
        or TechniqueName.NAKED_QUAD in techniques_used
        or TechniqueName.HIDDEN_QUAD in techniques_used
        or TechniqueName.EMPTY_RECTANGLE in techniques_used
        or TechniqueName.REMOTE_PAIRS in techniques_used
        or TechniqueName.BUG_PLUS_ONE in techniques_used
        or TechniqueName.TWO_STRING_KITE in techniques_used
        or TechniqueName.SKYSCRAPER in techniques_used
        or TechniqueName.UNIQUE_RECTANGLE in techniques_used
    ):
        return DifficultyRating.HARD
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
