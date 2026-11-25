# Echoes of Life: playbook

Rules the production runs follow. The weekly analysis updates the "Learned" section from real
metrics; the "Starting rules" stay until the numbers say otherwise.

## Identity

- Name: Echoes of Life. Tagline: "Stories that make you feel. Thoughts that stay with you."
- Language: English. Audience: international, the US first; many viewers are teenagers and young adults.
- Two pillars:
  1. **Time & potential (main, the larger share: the 11:00 edit, the psychology video and half the stories):** for young people who feel late or behind.
     The message is "you are not late, and you can do more than you think: start small, today".
     Empowering and concrete, never shaming, never hustle-toxic (sleep, rest and bad days are allowed),
     no comparisons with real named people, no invented statistics or "he was 22 when..." stories.
     Footage: students at night, sunrise runs, notebooks, trains and roads, city lights, clocks.
     Hashtags draw from #motivation #selfimprovement #growthmindset #studymotivation #discipline.
  2. **Bittersweet reflections:** nostalgia, family, love, loneliness, small moral questions.
- Tone: calm, warm, never preachy, never morbid. Every video ends on something the viewer can do or feel today.
- Look: cinematic stock footage, warm desaturated grade, grain, slow push-ins, serif hook title, word-timed captions, echo-rings end card.

## Daily lineup (from 2026-11-25, Igor's decision)

Four videos a day, posted in Brasília time (New York is 2 hours behind until March):

| Slot | Video | Why |
|---|---|---|
| 11:00 (09:00 NY) | Short edit, feeling behind, 7–15 s | Reach; a calm "you're on your way" before the school or work day |
| 14:00 (12:00 NY) | Long, human psychology, 65–90 s | Social comparison or time anxiety, sourced or openly reflective |
| 18:00 (16:00 NY) | Short edit, nostalgia, 7–15 s | Reach and replays after school |
| 21:00 (19:00 NY) | Long, story, 65–90 s | Fiction with a character, an emotional shift and a hopeful ending |

Long videos stay over 1 minute so they can count for Creator Rewards later. The old 35–45 s
narrated format is retired; its ideas are parked in `pauta.json`.

## Starting rules (hypotheses, not yet proven)

- Hook in the first 2 seconds, 9 words or fewer, shown as the title. It is a statement or a question that hits a universal memory.
- Long videos: 72–86 s, 165–195 words, 14–19 lines (v002: 159 words ran 71.6 s with the end card).
- One scene per line; a cut every 3–6 s.
- Specific images beat abstractions ("the porch light", "your mom's voice at dinner") .
- End with a gentle call to act ("call them today") or a question for the comments.
- Caption: one sentence that adds to the video, plus a question; 4–5 hashtags, always #echoesoflife.
- Posting: see "Daily lineup" above.

## Long videos: psychology and story

- **Psychology (14:00):** social comparison or time anxiety, explained the way a kind older friend
  would. Every factual claim has a credible source found that day (peer-reviewed paper,
  university, APA or a national health service), recorded in `script.json`; say it carefully
  ("psychologists call this…"), name an idea rather than quote a number, and never diagnose or
  advise treatment. Without a solid source, the piece becomes openly reflective. Structure: the
  feeling, why the mind does it, a kinder way to see it, one small thing to do tonight.
- **Story (21:00):** fiction and said to be ("This is a story about…"): one named character, one
  specific moment, an emotional shift, a satisfying and hopeful ending. Half the stories serve the
  main pillar (feeling behind, starting late), half nostalgia. No real people, no tragedies.

## Short edits (ambient; reach and followers)

Two a day, made to be watched to the end and replayed: **feeling behind** at 11:00 (people on
their way: commuters at sunrise, trains, roads, a city waking up, someone walking alone at blue
hour) and **nostalgia** at 18:00 (childhood, family, seasons, small towns, kids playing, warm
windows at dusk; v006 is the model). `pauta.json` marks each idea with its `mood`.

- 7–10 s, no narration, modelled on Igor's reference video (2026-11-24): the phone starts
  pointed at the ground (asphalt, wet pavement with reflections, leaves) for about half a
  second, then is lifted quickly (vertical motion blur) to reveal the view, and holds there by
  hand with a light sway for the rest of the clip. One view, no cuts. `tools/reveal.py` does this.
- The scene itself must touch the heart: golden hour, blue hour, warm city lights, calm water,
  a landmark with something meaningful beside it. Motion is real and natural, never sped up or
  timelapse (check a frame at two times a few seconds apart; if the sky changes fast, skip it).
- Pick a source whose two halves are both worth looking at: the turn should reveal something.
- People make it (Igor, 2026-11-24): prefer street-level scenes with life in them (people walking
  past a lit landmark at blue hour) over empty landscapes. Example: v005, Tokyo Station.
- Avoid shots dominated by billboards or brand logos (e.g. busy crossings full of ads).
- Image quality matters (Igor, 2026-11-24): 4K sources only, no film grain (TikTok's re-encode
  turns it into blur), light sharpening and a high-bitrate upload copy. The tools do this by default.
- About half carry one short lowercase line in Playfair italic (10 words or fewer, shown after
  the lift) that fits the mood ("rest is not falling behind", "someone rode next to you until you
  didn't need them to."); the other half have no text. The analysis compares them.
- Sound: the export is music-free (silent track). Igor adds a soft, sung, currently trending song
  from the TikTok library in the app; each delivery names 2–3 picks with a start point that puts a
  sung line or a beat on the camera lift.
- Caption: a short question tied to the place ("Which city would you watch this from?"). Pinned
  comment: a light prompt such as "What song would you play here? 🎧".
- AI label only when the footage itself looks AI-generated (no synthetic voice in this format).

## Engagement: invite, never beg

Each video carries one invitation that grows out of its own content, so answering feels natural.
Rotate the kind across the week and let the metrics decide which works.

- **Comment:** a question a viewer can answer in a few words, asked in the caption and in the
  pinned comment, sometimes as the final spoken line. Good shapes: "What's one thing you'd
  start tonight?", fill in the blank ("The last time I ___ was…"), A or B dilemmas, "What would you
  tell your 15-year-old self?". Ask about experiences and opinions, never personal details.
- **Save:** for advice-like videos, an end-card line such as "save this for the day you need it".
- **Share:** when someone specific comes to mind, "send this to someone who needs it today".
- **Pinned comment:** Igor posts it as the first comment and pins it. It is a second, more
  playful question than the caption ("What's the story your parents always tell twice? 👇"),
  never a fake personal memory written as if it were Igor's.
- The end card shows the save/share line or "follow for more"; only one call to action per video.
- Never: "like if you agree", "comment YES", "type 1 for…", follow-for-follow, like-for-like,
  fake "part 2" promises, false urgency, or asking for age, school, location or other personal
  information (many viewers are teenagers). TikTok treats fake engagement as ineligible for the
  For You feed, and forced asks also feel cheap.
- Keep the mood mostly hopeful: a channel of only sad videos risks being shown less, and the
  endings should leave people lighter than they arrived.

## Pilots in validation (2026-11-24)

Igor's brief of 2026-11-24 (`docs/brief-2026-11-24-stoic-direction.md`) points the channel toward
"modern philosophy for a generation that feels lost": emotional storytelling, human psychology and
modern Stoicism, with more than one visual format. Two pilots test it before anything changes in
the daily routine. Nothing here is a learned rule yet.

**Reference sent by Igor: @tonito.rt, video 7581604527090961687**
- Observed in the file he uploaded: 5.2 s, one static shot of a young man standing still on a metro
  platform while a train passes behind him; a 12-word principle, one word per line with a period,
  lowercase, small cream sans-serif, on screen from the first frame to the last over his dark
  jacket; muted cool grade; a sung song underneath (which song was not verified).
- Derived: the video ID encodes its upload time, 2025-12-08 (UTC).
- Not accessible: the video's own views, likes, shares and saves (TikTok blocks automated access;
  not worked around). Igor can add them from the app.
- Third-party, TokPortal, scraped 2026-09-28: the account had 1,059,735 followers and 2,777 videos;
  its last 10 videos averaged 7.17M views, 1.15M likes, 1,818 comments and 90.5K shares, so likes
  were about 16% and shares about 1.3% of views, comments about 0.03%.
- Hypotheses (one reference, tentative): the whole message readable from frame one and short
  enough to read in one breath invites replays; a principle people want to identify with travels
  by likes and shares more than by comments; a still subject against a moving world carries the
  mood without cuts.

**Pilots**
- v007, Cinematic One Shot (`tools/oneshot.py`): one real shot (a man walking out of morning mist
  into the sun), 6.5 s, "do. your. part. today. the. timeline. was. never. yours." (our own line on
  Epictetus' dichotomy of control, Enchiridion 1), music-free. Ready to post.
- v008, Philosophical Visual Essay: Seneca, On the Shortness of Life, with the Basore translation
  quote checked; visual arc from 2 a.m. blue to sunrise warmth. Delivered as a draft without voice
  (`tools/draft_voice.py`) so Igor approves the images before credits are spent.
- Long videos are rendered without film grain from now on (`"grain": 0` in script.json): the
  same TikTok re-encode problem we saw on the ambient videos.

## Learned (updated weekly, newest first)

_No data yet. First analysis: Monday 2026-11-30._
