# xDraft launch: pages, redirects, order

MindMap AI becomes **xDraft** with app version 2.0.0 (ADR 0017 in the `tdduydev/xdev-xdraft` repository, task MM-177). This branch adds the xDraft pages and points the product directory and home page to them. It does not remove or change any MindMap AI page. The old URLs move to the new ones through Cloudflare redirects, because GitHub Pages cannot answer with a 301 for a page that exists.

## What this branch changes

- New pages from `src/apps/xdraft.{en,vi,ja}.json`: `/xdraft/`, `/xdraft/privacy/`, `/xdraft/terms/`, `/xdraft/support/`, with the same four under `/vi/` and `/ja/`.
- Privacy, terms and support are the MindMap AI text with only the product name and links changed (`MindMap AI` → `xDraft`, `MindMap AI Pro` → `xDraft Pro`, `MindMap AI Backup` → `xDraft Backup`). Effective dates stay the same. No data commitment was added or removed.
- `/products/`, `/vi/products/` and the home page list xDraft instead of MindMap AI.
- `/brand/` and `/vi/brand/` show the xDraft lockup (X + DRAFT / AI DIAGRAM STUDIO).
- `src/apps/mindmap.*.json` has `"superseded_by": "xdraft"`. `check_site.py` then accepts that the product directory no longer links to `/mindmap/`.

## What stays

- `/mindmap/`, `/mindmap/privacy/`, `/mindmap/terms/` and `/mindmap/support/` in EN, VI and JA are still built. MindMap AI 1.x and App Store Connect use these URLs until 2.0.0 ships.
- `/mindmap/m/`, the map link page that also opens the App Clip. It is never redirected: builds 1.0 to 1.2 and links already sent use it (ADR 0017).
- `/.well-known/apple-app-site-association`. It is never redirected and not changed.

## Redirects to create in Cloudflare

All entries are **301**, with the **query string kept**, and match the **exact path** only. Do not use subpath or prefix matching: `/mindmap/` must not catch `/mindmap/m/`.

| Source | Target |
| --- | --- |
| `https://xdev.asia/mindmap/` | `https://xdev.asia/xdraft/` |
| `https://xdev.asia/mindmap/privacy/` | `https://xdev.asia/xdraft/privacy/` |
| `https://xdev.asia/mindmap/terms/` | `https://xdev.asia/xdraft/terms/` |
| `https://xdev.asia/mindmap/support/` | `https://xdev.asia/xdraft/support/` |
| `https://xdev.asia/vi/mindmap/` | `https://xdev.asia/vi/xdraft/` |
| `https://xdev.asia/vi/mindmap/privacy/` | `https://xdev.asia/vi/xdraft/privacy/` |
| `https://xdev.asia/vi/mindmap/terms/` | `https://xdev.asia/vi/xdraft/terms/` |
| `https://xdev.asia/vi/mindmap/support/` | `https://xdev.asia/vi/xdraft/support/` |
| `https://xdev.asia/ja/mindmap/` | `https://xdev.asia/ja/xdraft/` |
| `https://xdev.asia/ja/mindmap/privacy/` | `https://xdev.asia/ja/xdraft/privacy/` |
| `https://xdev.asia/ja/mindmap/terms/` | `https://xdev.asia/ja/xdraft/terms/` |
| `https://xdev.asia/ja/mindmap/support/` | `https://xdev.asia/ja/xdraft/support/` |
| `https://xdev.asia/mindmap` | `https://xdev.asia/xdraft/` |
| `https://xdev.asia/mindmap/privacy` | `https://xdev.asia/xdraft/privacy/` |
| `https://xdev.asia/mindmap/support` | `https://xdev.asia/xdraft/support/` |

The last three are the URLs without a trailing slash. MindMap AI 1.x opens these from `AppLinks.swift`. Without them, GitHub Pages first answers with a 301 to the slash form, and Cloudflare then redirects again. The result is the same page after two redirects instead of one.

Never redirect:

- `/mindmap/m`, `/mindmap/m/` or any path below it;
- `/.well-known/apple-app-site-association`.

[Unverified] The Cloudflare feature that fits an exact list of 15 paths is **Bulk Redirects**: one list with the entries above, *Preserve query string* on, *Subpath matching* and *Preserve path suffix* off. Check how many entries the zone's plan allows in the dashboard before you start. Single Redirect rules also work, with one rule for each row.

## Release order

ADR 0017 requires that the new pages and the redirects work before a build that links to them is submitted. `AppLinks` changes only after that.

1. **Before merging:**
   - a person checks the trademark (ADR 0017);
   - a native speaker reviews the VI and JA copy of the overview (`src/apps/xdraft.vi.json`, `src/apps/xdraft.ja.json`);
   - the product owner approves the overview text and the pricing lines (Free: Mind Map and Flowchart; Pro USD 19.99: the Architecture family, AI conversions, Suggest Messages).
   Merging makes xDraft public on the product directory, so merge close to the 2.0.0 submission.
2. **Merge `xdraft` into `main`.** The *Build and deploy site* workflow builds, checks and deploys to GitHub Pages. Wait until the run is green.
3. **Check the new pages:** each command below should print `HTTP/2 200`.

   ```sh
   for p in xdraft/ xdraft/privacy/ xdraft/terms/ xdraft/support/ vi/xdraft/ vi/xdraft/privacy/ ja/xdraft/ ja/xdraft/privacy/; do
     printf '%s ' "$p"; curl -sI "https://xdev.asia/$p" | head -1
   done
   ```

4. **Turn on the redirects** listed above in Cloudflare.
5. **Check the redirects and what must not move:**

   ```sh
   # Each line: 301 and the new location, in one hop.
   for p in mindmap mindmap/ mindmap/privacy mindmap/privacy/ mindmap/terms/ mindmap/support mindmap/support/ vi/mindmap/ vi/mindmap/privacy/ ja/mindmap/ ja/mindmap/support/; do
     printf '%s ' "$p"; curl -sI "https://xdev.asia/$p?from=check" | grep -i -E '^(HTTP|location)' | tr '\n' ' '; echo
   done
   # Must still answer 200 without a location header.
   curl -sI https://xdev.asia/mindmap/m/ | head -1
   curl -sI https://xdev.asia/.well-known/apple-app-site-association | head -1
   ```

   The location keeps `?from=check`. `/mindmap/m/` and the AASA answer `200`.
6. **App Store Connect:** change the Privacy Policy URL, the Support URL and the Marketing URL to the `/xdraft/` pages.
7. **App:** change `AppLinks.swift` to `https://xdev.asia/xdraft`, `/xdraft/privacy` and `/xdraft/support` in the 2.0.0 build, then submit it.
8. **Later:** once no supported build links to `/mindmap/…` any more, the old app pages can be removed from `src/apps/`. The redirects stay. `/mindmap/m/` and the AASA stay for as long as the App Clip and old links exist.

## Open for people

- Trademark check in classes 9 and 42 (VN, US, JP, EU) before the App Store name changes (ADR 0017).
- Native review of the VI and JA overview copy. The legal pages reuse the MindMap AI translations already published, with only the name changed. The JA legal pages keep their notice that the English version prevails.
- Cloudflare access to create the redirects; this repository cannot do it.
- When to merge: merging makes xDraft public on the product directory before the App Store shows the new name.
