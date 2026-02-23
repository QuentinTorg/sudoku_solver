import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.sue_de_coq import apply_sue_de_coq


class SueDeCoqTechniqueTests(unittest.TestCase):
    def test_apply_sue_de_coq_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {3, 4},  # intersection (row 1, box 1) => digits {1,2,3,4}
            3: {1},
            4: {2},  # row subset covers {1,2}
            5: {1, 5},
            6: {2, 6},  # row eliminations
            9: {3},
            10: {4},  # box subset covers {3,4}
            11: {3, 7},
            18: {4, 8},  # box eliminations
        }

        step = apply_sue_de_coq(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "sue_de_coq")
        self.assertEqual(step.placements, [])
        self.assertEqual(
            step.eliminations,
            [(5, 1), (6, 2), (11, 3), (18, 4)],
        )

    def test_apply_sue_de_coq_returns_none_when_intersection_not_qualified(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 2},
            1: {2, 3},  # intersection union has 3 digits, not 4
            3: {1},
            4: {2},
            9: {3},
            10: {4},
            11: {3, 7},
            18: {4, 8},
        }

        step = apply_sue_de_coq(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
