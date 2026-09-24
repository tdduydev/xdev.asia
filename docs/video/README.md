# AI Studio narrated product tour

Two 1280 × 720 MP4 editions, Vietnamese and English, organised into seven chapters.
The video is an illustrated narrated tour, not a recording of a live backend demo.
It uses real locally rendered frontend screens with intercepted synthetic API data.
Narration uses synthetic voices: vi-VN-HoaiMyNeural and en-US-JennyNeural.

Editable narration: `script.vi.json` and `script.en.json`. Each tour has 29 illustrated
segments; application configuration and evaluation are covered inside their parent
segments. The website provides all 60 topic guides, 7 seek buttons, localized WebVTT
captions and a full transcript. MP4 files also contain chapter metadata.

## Regenerate

Install `scripts/video-requirements.txt` in a separate Python environment. Playwright
and Chrome are needed for frame rendering. Network access is needed for speech
synthesis; only the public narration text is sent, never credentials or workspace
records. Exact timing can vary when regenerating synthesized speech.

```sh
python3 scripts/prepare_studio_video.py
# Clear /tmp/xdev-video/<locale>/*.done when changing narration.
/path/to/venv/bin/python scripts/narrate_studio_video.py
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node scripts/render_studio_video_frames.cjs
/path/to/venv/bin/python scripts/encode_studio_video.py
python3 scripts/build.py
python3 scripts/check_site.py
python3 scripts/preview.py --port 4321
```

Artifacts live in `src/assets/ai-studio/video/` and are copied into `dist/` by the
build. Manifests contain actual chapter times, narration and durations. Encoding
uses a small speed adjustment if needed to keep each edition between 5 and 7 minutes.

Use `scripts/preview.py` instead of Python's basic `http.server`: byte-range
responses are required for dependable browser chapter seeking. Hosted static
servers must also support byte ranges and the `video/mp4` MIME type.

Validation:

```sh
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright SITE_PREVIEW=http://127.0.0.1:4321 node scripts/check_studio_video.cjs
```

This checks playback, audio/video decoding, localized caption cues, chapter
seeking, downloads, transcript access and mobile overflow. It does not establish
backend feature acceptance or independently review pronunciation.

A separate drawn product story is documented in [story/README.md](story/README.md).
