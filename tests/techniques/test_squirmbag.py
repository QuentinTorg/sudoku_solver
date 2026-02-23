import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.squirmbag import apply_squirmbag


class SquirmbagTechniqueTests(unittest.TestCase):
    def test_apply_squirmbag_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates: dict[int, set[int]] = {}
        for row in range(5):
            for col in range(5):
                candidates[row * 9 + col] = {7}
        candidates[45] = {7, 9}

        step = apply_squirmbag(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "squirmbag")
        self.assertEqual(step.eliminations, [(45, 7)])

    def test_apply_squirmbag_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates: dict[int, set[int]] = {}
        for row in range(4):
            for col in range(5):
                candidates[row * 9 + col] = {7}
        candidates[45] = {7, 9}

        step = apply_squirmbag(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
