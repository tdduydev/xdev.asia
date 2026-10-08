"""Pages for xDev apps: an overview plus legal and support documents, in EN and VI.

Each app is a pair of files, src/apps/<slug>.en.json and src/apps/<slug>.vi.json,
with the same structure, plus its icon under src/assets/apps/<slug>/. A new app
needs only those files: build.py and check_site.py discover them. An app may add
src/apps/<slug>.ja.json; only that app's pages then get a Japanese version.
"""
from html import escape, unescape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
APPS = ROOT / 'src/apps'
LANGUAGES = ['en', 'vi']
# Languages an app may add on its own; the rest of the site stays in LANGUAGES.
OPTIONAL_LANGUAGES = ['ja']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# Branch colours of the hero illustration, taken from the app's topic palette.
HUES = [('#0759ed', '#e2edff', '#0b3a8c'), ('#c27a1f', '#fbefe0', '#6d430c'), ('#23897b', '#def1ee', '#0f4c44')]


def load_apps():
    """Return one {language: content} mapping per app, sorted by slug, English first."""
    apps = []
    for english in sorted(APPS.glob('*.en.json')):
        slug = english.name[:-len('.en.json')]
        languages = LANGUAGES + [language for language in OPTIONAL_LANGUAGES if (APPS / f'{slug}.{language}.json').exists()]
        apps.append({language: json.loads((APPS / f'{slug}.{language}.json').read_text()) for language in languages})
    return apps


def app_routes(content):
    """Site paths of an app's pages, overview first."""
    return [content['slug'] + '/'] + [f"{content['slug']}/{document['slug']}/" for document in content['documents']]


def target(link, slug):
    # 'app:' names a page of the same app, so copy never hard-codes the site origin;
    # decorate() resolves @route:…@ relative to the current page and language.
    if not link.startswith('app:'):
        return link
    page, _, fragment = link[4:].partition('#')
    return f'@route:{slug}/' + (page + '/' if page else '') + '@' + ('#' + fragment if fragment else '')


def inline(text, slug):
    """Escape copy, then allow the only markup it needs: **strong** and [label](link)."""
    html = escape(text, quote=False)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    return re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: f'<a href="{escape(target(unescape(m.group(2)), slug), quote=True)}">{m.group(1)}</a>', html)


def readable_email(html):
    # xdev.asia sits behind Cloudflare, whose email obfuscation swaps addresses for
    # "[email protected]" until a script runs; these comments opt the contact out, so
    # App Review and visitors without JavaScript still see it.
    return re.sub(r'<a href="mailto:[^"]*">.*?</a>', lambda m: '<!--email_off-->' + m.group(0) + '<!--/email_off-->', html)


def format_date(iso, language):
    year, month, day = (int(part) for part in iso.split('-'))
    if language == 'ja':
        return f'{year}年{month}月{day}日'
    return f'{day} tháng {month} năm {year}' if language == 'vi' else f'{day} {MONTHS[month - 1]} {year}'


def app_bar(c, current):
    e = escape
    pages = [('', c['labels']['overview'])] + [(d['slug'], d['nav']) for d in c['documents']]
    links = ''.join(
        f'<a href="{target("app:" + slug, c["slug"])}"' + (' aria-current="page"' if slug == current else '') + f'>{e(label)}</a>'
        for slug, label in pages
    )
    return (f'<div class="app-bar"><div class="container app-bar-inner"><a class="app-bar-brand" href="{target("app:", c["slug"])}">'
            f'<img src="{c["icon"]}" alt="" width="28" height="28"><span>{e(c["short_name"])}</span></a>'
            f'<nav aria-label="{e(c["labels"]["pages"], quote=True)}">{links}</nav></div></div>')


def hero_map(m):
    """Static mind map drawing; it needs no script and scales with its viewBox."""
    e = escape
    width, height, cx, cy = 640, 400, 320, 190
    rows = [80, 190, 300]
    shapes = ''
    labels = ''
    for index, branch in enumerate(m['branches'][:6]):
        stroke, fill, ink = HUES[index % len(HUES)]
        left = index < 3
        y = rows[index % 3]
        node_x = 30 if left else 460
        start = cx - 85 if left else cx + 85
        end = node_x + 150 if left else node_x
        bend = -30 if left else 30
        shapes += f'<path d="M{start} {cy} C{start + bend} {cy} {end - bend} {y} {end} {y}" stroke="{stroke}" stroke-width="2.5" fill="none"/>'
        shapes += f'<rect x="{node_x}" y="{y - 22}" width="150" height="44" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        labels += f'<text x="{node_x + 75}" y="{y + 5}" fill="{ink}" font-size="14" font-weight="600" text-anchor="middle">{e(branch)}</text>'
    suggestion = (f'<path d="M{cx} {cy + 28} V{cy + 112}" stroke="#7c8ba3" stroke-width="2" stroke-dasharray="5 6"/>'
                  f'<rect x="{cx - 90}" y="{cy + 112}" width="180" height="44" rx="12" fill="#ffffff" stroke="#7c8ba3" stroke-width="1.8" stroke-dasharray="6 5"/>'
                  f'<text x="{cx}" y="{cy + 139}" fill="#0759ed" font-size="14" font-weight="600" text-anchor="middle">✦ {e(m["suggestion"])}</text>')
    center = (f'<rect x="{cx - 85}" y="{cy - 28}" width="170" height="56" rx="14" fill="#102544" stroke="#0759ed" stroke-width="2"/>'
              f'<text x="{cx}" y="{cy + 6}" fill="#ffffff" font-size="16" font-weight="650" text-anchor="middle">{e(m["center"])}</text>')
    return (f'<figure class="app-hero-visual"><div class="app-window-bar" aria-hidden="true"><span></span><span></span><span></span></div>'
            f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{e(m["label"], quote=True)}" font-family="Inter, Arial, sans-serif">'
            f'<title>{e(m["label"])}</title>{shapes}{suggestion}{center}{labels}</svg></figure>')


def hero_screenshot(s):
    """A screenshot of the app in the hero frame, for apps without a map illustration."""
    e = escape
    return (f'<figure class="app-hero-visual"><div class="app-window-bar" aria-hidden="true"><span></span><span></span><span></span></div>'
            f'<img src="{e(s["src"], quote=True)}" alt="{e(s["alt"], quote=True)}" width="{s["width"]}" height="{s["height"]}"></figure>')


def heading(label, title, intro=None):
    e = escape
    text = f'<p>{e(intro)}</p>' if intro else ''
    return f'<div class="app-section-heading"><p class="eyebrow">{e(label)}</p><h2>{e(title)}</h2>{text}</div>'


def render_overview(c):
    e = escape
    o = c['overview']
    slug = c['slug']
    actions = ''.join(
        f'<a class="{"button primary" if a.get("primary") else "text-link"}" href="{target(a["href"], slug)}">{e(a["label"])}'
        f'<span aria-hidden="true">{"↓" if a["href"].startswith("#") else "→"}</span></a>'
        for a in o['actions']
    )
    if c.get('store_url'):
        actions = f'<a class="button black" href="{e(c["store_url"], quote=True)}">{e(o.get("store_action", "App Store"))}<span aria-hidden="true">↗</span></a>' + actions
    status = f'<p class="app-status"><span aria-hidden="true"></span>{e(o["status"])}</p>' if o.get('status') else ''
    visual = hero_map(o['map']) if o.get('map') else hero_screenshot(o['screenshot']) if o.get('screenshot') else ''
    sections = ''
    jumps = []
    if 'features' in o:
        f = o['features']
        items = ''.join(f'<article><span class="app-number">{i:02d}</span><h3>{e(item["title"])}</h3><p>{e(item["text"])}</p></article>' for i, item in enumerate(f['items'], 1))
        sections += f'<section class="container app-section" id="features">{heading(f["label"], f["title"], f.get("intro"))}<div class="app-features">{items}</div></section>'
        jumps.append(('features', f['label']))
    if 'privacy' in o:
        p = o['privacy']
        points = ''.join(f'<li>{e(point)}</li>' for point in p['points'])
        sections += (f'<section class="app-privacy" id="privacy"><div class="container app-privacy-inner"><div><p class="eyebrow">{e(p["label"])}</p><h2>{e(p["title"])}</h2>'
                     f'<p>{e(p["text"])}</p><a class="button white" href="{target(p["href"], slug)}">{e(p["action"])}<span aria-hidden="true">→</span></a></div><ul>{points}</ul></div></section>')
        jumps.append(('privacy', p['label']))
    if 'pricing' in o:
        p = o['pricing']
        plans = ''
        for plan in p['plans']:
            note = f'<span>{e(plan["price_note"])}</span>' if plan.get('price_note') else ''
            items = ''.join(f'<li>{e(item)}</li>' for item in plan['items'])
            plans += f'<article class="app-plan"><h3>{e(plan["name"])}</h3><p class="app-price"><strong>{e(plan["price"])}</strong>{note}</p><p class="app-plan-text">{e(plan["text"])}</p><ul>{items}</ul></article>'
        sections += f'<section class="container app-section" id="pricing">{heading(p["label"], p["title"], p.get("intro"))}<div class="app-plans">{plans}</div><p class="app-plan-note">{e(p["note"])}</p></section>'
        jumps.append(('pricing', p['label']))
    if 'platforms' in o:
        p = o['platforms']
        items = ''.join(f'<article><div class="app-platform-top"><h3>{e(item["name"])}</h3><span class="app-pill">{e(item["status"])}</span></div><p>{e(item["text"])}</p></article>' for item in p['items'])
        languages = f'<p class="app-platform-note">{e(p["languages"])}</p>' if p.get('languages') else ''
        sections += f'<section class="container app-section" id="platforms">{heading(p["label"], p["title"])}<div class="app-platforms">{items}</div>{languages}</section>'
        jumps.append(('platforms', p['label']))
    help_ = o['help']
    cards = ''.join(f'<a href="{target("app:" + d["slug"], slug)}"><h3>{e(d["heading"])}</h3><p>{e(d["summary"])}</p><span>{e(d["nav"])} <span aria-hidden="true">→</span></span></a>' for d in c['documents'])
    contact = f'<p class="app-help-contact">{e(help_["contact"])} <a href="mailto:{e(c["email"], quote=True)}">{e(c["email"])}</a></p>'
    sections += f'<section class="container app-section" id="help">{heading(help_["label"], help_["title"])}<div class="app-doc-cards">{cards}</div>{contact}</section>'
    jumps.append(('help', help_['label']))
    jump_links = ''.join(f'<a href="#{anchor}">{e(label)}</a>' for anchor, label in jumps)
    return (f'<main id="main" class="app-page">{app_bar(c, "")}'
            f'<section class="container app-hero"><div class="app-hero-copy"><img class="app-icon" src="{c["icon"]}" alt="{e(c["icon_alt"], quote=True)}" width="104" height="104">'
            f'<p class="eyebrow">{e(o["eyebrow"])}</p><h1>{e(o["headline"])}</h1><p class="lead">{e(o["lead"])}</p>{status}'
            f'<div class="app-actions">{actions}</div><p class="app-hero-note">{e(o["note"])}</p></div>{visual}</section>'
            f'<nav class="container app-jumps" aria-label="{e(c["labels"]["page_contents"], quote=True)}">{jump_links}</nav>{sections}</main>')


def render_document(c, d, language):
    e = escape
    slug = c['slug']
    labels = c['labels']
    date = ''
    if d.get('effective_date'):
        date = f'<p class="app-doc-date">{e(labels["effective"])}: <time datetime="{d["effective_date"]}">{format_date(d["effective_date"], language)}</time></p>'
    # A translated legal page says which version prevails; it opens the page so it is read first.
    notice = f'<p class="app-doc-notice">{inline(d["translation_notice"], slug)}</p>' if d.get('translation_notice') else ''
    intro = ''.join(f'<p class="app-doc-lead">{inline(text, slug)}</p>' for text in d['intro'])
    sections = ''
    toc = ''
    for section in d['sections']:
        title = f'<h2>{e(section["title"])}</h2>' if section.get('title') else ''
        body = ''.join(f'<p>{inline(text, slug)}</p>' for text in section['paragraphs'])
        style = ' app-callout' if section.get('callout') else ''
        sections += f'<section id="{section["id"]}" class="app-doc-section{style}">{title}{body}</section>'
        toc += f'<li><a href="#{section["id"]}">{e(section.get("toc") or section["title"])}</a></li>'
    aside = (f'<aside class="app-doc-aside"><nav class="app-toc" aria-label="{e(labels["on_this_page"], quote=True)}"><p>{e(labels["on_this_page"])}</p><ol>{toc}</ol></nav>'
             f'<div class="app-doc-provider"><p>{e(labels["provided_by"])}</p><strong>{e(c["provider"])}</strong><a href="mailto:{e(c["email"], quote=True)}">{e(c["email"])}</a></div></aside>')
    return (f'<main id="main" class="app-page">{app_bar(c, d["slug"])}<div class="container app-doc-layout"><article class="app-doc">{notice}'
            f'<p class="eyebrow">{e(c["name"])}</p><h1>{e(d["heading"])}</h1>{date}{intro}{sections}</article>{aside}</div></main>')


def render_app_pages(language, c):
    """Yield (path, title, description, body) for every page of one app in one language."""
    o = c['overview']
    yield c['slug'] + '/', o['title'], o['description'], readable_email(render_overview(c))
    for d in c['documents']:
        yield f"{c['slug']}/{d['slug']}/", d['title'], d['description'], readable_email(render_document(c, d, language))
