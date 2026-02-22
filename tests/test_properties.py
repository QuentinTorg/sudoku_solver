import unittest

from sudoku_solver.grid import format_grid, parse_grid
from sudoku_solver.solver import solve_from_string
from sudoku_solver.types import SolveStatus
from sudoku_solver.units import all_units

try:
    from hypothesis import given, settings
    from hypothesis import strategies as st
except ModuleNotFoundError:  # pragma: no cover - optional local dependency
    HYPOTHESIS_AVAILABLE = False
else:
    HYPOTHESIS_AVAILABLE = True


SOLVED_GRID = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"


def _build_puzzle(blank_positions: set[int]) -> str:
    return "".join(
        "." if index in blank_positions else SOLVED_GRID[index]
        for index in range(81)
    )


if HYPOTHESIS_AVAILABLE:

    class PropertyTests(unittest.TestCase):
        @settings(max_examples=80, deadline=None)
        @given(st.sets(st.integers(min_value=0, max_value=80), max_size=25))
        def test_parse_format_round_trip_for_valid_masked_grid(
            self,
            blank_positions: set[int],
        ) -> None:
            puzzle = _build_puzzle(blank_positions)
            grid = parse_grid(puzzle)
            self.assertEqual(format_grid(grid), puzzle)

        @settings(max_examples=60, deadline=None)
        @given(st.sets(st.integers(min_value=0, max_value=80), max_size=25))
        def test_solver_never_changes_givens_for_valid_masked_grid(
            self,
            blank_positions: set[int],
        ) -> None:
            puzzle = _build_puzzle(blank_positions)
            result = solve_from_string(puzzle)
            self.assertNotEqual(result.status, SolveStatus.INVALID)

            for index, char in enumerate(puzzle):
                if char == ".":
                    continue
                self.assertEqual(result.grid_string[index], char)

            if result.status is SolveStatus.SOLVED:
                for _, unit_cells in all_units():
                    digits = {int(result.grid_string[cell]) for cell in unit_cells}
                    self.assertEqual(digits, set(range(1, 10)))

else:

    class PropertyTests(unittest.TestCase):
        @unittest.skip("hypothesis not installed")
        def test_hypothesis_dependency_missing(self) -> None:
            self.fail("hypothesis not installed")


if __name__ == "__main__":
    unittest.main()
