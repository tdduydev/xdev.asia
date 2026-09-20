"""Check the generated site without network access or third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'dist'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.stack = []
        self.ids = set()
        self.links = []
        self.alternates = {}
        self.language = None
        self.canonical = None
        self.headings = 0
        self.feed(text)
        assert not self.stack, f"Unclosed tags: {self.stack}"

    def handle_starttag(self, tag, attrs):
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(tag)
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'html':
            self.language = attrs.get('lang')
        if tag == 'h1':
            self.headings += 1
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag == 'link' and attrs.get('rel') == 'alternate':
            self.alternates[attrs.get('hreflang')] = attrs.get('href')
        for key in ['href', 'src']:
            if attrs.get(key):
                self.links.append(attrs[key])

    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1] == tag, f'Unbalanced closing tag: {tag}'
        self.stack.pop()


def check():
    en = json.loads((ROOT / 'src/studio.en.json').read_text())
    vi = json.loads((ROOT / 'src/studio.vi.json').read_text())
    slugs = [p['slug'] for p in en['pages']]
    assert slugs == [p['slug'] for p in vi['pages']], 'Locale routes differ'
    paths = ['', 'ai-studio/', 'ai-studio/docs/'] + [f'ai-studio/docs/{slug}/' for slug in slugs]
    expected = {prefix + path + 'index.html' for prefix in ['', 'vi/'] for path in paths}
    actual = {str(p.relative_to(OUT)) for p in OUT.rglob('*.html')}
    assert actual == expected, f'Missing or stale pages: {actual ^ expected}'
    pages = {}
    for name in sorted(expected):
        file = OUT / name
        text = file.read_text()
        assert not re.search(r'forge|@(?:home|studio|docs|quickstart)@', text, re.I), f'Hidden product or unresolved placeholder: {name}'
        page = Page(text)
        assert page.language == ('vi' if name.startswith('vi/') else 'en'), name
        assert page.headings == 1, name
        assert page.canonical and page.canonical.endswith('/' + name.removesuffix('index.html')), name
        assert set(page.alternates) == {'en', 'vi', 'x-default'}, name
        assert page.alternates['en'] == page.alternates['x-default'], name
        for locale in ['en', 'vi']:
            target = name.removeprefix('vi/')
            if locale == 'vi':
                target = 'vi/' + target
            assert page.alternates[locale].endswith('/' + target.removesuffix('index.html')), name
        pages[file.resolve()] = page
    for file, page in pages.items():
        for link in page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file
            assert target.is_relative_to(OUT.resolve()), f'Link escapes output: {file}: {link}'
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), f'Broken link: {file}: {link}'
            if parsed.fragment:
                assert target in pages and unquote(parsed.fragment) in pages[target].ids, f'Broken anchor: {file}: {link}'
    home = (OUT / 'index.html').read_text()
    assert 'href="ai-studio/"' in home, 'Home must link to local product overview'
    assert 'https://ai-studio.xdev.asia' not in home, 'Home must not launch the app directly'
    assert 'From idea' in home, 'English must be the default'
    print(f'PASS: {len(pages)} pages; local links, anchors, locale pairs, metadata, English default, no Forge.')

if __name__ == '__main__':
    check()
