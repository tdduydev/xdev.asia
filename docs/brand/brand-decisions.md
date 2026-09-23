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
