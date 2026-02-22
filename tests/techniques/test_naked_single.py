import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.naked_single import apply_naked_single
from sudoku_solver.types import TechniqueName


class NakedSingleTechniqueTests(unittest.TestCase):
    def test_apply_naked_single_returns_step_when_move_exists(self) -> None:
        grid = parse_grid("53467891267219534819834256785976142342685379171392485696153728428741963534528617.")
        candidates = {80: {9}}

        step = apply_naked_single(grid, candidates)

        self.assertIsNotNone(step)
        self.assertEqual(step.technique, TechniqueName.NAKED_SINGLE)
        assert step is not None
        self.assertEqual(step.placements, [(80, 9)])
        self.assertEqual(step.eliminations, [])
        self.assertEqual(step.affected_units, ["r9c9"])


if __name__ == "__main__":
    unittest.main()
