# API Documentation - Phong Thủy Số

## Authentication

Các API yêu cầu xác thực qua một trong hai cách:
- JWT Token thông qua Authorization header
- API Key thông qua api_key header

### Đăng nhập
```
POST /api/user/token
```
Request:
```json
{
  "username": "email@example.com",
  "password": "password"
}
```
Response:
```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "name": "User Name",
    "email": "email@example.com",
    "role": "user",
    "isPremium": false,
    "remainingQuestions": 5,
    "createdAt": "2023-09-01T00:00:00Z"
  }
}
```

### Đăng ký
```
POST /api/user/register
```
Request:
```json
{
  "name": "User Name",
  "email": "email@example.com",
  "password": "password",
  "phoneNumber": "0987654321"
}
```
Response:
```json
{
  "id": "user_id",
  "name": "User Name",
  "email": "email@example.com",
  "role": "user",
  "phoneNumber": "0987654321",
  "remainingQuestions": 5,
  "isPremium": false,
  "createdAt": "2023-09-01T00:00:00Z"
}
```

## Phân tích số điện thoại

### Phân tích số điện thoại
```
POST /api/batcuclinh_so/analyze_phone
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```
hoặc
```
api_key: YOUR_API_KEY
```

Request:
```json
{
  "phone_number": "0987654321",
  "request_type": "phone_analysis",
  "context": {
    "purpose": "kinh doanh"
  }
}
```
Response:
```json
{
  "phone_number": "0987654321",
  "network_code": "098",
  "subscriber_number": "7654321",
  "analysis": [
    {
      "number": "09",
      "tinh": "SINH_KHI",
      "name": "Sinh Khí",
      "description": "Vui vẻ, quý nhân, dẫn đạo lực",
      "energy": 3,
      "position": "Nên ở giữa",
      "nature": "Cát"
    },
    // ... Các cặp số khác
  ],
  "combinations": [
    {
      "numbers": "09-87",
      "combination": "SINH_KHI_LUC_SAT",
      "description": "Quý nhân gặp xung đột",
      "detailed_description": "..."
    }
  ],
  "total_score": 7.5,
  "luck_level": "Tốt"
}
```

### Lấy lịch sử phân tích
```
GET /api/phone-analysis/history?limit=10&skip=0
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Response:
```json
[
  {
    "_id": "analysis_id",
    "userId": "user_id",
    "phoneNumber": "0987654321",
    "createdAt": "2023-09-01T00:00:00Z",
    "result": {
      "total_score": 7.5,
      "luck_level": "Tốt"
    }
  },
  // ... Các phân tích khác
]
```

### Lấy chi tiết phân tích
```
GET /api/phone-analysis/{phone_number}
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Response:
```json
{
  "_id": "analysis_id",
  "userId": "user_id",
  "phoneNumber": "0987654321",
  "result": {
    "phone_number": "0987654321",
    "network_code": "098",
    "subscriber_number": "7654321",
    "analysis": [...],
    "combinations": [...],
    "total_score": 7.5,
    "luck_level": "Tốt"
  },
  "geminiResponse": "...",
  "createdAt": "2023-09-01T00:00:00Z"
}
```

## Gợi ý số điện thoại
```
GET /analyze_number?number={number}&user_data={user_data_json}
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```
hoặc
```
api_key: YOUR_API_KEY
```

Tham số:
- `number`: Số điện thoại cần phân tích
- `user_data`: Dữ liệu người dùng bổ sung (JSON string)

Response:
```json
{
  "agent": "BatCucLinhSo Agent",
  "status": "success",
  "content": "Phân tích chi tiết số điện thoại...",
  "metadata": {
    "score": 7.5,
    "luck_level": "Tốt",
    "analysis": {...}
  }
}
```

## Quản lý tài khoản

### Thông tin người dùng
```
GET /api/user/me
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Response:
```json
{
  "id": "user_id",
  "name": "User Name",
  "email": "email@example.com",
  "role": "user",
  "phoneNumber": "0987654321",
  "remainingQuestions": 5,
  "isPremium": false,
  "createdAt": "2023-09-01T00:00:00Z",
  "lastLogin": "2023-09-01T00:00:00Z"
}
```

### Cập nhật thông tin người dùng
```
PUT /api/user/me
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Request:
```json
{
  "fullname": "New Name",
  "email": "new.email@example.com",
  "password": "new_password"
}
```

Response:
```json
{
  "id": "user_id",
  "name": "New Name",
  "email": "new.email@example.com",
  "role": "user",
  "phoneNumber": "0987654321",
  "remainingQuestions": 5,
  "isPremium": false,
  "createdAt": "2023-09-01T00:00:00Z",
  "lastLogin": "2023-09-01T00:00:00Z"
}
```

## API Keys

### Tạo API key
```
POST /api/apikeys
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Request:
```json
{
  "name": "My API Key",
  "expires_at": "2024-09-01T00:00:00Z"
}
```

Response:
```json
{
  "id": "key_id",
  "key": "api_key_value",
  "name": "My API Key",
  "created_at": "2023-09-01T00:00:00Z",
  "expires_at": "2024-09-01T00:00:00Z",
  "last_used_at": null,
  "is_active": true
}
```

### Danh sách API keys
```
GET /api/apikeys
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Response:
```json
[
  {
    "id": "key_id",
    "key": "api_key_value",
    "name": "My API Key",
    "created_at": "2023-09-01T00:00:00Z",
    "expires_at": "2024-09-01T00:00:00Z",
    "last_used_at": null,
    "is_active": true
  }
]
```

### Xóa API key
```
DELETE /api/apikeys/{api_key_id}
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Response:
```json
{
  "message": "API key deleted successfully"
}
```

## Thanh toán và gói dịch vụ

### Danh sách gói
```
GET /api/payment/plans
```

Response:
```json
[
  {
    "id": "plan_id",
    "name": "Gói Cơ Bản",
    "type": "basic",
    "price": 100000,
    "currency": "VND",
    "interval": "month",
    "description": "Gói cơ bản với 50 lần phân tích mỗi tháng",
    "features": [
      "Phân tích số điện thoại",
      "Lịch sử phân tích"
    ],
    "quota": 50,
    "created_at": "2023-09-01T00:00:00Z",
    "updated_at": "2023-09-01T00:00:00Z"
  }
]
```

### Chi tiết gói
```
GET /api/payment/plans/{plan_id}
```

Response:
```json
{
  "id": "plan_id",
  "name": "Gói Cơ Bản",
  "type": "basic",
  "price": 100000,
  "currency": "VND",
  "interval": "month",
  "description": "Gói cơ bản với 50 lần phân tích mỗi tháng",
  "features": [
    "Phân tích số điện thoại",
    "Lịch sử phân tích"
  ],
  "quota": 50,
  "created_at": "2023-09-01T00:00:00Z",
  "updated_at": "2023-09-01T00:00:00Z"
}
```

### Tạo thanh toán
```
POST /api/payment
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Request:
```json
{
  "plan_id": "plan_id",
  "payment_method": "credit_card",
  "amount": 100000,
  "currency": "VND"
}
```

Response:
```json
{
  "id": "payment_id",
  "user_id": "user_id",
  "plan_id": "plan_id",
  "payment_method": "credit_card",
  "amount": 100000,
  "currency": "VND",
  "status": "completed",
  "created_at": "2023-09-01T00:00:00Z",
  "updated_at": "2023-09-01T00:00:00Z",
  "transaction_id": "transaction_id"
}
```

### Lịch sử thanh toán
```
GET /api/payment/history
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Response:
```json
[
  {
    "id": "payment_id",
    "user_id": "user_id",
    "plan_id": "plan_id",
    "payment_method": "credit_card",
    "amount": 100000,
    "currency": "VND",
    "status": "completed",
    "created_at": "2023-09-01T00:00:00Z",
    "updated_at": "2023-09-01T00:00:00Z",
    "transaction_id": "transaction_id"
  }
]
```

### Gói đăng ký hiện tại
```
GET /api/payment/subscription
```
Headers:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

Response:
```json
{
  "id": "subscription_id",
  "user_id": "user_id",
  "plan_id": "plan_id",
  "status": "active",
  "start_date": "2023-09-01T00:00:00Z",
  "end_date": "2023-10-01T00:00:00Z",
  "created_at": "2023-09-01T00:00:00Z",
  "updated_at": "2023-09-01T00:00:00Z",
  "is_active": true,
  "auto_renew": true
}
```

## Kiểm tra sức khỏe hệ thống

### Kiểm tra trạng thái
```
GET /health
```

Response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime": 3600
}
```

## Danh sách agents
```
GET /agents
```

Response:
```json
{
  "agents": [
    {
      "name": "Root Agent",
      "type": "root",
      "model": "gemini-2.0-flash",
      "status": "active"
    },
    {
      "name": "BatCucLinhSo Agent",
      "type": "bat_cuc_linh_so",
      "model": "gemini-2.0-flash",
      "status": "active"
    }
  ]
}
``` 