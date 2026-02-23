import json
import tempfile
import unittest
from pathlib import Path

import scripts.check_benchmark_guardrail as guardrail


class BenchmarkGuardrailTests(unittest.TestCase):
    def test_main_passes_when_metrics_within_limits(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            payload = {
                "time_ms_avg": 120.0,
                "time_ms_p95": 600.0,
                "throughput_puzzles_per_second": 8.0,
            }
            path = Path(tmpdir) / "benchmark.json"
            path.write_text(f"{json.dumps(payload)}\n", encoding="utf-8")

            exit_code = guardrail.main([str(path)])
            self.assertEqual(exit_code, 0)

    def test_main_fails_when_metrics_violate_limits(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            payload = {
                "time_ms_avg": 900.0,
                "time_ms_p95": 3000.0,
                "throughput_puzzles_per_second": 1.0,
            }
            path = Path(tmpdir) / "benchmark.json"
            path.write_text(f"{json.dumps(payload)}\n", encoding="utf-8")

            exit_code = guardrail.main([str(path)])
            self.assertEqual(exit_code, 1)

    def test_main_returns_error_for_missing_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            payload = {"time_ms_avg": 120.0}
            path = Path(tmpdir) / "benchmark.json"
            path.write_text(f"{json.dumps(payload)}\n", encoding="utf-8")

            exit_code = guardrail.main([str(path)])
            self.assertEqual(exit_code, 2)


if __name__ == "__main__":
    unittest.main()
