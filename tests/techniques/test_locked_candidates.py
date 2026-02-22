import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.locked_candidates import apply_locked_candidates
from sudoku_solver.types import TechniqueName


class LockedCandidatesTechniqueTests(unittest.TestCase):
    def test_apply_locked_candidates_returns_step_when_elimination_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 5},
            1: {2, 5},
            2: {1, 2},
            3: {5, 6},
            4: {5, 7},
            5: {6, 7},
            9: {1, 2},
            10: {1, 2},
            11: {1, 2},
        }

        step = apply_locked_candidates(grid, candidates)

        self.assertIsNotNone(step)
        self.assertEqual(step.technique, TechniqueName.LOCKED_CANDIDATES)
        assert step is not None
        self.assertEqual(step.eliminations, [(3, 5), (4, 5)])
        self.assertEqual(step.affected_units, ["box1", "row1"])

    def test_apply_locked_candidates_returns_none_for_no_pattern(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},
            2: {3, 4},
            10: {1, 4},
        }
        step = apply_locked_candidates(grid, candidates)
        self.assertIsNone(step)

    def test_apply_locked_candidates_returns_step_for_column_claiming(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {7, 8},
            9: {3, 7},
            19: {4, 7},
            30: {1, 2},
        }

        step = apply_locked_candidates(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique, TechniqueName.LOCKED_CANDIDATES)
        self.assertEqual(step.eliminations, [(19, 7)])
        self.assertEqual(step.affected_units, ["col1", "box1"])


if __name__ == "__main__":
    unittest.main()
