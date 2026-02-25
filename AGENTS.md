# AGENTS.md

Guidance for future coding agents working in this repository.

## Project Context

- Repository: `sudoku_solver`
- Goal: explainable Sudoku solver with human-style techniques as the default mode.
- Priority: correctness, deterministic behavior, documentation quality, and measurable performance.

## User Workflow Preferences

- Work incrementally.
- If asked to do multiple items, complete them one-by-one.
- Validate each item before moving to the next.
- Make independent commits for logical groups of changes.
- If blocked, stop and clearly report the blocker and current state.

## Commit and Validation Requirements

Before each commit (or each logical phase), run relevant checks:

- `ruff format --check .` (or changed files)
- `ruff check .` (or changed files)
- `mypy sudoku_solver scripts`
- `python -m unittest discover -s tests -t .`
- Coverage when tests change significantly:
  - `python -m coverage run --branch --source=sudoku_solver -m unittest discover -s tests -t .`
  - `python -m coverage report -m`

Current CI coverage gate target is **97%**.

## Testing Preferences

- Add/expand unit tests for every new technique and every bug fix.
- Prefer direct regression tests that reproduce the exact bug condition.
- If adding technique skeletons, ensure tests are meaningful and not silently passing without behavior checks.
- Keep regression tests aligned with current behavior (human-only by default, no fallback in dataset regressions).

## Technique and Solver Preferences

- Human-only solving is the default behavior.
- Fallback search is optional and should remain explicitly opt-in.
- Keep technique execution deterministic.
- Preserve/extend the cost-aware scheduler (primary/deferred/ultra-expensive) to control runtime.
- When adding advanced rules, prefer conservative/validity-safe eliminations.

## Benchmarking and Performance Expectations

When technique behavior changes:

- Benchmark before/after and report deltas.
- Use smaller datasets (`puzzles/top87.txt`, `puzzles/top95.txt`) during iteration.
- Use `puzzles/top1465.txt` for larger validation when requested.
- Report at minimum:
  - solved/stalled/invalid counts
  - elapsed total
  - average/median/p95 time
- Include per-technique profiler output when relevant (`scripts/benchmark.py --profile-techniques`).

## Documentation Preferences

- Keep root `README.md` concise and project-oriented.
- Keep detailed technique explanations in `sudoku_solver/techniques/README.md`.
- `sudoku_solver/techniques/README.md` should include:
  - a technique index table (family/tier/status/expected cost)
  - full-grid illustrative tables for each technique
  - notes for sub-implementations where applicable
- Update docs whenever behavior, CLI, CI, or technique coverage changes.

## CI Preferences

- CI should run lint, format check, type checks, tests, and coverage gate.
- Dataset workflow should run human-only regressions (no fallback flag).
- Keep benchmark artifacts machine-readable (`.json`, `.csv`) and text summary.
- Maintain benchmark guardrail checks in dataset CI.

## Repository Hygiene

- Do not commit generated artifacts or caches.
- Ensure `.gitignore` continues to cover common outputs (`__pycache__`, `*.pyc`, `.coverage*`, `.hypothesis`, `.mypy_cache`, `.ruff_cache`, `build`, `dist`, `*.egg-info`, `*.cover`, `htmlcov`).
- Clean local artifacts when they accumulate.

## Environment Notes

- Use the repo virtual environment when present (`venv/` or `.venv/`).
- For benchmark/tooling commands, ensure local workspace code is used (benchmark script is pinned to workspace import path).

## Communication Preferences

- Be direct and technical.
- Include concrete numbers for benchmarks and validation.
- Use concise progress updates during long-running tasks.
