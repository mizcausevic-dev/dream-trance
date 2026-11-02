        events.append(_ev(bar, 0, 600, 49, 96))
    return events


def build_kit(kit_id, slug, title, bpm, part_bars, arr_bars, changes, change_bars, phrases, arr_phrases, builders):
    tempo_us = bpm_to_us(bpm)
    kit = {
        "id": kit_id,
        "slug": slug,
        "title": title,
        "bpm": bpm,
        "tempo_us": tempo_us,
        "part_bars": part_bars,
        "arrangement_bars": arr_bars,
        "changes": changes,
        "change_bars": change_bars,
        "phrases": phrases,
        "arrangement_phrases": arr_phrases,
    }
    parts = []
    for role in ROLE_ORDER:
        for variation in ("a", "b"):
            part = make(kit, role, variation)
            add_events(part, builders[role](variation))
            parts.append(part.finish())
    arrangement = builders["arrangement"](kit, parts)
    return kit, parts, arrangement


def compose():
    kits = []
    all_parts = []
    arrangements = []
    # Kit definitions are assembled in earlier chunks; this chunk closes compose().
    for builder in _KIT_BUILDERS:
        kit, parts, arrangement = builder()
        kits.append(kit)
        all_parts.extend(parts)
        arrangements.append(arrangement)
    catalog = {
        "pack_id": PACK_ID,
        "pack_name": PACK_NAME,
        "generator_version": GENERATOR_VERSION,
        "ppq": PPQ,
        "roles": [{"id": role, "label": ROLE_NAME[role]} for role in ROLE_ORDER],
        "kits": kits,
    }
    preview = arrangements[0]
    identity = {"unique_velocity_fingerprints": True, "no_transposed_clones": True}
    parts = all_parts
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
