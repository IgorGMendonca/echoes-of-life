# Echoes of Life: instructions for Claude

This repository runs the Echoes of Life TikTok channel for Igor. Claude produces the videos;
Igor posts them by hand. Talk to Igor in Brazilian Portuguese; everything in the videos,
captions and hashtags is in English.

Read `PLAYBOOK.md` before writing anything: it holds the channel identity and the rules learned
from the metrics. `pauta.json` is the idea backlog, `log.json` records every video produced.

## Skills (in `.claude/skills/`)

The pipeline stays Python + ffmpeg (`tools/`); the skills sharpen the writing, the direction and
the review. Read a skill's SKILL.md when its step comes up:

- Writing any script or on-screen line: `emotional-storytelling`, `gen-z-emotional-insights` and
  `scriptwriting` (hooks, structures, writing for the ear, AI-sounding tells). Write three honest
  hooks, pick the best, and keep the other two in `script.json` as `"hooks_considered"`.
- Hooks, pacing and the weekly analysis: `short-form-retention`.
- Short edits (ambient) and footage choices: `cinematic-video-direction`.
- Picking and framing themes for teens and young adults: `gen-z-emotional-insights`.
- ElevenLabs settings, casting and checking the narration: `voice-direction`.
- Before delivering: `video-quality-review` as the final gate. Score its rubric for each video,
  revise anything under 7 and say what you changed.
- `video-director`, `sound-design`, `image-generation` and the Remotion skills (fetched by
  `setup.sh`) are for work built in Remotion or with generated images; use their craft rules, not
  their pipelines, unless Igor asks. Their scripts that need OpenRouter, OpenAI, Gemini or other keys
  are not configured here; do not run them.
- `docs/skill-kit-prompt.md` is Igor's reference brief behind the kit (written for the working name
  "The Unspoken"; the channel is Echoes of Life). Its four-video batch is the daily lineup since
  2026-11-25; where the two differ, this file wins.

## Setup (every run starts on a fresh machine)

1. Clone this repo into `/home/claude/echoes-of-life` if it is not there (attach
   `IgorGMendonca/echoes-of-life` with push access first), `cd` into it and run `./setup.sh`.
2. The task prompt gives `ELEVEN_KEY` and `PIXABAY_KEY`. Write them only to
   `/home/claude/.secrets/echoes.env` (mode 600, outside the repo) and load them with
   `set -a; . /home/claude/.secrets/echoes.env; set +a`. Never write a key into the repo, a commit,
   a message or a log.
3. Run every tool from the repo root; video folders are `videos/<slug>/`.

## Daily production

Four videos a day since 2026-11-25 (Igor's decision): two short edits and two long narrated videos.

| Slot (Brasília) | Video | Idea from `pauta.json` (next `todo`, list order) |
|---|---|---|
| 11:00 | short edit, feeling behind | `"format": "ambient", "mood": "behind"` |
| 14:00 | long, human psychology | `"format": "long", "kind": "psychology"` |
| 18:00 | short edit, nostalgia | `"format": "ambient", "mood": "nostalgia"` |
| 21:00 | long, story (fiction) | `"format": "long", "kind": "story"` |

Ideas with `"status": "parked"` are never picked.

1. **Pick the date.** Get the current date and time in America/Sao_Paulo. Candidates, in order:
   today (only if it is before 09:00, so the 11:00 slot is still reachable), tomorrow, the day
   after. Take the first candidate that has no video in `log.json`. If all are covered, send Igor
   one short line and stop.
2. **Number them.** Slugs continue from the highest in `log.json`, in slot order (11:00, 14:00,
   18:00, 21:00). Upload name: `echoes_<slug>_<3-5 word kebab of the hook or scene>`.
3. **Order of work.** Make the two short edits first (they need no voice credits), then the
   psychology video, then the story.
4. **Short edits** (no narration, no ElevenLabs credits), for each:
   1. Write `videos/<slug>/script.json` in the shape of `videos/v006/script.json`: the idea's
      `setting` becomes `theme`; its `text` (if any) becomes `"text": {"line", "from", "to", "y"}`
      (at most one short lowercase line, shown after the lift); one entry in `lines` per shot
      with an empty `text` and a footage `query`/`alt`; `"mood"` from the idea; three honest
      ideas for the line or caption in `"hooks_considered"`; the post fields as in PLAYBOOK.md
      "Short edits" (`ai_label` only if the footage looks AI-made).
   2. `python3 tools/footage_candidates.py videos/<slug> 6 3800` (4K only) with one query for the
      view and one for the ground ("asphalt road", "wet street reflections", "leaves on road").
      Pick ONE beautiful 4K view with real, natural motion and life in it that fits the mood
      (PLAYBOOK "Short edits") and one ground clip whose light suits the view. Nothing used in the
      last 20 videos, no billboards, logos or people facing the camera. Pull a frame at two times
      from the view to rule out timelapses.
   3. Write `footage/scenes.json` in the shape of `videos/v006/footage/scenes.json` (a `"ground"`
      entry and a `"view"` entry with `"fx"` framing the subject, `"dur"` 7–10 s, `"shake"` about 8;
      `"fx_to"` only for a slow follow) and add `"reveal": {"at": 0.55, "dur": 0.7}` and
      `"music_free": true` to script.json (Igor adds a song on TikTok, so the export carries
      silence). Then `python3 tools/fetch_clips.py videos/<slug>` and
      `python3 tools/ambient.py videos/<slug>`.
   4. Sound: search the web once per run for this week's trending TikTok sounds (several chart
      sources) and pick, for each edit, 2–3 soft, sung songs that fit its mood; for each give
      title, artist and where to start it (the first sung line or a beat on the camera lift, about
      0.6–1.2 s). Never put them in the file.
   5. `python3 tools/reveal.py videos/<slug>` renders it. Pull frames every 0.1 s over the first
      2 s and one at the end, and Read them: the ground, a blurred lift, the subject well framed,
      text (if any) clear of the subject and readable. Adjust `fx`, `eq`, text `y`/`from` or the
      reveal timing and render again; then `finish.py videos/<slug> <upload name>` (must exit 0).
5. **Long videos** (psychology and story), for each:
   1. Write `videos/<slug>/script.json` in the shape of `videos/v002/script.json`, with
      `"format": "long"` and `"kind": "psychology"|"story"`. Line 0 is the hook exactly as it will
      be shown. Length: 165–195 words in 14–19 lines (about 72–86 s with the end card; v002 had
      159 words and ran 71.6 s; `finish.py` accepts 64–91 s). Every line gets a footage `query`
      and `alt`: 2–3 words naming something filmable ("empty kitchen morning", "old man window"),
      never a feeling. Keep the same voice block. The post caption is one line that adds to the
      video plus a question; 4–5 hashtags ending with `#echoesoflife`; `"ai_label": true`. Follow
      "Engagement" in PLAYBOOK.md: add `"post.pinned_comment"` (a second, playful question for
      Igor to pin) and `"endcard"` (a save or share invitation when it fits, otherwise "follow
      for more").
      - **Psychology:** social comparison or time anxiety, unless the idea names another
        well-established topic. Before writing, search the web for credible sources (peer-reviewed
        papers, university, APA or national health service pages) for every factual claim,
        starting from the idea's `research` lead, which is only a lead. Record them in
        `"sources": [{"claim", "title", "url"}]`. Say findings carefully ("psychologists call
        this…", "studies suggest…"); no numbers unless the source gives them; no diagnoses, no
        therapy or medical advice. A claim you cannot source is cut, or the piece becomes openly
        reflective ("Here's a thought…") with `"reflective": true`.
      - **Story:** one specific character and moment, a real emotional shift and a satisfying,
        hopeful ending. Say it is a story in the video ("This is a story about…") and add
        `"fiction": true`.
   2. `python3 tools/tts.py videos/<slug>` (exit code 2 = ElevenLabs refused: see Errors).
   3. `python3 tools/footage_candidates.py videos/<slug> 4`, then Read every
      `footage/sheet_XX.jpg`. For each line pick the clip that shows what the line says, looks
      cinematic and fits the warm, quiet grade. Reject: visible text, logos, watermarks, UI,
      cartoon/3D unless the whole video is illustrated, people talking to camera, anything
      sexual, violent or medical, and any `pixabay_id` used in the last 20 entries of `log.json`.
      If nothing fits, change that line's query and search again (edit script.json, re-run).
   4. Write `videos/<slug>/footage/scenes.json`, one entry per line, in the shape of
      `videos/v001/footage/scenes.json`: `pixabay_id`, `src_start` (skip the first second),
      `fx` (0–1 horizontal crop centre that keeps the subject in the 9:16 frame), `zoom`
      0.04–0.06, optional `eq` to darken bright daylight clips, `"zoom_out": true` on the last.
      Then `python3 tools/fetch_clips.py videos/<slug>`. Check each clip is long enough for its
      scene (`timeline.json` cuts + 0.5 s) and move `src_start` if not.
   5. `python3 tools/timeline.py videos/<slug>`; note `total`.
   6. `python3 tools/music.py videos/<slug>/audio/music.wav <total> <seed> <swell_at>`, with a
      seed not used in `log.json` (e.g. slug number × 13) and `swell_at` = start of the
      second-to-last line.
   7. Review before the full render: `python3 tools/render.py videos/<slug> frames 1.8 <three
      mid-scene times> <total-1.2>`, Read the stills. The subject must be in frame, captions
      readable, nothing awkward. Fix `fx`/`eq`/clip and look again.
   8. `python3 tools/render.py videos/<slug> full` (one full render per video).
   9. `python3 tools/finish.py videos/<slug> <upload name>` must exit 0; it makes the upload
      copy and `post.txt` and checks size, fps, −14 LUFS, true peak and duration.
6. **Quality gate.** Run the `video-quality-review` rubric on each finished file (frames at start,
   middle, end and every cut) and fix anything under 7 before delivering.
7. **Deliver.** Send the four upload files with SendUserFile (status `proactive`), then one
   SendUserMessage in Portuguese with, for each video in slot order: the date and time to post,
   the caption and hashtags in a code block ready to paste, the pinned comment in its own code
   block (post it as the first comment and pin it), the reminder to turn on "Conteúdo gerado por
   IA" when `ai_label` is true, and for the short edits the 2–3 TikTok sound picks with their
   start point (the export is silent; he adds the song in the app). For the psychology video add
   one line naming its sources, so Igor can answer comments. Keep it short.
8. **Record.** Set the four ideas in `pauta.json` to `"status": "done", "slug": "<slug>"`, append
   all four to `log.json` (same fields as v002 and v006, plus `kind` or `mood`, and `sources` for
   psychology), commit only scripts, scenes and the json files (media is git-ignored) with a
   message like `Add v007–v010 for 2026-11-25`, and push to `main`.

## Pilot formats (being validated; not in the daily routine yet)

- **Cinematic One Shot** (5–12 s): one real shot, the whole line on screen from the first frame, one
  word per line. Script in the shape of `videos/v007/script.json` (`"format": "oneshot"`, `"stack"`,
  optional `"shade"`), one entry in `footage/scenes.json`, then `python3 tools/oneshot.py
  videos/<slug>` and `finish.py` (music-free).
- **Draft without voice**: when Igor wants to approve the images first, run
  `python3 tools/draft_voice.py videos/<slug>` instead of `tts.py` (silent lines timed at the
  narrator's measured pace), then `timeline.py`, a silent `audio/music.wav`, `render.py full`, and
  deliver a light copy named `..._PREVIEW-no-voice.mp4` without `finish.py`. Once approved: `tts.py`,
  `timeline.py`, `music.py`, `render.py full`, `finish.py`.
- `docs/brief-2026-11-24-stoic-direction.md` is Igor's brief for the Stoic direction. The daily
  routine changes only after he validates the pilots (v007, v008).

## Weekly analysis (Mondays)

1. Use the Windsor.ai connector, connector `tiktok_organic`, account "Echoes of Life". Call
   `get_fields` before `get_data` and use only field names it returns. Read the last 7 and the
   last 30 days: per video views, reach, average watch time, full-watch rate, likes, comments,
   shares, new followers if available, traffic sources and audience countries.
2. Match TikTok videos to `log.json` by caption text. Compare short vs long, themes, hook styles
   and posting slots on completion rate, average watch time as a share of duration, views, and
   follows and shares per 1,000 views.
3. Add 3–6 dated bullets to "Learned" in PLAYBOOK.md, each with its sample size. Draw a
   conclusion only from 3+ videos per group, and mark it tentative until there are two weeks of
   data. Change a starting rule only when two weeks of data contradict it.
4. Reorder the `todo` ideas in `pauta.json` toward what works and add new original ideas so at
   least 7 `todo` ideas remain of each of the four kinds (short edit behind, short edit nostalgia,
   long psychology, long story). Compare the four kinds with each other, short edits with and
   without the text line and by setting (city, rain, sea, nature…), and stories vs psychology.
5. If more than half the views come from Brazil, say so: the channel is aimed at the US.
6. Commit and push, then send Igor a short Portuguese summary: the key numbers, what worked,
   what changes this week, anything he should do.

## Content rules

- Write everything original. No song lyrics, poems or passages from books, no famous quotes
  attributed to real people, no real private people, no brands.
- Stories are fiction and say so ("This is a story about…", "Imagine…"); never present an
  invented story as something that happened.
- Psychology topics stay general and well established; no diagnoses, no medical or therapy
  advice, no statistics you cannot source.
- Stay away from suicide, self-harm, abuse, eating disorders, politics and real tragedies.
  Loneliness and loss themes always turn toward connection and hope.
- Many viewers are teenagers. Motivation stays healthy: no shaming, no pressure about money,
  looks or bodies, no diet or appearance content, and never frame being "behind" as failure.
- Every narrated post is labelled AI-generated (synthetic voice); short edits only when the
  footage itself is AI-generated.

## Errors

- Retry a failing step once. If it fails again, finish the other video if you can, deliver it,
  and tell Igor in Portuguese what failed and what he can do.
- ElevenLabs `quota_exceeded`, `payment_required` or similar: tell Igor the voice credits ran
  out (a long video uses about 1,000 credits, so the lineup needs about 2,000 a day) and do not
  deliver narrated videos without narration. Still make and deliver the two short edits, which
  need no credits.
- Never weaken the checks in `tools/finish.py` to make a video pass.
- Commit messages end with `Co-Authored-By: Claude <noreply@anthropic.com>`.
