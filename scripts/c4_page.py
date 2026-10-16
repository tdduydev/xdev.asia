"""Render the independent, bilingual C4 Model open book on xDev Asia.

The content lives in src/c4.en.json and src/c4.vi.json. Only chapters with
sections are published; upcoming chapter cards are intentionally non-clickable.
"""
from html import escape
import math

def e(value):
    return escape(str(value), quote=True)

def published_chapters(content):
    return [item for item in content['chapters'] if item['sections']]

def chapter_route(slug):
    return '@route:c4-model/chapters/' + slug + '/@'

def chapter_link(item, label):
    return f'<a href="{chapter_route(item["slug"])}">{e(label)}</a>'

def level_diagram(index, language):
    """Original, CSS-rendered teaching examples, never customer architecture."""
    labels = {
        'en': [
            ('External System', 'Data Platform', 'Operator', 'Domain System'),
            ('Web Portal', 'API Service', 'Data Store', 'Message Queue'),
            ('Controller', 'Validator', 'Matching Service', 'Repository'),
            ('IMatcher', 'RuleMatcher', 'ScoreMatcher', 'Strategy')
        ],
        'vi': [
            ('Hệ thống ngoài', 'Nền tảng dữ liệu', 'Người dùng', 'CSDL chuyên ngành'),
            ('Web Portal', 'API Service', 'Data Store', 'Message Queue'),
            ('Controller', 'Validator', 'Matching Service', 'Repository'),
            ('IMatcher', 'RuleMatcher', 'ScoreMatcher', 'Strategy')
        ]
    }[language][index]
    boxes = ''.join(
        f'<div class="c4-node c4-node-{i}"><span class="c4-node-index">{i+1:02d}</span><strong>{e(label)}</strong></div>'
        for i, label in enumerate(labels)
    )
    return f'<div class="c4-diagram c4-diagram-{index}" role="img" aria-label="{e("Architectural illustration: " + ", ".join(labels))}"><div class="c4-diagram-lines" aria-hidden="true"><i></i><i></i><i></i></div>{boxes}</div>'

def level_explorer(content):
    ui = content['ui']
    tabs = ''.join(
        f'<button type="button" role="tab" id="c4-tab-{index}" aria-controls="c4-panel-{index}" '
        f'aria-selected="{str(index == 0).lower()}" data-c4-tab="{index}" tabindex="{0 if index == 0 else -1}">'
        f'<span>{e(level["code"])}</span><strong>{e(level["name"])}</strong></button>'
        for index, level in enumerate(content['levels'])
    )
    panels = ''
    for index, level in enumerate(content['levels']):
        panels += (
            f'<section role="tabpanel" id="c4-panel-{index}" aria-labelledby="c4-tab-{index}" '
            f'data-c4-panel="{index}"{" hidden" if index else ""}>'
            f'{level_diagram(index, content["language"])}'
            f'<div class="c4-diagram-caption"><div><span>{e(level["name"])}</span>'
            f'<h3>{e(level["title"])}</h3><p>{e(level["description"])}</p></div>'
            f'<dl><dt>{e(ui["labelContext"])}</dt><dd>{e(level["scope"])}</dd>'
            f'<dt>{e(ui["labelExample"])}</dt><dd>{e(level["example"])}</dd></dl></div></section>'
        )
    return (
        '<div class="c4-explorer">'
        f'<div class="c4-explorer-top"><span><span class="c4-online-dot"></span>C4 / ARCHITECTURE MAP</span><span>01—04</span></div>'
        f'<div class="c4-level-tabs" role="tablist" aria-label="{e(ui["keyboard"])}">{tabs}</div>'
        f'<div class="c4-level-panels">{panels}</div></div>'
    )

def chapter_card(content, item):
    ui = content['ui']
    ready = bool(item['sections'])
    search = e(' '.join([item['title'], item['summary'], content['parts'][item['part'] - 1]]).lower())
    if ready:
        action = f'<span class="c4-card-link">{e(ui["read"])} <span aria-hidden="true">↗</span></span>'
        start = f'<a class="c4-chapter-card" href="{chapter_route(item["slug"])}" data-c4-chapter data-search="{search}">'
        end = '</a>'
    else:
        action = f'<span class="c4-coming">{e(ui["planned"])}</span>'
        start = f'<article class="c4-chapter-card c4-card-planned" data-c4-chapter data-search="{search}">'
        end = '</article>'
    return (
        start + f'<div class="c4-card-meta"><span>{item["number"]:02d} / 15</span>'
        f'<span class="c4-pill{" c4-pill-wip" if not ready else ""}">{e(ui["published"] if ready else ui["planned"])}</span></div>'
        f'<h3>{e(item["title"])}</h3><p>{e(item["summary"])}</p>{action}' + end
    )

def render_index(content):
    ui = content['ui']
    ready = len(published_chapters(content))
    parts = ''
    for index, title in enumerate(content['parts'], 1):
        entries = [item for item in content['chapters'] if item['part'] == index]
        parts += (
            f'<section class="c4-chapter-group" data-c4-group><div class="c4-group-head"><span>{e(ui["part"])} {index:02d}</span>'
            f'<h3>{e(title)}</h3></div><div class="c4-chapter-grid">'
            + ''.join(chapter_card(content, item) for item in entries) + '</div></section>'
        )
    resources = ''.join(f'<a href="{e(r["url"])}" target="_blank" rel="noopener noreferrer">{e(r["title"])}<span aria-hidden="true">↗</span></a>' for r in content['resources'])
    return f'''<main id="main" class="c4-site c4-landing">
<section class="c4-hero container" aria-labelledby="c4-title">
<div class="c4-hero-copy"><p class="c4-kicker"><span class="c4-spark">✳</span> {e(content["eyebrow"])}</p>
<h1 id="c4-title"><span>C4</span> Model<span class="c4-title-period">.</span></h1>
<h2>{e(content["subtitle"])}</h2><p class="c4-lead">{e(content["description"])}</p>
<div class="c4-actions"><a class="c4-action-primary" href="{chapter_route(content["chapters"][0]["slug"])}">{e(ui["start"])}<span aria-hidden="true">↗</span></a>
<a class="c4-action-secondary" href="#c4-chapters">{e(ui["toc"])}<span aria-hidden="true">↓</span></a></div>
<div class="c4-hero-count"><span><strong>04</strong> Context · Container · Component · Code</span>
<span><strong>{ready:02d}</strong> / 15 {e(ui["published"]).lower()}</span></div></div>
<div class="c4-hero-visual">{level_explorer(content)}</div>
</section>
<section class="c4-intro-band"><div class="container c4-intro-grid"><div><p class="c4-eyebrow">01 / EXPLORE</p>
<h2>{e(ui["levels"])}</h2></div><div><p>{e(ui["levelsIntro"])}</p><p class="c4-intro-callout">{e(ui["note"])}</p></div></div></section>
<section id="c4-chapters" class="c4-book container">
<div class="c4-section-head"><div><p class="c4-eyebrow">02 / THE BOOK</p><h2>{e(ui["chapters"])}</h2><p>{e(ui["chaptersIntro"])}</p></div>
<div class="c4-search"><label for="c4-search-input">{e(ui["all"])}</label><input id="c4-search-input" type="search" data-c4-search placeholder="{e(ui["search"])}" autocomplete="off"></div></div>
<div class="c4-book-grid">{parts}</div><p class="c4-search-empty" data-c4-empty hidden>{e(ui["empty"])}</p></section>
<section class="c4-resources container"><div><p class="c4-eyebrow">03 / REFERENCES</p><h2>{e(ui["resources"])}</h2><p>{e(ui["disclaimer"])}</p></div><div class="c4-resource-links">{resources}</div></section>
</main>'''

def render_chapter(content, item):
    ui = content['ui']
    ready = published_chapters(content)
    current = ready.index(item)
    previous = ready[current-1] if current > 0 else None
    following = ready[current+1] if current + 1 < len(ready) else None
    word_count = sum(len(' '.join(s.get('paragraphs', [])).split()) + sum(len(p.split()) for p in s.get('points', [])) for s in item['sections'])
    read_minutes = max(2, math.ceil(word_count / (180 if content['language'] == 'vi' else 220)))
    sections = ''
    for i, section in enumerate(item['sections'], 1):
        body = ''.join(f'<p>{e(p)}</p>' for p in section.get('paragraphs', []))
        points = section.get('points', [])
        if points:
            body += '<ul class="c4-points">' + ''.join(f'<li>{e(point)}</li>' for point in points) + '</ul>'
        sections += f'<section class="c4-reading-section" id="section-{i}"><span class="c4-section-index">{i:02d} / {len(item["sections"]):02d}</span><h2>{e(section["heading"])}</h2>{body}</section>'
    if item.get('questions'):
        sections += (
            '<section class="c4-questions"><p class="c4-eyebrow">REFLECT</p>'
            f'<h2>{e(ui["question"])}</h2><ol>'
            + ''.join(f'<li>{e(q)}</li>' for q in item['questions']) + '</ol></section>'
        )
    links = ''
    if previous:
        links += f'<a class="c4-chapter-nav-link" href="{chapter_route(previous["slug"])}"><span>← {e(ui["previous"])}</span><strong>{e(previous["title"])}</strong></a>'
    if following:
        links += f'<a class="c4-chapter-nav-link" href="{chapter_route(following["slug"])}"><span>{e(ui["next"])} →</span><strong>{e(following["title"])}</strong></a>'
    toc = ''.join(f'<a href="#section-{i}"><span>{i:02d}</span>{e(section["heading"])}</a>' for i,section in enumerate(item['sections'],1))
    sidebar = ''
    for group_no, part_name in enumerate(content['parts'], 1):
        group = [ch for ch in content['chapters'] if ch['part'] == group_no]
        sidebar += f'<div class="c4-reader-part"><strong>{e(ui["part"])} {group_no:02d} · {e(part_name)}</strong>'
        for ch in group:
            if ch['sections']:
                selected = ' aria-current="page"' if ch['slug'] == item['slug'] else ''
                sidebar += f'<a href="{chapter_route(ch["slug"])}"{selected}><span>{ch["number"]:02d}</span>{e(ch["title"])}</a>'
            else:
                sidebar += f'<span class="c4-reader-soon"><span>{ch["number"]:02d}</span>{e(ch["title"])}</span>'
        sidebar += '</div>'
    return f'''<main id="main" class="c4-site c4-reader">
<div class="container c4-crumb"><a href="@route:c4-model/@">C4 Model</a><span>/</span><span>{e(ui["part"])} {item["part"]:02d}</span><span>/</span><span>{item["number"]:02d}</span></div>
<div class="container c4-reader-grid">
<aside class="c4-sidebar"><a class="c4-back" href="@route:c4-model/@">← {e(ui["back"])}</a><nav aria-label="{e(ui["toc"])}">{sidebar}</nav></aside>
<article class="c4-article">
<div class="c4-article-intro"><p class="c4-eyebrow">{e(ui["part"])} {item["part"]:02d} / {item["number"]:02d} — {e(ui["reading"])}</p>
<h1>{e(item["title"])}</h1><p class="c4-article-deck">{e(item["summary"])}</p>
<div class="c4-article-meta"><span>{e(ui["published"])}</span><span>·</span><span>~{read_minutes} {e(ui["readTime"])}</span><span>·</span><span>xDev Asia</span></div></div>
<nav class="c4-inpage" aria-label="{e(ui["contents"])}"><strong>{e(ui["contents"])}</strong>{toc}</nav>
<div class="c4-prose">{sections}</div><aside class="c4-takeaway"><span>✳</span><div><strong>{e(ui["noteTitle"])}</strong><p>{e(ui["note"])}</p></div></aside>
<nav class="c4-chapter-nav" aria-label="{e(ui["toc"])}">{links}</nav>
<div class="c4-chapter-foot"><p>{e(ui["review"])}</p><a href="https://c4model.com/" target="_blank" rel="noopener noreferrer">{e(ui["reference"])} ↗</a></div>
</article></div></main>'''
