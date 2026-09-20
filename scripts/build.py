"""Build the bilingual static site using Python's standard library."""
from pathlib import Path
from html import escape
import json
import os
import posixpath
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
ORIGIN = os.environ.get('SITE_URL', 'https://xdev.asia').rstrip('/')


def route(language, path=''):
    return ('vi/' if language == 'vi' else '') + path


def relative(source, target):
    return posixpath.relpath(target or '.', source or '.') + ('/' if not Path(target).suffix else '')


def decorate(page, language, path):
    current = route(language, path)
    prefix = relative(current, '')
    page = page.replace('href="assets/', f'href="{prefix}assets/').replace('src="assets/', f'src="{prefix}assets/').replace('href="styles.css"', f'href="{prefix}styles.css"')
    page = page.replace('@home@', relative(current, route(language))).replace('@studio@', relative(current, route(language, 'ai-studio/')))
    page = page.replace('@docs@', relative(current, route(language, 'ai-studio/docs/')))
    page = page.replace('@quickstart@', relative(current, route(language, 'ai-studio/docs/quickstart/')))
    switcher = '<div class="language-switch" role="group" aria-label="' + ('Language' if language == 'en' else 'Ngôn ngữ') + '">'
    for lang, label in [('en', 'English'), ('vi', 'Tiếng Việt')]:
        active = ' aria-current="page"' if lang == language else ''
        switcher += f'<a href="{relative(current, route(lang, path))}" lang="{lang}" hreflang="{lang}" aria-label="{label}"{active}>{lang.upper()}</a>'
    switcher += '</div>'
    page = page.replace('</nav>', '</nav>' + switcher, 1)
    canonical = ORIGIN + '/' + current
    metadata = f'<link rel="canonical" href="{canonical}">\n'
    for lang in ['en', 'vi', 'x-default']:
        metadata += f'<link rel="alternate" hreflang="{lang}" href="{ORIGIN}/{route("en" if lang == "x-default" else lang, path)}">\n'
    metadata += f'<meta property="og:locale" content="{"en_US" if language == "en" else "vi_VN"}"><meta property="og:url" content="{canonical}">'
    page = page.replace('</head>', metadata + '</head>')
    target = OUT / current / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page)


def shell(language, title, description, body):
    en = language == 'en'
    return f'''<!doctype html><html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — xDev Asia</title><meta name="description" content="{escape(description, quote=True)}"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:type" content="website"><link rel="icon" href="assets/favicon.png"><link rel="stylesheet" href="styles.css"></head><body>
<a class="skip" href="#main">{'Skip to content' if en else 'Đến nội dung chính'}</a>
<header><div class="container header-inner"><a class="brand" href="@home@" aria-label="xDev Asia"><img src="assets/xdev-logo.svg" alt="xDev" width="143" height="50"><span>ASIA</span></a><nav aria-label="{'Main navigation' if en else 'Điều hướng chính'}"><a href="@studio@">AI Studio</a><a href="@docs@">{'Docs' if en else 'Tài liệu'}</a><a href="https://blog.xdev.asia">Blog ↗</a></nav></div></header>
{body}<footer class="container"><a href="@home@">© 2026 xDev Asia</a><div class="footer-links"><a href="@studio@">AI Studio</a><a href="@docs@">{'Documentation' if en else 'Hướng dẫn sử dụng'}</a></div></footer></body></html>'''


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
    decorate(english, 'en', '')
    decorate(template, 'vi', '')
    for language in ['en', 'vi']:
        content = json.loads((ROOT / f'src/studio.{language}.json').read_text())
        en = language == 'en'
        cards = ''.join(f'<article><span class="principle-number">/ {i:02}</span><h3>{escape(item[0])}</h3><p>{escape(item[1])}</p></article>' for i, item in enumerate(content['features'], 1))
        body = f'''<main id="main"><section class="container product-hero"><div class="eyebrow">XDEV AI STUDIO</div><h1>{content['headline']}</h1><p class="lead">{escape(content['description'])}</p><div class="hero-actions"><a class="button primary" href="@quickstart@">{content['start']} →</a><a class="text-link" href="@docs@">{content['docs']} →</a></div></section><section class="container product-features"><div class="principles">{cards}</div></section><section class="container"><div class="blog-panel studio-next"><div><div class="eyebrow">{content['next_label']}</div><h2>{content['next_title']}</h2><p>{content['next_text']}</p><a class="button white" href="@docs@">{content['docs']} →</a></div><div><p>{content['app_text']}</p><a class="button white" href="https://ai-studio.xdev.asia">{content['app_link']} ↗</a></div></div></section></main>'''
        decorate(shell(language, 'XDev AI Studio', content['description'], body), language, 'ai-studio/')
        pages = content['pages']
        entries = [{'slug': '', 'title': content['docs'], 'description': content['docs_description'], 'sections': []}] + pages
        for entry in entries:
            path = 'ai-studio/docs/' + (entry['slug'] + '/' if entry['slug'] else '')
            nav = ''
            for item in entries:
                target = 'ai-studio/docs/' + (item['slug'] + '/' if item['slug'] else '')
                active = ' aria-current="page"' if item['slug'] == entry['slug'] else ''
                nav += f'<a href="{relative(route(language,path),route(language,target))}"{active}>{escape(item["title"])}</a>'
            sections = ''
            for section in entry['sections']:
                sections += f'<section><h2>{escape(section["title"])}</h2>'
                if 'text' in section:
                    sections += f'<p>{escape(section["text"])}</p>'
                if 'steps' in section:
                    sections += '<ol>' + ''.join(f'<li>{escape(step)}</li>' for step in section['steps']) + '</ol>'
                sections += '</section>'
            if not entry['slug']:
                sections = '<div class="doc-cards">' + ''.join(f'<a href="{item["slug"]}/"><h2>{escape(item["title"])}</h2><p>{escape(item["description"])}</p><span>{"Read guide" if en else "Đọc hướng dẫn"} →</span></a>' for item in pages) + '</div>'
            else:
                index = pages.index(entry)
                if index + 1 < len(pages):
                    following = pages[index + 1]
                    sections += f'<a class="button primary" href="../{following["slug"]}/">{escape(following["title"])} →</a>'
            body = f'<main id="main" class="container docs-layout"><aside><div class="eyebrow">AI STUDIO / DOCS</div><nav aria-label="{"Documentation" if en else "Mục lục tài liệu"}">{nav}</nav></aside><article class="doc-content"><a class="text-link" href="@studio@">← AI Studio</a><h1>{escape(entry["title"])}</h1><p class="lead">{escape(entry["description"])}</p>{sections}</article></main>'
            decorate(shell(language, entry['title'], entry['description'], body), language, path)
    (OUT / '.nojekyll').touch()
    print(f'Built {len(list(OUT.rglob("index.html")))} localized pages.')

if __name__ == '__main__':
    build()
