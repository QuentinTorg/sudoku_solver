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
    NAKED_QUAD = "naked_quad"
    HIDDEN_QUAD = "hidden_quad"
    XY_WING = "xy_wing"
    XYZ_WING = "xyz_wing"
    X_WING = "x_wing"
    FINNED_X_WING = "finned_x_wing"
    SWORDFISH = "swordfish"
    FINNED_SWORDFISH = "finned_swordfish"
    JELLYFISH = "jellyfish"
    EMPTY_RECTANGLE = "empty_rectangle"
    REMOTE_PAIRS = "remote_pairs"
    UNIQUE_RECTANGLE = "unique_rectangle"
    SKYSCRAPER = "skyscraper"
    TWO_STRING_KITE = "two_string_kite"
    W_WING = "w_wing"


class SolveStatus(StrEnum):
    """Overall outcome of a solve attempt."""

    SOLVED = "solved"
    STALLED = "stalled"
    INVALID = "invalid"


class DifficultyRating(StrEnum):
    """Difficulty estimate derived from techniques needed to solve."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    UNSOLVED = "unsolved"


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
    technique_counts: dict[TechniqueName, int] = field(default_factory=dict)
    difficulty: DifficultyRating = DifficultyRating.UNSOLVED
    used_fallback_search: bool = False
