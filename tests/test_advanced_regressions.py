import unittest

from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import SolveStatus

ALL_TECHNIQUES = [
    "naked_single",
    "hidden_single",
    "locked_candidates",
    "naked_pair",
    "hidden_pair",
    "naked_triple",
    "hidden_triple",
    "naked_quad",
    "hidden_quad",
    "xy_wing",
    "xyz_wing",
    "x_wing",
    "w_wing",
    "swordfish",
    "jellyfish",
    "finned_x_wing",
    "finned_swordfish",
    "empty_rectangle",
    "remote_pairs",
    "two_string_kite",
    "skyscraper",
    "unique_rectangle",
]

# Dataset-derived cases that previously reached invalid states with advanced techniques.
INVALID_REGRESSION_PUZZLES = [
    "4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........",
    ".4..1.2.......9.7..1..........43.6..8......5....2.....7.5..8......6..3..9........",
    ".26.39......6....19.....7.......4..9.5....2....85.....3..2..9..4....762.........4",
    "....75....1..2.....4...3...5.....3.2...8...1.......6.....1..48.2........7........",
    "...658.....4......12............96.7...3..5....2.8...3..19..8..3.6.....4....473..",
]


class AdvancedTechniqueRegressionTests(unittest.TestCase):
    def test_invalid_regression_puzzles_do_not_become_invalid(self) -> None:
        for puzzle in INVALID_REGRESSION_PUZZLES:
            with self.subTest(puzzle=puzzle):
                result = solve_from_string(
                    puzzle,
                    techniques=ALL_TECHNIQUES,
                    allow_fallback_search=False,
                )
                self.assertNotEqual(result.status, SolveStatus.INVALID)


if __name__ == "__main__":
    unittest.main()
