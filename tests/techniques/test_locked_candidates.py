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


if __name__ == "__main__":
    unittest.main()
