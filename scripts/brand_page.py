"""Render the selected logo family and its bilingual usage guide."""
from html import escape


def render_brand(c):
    e = escape
    base = 'assets/brand/wordmark-v2/'
    cards = ''
    files = ''
    for kind, label in [('master', c['master']), ('ai-studio', c['product'])]:
        for theme in ['light', 'dark']:
            asset = f'{base}{kind}-{theme}.svg'
            title = f'{label} / {c[theme]}'
            cards += f'<figure class="brand-tile {theme}"><figcaption>{e(title)}</figcaption><img src="{asset}" alt="{e(title)}" width="300" height="150"><a href="{asset}" download>{e(c["file_label"])} <span aria-hidden="true">↓</span></a></figure>'
            files += f'<a href="{asset}" download><span>{e(title)}</span><span>SVG ↓</span></a>'
    palette = ''.join(f'<li><span class="brand-swatch" style="background:{color}" aria-hidden="true"></span><strong>{e(label)}</strong><code>{color}</code></li>' for label, color in c['colors'])
    rules = ''.join(f'<li><h3>{e(title)}</h3><p>{e(text)}</p></li>' for title, text in c['rules'])
    return f'''<main id="main" class="brand-guide container">
<section class="brand-intro"><div><p class="brand-kicker">{e(c['kicker'])}</p><h1>{c['headline']}</h1><p class="brand-lead">{e(c['intro'])}</p><div class="brand-actions"><a class="button primary" href="#logo-family">{e(c['explore'])}</a><a class="text-link" href="#downloads">{e(c['download'])} ↓</a></div></div><div class="brand-cover"><img src="{base}master-light.svg" alt="xDev" width="380" height="190"><span>xDev</span></div></section>
<section class="brand-story"><h2>{c['story_title']}</h2><p>{e(c['story'])}</p></section>
<section id="logo-family"><div class="brand-section-heading"><h2>{e(c['family_title'])}</h2><p>{e(c['family_text'])}</p></div><div class="brand-logo-grid">{cards}</div></section>
<section class="brand-type"><div><h2>{c['type_title']}</h2><p>{e(c['type_text'])}</p></div><figure><img src="{base}ai-studio-light.svg" alt="AI Studio" width="320" height="156"><figcaption>X + AI / STUDIO</figcaption></figure></section>
<section><div class="brand-section-heading"><h2>{e(c['palette_title'])}</h2><p>{e(c['palette_text'])}</p></div><ul class="brand-palette">{palette}</ul></section>
<section><h2>{e(c['rules_title'])}</h2><ul class="brand-rules">{rules}</ul></section>
<section class="brand-extension"><div><p class="brand-kicker">{e(c['notes_label'])}</p><h2>{e(c['notes_title'])}</h2><p>{e(c['notes_text'])}</p></div><img src="{base}notes-dark.svg" alt="X NOTES" width="330" height="156"></section>
<section id="downloads"><div class="brand-section-heading"><h2>{e(c['files_title'])}</h2><p>{e(c['files_text'])}</p></div><div class="brand-downloads">{files}</div></section><p class="brand-signoff">{e(c['ending'])}</p></main>'''
