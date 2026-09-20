# xDev Asia landing page

Trang giới thiệu tiếng Việt cho XDev AI Studio và XDev Forge. Website tĩnh, không cần build hay dependencies.

## Xem tại máy

```sh
python3 -m http.server 4321 --directory dist --bind 127.0.0.1
```

Nội dung và giao diện nằm trong `dist/index.html`, `dist/styles.css`. Logo, favicon và font lấy từ blog.xdev.asia ngày 2026-09-20. Logo giữ nguyên SVG gốc. Các liên kết sản phẩm dùng ai-studio.xdev.asia và forge.xdev.asia.

Có thể phục vụ thư mục `dist` bằng bất kỳ static web server nào. Cấu hình Sites được lưu tại `.openai/hosting.json` khi đăng ký thành công. Việc tạo trang không tự thay đổi DNS của xdev.asia.
