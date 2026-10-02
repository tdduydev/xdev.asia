# xDev Hive product page and narrated film

The English and Vietnamese landing pages use `src/hive.*.json`,
`scripts/hive_page.py`, and `src/assets/hive-page.css` / `hive-page.js`.
Hive is positioned as AI SDLC orchestration: claim tasks → build → review → learn. Documents, skills, and memory support that development workflow.
The page covers the product problem, six screenshot panels, six capability
families, four use cases, setup choices, human review, and FAQ.

## Showcase sources

The six UI captures per language show the real adjacent Hive frontend, built
from its current working tree. A disposable SQLite hub binds to loopback and is
seeded with an illustrative Atlas project. No production hub, customer records,
CLI subscriptions, or external repo integrations are accessed. The temporary
bootstrap token is never written into the delivered images or video.

`capture.json` records capture time and dimensions. Demo document contents stay
in English in both editions; navigation, controls, and interface copy follow the
selected locale. Screenshots illustrate the frontend, not acceptance of all
backend or runner features.

```sh
# Build the adjacent Hive web frontend first.
cd ../xdev-hive && npm run build -w @xdev-hive/web
cd ../xdev.asia
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node scripts/capture_hive.cjs
```

`HIVE_SOURCE` and `CHROME_PATH` can override the adjacent checkout and Chrome.
The capture process stops the demo hub when finished. It uses port 7799 and will
fail if a new hub cannot start there.

## Product film

12 scenes in 7 chapters, 1280 × 720 at 24fps. Vietnamese: 4:34;
English: 4:51. The film introduces AI SDLC orchestration, then covers context → documents → memory and
skills → tasks and runs → human review → local/team deployment → getting
started. Branded title cards and actual demo UI captures use a restrained camera
push and fades. No background music is used. Both editions have synthetic speech,
WebVTT captions, MP4 chapter metadata, posters, downloads, and a full transcript.

Editable sources: `script.vi.json` and `script.en.json`. Speech uses Edge TTS
(vi-VN-HoaiMyNeural and en-US-JennyNeural). Only public product narration is sent
to the speech service. Cache entries are keyed by voice and narration content.
Human pronunciation review is still recommended before a public launch.

```sh
uv venv /tmp/xdev-hive-video-venv
uv pip install --python /tmp/xdev-hive-video-venv/bin/python -r docs/hive/requirements.txt
# ffmpeg / ffprobe are required on PATH.
/tmp/xdev-hive-video-venv/bin/python scripts/build_hive_video.py
python3 scripts/build.py
python3 scripts/check_site.py
python3 scripts/check_hive_media.py
python3 scripts/preview.py --port 4321
```

The renderer uses the approved `hive-light.svg` wordmark rasterized as `brand.png`.
To regenerate it with Sharp:

```js
await sharp('src/assets/brand/wordmark-v2/hive-light.svg')
  .resize(174,80,{fit:'contain',background:'#f7f9fc'})
  .png().toFile('src/assets/hive/video/brand.png');
```

`HIVE_VIDEO_FONT` selects an Arial-compatible TTF; the default is macOS Arial.
Its bold font must be available as `Arial Bold.ttf` in the same directory.
`HIVE_VIDEO_WORK` overrides the temporary cache. Re-encoding reuses narration.
Asset generation needs Pillow/Edge TTS, but ordinary site builds need only Python
stdlib. Serve `dist` with byte-range support for browser chapter seeking.

Tabs support arrow keys, Home, and End. All six panels remain visible when
JavaScript is disabled. Video controls, captions, downloads, and transcripts
remain usable without scripts. Hero connector motion pauses offscreen or in
hidden tabs, respects reduced motion, and provides a pause control.
