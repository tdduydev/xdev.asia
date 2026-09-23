# xDev Asia

Static English/Vietnamese product website and user guides for XDev AI Studio. English is the default. Forge is not included in the generated site.

## Routes

| English | Vietnamese | Purpose |
| --- | --- | --- |
| `/` | `/vi/` | xDev home; product links lead to the local overview |
| `/brand/` | `/vi/brand/` | Brand story, selected logos and SVG downloads |
| `/ai-studio/` | `/vi/ai-studio/` | Product introduction; all actions stay on this site |
| `/ai-studio/docs/` | `/vi/ai-studio/docs/` | Documentation index |
| `/ai-studio/docs/quickstart/` | `/vi/ai-studio/docs/quickstart/` | First application |
| `/ai-studio/docs/knowledge/` | `/vi/ai-studio/docs/knowledge/` | Knowledge bases |
| `/ai-studio/docs/workflows/` | `/vi/ai-studio/docs/workflows/` | Workflow setup |
| `/ai-studio/docs/publishing/` | `/vi/ai-studio/docs/publishing/` | Publication and maintenance |

EN/VI switches to the corresponding page. Navigation works without JavaScript. Each route has its own title, description, canonical and alternate-language metadata. Relative links also support a GitHub Pages repository subpath.

## Build, check, preview

Python 3.12 or newer; no package installation required.

```sh
python3 scripts/build.py
python3 scripts/check_site.py
python3 scripts/preview.py --port 4321
```

Open http://127.0.0.1:4321/. `dist/` is exclusively generated and is replaced on every build. Edit files under `src/`, not `dist/`.

- `src/index.vi.html`: Vietnamese home template.
- `src/home.en.json`: English home translations.
- `src/studio.en.json`, `src/studio.vi.json`: localized overview and documentation. Add matching guide slugs in both files to generate `/ai-studio/docs/<slug>/`.
- `src/styles.css`, `src/assets/`: shared styles and assets.
- `scripts/build.py`: page layouts and route generation.
- `scripts/check_site.py`: page inventory, local links/anchors, metadata, locale parity, default language and product visibility checks.

Set `SITE_URL` to the final origin, including any repository subpath, when building for another URL. Default: `https://xdev.asia`. For example:

```sh
SITE_URL=https://tdduydev.github.io/xdev.asia python3 scripts/build.py
python3 scripts/check_site.py
```

## CI/CD: automatic GitHub Pages deployment

`.github/workflows/site.yml` builds and validates pull requests and pushes to `main`, then uploads the `xdev-site` artifact for review. A push to `main` also deploys to GitHub Pages after the build and validation pass. Pull requests only build and validate.

You can also deploy manually using **Run workflow** on `main` with **deploy** checked; leaving it unchecked runs only the build. The deploy job uses only the artifact produced by the successful build in that same run. No repository changes, Git pushes, or Sites publication are performed by this workflow.

One-time setup, to perform only when ready to move hosting:

1. Push the reviewed workflow and source to GitHub.
2. In repository **Settings → Pages**, select **GitHub Actions** as the source.
3. Set the repository variable `SITE_URL` to the published origin. For a first test without a custom domain, use `https://tdduydev.github.io/xdev.asia`.
4. Optionally require a reviewer on the `github-pages` environment.
5. Push to `main` (or manually run **Build and deploy site** with **deploy** checked), then inspect the deployment URL.
6. To use `xdev.asia`, configure the custom domain in Pages and switch its DNS only after the Pages deployment is verified. Existing Sites DNS records do not route to GitHub Pages. Do not change blog or product subdomains.

Authentication uses GitHub's scoped `GITHUB_TOKEN`/OIDC; no personal token is needed. Build has read-only repository permissions; only deployment receives `pages: write` and `id-token: write`.

Official setup: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

The existing `.openai/hosting.json` remains as the previous Sites project reference. It contains no credentials and is not used by GitHub Pages. This change does not publish to Sites, migrate DNS, or enable GitHub Pages by itself.

## Content basis

The introductory guides were checked against the adjacent XDev AI Studio source on 2026-09-20: application creation, draft editor, publish action, knowledge creation wizard, and workflow editor. The manual now covers 60 topic guides across eight groups with localized screenshots, step-by-step instructions, and expected results. Available actions depend on workspace permissions and configuration. Update both language files when the product changes.

The logo, favicon and font were retrieved from blog.xdev.asia on 2026-09-20. The application itself is at https://ai-studio.xdev.asia.


## Illustrated manual (2026-09-23)

The product and manual live under `/ai-studio/` (English default) and `/vi/ai-studio/`. There are 60 articles per language with localized interface screenshots. All product-page and manual actions stay on xdev.asia; no app-domain launch links or redirects are generated. Screenshots open as full-size local images.

Besides the four original guides, the manual covers models, data sources, tools/MCP, approvals, API access, triggers, memory, monitoring, workspace management, data protection, branding and related services, training, account settings and instance administration.

Screenshots show the real local AI Studio frontend rendered by Chrome with **synthetic API responses** intercepted by Playwright. They do not contain customer data or credentials, and do not verify backend behavior. Example names and usage metrics are illustrations. Capture source: adjacent `xdev-ai-studio` checkout at `041daf6` plus the current workspace changes, 1440 × 1000 pixels, English and Vietnamese.

To regenerate, build and serve the adjacent Studio frontend locally, then run with a locally installed Playwright module:

```sh
STUDIO_URL=http://localhost:3116 PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node scripts/capture_studio.cjs
python3 scripts/build.py
python3 scripts/check_site.py
# With dist served on port 4321:
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright node scripts/check_browser.cjs
```

`STUDIO_WEB`, `CHROME_PATH` and `SITE_PREVIEW` can override the source path, Chrome executable and site preview URL. `ONLY=apps,editor` captures selected screens. The capture script only accepts a localhost Studio origin and supplies demo data rather than reading a live workspace.

The browser check loads all 36 articles and their images, switches languages, follows the table of contents and full-size images, and checks desktop/tablet/mobile layouts with JavaScript disabled. `check_site.py` checks image language, PNG dimensions, local links, and absence of application-domain links as well as the original site checks.

The complete generated website is in `dist/`. Keep its `assets/`, `ai-studio/` and `vi/` directories together when copying or hosting it. Open `dist/ai-studio/index.html` for the product overview or serve the whole `dist/` directory. No deployment is performed by these commands.

## AI Studio product overview

The EN/VI overview uses `scripts/studio_page.py`, the `landing` content in both
`src/studio.*.json` files, and `src/assets/studio-page.css` / `studio-page.js`.
It includes a user-triggered illustrative workflow and four localized screenshot
tabs. The illustration makes no API calls. With JavaScript disabled, all four
sections remain visible and the tab links work as anchors. Motion follows the
visitor's reduced-motion setting.

To check both locales, mobile/desktop layouts, keyboard tab navigation, simulation
replay, image loading, and the no-JavaScript fallback:

```sh
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright SITE_PREVIEW=http://127.0.0.1:4321 node scripts/check_studio_browser.cjs
```

The motion pass applies `micro-interaction`, `svg-animation`,
`60fps-animation`, and `accessible-animation` from
[iart-ai/web-animation-skills](https://github.com/iart-ai/web-animation-skills).
Runtime motion uses native Web Animations and CSS; no animation CDN is required.
The workflow has SVG packets, a completion bar and replay feedback; tabs have a
transform-based sliding indicator. Reduced motion keeps brief opacity feedback
and reacts to preference changes without reloading.

```sh
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright SITE_PREVIEW=http://127.0.0.1:4321 node scripts/check_studio_motion.cjs
```

This check saves deterministic animation frames and a Chrome trace in `/tmp/`,
checks live preference changes, and reports Layout/Paint events in a short
mid-animation sample. That sample is not a device-wide frame-rate guarantee.

## Homepage: the xDev build space

The homepage uses `src/index.vi.html`, `src/home.en.json`, and
`src/assets/home-page.css` / `home-page.js`. Its focal point is a locally rendered
extruded X derived from the brand, with rotate, structure, and reset controls.
The canvas uses a finite animation loop and stops at rest, offscreen, when the
page is hidden, or when reduced motion is enabled. A static SVG remains available
without JavaScript or a canvas context. Product previews use the existing
localized screenshots; all three remain readable without JavaScript.

[Visual direction and research](docs/visual-direction.md) records the composition,
reference sources, tokens, and motion choices. No external graphics or animation
libraries are required. AI Studio uses the same typography and navy workbench
treatment; documentation retains its reading layout.

```sh
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright SITE_PREVIEW=http://127.0.0.1:4321 node scripts/check_home_browser.cjs
```

The check covers both locales at five screen widths, screenshot language,
keyboard tabs, sculpture controls, idle frame-loop termination, live reduced
motion, no-JavaScript/canvas fallbacks, and product navigation.

## Brand guide

`/brand/` and `/vi/brand/` present the selected X + DEV / AI Studio logo family,
light and dark variants, palette, usage guidance and SVG downloads. Footer links
make the guide accessible from the homepage and product documentation.

Edit `src/brand.en.json` and `src/brand.vi.json` for copy,
`scripts/brand_page.py` for markup and `src/assets/brand-guide.css` for styling.
The page works without JavaScript. See [selected brand decisions](docs/brand/brand-decisions.md).

## Grouped documentation navigation

`scripts/docs_page.py` owns the five shared EN/VI topic groups and validates that
each guide appears exactly once. Existing article URLs remain unchanged. The
current topic expands automatically, with native details/summary controls that
also work without JavaScript. The index groups articles by topic; article pages
include topic breadcrumbs, a table of contents and previous/next navigation.
Styling lives in `src/assets/docs-page.css`.

```sh
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright SITE_PREVIEW=http://127.0.0.1:4321 node scripts/check_docs_navigation.cjs
```

## Feature catalog and bilingual narrated tour

The product overview now shares the documentation inventory: 60 topics and 120
localized articles. See [source coverage](docs/feature-coverage.md) for scope and
[video generation](docs/video/README.md) for the editable narration and rendering
pipeline. The seven-chapter tour has separate English/Vietnamese MP4s, captions,
transcripts and download links. Serve previews with `scripts/preview.py` so video
chapter seeking receives HTTP byte-range support.

## Demo booking and workflow scenarios

The EN/VI product hero links to `#book-demo`, where visitors can contact Duy on
Facebook to agree on a demo time. This is a contact request, not an automatically
confirmed calendar reservation. Localized copy and the destination live in
`landing.booking` in both Studio content files.

The illustrative workflow provides three scenarios and six processing stages,
including rules and a simulated human review. It runs locally without submitting
requests or calling a model. Each scenario has its own sample request and result;
selection restarts the illustration. Reduced motion and static no-JavaScript viewing
remain available. Check with `scripts/check_studio_demo.cjs` using the same
`PLAYWRIGHT_MODULE` and `SITE_PREVIEW` variables as other browser checks.

The workflow illustration uses a 16:9 canvas with two rows of connected nodes
and a dashed revision path. Completed connectors reflect the simulated run.
On small screens the diagram scrolls horizontally to keep node labels readable.

The workflow now autoplays while its canvas is visible, with bright SVG particles
traveling along the actual connector paths. It pauses offscreen or in hidden tabs,
provides a pause/resume control, and shows a static completed result for reduced
motion. The former run button is removed. `check_studio_demo.cjs` verifies the
automatic loop, actual particle movement and pause behavior in both languages.
