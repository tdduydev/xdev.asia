"""The overview shares its feature inventory with the grouped manual."""
import json
from pathlib import Path
from html import escape as e
from docs_page import GROUPS
ROOT=Path(__file__).resolve().parents[1]
def render_features(language, content):
 en=language=='en'; c=content['feature_catalog'];pages={p['slug']:p for p in content['pages']}
 groups=''
 for _,vi,eng,slugs in GROUPS:
  items=''.join(f'<a href="docs/{slug}/"><h4>{e(pages[slug]["title"])}</h4><p>{e(pages[slug]["description"])}</p><span aria-hidden="true">↗</span></a>' for slug in slugs)
  groups+=f'<details class="feature-group" open><summary>{e(eng if en else vi)}<span>{len(slugs)}</span></summary><div class="feature-items">{items}</div></details>'
 return f'<section class="container studio-feature-catalog" id="features"><div class="studio-section-heading"><h2>{e(c["title"])}</h2><p>{e(c["intro"])}</p></div>{groups}</section>'

def render_video(language):
 path=ROOT/f'src/assets/ai-studio/video/manifest.{language}.json'
 if not path.exists():return ''
 data=json.loads(path.read_text());en=language=='en';base='assets/ai-studio/video/'
 chapters=''.join(f'<li><button type="button" data-video-seek="{chapter["start"]}" hidden><span>{chapter["time"]}</span>{e(chapter["title"])}</button><noscript><span>{chapter["time"]} — {e(chapter["title"])}</span></noscript></li>' for chapter in data['chapters'])
 transcript=''.join(f'<section><h4>{e(s["title"])}</h4><p>{e(s["narration"])}</p></section>' for s in data['slides'])
 return f'''<section class="container studio-video" id="video"><div class="studio-section-heading"><h2>{'A guided tour of AI Studio' if en else 'Khám phá AI Studio qua video'}</h2><p>{'Seven chapters, English narration and captions. Screens show illustrative data.' if en else 'Bảy chương, lời dẫn và phụ đề tiếng Việt. Giao diện dùng dữ liệu minh họa.'}</p></div><div class="studio-video-layout"><video id="studio-tour" controls preload="metadata" playsinline poster="{base}poster.{language}.png" aria-label="{'AI Studio introduction' if en else 'Video giới thiệu AI Studio'}"><source src="{base}ai-studio.{language}.mp4" type="video/mp4"><track kind="captions" src="{base}captions.{language}.vtt" srclang="{language}" label="{'English' if en else 'Tiếng Việt'}" default></video><nav aria-label="{'Video chapters' if en else 'Chương video'}"><h3>{'Chapters' if en else 'Các chương'}</h3><ol>{chapters}</ol></nav></div><div class="studio-video-links"><a href="{base}ai-studio.{language}.mp4" download>{'Download video' if en else 'Tải video'} · {data['duration_label']}</a><a href="{base}captions.{language}.vtt" download>{'Download captions' if en else 'Tải phụ đề'}</a></div><details class="video-transcript"><summary>{'Read the transcript' if en else 'Đọc lời thoại video'}</summary>{transcript}</details></section>'''

def render_story(language):
 data=json.loads((ROOT/f'src/assets/ai-studio/story/manifest.{language}.json').read_text())
 en=language=='en';base='assets/ai-studio/story/';duration=f"{int(data['duration'])//60}:{int(data['duration'])%60:02}"
 chapters=''.join(f'<button type="button" data-story-seek="{s["start"]}" hidden><span>{i+1:02}</span>{e(s["title"])}</button>' for i,s in enumerate(data['scenes']))
 transcript=''.join(f'<section><h4>{e(s["title"])}</h4><p>{e(s["narration"])}</p></section>' for s in data['scenes'])
 return f'''<section class="container studio-story" id="story"><div class="studio-section-heading"><h2>{'AI Studio: from a use case to operations' if en else 'AI Studio: từ bài toán đến vận hành'}</h2><p>{'An illustrated use case connects knowledge, AI Gateway, customizable workflows, sandbox execution and data controls.' if en else 'Một tình huống xuyên suốt kết nối tri thức, AI Gateway, workflow tùy chỉnh, sandbox và các lớp kiểm soát dữ liệu.'}</p></div><video id="studio-story" controls preload="metadata" playsinline poster="{base}poster.v2.{language}.png" aria-label="{'Why AI Studio — drawn story' if en else 'Vì sao có AI Studio — câu chuyện bằng nét vẽ'}"><source src="{base}story.v2.{language}.mp4" type="video/mp4"><track kind="captions" src="{base}captions.{language}.vtt" srclang="{language}" label="{'English' if en else 'Tiếng Việt'}" default></video><details class="story-index"><summary>{("Choose a chapter" if en else "Chọn nội dung muốn xem")} · {len(data["scenes"])} {("chapters" if en else "phần")}</summary><div class="story-chapters" role="group" aria-label="{'Story chapters' if en else 'Các phần của câu chuyện'}">{chapters}</div></details><p class="story-meta">{duration} · {'Drawn animation · Synthetic narration' if en else 'Hoạt hình nét vẽ · Giọng đọc tổng hợp'} · <a href="{base}story.v2.{language}.mp4" download>{'Download video' if en else 'Tải video'}</a></p><details class="story-transcript"><summary>{'Read the story' if en else 'Đọc lời dẫn'}</summary>{transcript}</details></section>'''
