import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.locked_candidates import apply_locked_candidates
from sudoku_solver.types import TechniqueName


class LockedCandidatesTechniqueTests(unittest.TestCase):
    def test_apply_locked_candidates_returns_step_when_elimination_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {idx: {1, 2, 3} for idx in range(81)}

        step = apply_locked_candidates(grid, candidates)

        self.assertIsNotNone(step)
        self.assertEqual(step.technique, TechniqueName.LOCKED_CANDIDATES)


if __name__ == "__main__":
    unittest.main()
