import unittest

from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import SolveStatus


class SolverTests(unittest.TestCase):
    def test_solve_from_string_returns_solved_for_completed_grid(self) -> None:
        solved = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
        result = solve_from_string(solved)
        self.assertEqual(result.status, SolveStatus.SOLVED)
        self.assertEqual(result.grid_string, solved)
        self.assertEqual(result.steps, [])

    def test_solve_from_string_marks_stalled_when_no_v1_move_exists(self) -> None:
        hard = ".....6....59.....82....8....45........3........6..3.54...325..6.................."
        result = solve_from_string(hard)
        self.assertEqual(result.status, SolveStatus.STALLED)
        self.assertTrue(result.steps)


if __name__ == "__main__":
    unittest.main()
