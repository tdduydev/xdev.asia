"""Generate standalone English and Vietnamese pages. Python standard library only."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
translations = {
'Từ ý tưởng đến sản phẩm, cùng AI': 'From idea to product, with AI',
'Khám phá XDev AI Studio và XDev Forge: xây dựng ứng dụng AI, kết nối tri thức và phát triển phần mềm cùng đội agent.': 'Discover XDev AI Studio and XDev Forge: build AI applications, connect knowledge, and develop software with AI teams.',
'Hai sản phẩm. Một hướng đi: đưa AI vào công việc thực tế.': 'Two products. One purpose: bring AI into everyday work.',
'Đến nội dung chính': 'Skip to main content',
'xDev Asia — Trang chủ': 'xDev Asia — Home',
'Điều hướng chính': 'Main navigation',
'Sản phẩm': 'Products',
'Cách tiếp cận': 'Our approach',
'Khám phá xDev': 'Explore xDev',
'CÔNG NGHỆ ĐỂ TẠO NÊN GIÁ TRỊ': 'TECHNOLOGY THAT CREATES VALUE',
'Từ ý tưởng<br>đến sản phẩm,<br><span>cùng AI.</span>': 'From idea<br>to product,<br><span>with AI.</span>',
'Biến tri thức thành ứng dụng. Biến kế hoạch thành phần mềm. xDev mang AI đến gần hơn với công việc của bạn.': 'Turn knowledge into applications. Turn plans into software. xDev brings AI closer to the work you do.',
'Khám phá sản phẩm': 'Explore products',
'Đọc blog xDev': 'Read the xDev blog',
'Được xây dựng từ thực tiễn.': 'Built from real-world experience.',
'Dành cho những người muốn tạo ra điều mới.': 'For people ready to create something new.',
'Từ ý tưởng, XDev AI Studio giúp xây dựng ứng dụng AI và XDev Forge giúp phát triển phần mềm': 'From your idea, XDev AI Studio helps build AI applications and XDev Forge helps develop software',
'Ý tưởng của bạn': 'Your idea',
'Xây ứng dụng AI': 'Build AI apps',
'Phát triển phần mềm': 'Develop software',
'Ý TƯỞNG': 'IDEA', 'CÔNG CỤ': 'TOOLS', 'SẢN PHẨM': 'PRODUCTS',
'HỆ SINH THÁI XDEV': 'THE XDEV ECOSYSTEM',
'Hai sản phẩm. ': 'Two products. ',
'Một hướng đi: đưa AI vào công việc thực tế.': 'One purpose: bring AI into everyday work.',
'Xem hai sản phẩm': 'View both products',
'Công cụ phù hợp.<br>Khả năng rộng mở.': 'The right tools.<br>New possibilities.',
'Từ xây ứng dụng AI đến phát triển phần mềm,<br>chọn điểm bắt đầu phù hợp với bạn.': 'From AI applications to software development,<br>find the right place to start.',
'Đưa tri thức của tổ chức vào ứng dụng AI. Thiết kế workflow, kết nối dữ liệu và lựa chọn mô hình trong cùng một không gian làm việc.': 'Put your organization’s knowledge to work in AI applications. Design workflows, connect data, and choose models in one workspace.',
'Xây workflow bằng giao diện trực quan': 'Build workflows visually',
'Kết nối kho tri thức và công cụ qua MCP': 'Connect knowledge and tools through MCP',
'Phân quyền và kiểm soát luồng dữ liệu': 'Manage access and control data flows',
'Dành cho đội ngũ ứng dụng AI': 'For teams putting AI to work',
'Mở AI Studio': 'Open AI Studio',
'Từ yêu cầu đến mã nguồn cùng đội agent AI. Tổ chức công việc, thực thi trên nhánh Git và giữ quyền duyệt ở những bước quan trọng.': 'Go from requirements to code with a team of AI agents. Organize tasks, work on Git branches, and review the steps that matter.',
'Phân chia công việc cho đội agent': 'Assign tasks to your agent team',
'Viết mã, chạy kiểm thử và tạo commit': 'Write code, run tests, and commit changes',
'Theo dõi tiến độ và duyệt kết quả': 'Track progress and review results',
'Dành cho đội ngũ phát triển': 'For software development teams',
'Mở XDev Forge': 'Open XDev Forge',
'CÁCH TIẾP CẬN': 'OUR APPROACH',
'AI làm nhiều hơn.<br>Bạn vẫn nắm quyền.': 'AI does more.<br>You stay in control.',
'Công cụ tốt giúp bạn đi xa hơn,<br>với sự rõ ràng trong từng bước.': 'Better tools take you further,<br>with clarity at every step.',
'Bắt đầu từ công việc thật': 'Start with real work',
'Khai thác tri thức nội bộ, tự động hóa quy trình và xây phần mềm từ nhu cầu cụ thể.': 'Use internal knowledge, automate workflows, and build software around real needs.',
'Kết nối cách bạn làm việc': 'Connect the way you work',
'Đưa mô hình, nguồn dữ liệu, công cụ và kho mã vào luồng công việc của đội ngũ.': 'Bring models, data sources, tools, and repositories into your team’s workflow.',
'Giữ con người ở trung tâm': 'Keep people at the center',
'Bạn đặt mục tiêu, quản lý quyền truy cập và xem xét kết quả trước khi đi tiếp.': 'You set the goals, manage access, and review results before moving forward.',
'CHIA SẺ TỪ THỰC TẾ': 'LESSONS FROM REAL WORK',
'Cùng xây dựng.<br>Cùng học hỏi.': 'Build together.<br>Learn together.',
'Những ghi chép về lập trình, AI, DevOps và kiến trúc hệ thống. Từ điều đã học đến những gì đang làm.': 'Notes on programming, AI, DevOps, and system architecture. From what we learn to what we build.',
'Ghé blog.xdev.asia': 'Visit blog.xdev.asia',
'Chủ đề trên blog': 'Blog topics',
'Lập trình & AI': 'Programming & AI',
'Kiến trúc hệ thống': 'System architecture',
'Series học tập': 'Learning series',
'xDev Asia — Về đầu trang': 'xDev Asia — Back to top',
'Từ ý tưởng đến giá trị thực.': 'From ideas to real value.',
}

def build():
    template = (ROOT / 'src/index.vi.html').read_text()
    english = template
    # Longest first so short labels cannot alter longer sentences.
    for vi, en in sorted(translations.items(), key=lambda item: -len(item[0])):
        if vi not in template:
            raise ValueError(f'Translation source missing: {vi}')
        english = english.replace(vi, en)
    english = english.replace('lang="vi"', 'lang="en"', 1)
    for language, page in [('en', english), ('vi', template)]:
        prefix = './' if language == 'en' else '../'
        page = page.replace('href="assets/', f'href="{prefix}assets/').replace('src="assets/', f'src="{prefix}assets/').replace('href="styles.css"', f'href="{prefix}styles.css"')
        current_en = ' aria-current="page"' if language == 'en' else ''
        current_vi = ' aria-current="page"' if language == 'vi' else ''
        switcher = f'<div class="language-switch" role="group" aria-label="{"Language" if language == "en" else "Ngôn ngữ"}"><a href="{prefix}" lang="en" hreflang="en" aria-label="English"{current_en}>EN</a><a href="{prefix}vi/" lang="vi" hreflang="vi" aria-label="Tiếng Việt"{current_vi}>VI</a></div>'
        page = page.replace('</nav>', '</nav>' + switcher, 1)
        canonical = 'https://xdev.asia/' + ('vi/' if language == 'vi' else '')
        metadata = f'<link rel="canonical" href="{canonical}">\n<link rel="alternate" hreflang="en" href="https://xdev.asia/">\n<link rel="alternate" hreflang="vi" href="https://xdev.asia/vi/">\n<link rel="alternate" hreflang="x-default" href="https://xdev.asia/">\n<meta property="og:locale" content="{"en_US" if language == "en" else "vi_VN"}">\n<meta property="og:url" content="{canonical}">\n'
        page = page.replace('</head>', metadata + '</head>')
        target = ROOT / 'dist' / ('index.html' if language == 'en' else 'vi/index.html')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)
    print('Generated English / and Vietnamese /vi/.')

if __name__ == '__main__':
    build()
