"""Core types used across the solver package."""

from dataclasses import dataclass, field
from enum import StrEnum


class TechniqueName(StrEnum):
    """Enumeration of supported human-solving techniques."""

    NAKED_SINGLE = "naked_single"
    HIDDEN_SINGLE = "hidden_single"
    LOCKED_CANDIDATES = "locked_candidates"
    NAKED_PAIR = "naked_pair"
    HIDDEN_PAIR = "hidden_pair"
    NAKED_TRIPLE = "naked_triple"
    HIDDEN_TRIPLE = "hidden_triple"
    XYZ_WING = "xyz_wing"


class SolveStatus(StrEnum):
    """Overall outcome of a solve attempt."""

    SOLVED = "solved"
    STALLED = "stalled"
    INVALID = "invalid"


@dataclass(slots=True)
class Grid:
    """In-memory representation of a Sudoku grid."""

    cells: tuple[int, ...]


@dataclass(slots=True)
class Step:
    """Single explainable solving step."""

    technique: TechniqueName
    placements: list[tuple[int, int]] = field(default_factory=list)
    eliminations: list[tuple[int, int]] = field(default_factory=list)
    affected_units: list[str] = field(default_factory=list)
    rationale: str = ""
    grid_snapshot_after: str = ""


@dataclass(slots=True)
class SolveResult:
    """Result object returned by solve operations."""

    status: SolveStatus
    grid: Grid
    grid_string: str
    steps: list[Step] = field(default_factory=list)
    message: str = ""
