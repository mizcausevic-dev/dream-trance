"""Catalog page. Kit lanes are measured from the fetched MIDI files."""

from __future__ import annotations

import json
from pathlib import Path

from tools.article import TAG_LINE, TITLE
from tools.screening import pack_frames, render_media
from tools.statements import AUDITION, ON_PICTURE, PREVIEW_LINE, PROGRAM, PUBLICATION, WARNING


def write_page(path: Path, catalog: dict, report: dict, preview: dict, film: dict) -> None:
    path.write_text(render_page(catalog, report, preview, film), encoding="utf-8")
    root = path.parent
    path.with_name("media.html").write_text(render_media({
        "pack_name": catalog["pack_name"],
        "subject": (
            "The still is five horizontal lanes on a midnight field. "
            "Long pale bars are the pad. A bright lane is the lead. Mid bars are the keys. "
            "Short ticks are the drums."
        ),
        "colors": {
            "bg": "#081020",
            "paper": "#e8f0fa",
            "ink": "#102030",
            "accent": "#9ec4e8",
            "muted": "#6a8499",
        },
        "frames": pack_frames(root),
        "preview_seconds": preview["seconds_encoded"],
        "film_seconds": film["duration_seconds"],
    }), encoding="utf-8")
