# xDev Asia

Bilingual product landing page for **XDev AI Studio** and **XDev Forge**.

- `/` — English (default, including browsers configured for Vietnamese).
- `/vi/` — Vietnamese.
- The EN / VI links switch languages without JavaScript. Each language has its own URL, document language, page title, description, and alternate-language metadata.

## Preview

```sh
python3 -m http.server 4321 --directory dist --bind 127.0.0.1
```

Open http://127.0.0.1:4321/ or http://127.0.0.1:4321/vi/.

## Edit and build

Edit `src/index.vi.html` and the English translation mapping in `scripts/build.py`, then run:

```sh
python3 scripts/build.py
```

Shared styles are in `dist/styles.css`; brand assets are in `dist/assets/`. The generated HTML is tracked so the site can be served directly from `dist/`, without installing packages or running JavaScript. The build uses only the Python standard library.

The original logo, favicon, and font were retrieved from blog.xdev.asia on 2026-09-20. Product links point to ai-studio.xdev.asia and forge.xdev.asia.

## Hosting

Serve `dist/` using any static web server with directory-index support. The existing Sites project is identified by `.openai/hosting.json`; that file contains no credentials. Sites publication requires pushing the same source revision to its managed repository and saving/deploying the packaged static files. A GitHub push alone does not publish the Site or change DNS.
