"""Golden Master approval — fixed text format for int[6] and error codes."""

from __future__ import annotations

import os
from pathlib import Path

_TESTS_ROOT = Path(__file__).resolve().parent

INT6_PREFIX = "INT6"
ERR_PREFIX = "ERR"


def format_golden(actual: list[int] | dict[str, str]) -> str:
    """Serialize success int[6] or error dict to canonical golden text."""
    if isinstance(actual, dict):
        code = actual["code"]
        message = actual.get("message", "")
        return f"{ERR_PREFIX}:{code}:{message}"
    if len(actual) != 6:
        raise ValueError(f"int[6] expected, got length {len(actual)}")
    body = ",".join(str(x) for x in actual)
    return f"{INT6_PREFIX}:{body}"


def assert_matches_golden(
    actual: list[int] | dict[str, str],
    relative: str,
) -> None:
    """Compare actual to tests/golden/<relative>; update file when UPDATE_GOLDEN=1."""
    golden_path = _TESTS_ROOT / relative
    formatted = format_golden(actual)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        golden_path.parent.mkdir(parents=True, exist_ok=True)
        golden_path.write_text(formatted + "\n", encoding="utf-8")
        return

    if not golden_path.is_file():
        raise AssertionError(
            f"Golden file missing: {golden_path}. "
            f"Run with UPDATE_GOLDEN=1 to create it."
        )

    expected = golden_path.read_text(encoding="utf-8").strip()
    if formatted == expected:
        return

    raise AssertionError(
        f"Golden mismatch for {relative}\n"
        f"  expected: {expected!r}\n"
        f"  actual:   {formatted!r}"
    )
