"""
Pytest root configuration.

Pytest chokes on a few Windows-specific entries (like the `nul` device) and
broken links inside `node_modules`. We defensively skip anything that is not a
real file or directory before collection.
"""

import os
from pathlib import Path

import _pytest.main as _pytest_main


_IGNORE_PATTERNS = {"nul", "node_modules", ".bin", "build", "dist", "venv", ".git"}
_original_collectfile = _pytest_main.Session._collectfile


def _safe_collectfile(self, fspath: Path, handle_dupes: bool = True):
    """Skip entries that are neither files nor directories (e.g., `nul`)."""
    if not (fspath.is_file() or fspath.is_dir()):
        return ()
    return _original_collectfile(self, fspath, handle_dupes)


def pytest_configure(config):  # noqa: D401
    """Apply the safe collector before tests start."""
    _pytest_main.Session._collectfile = _safe_collectfile


def pytest_ignore_collect(path, config):  # noqa: D401
    """
    Skip problematic or irrelevant paths.

    - `nul` is a Windows device that appears in listings.
    - `node_modules` and build directories can hold broken links/executables
      that are not Python tests.
    """
    name = path.basename.lower()
    if name in _IGNORE_PATTERNS:
        return True

    path_str = str(path).lower()
    return any(part in path_str for part in ("\\node_modules\\", "/node_modules/"))
