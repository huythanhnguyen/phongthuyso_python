# API Interface - Phong Thuy So Bot

## Tổng quan
Tài liệu này mô tả các endpoints API hiện có trong ứng dụng Phong Thuy So Bot.

## Endpoint chung

### GET /
- **Mô tả:** Trang chủ, trả về trang HTML hoặc thông báo chào mừng.
- **Input:** Không có
- **Output:** HTML hoặc JSON `{"message": "Welcome to Phong Thuy API", "version": "1.0.0"}`
- **Trạng thái:** Đang hoạt động

### GET /health
- **Mô tả:** Kiểm tra trạng thái hoạt động của API
- **Input:** Không có
- **Output:** JSON `{"status": "healthy", "version": "1.0.0"}`
- **Trạng thái:** Đang hoạt động

### GET /agents
- **Mô tả:** Lấy danh sách các agents có sẵn
- **Input:** Không có
- **Output:** JSON danh sách các agents
- **Ví dụ:**
```json
{
  "agents": [
    {
      "name": "Root Agent",
      "type": "root",
      "description": "Agent chính điều phối các yêu cầu",
      "sub_agents": [
        {"name": "BatCucLinhSo Agent", "type": "batcuclinh_so"},
        {"name": "Payment Agent", "type": "payment"},
        {"name": "User Agent", "type": "user"}
      ]
    }
  ]
}
```
- **Trạng thái:** Đang hoạt động

## Endpoints phân tích số

### GET /analyze_number
- **Mô tả:** Phân tích số điện thoại
- **Phương thức:** GET
- **Input:**
  - Query parameters:
    - `number` (string, bắt buộc): Số điện thoại cần phân tích
    - `user_data` (string, tùy chọn): Dữ liệu người dùng bổ sung dạng JSON
  - Headers:
    - `api_key` (string, tùy chọn): API key để xác thực nếu không đăng nhập
- **Output:** JSON kết quả phân tích từ BatCucLinhSoAgent
- **Trạng thái:** Đang hoạt động

## Endpoints trò chuyện/chat

### POST /api/chat
- **Mô tả:** Gửi tin nhắn đến hệ thống agent
- **Phương thức:** POST
- **Input:**
  - Body:
    ```json
    {
      "message": "Nội dung tin nhắn",
      "context": {
        "key1": "value1",
        "key2": "value2"
      }
    }
    ```
  - Headers:
    - `api_key` (string, tùy chọn): API key để xác thực nếu không đăng nhập
- **Output:** JSON phản hồi từ agent
- **Ví dụ:**
```json
{
  "agent": "Root Agent",
  "status": "success",
  "content": "Nội dung phản hồi",
  "metadata": {},
  "is_final": true
}
```
- **Trạng thái:** Đang hoạt động

### GET /api/chat
- **Mô tả:** Lấy phản hồi dạng stream từ hệ thống agent
- **Phương thức:** GET
- **Input:**
  - Query parameters:
    - `session_id` (string, bắt buộc): ID phiên trò chuyện
    - `message` (string, tùy chọn): Tin nhắn tùy chọn
    - `user_id` (string, tùy chọn): ID người dùng tùy chọn
- **Output:** Server-Sent Events (SSE) stream
- **Trạng thái:** Đang hoạt động (dữ liệu mock)

## Endpoints tải lên tập tin

### POST /api/upload
- **Mô tả:** Tải lên tập tin (hình ảnh, PDF, âm thanh)
- **Phương thức:** POST
- **Input:**
  - Form data:
    - `file` (file, bắt buộc): Tập tin cần tải lên
    - `type` (string, tùy chọn): Loại tập tin (image, pdf, audio, text)
    - `metadata` (string, tùy chọn): Metadata dạng JSON
- **Output:** JSON thông tin về tập tin đã tải lên
- **Ví dụ:**
```json
{
  "status": "success",
  "file_id": "f1a2b3c",
  "file_url": "/static/uploads/f1a2b3c.jpg",
  "metadata": {
    "file_type": "image",
    "file_size": 123456,
    "upload_date": "2024-11-01T12:00:00.000Z",
    "original_filename": "photo.jpg"
  }
}
```
- **Trạng thái:** Đang hoạt động

## Endpoints quản lý người dùng

### POST /api/user/register
- **Mô tả:** Đăng ký người dùng mới
- **Phương thức:** POST
- **Input:**
  - Body:
    ```json
    {
      "email": "user@example.com",
      "fullname": "Nguyễn Văn A",
      "password": "mật_khẩu"
    }
    ```
- **Output:** JSON thông tin người dùng đã đăng ký
- **Trạng thái:** Hoạt động với dữ liệu mock

### POST /api/user/token
- **Mô tả:** Đăng nhập để lấy token truy cập
- **Phương thức:** POST
- **Input:**
  - Form data:
    - `username` (string, bắt buộc): Email người dùng
    - `password` (string, bắt buộc): Mật khẩu
- **Output:** JSON chứa token truy cập và thông tin người dùng
- **Ví dụ:**
```json
{
  "access_token": "token_string",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "fullname": "Nguyễn Văn A",
    "created_at": "2024-11-01T12:00:00.000Z",
    "updated_at": "2024-11-01T12:00:00.000Z",
    "is_active": true,
    "is_premium": false,
    "quota_remaining": 5
  }
}
```
- **Trạng thái:** Hoạt động với dữ liệu mock

### GET /api/user/me
- **Mô tả:** Lấy thông tin người dùng hiện tại
- **Phương thức:** GET
- **Input:** Không có (sử dụng Bearer token)
- **Output:** JSON thông tin người dùng
- **Trạng thái:** Hoạt động với dữ liệu mock

### PUT /api/user/me
- **Mô tả:** Cập nhật thông tin người dùng
- **Phương thức:** PUT
- **Input:**
  - Body:
    ```json
    {
      "fullname": "Nguyễn Văn A Mới",
      "email": "new_email@example.com",
      "password": "mật_khẩu_mới"
    }
    ```
- **Output:** JSON thông tin người dùng đã cập nhật
- **Trạng thái:** Hoạt động với dữ liệu mock

## Endpoints quản lý API key

### POST /api/apikeys
- **Mô tả:** Tạo API key mới
- **Phương thức:** POST
- **Input:**
  - Body:
    ```json
    {
      "name": "My API Key",
      "expires_at": "2025-11-01T12:00:00.000Z"
    }
    ```
- **Output:** JSON thông tin API key đã tạo
- **Ví dụ:**
```json
{
  "id": "key_id",
  "key": "pts_a1b2c3d4e5f6",
  "name": "My API Key",
  "created_at": "2024-11-01T12:00:00.000Z",
  "expires_at": "2025-11-01T12:00:00.000Z",
  "last_used_at": null,
  "is_active": true
}
```
- **Trạng thái:** Hoạt động với dữ liệu mock

### GET /api/apikeys
- **Mô tả:** Lấy danh sách API key của người dùng hiện tại
- **Phương thức:** GET
- **Input:** Không có (sử dụng Bearer token)
- **Output:** JSON mảng các API key
- **Trạng thái:** Hoạt động với dữ liệu mock

### DELETE /api/apikeys/{api_key_id}
- **Mô tả:** Xóa API key
- **Phương thức:** DELETE
- **Input:**
  - Path parameters:
    - `api_key_id` (string, bắt buộc): ID của API key cần xóa
- **Output:** JSON `{"message": "API key deleted successfully"}`
- **Trạng thái:** Hoạt động với dữ liệu mock

## Endpoints thanh toán và gói dịch vụ

### GET /api/payment/plans
- **Mô tả:** Lấy danh sách các gói dịch vụ
- **Phương thức:** GET
- **Input:** Không có
- **Output:** JSON mảng các gói dịch vụ
- **Trạng thái:** Hoạt động với dữ liệu mock

### GET /api/payment/plans/{plan_id}
- **Mô tả:** Lấy thông tin chi tiết của một gói dịch vụ
- **Phương thức:** GET
- **Input:**
  - Path parameters:
    - `plan_id` (string, bắt buộc): ID của gói dịch vụ
- **Output:** JSON thông tin gói dịch vụ
- **Trạng thái:** Hoạt động với dữ liệu mock

### POST /api/payment
- **Mô tả:** Tạo thanh toán mới
- **Phương thức:** POST
- **Input:**
  - Body:
    ```json
    {
      "plan_id": "premium",
      "payment_method": "momo",
      "amount": 199000,
      "currency": "VND"
    }
    ```
- **Output:** JSON thông tin thanh toán
- **Trạng thái:** Hoạt động với dữ liệu mock (tự động chuyển thành "completed")

### GET /api/payment/history
- **Mô tả:** Lấy lịch sử thanh toán của người dùng hiện tại
- **Phương thức:** GET
- **Input:** Không có (sử dụng Bearer token)
- **Output:** JSON mảng các thanh toán
- **Trạng thái:** Hoạt động với dữ liệu mock

### GET /api/payment/subscription
- **Mô tả:** Lấy thông tin gói đăng ký hiện tại của người dùng
- **Phương thức:** GET
- **Input:** Không có (sử dụng Bearer token)
- **Output:** JSON thông tin gói đăng ký hoặc null nếu không có
- **Trạng thái:** Hoạt động với dữ liệu mock 