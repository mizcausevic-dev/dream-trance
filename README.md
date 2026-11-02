# Dream Trance

Original note-only MIDI construction kits. Four kits, five core roles, two variations of each role. The roles are drums, bass, keys, lead, and pad. Each part is 8 bars. Each kit has one 32-bar arrangement built from variation A. There are no reference-only parts.

This is a creative direction: lyrical motifs, gentle tension, rhythmic foundations, and spacious melodic development. It is not a claim that the files are authentic genre productions. Tempos sit in the project range 125 to 140 BPM. The GitHub repository is https://github.com/mizcausevic-dev/dream-trance and it is public. The catalog page is https://mizcausevic-dev.github.io/dream-trance/ .

## What you can open

- `index.html` is the file catalog. The kit chooser draws lanes from the MIDI bytes.
- `media.html` is the stills page. The film sits under the pictures.
- `midi/arrangement.mid` is the Format 1 arrangement of Glass Harbor, variation A, 32 bars.
- The other three arrangements live next to their part files under `midi/`.
- Individual Format 0 parts live under `midi/`.
- `midi/validation-Cursor.json` is the report from reopening those exact bytes.
- `preview/preview.mp3` is the primary music preview. It is 15.047 seconds in the encoded file. preview, not a master.
- `film/preview.mp4` and `film/preview.vtt` are the film. On-picture and caption text is `preview, not master`.
- `art/hero.jpg` is a 1280x720 illustration. `art/square.jpg` is 1080x1080. Neither is a photograph.

Use either the combined arrangement or the separate parts. Do not stack the part files on top of the combined file.

## Kits

- k01 Glass Harbor: 128 BPM, parts 8 bars, arrangement 32 bars, D major, tonic D.
- k02 Soft Lantern: 132 BPM, parts 8 bars, arrangement 32 bars, A dorian, tonic A.
- k03 Wide Meadow: 136 BPM, parts 8 bars, arrangement 32 bars, F lydian, tonic F.
- k04 Night Window: 126 BPM, parts 8 bars, arrangement 32 bars, B natural minor, tonic B.

Core files: 40. Reference files: 0. There is no reference-only part. Drums, bass, keys, lead, and pad are core. The arrangements reuse those files.

Drums use channel 10 and the map in this catalog. Bass is monophonic, MIDI 28 to 52. Keys are MIDI 48 to 79, at most four notes. Lead is monophonic, MIDI 60 to 86. Pad is MIDI 45 to 76, at most four notes. C4 is 60. C4 is 60. PPQ is 960. Meter is 4/4. Offsets are 0. Seeds identify kits and are not random draws. Generator dream-trance-1.0.0.

Drums use channel 10. The drum map is kick 36, snare 38, closed hat 42, open hat 46, crash 49. Closed and open hats do not overlap, and no choke controller is written. Keys and lead stay in separate roles.

## Preview path

The preview renders bars 17-24 of `midi/arrangement.mid` (ticks 61440 through 92160) with `simple-synth-1.0.0`. Those notes are variation A of all five Glass Harbor parts, each shifted to the Melody section of the arrangement. The 32-bar arrangement stays in the MIDI. It is not the MP3. Tempo authority is the encoded microsecond value in the MIDI, 468750 us per quarter note. Sample positions use `floor(seconds * 44100 + 0.5)` from the excerpt start. Intervals are not summed. Sample-exact repeating loops at an arbitrary BPM are not promised.

The synth mapping is documented in the preview manifest. Bass is a sine. Keys are a triangle. The lead is a brighter triangle. The pad is a quieter sine with a slow attack. The pad attack is the synth envelope, not a message in the MIDI. Drum pitches select short sines or noise bursts. No program changes are encoded. A conventional GM player will normally use its default piano program for pitched channels unless configured otherwise; compatible GM channel 10 percussion is treated separately. Player behavior may vary. The mapping is not encoded in the MIDI.

Encoded MP3 settings: libmp3lame, 192 kbps. Film audio is AAC at 160 kbps re-encoded from that MP3, so the decoded film audio is not byte-identical to the MP3. Film duration probe: 15.000 seconds. MP3 container probe 15.047 seconds. MP4 probe 15.000 seconds. The film ends on a video frame, so it is slightly shorter than the MP3 container. The music is the same preview, not a different excerpt. The picture is a still illustration with rasterized disclosure text. DejaVu Sans Bold from the build machine supplies the glyphs. The font file is not in this pack.

No human listening audition was performed for this build. A sample peak is recorded in the preview manifest. It is not a loudness measurement.

## Build

From the repository root, with Python 3.11+ and ffmpeg (libmp3lame, aac, libx264):

```bash
python3 tools/build_pack.py
python3 -m http.server 43228
```

The page is static. It is served with Python's HTTP server so the MIDI and media keep working relative paths. There is no application server and no package install. Standard library only.

`build/` holds the intermediate WAV, the procedural PPM, and the film plate. Those files are gitignored. The delivered audio is the MP3.

## Checks the validator actually runs

File existence, parse, PPQ, tempo, 4/4, end-of-track boundary, note pairing, ranges, monophonic bass and lead, role polyphony caps, channel 10 map, same-pitch overlap, note-off before note-on at a shared tick, absence of program changes and other channel messages, closed and open hat overlap, departure flags against the declared pitch-class set, agreement with the canonical score, and agreement between each arrangement and the placed source parts. Variation A attack times must differ across kits for each role. Variation B must not be a uniform transpose of A. No pitched part may be a transposed copy of another with the same velocities. A negative overlap fixture is written outside the pack and must be rejected.

## Drafts and publication

Social captions, the X post, and the Medium article are drafts. They are not access controls. If this repository is public, the drafts are public. Do not treat them as posted to Instagram, X, or Medium.

Prepared repository description: Original note-only Dream Trance construction kits with matched validation and a simple-synth preview.

Prepared topics: midi, trance, music-production, composition, construction-kit.

No release tag was created. `index.html` keeps its name because players and links depend on it. This page is the file catalog the pack requires. GitHub Pages serves the gh-pages branch.

## Limitations

Variation A and variation B of a kit are alternatives. The arrangement already contains variation A, so stacking the part files on top of it doubles those notes. Parts from different kits do not share a tempo or a collection. Keys are chords or broken figures. The lead is one monophonic line. These parts are original.
