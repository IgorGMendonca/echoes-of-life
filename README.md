# Echoes of Life

Pipeline that turns one idea into a finished vertical video (1080×1920, 30 fps) for the
Echoes of Life TikTok channel: emotional, reflective micro-stories in English, narrated over
cinematic stock footage, with word-timed captions and an original piano bed.

## How a video is made

Each video lives in `videos/<slug>/` and starts from a `script.json`
(see `videos/v001/script.json`): the hook, one entry per narrated line with a footage
search query, the voice, and the post caption and hashtags.

| Step | Command | Output |
|---|---|---|
| 0. Setup (once per machine) | `./setup.sh` | ffmpeg, FluidSynth, soundfont, Python deps |
| 1. Voice | `python3 tools/tts.py videos/<slug>` | `audio/line_XX.mp3` + character timestamps (ElevenLabs) |
| 2. Footage candidates | `python3 tools/footage_candidates.py videos/<slug> 4` | contact sheets `footage/sheet_XX.jpg` (Pixabay) |
| 3. Pick clips | write `footage/scenes.json` (pixabay_id, start, crop, zoom), then `python3 tools/fetch_clips.py videos/<slug>` | `footage/clips/scene_N.mp4` |
| 4. Timeline + captions | `python3 tools/timeline.py videos/<slug>` | `timeline.json`, `captions.ass`, `audio/voice.wav` |
| 5. Music | `python3 tools/music.py videos/<slug>/audio/music.wav <seconds> <seed> <swell_at>` | original piano + strings bed |
| 6. Review stills | `python3 tools/render.py videos/<slug> frames 1.8 7 16 30 39.8` | `review/frame_*.jpg` |
| 7. Render | `python3 tools/render.py videos/<slug> full` | `render/<slug>.mp4` |

| 8. Upload copy + checks | `python3 tools/finish.py videos/<slug> <upload_name>` | `render/<upload_name>.mp4`, `render/post.txt` |

The full procedure Claude follows in the scheduled runs (daily production and the weekly
metrics analysis) is in `CLAUDE.md`; the channel rules are in `PLAYBOOK.md`, the idea backlog in
`pauta.json` and the record of every video in `log.json`.

## Secrets

Never commit keys. The scripts read them from the environment:

- `ELEVEN_KEY`: ElevenLabs key restricted to Text to Speech, Music and Voices (read).
- `PIXABAY_KEY`: Pixabay API key.

## Look and sound

- Grade: slightly desaturated, warm, vignette, light film grain; slow push-in per scene; 0.5 s crossfades.
- Hook: Playfair Display italic, centre; captions: Inter SemiBold 82 px at 64% height, words fill as spoken.
- End card: `library/endcard.png` (echo rings) + "Echoes of Life" / "follow for more".
- Mix: −14 LUFS integrated, true peak ≤ −1 dBFS, music about 10 dB under the voice, ducked by the voice.
- Every post is labelled as AI-generated content (synthetic voice).

## Licences

Footage: Pixabay Content License. Fonts: Playfair Display (SIL OFL 1.1, `library/fonts/OFL.txt`),
Inter (system). Music: composed by `tools/music.py` and rendered with the FluidR3 GM soundfont.
