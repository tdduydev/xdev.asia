# Why AI Studio — drawn product story

Brief: a Vietnamese/English product explainer for teams considering AI Studio.
The story explains the product problem and rationale, not a biographical origin
story or a claim that every integration is deployed. 16:9, 1280×720, 24fps,
Vietnamese 6:05.5 and English 6:39. Synthetic narration, no background music.

Material: blue and navy ink on dotted paper. Original whole-pose employee cels
(work, think, happy), authored contours and stable held strokes. The same
purchasing-assistant example connects the problem, knowledge, workflow and review.
No camera motion. The closing logo uses the approved embedded SVG.

## Beat sheet

1. Scattered documents and an employee's question.
2. An illustrative purchasing assistant and human review.
3. Document ingestion, OCR, NER/PII, chunking and indexing.
4. Access-controlled knowledge retrieval and relevant context.
5. Custom workflows, branches, variables, debugging, versions and DSL.
6. AI Gateway: model routing and eligible fallback providers.
7. PII policy and controlled outbound data; blocked route stops at the boundary.
8. Code execution through a separately configured sandbox service.
9. Human approval before a tool call; feedback returns to the draft.
10. API, MCP and workflow tools.
11. Publishing, channels, keys, quotas and triggers.
12. Conversation memory, reviewed memories, speech and images.
13. Logs, evaluations, annotations and training.
14. Workspace and instance operations, roles, identity and S3.
15. Four example use cases.
16. Connected closing overview.

Scene lengths derive from speech plus 1.5 seconds of breathing room. Arrows
terminate on card ports; packet motion follows the same curve as its arrowhead.
Dashed return paths show feedback. Capability maps use undirected lines rather
than implying execution order. The approval diagram has no tool-call bypass.
Inspect full-size security/approval/sandbox frames, contact sheets and motion
strips. Browser checks also validate connector endpoints and approval topology.

All 60 manual topics map to these feature groups in [COVERAGE.md](COVERAGE.md).
The film is a product overview; detailed operations remain in the manual.
Gateway is a descriptive name for the existing provider policy/runtime layer.
NER detection and sandbox isolation depend on configuration and deployment;
the film does not promise exhaustive PII detection or security certification.

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
narrated Canvas playback; source.zip is the self-contained HTML bundle. story.v2.vi.mp4 and story.v2.en.mp4
are the portable offline delivery. The source bundle includes v2 narration. Browser rasterization may differ across
versions; a pinned Chrome/font runtime is required for pixel-identical renders.
The diagrams illustrate concepts, not actual backend execution. Speech
pronunciation has not been reviewed by a human narrator.
