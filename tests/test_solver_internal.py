import unittest
from unittest.mock import patch

from sudoku_solver.grid import parse_grid
from sudoku_solver.solver import (
    _apply_step,
    _classify_difficulty,
    _find_contradiction,
    _find_unique_solution,
    _resolve_techniques,
    solve,
)
from sudoku_solver.types import DifficultyRating, Grid, SolveStatus, Step, TechniqueName


class SolverInternalTests(unittest.TestCase):
    def test_resolve_techniques_rejects_unknown_name(self) -> None:
        with self.assertRaises(ValueError) as exc:
            _resolve_techniques(["unknown_technique"])
        self.assertIn("Unknown technique", str(exc.exception))

    def test_find_contradiction_detects_missing_candidate_entry(self) -> None:
        cells = [0] + [1] * 80
        message = _find_contradiction(cells, {})
        self.assertIn("Cell 0 has no valid candidates", message)

    def test_find_contradiction_detects_empty_candidate_set(self) -> None:
        cells = [0] + [1] * 80
        message = _find_contradiction(cells, {0: set()})
        self.assertIn("Cell 0 has no valid candidates", message)

    def test_apply_step_rejects_invalid_placement_index(self) -> None:
        changed, error = _apply_step(
            [0] * 81,
            {0: {1}},
            Step(technique=TechniqueName.NAKED_SINGLE, placements=[(81, 1)]),
        )
        self.assertFalse(changed)
        self.assertIn("Invalid placement index", error)

    def test_apply_step_rejects_invalid_placement_digit(self) -> None:
        changed, error = _apply_step(
            [0] * 81,
            {0: {1}},
            Step(technique=TechniqueName.NAKED_SINGLE, placements=[(0, 10)]),
        )
        self.assertFalse(changed)
        self.assertIn("Invalid placement digit", error)

    def test_apply_step_rejects_conflicting_placement(self) -> None:
        changed, error = _apply_step(
            [2] + [0] * 80,
            {},
            Step(technique=TechniqueName.NAKED_SINGLE, placements=[(0, 1)]),
        )
        self.assertFalse(changed)
        self.assertIn("Conflicting placement", error)

    def test_apply_step_rejects_placement_not_in_candidates(self) -> None:
        changed, error = _apply_step(
            [0] * 81,
            {0: {2}},
            Step(technique=TechniqueName.NAKED_SINGLE, placements=[(0, 1)]),
        )
        self.assertFalse(changed)
        self.assertIn("not valid for cell", error)

    def test_apply_step_rejects_invalid_elimination_index(self) -> None:
        changed, error = _apply_step(
            [0] * 81,
            {0: {1}},
            Step(technique=TechniqueName.NAKED_PAIR, eliminations=[(81, 1)]),
        )
        self.assertFalse(changed)
        self.assertIn("Invalid elimination index", error)

    def test_apply_step_rejects_invalid_elimination_digit(self) -> None:
        changed, error = _apply_step(
            [0] * 81,
            {0: {1}},
            Step(technique=TechniqueName.NAKED_PAIR, eliminations=[(0, 0)]),
        )
        self.assertFalse(changed)
        self.assertIn("Invalid elimination digit", error)

    def test_apply_step_reports_no_change_when_nothing_applies(self) -> None:
        cells = [1] + [0] * 80
        candidates = {1: {2}}
        changed, error = _apply_step(
            cells,
            candidates,
            Step(
                technique=TechniqueName.NAKED_PAIR,
                placements=[],
                eliminations=[(0, 1), (1, 3)],
            ),
        )
        self.assertFalse(changed)
        self.assertIsNone(error)

    def test_apply_step_allows_redundant_placement_without_change(self) -> None:
        cells = [1] + [0] * 80
        changed, error = _apply_step(
            cells,
            {},
            Step(technique=TechniqueName.NAKED_SINGLE, placements=[(0, 1)]),
        )
        self.assertFalse(changed)
        self.assertIsNone(error)

    def test_find_unique_solution_rejects_duplicate_givens(self) -> None:
        solution, count = _find_unique_solution([1, 1] + [0] * 79)
        self.assertIsNone(solution)
        self.assertEqual(count, 0)

    def test_find_unique_solution_reports_non_unique_puzzle(self) -> None:
        solution, count = _find_unique_solution([0] * 81)
        self.assertIsNone(solution)
        self.assertGreaterEqual(count, 2)

    def test_solve_returns_invalid_when_step_application_errors(self) -> None:
        bad_step = Step(
            technique=TechniqueName.NAKED_SINGLE,
            placements=[(81, 1)],
        )
        with patch("sudoku_solver.solver.apply_naked_single", return_value=bad_step):
            result = solve(parse_grid("." * 81), techniques=["naked_single"])
        self.assertEqual(result.status, SolveStatus.INVALID)
        self.assertIn("Invalid placement index", result.message)

    def test_solve_handles_no_change_steps_and_uses_fallback(self) -> None:
        no_change_step = Step(
            technique=TechniqueName.NAKED_SINGLE,
            placements=[],
            eliminations=[(0, 9)],
        )
        puzzle = (
            "53467891267219534819834256785976142342685379171392485696153728428741963534528617."
        )
        with patch("sudoku_solver.solver.apply_naked_single", return_value=no_change_step):
            result = solve(parse_grid(puzzle), techniques=["naked_single"])
        self.assertEqual(result.status, SolveStatus.SOLVED)
        self.assertEqual(result.message, "Puzzle solved with fallback search.")

    def test_solve_returns_invalid_when_fallback_finds_no_solution(self) -> None:
        with patch("sudoku_solver.solver._find_unique_solution", return_value=(None, 0)):
            result = solve(parse_grid("." * 81), techniques=[])
        self.assertEqual(result.status, SolveStatus.INVALID)
        self.assertIn("No valid solution exists", result.message)

    def test_solve_from_grid_with_no_zeroes_returns_immediate_solved(self) -> None:
        solved = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        result = solve(parse_grid(solved))
        self.assertEqual(result.status, SolveStatus.SOLVED)
        self.assertEqual(result.message, "Puzzle is already solved.")

    def test_solve_detects_invalid_candidate_state_from_normalization(self) -> None:
        with patch("sudoku_solver.solver._normalize_candidates", return_value={}):
            result = solve(parse_grid("." * 81), techniques=[])
        self.assertEqual(result.status, SolveStatus.INVALID)
        self.assertIn("Cell 0 has no valid candidates", result.message)

    def test_solve_reports_invalid_for_short_grid(self) -> None:
        with self.assertRaises(ValueError):
            solve(Grid(cells=(0,) * 80))

    def test_classify_difficulty_returns_medium_for_pair_based_techniques(self) -> None:
        steps = [
            Step(technique=TechniqueName.NAKED_SINGLE),
            Step(technique=TechniqueName.NAKED_PAIR),
        ]
        rating = _classify_difficulty(steps, used_fallback=False)
        self.assertEqual(rating, DifficultyRating.MEDIUM)

    def test_classify_difficulty_returns_hard_for_triples(self) -> None:
        steps = [Step(technique=TechniqueName.HIDDEN_TRIPLE)]
        rating = _classify_difficulty(steps, used_fallback=False)
        self.assertEqual(rating, DifficultyRating.HARD)

    def test_classify_difficulty_returns_expert_for_fallback(self) -> None:
        steps = [Step(technique=TechniqueName.NAKED_SINGLE)]
        rating = _classify_difficulty(steps, used_fallback=True)
        self.assertEqual(rating, DifficultyRating.EXPERT)


if __name__ == "__main__":
    unittest.main()
