import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import scripts.benchmark as benchmark
from sudoku_solver.types import SolveStatus


class _DummyResult:
    def __init__(self, status: SolveStatus) -> None:
        self.status = status


class BenchmarkScriptTests(unittest.TestCase):
    def test_main_writes_json_csv_and_technique_profile(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            puzzle_file = tmp_path / "puzzles.txt"
            puzzle_file.write_text(f"{'.' * 81}\n{'1' * 81}\n", encoding="utf-8")
            json_file = tmp_path / "benchmark.json"
            csv_file = tmp_path / "benchmark.csv"

            statuses = [SolveStatus.SOLVED, SolveStatus.STALLED]
            index = 0

            def _fake_solve_from_string(puzzle: str, **kwargs: object) -> _DummyResult:
                nonlocal index
                hook = kwargs.get("technique_attempt_hook")
                if callable(hook):
                    hook("naked_single", 0.001, False)
                    hook("hidden_single", 0.002, True)
                result = _DummyResult(statuses[index])
                index += 1
                return result

            stdout = io.StringIO()
            with patch("scripts.benchmark.solve_from_string", side_effect=_fake_solve_from_string):
                with redirect_stdout(stdout):
                    exit_code = benchmark.main(
                        [
                            str(puzzle_file),
                            "--progress-every",
                            "0",
                            "--top-slowest",
                            "0",
                            "--profile-techniques",
                            "--top-techniques",
                            "5",
                            "--output-json",
                            str(json_file),
                            "--output-csv",
                            str(csv_file),
                        ]
                    )

            self.assertEqual(exit_code, 0)
            self.assertIn("technique_profile:", stdout.getvalue())
            self.assertTrue(json_file.exists())
            self.assertTrue(csv_file.exists())

            payload = json.loads(json_file.read_text(encoding="utf-8"))
            self.assertEqual(payload["processed"], 2)
            self.assertEqual(payload["solved"], 1)
            self.assertEqual(payload["stalled"], 1)
            self.assertEqual(payload["invalid"], 0)
            technique_names = [entry["name"] for entry in payload["techniques"]]
            self.assertIn("naked_single", technique_names)
            self.assertIn("hidden_single", technique_names)

            csv_rows = csv_file.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(csv_rows[0], "line_number,status,elapsed_seconds")
            self.assertEqual(len(csv_rows), 3)

    def test_main_rejects_negative_top_techniques(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            puzzle_file = Path(tmpdir) / "puzzles.txt"
            puzzle_file.write_text(f"{'.' * 81}\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                benchmark.main([str(puzzle_file), "--top-techniques", "-1"])


if __name__ == "__main__":
    unittest.main()
