# Phong Thủy Số

Hệ thống phân tích và tư vấn phong thủy dựa trên AI, cung cấp các dịch vụ phân tích bát tự, thần số học và các phân tích phong thủy khác thông qua API RESTful và giao diện người dùng thân thiện.

## Tính năng chính

- Phân tích bát cục linh số (Bát Tự)
- Tư vấn phong thủy cá nhân
- Hỗ trợ nhiều phương pháp luận khác nhau
- Tương tác thông qua trò chuyện tự nhiên
- Hệ thống thanh toán tích hợp
- Quản lý tài khoản người dùng

## Cài đặt

### Yêu cầu hệ thống

- Python 3.9+
- MongoDB
- Google ADK và API keys cho các dịch vụ liên quan

### Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Biến môi trường

Tạo file `.env` trong thư mục gốc với nội dung:

```
MONGODB_URI=your_mongodb_connection_string
GOOGLE_APPLICATION_CREDENTIALS=path_to_your_google_credentials.json
SECRET_KEY=your_secret_key_for_jwt
```

## Chạy ứng dụng

### Chạy với dữ liệu mẫu

```bash
python run_app_with_seed.py
```

### Chạy ở chế độ debug

```bash
python run_app_debug.py
```

### Chạy tests

```bash
pytest
```

## Kiến trúc

Dự án sử dụng kiến trúc agent-based với các thành phần chính:

- **Root Agent**: Điều phối các agent con và xử lý luồng chính
- **User Agent**: Quản lý thông tin và tương tác người dùng
- **Bát Cục Linh Số Agent**: Phân tích dữ liệu phong thủy chuyên sâu
- **Payment Agent**: Xử lý các giao dịch thanh toán

Chi tiết thêm về kiến trúc xem trong file `architecture.md`.

## API

Tài liệu API đầy đủ có thể tìm thấy trong file `api.md`.

## Đóng góp

- Tuân thủ các quy tắc trong `.cursor.rule`
- Tạo pull request với mô tả chi tiết về thay đổi
- Viết test cho các tính năng mới
- Đảm bảo code đã được kiểm tra với flake8 và mypy

## Giấy phép

Mã nguồn này được cấp phép riêng và không được sử dụng hoặc phân phối nếu không có sự cho phép rõ ràng. 