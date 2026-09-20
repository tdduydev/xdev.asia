# xDev Asia

Static English/Vietnamese product website and user guides for XDev AI Studio. English is the default. Forge is not included in the generated site.

## Routes

| English | Vietnamese | Purpose |
| --- | --- | --- |
| `/` | `/vi/` | xDev home; product links lead to the local overview |
| `/ai-studio/` | `/vi/ai-studio/` | Product introduction; explicit link to the application |
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
python3 -m http.server 4321 --directory dist --bind 127.0.0.1
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

## CI/CD: GitHub Pages (prepared, not enabled or deployed)

`.github/workflows/site.yml` builds and validates pull requests and pushes to `main`, then uploads the `xdev-site` artifact for review. Those events **do not deploy**.

Deployment requires a manual **Run workflow** on `main` with **deploy** checked. The deploy job uses only the artifact produced by the successful build in that same run. No repository changes, Git pushes, or Sites publication are performed by this workflow.

One-time setup, to perform only when ready to move hosting:

1. Push the reviewed workflow and source to GitHub.
2. In repository **Settings → Pages**, select **GitHub Actions** as the source.
3. Set the repository variable `SITE_URL` to the published origin. For a first test without a custom domain, use `https://tdduydev.github.io/xdev.asia`.
4. Optionally require a reviewer on the `github-pages` environment.
5. Run **Build and deploy site** on `main`, check **deploy**, and inspect the deployment URL.
6. To use `xdev.asia`, configure the custom domain in Pages and switch its DNS only after the Pages deployment is verified. Existing Sites DNS records do not route to GitHub Pages. Do not change blog or product subdomains.

Authentication uses GitHub's scoped `GITHUB_TOKEN`/OIDC; no personal token is needed. Build has read-only repository permissions; only deployment receives `pages: write` and `id-token: write`.

Official setup: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

The existing `.openai/hosting.json` remains as the previous Sites project reference. It contains no credentials and is not used by GitHub Pages. This change does not publish to Sites, migrate DNS, or enable GitHub Pages by itself.

## Content basis

The introductory guides were checked against the adjacent XDev AI Studio source on 2026-09-20: application creation, draft editor, publish action, knowledge creation wizard, and workflow editor. They describe basic user flows, not an exhaustive reference. Available actions depend on workspace permissions and configuration. Update both language files when the product changes.

The logo, favicon and font were retrieved from blog.xdev.asia on 2026-09-20. The application itself is at https://ai-studio.xdev.asia.
