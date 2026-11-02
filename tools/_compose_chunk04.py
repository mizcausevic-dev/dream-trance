       "range_statement": (
            "Drums use channel 10 and the map in this catalog. "
            "Bass is monophonic, MIDI 28 to 52. Keys are MIDI 48 to 79, at most four notes. "
            "Lead is monophonic, MIDI 60 to 86. Pad is MIDI 45 to 76, at most four notes. C4 is 60."
        ),
        "kits": catalog_kits,
        "parts": [{
            "id": part["id"],
            "kit_id": part["kit_id"],
            "role": part["role"],
            "variation": part["variation"],
            "core": part["core"],
            "channel": part["channel"],
            "path": part["path"],
            "notes": len(part["notes"]),
            "container_bars": part["container_bars"],
            "bpm": part["bpm"],
            "monophonic": part["monophonic"],
        } for part in parts],
        "arrangements": [{
            "id": item["id"],
            "kit_id": item["kit_id"],
            "path": item["path"],
            "bpm": item["bpm"],
            "container_bars": item["container_bars"],
            "description": item["description"],
            "placements": {track["source_part"]: track["placements"] for track in item["tracks"] if track["source_part"]},
        } for item in arrangements],
        "arrangement": {
            "id": preview["id"],
            "path": preview["path"],
            "kit_id": "k01",
            "container_bars": 32,
            "description": preview["description"],
        },
        "preview": {
            "kit_id": "k01",
            "title": "Glass Harbor",
            "bpm": 128,
            "musical_bars": "17-24",
            "start_bar_index": 16,
            "end_bar_index": 24,
            "start_tick": 16 * BAR,
            "end_tick": 24 * BAR,
            "variation": "a",
            "arrangement_path": preview["path"],
            "statement": "Bars 17-24 of the Glass Harbor arrangement. Eight bars at 128 BPM. Variation A of drums, bass, keys, lead, and pad.",
        },
        "preview_part_ids": [f"k01.{role}.a" for role in ROLE_ORDER],
        "stack_warning": (
            "Use either the combined arrangement or the separate parts. "
            "Do not stack the part files on top of the combined file."
        ),
    }
    score = {
        "pack_id": PACK_ID,
        "generator_version": GENERATOR_VERSION,
        "ppq": PPQ,
        "parts": parts,
        "arrangements": arrangements,
        "arrangement": preview,
        "identity_check": identity,
    }
    return {"catalog": catalog, "score": score}
