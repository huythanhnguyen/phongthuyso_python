# Phong Thuy So

Ứng dụng phân tích Bát Cục Linh Số dựa trên công nghệ AI.

## Kết nối MongoDB

### Cấu hình kết nối

Ứng dụng sử dụng MongoDB Atlas làm cơ sở dữ liệu chính. Chuỗi kết nối mặc định đã được cấu hình trong mã nguồn:

```python
# MongoDB connection string từ biến môi trường hoặc chuỗi mặc định
MONGODB_URI = os.environ.get(
    "MONGODB_URI", 
    "mongodb+srv://hihuythanh:Thanh%401984@cluster0.tp90k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Tên database mặc định
DEFAULT_DB_NAME = os.environ.get("MONGODB_DB_NAME", "phongthuyso")
```

### Kiểm tra kết nối

Bạn có thể kiểm tra kết nối MongoDB bằng cách chạy script test_mongodb.py:

```bash
python test_mongodb.py
```

### Sử dụng trong ứng dụng

Kết nối MongoDB được tự động khởi tạo khi ứng dụng khởi động qua sự kiện `startup_event` trong file `main.py`.

Để sử dụng MongoDB trong code, bạn có thể sử dụng các hàm tiện ích trong module `shared_libraries.database.models`:

```python
from shared_libraries.database import models

async def my_function():
    # Lấy thông tin người dùng
    user = await models.get_user_by_email("example@example.com")
    
    # Thêm bản ghi phân tích mới
    analysis_data = {
        "user_id": user["_id"],
        "phone_number": "0912345678",
        "result": "Số điện thoại có ngũ hành Kim mạnh..."
    }
    analysis_id = await models.create_analysis(analysis_data)
```

## Các Collections

Ứng dụng sử dụng các collections sau trong MongoDB:

- `users`: Lưu trữ thông tin người dùng
- `sessions`: Lưu trữ phiên làm việc
- `analyses`: Lưu trữ kết quả phân tích
- `payments`: Lưu trữ thông tin thanh toán
- `subscriptions`: Lưu trữ thông tin đăng ký gói dịch vụ
- `plans`: Lưu trữ thông tin các gói dịch vụ
- `api_keys`: Lưu trữ các API key

## Khởi chạy ứng dụng

```bash
# Cài đặt các dependencies
pip install -r requirements.txt

# Khởi chạy ứng dụng
python main.py
```

Ứng dụng sẽ chạy tại địa chỉ http://localhost:8000 mặc định. 