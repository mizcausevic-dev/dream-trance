 = []
    pitched = [part for part in parts if part["role"] != "drums"]
    for index, left in enumerate(pitched):
        for right in pitched[index + 1:]:
            if is_same_velocity_transpose(left["notes"], right["notes"]):
                raise ValueError(f"{left['id']} and {right['id']} are a transposed copy with the same velocities")
    for role, kits_map in by_role.items():
        seen = {}
        for kit_id, versions in kits_map.items():
            left = versions["a"]["notes"]
            right = versions["b"]["notes"]
            if _sig(left) == _sig(right):
                raise ValueError(f"{kit_id} {role} variations match")
            if role != "drums" and (is_uniform_transpose(left, right) or is_uniform_transpose(right, left)):
                raise ValueError(f"{kit_id} {role} variation B is only a transpose of A")
            attacks = _attacks(left)
            if attacks in seen:
                raise ValueError(f"{role} variation A attack tuple repeats {seen[attacks]} and {kit_id}")
            seen[attacks] = kit_id
            report.append({
                "kit_id": kit_id,
                "role": role,
                "a_notes": len(left),
                "b_notes": len(right),
                "a_attacks": len(set(attacks)),
            })
    return {
        "rows": report,
        "method": (
            "For each core role, variation A and variation B differ in rhythm. "
            "Variation B is not a uniform transpose of variation A. "
            "No pitched part is a transposed copy of another pitched part with the same velocities. "
            "Variation A attack-time tuples are unique across the four kits."
        ),
    }


def _pitches_at(part, start):
    return [note["pitch"] for note in part["notes"] if note["performed_start"] == start]


def _require_names(text, names):
    for name in names:
        if name not in text:
            raise ValueError(f"identity or departure text is missing {name}")


def assert_story(parts, kit_rows):
    by_id = {part["id"]: part for part in parts}
    lead = [note["pitch"] for note in by_id["k01.lead.a"]["notes"]]
    expected_lead = [74, 78, 81, 79, 78, 76, 74, 71, 73, 74, 78, 76, 74, 69]
    if lead != expected_lead:
        raise ValueError(f"Glass Harbor lead {lead}")
    if spell_list(lead) != "D5 F#5 A5 G5 F#5 E5 D5 B4 C#5 D5 F#5 E5 D5 A4":
        raise ValueError(spell_list(lead))
    for start_bar, span, pitches, name, spelling in K01_KEYS:
        window_start = start_bar * BAR
        window_end = (start_bar + span) * BAR
        sounding = sorted({
            note["pitch"] for note in by_id["k01.keys.a"]["notes"]
            if window_start <= note["performed_start"] < window_end
        })
        if sounding != sorted(pitches):
            raise ValueError(f"{name} keys {sounding} != {spelling}")
    for start_bar, _span, pitches, name, spelling in K01_PAD:
        sounding = sorted(_pitches_at(by_id["k01.pad.a"], start_bar * BAR))
        if sounding != sorted(pitches):
            raise ValueError(f"{name} pad {sounding} != {pitches} ({spelling})")
    bass = [note["pitch"] for note in by_id["k01.bass.a"]["notes"]]
    if bass != [38, 45, 38, 45, 43, 50, 43, 50, 35, 42, 35, 42, 33, 40, 33, 40]:
        raise ValueError(f"Glass Harbor bass {bass}")
    lantern = [note["pitch"] for note in by_id["k02.lead.a"]["notes"]]
    if lantern[:3] != [72, 74, 76]:
        raise ValueError(f"Soft Lantern opening {lantern[:3]}")
    if spell_list(lantern[:3]) != "C5 D5 E5":
        raise ValueError(spell_list(lantern[:3]))
    for start_bar, _span, pitches, name, spelling in K02_KEYS:
        sounding = sorted(_pitches_at(by_id["k02.keys.a"], start_bar * BAR))
        if sounding != sorted(pitches):
            raise ValueError(f"{name} {sounding} != {spelling}")
    meadow = [note["pitch"] for note in by_id["k03.lead.a"]["notes"] if note["performed_start"] < BAR]
    if meadow != [77, 84, 81] or spell_list(meadow) != "F5 C6 A5":
        raise ValueError(f"Wide Meadow leap {meadow} {spell_list(meadow)}")
    for start_bar, _span, pitches, name, spelling in K03_KEYS:
        sounding = sorted(_pitches_at(by_id["k03.keys.a"], start_bar * BAR))
        if sounding != sorted(pitches):
            raise ValueError(f"{name} keys {sounding} != {spelling}")
    for start_bar, _span, pitches, name, spelling in K03_PAD:
        sounding = sorted(_pitches_at(by_id["k03.pad.a"], start_bar * BAR))
        if sounding != sorted(pitches):
            raise ValueError(f"{name} pad {sounding} != {spelling}")
    night = [note["pitch"] for note in by_id["k04.lead.a"]["notes"]]
    if night != [74, 73, 71, 67, 69, 76, 74, 73, 71, 66]:
        raise ValueError(f"Night Window lead {night}")
    if spell_list(night) != "D5 C#5 B4 G4 A4 E5 D5 C#5 B4 F#4":
        raise ValueError(spell_list(night))
    window = [note["pitch"] for note in by_id["k04.keys.a"]["notes"] if note["performed_start"] < BAR]
    if window != [59, 66, 62, 59] or spell_list(window) != "B3 F#4 D4 B3":
        raise ValueError(f"Night Window keys {window} {spell_list(window)}")
    for start_bar, _span, pitches, name, spelling in K04_PAD:
        sounding = sorted(_pitches_at(by_id["k04.pad.a"], start_bar * BAR + 960))
        if sounding != sorted(pitches):
            raise ValueError(f"{name} pad {sounding} != {spelling}")
    expected_departures = {
        "k01.bass.b": [36],
        "k02.lead.b": [73],
        "k03.bass.b": [46],
        "k04.pad.b": [70],
    }
    for part in parts:
        if part["role"] == "drums":
            continue
        found = [note["pitch"] for note in part["notes"] if note["departure"]]
        if found != expected_departures.get(part["id"], []):
            raise ValueError(f"{part['id']} departures {found}")
    by_kit = {kit["id"]: kit for kit in kit_rows}
    _require_names(by_kit["k01"]["identity"], ["D5 F#5 A5", "D4 F#4 A4 C#5", "D3 F#3 A3 C#4", "D2 A2"])
    _require_names(by_kit["k01"]["departures"][0], ["C2 (36)"])
    _require_names(by_kit["k02"]["identity"], ["C5 D5 E5", "A3 C4 E4 G4", "F#m7b5 spelled F#3 A3 C4 E4"])
    _require_names(by_kit["k02"]["departures"][0], ["C#5 (73)"])
    _require_names(by_kit["k03"]["identity"], ["F5 to C6", "F3 A3 C4 B4", "F3 C4 B4"])
    _require_names(by_kit["k03"]["departures"][0], ["Bb2 (46)"])
    _require_names(by_kit["k04"]["identity"], ["D5", "B3 F#4 D4 B3", "B3 D4 F#4 C#5"])
    _require_names(by_kit["k04"]["departures"][0], ["A#4 (70)"])
    if by_kit["k04"]["lead"] if False else False:
        raise ValueError("unused")


def _shift_notes(source, bar_offset):
    shift = bar_offset * BAR
    shifted = []
    for note in source["notes"]:
        start = note["performed_start"] + shift
        shifted.append({
            "nominal_start": start,
            "offset": 0,
            "performed_start": start,
            "duration": note["duration"],
            "pitch": note["pitch"],
            "velocity": note["velocity"],
            "channel": note["channel"],
            "departure": note["departure"],
        })
    return shifted


def build_arrangement(kit, by_id):
    container = kit["arrangement_bars"] * BAR
    tracks = [{"name": "Conductor", "source_part": None, "channel": None, "placements": [], "notes": []}]
    for role in ROLE_ORDER:
        source = by_id[f"{kit['id']}.{role}.a"]
        notes = []
        for offset in kit["placements"][role]:
            notes.extend(_shift_notes(source, offset))
        notes.sort(key=lambda note: (note["performed_start"], note["pitch"]))
        for note in notes:
            end = note["performed_start"] + note["duration"]
            if end > container:
                raise ValueError(f"{kit['id']} {role} arrangement boundary")
        tracks.append({
            "name": ROLE_NAME[role],
            "source_part": source["id"],
            "channel": source["channel"],
            "placements": list(kit["placements"][role]),
            "notes": notes,
        })
    path = "midi/arrangement.mid" if kit["id"] == "k01" else f"midi/{kit['slug']}/arrangement.mid"
    return {
        "id": f"{kit['id']}-arrangement-a",
        "kit_id": kit["id"],
        "path": path,
        "format": 1,
        "container_ticks": container,
        "container_bars": 32,
        "bpm": kit["bpm"],
        "tempo_us": kit["tempo_us"],
        "meter": "4/4",
        "description": (
            f"{kit['title']} variation A arranged over 32 bars. "
            "Bars 1-8 are drums and pad. Bars 9-16 add bass and keys. "
            "Bars 17-24 add the lead. Bars 25-32 keep drums, pad, bass, and lead, and leave the keys out. "
            "Each musical track is one or more copies of the 8-bar part, placed at the listed bar offsets."
        ),
        "tracks": tracks,
    }


def compose():
    kit_rows = kits()
    if len(kit_rows) != 4:
        raise ValueError("expected four kits")
    if any(sum(kit["change_bars"]) != 8 for kit in kit_rows):
        raise ValueError("change bars must fill 8 bars")
    parts = []
    for kit in kit_rows:
        builder = BUILDERS[kit["id"]]
        for variation in ("a", "b"):
            events = builder(variation)
            if set(events) != set(ROLE_ORDER):
                raise ValueError(kit["id"])
            for role in ROLE_ORDER:
                part = make(kit, role, variation)
                add_events(part, events[role])
                parts.append(part.finish())
    for part in parts:
        if part["role"] == "drums":
            assert_hats(part)
    assert_collections(kit_rows, parts)
    assert_story(parts, kit_rows)
    identity = assert_identities(parts)
    by_id = {part["id"]: part for part in parts}
    arrangements = [build_arrangement(kit, by_id) for kit in kit_rows]
    preview = arrangements[0]
    if preview["kit_id"] != "k01" or any(16 not in track["placements"] for track in preview["tracks"] if track["source_part"]):
        raise ValueError("preview arrangement does not place every Glass Harbor role at bar 16")
    core = [part for part in parts if part["core"]]
    refs = [part for part in parts if not part["core"]]
    if len(core) != 40 or refs:
        raise ValueError((len(core), len(refs)))
    catalog_kits = []
    for kit in kit_rows:
        catalog_kits.append({key: kit[key] for key in (
            "id", "slug", "title", "bpm", "tempo_us", "effective_bpm", "part_bars", "arrangement_bars",
            "bars", "meter", "bar_ticks", "tonic", "tonal_reference", "collection_name", "pitch_classes",
            "departures", "seed", "identity", "limitations", "harmonic_rhythm", "phrases",
            "arrangement_phrases", "changes", "change_bars", "spell", "placements", "stochastic_draws",
        )})
    catalog = {
        "pack_id": PACK_ID,
        "pack_name": PACK_NAME,
        "catalog_version": GENERATOR_VERSION,
        "generator_version": GENERATOR_VERSION,
        "ppq": PPQ,
        "c4": 60,
        "meter": {"numerator": 4, "denominator": 4, "bar_ticks": BAR},
        "container_plan": "Core parts are 8 bars. Arrangements are 32 bars. Lengths were fixed before the notes.",
        "creative_direction": (
            "Lyrical original motifs, gentle tension, rhythmic foundations, and spacious melodic development. "
            "The BPM range is a project choice, not a claim that these files are authentic genre productions."
        ),
        "note_policy": "Note-only MIDI. No program changes, controllers, pitch bend, or samples are encoded.",
        "microtiming": "offset is 0; performed_start = nominal_start",
        "stochastic_draws": 0,
        "seed_meaning": "Seeds identify kits. Nothing is random.",
        "core_part_count": 40,
        "reference_part_count": 0,
        "reference_note": "There is no reference-only part. Drums, bass, keys, lead, and pad are core. The arrangements reuse those files.",
        "drum_map": {str(pitch): name for pitch, name in DRUM_MAP.items()},
        "drum_channel": 10,
 