# Echoes of Life: instructions for Claude

This repository runs the Echoes of Life TikTok channel for Igor. Claude produces the videos;
Igor posts them by hand. Talk to Igor in Brazilian Portuguese; everything in the videos,
captions and hashtags is in English.

Read `PLAYBOOK.md` before writing anything: it holds the channel identity and the rules learned
from the metrics. `pauta.json` is the idea backlog, `log.json` records every video produced.

## Setup (every run starts on a fresh machine)

1. Clone this repo into `/home/claude/echoes-of-life` if it is not there (attach
   `IgorGMendonca/echoes-of-life` with push access first), `cd` into it and run `./setup.sh`.
2. The task prompt gives `ELEVEN_KEY` and `PIXABAY_KEY`. Write them only to
   `/home/claude/.secrets/echoes.env` (mode 600, outside the repo) and load them with
   `set -a; . /home/claude/.secrets/echoes.env; set +a`. Never write a key into the repo, a commit,
   a message or a log.
3. Run every tool from the repo root; video folders are `videos/<slug>/`.

## Daily production

1. **Pick the date.** Get today's date in America/Sao_Paulo. Of tomorrow and the day after, take
   the first date that has no video in `log.json`. If both are covered, send Igor one short line
   and stop. Produce two videos for that date: the next `todo` idea with `"format": "short"`
   (posting slot 14:00) and the next `todo` with `"format": "long"` (slot 21:00), in list order.
2. **Number them.** Slugs continue from the highest in `log.json`: `v002`, `v003`, ...
   Upload name: `echoes_<slug>_<3-5 word kebab of the hook>`.
3. **For each video** (short first):
   1. Write `videos/<slug>/script.json` in the shape of `videos/v001/script.json`, adding
      `"format": "short"|"long"`. Line 0 is the hook exactly as it will be shown. Follow the
      lengths in PLAYBOOK.md (short 80–100 words / 7–9 lines, long 150–175 words / 13–17 lines).
      Every line gets a footage `query` and `alt`: 2–3 words naming something filmable
      ("empty kitchen morning", "old man window"), never a feeling. Keep the same voice block.
      The post caption is one line that adds to the video plus a question; 4–5 hashtags ending
      with `#echoesoflife`; `"ai_label": true`.
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
4. **Deliver.** Send both upload files with SendUserFile (status `proactive`), then one
   SendUserMessage in Portuguese with, for each video: the date and time to post, the caption
   and hashtags in a code block ready to paste, and the reminder to turn on "Conteúdo gerado por
   IA". Keep it short.
5. **Record.** Set the two ideas in `pauta.json` to `"status": "done", "slug": "<slug>"`, append
   both to `log.json` (same fields as v001), commit only scripts, scenes and the json files
   (media is git-ignored) with a message like `Add v002, v003 for 2026-11-25`, and push to `main`.

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
   least 14 remain, alternating long and short.
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
- Every post is labelled AI-generated (synthetic voice).

## Errors

- Retry a failing step once. If it fails again, finish the other video if you can, deliver it,
  and tell Igor in Portuguese what failed and what he can do.
- ElevenLabs `quota_exceeded`, `payment_required` or similar: stop, tell Igor the voice credits
  ran out (the free plan has 10,000 credits a month; a short video uses about 500, a long one
  about 900), and do not deliver videos without narration.
- Never weaken the checks in `tools/finish.py` to make a video pass.
- Commit messages end with `Co-Authored-By: Claude <noreply@anthropic.com>`.
