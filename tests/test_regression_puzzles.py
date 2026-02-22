import unittest

from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import SolveStatus

# Puzzles that should solve with the current enabled technique set.
REGRESSION_SOLVED_PUZZLES = [
    (
        "top1465_line1",
        "4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........",
    ),
]


class RegressionPuzzleTests(unittest.TestCase):
    def test_regression_puzzles_are_solved(self) -> None:
        for label, puzzle in REGRESSION_SOLVED_PUZZLES:
            with self.subTest(puzzle=label):
                result = solve_from_string(puzzle)
                self.assertEqual(result.status, SolveStatus.SOLVED)


if __name__ == "__main__":
    unittest.main()
