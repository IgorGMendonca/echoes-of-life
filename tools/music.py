"""Compose a slow, bittersweet piano + strings bed and render it with FluidSynth.

Usage: python3 music.py <out.wav> <seconds> [seed] [swell_at_seconds]
The piece is generated fresh from the seed (key, progression and melody vary),
so every video can get its own original track. Nothing here is licensed from anyone.
"""
import math, os, random, subprocess, sys, tempfile
import mido

out, seconds = sys.argv[1], float(sys.argv[2])
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
swell_at = float(sys.argv[4]) if len(sys.argv) > 4 else seconds * 0.78
rng = random.Random(seed)
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

# chord tones as semitones above the key's tonic (major key, vi-IV-I-V family)
CHORDS = {
    "I": [0, 4, 7, 11], "I/3": [4, 7, 12, 14], "ii": [2, 5, 9, 12], "iii": [4, 7, 11, 14],
    "IV": [5, 9, 12, 16], "V": [7, 11, 14, 17], "Vsus": [7, 12, 14, 17], "vi": [9, 12, 16, 19],
}
PROGRESSIONS = [
    ["IV", "I/3", "vi", "V", "IV", "I/3", "ii", "Vsus", "IV", "vi", "IV", "I"],
    ["vi", "IV", "I", "V", "vi", "IV", "I/3", "Vsus", "IV", "iii", "IV", "I"],
    ["I", "iii", "vi", "IV", "I", "iii", "IV", "Vsus", "vi", "IV", "ii", "I"],
]
prog = rng.choice(PROGRESSIONS)
key = rng.choice([0, 2, 5, 7, -3])          # C, D, F, G, A-flat-ish range
bars = len(prog)
bar_sec = seconds / (bars - 0.25)            # last chord rings to the end
bpm = 240 / bar_sec
tpb = 480
mid = mido.MidiFile(ticks_per_beat=tpb)
tempo = mido.bpm2tempo(bpm)

piano, strings = mido.MidiTrack(), mido.MidiTrack()
mid.tracks += [piano, strings]
piano.append(mido.MetaMessage("set_tempo", tempo=tempo))
piano.append(mido.Message("program_change", channel=0, program=0))
strings.append(mido.Message("program_change", channel=1, program=49))
piano.append(mido.Message("control_change", channel=0, control=7, value=110))
strings.append(mido.Message("control_change", channel=1, control=7, value=70))

events = []  # (tick, channel, type, a, b)
beat = tpb
bar_t = 4 * beat
swell_bar = min(bars - 2, int(swell_at / bar_sec))


def hum(t):
    return max(0, t + rng.randint(-18, 18))


def vel(v):
    return max(1, min(127, v + rng.randint(-5, 5)))


melody_prev = None
for b, name in enumerate(prog):
    t0 = b * bar_t
    tones = [key + x for x in CHORDS[name]]
    root = key + CHORDS[name][0] % 12
    intensity = 1.0 + (0.35 if b >= swell_bar else 0) - (0.2 if b < 2 else 0)
    # pedal
    events += [(t0, 0, "cc", 64, 0), (t0 + 10, 0, "cc", 64, 100)]
    # left hand: low root + fifth, whole bar
    for n in (36 + root % 12, 43 + root % 12):
        events.append((hum(t0), 0, "on", n, vel(int(34 * intensity))))
        events.append((t0 + bar_t - 20, 0, "off", n, 0))
    if b == bars - 1:
        for n in tones:
            events.append((hum(t0 + 30), 0, "on", 60 + n % 12 + (12 if n % 12 < 4 else 0), vel(30)))
            events.append((t0 + int(bar_t * 1.5), 0, "off", 60 + n % 12 + (12 if n % 12 < 4 else 0), 0))
        continue
    # right hand: gentle broken chord, quarter notes (eighths in the swell)
    pattern = [0, 2, 1, 2] if b < swell_bar else [0, 2, 1, 3, 2, 1, 3, 2]
    step = bar_t // len(pattern)
    for k, idx in enumerate(pattern):
        n = 60 + tones[idx % len(tones)] % 12 + (12 if idx == 3 else 0)
        t = hum(t0 + k * step)
        events.append((t, 0, "on", n, vel(int(30 * intensity))))
        events.append((t + step * 2, 0, "off", n, 0))
    # melody from bar 4: one or two long notes high, chord tones, stepwise preference
    if b >= 3:
        cands = sorted({72 + x % 12 for x in tones} | {84 + x % 12 for x in tones if x % 12 < 5})
        if melody_prev:
            cands.sort(key=lambda n: abs(n - melody_prev) + rng.random() * 3)
        n1 = cands[0]
        melody_prev = n1
        events.append((hum(t0 + 6), 0, "on", n1, vel(int(48 * intensity))))
        if rng.random() < 0.55:
            events.append((t0 + 2 * beat - 30, 0, "off", n1, 0))
            n2 = rng.choice([c for c in cands[:3] if c != n1] or [n1])
            events.append((hum(t0 + 2 * beat + 6), 0, "on", n2, vel(int(42 * intensity))))
            events.append((t0 + bar_t - 30, 0, "off", n2, 0))
            melody_prev = n2
        else:
            events.append((t0 + bar_t - 30, 0, "off", n1, 0))
    # strings pad from bar 5
    if b >= 4:
        for n in (48 + tones[0] % 12, 55 + tones[1] % 12, 60 + tones[2] % 12):
            events.append((t0, 1, "on", n, 40 if b < swell_bar else 58))
            events.append((t0 + bar_t - 5, 1, "off", n, 0))

# string expression: slow rise into the swell, fall at the end
for b in range(4, bars):
    v = 40 + int(60 * max(0, min(1, (b - 4) / max(1, swell_bar - 4))))
    if b == bars - 1:
        v = 55
    events.append((b * bar_t, 1, "cc", 11, v))

events.sort(key=lambda e: (e[0], 0 if e[2] == "off" else 1))
last = {0: 0, 1: 0}
for t, ch, kind, a, b2 in events:
    track = piano if ch == 0 else strings
    delta = t - last[ch]
    last[ch] = t
    if kind == "on":
        track.append(mido.Message("note_on", channel=ch, note=a, velocity=b2, time=delta))
    elif kind == "off":
        track.append(mido.Message("note_off", channel=ch, note=a, velocity=0, time=delta))
    else:
        track.append(mido.Message("control_change", channel=ch, control=a, value=b2, time=delta))

tmp = tempfile.mkdtemp()
midi_path = os.path.join(tmp, "bed.mid")
raw = os.path.join(tmp, "raw.wav")
mid.save(midi_path)
subprocess.run(["fluidsynth", "-ni", "-q", "-g", "0.7", "-r", "48000",
                "-o", "synth.reverb.room-size=0.85", "-o", "synth.reverb.level=0.8",
                "-o", "synth.reverb.width=1.0", "-o", "synth.reverb.damp=0.4",
                "-F", raw, SF2, midi_path], check=True)
fade_out = 2.2
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af",
                f"highpass=f=55,lowpass=f=5200,aecho=0.85:0.6:70|140:0.22|0.12,"
                f"atrim=0:{seconds},afade=t=in:d=1.2,afade=t=out:st={seconds - fade_out}:d={fade_out},"
                f"loudnorm=I=-20:TP=-2:LRA=11",
                "-ar", "48000", "-ac", "2", out], check=True)
print(f"bpm {bpm:.1f} key {key} prog {' '.join(prog)} -> {out}")
