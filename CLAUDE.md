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
- One-shot and nostalgia edits, and footage choices: `cinematic-video-direction`.
- Picking and framing themes for teens and young adults: `gen-z-emotional-insights`.
- ElevenLabs settings, casting and checking the narration: `voice-direction`.
- Before delivering: `video-quality-review` as the final gate. Score its rubric for each video,
  revise anything under 7 and say what you changed.
- `video-director`, `sound-design`, `image-generation` and the Remotion skills (fetched by
  `setup.sh`) are for work built in Remotion or with generated images; use their craft rules, not
  their pipelines, unless Igor asks. Their scripts that need OpenRouter, OpenAI, Gemini or other keys
  are not configured here; do not run them.
- `docs/skill-kit-prompt.md` (the four-video batch) and `docs/brief-2026-11-24-stoic-direction.md`
  (the Stoic direction, formats and music direction) are Igor's briefs, written for the working name
  "The Unspoken"; the channel is Echoes of Life. Where they differ from this file, this file wins.

## Setup (every run starts on a fresh machine)

1. Clone this repo into `/home/claude/echoes-of-life` if it is not there (attach
   `IgorGMendonca/echoes-of-life` with push access first), `cd` into it and run `./setup.sh`.
2. The task prompt gives `ELEVEN_KEY` and `PIXABAY_KEY`. Write them only to
   `/home/claude/.secrets/echoes.env` (mode 600, outside the repo) and load them with
   `set -a; . /home/claude/.secrets/echoes.env; set +a`. Never write a key into the repo, a commit,
   a message or a log.
3. Run every tool from the repo root; video folders are `videos/<slug>/`.

## Daily production

Four videos a day. Since 2026-11-25 the lineup follows the pilots Igor approved on 2026-11-24
(v007 and v008: "vamos seguir esse padrão"):

| Slot (Brasília) | Video | Idea from `pauta.json` (next `todo`, list order) |
|---|---|---|
| 11:00 | one-shot edit, feeling behind (like v007) | `"format": "oneshot"` |
| 14:00 | long, philosophical essay (like v008) | `"format": "long", "kind": "philosophy"` |
| 18:00 | short edit, nostalgia (tilt-up reveal, like v006) | `"format": "ambient", "mood": "nostalgia"` |
| 21:00 | long, story (fiction) | `"format": "long", "kind": "story"` |

The two short formats differ on purpose (the brief asks for more than one visual model, and the
weekly analysis compares them). Ideas with `"status": "parked"` are never picked.

Every `script.json` carries `"post": {"search_phrase", "keywords": [two related ones], …}` and
follows PLAYBOOK.md "Search and hashtags": the search phrase starts the caption's first line and
shows up on screen early (and in the first spoken line of a long video); hashtags come from that
section's sets, never #fyp, #foryou or #viral.

0. **Metrics first.** Before producing, read how the posted videos are doing: Windsor.ai
   connector `tiktok_organic`, `get_data` with the fields listed at the top of
   `tools/early_read.py` and `date_preset` "last_7dT". Save the result as it came to
   `metrics/raw_<UTC date and time>Z.json` and run `python3 tools/early_read.py <that file>`: it
   matches the videos to `log.json` (writing `tiktok_id`), appends a dated snapshot to
   `metrics.json` (so every video gets readings at about 1, 3 and 7 days) and prints a table of
   hours since posting, views per hour, average watch as a share of the length, full-watch rate,
   and likes, comments, shares, saves and follows per 100 views. Give Igor one line from it in the
   delivery message. Early numbers on a new account are hints, not rules: they may steer the
   choice among the next ideas and hooks, never the lineup; the weekly analysis decides that. If
   the connector fails, say so in one line and go on with production.
1. **Pick the date.** Get the current date and time in America/Sao_Paulo. Candidates, in order:
   today (only if it is before 09:00, so the 11:00 slot is still reachable), tomorrow, the day
   after. Take the first candidate that has no video in `log.json` in one of the four regular slots
   (videos whose `slot` starts with "extra" do not count: Igor sometimes asks for one more). If all
   are covered, send Igor one short line and stop.
2. **Number them.** Slugs continue from the highest in `log.json`, in slot order (11:00, 14:00,
   18:00, 21:00). Upload name: `echoes_<slug>_<3-5 word kebab of the line, hook or scene>`.
3. **Order of work.** Make the two short videos first (they need no voice credits), then the
   philosophy essay, then the story.
4. **One-shot edit (11:00)**, no narration:
   1. Write `videos/<slug>/script.json` in the shape of `videos/v007/script.json`:
      `"format": "oneshot"`, `"mood": "behind"`, the idea's `setting` as `theme`, and `"stack"` with
      the idea's `line` one word per entry, lowercase, each ending with a period (6–12 words). The
      line is ours: a principle worth keeping, in plain modern English; keep its Stoic idea and work
      in `"philosophy": {"idea", "source", "use": "interpretation in our own words, not a quote"}`.
      Three honest lines in `"hooks_considered"`. Post fields: a caption that adds the idea behind the
      line plus a question, 4–5 hashtags ending with `#echoesoflife`, `"pinned_comment"`;
      `"music_free": true`; `ai_label` only if the footage looks AI-made.
   2. `python3 tools/footage_candidates.py videos/<slug> 6 3800` (4K) with two or three queries for
      the idea's scene. Pick ONE real shot (check the tags for "ai generated"): a person standing
      still or walking slowly while the world moves (trains, crowds, traffic, waves, mist), or a
      quiet human scene, with a calm dark area where the words can sit. No faces to camera, no
      text, logos or nudity, nothing used in the last 20 videos. Pull full-width frames at three
      times to see where the subject goes, then choose `src_start`, `dur` (6–8 s) and `fx` so the
      subject never crosses the words.
   3. `footage/scenes.json` in the shape of `videos/v007/footage/scenes.json` (one entry,
      `"shake": 0`). Place the stack: left-aligned at `"x"` 0.07–0.12 (or a right column), `"y"` so
      the block ends above 0.82 of the height, `"size"` 54; add `"shade"` when the background behind
      the words is bright. Then `python3 tools/fetch_clips.py videos/<slug>` and
      `python3 tools/oneshot.py videos/<slug>`.
   4. Pull frames at 0.0 s, the middle and the end, and Read them: the whole line readable on the
      very first frame, the subject clear of the words, nothing awkward. Adjust and render again;
      then `finish.py videos/<slug> <upload name>` (must exit 0).
   5. Sound: 2–3 picks (soft sung or instrumental, see the music direction in the brief): title,
      artist, why it fits and where to start it. Say when you could not verify that a song is in the
      TikTok library. Never put them in the file.
5. **Nostalgia edit (18:00)**, no narration:
   1. Write `videos/<slug>/script.json` in the shape of `videos/v006/script.json`: the idea's
      `setting` becomes `theme`; its `text` becomes `"text": {"line", "from", "to", "y"}` (one
      short lowercase line, shown after the lift; every nostalgia edit has one since Igor's
      decision of 2026-11-25, so write one in the same spirit when the idea has none); one entry in `lines` per shot
      with an empty `text` and a footage `query`/`alt`; `"mood"` from the idea; three honest
      ideas for the line or caption in `"hooks_considered"`; the post fields as in PLAYBOOK.md
      "Nostalgia edits" (`ai_label` only if the footage looks AI-made).
   2. `python3 tools/footage_candidates.py videos/<slug> 6 3800` (4K only) with one query for the
      view and one for the ground ("asphalt road", "wet street reflections", "leaves on road").
      Pick ONE beautiful 4K view with real, natural motion and life in it that fits the mood
      and one ground clip whose light suits the view. Nothing used in the last 20 videos, no
      billboards, logos or people facing the camera. The view needs a calm area (sky, a dark
      wall, water) where the line stays clear of the subject in the 9:16 crop; if the subject
      fills the frame, choose other footage, never drop the line. Pull a frame at two times from
      the view to rule out timelapses.
   3. Write `footage/scenes.json` in the shape of `videos/v006/footage/scenes.json` (a `"ground"`
      entry and a `"view"` entry with `"fx"` framing the subject, `"dur"` 7–10 s, `"shake"` about 8;
      `"fx_to"` only for a slow follow) and add `"reveal": {"at": 0.55, "dur": 0.7}` and
      `"music_free": true` to script.json. Then `python3 tools/fetch_clips.py videos/<slug>` and
      `python3 tools/ambient.py videos/<slug>`.
   4. Sound: search the web once per run for this week's trending TikTok sounds (several chart
      sources) and pick 2–3 soft, sung songs that fit; for each give title, artist and where to
      start it (the first sung line or a beat on the camera lift, about 0.6–1.2 s).
   5. `python3 tools/reveal.py videos/<slug>` renders it. Pull frames every 0.1 s over the first
      2 s and one at the end, and Read them: the ground, a blurred lift, the subject well framed,
      the text clear of the subject and readable. Adjust `fx`, `eq`, text `y`/`from` or the
      reveal timing and render again; then `finish.py videos/<slug> <upload name>` (must exit 0).
6. **Long videos** (philosophy and story), for each:
   1. Write `videos/<slug>/script.json` in the shape of `videos/v008/script.json`, with
      `"format": "long"` and `"kind": "philosophy"|"story"`. Line 0 is the hook exactly as it will
      be shown (it is on screen from the first frame). Length: 165–195 words in 14–19 lines (about
      70–85 s read in one take; v008 had 181 words and ran 77.7 s; `finish.py` accepts 64–91 s).
      Add `"bed": "none"`: the file carries the voice alone and Igor adds an instrumental from the
      TikTok library (his decision, 2026-11-24). Every line gets a
      footage `query` and `alt`: 2–3 words naming something filmable ("empty kitchen morning",
      "old man window"), never a feeling. Plan the light as an arc: night and blue while the
      feeling is heavy, warm daylight once the thought turns. Keep the same voice block. The post
      caption is one line that adds to the video plus a question; 4–5 hashtags ending with
      `#echoesoflife`; `"ai_label": true`. Follow "Engagement" in PLAYBOOK.md: add
      `"post.pinned_comment"` and `"endcard"` (a save or share invitation when it fits, otherwise
      "follow for more").
      - **Philosophy:** a feeling from the idea (feeling behind, comparison, time anxiety…) seen
        through a Stoic text, in the order of v008: the hook, a modern scene, what the philosopher
        said, what it means and what it does not mean, one small thing to do tonight, a closing
        line. Before writing, find the passage named in the idea's `stoic` lead (only a lead) in a
        public-domain translation online (Wikisource, Project Gutenberg, Perseus or a reliable
        reprint: Basore or Gummere for Seneca, Oldfather or Higginson for Epictetus, Long for
        Marcus Aurelius). Quote at most one short passage, word for word, and say who wrote it
        and where; everything else is our paraphrase or interpretation. Record each in
        `"philosophy": [{"type": "quote"|"paraphrase"|"interpretation", "text", "work",
        "translation", "checked": [urls]}]`. If the passage cannot be found, do not quote: paraphrase
        and mark it. Never attribute a modern saying to a philosopher; "amor fati" is Nietzsche's
        phrase, not the Stoics'. Stoicism here is perspective and calm, never coldness, bottled-up
        feelings, isolation, hustle or toughness; memento mori stays gentle, never morbid. Any
        psychology claim needs a credible source in `"sources"` (peer-reviewed paper, university,
        APA or national health service page), said carefully, or it is cut.
      - **Story:** one specific character and moment, a real emotional shift and a satisfying,
        hopeful ending. Say it is a story in the video ("This is a story about…") and add
        `"fiction": true`. A Stoic idea may sit underneath, never as a lecture.
   2. `python3 tools/tts.py videos/<slug>` reads the whole script in one take (exit code 2 =
      ElevenLabs refused: see Errors). Never stitch separately generated sentences with silence
      between them: Igor heard that as the audio stalling after every sentence (v008). If a
      sentence comes out wrong, fix the text (a comma gives the voice a breath) and generate the
      whole take again.
   3. `python3 tools/footage_candidates.py videos/<slug> 4`, then Read every
      `footage/sheet_XX.jpg`. For each line pick the clip that shows what the line says, looks
      cinematic and fits the grade and the light arc. Reject: visible text, logos, watermarks, UI,
      cartoon/3D unless the whole video is illustrated, people talking to camera, nudity (classical
      statues included), anything sexual, violent or medical, and any `pixabay_id` used in the last
      20 entries of `log.json`. Prefer real footage; check the tags for "ai generated". If nothing
      fits, change that line's query and search again (edit script.json, re-run).
   4. Write `videos/<slug>/footage/scenes.json`, one entry per line, in the shape of
      `videos/v008/footage/scenes.json`: `pixabay_id`, `src_start` (skip the first second),
      `fx` (0–1 horizontal crop centre that keeps the subject in the 9:16 frame; check the clip at
      full width, the thumbnail is not the whole clip), `zoom` 0.04–0.06, optional `eq` to darken
      bright daylight clips, `"zoom_out": true` on the last. Then
      `python3 tools/fetch_clips.py videos/<slug>`. Check each clip is long enough for its scene
      (`timeline.json` cuts + 0.5 s) and move `src_start` if not.
   5. `python3 tools/timeline.py videos/<slug>`; note `total`.
   6. No music in the file. Pick 2–3 calm instrumental songs for the delivery (the brief's music
      direction or this week's TikTok charts): title, artist, why it fits, where to start; say when
      you could not verify that a song is in the TikTok library.
   7. Review before the full render: `python3 tools/render.py videos/<slug> frames 1.8 <a time in
      every scene> <total-1.2>`, Read the stills. The subject must be in frame, captions
      readable, nothing awkward. Fix `fx`/`eq`/clip and look again.
   8. `python3 tools/render.py videos/<slug> full` (one full render per video).
   9. `python3 tools/finish.py videos/<slug> <upload name>` must exit 0; it makes the upload
      copy and `post.txt` and checks size, fps, −14 LUFS, true peak and duration.
7. **Quality gate.** Run the `video-quality-review` rubric on each finished file (frames at start,
   middle, end and every cut) and fix anything under 7 before delivering.
8. **Deliver.** Send the four upload files with SendUserFile (status `proactive`), then one
   SendUserMessage in Portuguese with, for each video in slot order: the date and time to post,
   the caption and hashtags in a code block ready to paste, the pinned comment in its own code
   block (post it as the first comment and pin it), the reminder to turn on "Conteúdo gerado por
   IA" when `ai_label` is true, and the 2–3 sound picks for every video with their start point
   (he adds the song in the app; under the long videos he sets the added sound to about 15–20% and
   the original sound to 100%), and the three keywords to suggest under "Manage keywords" once
   the video is up (the search phrase and the two related ones). For the philosophy essay add
   one line naming the text, section and translation (and any psychology source), so Igor can
   answer comments. Keep it short.
9. **Record.** Set the four ideas in `pauta.json` to `"status": "done", "slug": "<slug>"`, append
   all four to `log.json` (same fields as v006, v007 and v008, with `kind` or `mood`, and the
   `philosophy` and `sources` entries for the essay), commit only scripts, scenes, the json files
   and `metrics/` (media is git-ignored) with a message like `Add v009–v012 for 2026-11-25`, and
   push to `main`.

## Other tools

- **Draft without voice**: when Igor wants to approve the images first, run
  `python3 tools/draft_voice.py videos/<slug>` instead of `tts.py` (silent lines timed at the
  narrator's measured pace), then `timeline.py`, a silent `audio/music.wav`, `render.py full`, and
  deliver a light copy named `..._PREVIEW-no-voice.mp4` without `finish.py`. Once approved: move
  the draft audio aside, then `tts.py`, `timeline.py`, `render.py full`, `finish.py`.
- `render.py` brings the audio to −14 LUFS with one fixed gain and a limiter. With `"bed": "none"`
  that is the voice alone; older projects without it still mix the generated piano (`music.py`),
  compressed and ducked under the voice.
- `tts.py --per-line [index ...]` is the old one-clip-per-sentence mode, kept only for old
  projects.

## Weekly analysis (Mondays)

1. Use the Windsor.ai connector, connector `tiktok_organic`, account "Echoes of Life". Call
   `get_fields` before `get_data` and use only field names it returns. Read the last 7 and the
   last 30 days: per video views, reach, average watch time, full-watch rate, likes, comments,
   shares, new followers if available, traffic sources and audience countries.
2. Match TikTok videos to `log.json` (`tools/early_read.py` does it by `tiktok_id`, caption, then
   duration) and use the dated snapshots in `metrics.json` to compare videos at the same age
   (about 1, 3 and 7 days). Compare the four kinds, themes, hook styles and posting slots on
   completion rate, average watch time as a share of duration, views, and follows and shares per
   1,000 views; use medians, not the best video.
3. Add 3–6 dated bullets to "Learned" in PLAYBOOK.md, each with its sample size. Draw a
   conclusion only from 3+ videos per group, and mark it tentative until there are two weeks of
   data. Change a starting rule only when two weeks of data contradict it.
4. Reorder the `todo` ideas in `pauta.json` toward what works and add new original ideas so at
   least 7 `todo` ideas remain of each of the four kinds (one-shot, nostalgia edit, long
   philosophy, long story). Compare the four kinds with each other, the one-shot against the
   tilt-up reveal, nostalgia edits by setting and by kind of line, and philosophy
   against stories.
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
