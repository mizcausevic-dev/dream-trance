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


def render_page(catalog: dict, report: dict, preview: dict, film: dict) -> str:
    part_rows = []
    for part in catalog["parts"]:
        part_rows.append(
            "<tr>"
            f"<td><a href=\"{part['path']}\">{part['id']}</a></td>"
            f"<td>{part['role']}</td>"
            f"<td>{part['variation']}</td>"
            f"<td>core</td>"
            f"<td>{part['bpm']}</td>"
            f"<td>{part['container_bars']}</td>"
            f"<td>{part['notes']}</td>"
            "</tr>"
        )
    arrangement_rows = []
    for item in catalog["arrangements"]:
        arrangement_rows.append(
            "<tr>"
            f"<td><a href=\"{item['path']}\">{item['kit_id']}</a></td>"
            f"<td>{item['bpm']}</td>"
            f"<td>{item['container_bars']}</td>"
            f"<td>{item['description']}</td>"
            "</tr>"
        )
    kit_items = []
    for kit in catalog["kits"]:
        kit_items.append(
            f"<li><strong>{kit['id']} {kit['title']}</strong>, {kit['bpm']} BPM, {kit['collection_name']}, "
            f"tonic {kit['tonal_reference']}. Parts are {kit['part_bars']} bars. "
            f"The arrangement is {kit['arrangement_bars']} bars. {kit['identity']} "
            f"Limitations: {kit['limitations']}</li>"
        )
    payload = {
        "kits": [
            {
                "id": kit["id"],
                "title": kit["title"],
                "bpm": kit["bpm"],
                "bars": kit["part_bars"],
                "arrangement_bars": kit["arrangement_bars"],
                "collection": kit["collection_name"],
                "tonic": kit["tonal_reference"],
                "identity": kit["identity"],
                "limitations": kit["limitations"],
                "harmonic_rhythm": kit["harmonic_rhythm"],
                "phrases": kit["phrases"],
                "arrangement_phrases": kit["arrangement_phrases"],
                "changes": kit["changes"],
                "change_bars": kit["change_bars"],
                "tempo_us": kit["tempo_us"],
                "spell": kit["spell"],
                "departures": kit["departures"],
            }
            for kit in catalog["kits"]
        ],
        "parts": [
            {
                "id": part["id"],
                "kit_id": part["kit_id"],
                "role": part["role"],
                "variation": part["variation"],
                "path": part["path"],
            }
            for part in catalog["parts"]
        ],
        "arrangements": [
            {
                "kit_id": item["kit_id"],
                "path": item["path"],
                "bpm": item["bpm"],
                "bars": item["container_bars"],
            }
            for item in catalog["arrangements"]
        ],
        "roles": [
            {"id": "pad", "label": "Pad"},
            {"id": "lead", "label": "Lead"},
            {"id": "keys", "label": "Keys"},
            {"id": "bass", "label": "Bass"},
            {"id": "drums", "label": "Drums"},
        ],
    }
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    seconds = f"{preview['seconds_encoded']:.3f}"
    film_seconds = f"{film['duration_seconds']:.3f}"
    html = TEMPLATE
    replacements = {
        "__DATA__": data,
        "__WARNING__": WARNING,
        "__AUDITION__": AUDITION,
        "__PROGRAM__": PROGRAM,
        "__PREVIEW_LINE__": PREVIEW_LINE,
        "__ON_PICTURE__": ON_PICTURE,
        "__PUBLICATION__": PUBLICATION,
        "__TAG_LINE__": TAG_LINE,
        "__ARTICLE_TITLE__": TITLE,
        "__RANGE__": catalog["range_statement"],
        "__DIRECTION__": catalog["creative_direction"],
        "__RESULT__": report["result"],
        "__CORE__": str(catalog["core_part_count"]),
        "__REFS__": str(catalog["reference_part_count"]),
        "__PART_ROWS__": "".join(part_rows),
        "__ARR_ROWS__": "".join(arrangement_rows),
        "__KIT_ITEMS__": "".join(kit_items),
        "__PREVIEW_SECONDS__": seconds,
        "__FILM_SECONDS__": film_seconds,
        "__PREVIEW_STATEMENT__": catalog["preview"]["statement"],
        "__REF_NOTE__": catalog["reference_note"],
    }
    for key, value in replacements.items():
        html = html.replace(key, value)
    return html


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dream Trance</title>
  <style>
    :root {
      --bg: #1c1410;
      --paper: #f6efe4;
      --ink: #2a1c14;
      --teal: #c47a45;
      --teal-2: #e0a15a;
      --sand: #f2e3a0;
      --muted: #d9cbb8;
      --line: rgba(246, 239, 228, .16);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; background: var(--bg); color: var(--paper);
      font-family: Georgia, "Iowan Old Style", Palatino, serif;
      line-height: 1.45;
    }
    a { color: var(--teal-2); }
    button, .meta, .note, .transport, .lane-label, .legend { font-family: ui-monospace, Menlo, Consolas, monospace; }
    .top {
      display: flex; justify-content: space-between; gap: 12px; align-items: center;
      padding: 12px 20px; background: #140e0c; border-bottom: 1px solid var(--line);
    }
    .brand { letter-spacing: .14em; text-transform: uppercase; font-size: .72rem; color: var(--paper); text-decoration: none; }
    .top nav { display: flex; gap: 14px; flex-wrap: wrap; font-size: .78rem; }
    main { width: min(1180px, calc(100% - 2rem)); margin: 0 auto; }
    .stage {
      display: grid; grid-template-columns: minmax(0, .82fr) minmax(0, 1.18fr);
      gap: 28px; align-items: start; padding: 26px 0 8px;
    }
    .stage > div { min-width: 0; }
    h1 { font-weight: 500; font-size: clamp(2.2rem, 5vw, 4.2rem); line-height: .92; margin: 8px 0 10px; }
    h2 { font-weight: 500; margin: 28px 0 8px; }
    .kicker { letter-spacing: .16em; text-transform: uppercase; color: var(--teal-2); font-size: .74rem; margin: 0; }
    .meta, .note { color: var(--muted); font-size: .82rem; }
    .hero img, audio, video, .stage img { display: block; width: 100%; height: auto; }
    .hero img { border-radius: 12px; }
    .rail, .phrases, .switch { display: flex; gap: 8px; flex-wrap: wrap; margin: 8px 0; }
    button {
      border: 1px solid var(--line); background: transparent; color: var(--paper);
      border-radius: 999px; padding: 7px 11px; cursor: pointer;
    }
    button[aria-pressed="true"] { background: var(--teal); color: white; border-color: var(--teal); }
    .transport {
      display: flex; gap: 10px; flex-wrap: wrap; align-items: center;
      margin: 8px 0 12px;
    }
    .scroller { overflow-x: auto; max-width: 100%; background: transparent; color: var(--ink); }
    .roll-wrap {
      display: grid; grid-template-columns: 9.4rem minmax(0, 1fr); align-items: start;
      background: var(--paper); color: var(--ink); border-radius: 16px; padding: 8px 0 12px;
    }
    .label-col { display: flex; flex-direction: column; }
    .ruler { position: relative; height: 28px; }
    .ruler-gap { height: 28px; }
    .change {
      position: absolute; top: 4px; height: 20px; border-left: 2px solid var(--teal);
      padding-left: 5px; font-size: 11px; white-space: nowrap; overflow: hidden;
    }
    .lane-label {
      height: 78px;
      font-size: 10px; letter-spacing: .08em; text-transform: uppercase; color: #6a4632;
      padding: 8px 8px 0 0;
    }
    .lane-notes { position: relative; height: 72px; border-top: 1px solid rgba(42, 28, 20, .12); }
    .lane-label { height: 72px; }
    .block { position: absolute; border-radius: 3px; min-width: 3px; }
    .block.pad { background: #c9deef; }
    .block.lead { background: #f2f6ff; }
    .block.keys { background: #7ea2c4; }
    .block.bass { background: #1c3148; }
    .block.drums { background: #5c7c99; }
    .legend { display: flex; gap: 12px; flex-wrap: wrap; font-size: .75rem; color: var(--muted); }
    .swatch { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 4px; }
    .table-scroll { overflow-x: auto; max-width: 100%; }
    table { width: 100%; border-collapse: collapse; font-size: .8rem; }
    th, td { text-align: left; padding: 7px 6px; border-bottom: 1px solid var(--line); vertical-align: top; }
    .flow { display: flex; flex-wrap: wrap; gap: 8px; }
    .flow span { border: 1px solid var(--line); border-radius: 999px; padding: 4px 8px; font-size: .78rem; }
    .map { padding-left: 1.1rem; }
    .map li { margin: 0 0 10px; }
    @media (max-width: 860px) {
      .stage { grid-template-columns: 1fr; }
      .top { align-items: flex-start; flex-direction: column; }
    }
  </style>
</head>
<body>
  <header class="top">
    <a class="brand" href="index.html">Dream Trance</a>
    <nav>
