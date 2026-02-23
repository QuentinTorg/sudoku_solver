import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.finned_swordfish import apply_finned_swordfish


class FinnedSwordfishTechniqueTests(unittest.TestCase):
    def test_apply_finned_swordfish_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {5, 8},
            4: {1, 5},
            2: {3, 5},  # fin
            28: {2, 5},
            34: {4, 5},
            58: {6, 5},
            61: {7, 5},
            10: {5, 9},  # elimination target inside fin box
        }

        step = apply_finned_swordfish(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "finned_swordfish")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(10, 5)])

    def test_apply_finned_swordfish_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            1: {5, 8},
            4: {1, 5},
            2: {3, 5},
            28: {2, 5},
            35: {4, 5},  # shifted column breaks fish base
            58: {6, 5},
            61: {7, 5},
            10: {5, 9},
        }

        step = apply_finned_swordfish(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
