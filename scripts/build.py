"""Build the bilingual static site using Python's standard library.

The site is EN/VI. An app's own pages may add a language (see app_pages.py); such a
page links the rest of the site in English.
"""
from pathlib import Path
from html import escape
import json
import os
import posixpath
import re
import shutil
from app_pages import LANGUAGES as SITE_LANGUAGES, load_apps, render_app_pages
from studio_page import render_studio
from brand_page import render_brand
from docs_page import render_docs
from hive_page import render_hive
from products_page import render_products

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
LANGUAGE_NAMES = {'en': 'English', 'vi': 'Tiếng Việt', 'ja': '日本語'}
# Shared chrome: header, footer, language switch and metadata.
UI = {
    'en': {'skip': 'Skip to content', 'main_navigation': 'Main navigation', 'products': 'Products', 'docs': 'Docs', 'brand': 'Brand',
           'documentation': 'Documentation', 'studio_docs': 'AI Studio docs', 'social': 'Connect with Duy', 'language': 'Language', 'locale': 'en_US'},
    'vi': {'skip': 'Đến nội dung chính', 'main_navigation': 'Điều hướng chính', 'products': 'Sản phẩm', 'docs': 'Tài liệu', 'brand': 'Thương hiệu',
           'documentation': 'Hướng dẫn sử dụng', 'studio_docs': 'Tài liệu AI Studio', 'social': 'Kết nối với Duy', 'language': 'Ngôn ngữ', 'locale': 'vi_VN'},
    'ja': {'skip': '本文へスキップ', 'main_navigation': 'メインナビゲーション', 'products': '製品', 'docs': 'ドキュメント', 'brand': 'ブランド',
           'documentation': 'ガイド', 'studio_docs': 'AI Studioガイド', 'social': 'Duyとつながる', 'language': '言語', 'locale': 'ja_JP'},
}
ORIGIN = os.environ.get('SITE_URL', 'https://xdev.asia').rstrip('/')


def route(language, path=''):
    return (language + '/' if language != 'en' else '') + path


def relative(source, target):
    return posixpath.relpath(target or '.', source or '.') + ('/' if not Path(target).suffix else '')


def decorate(page, language, path, languages=SITE_LANGUAGES):
    """Write one page; `languages` are the locales this page exists in."""
    current = route(language, path)
    prefix = relative(current, '')
    # Site-wide pages exist only in EN/VI, so a page in another language links them in English.
    site = language if language in SITE_LANGUAGES else 'en'
    ui = UI[language]
    page = page.replace('href="assets/', f'href="{prefix}assets/').replace('src="assets/', f'src="{prefix}assets/').replace('href="styles.css"', f'href="{prefix}styles.css"')
    page = page.replace('poster="assets/', f'poster="{prefix}assets/')
    page = page.replace('@home@', relative(current, route(site))).replace('@studio@', relative(current, route(site, 'ai-studio/')))
    page = page.replace('@docs@', relative(current, route(site, 'ai-studio/docs/')))
    page = page.replace('@quickstart@', relative(current, route(site, 'ai-studio/docs/quickstart/')))
    page = page.replace('@brand@', relative(current, route(site, 'brand/')))
    page = page.replace('@products@', relative(current, route(site, 'products/')))
    page = page.replace('@hive@', relative(current, route(site, 'hive/')))
    # Generic form for data-driven pages: @route:mindmap/privacy/@ links to that path in this page's language.
    page = re.sub(r'@route:([^@"\s]*)@', lambda match: relative(current, route(language, match.group(1))), page)
    social_links = '<div class="social-links" role="group" aria-label="' + ui['social'] + '">' + ''.join(
        f'<a href="{url}">{label}<span aria-hidden="true"> ↗</span></a>'
        for label, url in [('Facebook', 'https://www.facebook.com/duydev/'), ('GitHub', 'https://github.com/tdduydev'), ('LinkedIn', 'https://www.linkedin.com/in/duydev/')]
    ) + '</div>'
    page = page.replace('@social@', social_links)
    switcher = f'<div class="language-switch"><svg class="language-globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg><select aria-label="{ui["language"]}" data-language-select>'
    fallback = ''
    for lang in languages:
        name = LANGUAGE_NAMES[lang]
        target = relative(current, route(lang, path))
        selected = ' selected' if lang == language else ''
        switcher += f'<option value="{target}" lang="{lang}"{selected}>{name}</option>'
        fallback += f'<a href="{target}" lang="{lang}" hreflang="{lang}">{name}</a>'
    switcher += f'</select><noscript><style>[data-language-select]{{display:none!important}}</style>{fallback}</noscript></div>'
    page = page.replace('</body>', f'<script src="{prefix}assets/language-switch.js" defer></script></body>')
    page = page.replace('</nav>', '</nav>' + switcher, 1)
    canonical = ORIGIN + '/' + current
    metadata = f'<link rel="canonical" href="{canonical}">\n'
    for lang in [*languages, 'x-default']:
        metadata += f'<link rel="alternate" hreflang="{lang}" href="{ORIGIN}/{route("en" if lang == "x-default" else lang, path)}">\n'
    metadata += f'<meta property="og:locale" content="{ui["locale"]}"><meta property="og:url" content="{canonical}">'
    page = page.replace('</head>', metadata + '</head>')
    target = OUT / current / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page)


def shell(language, title, description, body, product=False):
    ui = UI[language]
    logo = 'ai-studio-light.svg' if product else 'master-light.svg'
    brand_name = 'XDev AI Studio' if product else 'xDev'
    return f'''<!doctype html><html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — xDev Asia</title><meta name="description" content="{escape(description, quote=True)}"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:type" content="website"><link rel="icon" href="assets/favicon.png"><link rel="stylesheet" href="styles.css"></head><body>
<a class="skip" href="#main">{ui['skip']}</a>
<header><div class="container header-inner"><a class="brand" href="@home@" aria-label="xDev Asia"><img src="assets/brand/wordmark-v2/{logo}" alt="{brand_name}" width="143" height="70"></a><nav aria-label="{ui['main_navigation']}"><a href="@products@">{ui['products']}</a><a href="@docs@">{ui['docs']}</a><a href="https://blog.xdev.asia">Blog ↗</a></nav></div></header>
{body}<footer class="container"><a href="@home@">© 2026 xDev Asia</a><div class="footer-navigation"><div class="footer-links"><a href="@products@">{ui['products']}</a><a href="@brand@">{ui['brand']}</a><a href="@studio@">AI Studio</a><a href="@docs@">{ui['documentation']}</a></div>@social@</div></footer></body></html>'''


def build():
    # dist is exclusively generated; this removes retired pages as well.
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / 'src/assets', OUT / 'assets')
    shutil.copyfile(ROOT / 'src/styles.css', OUT / 'styles.css')
    template = (ROOT / 'src/index.vi.html').read_text()
    english = template
    for vi, en in sorted(json.loads((ROOT / 'src/home.en.json').read_text()).items(), key=lambda item: -len(item[0])):
        if vi not in template:
            raise ValueError(f'Translation source missing: {vi}')
        english = english.replace(vi, en)
    english = english.replace('lang="vi"', 'lang="en"', 1)
    for language, home in [('en', english), ('vi', template)]:
        products = json.loads((ROOT / f'src/products.{language}.json').read_text())
        home = home.replace('@catalog@', render_products(language, products, compact=True))
        decorate(home, language, '')
        directory = shell(language, products['title'], products['intro'], render_products(language, products))
        directory = directory.replace('</head>', '<link rel="stylesheet" href="assets/products-page.css"></head>')
        decorate(directory, language, 'products/')
    for language in ['en', 'vi']:
        content = json.loads((ROOT / f'src/studio.{language}.json').read_text())
        en = language == 'en'
        body = render_studio(language, content)
        decorate(shell(language, 'XDev AI Studio', content['description'], body, product=True), language, 'ai-studio/')
        pages = content['pages']
        entries = [{'slug': '', 'title': content['docs'], 'description': content['docs_description'], 'sections': []}] + pages
        for entry in entries:
            path = 'ai-studio/docs/' + (entry['slug'] + '/' if entry['slug'] else '')
            sections = ''
            for number, section in enumerate(entry['sections'], 1):
                sections += f'<section id="section-{number}"><h2>{escape(section["title"])}</h2>'
                if 'text' in section:
                    sections += f'<p>{escape(section["text"])}</p>'
                if 'steps' in section:
                    sections += '<ol>' + ''.join(f'<li>{escape(step)}</li>' for step in section['steps']) + '</ol>'
                if 'image' in section:
                    asset = f'assets/ai-studio/{section["image"]}.{language}.png'
                    caption = escape(section['caption'])
                    alt = escape(section['caption'].split(':')[0], quote=True)
                    sections += f'<figure class="guide-figure"><a href="{asset}" target="_blank" rel="noopener" aria-label="{alt}"><img src="{asset}" alt="{alt}" width="1440" height="1000" loading="lazy" decoding="async"></a><figcaption>{caption}</figcaption></figure>'
                sections += '</section>'
            body = render_docs(language, content, entry, sections)
            page = shell(language, entry['title'], entry['description'], body, product=True)
            page = page.replace('</head>', '<link rel="stylesheet" href="assets/docs-page.css"></head>')
            decorate(page, language, path)
    for language in ['en', 'vi']:
        hive = json.loads((ROOT / f'src/hive.{language}.json').read_text())
        page = shell(language, 'xDev Hive — AI SDLC', hive['description'], render_hive(language, hive))
        page = page.replace('wordmark-v2/master-light.svg', 'wordmark-v2/hive-light.svg')
        page = page.replace('alt="xDev"', 'alt="xDev Hive"')
        page = page.replace('>Hướng dẫn sử dụng</a>', '>Tài liệu AI Studio</a>').replace('>Documentation</a>', '>AI Studio docs</a>')
        # Hive's navigation must not present AI Studio's manual as its own docs.
        page = page.replace('<a href="@docs@">' + ('Docs' if language == 'en' else 'Tài liệu') + '</a>', '<a href="#features">' + ('Features' if language == 'en' else 'Tính năng') + '</a>')
        page = page.replace('</head>', '<link rel="stylesheet" href="assets/hive-page.css"></head>')
        decorate(page, language, 'hive/')
    for app in load_apps():
        for language in app:
            content = app[language]
            support = 'support/' if any(document['slug'] == 'support' for document in content['documents']) else ''
            for path, title, description, body in render_app_pages(language, content):
                page = shell(language, title, description, body)
                page = page.replace('<link rel="icon" href="assets/favicon.png">', f'<link rel="icon" href="{content["favicon"]}">')
                page = page.replace('</head>', f'<meta property="og:image" content="{ORIGIN}/{content["icon"]}"><link rel="stylesheet" href="assets/app-pages.css"></head>')
                # An app has no manual: the header's Docs slot leads to its own support page instead.
                page = page.replace(f'<a href="@docs@">{UI[language]["docs"]}</a>', f'<a href="@route:{content["slug"]}/{support}@">{escape(content["labels"]["support"])}</a>', 1)
                page = page.replace(f'<a href="@docs@">{UI[language]["documentation"]}</a>', f'<a href="@docs@">{UI[language]["studio_docs"]}</a>')
                decorate(page, language, path, list(app))
    for language in ['en', 'vi']:
        brand = json.loads((ROOT / f'src/brand.{language}.json').read_text())
        page = shell(language, brand['title'], brand['description'], render_brand(brand))
        page = page.replace('</head>', '<link rel="stylesheet" href="assets/brand-guide.css"></head>')
        decorate(page, language, 'brand/')
    (OUT / '.nojekyll').touch()
    print(f'Built {len(list(OUT.rglob("index.html")))} localized pages.')

if __name__ == '__main__':
    build()
