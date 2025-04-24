# API Phong Thuỷ Số

API này cung cấp các endpoint để phân tích phong thủy số và quản lý người dùng.

## Base URL

```
http://localhost:8000
```

## Xác thực

API sử dụng xác thực OAuth2 với JWT token. Để gọi các API yêu cầu xác thực, thêm header sau:

```
Authorization: Bearer {token}
```

Bạn có thể lấy token bằng cách gọi API đăng nhập `/api/user/token`.

## API Công khai

### Health Check

Kiểm tra trạng thái hoạt động của API.

```
GET /health
```

**Response:**

```json
{
  "status": "ok",
  "timestamp": "2025-04-24T01:10:00Z"
}
```

### Lấy danh sách agent

Trả về danh sách các agent có sẵn.

```
GET /agents
```

**Response:**

```json
{
  "agents": [
    {
      "id": "phongthuy_agent",
      "name": "Phong Thủy Agent",
      "description": "Phân tích phong thủy số điện thoại"
    }
  ]
}
```

### Phân tích số điện thoại

Phân tích số điện thoại theo phong thủy.

```
GET /analyze_number
```

**Parameters:**

- `number` (required): Số điện thoại cần phân tích
- `user_data` (optional): Dữ liệu người dùng bổ sung dưới dạng JSON

**Response:**

```json
{
  "agent": "phongthuy_agent",
  "status": "success",
  "content": "Phân tích chi tiết về số điện thoại",
  "metadata": {
    "number": "0912345678",
    "score": 85,
    "elements": ["Kim", "Mộc"],
    "lucky_elements": ["Kim"],
    "recommendations": ["Phù hợp với người mệnh Kim"]
  }
}
```

## API Chat

### Gửi tin nhắn chat

Gửi tin nhắn để trò chuyện với bot.

```
POST /api/chat
```

**Request Body:**

```json
{
  "message": "Phân tích số 0912345678",
  "context": {
    "user_id": "user123"
  }
}
```

**Response:**

```json
{
  "agent": "phongthuy_agent",
  "status": "success",
  "content": "Đang phân tích số 0912345678...",
  "metadata": {
    "session_id": "sess_123456"
  },
  "is_final": false
}
```

### Nhận kết quả chat

Nhận kết quả cuối cùng của cuộc trò chuyện.

```
GET /api/chat?session_id={session_id}
```

**Parameters:**

- `session_id` (required): ID phiên chat từ response trước đó

**Response:**

```json
{
  "agent": "phongthuy_agent",
  "status": "success",
  "content": "Số 0912345678 có yếu tố Kim mạnh, phù hợp với người mệnh Kim...",
  "metadata": {
    "analysis": {
      "score": 85,
      "elements": ["Kim", "Mộc"]
    }
  },
  "is_final": true
}
```

## API Người dùng

### Đăng ký người dùng

Đăng ký người dùng mới.

```
POST /api/user/register
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "fullname": "Nguyễn Văn A",
  "password": "your-password"
}
```

**Response:**

```json
{
  "id": "user_123",
  "email": "user@example.com",
  "fullname": "Nguyễn Văn A",
  "created_at": "2025-04-24T01:10:00Z",
  "updated_at": "2025-04-24T01:10:00Z",
  "is_active": true,
  "is_premium": false,
  "quota_remaining": 10
}
```

### Đăng nhập

Đăng nhập và lấy token truy cập.

```
POST /api/user/token
```

**Request Body (form data):**

```
username: user@example.com
password: your-password
```

**Response:**

```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "fullname": "Nguyễn Văn A",
    "created_at": "2025-04-24T01:10:00Z",
    "updated_at": "2025-04-24T01:10:00Z",
    "is_active": true,
    "is_premium": false,
    "quota_remaining": 10
  }
}
```

### Lấy thông tin người dùng hiện tại

Lấy thông tin người dùng đã đăng nhập.

```
GET /api/user/me
```

**Response:**

```json
{
  "id": "user_123",
  "email": "user@example.com",
  "fullname": "Nguyễn Văn A",
  "created_at": "2025-04-24T01:10:00Z",
  "updated_at": "2025-04-24T01:10:00Z",
  "is_active": true,
  "is_premium": false,
  "quota_remaining": 10
}
```

### Cập nhật thông tin người dùng

Cập nhật thông tin người dùng.

```
PUT /api/user/me
```

**Request Body:**

```json
{
  "fullname": "Nguyễn Văn B",
  "email": "userb@example.com"
}
```

**Response:**

```json
{
  "id": "user_123",
  "email": "userb@example.com",
  "fullname": "Nguyễn Văn B",
  "created_at": "2025-04-24T01:10:00Z",
  "updated_at": "2025-04-24T01:15:00Z",
  "is_active": true,
  "is_premium": false,
  "quota_remaining": 10
}
```

## API Key

### Tạo API Key

Tạo API key mới.

```
POST /api/apikeys
```

**Request Body:**

```json
{
  "name": "Frontend App"
}
```

**Response:**

```json
{
  "id": "key_123",
  "key": "pk_test_123456",
  "name": "Frontend App",
  "created_at": "2025-04-24T01:20:00Z",
  "expires_at": null,
  "last_used_at": null,
  "is_active": true
}
```

### Lấy danh sách API Key

Lấy danh sách API key của người dùng.

```
GET /api/apikeys
```

**Response:**

```json
[
  {
    "id": "key_123",
    "key": "pk_test_123456",
    "name": "Frontend App",
    "created_at": "2025-04-24T01:20:00Z",
    "expires_at": null,
    "last_used_at": null,
    "is_active": true
  }
]
```

### Xóa API Key

Xóa API key.

```
DELETE /api/apikeys/{api_key_id}
```

**Response:**

```json
{
  "message": "API key deleted successfully"
}
```

## API Thanh toán

### Lấy danh sách gói dịch vụ

Lấy danh sách các gói dịch vụ có sẵn.

```
GET /api/payment/plans
```

**Response:**

```json
[
  {
    "id": "plan_free",
    "name": "Gói Miễn phí",
    "type": "free",
    "price": 0,
    "currency": "VND",
    "interval": "month",
    "description": "Dùng thử với số lượt giới hạn",
    "features": ["Phân tích cơ bản", "10 lượt tra cứu"],
    "quota": 10,
    "created_at": "2025-04-24T01:10:00Z",
    "updated_at": "2025-04-24T01:10:00Z"
  },
  {
    "id": "plan_basic",
    "name": "Gói Cơ bản",
    "type": "basic",
    "price": 99000,
    "currency": "VND",
    "interval": "month",
    "description": "Phù hợp cho người dùng cá nhân",
    "features": ["Phân tích đầy đủ", "100 lượt tra cứu", "Hỗ trợ qua email"],
    "quota": 100,
    "created_at": "2025-04-24T01:10:00Z",
    "updated_at": "2025-04-24T01:10:00Z"
  }
]
```

### Lấy chi tiết gói dịch vụ

Lấy thông tin chi tiết về một gói dịch vụ.

```
GET /api/payment/plans/{plan_id}
```

**Response:**

```json
{
  "id": "plan_basic",
  "name": "Gói Cơ bản",
  "type": "basic",
  "price": 99000,
  "currency": "VND",
  "interval": "month",
  "description": "Phù hợp cho người dùng cá nhân",
  "features": ["Phân tích đầy đủ", "100 lượt tra cứu", "Hỗ trợ qua email"],
  "quota": 100,
  "created_at": "2025-04-24T01:10:00Z",
  "updated_at": "2025-04-24T01:10:00Z"
}
```

### Tạo thanh toán

Tạo một thanh toán mới.

```
POST /api/payment
```

**Request Body:**

```json
{
  "plan_id": "plan_basic",
  "payment_method": "momo",
  "amount": 99000,
  "currency": "VND"
}
```

**Response:**

```json
{
  "id": "payment_123",
  "user_id": "user_123",
  "plan_id": "plan_basic",
  "payment_method": "momo",
  "amount": 99000,
  "currency": "VND",
  "status": "pending",
  "created_at": "2025-04-24T01:25:00Z",
  "updated_at": "2025-04-24T01:25:00Z",
  "transaction_id": null
}
```

### Lấy lịch sử thanh toán

Lấy lịch sử thanh toán của người dùng.

```
GET /api/payment/history
```

**Response:**

```json
[
  {
    "id": "payment_123",
    "user_id": "user_123",
    "plan_id": "plan_basic",
    "payment_method": "momo",
    "amount": 99000,
    "currency": "VND",
    "status": "completed",
    "created_at": "2025-04-24T01:25:00Z",
    "updated_at": "2025-04-24T01:30:00Z",
    "transaction_id": "tx_momo_123"
  }
]
```

### Lấy thông tin đăng ký

Lấy thông tin gói đăng ký hiện tại của người dùng.

```
GET /api/payment/subscription
```

**Response:**

```json
{
  "id": "sub_123",
  "user_id": "user_123",
  "plan_id": "plan_basic",
  "status": "active",
  "start_date": "2025-04-24T01:30:00Z",
  "end_date": "2025-05-24T01:30:00Z",
  "created_at": "2025-04-24T01:30:00Z",
  "updated_at": "2025-04-24T01:30:00Z",
  "is_active": true,
  "auto_renew": true
}
```

## Upload File

### Upload file

Tải lên file (ảnh hoặc tài liệu).

```
POST /api/upload
```

**Request Body (form-data):**

```
file: (binary)
type: "image"
metadata: "{\"description\":\"Ảnh mô tả\"}"
```

**Response:**

```json
{
  "filename": "f12345.jpg",
  "url": "/static/uploads/f12345.jpg",
  "type": "image",
  "size": 12345,
  "metadata": {
    "description": "Ảnh mô tả"
  }
}
``` 