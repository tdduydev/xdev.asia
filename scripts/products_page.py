"""Render the product directory and the homepage product summary."""
from html import escape

def render_products(language, content, compact=False):
    cards = ''
    card_heading = 'h3' if compact else 'h2'
    for index, product in enumerate(content['products'], 1):
        mark = (f'<img src="assets/brand/wordmark-v2/{product["logo"]}" alt="{escape(product["name"])}" width="210" height="90">')
        tags = ''.join(f'<li>{escape(tag)}</li>' for tag in product['tags'])
        cards += f'''<article class="product-card" id="product-{product['id']}"><div class="product-card-top"><span>0{index}</span><span>{escape(product['category'])}</span></div><div class="product-mark">{mark}</div><{card_heading}>{escape(product['name'])}</{card_heading}><p>{escape(product['description'])}</p><ul class="product-tags" aria-label="{escape(content['capabilities'])}">{tags}</ul><a class="product-link" href="{product['href']}">{escape(product['action'])}<span aria-hidden="true"> ↗</span></a></article>'''
    title = content['home_title'] if compact else content['headline']
    heading = 'h2' if compact else 'h1'
    body = f'''<section class="product-directory container {'product-summary' if compact else 'product-directory-full'}" {'id="san-pham"' if compact else ''}><div class="product-intro"><p class="eyebrow">xDev / {escape(content['title'])}</p><{heading}>{escape(title)}</{heading}><p>{escape(content['intro'])}</p></div><div class="product-grid">{cards}</div>'''
    if compact:
        body += f'<a class="product-all" href="@products@">{escape(content["all"])} <span aria-hidden="true">↗</span></a>'
    else:
        body += f'<div class="product-connection"><p class="eyebrow">{escape(content["connection_label"])}</p><h2>{escape(content["connection_title"])}</h2><p>{escape(content["connection_text"])}</p></div>'
    body += '</section>'
    return body if compact else f'<main id="main">{body}</main>'
