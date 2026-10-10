# xDraft launch: pages, redirects, order

MindMap AI becomes **xDraft** with app version 2.0.0 (ADR 0017 in the `tdduydev/xdev-xdraft` repository, task MM-177). The product owner decided on 2026-10-10 to publish the xDraft pages at once and to retire the MindMap AI pages.

## What changed on the site

- New pages from `src/apps/xdraft.{en,vi,ja}.json`: `/xdraft/`, `/xdraft/privacy/`, `/xdraft/terms/`, `/xdraft/support/`, with the same four under `/vi/` and `/ja/`.
- Privacy, terms and support are the MindMap AI text with only the product name and links changed (`MindMap AI` → `xDraft`, `MindMap AI Pro` → `xDraft Pro`, `MindMap AI Backup` → `xDraft Backup`). Effective dates stay the same. No data commitment was added or removed.
- `/products/`, `/vi/products/` and the home page list xDraft instead of MindMap AI. `/brand/` and `/vi/brand/` show the xDraft lockup (X + DRAFT / AI DIAGRAM STUDIO).
- The MindMap AI app pages are gone (`src/apps/mindmap.*.json` and its icon). Each of their twelve paths now holds a page generated from `src/redirects.json` that replaces itself with the matching xDraft page. It keeps the query and the fragment, is `noindex`, and names the xDraft page as canonical. MindMap AI 1.x and the current App Store Connect URLs therefore still reach the right page, through the browser instead of a 301.
- `/mindmap/m/` says xDraft instead of MindMap AI, copied from `docs/web/mindmap/m/` of the app repository.

## What stays

- The path `/mindmap/m/`: the map link page that also opens the App Clip. It is never redirected, because builds 1.0 to 1.2 and links already sent use it (ADR 0017).
- `/.well-known/apple-app-site-association`: never redirected and not changed.

## Redirects to create in Cloudflare

The redirect pages already send visitors on. A Cloudflare 301 is still better: search engines and link checkers see a permanent move, and there is one hop instead of a page load. All entries are **301**, with the **query string kept**, and match the **exact path** only. Do not use subpath or prefix matching: `/mindmap/` must not catch `/mindmap/m/`.

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

Keep `src/redirects.json` and this list the same.

Never redirect:

- `/mindmap/m`, `/mindmap/m/` or any path below it;
- `/.well-known/apple-app-site-association`.

[Unverified] The Cloudflare feature that fits an exact list of 15 paths is **Bulk Redirects**: one list with the entries above, *Preserve query string* on, *Subpath matching* and *Preserve path suffix* off. Check how many entries the zone's plan allows in the dashboard before you start. Single Redirect rules also work, with one rule for each row.

## Release order

ADR 0017 requires that the new pages work before a build that links to them is submitted. `AppLinks` changes only after that.

1. Merge into `main`. The *Build and deploy site* workflow builds, checks and deploys to GitHub Pages. Wait until the run is green.
2. **Check the new pages and the redirect pages:**

   ```sh
   # Each line: HTTP/2 200.
   for p in xdraft/ xdraft/privacy/ xdraft/terms/ xdraft/support/ vi/xdraft/ vi/xdraft/privacy/ ja/xdraft/ ja/xdraft/privacy/ mindmap/m/ .well-known/apple-app-site-association; do
     printf '%s ' "$p"; curl -sI "https://xdev.asia/$p" | head -1
   done
   # Each old page names its xDraft page as canonical.
   curl -s https://xdev.asia/mindmap/privacy/ | grep -o 'rel="canonical" href="[^"]*"'
   ```

3. **Optional: turn on the Cloudflare redirects** listed above, then check them:

   ```sh
   # Each line: 301 and the new location, in one hop.
   for p in mindmap mindmap/ mindmap/privacy mindmap/privacy/ mindmap/terms/ mindmap/support mindmap/support/ vi/mindmap/ vi/mindmap/privacy/ ja/mindmap/ ja/mindmap/support/; do
     printf '%s ' "$p"; curl -sI "https://xdev.asia/$p?from=check" | grep -i -E '^(HTTP|location)' | tr '\n' ' '; echo
   done
   # Must still answer 200 without a location header.
   curl -sI https://xdev.asia/mindmap/m/ | head -1
   curl -sI https://xdev.asia/.well-known/apple-app-site-association | head -1
   ```

4. **App Store Connect:** change the Privacy Policy URL, the Support URL and the Marketing URL to the `/xdraft/` pages.
5. **App:** change `AppLinks.swift` to `https://xdev.asia/xdraft`, `/xdraft/privacy` and `/xdraft/support` in the 2.0.0 build, then submit it.
6. **Later:** the redirect pages stay for as long as a supported build or an old link may point at `/mindmap/…`. `/mindmap/m/` and the AASA stay for as long as the App Clip and old links exist.

## Open for people

- Trademark check in classes 9 and 42 (VN, US, JP, EU) before the App Store name changes (ADR 0017).
- Native review of the VI and JA overview copy. The legal pages reuse the MindMap AI translations already published, with only the name changed. The JA legal pages keep their notice that the English version prevails.
- Cloudflare access to create the optional 301 redirects; this repository cannot do it.
- xDraft is public on the site before the App Store shows the new name; the product owner accepted this on 2026-10-10.
