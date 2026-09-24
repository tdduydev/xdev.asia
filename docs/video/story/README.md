# Why AI Studio — drawn product story

Brief: a Vietnamese/English product explainer for teams considering AI Studio.
The story explains the product problem and rationale, not a biographical origin
story or a claim that every integration is deployed. 16:9, 1280×720, 24fps,
about 1 minute 45 seconds per edition. Synthetic narration, no background music.

Material: blue and navy ink on a quiet dotted paper ground. Original authored
contours and draw-on marks; no characters, external photos, or generated footage.
Motion reference: a whiteboard explanation, documents physically gathering,
data travelling through connected nodes, a review gate, and a closing overview.
Stable per-stroke seeds; continuous root motion; held drawings remain unchanged.
The closing logo is the approved SVG, not an approximation made by the renderer.

## Beat sheet

1. Scattered documents, systems and experience; a search line reaches a question.
2. A question reaches a model; branches expose missing data, access and next steps.
3. Documents gather into a knowledge base; context travels to retrieval output.
4. Five workflow nodes draw in sequence; data packets follow their connections.
5. Test, inspect, approve and publish; a feedback line returns from the output.
6. The connected product view, approved identity and a held closing invitation.

Scene lengths derive from each spoken segment plus 1.5 seconds of breathing room.
Hardest action: scene 4, authored node contours followed by connector strokes and
staggered packets. Inspected in a 12-frame strip, full-size frame and contact sheet.
No physical character contacts or anatomy are involved. No camera motion.

## Sources and licensing

Applied skill: https://github.com/alesha-pro/tools/tree/main/skills/hand-drawn-canvas-animation
Engine core.js, studio.js, cels.js and render.mjs: alesha-pro/tools, MIT,
copyright 2026 Alexey Fateev; licence copied beside the source assets.
Original narrative and drawing code: this repository. Inter and approved brand
SVG copied from the website's existing assets. Narration: edge-tts with
vi-VN-HoaiMyNeural and en-US-JennyNeural, as in the existing product tour.
No external audio recordings, customer data or credentials were submitted.

## Rebuild

Install Python video-requirements.txt and `npm ci` in this directory. System
Chrome and ffmpeg must be on PATH. The renderer itself is copied unchanged.

1. Run `prepare.py` to synthesize segments, captions and timing manifests.
2. Run `node render.mjs ../../../src/assets/ai-studio/story/story.vi.html --grid 24 --out /tmp/story-render` and inspect the grid; repeat for English.
3. Run the renderer without `--grid` for both HTML files.
4. Run `finish.py` to mux narration, capture posters and package offline source.
5. Run the website build and browser validation.

Output: `src/assets/ai-studio/story/`. Open story.vi.html or story.en.html for
narrated Canvas playback; source.zip is the self-contained HTML bundle. MP4s
are the portable offline delivery. Browser rasterization may differ across
versions; a pinned Chrome/font runtime is required for pixel-identical renders.
The diagrams illustrate concepts, not actual backend execution. Speech
pronunciation has not been reviewed by a human narrator.
