import unittest

from sudoku_solver.engines.fish_engine import (
    find_finned_swordfish_elimination,
    find_finned_x_wing_elimination,
    find_franken_mutant_fish_elimination,
    find_standard_fish_elimination,
)


class FishEngineTests(unittest.TestCase):
    def test_find_standard_fish_elimination_for_x_wing(self) -> None:
        candidates = {
            10: {1, 7},
            16: {2, 7},
            46: {3, 7},
            52: {4, 7},
            28: {7, 9},
            79: {5, 7},
        }

        fish = find_standard_fish_elimination(
            candidates,
            7,
            size=2,
            exact_line_size=True,
        )

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.eliminations, ((28, 7), (79, 7)))

    def test_find_finned_x_wing_elimination(self) -> None:
        candidates = {
            10: {1, 4},
            13: {2, 4},
            11: {3, 4},
            37: {5, 4},
            40: {6, 4},
            19: {4, 9},
        }

        fish = find_finned_x_wing_elimination(candidates, 4)

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.eliminations, ((19, 4),))

    def test_find_finned_swordfish_elimination(self) -> None:
        candidates = {
            1: {5, 8},
            4: {1, 5},
            2: {3, 5},
            28: {2, 5},
            34: {4, 5},
            58: {6, 5},
            61: {7, 5},
            10: {5, 9},
        }

        fish = find_finned_swordfish_elimination(candidates, 5)

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.eliminations, ((10, 5),))

    def test_find_franken_mutant_fish_elimination(self) -> None:
        candidates = {
            3: {1, 7},
            4: {2, 7},
            12: {3, 7},
            22: {4, 7},
            57: {5, 7},
            58: {6, 7},
        }

        fish = find_franken_mutant_fish_elimination(candidates, 7)

        self.assertIsNotNone(fish)
        assert fish is not None
        self.assertEqual(fish.eliminations, ((57, 7), (58, 7)))


if __name__ == "__main__":
    unittest.main()
