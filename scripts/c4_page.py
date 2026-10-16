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
    return '@route:xdraft/c4-model/' + slug + '/@'

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


def reading_minutes(item, language):
    count = sum(len(' '.join(section.get('paragraphs', [])).split()) +
                sum(len(point.split()) for point in section.get('points', []))
                for section in item.get('sections', []))
    return max(2, math.ceil(count / (180 if language == 'vi' else 220)))

def blog_card(content, item, featured=False):
    ui, labels = content['ui'], content['blog']
    category = content['parts'][item['part'] - 1]
    ready = bool(item['sections'])
    search = e(' '.join((item['title'], item['summary'], category)).casefold())
    info = (f'<span>{e(category)}</span><span aria-hidden="true">·</span>'
            f'<span>{reading_minutes(item, content["language"])} {e(labels["minutes"])}</span>') if ready else f'<span>{e(category)}</span>'
    tag = 'a' if ready else 'article'
    attr = (f' href="{chapter_route(item["slug"])}"' if ready else '')
    klass = 'c4-post-card' + (' c4-post-pending' if not ready else '') + (' c4-post-featured' if featured else '')
    content_html = (
        f'<div class="c4-post-card-overline"><span class="c4-post-num">{item["number"]:02d} / 15</span>'
        f'<span class="c4-post-category">{e(category)}</span></div>'
        f'<div class="c4-post-art c4-post-art-{item["number"] % 4}" aria-hidden="true">'
        f'<span>CONT<span class="c4-art-emph">EXT</span> / CODE</span><b>{item["number"]:02d}</b><i></i></div>'
        f'<div class="c4-post-card-copy"><div class="c4-post-meta">{info}</div>'
        f'<h3>{e(item["title"])}</h3><p>{e(item["summary"])}</p>'
        f'<span class="c4-post-link">{e(ui["read"] if ready else ui["planned"])} '
        + ('<span aria-hidden="true">↗</span>' if ready else '') + '</span></div>'
    )
    return (f'<{tag} class="{klass}"{attr} data-c4-chapter data-c4-topic="{item["part"]}" '
            f'data-search="{search}">{content_html}</{tag}>')

def render_index(content):
    ui, labels = content['ui'], content['blog']
    articles = published_chapters(content)
    lead = articles[0]
    article_cards = ''.join(blog_card(content, item) for item in content['chapters'][1:])
    topic_filters = ''.join(
        f'<button type="button" data-c4-filter="{i}" aria-pressed="false">{e(title)}</button>'
        for i, title in enumerate(content['parts'], 1)
    )
    resources = ''.join(
        f'<a href="{e(item["url"])}" target="_blank" rel="noopener noreferrer">'
        f'{e(item["title"])} <span aria-hidden="true">↗</span></a>' for item in content['resources']
    )
    return f'''<main id="main" class="c4-site c4-blog">
<section class="container c4-blog-hero">
<div class="c4-blog-breadcrumb"><a href="@route:xdraft/@">xDraft</a><span>/</span><span>C4 Model</span><span class="c4-blog-pulse" aria-hidden="true">●</span></div>
<p class="c4-eyebrow">{e(labels["kicker"])}</p>
<div class="c4-blog-hero-grid"><div class="c4-blog-hero-copy">
<h1><span>C4 Model.</span><br>{e(ui["chapters"])}</h1>
<p class="c4-blog-tagline">{e(content["subtitle"])}</p>
<p class="c4-blog-introduction">{e(content["description"])}</p>
<div class="c4-blog-hero-actions"><a class="c4-action-primary" href="{chapter_route(lead["slug"])}">{e(ui["start"])} ↗</a>
<a class="c4-action-secondary" href="#c4-chapters">{e(ui["toc"])} ↓</a></div>
<p class="c4-blog-byline"><span class="c4-blog-dot"></span> xDev Editorial <span aria-hidden="true">/</span> {len(articles)} {e(labels["articleCount"])}</p>
</div><div class="c4-blog-hero-art">{level_explorer(content)}</div></div>
</section>
<section class="container c4-blog-feature">
<div class="c4-blog-feature-label"><span>{e(labels["featured"])}</span><span>01 — C4</span></div>
<a class="c4-blog-feature-layout" href="{chapter_route(lead["slug"])}">
<div class="c4-feature-visual" aria-hidden="true"><span>THE ARCHITECTURE SERIES</span>
<div class="c4-feature-shapes"><b>Context</b><b>Container</b><b>Component</b><b>Code</b></div><span>© xDev Architecture Notes</span></div>
<div class="c4-feature-copy"><div class="c4-post-meta"><span>{e(content["parts"][lead["part"]-1])}</span><span>·</span><span>{reading_minutes(lead,content["language"])} {e(labels["minutes"])}</span></div>
<h2>{e(lead["title"])}</h2><p>{e(lead["summary"])}</p>
<span class="c4-feature-read">{e(ui["read"])} ↗</span></div></a></section>
<section class="container c4-blog-list" id="c4-chapters">
<div class="c4-blog-section-top"><div><p class="c4-eyebrow">{e(labels["browse"])}</p><h2>{e(ui["chapters"])}</h2>
<p>{e(ui["chaptersIntro"])}</p></div><div class="c4-search"><label for="c4-search-input">{e(ui["all"])}</label>
<input id="c4-search-input" data-c4-search type="search" placeholder="{e(ui["search"])}" autocomplete="off"></div></div>
<div class="c4-topic-filter" role="group" aria-label="{e(labels["browse"])}">
<button type="button" data-c4-filter="0" aria-pressed="true">{e(labels["allTopics"])}</button>{topic_filters}</div>
<div class="c4-blog-card-grid">{article_cards}</div><p class="c4-search-empty" data-c4-empty hidden>{e(ui["empty"])}</p></section>
<section class="c4-blog-tool-promo"><div class="container c4-blog-promo-layout"><div><p class="c4-eyebrow">{e(labels["appEyebrow"])}</p>
<h2>{e(labels["appTitle"])}</h2><p>{e(labels["appDescription"])}</p><a class="c4-action-primary" href="@route:xdraft/@">{e(labels["appAction"])} ↗</a></div>
<div class="c4-promo-diagram" aria-hidden="true"><span>xDraft / C4</span><div><b>SYSTEM</b><i>↓</i><b>CONTAINER</b><i>↓</i><b>COMPONENT</b></div></div></div></section>
<section class="container c4-blog-references"><div><p class="c4-eyebrow">REFERENCES</p><h2>{e(ui["resources"])}</h2>
<p>{e(ui["disclaimer"])}</p></div><div class="c4-resource-links">{resources}</div></section>
</main>'''

def render_chapter(content, item):
    ui, labels = content['ui'], content['blog']
    ready = published_chapters(content)
    current = ready.index(item)
    previous = ready[current-1] if current > 0 else None
    following = ready[current+1] if current + 1 < len(ready) else None
    parts = content['parts']
    sections = ''
    for i, section in enumerate(item['sections'], 1):
        text = ''.join(f'<p>{e(paragraph)}</p>' for paragraph in section.get('paragraphs', []))
        if section.get('points'):
            text += '<ul class="c4-points">' + ''.join(
                f'<li>{e(point)}</li>' for point in section['points']) + '</ul>'
        sections += (f'<section class="c4-reading-section" id="section-{i}">'
                     f'<span class="c4-section-index">{i:02d} / {len(item["sections"]):02d}</span>'
                     f'<h2>{e(section["heading"])}</h2>{text}</section>')
    if item.get('questions'):
        sections += ('<section class="c4-questions"><p class="c4-eyebrow">DISCUSSION</p>'
                     f'<h2>{e(ui["question"])}</h2><ol>' + ''.join(
                         f'<li>{e(q)}</li>' for q in item['questions']) + '</ol></section>')
    contents = ''.join(
        f'<a href="#section-{i}"><span>{i:02d}</span>{e(section["heading"])}</a>'
        for i, section in enumerate(item['sections'], 1)
    )
    related = ''.join(blog_card(content, ch) for ch in
                      [ch for ch in ready if ch['slug'] != item['slug']][:3])
    direction = ''
    for neighbor, direction_label, icon in ((previous, ui['previous'], '←'), (following, ui['next'], '→')):
        if neighbor:
            direction += (f'<a class="c4-chapter-nav-link" href="{chapter_route(neighbor["slug"])}">'
                          f'<span>{icon} {e(direction_label)}</span>'
                          f'<strong>{e(neighbor["title"])}</strong></a>')
    return f'''<main id="main" class="c4-site c4-blog c4-blog-article">
<div class="container c4-crumb"><a href="@route:xdraft/@">xDraft</a><span>/</span>
<a href="@route:xdraft/c4-model/@">C4 Model</a><span>/</span><span>{e(parts[item["part"]-1])}</span></div>
<div class="container c4-reader-grid"><aside class="c4-sidebar">
<a class="c4-back" href="@route:xdraft/c4-model/@">← {e(ui["back"])}</a>
<nav aria-label="{e(ui["toc"])}"><div class="c4-reader-part"><strong>{e(ui["toc"])}</strong>
{''.join(f'<a href="{chapter_route(ch["slug"])}"'+(' aria-current="page"' if ch["slug"]==item["slug"] else '')+f'><span>{ch["number"]:02d}</span>{e(ch["title"])}</a>' for ch in ready)}
</div></nav></aside>
<article class="c4-article" itemscope itemtype="https://schema.org/BlogPosting">
<div class="c4-article-intro"><p class="c4-eyebrow">{e(parts[item["part"]-1])} / C4 MODEL</p>
<h1 itemprop="headline">{e(item["title"])}</h1><p class="c4-article-deck" itemprop="description">{e(item["summary"])}</p>
<div class="c4-article-meta"><span>{e(labels["author"])}</span><span>·</span>
<span>{reading_minutes(item,content["language"])} {e(labels["minutes"])}</span><span>·</span><span>C4 / {item["number"]:02d}</span></div></div>
<div class="c4-inpage"><strong>{e(ui["contents"])}</strong>{contents}</div>
<div class="c4-prose" itemprop="articleBody">{sections}</div>
<aside class="c4-takeaway"><span>✳</span><div><strong>{e(ui["noteTitle"])}</strong><p>{e(ui["note"])}</p></div></aside>
<nav class="c4-chapter-nav" aria-label="{e(ui["toc"])}">{direction}</nav>
<div class="c4-chapter-foot"><p>{e(ui["review"])}</p><a href="https://c4model.com/" target="_blank" rel="noopener noreferrer">{e(ui["reference"])} ↗</a></div>
</article></div>
<section class="container c4-related"><div class="c4-blog-section-top"><div><p class="c4-eyebrow">C4 / JOURNAL</p><h2>{e(labels["related"])}</h2></div></div>
<div class="c4-blog-card-grid">{related}</div></section></main>'''
