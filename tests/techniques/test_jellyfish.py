import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.jellyfish import apply_jellyfish


class JellyfishTechniqueTests(unittest.TestCase):
    def test_apply_jellyfish_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {1, 6},
            4: {2, 6},
            19: {3, 6},
            25: {4, 6},
            37: {5, 6},
            44: {7, 6},
            55: {8, 6},
            61: {9, 6},
            10: {6, 9},
            79: {5, 6},
        }

        step = apply_jellyfish(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "jellyfish")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(10, 6), (79, 6)])

    def test_apply_jellyfish_returns_none_when_no_pattern_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {1, 6},
            4: {2, 6},
            19: {3, 6},
            25: {4, 6},
            37: {5, 6},
            44: {7, 6},
            55: {8, 6},
            54: {8, 6},
            62: {9, 6},  # extra column breaks four-column union
            10: {6, 9},
        }

        step = apply_jellyfish(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
