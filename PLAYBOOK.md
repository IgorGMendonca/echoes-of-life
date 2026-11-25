# Echoes of Life: playbook

Rules the production runs follow. The weekly analysis updates the "Learned" section from real
metrics; the "Starting rules" stay until the numbers say otherwise.

## Identity

- Name: Echoes of Life. Tagline: "Stories that make you feel. Thoughts that stay with you."
- Language: English. Audience: international, the US first; many viewers are teenagers and young adults.
- Positioning (Igor's brief, 2026-11-24): "modern philosophy for a generation that feels lost":
  emotional storytelling, human psychology and modern Stoicism, filmed cinematically. Stoicism is a
  layer of depth under the feelings, never a lecture.
- Two pillars:
  1. **Time & potential (main, the larger share: the 11:00 one-shot, the philosophy essay and half the stories):** for young people who feel late or behind.
     The message is "you are not late, and you can do more than you think: start small, today".
     Empowering and concrete, never shaming, never hustle-toxic (sleep, rest and bad days are allowed),
     no comparisons with real named people, no invented statistics or "he was 22 when..." stories.
     Footage: students at night, sunrise runs, notebooks, trains and roads, city lights, clocks.
     Hashtags draw from #motivation #selfimprovement #growthmindset #studymotivation #discipline.
  2. **Bittersweet reflections:** nostalgia, family, love, loneliness, small moral questions.
- Tone: calm, warm, never preachy, never morbid. Every video ends on something the viewer can do or feel today.
- Look: real cinematic footage, warm desaturated grade, no grain, slow push-ins, serif hook title on the first frame, word-timed captions, echo-rings end card.

## Daily lineup (from 2026-11-25, Igor's decision after the v007 and v008 pilots)

Four videos a day, posted in Brasília time (New York is 2 hours behind until March):

| Slot | Video | Why |
|---|---|---|
| 11:00 (09:00 NY) | One-shot edit, feeling behind, 6–8 s (like v007) | Reach and replays; a principle to keep before the school or work day |
| 14:00 (12:00 NY) | Long, philosophical essay, 70–85 s (like v008) | A feeling seen through a Stoic text, quote verified |
| 18:00 (16:00 NY) | Nostalgia edit, tilt-up reveal, 7–10 s (like v006) | Reach and replays after school |
| 21:00 (19:00 NY) | Long, story, 70–85 s | Fiction with a character, an emotional shift and a hopeful ending |

Long videos stay over 1 minute so they can count for Creator Rewards later. The two short formats
are different on purpose: the brief asks for more than one visual model, and the weekly analysis
compares them. The old 35–45 s narrated format is retired; its ideas are parked in `pauta.json`.

## Starting rules (hypotheses, not yet proven)

- Hook in the first 2 seconds, 9 words or fewer, shown as the title. It is a statement or a question that hits a universal memory.
- Long videos: 70–85 s, 165–195 words, 14–19 lines, read in one take (v008: 181 words ran 77.7 s).
- One scene per line; a cut every 3–6 s.
- Specific images beat abstractions ("the porch light", "your mom's voice at dinner") .
- End with a gentle call to act ("call them today") or a question for the comments.
- Caption: one sentence that adds to the video, plus a question; 4–5 hashtags, always #echoesoflife.
- Posting: see "Daily lineup" above.

## Long videos: philosophy essay and story

- **Philosophy essay (14:00):** a feeling our audience knows (feeling behind, comparison, time
  anxiety, rest guilt) seen through one Stoic text, the way a kind older friend would explain it.
  Order, as in v008: the hook, a modern scene, what the philosopher said, what it means and what it
  does not mean, one small thing to do tonight, a closing line. At most one short quote, word for
  word from a public-domain translation and checked online that day, said with its author and
  work; everything else is our paraphrase or interpretation, recorded as such in `script.json`.
  Stoicism here is perspective and calm: never bottled-up feelings, coldness, isolation, hustle
  or toughness. Psychology joins only with a credible source, said carefully.
- **Story (21:00):** fiction and said to be ("This is a story about…"): one named character, one
  specific moment, an emotional shift, a satisfying and hopeful ending. Half the stories serve the
  main pillar (feeling behind, starting late), half nostalgia. No real people, no tragedies.
- **Look:** one real shot per line, light that moves from night blue (the heavy part) to warm
  daylight (the turn); the hook title on screen from the first frame; no film grain.
- **Voice (Igor, 2026-11-24):** the narration is read in one take, so the pauses are the voice's
  own. Separate takes joined by silence sounded like the audio stalling after every sentence.
- **Music (Igor, 2026-11-24):** none in the file. Igor adds a calm instrumental from the TikTok
  library and sets it to about 15–20% under the voice; each delivery names 2–3 picks.

## One-shot edits (11:00)

Modelled on the reference Igor sent (@tonito.rt, see "Pilots" below) and on v007.
- One real shot, 6–8 s, no cuts: a person still or walking slowly while the world moves (trains,
  crowds, traffic, waves, mist), or a quiet human scene. No faces to camera.
- The whole line is on screen from the first frame to the last: 6–12 words, one per line, each
  with a period, lowercase, small warm-cream sans-serif, on a calm dark area of the frame (a soft
  shade when needed). Readable in one breath, so the loop does the rest.
- The line is ours: a principle worth keeping, usually a Stoic idea in plain modern words
  (dichotomy of control, the present moment, patience, judgments). Never a quote, never attributed.
- Caption: the idea behind the line plus a question. Pinned comment: a second, lighter question.
- Music-free export; 2–3 song picks per delivery.

## Nostalgia edits (18:00, tilt-up reveal)

One a day, made to be watched to the end and replayed: childhood, family, seasons, small towns,
kids playing, warm windows at dusk; v006 is the model.

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

## Search and hashtags (TikTok SEO, from 2026-11-25)

TikTok search reads the caption, the words on screen, the spoken words and the hashtags, and
creators can now review the keywords TikTok attaches to each post. So every video gets one
**search phrase**, written the way people type it ("feeling behind in life", "seneca on time",
"stoicism for students", "childhood nostalgia"), and it appears naturally, never stuffed:
- on screen early (the hook title, or the stack when it fits),
- in the first spoken line of a long video,
- at the start of the caption's first line, then the line that adds something, then the question.

Hashtags: 4–5, in this order: one broad community tag, two or three that name the topic, and
#echoesoflife last. Never #fyp, #foryou or #viral: they say nothing about the video.
Starting sets (the weekly analysis rotates them):
- One-shot (feeling behind): #stoicism #feelingbehind #mindset #selfimprovement #echoesoflife
- Philosophy essay: #stoicism #<the philosopher: seneca, marcusaurelius, epictetus> #philosophy #feelingbehind #echoesoflife
- Nostalgia edit: #nostalgia #childhoodmemories #growingup #<season: autumn, winter, christmas> #echoesoflife
- Story: #shortstory #<theme: nostalgia or feelingbehind> #deepthoughts #emotional #echoesoflife
  (never #storytime: our stories are fiction)

After posting, Igor opens the video's three dots → "Manage keywords", blocks anything off-topic
and suggests the search phrase plus two related keywords; every delivery lists them.

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

## Pilots (2026-11-24, approved)

Igor's brief of 2026-11-24 (`docs/brief-2026-11-24-stoic-direction.md`) points the channel toward
"modern philosophy for a generation that feels lost". Two pilots tested it; Igor approved both the
same night ("Ficou muito bom, vamos seguir esse padrão") and they became the 11:00 and 14:00
formats from 2026-11-25. Nothing here is a learned rule from metrics yet.

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
  quote checked; visual arc from 2 a.m. blue to sunrise warmth. First a draft without voice
  (`tools/draft_voice.py`); after Igor's approval, narrated in one take and exported voice-only
  (he flagged the stalls between separately generated sentences and asked for TikTok music).
- Long videos are rendered without film grain from now on (`"grain": 0` in script.json): the
  same TikTok re-encode problem we saw on the ambient videos.

## Learned (updated weekly, newest first)

_No data yet. First analysis: Monday 2026-11-30._
