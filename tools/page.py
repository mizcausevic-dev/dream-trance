"""Loader for split page module."""
from __future__ import annotations
import pathlib
_root = pathlib.Path(__file__).resolve().parent
_code = "".join((_root / name).read_text(encoding="utf-8") for name in ['_page_chunk00.py', '_page_chunk01.py', '_page_chunk02.py', '_page_chunk03.py'])
exec(compile(_code, "tools/page.py", "exec"), globals())
