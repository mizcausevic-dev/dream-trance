"""Loader for split compose modules (build-time only)."""
from __future__ import annotations
import pathlib
_root = pathlib.Path(__file__).resolve().parent
_code = "".join((_root / name).read_text(encoding="utf-8") for name in (
    "_compose_part0.py",
    "_compose_part1.py",
    "_compose_part2.py",
))
exec(compile(_code, "tools/compose.py", "exec"), globals())
