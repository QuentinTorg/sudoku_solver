import unittest

from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import DifficultyRating, SolveStatus, TechniqueName


class SolverTests(unittest.TestCase):
    def test_solve_from_string_returns_solved_for_completed_grid(self) -> None:
        solved = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        result = solve_from_string(solved)
        self.assertEqual(result.status, SolveStatus.SOLVED)
        self.assertEqual(result.grid_string, solved)
        self.assertEqual(result.steps, [])
        self.assertEqual(result.difficulty, DifficultyRating.EASY)
        self.assertFalse(result.used_fallback_search)

    def test_solve_from_string_solves_when_v1_step_sequence_is_available(self) -> None:
        almost_solved = (
            "53467891267219534819834256785976142342685379171392485696153728428741963534528617."
        )
        result = solve_from_string(almost_solved)
        self.assertEqual(result.status, SolveStatus.SOLVED)
        self.assertEqual(result.grid_string, almost_solved[:-1] + "9")
        self.assertEqual(len(result.steps), 1)
        self.assertEqual(result.steps[0].technique, TechniqueName.NAKED_SINGLE)
        self.assertEqual(result.steps[0].placements, [(80, 9)])
        self.assertEqual(result.difficulty, DifficultyRating.EASY)
        self.assertFalse(result.used_fallback_search)

    def test_solve_from_string_returns_stalled_when_no_technique_applies(self) -> None:
        blank = "." * 81
        result = solve_from_string(blank)
        self.assertEqual(result.status, SolveStatus.STALLED)
        self.assertEqual(result.grid_string, blank)
        self.assertEqual(result.steps, [])
        self.assertEqual(result.difficulty, DifficultyRating.UNSOLVED)
        self.assertFalse(result.used_fallback_search)

    def test_solve_from_string_sets_fallback_flag_when_search_is_used(self) -> None:
        almost_solved = (
            "53467891267219534819834256785976142342685379171392485696153728428741963534528617."
        )
        result = solve_from_string(
            almost_solved,
            techniques=[],
            allow_fallback_search=True,
        )
        self.assertEqual(result.status, SolveStatus.SOLVED)
        self.assertTrue(result.used_fallback_search)
        self.assertEqual(result.message, "Puzzle solved with fallback search.")

    def test_solve_from_string_default_mode_disables_fallback_search(self) -> None:
        almost_solved = (
            "53467891267219534819834256785976142342685379171392485696153728428741963534528617."
        )
        result = solve_from_string(
            almost_solved,
            techniques=[],
        )
        self.assertEqual(result.status, SolveStatus.STALLED)
        self.assertFalse(result.used_fallback_search)
        self.assertIn("Fallback search is disabled.", result.message)


if __name__ == "__main__":
    unittest.main()
