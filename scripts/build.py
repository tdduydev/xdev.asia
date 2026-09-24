"""Build the bilingual static site using Python's standard library."""
from pathlib import Path
from html import escape
import json
import os
import posixpath
import shutil
from studio_page import render_studio
from brand_page import render_brand
from docs_page import render_docs

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'
LANGUAGES = [('en', 'English'), ('vi', 'Tiếng Việt')]
ORIGIN = os.environ.get('SITE_URL', 'https://xdev.asia').rstrip('/')


def route(language, path=''):
    return (language + '/' if language != 'en' else '') + path


def relative(source, target):
    return posixpath.relpath(target or '.', source or '.') + ('/' if not Path(target).suffix else '')


def decorate(page, language, path):
    current = route(language, path)
    prefix = relative(current, '')
    page = page.replace('href="assets/', f'href="{prefix}assets/').replace('src="assets/', f'src="{prefix}assets/').replace('href="styles.css"', f'href="{prefix}styles.css"')
    page = page.replace('poster="assets/', f'poster="{prefix}assets/')
    page = page.replace('@home@', relative(current, route(language))).replace('@studio@', relative(current, route(language, 'ai-studio/')))
    page = page.replace('@docs@', relative(current, route(language, 'ai-studio/docs/')))
    page = page.replace('@quickstart@', relative(current, route(language, 'ai-studio/docs/quickstart/')))
    page = page.replace('@brand@', relative(current, route(language, 'brand/')))
    social_label = 'Connect with Duy' if language == 'en' else 'Kết nối với Duy'
    social_links = '<div class="social-links" role="group" aria-label="' + social_label + '">' + ''.join(
        f'<a href="{url}">{label}<span aria-hidden="true"> ↗</span></a>'
        for label, url in [('Facebook', 'https://www.facebook.com/duydev/'), ('GitHub', 'https://github.com/tdduydev'), ('LinkedIn', 'https://www.linkedin.com/in/duydev/')]
    ) + '</div>'
    page = page.replace('@social@', social_links)
    label = 'Language' if language == 'en' else 'Ngôn ngữ'
    switcher = f'<div class="language-switch"><svg class="language-globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg><select aria-label="{label}" data-language-select>'
    fallback = ''
    for lang, name in LANGUAGES:
        target = relative(current, route(lang, path))
        selected = ' selected' if lang == language else ''
        switcher += f'<option value="{target}" lang="{lang}"{selected}>{name}</option>'
        fallback += f'<a href="{target}" lang="{lang}" hreflang="{lang}">{name}</a>'
    switcher += f'</select><noscript><style>[data-language-select]{{display:none!important}}</style>{fallback}</noscript></div>'
    page = page.replace('</body>', f'<script src="{prefix}assets/language-switch.js" defer></script></body>')
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


def shell(language, title, description, body, product=False):
    en = language == 'en'
    logo = 'ai-studio-light.svg' if product else 'master-light.svg'
    brand_name = 'XDev AI Studio' if product else 'xDev'
    return f'''<!doctype html><html lang="{language}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — xDev Asia</title><meta name="description" content="{escape(description, quote=True)}"><meta property="og:title" content="{escape(title, quote=True)}"><meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:type" content="website"><link rel="icon" href="assets/favicon.png"><link rel="stylesheet" href="styles.css"></head><body>
<a class="skip" href="#main">{'Skip to content' if en else 'Đến nội dung chính'}</a>
<header><div class="container header-inner"><a class="brand" href="@home@" aria-label="xDev Asia"><img src="assets/brand/wordmark-v2/{logo}" alt="{brand_name}" width="143" height="70"></a><nav aria-label="{'Main navigation' if en else 'Điều hướng chính'}"><a href="@studio@">AI Studio</a><a href="@docs@">{'Docs' if en else 'Tài liệu'}</a><a href="https://blog.xdev.asia">Blog ↗</a></nav></div></header>
{body}<footer class="container"><a href="@home@">© 2026 xDev Asia</a><div class="footer-navigation"><div class="footer-links"><a href="@brand@">{'Brand' if en else 'Thương hiệu'}</a><a href="@studio@">AI Studio</a><a href="@docs@">{'Documentation' if en else 'Hướng dẫn sử dụng'}</a></div>@social@</div></footer></body></html>'''


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
        brand = json.loads((ROOT / f'src/brand.{language}.json').read_text())
        page = shell(language, brand['title'], brand['description'], render_brand(brand))
        page = page.replace('</head>', '<link rel="stylesheet" href="assets/brand-guide.css"></head>')
        decorate(page, language, 'brand/')
    (OUT / '.nojekyll').touch()
    print(f'Built {len(list(OUT.rglob("index.html")))} localized pages.')

if __name__ == '__main__':
    build()
