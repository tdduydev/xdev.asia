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
        self.images = []
        self.anchors = []
        self.feed(text)
        assert not self.stack, f"Unclosed tags: {self.stack}"

    def handle_starttag(self, tag, attrs):
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(tag)
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'a':
            self.anchors.append(attrs.get('href', ''))
        if tag == 'html':
            self.language = attrs.get('lang')
        if tag == 'h1':
            self.headings += 1
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag == 'link' and attrs.get('rel') == 'alternate':
            self.alternates[attrs.get('hreflang')] = attrs.get('href')
        for key in ['href', 'src', 'poster']:
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
    paths = ['', 'brand/', 'products/', 'hive/', 'ai-studio/', 'ai-studio/docs/'] + [f'ai-studio/docs/{slug}/' for slug in slugs]
    expected = {prefix + path + 'index.html' for prefix in ['', 'vi/'] for path in paths}
    actual = {str(p.relative_to(OUT)) for p in OUT.rglob('*.html') if 'assets' not in p.relative_to(OUT).parts}
    assert actual == expected, f'Missing or stale pages: {actual ^ expected}'
    pages = {}
    for name in sorted(expected):
        file = OUT / name
        text = file.read_text()
        assert not re.search(r'forge|@(?:home|studio|docs|quickstart|brand|hive|products|catalog|social)@', text, re.I), f'Hidden product or unresolved placeholder: {name}'
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
        assert not any(urlsplit(link).hostname == 'ai-studio.xdev.asia' for link in page.anchors), f'Guide must stay on the product site: {name}'
        if '/docs/' in name and name.split('/')[-2] != 'docs':
            screenshots = [image for image in page.images if '/ai-studio/' in image.get('src', '')]
            assert screenshots, f'Missing feature screenshot: {name}'
            for image in screenshots:
                assert image.get('alt') and image.get('width') and image.get('height'), f'Inaccessible image: {name}'
                assert image['src'].endswith(f'.{page.language}.png'), f'Wrong screenshot language: {name}'
                target = (file.parent / image['src']).resolve()
                png = target.read_bytes()
                assert png[:8] == b'\x89PNG\r\n\x1a\n', f'Invalid screenshot: {target}'
                assert int.from_bytes(png[16:20], 'big') == 1440 and int.from_bytes(png[20:24], 'big') == 1000, target
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
    for prefix in ['', 'vi/']:
        home_page = Page((OUT / prefix / 'index.html').read_text())
        assert 'hive/' in home_page.anchors, 'Home must link to the Hive overview'
        hive = (OUT / prefix / 'hive/index.html').read_text()
        assert 'xDev Hive' in hive and 'MCP' in hive, 'Hive overview missing product content'
        locale = 'vi' if prefix else 'en'
        content = json.loads((ROOT / f'src/hive.{locale}.json').read_text())
        assert len(content['panels']) == 6 and len(content['catalog']) == 6
        for panel in content['panels']:
            png = (OUT / f'assets/hive/{panel["image"]}.{locale}.png').read_bytes()
            assert png[:8] == b'\x89PNG\r\n\x1a\n'
            assert (int.from_bytes(png[16:20], 'big'), int.from_bytes(png[20:24], 'big')) == (1440, 1000)
        base = OUT / 'assets/hive/video'
        manifest = json.loads((base / f'manifest.{locale}.json').read_text())
        assert manifest['language'] == locale and len(manifest['slides']) == 12
        assert len(manifest['chapters']) == 7
        starts = [chapter['start'] for chapter in manifest['chapters']]
        assert starts[0] == 0 and all(a < b for a, b in zip(starts, starts[1:]))
        assert starts[-1] < manifest['duration']
        assert (base / f'hive.{locale}.mp4').stat().st_size > 1_000_000
        captions = (base / f'captions.{locale}.vtt').read_text()
        assert captions.startswith('WEBVTT') and captions.count('-->') > 30
        def seconds(timestamp):
            h, m, s = timestamp.split(':')
            return int(h) * 3600 + int(m) * 60 + float(s)
        times = re.findall(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', captions)
        assert len(times) == captions.count('-->')
        previous = 0
        for begin, end in times:
            begin, end = seconds(begin), seconds(end)
            assert previous <= begin < end <= manifest['duration']
            previous = end
        assert all(f'id="hive-panel-{i}" class="hive-panel"' in hive for i in range(6)), 'No-JS panels must remain visible'
        assert f'srclang="{locale}"' in hive and 'id="hive-film"' in hive
    print(f'PASS: {len(pages)} pages; local links, anchors, locale pairs, metadata, English default, no Forge.')

if __name__ == '__main__':
    check()
