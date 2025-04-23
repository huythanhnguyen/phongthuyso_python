# API Documentation - Phong Thuy So

API này cung cấp các endpoint để phân tích phong thủy số.

## Base URL

```
https://api.phongthuyso.com
```

Trong môi trường phát triển:

```
http://localhost:8000
```

## Authentication

API cung cấp hai phương thức xác thực:

1. **OAuth2 Bearer Token** - Dùng cho ứng dụng web và mobile
2. **API Key** - Dùng cho tích hợp với bên thứ ba

### OAuth2 Bearer Token

Để lấy token:

```
POST /api/user/token

body:
{
  "username": "user@example.com",
  "password": "password"
}
```

Sử dụng token trong header:

```
Authorization: Bearer {access_token}
```

### API Key

Sử dụng API key trong header:

```
api_key: pts_your_api_key
```

## Endpoints

### Health Check

```
GET /health
```

Kiểm tra trạng thái hoạt động của API.

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Get Agents

```
GET /agents
```

Lấy danh sách các agent có sẵn trong hệ thống.

**Response:**

```json
{
  "agents": [
    {
      "name": "Root Agent",
      "type": "root"
    }
  ]
}
```

### Analyze Number

```
GET /analyze_number
```

Phân tích một số điện thoại và trả về thông tin phong thủy.

**Parameters:**

- `number` (required): Số điện thoại cần phân tích
- `user_data` (optional): Thông tin người dùng bổ sung ở định dạng JSON

**Authentication:**
- Bearer Token hoặc API Key (không bắt buộc, nhưng sẽ tính vào quota nếu được cung cấp)

**Example Request:**

```
GET /analyze_number?number=0123456789
```

**Example Response:**

```json
{
  "agent": "Simple Agent",
  "status": "success",
  "content": "Phân tích số điện thoại 0123456789: Số chủ đạo của bạn là 9",
  "metadata": {
    "digits": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "digit_sum": 45,
    "master_number": 9,
    "user_info": {
      "email": "user@example.com",
      "quota_remaining": 10
    }
  }
}
```

**Error Response:**

```json
{
  "status": "error",
  "detail": "Error message"
}
```

### Chat with Agent

```
POST /api/chat
```

Gửi tin nhắn tới hệ thống agents.

**Authentication:**
- Bearer Token hoặc API Key (không bắt buộc, nhưng sẽ tính vào quota nếu được cung cấp)

**Request Body:**

```json
{
  "message": "Phong thủy số điện thoại 0123456789 như thế nào?",
  "context": {
    "user_id": "user123",
    "session_id": "session456"
  }
}
```

**Response:**

```json
{
  "agent": "Phong Thuy Agent",
  "status": "success",
  "content": "Số điện thoại 0123456789 có số chủ đạo là 9. Đây là số may mắn trong phong thủy...",
  "metadata": {
    "confidence": 0.95,
    "analysis_type": "phone_number",
    "user_info": {
      "email": "user@example.com",
      "quota_remaining": 10
    }
  }
}
```

```
GET /api/chat
```

Nhận phản hồi từ agents (Streaming).

**Parameters:**

- `session_id` (required): ID của phiên chat

**Response:**

Event stream dạng text/event-stream với các event chứa JSON:

```json
{
  "agent": "Phong Thuy Agent",
  "status": "streaming",
  "content": "Số điện thoại...",
  "is_final": false
}
```

### Upload Files

```
POST /api/upload
```

Upload file (hình ảnh, PDF, âm thanh).

**Request:**

Multipart form-data với các field:
- `file`: File cần upload
- `type` (optional): Loại file (image, pdf, audio, text)
- `metadata` (optional): Metadata về file ở định dạng JSON

**Response:**

```json
{
  "status": "success",
  "file_id": "f123456",
  "file_url": "/static/uploads/f123456.jpg",
  "metadata": {
    "file_type": "image",
    "file_size": 1024,
    "upload_date": "2023-07-15T10:30:00Z",
    "original_filename": "photo.jpg"
  }
}
```

### User Management

#### Đăng ký tài khoản mới

```
POST /api/user/register
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "fullname": "Họ Tên",
  "password": "mật_khẩu"
}
```

**Response:**

```json
{
  "id": "user_id",
  "email": "user@example.com",
  "fullname": "Họ Tên",
  "created_at": "2023-07-15T10:30:00Z",
  "updated_at": "2023-07-15T10:30:00Z",
  "is_active": true,
  "is_premium": false,
  "quota_remaining": 5
}
```

#### Đăng nhập

```
POST /api/user/token
```

**Request Body (form data):**

```
username=user@example.com
password=mật_khẩu
```

**Response:**

```json
{
  "access_token": "token_string",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "fullname": "Họ Tên",
    "created_at": "2023-07-15T10:30:00Z",
    "updated_at": "2023-07-15T10:30:00Z",
    "is_active": true,
    "is_premium": false,
    "quota_remaining": 5
  }
}
```

#### Thông tin người dùng hiện tại

```
GET /api/user/me
```

**Authentication:**
- Bearer Token (required)

**Response:**

```json
{
  "id": "user_id",
  "email": "user@example.com",
  "fullname": "Họ Tên",
  "created_at": "2023-07-15T10:30:00Z",
  "updated_at": "2023-07-15T10:30:00Z",
  "is_active": true,
  "is_premium": false,
  "quota_remaining": 5
}
```

#### Cập nhật thông tin người dùng

```
PUT /api/user/me
```

**Authentication:**
- Bearer Token (required)

**Request Body:**

```json
{
  "fullname": "Họ Tên Mới",
  "email": "new_email@example.com",
  "password": "mật_khẩu_mới"
}
```

**Response:**

```json
{
  "id": "user_id",
  "email": "new_email@example.com",
  "fullname": "Họ Tên Mới",
  "created_at": "2023-07-15T10:30:00Z",
  "updated_at": "2023-07-16T15:45:00Z",
  "is_active": true,
  "is_premium": false,
  "quota_remaining": 5
}
```

### API Key Management

#### Tạo API Key mới

```
POST /api/apikeys
```

**Authentication:**
- Bearer Token (required)

**Request Body:**

```json
{
  "name": "Tên API Key",
  "expires_at": "2024-07-15T00:00:00Z" (optional)
}
```

**Response:**

```json
{
  "id": "key_id",
  "key": "pts_api_key_string",
  "name": "Tên API Key",
  "created_at": "2023-07-15T10:30:00Z",
  "expires_at": "2024-07-15T00:00:00Z",
  "last_used_at": null,
  "is_active": true
}
```

#### Lấy danh sách API Key

```
GET /api/apikeys
```

**Authentication:**
- Bearer Token (required)

**Response:**

```json
[
  {
    "id": "key_id_1",
    "key": "pts_api_key_string_1",
    "name": "API Key 1",
    "created_at": "2023-07-15T10:30:00Z",
    "expires_at": "2024-07-15T00:00:00Z",
    "last_used_at": "2023-07-16T15:45:00Z",
    "is_active": true
  },
  {
    "id": "key_id_2",
    "key": "pts_api_key_string_2",
    "name": "API Key 2",
    "created_at": "2023-08-20T14:20:00Z",
    "expires_at": null,
    "last_used_at": null,
    "is_active": true
  }
]
```

#### Xóa API Key

```
DELETE /api/apikeys/{api_key_id}
```

**Authentication:**
- Bearer Token (required)

**Response:**

```json
{
  "message": "API key deleted successfully"
}
```

### Payment and Subscription

#### Danh sách các gói dịch vụ

```
GET /api/payment/plans
```

**Response:**

```json
[
  {
    "id": "free",
    "name": "Miễn phí",
    "type": "free",
    "price": 0,
    "currency": "VND",
    "interval": "month",
    "description": "Gói dùng thử miễn phí",
    "features": ["Phân tích cơ bản số điện thoại", "5 lần phân tích/ngày"],
    "quota": 5,
    "created_at": "2023-07-15T10:30:00Z",
    "updated_at": "2023-07-15T10:30:00Z"
  },
  {
    "id": "basic",
    "name": "Cơ bản",
    "type": "basic",
    "price": 99000,
    "currency": "VND",
    "interval": "month",
    "description": "Gói cơ bản cho người dùng cá nhân",
    "features": ["Phân tích đầy đủ số điện thoại", "Phân tích CCCD", "50 lần phân tích/tháng"],
    "quota": 50,
    "created_at": "2023-07-15T10:30:00Z",
    "updated_at": "2023-07-15T10:30:00Z"
  }
]
```

#### Chi tiết gói dịch vụ

```
GET /api/payment/plans/{plan_id}
```

**Response:**

```json
{
  "id": "basic",
  "name": "Cơ bản",
  "type": "basic",
  "price": 99000,
  "currency": "VND",
  "interval": "month",
  "description": "Gói cơ bản cho người dùng cá nhân",
  "features": ["Phân tích đầy đủ số điện thoại", "Phân tích CCCD", "50 lần phân tích/tháng"],
  "quota": 50,
  "created_at": "2023-07-15T10:30:00Z",
  "updated_at": "2023-07-15T10:30:00Z"
}
```

#### Tạo thanh toán mới

```
POST /api/payment
```

**Authentication:**
- Bearer Token (required)

**Request Body:**

```json
{
  "plan_id": "basic",
  "payment_method": "credit_card",
  "amount": 99000,
  "currency": "VND"
}
```

**Response:**

```json
{
  "id": "payment_id",
  "user_id": "user_id",
  "plan_id": "basic",
  "payment_method": "credit_card",
  "amount": 99000,
  "currency": "VND",
  "status": "completed",
  "created_at": "2023-07-15T10:30:00Z",
  "updated_at": "2023-07-15T10:30:00Z",
  "transaction_id": "txn_123456"
}
```

#### Lịch sử thanh toán

```
GET /api/payment/history
```

**Authentication:**
- Bearer Token (required)

**Response:**

```json
[
  {
    "id": "payment_id_1",
    "user_id": "user_id",
    "plan_id": "basic",
    "payment_method": "credit_card",
    "amount": 99000,
    "currency": "VND",
    "status": "completed",
    "created_at": "2023-07-15T10:30:00Z",
    "updated_at": "2023-07-15T10:30:00Z",
    "transaction_id": "txn_123456"
  },
  {
    "id": "payment_id_2",
    "user_id": "user_id",
    "plan_id": "premium",
    "payment_method": "bank_transfer",
    "amount": 199000,
    "currency": "VND",
    "status": "completed",
    "created_at": "2023-08-15T14:20:00Z",
    "updated_at": "2023-08-15T14:20:00Z",
    "transaction_id": "txn_789012"
  }
]
```

#### Thông tin gói đăng ký hiện tại

```
GET /api/payment/subscription
```

**Authentication:**
- Bearer Token (required)

**Response:**

```json
{
  "id": "subscription_id",
  "user_id": "user_id",
  "plan_id": "basic",
  "status": "active",
  "start_date": "2023-07-15T10:30:00Z",
  "end_date": "2023-08-15T10:30:00Z",
  "created_at": "2023-07-15T10:30:00Z",
  "updated_at": "2023-07-15T10:30:00Z",
  "is_active": true,
  "auto_renew": true
}
```

## Error Handling

API trả về các mã lỗi HTTP tiêu chuẩn:

- `400 Bad Request`: Dữ liệu đầu vào không hợp lệ
- `401 Unauthorized`: Không được xác thực hoặc xác thực thất bại
- `402 Payment Required`: Cần thanh toán để sử dụng (hết quota)
- `403 Forbidden`: Không có quyền truy cập 
- `404 Not Found`: Không tìm thấy tài nguyên
- `422 Unprocessable Entity`: Lỗi validation
- `500 Internal Server Error`: Lỗi server không mong muốn

Tất cả phản hồi lỗi đều có cấu trúc:

```json
{
  "status": "error",
  "detail": "Mô tả chi tiết về lỗi"
}
``` 