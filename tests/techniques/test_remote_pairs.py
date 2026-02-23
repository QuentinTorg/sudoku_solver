import unittest

from sudoku_solver.grid import parse_grid
from sudoku_solver.techniques.remote_pairs import apply_remote_pairs


class RemotePairsTechniqueTests(unittest.TestCase):
    def test_apply_remote_pairs_returns_expected_eliminations(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 9},
            13: {1, 9},
            40: {1, 9},
            39: {1, 9},
            31: {1, 3, 9},
        }

        step = apply_remote_pairs(grid, candidates)

        self.assertIsNotNone(step)
        assert step is not None
        self.assertEqual(step.technique.value, "remote_pairs")
        self.assertEqual(step.placements, [])
        self.assertEqual(step.eliminations, [(31, 1), (31, 9)])

    def test_apply_remote_pairs_returns_none_when_pattern_absent(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            10: {1, 9},
            40: {1, 9},
            67: {1, 9},
            11: {1, 3, 9},
        }

        step = apply_remote_pairs(grid, candidates)
        self.assertIsNone(step)

    def test_apply_remote_pairs_skips_non_bipartite_components(self) -> None:
        grid = parse_grid("." * 81)
        candidates = {
            0: {1, 9},
            1: {1, 9},
            9: {1, 9},
            80: {1, 9},
            10: {1, 9, 3},
        }
        step = apply_remote_pairs(grid, candidates)
        self.assertIsNone(step)


if __name__ == "__main__":
    unittest.main()
