# sudoku_solver

[![CI](https://img.shields.io/github/actions/workflow/status/QuentinTorg/sudoku_solver/ci.yml?branch=main&label=ci)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/ci.yml)
[![Dataset Regression](https://img.shields.io/github/actions/workflow/status/QuentinTorg/sudoku_solver/dataset.yml?branch=main&label=dataset)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/dataset.yml)
[![Coverage Gate](https://img.shields.io/badge/coverage-%E2%89%A597%25-brightgreen)](https://github.com/QuentinTorg/sudoku_solver/actions/workflows/ci.yml)

Explainable Sudoku solver in Python with human-style techniques, step-by-step reasoning, CLI and library APIs, benchmarking tools, and CI quality gates.

## What This Project Does

- Solves 9x9 Sudoku puzzles from a single puzzle string or a puzzle file.
- Applies a deterministic sequence of human-style techniques and records each applied step.
- Can optionally use a bounded uniqueness search after human techniques stall.
- Reports structured outcomes (`solved`, `stalled`, `invalid`), difficulty rating, and optional telemetry.
- Includes unit tests, property tests (when `hypothesis` is installed), linting, typing checks, and coverage reporting.

## Feature Summary

- Techniques implemented:
  1. Naked Single
  2. Hidden Single
  3. Locked Candidates (pointing/claiming)
  4. Naked Pair
  5. Hidden Pair
  6. Naked Triple
  7. Hidden Triple
  8. XY-Wing
  9. XYZ-Wing
  10. X-Wing
  11. Naked Quad
  12. Hidden Quad
  13. W-Wing
  14. Swordfish
  15. Jellyfish
  16. Simple Coloring
  17. 3D Medusa (expanded)
  18. AIC (expanded)
  19. X-Cycles
  20. XY-Chain
  21. ALS-XZ (expanded)
  22. Sue de Coq (restricted)
  23. BUG+1
  24. Finned X-Wing / Sashimi X-Wing
  25. Finned Swordfish
  26. Empty Rectangle
  27. Remote Pairs
  28. Two-String Kite
  29. Skyscraper
  30. Unique Rectangle
  31. Grouped AIC (expanded)
  32. Nice Loops (expanded)
  33. ALS Chains (expanded)
  34. Death Blossom (restricted)
  35. Uniqueness Expansions (restricted)
  36. Fireworks (restricted)
  37. WXYZ-Wing (expanded)
  38. Exocet (restricted)
  39. Sue de Coq Full/Generalized (restricted)
  40. Kraken Fish (expanded)
  41. Sashimi Fish (expanded)
  42. Forcing Chains (expanded)
  43. Forcing Nets (expanded)
  44. Franken/Mutant Fish (expanded)
  45. Squirmbag
  See [Technique Reference](sudoku_solver/techniques/README.md) for detailed explanations and full-grid pattern tables.
- Default technique set:
  All implemented human techniques run by default.
  Runtime is controlled by the three-pass scheduler (primary, deferred, and
  ultra-expensive groups), so expensive techniques are not run first on every
  iteration.
  API `techniques=[...]` is still available when you want a custom subset or
  custom order.
- Advanced-technique safety:
  High-risk eliminations are conservatively validated against solution
  existence checks before they are applied, reducing false-positive
  eliminations that can otherwise produce invalid states.
- Fallback search:
  Uniqueness-aware backtracking is available when no configured technique can advance the grid.
  It is disabled by default; use `allow_fallback_search=True` (API) or
  `--allow-fallback-search` (CLI) to enable it.
- Result metadata:
  `steps`, `technique_counts`, `difficulty`, and `used_fallback_search` are returned for every solve attempt.

## Sudoku Terms (Quick Glossary)

- `Cell`: one square in the 9x9 grid.
- `Row`: horizontal set of 9 cells.
- `Column`: vertical set of 9 cells.
- `Box`: one 3x3 subgrid.
- `Unit`: any row, column, or box.
- `Candidate`: a digit that is still legal for an empty cell.
- `Peer`: a cell sharing a row, column, or box with another cell.
- `Placement`: writing a final digit into a cell.
- `Elimination`: removing a candidate from a cell.

## Technique Reference

Detailed explanations, full-grid pattern tables, and implementation notes for
every technique are in:

- [Technique Reference](sudoku_solver/techniques/README.md)

The list above remains the authoritative set of selectable technique keys. The
solver still runs them in a deterministic order by default.

## Result Model

`solve_from_string()` returns a `SolveResult` with:

- `status`: `solved`, `stalled`, or `invalid`
- `grid_string`: final grid string
- `steps`: ordered list of applied steps
- `technique_counts`: count per technique used
- `difficulty`: `easy`, `medium`, `hard`, `expert`, or `unsolved`
- `used_fallback_search`: `true` if non-human fallback search was used to finish
- `message`: contextual message

Difficulty is derived from the hardest technique used (or fallback search usage).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Install developer tooling:

```bash
pip install -e .[dev]
```

## Running

### Python API

```python
from sudoku_solver import solve_from_string

puzzle = "53..7....6..195....98....6.8...6...34..8..6...2...1.6....28....419..5....8..79"
result = solve_from_string(puzzle)
fallback_result = solve_from_string(puzzle, allow_fallback_search=True)
custom_techniques_result = solve_from_string(
    puzzle,
    techniques=[
        "naked_single",
        "hidden_single",
        "locked_candidates",
        "naked_pair",
        "hidden_pair",
    ],
)

print(result.status)
print(result.difficulty)
print(result.used_fallback_search)
print(result.grid_string)
print(result.technique_counts)
```

### CLI

Single puzzle:

```bash
python -m sudoku_solver "<81-char-puzzle>"
python -m sudoku_solver "<81-char-puzzle>" --show-steps
python -m sudoku_solver "<81-char-puzzle>" --show-telemetry
python -m sudoku_solver "<81-char-puzzle>" --allow-fallback-search
python -m sudoku_solver "<81-char-puzzle>" --max-steps 200
```

Puzzle file mode:

```bash
python -m sudoku_solver --puzzle-file puzzles/top1465.txt
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --max-failures 2
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --allow-fallback-search
python -m sudoku_solver --puzzle-file puzzles/top1465.txt --show-steps --show-telemetry
```

Note:
CLI uses the full default human-technique set. Custom technique subsets/orders
are configured through the Python API (`techniques=[...]`).

### Benchmark Harness

```bash
python scripts/benchmark.py puzzles/top1465.txt
python scripts/benchmark.py puzzles/top1465.txt --allow-fallback-search
python scripts/benchmark.py puzzles/top1465.txt --limit 200 --top-slowest 10 --progress-every 500
python scripts/benchmark.py puzzles/top1465.txt --profile-techniques --top-techniques 20
python scripts/benchmark.py puzzles/top1465.txt --output-json benchmark.json --output-csv benchmark.csv
python scripts/check_benchmark_guardrail.py benchmark.json --max-avg-ms 700 --max-p95-ms 2500 --min-throughput 2.5
```

Note:
`scripts/benchmark.py` pins import resolution to the local workspace root, so
it benchmarks the checked-out solver code without requiring `PYTHONPATH=.`.

## Input Format

- Exactly 81 characters.
- `1-9` for filled cells.
- `.` or `0` for empty cells.

## Repository Structure

- `sudoku_solver/grid.py`: parsing, formatting, and givens validation.
- `sudoku_solver/candidates.py`: candidate generation for empty cells.
- `sudoku_solver/units.py`: row/column/box helpers and peer calculation.
- `sudoku_solver/engines/`: shared family engines that reduce duplicated scans.
- `sudoku_solver/engines/chain_engine.py`: shared chain graph helpers (AIC/coloring/XY-chain support).
- `sudoku_solver/engines/fish_engine.py`: shared fish scanners (X-Wing/Swordfish/Jellyfish/finned families).
- `sudoku_solver/engines/als_engine.py`: shared ALS and petal-structure scans (ALS-XZ/ALS-Chains/Death Blossom).
- `sudoku_solver/engines/uniqueness_engine.py`: shared rectangle/pair scans for uniqueness-family rules.
- `sudoku_solver/techniques/`: individual technique implementations.
- [`sudoku_solver/techniques/README.md`](sudoku_solver/techniques/README.md): detailed technique explanations and full-grid pattern illustrations.
- `sudoku_solver/solver.py`: orchestration loop, step application, optional fallback search, difficulty classification.
- `sudoku_solver/cli.py`: CLI parser, single/file runners, progress and reporting output.
- `sudoku_solver/types.py`: core dataclasses/enums (`Grid`, `Step`, `SolveResult`, etc.).
- `scripts/benchmark.py`: dataset timing and throughput reporting.
- `tests/`: unit, internal, regression, technique, and property tests.
- `puzzles/`: bundled puzzle corpora.

## Code Data Flow

1. Parse input (`parse_grid`) and validate puzzle consistency.
2. Build candidate sets for empty cells (`get_candidates`).
3. Iterate technique adapters in fixed order and request one `Step` at a time.
4. Technique adapters may delegate scanning to shared family engines.
5. Apply step placements/eliminations (`_apply_step`) and update state.
6. Repeat until solved or no technique can progress.
7. If stalled by techniques and fallback is enabled, run uniqueness-aware fallback search.
8. Return `SolveResult` with final status, steps, telemetry, difficulty, and fallback usage flag.

## Quality Checks

### Pre-commit hooks

```bash
pre-commit install
pre-commit install --hook-type pre-push
pre-commit run --all-files
```

### Local checks

```bash
source venv/bin/activate
ruff format --check .
ruff check .
mypy
python -m unittest discover -s tests -t . -v
python -m coverage run --branch --source=sudoku_solver -m unittest discover -s tests -t .
python -m coverage report -m
```

### Unit tests and coverage (quick run)

```bash
source venv/bin/activate
python -m unittest discover -s tests -t . -v
```

```bash
source venv/bin/activate
python -m coverage erase
python -m coverage run --branch --source=sudoku_solver -m unittest discover -s tests -t .
python -m coverage report -m
python -m coverage html
```

Notes:

- Terminal summary is printed by `coverage report -m`.
- HTML report is written to `htmlcov/index.html`.
- CI enforces a minimum package coverage gate of 97%.

## CI

- `CI` workflow (`.github/workflows/ci.yml`) runs on pull requests and pushes to `main`:
  - Ruff format check
  - Ruff lint
  - Mypy type checking
  - Unit tests
  - Branch coverage gate (minimum 97%)
- `Dataset Regression` workflow (`.github/workflows/dataset.yml`) runs on pushes to `main` and manual dispatch:
  - Dataset regression on `puzzles/top95.txt` and `puzzles/top1465.txt`
  - Benchmark artifact generation (`.txt`, `.json`, `.csv`)
  - Benchmark performance guardrail checks on average latency, p95 latency, and throughput

## Future Work / Roadmap

1. [x] Add a CI performance guardrail that checks benchmark metrics against configured thresholds.
2. [x] Add a technique cost profiler report (call count, hit count, total/runtime averages) during benchmark runs.
3. [x] Make benchmark execution path usage explicit so local runs always target workspace code.
4. [x] Add machine-readable benchmark outputs (JSON/CSV) for run-to-run comparisons and automation.
5. Clean up legacy/noise artifacts in the repo (for example stray coverage byproducts).
6. Add a technique index table in `sudoku_solver/techniques/README.md` (family, complexity tier, status, expected cost).
7. Continue clarifying fallback-search docs and examples as optional/non-default behavior.
8. Add more property/invariant tests to harden solver correctness guarantees.

## Contributing

1. Create a branch for your change.
2. Install dev dependencies: `pip install -e .[dev]`.
3. Enable hooks: `pre-commit install` and `pre-commit install --hook-type pre-push`.
4. Add or update tests with any code changes.
5. Run local checks before opening a PR.
6. Open a PR with a clear description of behavior changes and test evidence.

Recommended contribution pattern:

- Keep technique changes isolated per PR when possible.
- Include at least one regression test for each bug fix.
- If adding a technique, document it in [`sudoku_solver/techniques/README.md`](sudoku_solver/techniques/README.md) and add focused tests under `tests/techniques/`.
