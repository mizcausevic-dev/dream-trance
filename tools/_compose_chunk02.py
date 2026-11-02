irs = [
        ([59, 71], [62, 69]),
        ([66, 74], [64, 71]),
        ([55, 67], [59, 66]),
        ([62, 69], [55, 62]),
        ([52, 64], [55, 67]),
        ([59, 71], [57, 64]),
        ([54, 66], [61, 73]),
        ([57, 69], [59, 66]),
    ]
    events = []
    for bar, (early, late) in enumerate(pairs):
        for pitch, velocity in zip(early, (64, 76)):
            events.append(_ev(bar, 1440, 420, pitch, velocity))
        for pitch, velocity in zip(late, (60, 72)):
            events.append(_ev(bar, 3360, 420, pitch, velocity))
    return events


def events_k01(variation):
    return {
        "drums": drums_k01(variation),
        "bass": bass_k01(variation),
        "keys": _arp(K01_KEYS, (0, 480, 960, 1440, 1920, 2400, 2880, 3360), 400, (64, 72, 80, 74)) if variation == "a" else _keys_b_stabs(K01_KEYS_B),
        "lead": _lead(K01_LEAD_A if variation == "a" else K01_LEAD_B),
        "pad": pad_k01(variation),
    }


def events_k02(variation):
    if variation == "a":
        keys = _hold(K02_KEYS, 0, 7000, (58, 64, 70, 76))
    else:
        keys = _arp(K02_KEYS, (960, 1440, 2880, 3360), 380, (66, 74, 70, 62))
    return {
        "drums": drums_k02(variation),
        "bass": bass_k02(variation),
        "keys": keys,
        "lead": _lead(K02_LEAD_A if variation == "a" else K02_LEAD_B),
        "pad": pad_k02(variation),
    }


def events_k03(variation):
    if variation == "a":
        keys = _hold(K03_KEYS, 0, 1400, (62, 70, 78, 74))
    else:
        keys = _arp(K03_KEYS, (1920, 2160, 2400, 2640, 2880, 3120, 3360, 3600), 160, (62, 70, 78, 66))
    return {
        "drums": drums_k03(variation),
        "bass": bass_k03(variation),
        "keys": keys,
        "lead": _lead(K03_LEAD_A if variation == "a" else K03_LEAD_B),
        "pad": pad_k03(variation),
    }


def events_k04(variation):
    return {
        "drums": drums_k04(variation),
        "bass": bass_k04(variation),
        "keys": keys_k04_a() if variation == "a" else keys_k04_b(),
        "lead": _lead(K04_LEAD_A) if variation == "a" else lead_k04_b(),
        "pad": pad_k04(variation),
    }


BUILDERS = {
    "k01": events_k01,
    "k02": events_k02,
    "k03": events_k03,
    "k04": events_k04,
}

PLACEMENTS = {
    "drums": [0, 8, 16, 24],
    "pad": [0, 8, 16, 24],
    "bass": [8, 16, 24],
    "keys": [8, 16],
    "lead": [16, 24],
}
PHRASES = [
    {"name": "Opening", "start_bar": 0},
    {"name": "Turn", "start_bar": 2},
    {"name": "Lift", "start_bar": 4},
    {"name": "Settle", "start_bar": 6},
]
ARRANGEMENT_PHRASES = [
    {"name": "Atmosphere", "start_bar": 0},
    {"name": "Foundation", "start_bar": 8},
    {"name": "Melody", "start_bar": 16},
    {"name": "Return", "start_bar": 24},
]


def _chord_sentence(chords, role):
    pieces = []
    for start, span, pitches, name, spelling in chords:
        if spell_list(pitches) != spelling:
            raise ValueError(name)
        pieces.append(f"{name} for {span} bar{'s' if span != 1 else ''} spelled {spelling}")
    return f"{role}: " + "; ".join(pieces) + "."


def kits():
    common_limit = (
        "Variation A and variation B are alternatives. Do not stack them. "
        "Do not mix parts from different kits: the tempos and collections differ. "
        "The 32-bar arrangement uses variation A only. "
        "Keys are chords or broken chords. The lead is one line. "
        "Closed and open hats never overlap, and no hat-choke controller is written."
    )
    rows = [
        {
            "id": "k01",
            "slug": "k01-glass-harbor",
            "title": "Glass Harbor",
            "bpm": 128,
            "tonic": "D",
            "collection_name": "D major",
            "pitch_classes": [1, 2, 4, 6, 7, 9, 11],
            "seed": 12828,
            "identity": (
                "Glass Harbor is 128 BPM in D major. Lead A states D5 F#5 A5, turns G5 F#5 E5 D5, "
                "lifts B4 C#5 D5 F#5, and settles E5 D5 A4. "
                "Keys A arpeggiate Dmaj7 spelled D4 F#4 A4 C#5, Gmaj7 spelled G3 B3 D4 F#4, "
                "Bm7 spelled B3 D4 F#4 A4, and A6 spelled A3 C#4 E4 F#4. "
                "The pad holds Dmaj7 spelled D3 F#3 A3 C#4, Gmaj7 spelled G3 B3 D4 F#4, "
                "Bm7 spelled B2 D3 F#3 A3, and A6 spelled A2 C#3 E3 F#3. "
                "Bass A sounds D2 A2, then G2 D3, then B1 F#2, then A1 E2. "
                "Variation B changes every role: the lead starts after the downbeat, the keys become stabs, "
                "the bass walks eighths with one C2, the pad enters late, and the kick moves to half time."
            ),
            "departures": [
                "Bass B has one C2 (36) at bar 1, tick 2880. C is outside D major. Bar 2 returns to G2."
            ],
            "changes": ["Dmaj7", "Gmaj7", "Bm7", "A6"],
            "change_bars": [2, 2, 2, 2],
            "harmonic_rhythm": _chord_sentence(K01_KEYS, "Keys A") + " " + _chord_sentence(K01_PAD, "Pad A"),
        },
        {
            "id": "k02",
            "slug": "k02-soft-lantern",
            "title": "Soft Lantern",
            "bpm": 132,
            "tonic": "A",
            "collection_name": "A dorian",
            "pitch_classes": [9, 11, 0, 2, 4, 6, 7],
            "seed": 13228,
            "identity": (
                "Soft Lantern is 132 BPM in A dorian. Lead A waits one beat, then states C5 D5 E5, "
                "holds G5 E5, turns D5 C5 A4, holds B4, then spells A4 C5 E5 F#5 and falls E5 D5 C5 A4. "
                "Keys A hold Am7 spelled A3 C4 E4 G4, G6 spelled G3 B3 D4 E4, "
                "F#m7b5 spelled F#3 A3 C4 E4, and Em7 spelled E3 G3 B3 D4. "
                "The pad answers on beat 3 with three-note subsets of those chords. "
                "Bass A holds A1 E2, G1 D2, F#1 C2, and E1 B1, one note per bar. "
                "Variation B breaks the keys into offbeat eighths and gives the lead long tones, "
                "including one C#5 outside A dorian."
            ),
            "departures": [
                "Lead B has one C#5 (73) at bar 5, tick 0. C# is outside A dorian. The next note is B4."
            ],
            "changes": ["Am7", "G6", "F#m7b5", "Em7"],
            "change_bars": [2, 2, 2, 2],
            "harmonic_rhythm": _chord_sentence(K02_KEYS, "Keys A"),
        },
        {
            "id": "k03",
            "slug": "k03-wide-meadow",
            "title": "Wide Meadow",
            "bpm": 136,
            "tonic": "F",
            "collection_name": "F lydian",
            "pitch_classes": [5, 7, 9, 11, 0, 2, 4],
            "seed": 13628,
            "identity": (
                "Wide Meadow is 136 BPM in F lydian. The B natural is the raised fourth, written as an ordinary note. "
                "Lead A leaps F5 to C6, then A5, and later spells D5 B4 G4 before F4. "
                "Keys A hold Fmaj7#11 spelled F3 A3 C4 B4, Cmaj7 spelled C4 E4 G4 B4, "
                "G6 spelled G3 B3 D4 E4, Dm7 spelled D3 F3 A3 C4, and a return to Fmaj7#11 spelled F3 A3 C4 B4. "
                "Pad A uses three-note subsets: Fmaj7#11 spelled F3 C4 B4, Cmaj7 spelled C4 E4 B4, "
                "G6 spelled G3 D4 E4, Dm7 spelled D3 F3 C4, and Fmaj7#11 spelled F3 A3 B4. "
                "Bass A pulses the root in eighths and sounds the fifth on beat 3, returning to F2 A2 C3 F2 in bar 8. "
                "Variation B moves the keys into the second half of the bar and walks the bass in offbeats, with one Bb2."
            ),
            "departures": [
                "Bass B has one Bb2 (46) at bar 3, tick 1440. Bb is outside F lydian. The next note is A2."
            ],
            "changes": ["Fmaj7#11", "Cmaj7", "G6", "Dm7", "Fmaj7#11"],
            "change_bars": [2, 2, 2, 1, 1],
            "harmonic_rhythm": _chord_sentence(K03_KEYS, "Keys A") + " " + _chord_sentence(K03_PAD, "Pad A"),
        },
        {
            "id": "k04",
            "slug": "k04-night-window",
            "title": "Night Window",
            "bpm": 126,
            "tonic": "B",
            "collection_name": "B natural minor",
            "pitch_classes": [11, 1, 2, 4, 6, 7, 9],
            "seed": 12628,
            "identity": (
                "Night Window is 126 BPM in B natural minor. There is no raised leading tone in variation A. "
                "Lead A starts on beat 3 with D5, then C#5 B4 G4, holds A4, lifts E5, and ends F#4. "
                "Keys A break tenths in quarter notes: bar 1 spells B3 F#4 D4 B3. "
                "The pad enters on beat 2 and holds Bm add9 spelled B3 D4 F#4 C#5, Gmaj7 spelled G3 B3 D4 F#4, "
                "Em7 spelled E3 G3 B3 D4, and F#m7 spelled F#3 A3 C#4 E4. "
                "Bass A sounds three offbeat sixteenths: B1 F#2 B1, then G1 D2 G1, E1 B1 E1, and F#1 C#2 F#1. "
                "Variation B answers with eighth-note lead cells, dyad keys, half-note bass, and one A#4 in the pad."
            ),
            "departures": [
                "Pad B has one A#4 (70) at bar 7, tick 0, beside C#5. A# is outside B natural minor. The next dyad is F#4 B4."
            ],
            "changes": ["Bm add9", "Gmaj7", "Em7", "F#m7"],
            "change_bars": [2, 2, 2, 2],
            "harmonic_rhythm": _chord_sentence(K04_PAD, "Pad A"),
        },
    ]
    built = []
    for row in rows:
        tempo_us = bpm_to_us(row["bpm"])
        built.append({
            **row,
            "tempo_us": tempo_us,
            "effective_bpm": effective_bpm(tempo_us),
            "part_bars": 8,
            "arrangement_bars": 32,
            "bars": 8,
            "meter": "4/4",
            "bar_ticks": BAR,
            "tonal_reference": row["tonic"],
            "limitations": common_limit,
            "phrases": PHRASES,
            "arrangement_phrases": ARRANGEMENT_PHRASES,
            "spell": SHARP,
            "placements": PLACEMENTS,
            "stochastic_draws": 0,
        })
    return built


def _sig(notes):
    return tuple((note["performed_start"], note["pitch"], note["duration"]) for note in notes)


def _attacks(notes):
    return tuple(note["performed_start"] for note in notes)


def is_uniform_transpose(left, right):
    if len(left) != len(right) or not left:
        return False
    paired = list(zip(left, right))
    if any(a["performed_start"] != b["performed_start"] or a["duration"] != b["duration"] for a, b in paired):
        return False
    deltas = {b["pitch"] - a["pitch"] for a, b in paired}
    return len(deltas) == 1 and deltas != {0}


def is_same_velocity_transpose(left, right):
    if not is_uniform_transpose(left, right):
        return False
    return all(a["velocity"] == b["velocity"] for a, b in zip(left, right))


def assert_hats(part):
    hats = [note for note in part["notes"] if note["pitch"] in (42, 46)]
    for index, left in enumerate(hats):
        left_end = left["performed_start"] + left["duration"]
        for right in hats[index + 1:]:
            right_end = right["performed_start"] + right["duration"]
            if left["performed_start"] < right_end and right["performed_start"] < left_end and left["pitch"] != right["pitch"]:
                raise ValueError(f"{part['id']} open and closed hats overlap")


def assert_collections(kit_rows, parts):
    allowed = {kit["id"]: set(kit["pitch_classes"]) for kit in kit_rows}
    for part in parts:
        if part["role"] == "drums":
            continue
        pool = allowed[part["kit_id"]]
        for note in part["notes"]:
            inside = (note["pitch"] % 12) in pool
            if note["departure"] and inside:
                raise ValueError(f"{part['id']} departure {note['pitch']} is inside the collection")
            if not note["departure"] and not inside:
                raise ValueError(f"{part['id']} note {note['pitch']} left the collection")


def assert_identities(parts):
    by_role = {}
    for part in parts:
        by_role.setdefault(part["role"], {}).setdefault(part["kit_id"], {})[part["variation"]] = part
    report