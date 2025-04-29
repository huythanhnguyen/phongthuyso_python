# MongoDB Database Module

Module này cung cấp các hàm tiện ích để kết nối và thao tác với cơ sở dữ liệu MongoDB trong dự án Phong Thủy Số.

## Cấu trúc

Module bao gồm các thành phần chính:

- `mongodb.py`: Cung cấp kết nối với MongoDB và các hàm quản lý kết nối
- `models.py`: Cung cấp các hàm tiện ích để thao tác với các collection
- `test_connection.py`: Script để kiểm tra kết nối với MongoDB

## Cấu hình kết nối

Kết nối MongoDB được cấu hình thông qua biến môi trường hoặc chuỗi kết nối mặc định:

```python
# Chuỗi kết nối MongoDB từ biến môi trường hoặc giá trị mặc định
MONGODB_URI = os.environ.get(
    "MONGODB_URI",
    "mongodb+srv://hihuythanh:Thanh%401984@cluster0.tp90k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Tên database mặc định
DEFAULT_DB_NAME = os.environ.get("MONGODB_DB_NAME", "phongthuyso")
```

## Sử dụng cơ bản

### Kết nối tới MongoDB

```python
from shared_libraries.database.mongodb import get_database

async def example_function():
    # Lấy đối tượng database
    db = await get_database()
    
    # Thực hiện các thao tác với database
    users_collection = db["users"]
    user = await users_collection.find_one({"email": "example@example.com"})
```

### Sử dụng các hàm tiện ích

```python
from shared_libraries.database import models

async def example_function():
    # Tạo người dùng mới
    user_data = {
        "email": "user@example.com",
        "fullname": "Nguyễn Văn A",
        "hashed_password": "hashed_password_here"
    }
    user_id = await models.create_user(user_data)
    
    # Lấy thông tin người dùng
    user = await models.get_user_by_email("user@example.com")
    
    # Cập nhật thông tin người dùng
    await models.update_user(user_id, {"fullname": "Nguyễn Văn B"})
```

## Kiểm tra kết nối

Để kiểm tra kết nối tới MongoDB, chạy script `test_connection.py`:

```bash
cd phongthuyso_python
python -m shared_libraries.database.test_connection
```

## Collections

Module này sử dụng các collection sau:

- `users`: Lưu trữ thông tin người dùng
- `sessions`: Lưu trữ phiên làm việc
- `analyses`: Lưu trữ kết quả phân tích
- `payments`: Lưu trữ thông tin thanh toán
- `subscriptions`: Lưu trữ thông tin đăng ký gói dịch vụ
- `plans`: Lưu trữ thông tin các gói dịch vụ
- `api_keys`: Lưu trữ các API key 