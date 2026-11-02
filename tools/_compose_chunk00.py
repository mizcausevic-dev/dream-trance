"""Original Dream Trance construction kits.

Container lengths were chosen before any notes: every core part is 8 bars,
every arrangement is 32 bars, meter 4/4. Tempos are integer quarter-note BPM
values inside the project range 125-140. Offsets are 0. Nothing is random.

The kits are Glass Harbor, Soft Lantern, Wide Meadow, and Night Window.
Each kit has its own tempo, collection, groove, and lead phrase.
"""

from __future__ import annotations

from tools.midi_io import BAR_TICKS_4_4, PPQ, bpm_to_us, effective_bpm

GENERATOR_VERSION = "dream-trance-1.0.0"
PACK_ID = "dream-trance"
PACK_NAME = "Dream Trance"
BAR = BAR_TICKS_4_4

DRUM_MAP = {
    36: "Bass Drum 1",
    38: "Acoustic Snare",
    42: "Closed Hi-Hat",
    46: "Open Hi-Hat",
    49: "Crash Cymbal 1",
}
ROLE_NAME = {
    "drums": "Drums",
    "bass": "Bass",
    "keys": "Keys",
    "lead": "Lead",
    "pad": "Pad",
}
ROLE_ORDER = ("drums", "bass", "keys", "lead", "pad")
SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]


class Part:
    def __init__(self, kit, role, variation, channel, slug, mono, poly, lo, hi):
        self.kit = kit
        self.part_id = f"{kit['id']}.{role}.{variation}"
        self.role = role
        self.variation = variation
        self.core = True
        self.channel = channel
        self.file_slug = slug
        self.monophonic = mono
        self.max_poly = poly
        self.lo = lo
        self.hi = hi
        self.container_ticks = kit["part_bars"] * BAR
        self.notes = []

    def add(self, start, duration, pitch, velocity, departure=False):
        end = start + duration
        if start < 0 or duration <= 0 or end > self.container_ticks:
            raise ValueError(f"{self.part_id} boundary {start}+{duration}")
        if not self.lo <= pitch <= self.hi:
            raise ValueError(f"{self.part_id} pitch {pitch}")
        if self.role == "drums" and pitch not in DRUM_MAP:
            raise ValueError(f"{self.part_id} drum pitch {pitch} is outside the map")
        if not 1 <= velocity <= 127:
            raise ValueError(f"{self.part_id} velocity {velocity}")
        active = 1
        for other in self.notes:
            o0 = other["performed_start"]
            o1 = o0 + other["duration"]
            if start < o1 and o0 < end:
                if other["pitch"] == pitch or self.monophonic:
                    raise ValueError(f"{self.part_id} overlap {pitch}@{start} with {other['pitch']}@{o0}")
                active += 1
        if active > self.max_poly:
            raise ValueError(f"{self.part_id} poly {active}")
        self.notes.append({
            "nominal_start": start,
            "offset": 0,
            "performed_start": start,
            "duration": duration,
            "pitch": pitch,
            "velocity": velocity,
            "channel": self.channel,
            "departure": departure,
        })

    def finish(self):
        ordered = sorted(self.notes, key=lambda note: (note["performed_start"], note["pitch"]))
        if len(ordered) < 4:
            raise ValueError(f"{self.part_id} too few notes")
        for index, note in enumerate(ordered, 1):
            note["id"] = f"{self.part_id}.n{index:04d}"
        return {
            "id": self.part_id,
            "kit_id": self.kit["id"],
            "slug": self.kit["slug"],
            "role": self.role,
            "variation": self.variation,
            "core": True,
            "channel": self.channel,
            "file_slug": self.file_slug,
            "path": f"midi/{self.kit['slug']}/{self.file_slug}.mid",
            "monophonic": self.monophonic,
            "max_poly": self.max_poly,
            "container_ticks": self.container_ticks,
            "container_bars": self.kit["part_bars"],
            "bpm": self.kit["bpm"],
            "tempo_us": self.kit["tempo_us"],
            "notes": ordered,
        }


def add_events(part, events):
    for event in events:
        bar, tick, dur, pitch, vel = event[:5]
        departure = bool(event[5]) if len(event) > 5 else False
        part.add(bar * BAR + tick, dur, pitch, vel, departure=departure)


def make(kit, role, variation):
    spec = {
        "drums": (9, f"drums-{variation}", False, 4, 36, 51),
        "bass": (0, f"bass-{variation}", True, 1, 28, 52),
        "keys": (1, f"keys-{variation}", False, 4, 48, 79),
        "lead": (2, f"lead-{variation}", True, 1, 60, 86),
        "pad": (3, f"pad-{variation}", False, 4, 45, 76),
    }
    channel, slug, mono, poly, lo, hi = spec[role]
    return Part(kit, role, variation, channel, slug, mono, poly, lo, hi)


def spell_pitch(pitch, flats=False):
    name = (FLAT if flats else SHARP)[pitch % 12]
    return f"{name}{pitch // 12 - 1}"


def spell_list(pitches, flats=False):
    return " ".join(spell_pitch(pitch, flats) for pitch in pitches)


def _ev(bar, tick, dur, pitch, vel, departure=False):
    row = (bar, tick, dur, pitch, vel)
    if departure:
        return row + (True,)
    return row


def _repeat(bars, rows):
    events = []
    for bar in bars:
        for row in rows:
            tick, dur, pitch, vel = row[:4]
            departure = bool(row[4]) if len(row) > 4 else False
            events.append(_ev(bar, tick, dur, pitch, vel, departure))
    return events


def _arp(chords, ticks, dur, velocities):
    events = []
    for start_bar, span, pitches, _name, spelling in chords:
        if spell_list(pitches) != spelling:
            raise ValueError(f"{_name} spelling {spelling} does not match {pitches}")
        step = 0
        for bar in range(start_bar, start_bar + span):
            for tick in ticks:
                pitch = pitches[step % len(pitches)]
                events.append(_ev(bar, tick, dur, pitch, velocities[step % len(velocities)]))
                step += 1
    return events


def _hold(chords, tick, dur, velocities):
    events = []
    for start_bar, span, pitches, name, spelling in chords:
        if spell_list(pitches) != spelling:
            raise ValueError(f"{name} spelling {spelling} does not match {pitches}")
        for pitch, velocity in zip(pitches, velocities):
            events.append(_ev(start_bar, tick, dur, pitch, velocity))
        if span != 1 and dur > BAR:
            pass
    return events


def _stab_pair(start_bar, span, low, high, low_vel, high_vel, low_dur, high_dur, high_tick):
    events = []
    for bar in range(start_bar, start_bar + span):
        for pitch, velocity in zip(low[0], low_vel):
            events.append(_ev(bar, 0, low_dur, pitch, velocity))
        for pitch, velocity in zip(high[0], high_vel):
            events.append(_ev(bar, high_tick, high_dur, pitch, velocity))
    return events


# Chord tables. The spelling is checked against the MIDI numbers before any file is written.

K01_KEYS = [
    (0, 2, [62, 66, 69, 73], "Dmaj7", "D4 F#4 A4 C#5"),
    (2, 2, [55, 59, 62, 66], "Gmaj7", "G3 B3 D4 F#4"),
    (4, 2, [59, 62, 66, 69], "Bm7", "B3 D4 F#4 A4"),
    (6, 2, [57, 61, 64, 66], "A6", "A3 C#4 E4 F#4"),
]
K01_PAD = [
    (0, 2, [50, 54, 57, 61], "Dmaj7", "D3 F#3 A3 C#4"),
    (2, 2, [55, 59, 62, 66], "Gmaj7", "G3 B3 D4 F#4"),
    (4, 2, [47, 50, 54, 57], "Bm7", "B2 D3 F#3 A3"),
    (6, 2, [45, 49, 52, 54], "A6", "A2 C#3 E3 F#3"),
]
K01_KEYS_B = [
    (0, 2, [62, 69, 73, 78], [66, 69, 74], "Dmaj7"),
    (2, 2, [55, 62, 66, 71], [59, 62, 67], "Gmaj7"),
    (4, 2, [59, 66, 69, 74], [62, 66, 71], "Bm7"),
    (6, 2, [57, 64, 66, 73], [61, 64, 69], "A6"),
]
K02_KEYS = [
    (0, 2, [57, 60, 64, 67], "Am7", "A3 C4 E4 G4"),
    (2, 2, [55, 59, 62, 64], "G6", "G3 B3 D4 E4"),
    (4, 2, [54, 57, 60, 64], "F#m7b5", "F#3 A3 C4 E4"),
    (6, 2, [52, 55, 59, 62], "Em7", "E3 G3 B3 D4"),
]
K03_KEYS = [
    (0, 1, [53, 57, 60, 71], "Fmaj7#11", "F3 A3 C4 B4"),
    (1, 1, [53, 57, 60, 71], "Fmaj7#11", "F3 A3 C4 B4"),
    (2, 1, [60, 64, 67, 71], "Cmaj7", "C4 E4 G4 B4"),
    (3, 1, [60, 64, 67, 71], "Cmaj7", "C4 E4 G4 B4"),
    (4, 1, [55, 59, 62, 64], "G6", "G3 B3 D4 E4"),
    (5, 1, [55, 59, 62, 64], "G6", "G3 B3 D4 E4"),
    (6, 1, [50, 53, 57, 60], "Dm7", "D3 F3 A3 C4"),
    (7, 1, [53, 57, 60, 71], "Fmaj7#11", "F3 A3 C4 B4"),
]
K03_PAD = [
    (0, 2, [53, 60, 71], "Fmaj7#11", "F3 C4 B4"),
    (2, 2, [60, 64, 71], "Cmaj7", "C4 E4 B4"),
    (4, 2, [55, 62, 64], "G6", "G3 D4 E4"),
    (6, 1, [50, 53, 60], "Dm7", "D3 F3 C4"),
    (7, 1, [53, 57, 71], "Fmaj7#11", "F3 A3 B4"),
]
K04_PAD = [
    (0, 2, [59, 62, 66, 73], "Bm add9", "B3 D4 F#4 C#5"),
    (2, 2, [55, 59, 62, 66], "Gmaj7", "G3 B3 D4 F#4"),
    (4, 2, [52, 55, 59, 62], "Em7", "E3 G3 B3 D4"),
    (6, 2, [54, 57, 61, 64], "F#m7", "F#3 A3 C#4 E4"),
]


def _keys_b_stabs(rows):
    events = []
    for start_bar, span, down, late, _name in rows:
        if spell_list(down) is None:
            raise ValueError(start_bar)
        for bar in range(start_bar, start_bar + span):
            for pitch, velocity in zip(down, (68, 74, 80, 86)):
                events.append(_ev(bar, 0, 700, pitch, velocity))
            for pitch, velocity in zip(late, (60, 66, 72)):
                events.append(_ev(bar, 2400, 900, pitch, velocity))
    return events


def _pad_beat3(voicings):
    events = []
    for bar, pitches in enumerate(voicings):
        for pitch, velocity in zip(pitches, (44, 50, 56)):
            events.append(_ev(bar, 1920, 1500, pitch, velocity))
    return events


def _lead(rows):
    return [_ev(*row) if len(row) == 5 else _ev(*row[:5], row[5]) for row in rows]


def drums_k01(variation):
    events = []
    if variation == "a":
        for bar in range(8):
            for tick, vel in ((0, 104), (960, 86), (1920, 98), (2880, 82)):
                events.append(_ev(bar, tick, 200, 36, vel - (bar % 3)))
            for tick in (0, 480, 960, 1440, 1920, 2400, 2880):
                events.append(_ev(bar, tick, 90, 42, 58 + (tick // 480) % 5))
            events.append(_ev(bar, 960, 180, 38, 92))
            events.append(_ev(bar, 2880, 180, 38, 88))
            events.append(_ev(bar, 3360, 280, 46, 70))
            if bar in (0, 4):
                events.append(_ev(bar, 0, 720, 49, 100 if bar == 0 else 84))
    else:
        for bar in range(8):
            events.append(_ev(bar, 0, 220, 36, 96))
            events.append(_ev(bar, 1920, 220, 36, 88))
            events.append(_ev(bar, 1920, 200, 38, 90))
            for tick, vel in ((480, 54), (1440, 62), (2400, 58)):
                events.append(_ev(bar, tick, 100, 42, vel))
            events.append(_ev(bar, 3360, 300, 46, 66))
    return events


def drums_k02(variation):
    events = []
    if variation == "a":
        for bar in range(8):
            events.append(_ev(bar, 0, 200, 36, 100))
            events.append(_ev(bar, 1440, 180, 36, 90))
            events.append(_ev(bar, 1920, 200, 38, 94))
            for tick in (0, 480, 960, 1440, 1920, 2400, 2880):
                events.append(_ev(bar, tick, 80, 42, 50 + (bar % 4) * 3))
            events.append(_ev(bar, 3360, 240, 46, 64))
    else:
        for bar in range(8):
            for tick, vel in ((0, 98), (960, 84), (1920, 92), (2880, 80)):
                events.append(_ev(bar, tick, 160, 36, vel))
            events.append(_ev(bar, 960, 160, 38, 88))
            events.append(_ev(bar, 2880, 160, 38, 84))
            for tick in (240, 720, 1200, 1680, 2160, 2640, 3120, 3600):
                events.append(_ev(bar, tick, 70, 42, 48))
    return events


def drums_k03(variation):
    events = []
    if variation == "a":
        for bar in range(8):
            events.append(_ev(bar, 0, 200, 36, 102))
            events.append(_ev(bar, 1920, 200, 36, 90))
            events.append(_ev(bar, 960, 160, 38, 86))
            events.append(_ev(bar, 3360, 160, 38, 80))
            for tick in (480, 1440, 2400):
                events.append(_ev(bar, tick, 90, 42, 56))
            events.append(_ev(bar, 2880, 360, 46, 68))
            if bar == 0:
      