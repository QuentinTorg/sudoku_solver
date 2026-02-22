import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.two_string_kite import apply_two_string_kite


class TwoStringKiteTechniqueTests(unittest.TestCase):
    def test_apply_two_string_kite_returns_expected_elimination(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 5},
            16: {2, 5},
            61: {3, 5},
            55: {5, 9},
        }

        step = apply_two_string_kite(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "two_string_kite")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(55, 5)])

    def test_apply_two_string_kite_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 5},
            16: {2, 5},
            62: {3, 5},  # shifted column endpoint breaks chain
            55: {5, 9},
        }

        step = apply_two_string_kite(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
