"""Loader for split compose modules."""
from __future__ import annotations
import pathlib
_root = pathlib.Path(__file__).resolve().parent
_chunks = ['_compose_chunk00.py', '_compose_chunk01.py', '_compose_chunk02.py', '_compose_chunk03.py', '_compose_chunk04.py']
_code = "".join((_root / name).read_text(encoding="utf-8") for name in _chunks)
exec(compile(_code, "tools/compose.py", "exec"), globals())
