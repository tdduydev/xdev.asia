"""Shared, localized manual hierarchy. URLs remain stable."""
from html import escape as e

GROUPS = [
 ('start', 'Bắt đầu', 'Getting started', ['quickstart', 'marketplace', 'models', 'account']),
 ('apps', 'Thiết kế ứng dụng', 'Application design', ['app-config', 'business-processes', 'inputs', 'speech-images', 'versions']),
 ('knowledge', 'Tri thức & dữ liệu', 'Knowledge & data', ['knowledge', 'documents', 'document-folders', 'document-chunks', 'retrieval', 'pipelines', 'sources', 'external-knowledge']),
 ('build', 'Workflow & tự động hóa', 'Workflows & automation', ['workflows', 'workflow-nodes', 'workflow-debug', 'workflow-dsl', 'workflow-library', 'triggers', 'trigger-events', 'approvals']),
 ('tools', 'Công cụ & tích hợp', 'Tools & integrations', ['tools', 'tool-api', 'tool-mcp', 'tool-workflow', 'extensions']),
 ('publish', 'Xuất bản & chất lượng', 'Publishing & quality', ['publishing', 'web-sharing', 'messaging-channels', 'api', 'workspace-keys', 'logs', 'annotations', 'evaluations', 'training-export', 'monitoring', 'memory', 'memory-review', 'memory-settings']),
 ('manage', 'Quản lý workspace', 'Workspace management', ['workspace', 'workspace-members', 'roles', 'quotas', 'security', 'egress', 'settings', 'storage', 'identity', 'training']),
 ('admin', 'Quản trị hệ thống', 'Instance administration', ['admin', 'admin-tenants', 'admin-users', 'admin-health', 'admin-runtime', 'admin-network', 'admin-flags']),
]


def render_docs(language, content, entry, sections):
    en = language == 'en'
    tr = lambda vi, eng: eng if en else vi
    pages = {p['slug']: p for p in content['pages']}
    ordered = [slug for *_, slugs in GROUPS for slug in slugs]
    if set(ordered) != set(pages) or len(ordered) != len(pages):
        raise ValueError('Every guide must belong to exactly one documentation group')
    slug = entry['slug']
    href = lambda target: ('../' if slug else './') + (target + '/' if target else '')
    current_group = next((g for g in GROUPS if slug in g[3]), None)
    title = lambda g: g[2] if en else g[1]
    nav = f'<a class="docs-overview" href="{href("")}"' + (' aria-current="page"' if not slug else '') + f'>{tr("Tổng quan hướng dẫn", "Guide overview")}</a>'
    for group in GROUPS:
        def link(s):
            return f'<a href="{href(s)}"' + (' aria-current="page"' if s == slug else '') + f'>{e(pages[s]["title"])}</a>'
        children = ''
        rendered = set()
        for item in group[3]:
            if item in rendered:
                continue
            descendants = [s for s in group[3] if pages[s].get('parent') == item]
            if descendants:
                family_open = ' open' if slug in [item] + descendants else ''
                children += f'<details class="docs-family"{family_open}><summary>{e(pages[item]["title"])}</summary><div>{link(item)}' + ''.join(link(s) for s in descendants) + '</div></details>'
                rendered.update(descendants)
            else:
                children += link(item)
            rendered.add(item)
        opened = ' open' if group == current_group or (not slug and group == GROUPS[0]) else ''
        nav += f'<details class="docs-group"{opened}><summary>{title(group)}<span>{len(group[3])}</span></summary><div class="docs-children">{children}</div></details>'
    label = tr('Mục lục tài liệu', 'Documentation navigation')
    navigation = f'<nav aria-label="{label}">{nav}</nav>'
    sidebar = f'<aside class="docs-sidebar"><div class="desktop-doc-nav"><a class="docs-product" href="@studio@"><img src="assets/brand/wordmark-v2/ai-studio-light.svg" alt="XDev AI Studio" width="140" height="68"><span>{tr("Hướng dẫn sử dụng", "User guide")}</span></a>{navigation}</div><details class="mobile-doc-nav"><summary>{tr("Duyệt hướng dẫn", "Browse guides")}<span>{e(title(current_group)) if current_group else tr("Tất cả chủ đề", "All topics")}</span></summary>{navigation}</details></aside>'
    toc = ''
    if not slug:
        sections = f'<div class="docs-art-banner"><img src="assets/ai-studio/artwork/guide-banner-v1.png" alt="" width="1672" height="941"><div><strong>{tr("Từ bước đầu đến vận hành.", "From first steps to operations.")}</strong><p>{tr("Hướng dẫn theo công việc bạn cần làm.", "Guides for the task in front of you.")}</p></div></div><a class="docs-start" href="quickstart/"><div><span>{tr("Lần đầu dùng AI Studio?", "New to AI Studio?")}</span><h2>{tr("Bắt đầu với ứng dụng đầu tiên", "Build your first application")}</h2><p>{tr("Làm quen từng bước, từ tạo ứng dụng đến chạy thử và xuất bản.", "Follow the steps from creating an application to testing and publishing it.")}</p></div><span aria-hidden="true">↗</span></a>'
        for group in GROUPS:
            rows = ''.join(f'<a href="{s}/"><div><h3>{e(pages[s]["title"])}</h3><p>{e(pages[s]["description"])}</p></div><span aria-hidden="true">→</span></a>' for s in group[3])
            sections += f'<section class="docs-topic" id="topic-{group[0]}"><h2>{title(group)} <span>{len(group[3])} {tr("bài", "guides")}</span></h2><div class="docs-topic-links">{rows}</div></section>'
    else:
        label = tr('Trong bài này', 'On this page')
        anchors = ''.join(f'<a href="#section-{n}">{e(s["title"])}</a>' for n, s in enumerate(entry['sections'], 1))
        toc = f'<aside class="docs-toc"><nav class="article-toc" aria-label="{label}"><strong>{label}</strong>{anchors}</nav></aside>'
        i = ordered.index(slug)
        links = ''
        for offset, vi, eng in [(-1, 'Bài trước', 'Previous guide'), (1, 'Bài tiếp theo', 'Next guide')]:
            index = i + offset
            if 0 <= index < len(ordered):
                target = ordered[index]
                links += f'<a href="{href(target)}"><span>{tr(vi, eng)}</span><strong>{e(pages[target]["title"])}</strong></a>'
        related = list(dict.fromkeys([r for r in entry.get('related', []) if r in pages] + [s for s, p in pages.items() if p.get('parent') == slug]))
        if related:
            sections += '<section class="docs-related"><h2>' + tr('Hướng dẫn liên quan', 'Related guides') + '</h2>' + ''.join(link(r) for r in related) + '</section>'
        sections += f'<nav class="docs-pagination" aria-label="{tr("Đọc tiếp", "Continue reading")}">{links}</nav>'
    crumb = f'<nav class="docs-breadcrumb" aria-label="Breadcrumb"><a href="@docs@">{tr("Hướng dẫn", "Guides")}</a>'
    if current_group:
        crumb += f'<span aria-hidden="true">/</span><a href="{href("")}#topic-{current_group[0]}">{title(current_group)}</a>'
    crumb += '</nav>'
    return f'<main id="main" class="docs-workspace container {"docs-index" if not slug else "docs-article"}">{sidebar}<article class="doc-content">{crumb}<h1>{e(entry["title"])}</h1><p class="lead">{e(entry["description"])}</p>{sections}</article>{toc}</main>'
