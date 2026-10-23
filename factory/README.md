# Video Factory — weekly production procedure (cloud, no local computer)

Faceless YouTube channel, Kurzgesagt-style flat-vector animated "What if…?" / explainer videos.
Per topic: **1 long video (16:9, ~3:45–4:20) + 2 Shorts (9:16) cut from it**. English narration, ElevenLabs voice
"Max – Elearning and Documentary" (model `eleven_v4`). All code is Python + pycairo + numpy/scipy + ffmpeg.

Everything lives in the GitHub repo `bugrahancamlibel/youtube-kanali` (this folder is `factory/`).
The user's computer is NOT needed and must not be used. Talk to the user (Boogie) in Turkish; video content is English.

## Setup in a fresh workspace
`pip install --break-system-packages pycairo numpy scipy pillow requests`; ffmpeg must exist; the Poppins font must be
installed (check `fc-list | grep -i poppins`; if missing: `pip download` is not enough — fetch the TTF files from
the google/fonts GitHub repo (`ofl/poppins/Poppins-Regular.ttf`, `Poppins-Bold.ttf`) into `~/.fonts` and run `fc-cache -f`).
Run all project commands from inside the project folder (e.g. `cd factory/qday && python3 main.py ...`).

## Layout
```
repo root
  config.json                     publisher settings (Upload-Post user, platforms, publish time)
  projects/<NN-slug>/project.json one per topic: titles, descriptions, state of every upload (read by the publisher)
  projects/<NN-slug>/Bilgiler.txt, ElevenLabs Metni.txt, shorts_plan.json
  publisher/publish.py            cloud publisher (GitHub Actions "Yayin", daily 20:35 + 21:35 Istanbul)
  publisher/approve.py            handles "onay"/"ret" comments on approval issues (Actions "Onay")
  publisher/tts.py                ElevenLabs API voice-over (Actions "Seslendirme", key is a repo secret)
  YAYIN_TAKVIMI.md                generated publishing calendar
  branch `videolar`: <NN-slug>/   the videos: long.mp4, short1.mp4, short2.mp4 (+ draft.mp4 for silent drafts)
factory/
  render.py, deepfake.py          core drawing helpers (person, face, glitch, pill, bubble, robot, big_eye…)
  long/base.py                    1920x1080 helpers (bg, hills, card, robot2, phone, money, stamp…)
  solar/props.py                  sun, cme, earth, aurora, pylon, transformer, satellite, city, icons…
  aijobs/                         TEMPLATE PROJECT (copy this for a new topic)
    script.py                     SCRIPT = list of scenes, each a list of narration lines; timeline()
    props_ai.py / scenes_ai.py    scene functions s0..s7 (signature: ctx, lt, t, L  where L = [(start,end)] per line)
    main.py                       renderer + 7 unique transitions (TRANS dict) ; modes: info / stills / warp
    audio_ai.py                   generative score + SFX keyed to lines (A(scene,line,offset)) ; supports 'warp'
    vo/align.py, vo/build.py      split the ElevenLabs take into lines (DP on silences) -> time-warp json + vo_track.wav
  qday/, glacier/                 projects 04 and 05 (silent, waiting for voice) - good examples of props/scenes
  tools/make_short.py             16:9 segment -> 9:16 Short (hook text, burned captions, freeze-frame end card)
  tools/short_plan.py             clean Short boundaries from (scene,line) pairs using vo/warp.json
  tools/shorts_from_plan.py       cuts both Shorts of a project from its shorts_plan.json
  tools/make_project.py           writes projects/<slug>/project.json
  tools/sheet.py                  contact sheet of PNGs
```

## Getting the repo in a session
Attach it with the add_repo tool (owner `bugrahancamlibel`, repo `youtube-kanali`, access `push`), clone it
(`git clone --depth 1`, main branch only — do not fetch the big `videolar` branch), and use `gh` for workflows and
issues (`gh workflow run ...`, `gh issue ...`). GitHub Releases are NOT available to Claude sessions (HTTP 403):
videos go to the `videolar` branch instead (see step 9). Each video file must be < 95 MB.
Commit with a clear message and push to `main` after every finished step, so nothing is lost if the session stops.

## Weekly run (each step must be verified before moving on)
0. **Voice-pending projects come first.** List `projects/*/project.json`; any with `"status": "needs_voice"` is a
   finished silent project (script, scenes, shorts_plan.json done, code in `factory/<factory_dir>/`). Try to voice the
   OLDEST one (step 4). If that works, finish it (steps 5-10) instead of starting a new topic.
   If there is not enough ElevenLabs credit: do NOT start new work that needs voice; you may still build ONE new silent
   project (steps 1-3 + silent draft, status `needs_voice`) if fewer than 3 projects are waiting, then notify the user.
1. **Topic research** (web): what's trending *this week* in science / tech / AI / space + proven "What if" formats.
   Do not repeat a topic that already has a folder in `projects/`. Verify every number with a reputable source; keep a source list.
2. **Script**: copy `factory/aijobs/` -> `factory/<slug>/`, rewrite `script.py` (8 scenes, ~28–35 lines,
   ~3,000–3,400 chars ≈ 3:45–4:10). Cold open hook in the first 10 s, title card at end of scene 0, honest framing.
   Write the line that will END Short 2 as a punchline, and make Short 2's first line understandable without context.
3. **Scenes**: write new `props_*.py` + `scenes_*.py` (reuse helpers). Keep text above y≈880, avoid glyphs missing from
   Poppins (arrows, ≈, −, ₿). Pick 7 different transitions in `main.py` TRANS. Render stills
   (`python3 main.py st stills <times>`) and review contact sheets (`tools/sheet.py`); fix overlaps / empty frames.
   Write `shorts_plan.json` (see `factory/qday/shorts_plan.json`; HL = TRANS half-lengths).
   Silent draft (only if no voice yet): `python3 audio_x.py music_draft.wav` and render `python3 main.py dN.mp4 x f0 f1`
   in 4 parallel parts, concat + mux -> push as `<slug>/draft.mp4` to the `videolar` branch (step 9).
4. **Voice (cloud)**: put the narration in `projects/<slug>/ElevenLabs Metni.txt` (lines separated by blank lines), push,
   then start the "Seslendirme" workflow with the REST API (GraphQL and `gh workflow run` do not work in sessions):
   `gh api -X POST repos/bugrahancamlibel/youtube-kanali/actions/workflows/seslendirme.yml/dispatches -f ref=main -f 'inputs[project]=<slug>'`.
   Poll every 30 s: `gh api "repos/bugrahancamlibel/youtube-kanali/actions/workflows/seslendirme.yml/runs?per_page=1" --jq '.workflow_runs[0] | [.status,.conclusion,.html_url]'`.
   On success the audio is on the `videolar` branch: `gh api -H "Accept: application/vnd.github.raw"
   "/repos/bugrahancamlibel/youtube-kanali/contents/<slug>/vo.mp3?ref=videolar" > vo/vo.mp3`, then
   `ffmpeg -i vo/vo.mp3 -ar 44100 vo/g1.wav`. If the run fails (usually "ElevenLabs kredisi yetersiz"), keep the project
   `needs_voice`, stop voice work and tell the user (give the run URL). NEVER buy or upgrade anything.
5. **Sync**: `python3 vo/align.py vo/g1.wav` -> check every line duration vs expected; fix doubtful boundaries by
   inspecting silences; then `python3 vo/build.py` (set HL to the TRANS half-lengths) -> `vo/warp.json`.
6. **Audio**: SFX section of `audio_*.py` for the scenes, `python3 audio_x.py music_vo.wav warp`, duck music under voice
   -> `final_mix.wav`; compute `captions_real.json` ([t0, t1, text, scene, line] in real time).
7. **Render**: `N=$(python3 main.py x warp n)`; render in parallel parts (`main.py partX.mp4 warp a b`), concat + mux.
   Final long video: x264 `-tune animation -crf 20 -maxrate 2500k -bufsize 5000k`, AAC 192k; must stay < 95 MB.
   Check a 1-frame-per-10s contact sheet.
8. **Shorts**: `python3 ../tools/shorts_from_plan.py . <final_long.mp4> <outdir>` (reads `shorts_plan.json`).
   RULES (user feedback, Oct 2026): every Short must END right after a payoff line (punchline / reveal), never
   mid-thought, never bleeding into the next line or a scene transition; the tool freezes a hero frame and adds a
   "WATCH THE FULL VIDEO" end card. Check the last 3 s of each Short. Hook text must be accurate.
9. **Package**: push the videos to the `videolar` branch as `<slug>/long.mp4`, `<slug>/short1.mp4`, `<slug>/short2.mp4`
   (exact names). Do it from a separate small clone so main stays light:
   `git clone --depth 1 -b videolar --filter=blob:none --no-checkout <url> /tmp/v && cd /tmp/v && git sparse-checkout set <slug>
   && git checkout videolar`, copy the files, commit, `git push`. Verify with
   `gh api -H "Accept: application/vnd.github.raw" "/repos/bugrahancamlibel/youtube-kanali/contents/<slug>/long.mp4?ref=videolar" | wc -c`.
   Write `projects/<slug>/project.json` with `tools/make_project.py` (status `ready`, approved false, NO dates —
   the publisher assigns them on approval), `Bilgiler.txt` (title, description with chapters + sources +
   "Narration: AI voice (ElevenLabs)", tags, script, sources) and `shorts_plan.json`. Commit + push.
10. **Ask for approval** (REST only): create the label once
    `gh api repos/bugrahancamlibel/youtube-kanali/labels -f name=onay-bekliyor -f color=fbca04` (422 = already exists, fine),
    write the issue body to a file and run
    `gh api repos/bugrahancamlibel/youtube-kanali/issues -f "title=[Onay] <NN> - <Title>" -F body=@body.md -f 'labels[]=onay-bekliyor'`.
    The body must contain the marker line `<!-- project: <slug> -->`, a Turkish summary (topic, why now, lengths), links to
    the three videos (`https://github.com/bugrahancamlibel/youtube-kanali/blob/videolar/<slug>/long.mp4` etc.), the
    Shorts hooks, sources, and: "Onaylamak için bu issue'ya **onay** yaz; istemiyorsan **ret** yaz. Onaylayınca
    sıradaki boş günlere otomatik yerleşir." Also send the three videos with SendUserFile so the user can watch them in
    the app, and finish with a short Turkish summary.

## Publishing (fully automatic, GitHub Actions)
- "Yayin" workflow runs every day at 20:35 and 21:35 Istanbul time: gives dates to newly approved projects
  (Short 1, long video next day, Short 2 two days later; next project two days after that; 20:30), shifts the
  remaining plan by whole days if it fell behind (order and spacing kept), uploads whatever is due to Upload-Post
  (secret `UPLOAD_POST_API_KEY`, user name in `config.json`), and writes the state back.
- "Onay" workflow: the user's "onay" / "ret" comment on an `onay-bekliyor` issue approves / rejects the project.
- `config.json` `mode`: `just_in_time` (default, works on any Upload-Post plan) or `schedule_ahead` (sends every
  approved item to Upload-Post at once with `scheduled_date`; needs a paid plan).
- Never publish anything by hand and never change `state` of uploads unless the user asks.
