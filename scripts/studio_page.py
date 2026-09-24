"""Product overview; all copy and screenshots follow the selected locale."""
from html import escape
from studio_features import render_features, render_video


def render_studio(language, content):
    c = content['landing']
    e = escape
    icons = [
        '<path d="M6 3h9l4 4v14H6z"></path><path d="M14 3v5h5M9 12h7M9 16h7"></path>',
        '<rect x="6" y="6" width="12" height="12" rx="3"></rect><path d="M9 2v4m6-4v4M9 18v4m6-4v4M2 9h4m-4 6h4m12-6h4m-4 6h4"></path>',
        '<rect x="3" y="4" width="18" height="16" rx="3"></rect><path d="M3 9h18m-13 5 3 2-3 2m6 0h3"></path>',
    ]
    icons = [f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>' for paths in icons]
    nodes = ''.join(f'<div class="studio-node" data-node="{i}"><span class="studio-node-icon" aria-hidden="true">{icons[i % len(icons)]}</span><div><strong>{e(title)}</strong><span>{e(detail)}</span></div><span class="studio-node-check" aria-hidden="true">✓</span></div>' for i, (title, detail) in enumerate(c['nodes']))
    wires = '<svg class="workflow-wires" viewBox="0 0 1000 562.5" fill="none" aria-hidden="true"><defs><marker id="workflow-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="currentColor"></path></marker></defs>' + ''.join(f'<path data-edge="{i}" d="{path}" marker-end="url(#workflow-arrow)"></path>' for i, path in enumerate(['M290 175H390', 'M610 175H710', 'M820 226V350', 'M710 400H610', 'M390 400H290'])) + '<path class="workflow-return" d="M940 400H965V100H820V124" marker-end="url(#workflow-arrow)"></path></svg>'
    canvas = f'<p class="workflow-pan-hint">{("Swipe or scroll horizontally to explore the workflow" if language == "en" else "Vuốt hoặc cuộn ngang để xem toàn bộ workflow")}</p><div class="workflow-viewport" tabindex="0" role="region" aria-label="{("Workflow canvas" if language == "en" else "Sơ đồ workflow")}"><div class="workflow-canvas"><div class="workflow-canvas-caption">{("Request → context → draft → review → delivery" if language == "en" else "Yêu cầu → ngữ cảnh → bản nháp → phê duyệt → kết quả")}</div>{wires}<div class="studio-flow">{nodes}</div><span class="workflow-return-label">{("Revise if needed" if language == "en" else "Chỉnh sửa nếu cần")}</span><span class="workflow-canvas-stamp">AI Studio · Workflow</span></div></div>'
    booking = c['booking']
    scenarios = ''.join(f'<option value="{i}" data-input="{e(item["input"])}" data-scenario-result="{e(item["result"])}">{e(item["title"])}</option>' for i, item in enumerate(c['scenarios']))
    booking_section = f'''<section class="container studio-booking" id="book-demo"><div><p class="studio-eyebrow">{e(booking['label'])}</p><h2>{e(booking['title'])}</h2><p>{e(booking['intro'])}</p><ul>{''.join(f'<li>{e(topic)}</li>' for topic in booking['topics'])}</ul></div><div class="studio-booking-contact"><h3>{e(booking['label'])}</h3><p>{e(booking['note'])}</p><a class="button primary" href="{e(booking['url'])}">{e(booking['contact'])}<span aria-hidden="true">↗</span></a></div></section>'''
    tabs = ''.join(f'<a class="studio-tab" href="#studio-panel-{i}" id="studio-tab-{i}">{e(panel["label"])}</a>' for i, panel in enumerate(c['panels']))
    panels = ''
    for i, panel in enumerate(c['panels']):
        asset = f'assets/ai-studio/{panel["image"]}.{language}.png'
        panels += f'''<section class="studio-panel" id="studio-panel-{i}" aria-labelledby="studio-tab-{i}"><div class="studio-panel-copy"><p class="studio-panel-detail">{e(panel['detail'])}</p><h3>{e(panel['title'])}</h3><p>{e(panel['text'])}</p><a class="studio-inline-link" href="docs/{panel['slug']}/">{e(c['guide'])}<span aria-hidden="true">↗</span></a></div><figure class="studio-screen"><a href="{asset}" target="_blank" rel="noopener" aria-label="{e(c['zoom'] + ': ' + panel['label'])}"><img src="{asset}" alt="{e(panel['label'] + ' — ' + c['image_note'])}" width="1440" height="1000" loading="lazy" decoding="async"></a><figcaption>{e(c['image_note'])}<span aria-hidden="true">↗</span></figcaption></figure></section>'''
    controls = ''.join(f'<a href="docs/{slug}/" class="studio-control"><span class="studio-control-icon" aria-hidden="true">{["✳", "⊞", "✓"][i]}</span><div><h3>{e(title)}</h3><p>{e(text)}</p></div><span aria-hidden="true">↗</span></a>' for i, (title, text, slug) in enumerate(c['controls']))
    steps = ''.join(f'<li><span class="studio-step-number">0{i+1}</span><h3><a href="docs/{slug}/">{e(title)}</a></h3><p>{e(text)}</p></li>' for i, (title, text, slug) in enumerate(c['steps']))
    states = ''.join(f'<span data-state="{i}" hidden>{e(state)}</span>' for i, state in enumerate(c['demo_states']))
    return f'''<link rel="stylesheet" href="assets/studio-page.css">
<main id="main" class="studio-landing">
<section class="container studio-hero"><div class="studio-hero-copy"><p class="studio-eyebrow">{e(c['eyebrow'])}</p><h1>{c['headline']}</h1><p class="studio-intro">{e(c['intro'])}</p><div class="studio-actions"><a class="button primary" href="#book-demo">{e(booking['label'])}</a><a class="studio-inline-link" href="#explore">{e(c['explore'])}<span aria-hidden="true">↓</span></a></div><div class="studio-catalog-links"><a href="#features">{("All features" if language == "en" else "Toàn bộ tính năng")}</a><a href="#video">{("Watch the tour" if language == "en" else "Xem video giới thiệu")}</a></div><p class="studio-hero-note">{e(c['note'])}</p></div>
<div class="studio-blueprint"><div class="studio-blueprint-top"><span>{e(c['demo_label'])}</span><span class="studio-demo-badge">{e(c['demo_badge'])}</span></div><div class="workflow-scenario"><label for="workflow-scenario">{e(c['scenario_label'])}</label><select id="workflow-scenario" data-scenario disabled>{scenarios}</select><p class="workflow-input-label">{e(c['sample_label'])}</p><p data-sample-input>{e(c['scenarios'][0]['input'])}</p></div>{canvas}<div class="workflow-result" data-workflow-result hidden><strong>{e(c['output_label'])}</strong><p data-output-text></p></div><div class="studio-demo-output"><span class="studio-status-dot" aria-hidden="true"></span><p role="status" aria-live="polite" data-demo-status>{e(c['demo_idle'])}</p><div class="studio-demo-progress" aria-hidden="true"><span></span></div></div><button class="workflow-pause" type="button" data-flow-pause data-pause="{('Pause animation' if language == 'en' else 'Tạm dừng')}" data-resume="{('Resume animation' if language == 'en' else 'Tiếp tục')}" hidden>{('Pause animation' if language == 'en' else 'Tạm dừng')}</button><p class="studio-demo-note">{e(c['demo_note'])}</p><div hidden data-demo-copy>{states}<span data-result>{e(c['demo_result'])}</span></div></div></section>
<div class="container"><ul class="studio-summary">{''.join(f'<li><span aria-hidden="true">✓</span>{e(item)}</li>' for item in c['strip'])}</ul></div>
<section class="container studio-explore" id="explore"><div class="studio-section-heading"><h2>{c['workspace_title']}</h2><p>{e(c['workspace_intro'])}</p></div><nav class="studio-tabs" aria-label="{e(c['gallery_label'])}">{tabs}</nav><div class="studio-panels">{panels}</div></section>
<section class="studio-control-section"><div class="container studio-control-layout"><div><span class="studio-control-emblem" aria-hidden="true">✳</span><h2>{c['control_title']}</h2><p class="studio-control-intro">{e(c['control_intro'])}</p></div><div class="studio-controls">{controls}</div></div></section>
{render_video(language)}
{render_features(language, content)}
<section class="container studio-journey"><h2>{e(c['journey_title'])}</h2><ol class="studio-steps">{steps}</ol></section>
{booking_section}
<section class="container studio-closing"><div class="studio-closing-inner"><div><h2>{c['closing_title']}</h2><p>{e(c['closing_text'])}</p></div><div class="studio-closing-actions"><a class="button white" href="@quickstart@">{e(c['start'])}</a><a class="studio-inline-link" href="@docs@">{e(c['closing_link'])}<span aria-hidden="true">↗</span></a></div></div></section>
</main><script src="assets/studio-page.js" defer></script>'''
