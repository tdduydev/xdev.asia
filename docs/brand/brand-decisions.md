# Bộ nhận diện xDev đã chốt

Ngày ghi nhận: 2026-09-23.

## Quyết định thiết kế

- Giữ tên thương hiệu **xDev** và chữ **X** xanh chuyển sắc của website hiện tại.
- Giữ nguyên hình thức chữ X, gradient và hiệu ứng sáng của từng phiên bản nền sáng/tối.
- Suffix **DEV** dùng nét SVG thanh, đầu nét và góc nối tròn. Cách viết tên trong nội dung vẫn là xDev.
- **AI Studio** dùng AI ở dòng trên, STUDIO nhỏ hơn ở dòng dưới. AI bắt đầu tại y=12; STUDIO tại y=43, kết thúc khoảng y=50.4, nằm trong chiều cao chữ X. Đây là bản căn chỉnh được người dùng chọn.
- **NOTES** chỉ minh họa khả năng mở rộng bộ nhận diện; chưa phải tên sản phẩm mới được chốt.
- Các phương án dev/Dev và hình tạo trước đó là tài liệu thử nghiệm, không phải logo được chọn.

## Nguồn và trang giới thiệu

- SVG được chọn: `src/assets/brand/wordmark-v2/master-{light,dark}.svg` và `ai-studio-{light,dark}.svg`.
- Nội dung: `src/brand.vi.json`, `src/brand.en.json`.
- Trang công khai: `/vi/brand/` và `/brand/`, truy cập qua liên kết ở chân trang.
- Bộ chữ phía sau X là đường vector; X vẫn là phần tử chữ như tài sản gốc. Khi cần bản xuất in ấn độc lập với font, chuyển X thành outline bằng đúng font đã duyệt.

Trang thương hiệu ghi lại ý tưởng, màu sắc, biến thể và hướng dẫn sử dụng. Giữ nguyên tỷ lệ logo, dùng đúng biến thể theo nền và dành khoảng trống quanh logo. Không kéo giãn hoặc tự vẽ lại chữ X khi thêm tên sản phẩm.

## xDev Hive — 2026-09-30

- Ban đầu chọn **X + HIVE** trên một dòng; được thay bằng bố cục HIVE / DEV HUB bên dưới. HIVE dùng cùng nét SVG 2.1, chữ hoa cao 24 đơn vị và góc bo của DEV.
- Giữ nguyên X gốc của từng bản nền sáng/tối, gồm gradient và hiệu ứng sáng.
- Tên trong nội dung là **xDev Hive**. Bản DEV / HIVE hai dòng và ý tưởng tổ ong hổ phách chỉ là thử nghiệm.
- File được chọn: `src/assets/brand/wordmark-v2/hive-{light,dark}.svg`. Cả hai có nền trong suốt, được giới thiệu và tải từ trang brand EN/VI.

## Bố cục HIVE / DEV HUB — 2026-09-30

- Người dùng chốt **HIVE / DEV HUB** theo cấu trúc AI / STUDIO: HIVE ở y=12, DEV HUB ở y=43, scale .31 và nét 2.4 như dòng STUDIO.
- DEV HUB thể hiện trọng tâm phát triển phần mềm. Tên trong nội dung vẫn là **xDev Hive**.
- Giữ nguyên X, gradient và hiệu ứng của bản nền sáng/tối. File `hive-{light,dark}.svg` là tài sản chính đã cập nhật; bản HIVE một dòng và DEV / HIVE chỉ là lịch sử thử nghiệm.

## xDraft — 2026-10-10

- MindMap AI đổi tên thành **xDraft** từ bản 2.0.0 (ADR 0017 trong repo `tdduydev/xdev-xdraft`). Tên trong nội dung là **xDraft**, tên đầy đủ **xDraft by xDev**, subtitle **AI Diagram Studio**.
- Icon app: product owner chọn **hướng A (Flow)** ngày 2026-10-10. Chữ X nối bằng connector vuông góc tới ba hình: hộp bo góc, hình thoi, hình trụ. Hướng B (Architecture) và C (Draft line) chỉ là thử nghiệm. Icon web `src/assets/apps/xdraft/{icon,favicon}.png` được render từ các layer SVG của `AppIcon.icon` trên nhánh MM-177.
- Lockup **X + DRAFT / AI DIAGRAM STUDIO** theo cấu trúc HIVE / DEV HUB: DRAFT ở y=12, AI DIAGRAM STUDIO ở y=43, scale .31, nét 2.4. Chữ D-R-A-F-T là đường vector, nét 2.1, chữ hoa cao 24 đơn vị. Light suffix #344568, dark #E8ECF8. viewBox 224 × 78.
- Giữ nguyên X, gradient và hiệu ứng sáng của từng bản nền sáng/tối, chép từ `hive-{light,dark}.svg`.
- File được chọn: `src/assets/brand/wordmark-v2/xdraft-{light,dark}.svg` (lockup hai dòng). Dùng ở trang sản phẩm và trang brand EN/VI. Bản X + DRAFT một dòng nằm ở `docs/brand/xdraft/` của repo app, dành cho chỗ quá hẹp; site chưa dùng.
- Chưa tra nhãn hiệu trong sổ đăng ký chính thức. Phải tra trước khi đổi tên trên App Store (ADR 0017).
