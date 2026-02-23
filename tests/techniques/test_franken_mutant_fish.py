import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.franken_mutant_fish import apply_franken_mutant_fish


class FrankenMutantFishTechniqueTests(unittest.TestCase):
    def test_apply_franken_mutant_fish_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            3: {1, 7},
            4: {2, 7},
            12: {3, 7},
            22: {4, 7},
            57: {5, 7},
            58: {6, 7},
        }

        step = apply_franken_mutant_fish(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "franken_mutant_fish")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(57, 7), (58, 7)])

    def test_apply_franken_mutant_fish_returns_none_when_no_pattern_exists(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            3: {1, 7},
            4: {2, 7},
            12: {3, 7},
            23: {4, 7},
        }

        step = apply_franken_mutant_fish(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
