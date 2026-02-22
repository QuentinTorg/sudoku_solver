import unittest

from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import SolveStatus


# Puzzles that are intentionally expected to stall with the current v1
# technique set. As new techniques are implemented, entries should move out
# of this list and into solved regression coverage.
CURRENTLY_UNSOLVED_PUZZLES = [
    (
        "top1465_line1",
        "4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........",
    ),
]


class RegressionPuzzleTests(unittest.TestCase):
    def test_currently_unsolved_puzzles_stall_not_invalid(self) -> None:
        for label, puzzle in CURRENTLY_UNSOLVED_PUZZLES:
            with self.subTest(puzzle=label):
                result = solve_from_string(puzzle)
                self.assertEqual(result.status, SolveStatus.STALLED)
                self.assertNotEqual(result.status, SolveStatus.INVALID)
                self.assertGreater(len(result.steps), 0)


if __name__ == "__main__":
    unittest.main()
