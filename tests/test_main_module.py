import importlib
import runpy
import unittest
from unittest.mock import patch


class MainModuleTests(unittest.TestCase):
    def test_module_can_be_imported_without_executing_main(self) -> None:
        with patch("sudoku_solver.cli.main", side_effect=AssertionError("should not run")):
            module = importlib.import_module("sudoku_solver.__main__")
        self.assertEqual(module.__name__, "sudoku_solver.__main__")

    def test_module_entrypoint_raises_system_exit_with_main_return_code(self) -> None:
        with patch("sudoku_solver.cli.main", return_value=7):
            with self.assertRaises(SystemExit) as exc:
                runpy.run_module("sudoku_solver.__main__", run_name="__main__")

        self.assertEqual(exc.exception.code, 7)


if __name__ == "__main__":
    unittest.main()
