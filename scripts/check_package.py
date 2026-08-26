"""Verify that the wheel contains typed source and static shell but no tests or fixtures."""

from __future__ import annotations

import zipfile
from pathlib import Path


def main() -> int:
    wheels = sorted(Path("dist").glob("cyrisk_console-0.1.0-*.whl"))
    if len(wheels) != 1:
        raise SystemExit("expected exactly one cyrisk_console v0.1.0 wheel")
    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
    required = {
        "cyrisk_console/__init__.py",
        "cyrisk_console/app.py",
        "cyrisk_console/auth.py",
        "cyrisk_console/static/index.html",
        "cyrisk_console/py.typed",
    }
    missing = required - names
    if missing:
        raise SystemExit(f"wheel missing required content: {sorted(missing)}")
    forbidden = {
        name for name in names if name.startswith("fixtures/") or name.startswith("tests/")
    }
    if forbidden:
        raise SystemExit(f"wheel contains forbidden content: {sorted(forbidden)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
