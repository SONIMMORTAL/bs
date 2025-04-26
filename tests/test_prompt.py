# tests/test_prompt.py
import pathlib
import sys

# Ensure the repo root (one level up) is on sys.path
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from main import build_prompt  # noqa: E402  (import after sys.path tweak)


class Dummy:
    """Minimal stand-in for argparse.Namespace."""
    pass


def test_event() -> None:
    d = Dummy()
    d.event = "Gala"
    d.date = "2025-05-30"
    d.tone = "upbeat"

    assert "Gala" in build_prompt(d)
