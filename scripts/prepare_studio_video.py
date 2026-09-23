"""Generate editable narration from the localized guide inventory."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CHAPTERS=[('Bắt đầu với AI Studio','Start with AI Studio',['quickstart','marketplace','models','account']),('Tri thức và dữ liệu','Knowledge and data',['knowledge','documents','retrieval','pipelines','sources','external-knowledge']),('Công cụ và tự động hóa','Tools and automation',['tools','extensions','workflows','triggers','approvals']),('Xuất bản và tích hợp','Publish and integrate',['publishing','api']),('Chất lượng và ghi nhớ','Quality and memory',['logs','annotations','monitoring','memory']),('Quản lý tổ chức','Manage your organisation',['workspace','roles','security','settings','storage','identity']),('Huấn luyện và quản trị','Training and administration',['training','admin'])]
for lang in ['vi','en']:
 c=json.loads((ROOT/f'src/studio.{lang}.json').read_text());pages={p['slug']:p for p in c['pages']}; slides=[]
 for n,(vi,en,slugs) in enumerate(CHAPTERS,1):
  for slug in slugs:
   p=pages[slug]; steps=next((s['steps'] for s in p['sections'] if 'steps' in s), [next((s['text'] for s in p['sections'] if s['title'] in ['Step 1','Bước 1']), p['description'])])
   image=next(s['image'] for s in p['sections'] if 'image' in s and s['image']!='signin')
   # Each feature gets its own narration and screen, not just a name in a list.
   narration=p['title']+'. '+p['description']+' '+steps[0]
   if slug in ['retrieval','annotations','extensions','external-knowledge','roles']:
    narration+=' '+p['sections'][-1].get('text','')
   if not slides:
    narration=('Chào mừng bạn đến với AI Studio. Trong video này, chúng ta đi qua bảy chương, từ xây ứng dụng, kết nối dữ liệu và tự động hóa đến vận hành và quản trị. Giao diện sử dụng dữ liệu minh họa. Các thao tác tùy thuộc quyền và cấu hình triển khai. ' if lang=='vi' else 'Welcome to AI Studio. This tour covers seven chapters, from building applications, connecting data and automating work to operations and administration. The screens use illustrative data. Available actions depend on permissions and deployment configuration. ')+narration
   if slug=='quickstart':
    narration+=(' Bạn có thể cấu hình biến, câu chào, nghiệp vụ, nhận dạng giọng nói, đọc văn bản và tạo ảnh khi có mô hình phù hợp.' if lang=='vi' else 'Configure variables, opening messages, business processes, speech recognition, text to speech and image generation with suitable models.')
   if slug=='monitoring':
    narration+=(' Trong ứng dụng, tạo bộ dữ liệu đánh giá, chạy thử và so sánh các lượt chạy tương thích; xuất dữ liệu huấn luyện khi cần.' if lang=='vi' else 'Inside an application, create evaluation datasets, run tests and compare compatible runs; export training data when needed.')
   if slug=='admin':
    narration+=(' Quản trị hệ thống còn có các mục tổ chức, tài khoản, sức khỏe dịch vụ, thiết lập lúc chạy, mạng và cờ tính năng. Quyền quản trị hệ thống tách biệt với vai trò trong workspace. Để thực hành từng bước, mở hướng dẫn tương ứng trên trang AI Studio. Cảm ơn bạn đã theo dõi.' if lang=='vi' else 'Instance administration also includes organisations, accounts, service health, runtime settings, network rules and feature flags. Instance administration is separate from workspace roles. For step-by-step practice, open the corresponding guide on the AI Studio website. Thank you for watching.')
   slides.append(dict(chapter=n,chapter_title=vi if lang=='vi' else en,slug=slug,title=p['title'],description=p['description'],image=image,narration=narration))
 (ROOT/f'docs/video/script.{lang}.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2)+'\n')
 print(lang,len(slides),sum(len(s['narration'].split()) for s in slides),'words')
