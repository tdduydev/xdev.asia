"""Bilingual Hive product story, real demo UI showcase, and narrated film."""
from html import escape as e
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]


def render_video(language,c):
    asset=ROOT/f'src/assets/hive/video/manifest.{language}.json'
    if not asset.exists():return ''
    data=json.loads(asset.read_text());base='assets/hive/video/'
    chapters=''.join(f'<li><button type="button" data-video-seek="{s["start"]}" hidden><span>{s["time"]}</span>{e(s["title"])}</button><noscript>{s["time"]} — {e(s["title"])}</noscript></li>' for s in data['chapters'])
    transcript=''.join(f'<section><h4>{e(s["title"])}</h4><p>{e(s["narration"])}</p></section>' for s in data['slides'])
    return f'''<section class="container hive-film" id="video"><div class="hive-section-heading"><p class="eyebrow">HIVE / PRODUCT FILM</p><h2>{e(c['video_title'])}</h2><p>{e(c['video_intro'])}</p></div><div class="hive-film-layout"><video id="hive-film" controls playsinline preload="metadata" poster="{base}poster.{language}.png" aria-label="{e(c['video_title'])}"><source src="{base}hive.{language}.mp4" type="video/mp4"><track kind="captions" src="{base}captions.{language}.vtt" srclang="{language}" label="{'Tiếng Việt' if language=='vi' else 'English'}" default></video><nav aria-label="{e(c['chapters'])}"><h3>{e(c['chapters'])}</h3><ol>{chapters}</ol></nav></div><p class="hive-film-note">{e(c['video_note'])} · {data['duration_label']}</p><div class="hive-downloads"><a href="{base}hive.{language}.mp4" download>{e(c['download_video'])} ↗</a><a href="{base}captions.{language}.vtt" download>{e(c['download_captions'])} ↗</a></div><details class="hive-transcript"><summary>{e(c['transcript'])}</summary>{transcript}</details></section>'''


def render_hive(language,c):
    tabs=''.join(f'<a href="#hive-panel-{i}" id="hive-tab-{i}" class="hive-tab">{e(p["label"])}</a>' for i,p in enumerate(c['panels']))
    panels=''.join(f'''<section id="hive-panel-{i}" class="hive-panel" aria-labelledby="hive-tab-{i}"><div><span class="hive-panel-number">0{i+1} / 06</span><h3>{e(p['title'])}</h3><p>{e(p['text'])}</p><span class="hive-screen-note">{e(c['image_note'])}</span></div><figure><a href="assets/hive/{p['image']}.{language}.png" target="_blank" rel="noopener" aria-label="{e(c['zoom']+': '+p['label'])}"><img src="assets/hive/{p['image']}.{language}.png" alt="{e(p['label']+' — '+c['image_note'])}" width="1440" height="1000" loading="lazy" decoding="async"></a><figcaption>{e(c['zoom'])}<span aria-hidden="true">↗</span></figcaption></figure></section>''' for i,p in enumerate(c['panels']))
    catalog=''.join(f'<article><span class="hive-number">0{i+1}</span><h3>{e(g["title"])}</h3><ul>'+''.join(f'<li>{e(item)}</li>' for item in g['items'])+'</ul></article>' for i,g in enumerate(c['catalog']))
    problems=''.join(f'<article><span class="hive-number">0{i+1}</span><h3>{e(title)}</h3><p>{e(text)}</p></article>' for i,(title,text) in enumerate(c['problems']))
    uses=''.join(f'<article><span class="hive-number">0{i+1}</span><h3>{e(title)}</h3><p>{e(text)}</p></article>' for i,(title,text) in enumerate(c['use_cases']))
    steps=''.join(f'<li><span>0{i+1}</span><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></li>' for i,s in enumerate(c['steps']))
    setup=''.join(f'<article><p class="eyebrow">0{i+1} / {e(title)}</p><h3>{e(title)}</h3><p>{e(text)}</p><a href="https://github.com/tdduydev/xdev-hive#readme">{e(c["start_action"])} <span aria-hidden="true">↗</span></a></article>' for i,(title,text) in enumerate(c['setup_options']))
    faq=''.join(f'<details><summary>{e(title)}</summary><p>{e(text)}</p></details>' for title,text in c['faq'])
    return f'''<main id="main" class="hive-page">
<section class="container hive-hero"><div><p class="eyebrow">{e(c['eyebrow'])}</p><h1>{e(c['headline'][0])}<br>{e(c['headline'][1])}</h1><p class="lead">{e(c['description'])}</p><div class="hive-actions"><a class="button primary" href="#video">{e(c['watch'])}<span aria-hidden="true">▷</span></a><a class="text-link" href="#showcase">{e(c['showcase_link'])}<span aria-hidden="true">↓</span></a></div><p class="hive-hero-note">{e(c['hero_note'])}</p></div>
<div class="hive-map" data-hive-map><div class="hive-map-header"><p>{e(c['map_label'])}</p><span>MCP</span></div><div class="hive-agent-list"><span>Claude Code</span><span>Codex</span><span>Gemini CLI</span><span>Cursor</span></div><div class="hive-connector" aria-hidden="true"><span></span></div><div class="hive-core"><img src="assets/brand/wordmark-v2/hive-dark.svg" alt="xDev Hive" width="210" height="100"><p>{e(c['hub'])}</p></div><div class="hive-connector" aria-hidden="true"><span></span></div><div class="hive-context-list">{''.join(f'<span>{e(label)}</span>' for label in c['context'])}</div><p class="hive-map-caption">{e(c['map_caption'])}</p><button type="button" class="hive-map-pause" hidden data-map-pause data-pause="{'Tạm dừng chuyển động' if language=='vi' else 'Pause animation'}" data-resume="{'Tiếp tục chuyển động' if language=='vi' else 'Resume animation'}">{'Tạm dừng chuyển động' if language=='vi' else 'Pause animation'}</button></div></section>
<nav class="container hive-jumps" aria-label="{'Nội dung trang' if language=='vi' else 'Page contents'}"><a href="#story">{e(c['story_label'])}</a><a href="#showcase">{e(c['showcase_link'])}</a><a href="#features">{e(c['explore'])}</a><a href="#video">{e(c['watch'])}</a><a href="#get-started">{e(c['start_label'])}</a></nav>
<section class="container hive-story" id="story"><div class="hive-section-heading"><p class="eyebrow">{e(c['story_label'])}</p><h2>{e(c['story_title'])}</h2><p>{e(c['story_intro'])}</p></div><div class="hive-problems">{problems}</div></section>
<section class="container hive-showcase" id="showcase"><div class="hive-section-heading"><p class="eyebrow">{e(c['showcase_label'])}</p><h2>{e(c['showcase_title'])}</h2><p>{e(c['showcase_intro'])}</p></div><nav class="hive-tabs" aria-label="{e(c['showcase_link'])}">{tabs}</nav><div class="hive-panels">{panels}</div></section>
<section class="hive-boundary"><div class="container"><span aria-hidden="true">✓</span><div><h2>{e(c['boundary_title'])}</h2><p>{e(c['boundary_text'])}</p></div></div></section>
{render_video(language,c)}
<section class="container hive-features" id="features"><div class="hive-section-heading"><p class="eyebrow">{e(c['catalog_label'])}</p><h2>{e(c['catalog_title'])}</h2><p>{e(c['catalog_intro'])}</p></div><div class="hive-feature-grid">{catalog}</div></section>
<section class="container hive-usecases"><div class="hive-section-heading"><p class="eyebrow">{e(c['use_label'])}</p><h2>{e(c['use_title'])}</h2></div><div class="hive-use-grid">{uses}</div></section>
<section class="container hive-workflow"><div class="hive-section-heading"><p class="eyebrow">{e(c['workflow_label'])}</p><h2>{e(c['workflow_title'])}</h2><p>{e(c['workflow_description'])}</p></div><ol>{steps}</ol></section>
<section class="container hive-setup" id="get-started"><div class="hive-section-heading"><p class="eyebrow">{e(c['setup_label'])}</p><h2>{e(c['setup_title'])}</h2></div><div class="hive-setup-grid">{setup}</div></section>
<section class="container hive-faq"><h2>{e(c['faq_title'])}</h2><div>{faq}</div></section>
<section class="container hive-start"><div><p class="eyebrow">{e(c['start_label'])}</p><h2>{e(c['start_title'])}</h2><p>{e(c['start_description'])}</p></div><a class="button primary" href="https://github.com/tdduydev/xdev-hive#readme">{e(c['start_action'])}<span aria-hidden="true">↗</span></a></section>
</main><script src="assets/hive-page.js" defer></script>'''
