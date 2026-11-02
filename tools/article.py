"""Factual article draft. Not published."""

from __future__ import annotations

from tools.statements import AUDITION, ON_PICTURE, PREVIEW_LINE, PROGRAM, PUBLICATION, WARNING

TITLE = "Dream Trance is a note-only MIDI construction kit"
SUBTITLE = "Four kits, separate keys and lead lines, and an 8-bar simple-synth preview that is not a master"
TAGS = ["midi", "trance", "music-production", "composition", "dream-trance"]
TAG_LINE = "Tags: " + ", ".join(TAGS)

PARAGRAPHS: list[str] = []


def set_preview_seconds(seconds: str) -> None:
    if len(TAGS) > 5:
        raise ValueError("Medium tags")
    body = [
        "DRAFT. " + PUBLICATION,
        TAG_LINE,
        "The pack is four construction kits in 4/4. Tempos are 128, 132, 136, and 126 BPM. Those integers sit in the project range 125 to 140. They are a creative direction, not a claim that the files are authentic dream trance productions. Every core part is 8 bars. Every kit has one 32-bar arrangement. Lengths were chosen before the notes were written.",
        "Each kit has two variations of five core roles: drums, bass, keys, lead, and pad. That is 40 core files. There are no reference-only files. Variation B changes the phrase. It is not a velocity edit and not a uniform transpose of variation A. Glass Harbor is 128 BPM in D major. Lead A states D5 F#5 A5, turns through G5 and E5, lifts B4 C#5 D5 F#5, and settles on A4. Keys A arpeggiate Dmaj7 spelled D4 F#4 A4 C#5 and related changes. Soft Lantern is 132 BPM in A dorian. Wide Meadow is 136 BPM in F lydian, with B natural written as an ordinary note. Night Window is 126 BPM in B natural minor, with keys and lead kept distinct.",
        "Drums use channel 10 and an explicit note map: kick 36, snare 38, closed hat 42, open hat 46, crash 49. Closed and open hats do not overlap. Bass is monophonic, MIDI 28 to 52. Keys allow four notes, MIDI 48 to 79. Lead is monophonic, MIDI 60 to 86. Pad allows four notes, MIDI 45 to 76. C4 is 60. The resolution is 960 ticks per quarter note. Offsets are 0. Variation B flags one outside note per kit: C2 in Glass Harbor bass, C#5 in Soft Lantern lead, Bb2 in Wide Meadow bass, and A#4 in Night Window pad.",
        PROGRAM,
        "The pad is ordinary notes. The preview synth plays them with a quiet sine and a slow attack. That envelope is not in the MIDI. Keys are a triangle figure. The lead is a brighter triangle. Bass is a sine. Drums are short sines or noise bursts chosen by the MIDI pitch. Nothing in the file is a sample or a program change.",
        "The primary preview is bars 17-24 of Glass Harbor at 128 BPM, variation A, all five roles. The encoded MP3 is "
        + seconds
        + " seconds. The 32-bar arrangement remains in the MIDI and is not the MP3. "
        + PREVIEW_LINE
        + ". The film takes its audio from that preview and shows the words "
        + ON_PICTURE
        + " on the picture and in the WebVTT captions.",
        AUDITION
        + " The validator reopened the MIDI bytes and compared them with the canonical score. That is a structural check. The sample peak written beside the preview is the peak of the integer mix. It is not a loudness measurement. Nothing in this build is claimed as a master.",
        "The stills are procedural illustrations of five lanes on a midnight field. Long pale bars stand for the pad. A bright lane stands for the lead. Short ticks stand for drums. They are not photographs of a session or of performers.",
        "When you use the files, use either the combined arrangement or the separate parts. " + WARNING,
        "Call to action: keep the MIDI, the matched report, and the preview together. Do not publish this draft to Medium, Instagram, or X from the draft files alone.",
    ]
    PARAGRAPHS[:] = body


def markdown() -> str:
    if not PARAGRAPHS:
        raise RuntimeError("preview seconds were not measured")
    body = "\n\n".join(PARAGRAPHS)
    return f"# {TITLE}\n\n{SUBTITLE}\n\n{body}\n"


def plain_text() -> str:
    if not PARAGRAPHS:
        raise RuntimeError("preview seconds were not measured")
    lines = [TITLE, "", SUBTITLE, "", *PARAGRAPHS, ""]
    return "\n".join(lines) + "\n"
