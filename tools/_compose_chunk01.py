          events.append(_ev(bar, 0, 600, 49, 96))
    else:
        for bar in range(8):
            for tick in (0, 960, 1920, 2880):
                events.append(_ev(bar, tick, 150, 36, 94 if tick == 0 else 82))
            events.append(_ev(bar, 2880, 180, 38, 90))
            for tick in (0, 240, 480, 720, 960, 1200, 1440, 1680, 1920, 2160, 2400, 2640, 3120, 3600):
                events.append(_ev(bar, tick, 60, 42, 46))
    return events


def drums_k04(variation):
    events = []
    if variation == "a":
        for bar in range(8):
            events.append(_ev(bar, 0, 240, 36, 100))
            events.append(_ev(bar, 2400, 200, 36, 86))
            events.append(_ev(bar, 1920, 220, 38, 92))
            for tick in (0, 960, 1920, 2880):
                events.append(_ev(bar, tick, 110, 42, 52))
            events.append(_ev(bar, 3360, 260, 46, 62))
    else:
        for bar in range(8):
            for tick, vel in ((0, 98), (1440, 84), (2880, 90)):
                events.append(_ev(bar, tick, 180, 36, vel))
            events.append(_ev(bar, 960, 150, 38, 86))
            events.append(_ev(bar, 2880, 150, 38, 82))
            for tick in (720, 1680, 2640, 3600):
                events.append(_ev(bar, tick, 80, 42, 50))
    return events


def bass_k01(variation):
    if variation == "a":
        rows = []
        pairs = [(38, 45), (38, 45), (43, 50), (43, 50), (35, 42), (35, 42), (33, 40), (33, 40)]
        for bar, (root, fifth) in enumerate(pairs):
            rows.append(_ev(bar, 0, 1400, root, 96 - bar))
            rows.append(_ev(bar, 2400, 1000, fifth, 78 - (bar % 4)))
        return rows
    return [
        _ev(0, 0, 700, 38, 88), _ev(0, 960, 700, 40, 80), _ev(0, 1920, 700, 42, 84), _ev(0, 2880, 700, 45, 76),
        _ev(1, 0, 700, 37, 86), _ev(1, 960, 700, 38, 82), _ev(1, 1920, 700, 42, 78), _ev(1, 2880, 700, 36, 74, True),
        _ev(2, 0, 700, 43, 90), _ev(2, 960, 700, 45, 82), _ev(2, 1920, 700, 47, 84), _ev(2, 2880, 700, 50, 76),
        _ev(3, 0, 700, 47, 86), _ev(3, 960, 700, 45, 80), _ev(3, 1920, 700, 43, 78), _ev(3, 2880, 700, 42, 72),
        _ev(4, 0, 700, 35, 92), _ev(4, 960, 700, 38, 84), _ev(4, 1920, 700, 42, 80), _ev(4, 2880, 700, 45, 74),
        _ev(5, 0, 700, 45, 86), _ev(5, 960, 700, 42, 80), _ev(5, 1920, 700, 40, 76), _ev(5, 2880, 700, 38, 70),
        _ev(6, 0, 700, 33, 88), _ev(6, 960, 700, 37, 82), _ev(6, 1920, 700, 40, 78), _ev(6, 2880, 700, 42, 74),
        _ev(7, 0, 700, 40, 84), _ev(7, 960, 700, 38, 78), _ev(7, 1920, 700, 37, 74), _ev(7, 2880, 700, 33, 68),
    ]


def bass_k02(variation):
    if variation == "a":
        pitches = [33, 40, 31, 38, 30, 36, 28, 35]
        vels = [98, 84, 90, 78, 88, 76, 86, 72]
        return [_ev(bar, 0, 3400, pitch, vel) for bar, (pitch, vel) in enumerate(zip(pitches, vels))]
    rows = [
        (45, 40), (43, 38), (42, 36), (40, 35), (38, 33), (36, 31), (35, 40), (33, 36),
    ]
    events = []
    for bar, (first, second) in enumerate(rows):
        events.append(_ev(bar, 240, 1100, first, 86 - bar))
        events.append(_ev(bar, 1680, 1500, second, 74))
    return events


def bass_k03(variation):
    if variation == "a":
        bars = [
            (41, 41, 48, 41),
            (41, 41, 48, 41),
            (36, 36, 43, 36),
            (36, 36, 43, 36),
            (43, 43, 50, 43),
            (43, 43, 50, 43),
            (38, 38, 45, 38),
            (41, 45, 48, 41),
        ]
        events = []
        for bar, pitches in enumerate(bars):
            for index, (tick, pitch) in enumerate(zip((0, 960, 1920, 2880), pitches)):
                events.append(_ev(bar, tick, 640, pitch, 94 if index == 0 else 76))
        return events
    rows = [
        (41, 40, 38, 36, False),
        (41, 43, 45, 43, False),
        (36, 38, 40, 43, False),
        (40, 46, 45, 43, True),
        (43, 45, 47, 50, False),
        (50, 48, 47, 45, False),
        (38, 40, 41, 45, False),
        (48, 45, 43, 41, False),
    ]
    events = []
    for bar, (a, b, c, d, depart) in enumerate(rows):
        events.append(_ev(bar, 480, 360, a, 80))
        events.append(_ev(bar, 1440, 360, b, 84, depart))
        events.append(_ev(bar, 2400, 360, c, 78))
        events.append(_ev(bar, 3360, 360, d, 72))
    return events


def bass_k04(variation):
    if variation == "a":
        bars = [(35, 42, 35), (35, 42, 35), (31, 38, 31), (31, 38, 31), (28, 35, 28), (28, 35, 28), (30, 37, 30), (30, 37, 30)]
        events = []
        for bar, pitches in enumerate(bars):
            for tick, pitch, vel in zip((240, 1680, 3120), pitches, (90, 78, 84)):
                events.append(_ev(bar, tick, 380, pitch, vel))
        return events
    pairs = [
        (35, 42, False),
        (38, 35, False),
        (31, 38, False),
        (35, 31, False),
        (28, 35, False),
        (31, 28, False),
        (30, 37, False),
        (37, 35, False),
    ]
    events = []
    for bar, (first, second, depart) in enumerate(pairs):
        events.append(_ev(bar, 0, 1600, first, 88, depart))
        events.append(_ev(bar, 1920, 1600, second, 76))
    return events


K01_LEAD_A = [
    (0, 0, 1800, 74, 78),
    (0, 1920, 1800, 78, 84),
    (1, 0, 2760, 81, 90),
    (2, 0, 840, 79, 86),
    (2, 960, 840, 78, 82),
    (2, 1920, 1800, 76, 74),
    (3, 0, 3600, 74, 70),
    (4, 0, 840, 71, 80),
    (4, 960, 840, 73, 84),
    (4, 1920, 1800, 74, 88),
    (5, 0, 3600, 78, 92),
    (6, 0, 1800, 76, 76),
    (6, 1920, 1800, 74, 72),
    (7, 0, 3600, 69, 68),
]
K01_LEAD_B = [
    (0, 480, 360, 76, 70), (0, 960, 360, 74, 74), (0, 1440, 720, 78, 80), (0, 2400, 900, 81, 86),
    (1, 0, 480, 78, 82), (1, 720, 480, 76, 76), (1, 1440, 1200, 74, 70), (1, 2880, 480, 73, 66),
    (2, 480, 900, 71, 72), (2, 1920, 1400, 69, 68),
    (3, 0, 1800, 66, 64), (3, 2400, 900, 69, 70),
    (4, 240, 700, 73, 78), (4, 1200, 700, 74, 82), (4, 2160, 1200, 78, 86),
    (5, 0, 900, 81, 90), (5, 1440, 480, 78, 80), (5, 2160, 960, 76, 74),
    (6, 480, 1400, 74, 72), (6, 2400, 900, 71, 68),
    (7, 960, 1800, 69, 64),
]
K02_LEAD_A = [
    (0, 960, 840, 72, 82), (0, 1920, 840, 74, 86), (0, 2880, 840, 76, 90),
    (1, 0, 1440, 79, 92), (1, 1920, 1440, 76, 80),
    (2, 960, 720, 74, 78), (2, 1920, 720, 72, 74), (2, 2880, 800, 69, 70),
    (3, 0, 3000, 71, 74),
    (4, 480, 960, 69, 80), (4, 1680, 960, 72, 84), (4, 2880, 800, 76, 88),
    (5, 0, 1800, 78, 90), (5, 2400, 1200, 76, 78),
    (6, 960, 1400, 76, 74), (6, 2880, 800, 74, 70),
    (7, 480, 1400, 72, 68), (7, 2400, 1200, 69, 64),
]
K02_LEAD_B = [
    (0, 0, 2700, 69, 70),
    (1, 960, 1800, 72, 76),
    (2, 0, 3400, 76, 82),
    (3, 480, 1800, 74, 74), (3, 2640, 900, 71, 68),
    (4, 0, 3600, 67, 64),
    (5, 0, 1440, 73, 80, True), (5, 1920, 1400, 71, 72),
    (6, 240, 900, 72, 74), (6, 1440, 1200, 76, 78), (6, 3000, 700, 74, 70),
    (7, 480, 2700, 69, 66),
]
K03_LEAD_A = [
    (0, 480, 1200, 77, 84), (0, 1920, 1100, 84, 92), (0, 3120, 700, 81, 86),
    (1, 0, 1400, 79, 80), (1, 1920, 1400, 76, 74),
    (2, 480, 900, 71, 78), (2, 1680, 900, 76, 82), (2, 2880, 840, 79, 86),
    (3, 0, 1800, 81, 88), (3, 2400, 1200, 77, 76),
    (4, 240, 700, 74, 80), (4, 1200, 700, 71, 74), (4, 2160, 1400, 67, 68),
    (5, 480, 2700, 72, 72),
    (6, 0, 900, 76, 84), (6, 1440, 900, 74, 78), (6, 2880, 840, 72, 70),
    (7, 0, 1800, 69, 74), (7, 2400, 1200, 65, 66),
]
K03_LEAD_B = [
    (0, 0, 800, 65, 70), (0, 960, 800, 67, 74), (0, 1920, 800, 69, 78), (0, 2880, 800, 71, 82),
    (1, 0, 800, 72, 84), (1, 960, 800, 71, 80), (1, 1920, 800, 69, 76), (1, 2880, 800, 67, 72),
    (2, 0, 800, 72, 78), (2, 960, 800, 74, 82), (2, 1920, 800, 76, 86), (2, 2880, 800, 77, 88),
    (3, 0, 800, 76, 84), (3, 960, 800, 74, 80), (3, 1920, 800, 72, 76), (3, 2880, 800, 69, 74),
    (4, 480, 1400, 79, 80), (4, 2160, 1400, 77, 76),
    (5, 0, 1800, 76, 72), (5, 2400, 1200, 74, 68),
    (6, 240, 1200, 72, 74), (6, 1680, 1600, 71, 78),
    (7, 0, 1600, 69, 70), (7, 1920, 1600, 65, 64),
]
K04_LEAD_A = [
    (0, 1920, 1600, 74, 76),
    (1, 0, 1400, 73, 72), (1, 1920, 1600, 71, 68),
    (2, 960, 1800, 67, 64),
    (3, 0, 2800, 69, 70),
    (4, 1920, 1400, 76, 80),
    (5, 480, 1800, 74, 74),
    (6, 0, 900, 73, 70), (6, 1440, 1800, 71, 66),
    (7, 960, 2200, 66, 60),
]


def lead_k04_b():
    cells = [
        [71, 74, 78, 76],
        [74, 71, 69, 67],
        [67, 69, 71, 74],
        [76, 74, 71, 69],
        [66, 69, 73, 71],
        [73, 71, 69, 66],
        [71, 74, 76, 78],
        [74, 71, 67, 66],
    ]
    events = []
    for bar, pitches in enumerate(cells):
        for tick, pitch, vel in zip((480, 1440, 2400, 3360), pitches, (72, 80, 86, 74)):
            events.append(_ev(bar, tick, 340, pitch, vel + (bar % 3)))
    return events


def pad_k01(variation):
    if variation == "a":
        return _hold(K01_PAD, 0, 7400, (46, 52, 58, 50))
    groups = [
        ([62, 69, 73], [66, 69, 74]),
        ([62, 69, 73], [66, 69, 74]),
        ([55, 62, 66], [59, 62, 67]),
        ([55, 62, 66], [59, 62, 67]),
        ([59, 66, 69], [62, 66, 71]),
        ([59, 66, 69], [62, 66, 71]),
        ([57, 64, 66], [61, 64, 69]),
        ([57, 64, 66], [61, 64, 69]),
    ]
    events = []
    for bar, (early, late) in enumerate(groups):
        for pitch, velocity in zip(early, (42, 48, 54)):
            events.append(_ev(bar, 480, 1100, pitch, velocity))
        for pitch, velocity in zip(late, (44, 50, 56)):
            events.append(_ev(bar, 2400, 1000, pitch, velocity))
    return events


def pad_k02(variation):
    if variation == "a":
        return _pad_beat3([
            [57, 64, 67],
            [57, 60, 64],
            [55, 62, 64],
            [55, 59, 64],
            [54, 60, 64],
            [54, 57, 64],
            [52, 59, 62],
            [52, 55, 59],
        ])
    events = []
    for start_bar, _span, pitches, _name, _spelling in K02_KEYS:
        for pitch, velocity in zip(pitches, (40, 48, 56, 52)):
            events.append(_ev(start_bar, 240, 2800, pitch, velocity))
    return events


def pad_k03(variation):
    if variation == "a":
        events = []
        for start_bar, span, pitches, _name, _spelling in K03_PAD:
            dur = 7400 if span == 2 else 3600
            for pitch, velocity in zip(pitches, (48, 54, 60)):
                events.append(_ev(start_bar, 0, dur, pitch, velocity))
        return events
    voicings = [
        [53, 60, 71],
        [57, 64, 71],
        [60, 64, 67],
        [60, 67, 71],
        [55, 62, 64],
        [59, 64, 67],
        [50, 57, 60],
        [53, 57, 65],
    ]
    events = []
    for bar, pitches in enumerate(voicings):
        for pitch, velocity in zip(pitches, (46, 52, 58)):
            events.append(_ev(bar, 960, 1800, pitch, velocity))
    return events


def pad_k04(variation):
    if variation == "a":
        return _hold(K04_PAD, 960, 2200, (44, 50, 56, 62))
    pairs = [
        ([59, 66], [62, 69]),
        ([71, 74], [69, 73]),
        ([55, 62], [59, 66]),
        ([67, 71], [64, 69]),
        ([52, 59], [55, 62]),
        ([64, 71], [67, 71]),
        ([54, 61], [57, 64]),
        ([70, 73], [66, 71]),
    ]
    events = []
    for bar, (early, late) in enumerate(pairs):
        for index, pitch in enumerate(early):
            departure = bar == 7 and pitch == 70
            events.append(_ev(bar, 0, 640, pitch, 48 + index * 6, departure))
        for index, pitch in enumerate(late):
            events.append(_ev(bar, 1920, 640, pitch, 52 + index * 4))
    return events


def keys_k04_a():
    cells = [
        [59, 66, 62, 59],
        [62, 69, 66, 62],
        [55, 62, 59, 55],
        [59, 66, 62, 59],
        [52, 59, 55, 52],
        [55, 62, 59, 55],
        [54, 61, 57, 54],
        [57, 64, 61, 57],
    ]
    events = []
    for bar, pitches in enumerate(cells):
        for tick, pitch, vel in zip((0, 960, 1920, 2880), pitches, (70, 82, 76, 68)):
            events.append(_ev(bar, tick, 760, pitch, vel))
    return events


def keys_k04_b():
    pa