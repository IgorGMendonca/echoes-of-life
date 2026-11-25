# Echoes of Life: playbook

Rules the production runs follow. The weekly analysis updates the "Learned" section from real
metrics; the "Starting rules" stay until the numbers say otherwise.

## Identity

- Name: Echoes of Life. Tagline: "Stories that make you feel. Thoughts that stay with you."
- Language: Brazilian Portuguese since 2026-11-25 (Igor: TikTok was delivering the channel almost
  only in Brazil); English before. Audience: Brazil; many viewers are teenagers and young adults.
- Positioning (Igor's brief, 2026-11-24): "modern philosophy for a generation that feels lost":
  emotional storytelling, human psychology and modern Stoicism, filmed cinematically. Stoicism is a
  layer of depth under the feelings, never a lecture.
- Two pillars:
  1. **Time & potential (main, the larger share: the 11:00 one-shot, the philosophy essay and half the stories):** for young people who feel late or behind.
     The message is "you are not late, and you can do more than you think: start small, today".
     Empowering and concrete, never shaming, never hustle-toxic (sleep, rest and bad days are allowed),
     no comparisons with real named people, no invented statistics or "he was 22 when..." stories.
     Footage: students at night, sunrise runs, notebooks, trains and roads, city lights, clocks.
     Hashtags draw from #motivacao #disciplina #desenvolvimentopessoal #autoconhecimento #estudos.
  2. **Bittersweet reflections:** nostalgia, family, love, loneliness, small moral questions.
- Tone: calm, warm, never preachy, never morbid. Every video ends on something the viewer can do or feel today.
- Look: real cinematic footage in 4K only (see "Image quality" in CLAUDE.md), warm desaturated grade, no grain, slow push-ins, serif hook title on the first frame, word-timed captions, echo-rings end card.

## Daily lineup (from 2026-11-25, Igor's decision after the v007 and v008 pilots)

Four videos a day, posted in Brasília time (the audience is in Brazil since 2026-11-25; the New
York times below are kept only for reference):

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
- Long videos: 70–85 s, 150–180 words in Portuguese, 14–19 lines, read in one take (English v008: 181 words ran 77.7 s).
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
- **Story (21:00):** fiction and said to be ("Esta é uma história sobre…"): one named character, one
  specific moment, an emotional shift, a satisfying and hopeful ending. Half the stories serve the
  main pillar (feeling behind, starting late), half nostalgia. No real people, no tragedies.
- **Look:** one real shot per line, light that moves from night blue (the heavy part) to warm
  daylight (the turn); the hook title on screen from the first frame; no film grain.
- **Voice in Portuguese (2026-11-25):** Brian (`nPczCjzI2devNBz1zQrb`, eleven_multilingual_v2,
  the settings in `tools/tts.py`) reads the Portuguese script, because the free plan's API refuses
  the Voice Library, where the native Brazilian narrators are. If Igor upgrades (Starter or above),
  cast with the `voice-direction` skill among calm, deep pt-BR narrators such as Leo Antonio
  (`EbiSUflQjzm4g7S895SC`), Lucas, Deep & Profound (`GIuLCSVfgJaUuh7hYOY8`) and Victor Power
  (`YNOujSUmHtgN6anjqXPf`), and write the chosen voice here.
- **Voice (Igor, 2026-11-24):** the narration is read in one take, so the pauses are the voice's
  own. Separate takes joined by silence sounded like the audio stalling after every sentence.
- **First second (from v011, 2026-11-25 early read):** the voice starts at 0.1 s (`"lead": 0.1` in
  script.json; `timeline.py` still defaults to 0.5 s for older projects) and the first shot has a
  person or a hand in motion, because v008's viewers left after about 1.7 s on average.
- **Music (Igor, 2026-11-24):** none in the file. Igor adds a calm instrumental from the TikTok
  library and sets it to about 15–20% under the voice; each delivery names 2–3 picks.

## One-shot edits (11:00)

Modelled on the reference Igor sent (@tonito.rt, see "Pilots" below) and on v007.
- One real shot, 6–8 s, no cuts: a person still or walking slowly while the world moves (trains,
  crowds, traffic, waves, mist), or a quiet human scene. No faces to camera.
- The whole line is on screen from the first frame to the last: 6–12 words, one per line, each
  with a period, lowercase, small warm-cream sans-serif, on a calm dark area of the frame (a soft
  shade when needed). Readable in one breath, so the loop does the rest.
- The line is ours: a principle worth keeping, usually a Stoic idea in plain modern Portuguese
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
- Every one carries one short lowercase line in Playfair italic (10 words or fewer, shown after
  the lift) that fits the mood; in Portuguese since 2026-11-25 ("ninguém olhava o relógio naquela
  época."; earlier, in English: "rest is not falling behind"). Igor, 2026-11-25, after a no-text cut of v012: always the line on
  screen; pick a view with a calm area (sky, dark wall, water) that keeps it clear of the
  subject, and if the subject fills the frame, change the footage rather than drop the line.
- Sound: the export is music-free (silent track). Igor adds a soft, sung, currently trending song
  from the TikTok library in the app; each delivery names 2–3 picks with a start point that puts a
  sung line or a beat on the camera lift.
- Caption: a short question tied to the place ("De qual cidade você assistiria isso?"). Pinned
  comment: a light prompt such as "Que música você colocaria aqui? 🎧".
- AI label only when the footage itself looks AI-generated (no synthetic voice in this format).

## Search and hashtags (TikTok SEO, from 2026-11-25)

TikTok search reads the caption, the words on screen, the spoken words and the hashtags, and
creators can now review the keywords TikTok attaches to each post. So every video gets one
**search phrase**, written the way people type it, in Portuguese since 2026-11-25 ("me sinto
atrasado na vida", "sêneca sobre o tempo", "estoicismo para estudantes", "nostalgia da
infância"), and it appears naturally, never stuffed:
- on screen early (the hook title, or the stack when it fits),
- in the first spoken line of a long video,
- at the start of the caption's first line, then the line that adds something, then the question.

Hashtags: 4–5, in this order: one broad community tag, two or three that name the topic, and
#echoesoflife last. Never #fyp, #foryou or #viral: they say nothing about the video.
Starting sets in Portuguese (2026-11-25; written without accents, the form most posts use, e.g.
#reflexao and #motivacao; the weekly analysis rotates them):
- One-shot (feeling behind): #estoicismo #reflexao #motivacao #desenvolvimentopessoal #echoesoflife
- Philosophy essay: #estoicismo #<the philosopher: seneca, marcoaurelio, epicteto> #filosofia #reflexao #echoesoflife
- Nostalgia edit: #nostalgia #infancia #saudade #<period or season: anos2000, natal, ferias> #echoesoflife
- Story: #conto #reflexao #<theme: nostalgia or motivacao> #emocionante #echoesoflife
  (#conto says fiction; never #storytime or #historiareal: our stories are invented)
- City edit: #<city> #<country> #viagem #<region: europa, asia> #echoesoflife
English sets used before the switch: #stoicism #feelingbehind #mindset #selfimprovement;
#nostalgia #childhoodmemories #growingup; #shortstory #deepthoughts #emotional.

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
- The end card shows the save/share line ("salva pra quando você precisar", "manda pra quem
  precisa ouvir isso hoje") or "siga para ver mais"; only one call to action per video.
- Never: "like if you agree", "comment YES", "type 1 for…", follow-for-follow, like-for-like,
  fake "part 2" promises, false urgency, or asking for age, school, location or other personal
  information (many viewers are teenagers). TikTok treats fake engagement as ineligible for the
  For You feed, and forced asks also feel cheap.
- Keep the mood mostly hopeful: a channel of only sad videos risks being shown less, and the
  endings should leave people lighter than they arrived.

## City edits (extras on request, from 2026-11-25)

Igor asked for short city videos besides the lineup: v014 (China at night, 13.7 s) and v015
(Venice, 7.4 s). His direction for v015: "é interessante que a música contraste com a cidade
escolhida, como no exemplo que mandei. Mantenha a qualidade do vídeo alta [...] Uns 7-8seg de
vídeo impactantes". His example was a Tokyo-at-night montage (13.7 s, 10 shots, heavy electronic
track with a drop near 4 s and cuts on the beat after it).
- Igor, 2026-11-25, after v016 (Seoul seen from the air): "Os vídeos estão ficando com muita
  imagem da cidade de longe, algo mais próximo, mostrando as pessoas e ruas legais fica melhor,
  não precisa ser sempre acelerado também". So: street level first, with people and streets that
  have character (neon, lanterns, markets, canals, rain, snow); one wide view at most; real-time
  motion by default. Reject hyperlapses and time-lapses: check the tags and compare two frames
  0.2 s apart (in a time-lapse the crowd jumps; Pixabay's 4K Seoul street clips all do). v017
  (Japan at night) is the model.
- Igor, 2026-11-25, after v017: "Ainda sinto falta de cenas mais belas, algo cinematográfico
  mesmo, use as skills para isso, o importante é o cenário". Following the
  `cinematic-video-direction` skill (aesthetic edits: 7–15 s, 1–3 shots): two or three long shots,
  each a scene beautiful enough to hold on its own (blue or golden hour, snow, rain, mist, lamps,
  reflections), in real time with one slow camera move per shot (a `"pan"` across the 4K frame or
  a slow push-in), 0.6–0.8 s dissolves, warm highlights over cool shadows and a soft `"glow"` on
  the lights. People belong to the scenery, they are not the subject.
- Igor, 2026-11-25, after v018 (two shots): "Faltou imagens, precisa mostrar um ambiente nostálgico
  e que impacte as pessoas, a última imagem até que fez sentido" (the last shot was Kyoto under
  snow). So: 5–6 shots in 12–14 s, each a nostalgic scene that could be a memory (a wet street at
  dusk reflecting the sky, a local train crossing a bridge, a misty alley under a street lamp, a
  village under snow, lanterns), arranged as an arc from dusk to night or snow, with a short line
  that hits ("parece lembrança, / mas eu nunca estive aqui."). 60 fps clips may play at half speed
  (`"speed": 0.5`, a true slow motion); never faster than real time. v019 is the model; the
  multi-cut layout below is for energetic songs.
- 7–8 s, 4–6 real 4K shots, the strongest street-level shot first, cuts every 1.2–1.8 s (near-hard
  `"xfade"` 0.05 for an energetic song, 0.2–0.25 for a deep one), the city's name on screen at the
  start over a calm area (water, sky, a dark wall), and the last shot slightly longer with a slow
  zoom out.
- Vivid, natural colour instead of the essays' muted grade, lighter sharpening and a high-quality
  master: `"grade"`, `"sharpen"` 0.3, `"crf"` 12, `"preset"` "slow" in script.json (v015).
- The music contrasts with the place (a romantic old city under a street or game theme, a sleek
  metropolis under Brazilian funk or forró). Pick 2–3 currently trending sounds, clean enough for
  teenagers (instrumental first; check lyrics before recommending a song with words), never in the
  file. Brand names stay out of our own text and hashtags; the sound's title shows by itself.
- Music-free export, `"slot": "extra"` in `log.json`; post between the regular slots.

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

- 2026-11-25 (evening): Igor switched the channel to Brazilian Portuguese because TikTok was
  delivering it almost only in Brazil (his reading of the app's analytics; the connector still
  returns no countries). Everything made from then on is in Portuguese; the English posts stay up.

- 2026-11-25 18:44 UTC (tentative; 13 posts, 2.9–29 h old): v011, the second essay, reached 448
  views in 5.6 h (79/h) and brought 35 follows, 7.8 per 100 views, the best follow rate so far
  (the two breakouts: 0.4–0.5 per 100), though viewers still left after 1.9 s of 77 s. The v008
  repost stopped (+9 views in 5 h, 2,912) and "I miss the days…" slowed to about 210/h (9,636).
  v012, the 18:00 nostalgia edit posted at 09:17 Brasília, had 1 view after 6.5 h, the only
  regular post that never got the first test batch of about 100 views; an unlogged Shibuya clip
  sat at 1 view after 3.2 h too. Hint (one post): the essay format earns follows even without
  watch time; check that a post is public and eligible for For You when it stays near zero.

- 2026-11-25 (tentative; 9 posts, one per format, 5–21 h old, 68–4,256 views each): only two
  posts got past TikTok's first test batch of about 70–150 views, the v008 essay repost (1,737
  views in 5.3 h) and an ambient clip captioned "I miss the days when life felt slower…" (4,256
  in 12.7 h). Both ran about 330 views/h with about 14–15 likes per 100 views; the other seven
  had 1–9 likes per 100 and 6–12 views/h. 96–99.6% of every post's views came from For You. The
  essay kept almost nobody (1.7 s of 78 s on average, 0.1% to the end), so its reach came from
  the first frame and caption, not from watching; v007, the one-shot, sat at 68 views (27% of its
  length watched, 4.9% to the end). Hints only: a first-person, relatable caption line, and a
  long video whose voice and moving image start at once. Audience countries not yet delivered.

- 2026-11-25 13:46 UTC (tentative; 11 posts, 0.7–24 h old): the two breakouts kept growing
  ("I miss the days…" 8,579 views, 545/h over 15.7 h; the v008 repost 2,903, 350/h over 8.3 h)
  and both still have the highest like rates (16.3 and 18.4 per 100 views); every other post sits
  at 76–154 views with 1–11 likes per 100. Both winners open the caption with a sentence people
  agree with on sight (a first-person feeling; a verified quote), and neither is carried by
  watch time (1.7–2.3 s on average). The two one-shots (v007, v009) stalled at 76–79 views.
  v011, with the voice from 0.16 s and a question hook, averaged 3.1 s after 0.7 h (v008: 1.7 s),
  75 views only. Hint to test: open every caption with one quotable sentence before the question.
  Audience countries still come back empty from the connector.

_First full analysis: Monday 2026-11-30._
