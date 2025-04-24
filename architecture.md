# Kiến trúc dự án Phong Thủy Số

## 1. Tổng quan kiến trúc

Dự án Phong Thủy Số được xây dựng theo kiến trúc đa tác tử (Multi-Agent Architecture) dựa trên mô hình tham khảo từ Google Agent Development Kit (ADK). Hệ thống bao gồm các thành phần chính được tổ chức theo mô hình sau:

```
                                              ┌───────────────────────┐
                                              │  phone_number_agent   │
                                              └───────────────────────┘
                                                         ▲
                                                         │
                                              ┌───────────────────────┐
                                              │      cccd_agent       │
                                              └───────────────────────┘
                                                         ▲
                                                         │
                 ┌───────────────────────┐    ┌───────────────────────┐
                 │                       │    │                       │
                 │  batcuclinh_so_agent  │───▶│  bank_account_agent   │
                 │                       │    │                       │
                 └───────────────────────┘    └───────────────────────┘
                             ▲                           ▲
                             │                           │
                             │                ┌───────────────────────┐
                             │                │   password_agent      │
                             │                └───────────────────────┘
                             │                           
                             │                           
                             │                
┌───────────────────────┐    │                
│                       │    │
│      root_agent       │────┼───────────────────────────────────────────┐
│                       │    │                                           │
└───────────────────────┘    │                                           │
                             │                                           ▼
                 ┌───────────────────────┐                    ┌───────────────────────┐
                 │                       │                    │                       │
                 │     payment_agent     │───────────────────▶│   subscription_agent  │
                 │                       │                    │                       │
                 └───────────────────────┘                    └───────────────────────┘
                             ▲                                          
                             │                                          
                             │                               
                             │                               
                             │                                         
                             │                                         
                             │                              
                             │
                 ┌───────────────────────┐                   ┌───────────────────────┐
                 │                       │                   │                       │
                 │      user_agent       │──────────────────▶│     profile_agent     │
                 │                       │                   │                       │
                 └───────────────────────┘                   └───────────────────────┘
                                                                      
                                                                       
                                                            ┌───────────────────────┐
                                                            │   apikey_agent        │
                                                            └───────────────────────┘
                                                                     
```

## 2. Các thành phần chính

### 2.1. Root Agent

Root Agent đóng vai trò là điểm truy cập chính, phân tích yêu cầu của người dùng và điều hướng đến các agent chuyên biệt phù hợp.

**Mục tiêu:** 
- Phân tích yêu cầu của người dùng
- Điều phối yêu cầu đến các sub-agent phù hợp
- Duy trì context và trạng thái hội thoại

**Cấu trúc:**
```
phongthuyso_python/agents/root_agent/
├── agent.py              # Triển khai RootAgent
├── tools/                # Các công cụ của RootAgent
│   ├── agent_router.py   # Công cụ điều hướng yêu cầu
│   ├── intent_classifier.py # Phân loại ý định của người dùng
│   ├── conversation_manager.py # Quản lý hội thoại
│   ├── context_tracker.py # Theo dõi và cập nhật context
├── prompts/              # Các mẫu prompt cho agent
├── __init__.py           # Package initialization
```

### 2.2. Sub-Agents

#### 2.2.1. BatCucLinhSo Agent

Agent chuyên biệt cho việc phân tích số theo phương pháp Bát Cục Linh Số. Agent này có các sub-agent riêng để xử lý các loại phân tích khác nhau.

**Mục tiêu:** 
- Phân tích số điện thoại, CCCD, STK ngân hàng, mật khẩu theo nguyên lý Bát Cục Linh Số
- Đưa ra báo cáo phân tích và đề xuất

**Cấu trúc:**
```
phongthuyso_python/agents/batcuclinh_so_agent/
├── agent.py              # Triển khai BatCucLinhSoAgent chính
├── sub_agents/           # Các sub-agent chuyên biệt
│   ├── phone_number_agent.py  # Phân tích số điện thoại
│   ├── cccd_agent.py     # Phân tích số CCCD
│   ├── bank_account_agent.py # Phân tích STK ngân hàng
│   ├── password_agent.py # Phân tích mật khẩu
├── __init__.py           # Package initialization
```

**Sub-agents của BatCucLinhSo:**

1. **Phone Number Agent**:
   - Chuyên phân tích số điện thoại
   - Xem xét ý nghĩa các cặp số, đặc biệt là 3 số cuối
   - Đánh giá mức độ tương thích với mục đích sử dụng

2. **CCCD Agent**:
   - Chuyên phân tích số Căn cước công dân
   - Tập trung vào 6 số cuối (phần số ngẫu nhiên)
   - Xác định ảnh hưởng đến vận mệnh và các khía cạnh cuộc sống

3. **Bank Account Agent**:
   - Phân tích số tài khoản ngân hàng
   - Đặc biệt tập trung vào 4 số cuối
   - Đánh giá mức độ phù hợp với mục đích tài chính

4. **Password Agent**:
   - Phân tích mật khẩu theo phong thủy số học
   - Cân bằng giữa bảo mật và năng lượng tích cực
   - Đề xuất mật khẩu có năng lượng tốt

#### 2.2.2. Payment Agent

Agent chuyên xử lý các vấn đề liên quan đến thanh toán và gói dịch vụ.

**Mục tiêu:**
- Xử lý các giao dịch thanh toán
- Quản lý gói dịch vụ và quota
- Tích hợp với cổng thanh toán

**Cấu trúc:**
```
phongthuyso_python/agents/payment_agent/
├── agent.py              # Triển khai PaymentAgent
├── sub_agents/           # Các sub-agent chuyên biệt
│   ├── subscription_agent.py # Quản lý đăng ký và gói dịch vụ
├── __init__.py           # Package initialization
```

**Sub-agents của Payment:**

1. **Subscription Agent**:
   - Quản lý các gói dịch vụ và subscription
   - Xử lý việc gia hạn và nâng cấp gói
   - Tính toán quota và hạn mức

#### 2.2.3. User Agent

Agent chuyên xử lý các vấn đề liên quan đến quản lý người dùng.

**Mục tiêu:**
- Quản lý tài khoản người dùng
- Xác thực và phân quyền
- Quản lý API keys

**Cấu trúc:**
```
phongthuyso_python/agents/user_agent/
├── agent.py              # Triển khai UserAgent
├── sub_agents/           # Các sub-agent chuyên biệt
│   ├── profile_agent.py  # Quản lý thông tin cá nhân
│   ├── apikey_agent.py   # Quản lý API keys
├── __init__.py           # Package initialization
```

**Sub-agents của User:**

1. **Profile Agent**:
   - Quản lý thông tin cá nhân của người dùng
   - Xử lý cập nhật profile và các thiết đặt
   - Lưu trữ lịch sử hoạt động

2. **API Key Agent**:
   - Quản lý tạo, xóa, cập nhật API keys
   - Theo dõi việc sử dụng API keys
   - Áp dụng chính sách giới hạn tần suất

### 2.3. Tools

Tools là các thành phần chức năng được sử dụng bởi các agent để thực hiện các tác vụ cụ thể. Các tools được tổ chức tập trung trong một thư mục riêng.

**Cấu trúc:**
```
phongthuyso_python/tools/
├── batcuclinhso_analysis/       # Công cụ phân tích số
│   ├── number_analyzer.py       # Phân tích cặp số
│   ├── energy_calculator.py     # Tính năng lượng
│   ├── recommendation_engine.py # Đưa ra đề xuất
├── payment/                    # Công cụ thanh toán
│   ├── payment_processor.py    # Xử lý thanh toán
│   ├── quota_manager.py        # Quản lý quota
│   ├── billing_calculator.py   # Tính phí
├── user/                       # Công cụ quản lý người dùng
│   ├── auth_service.py         # Dịch vụ xác thực
│   ├── profile_manager.py      # Quản lý hồ sơ
│   ├── apikey_generator.py     # Tạo API keys
├── common/                     # Công cụ dùng chung
│   ├── context_manager.py      # Quản lý context
│   ├── session_manager.py      # Quản lý phiên
│   ├── logger.py               # Ghi log
├── __init__.py                 # Tools initialization
```

## 3. Luồng xử lý

### 3.1. Phân tích số điện thoại

1. FastAPI nhận request phân tích số điện thoại
2. Request được chuyển đến RootAgent
3. RootAgent xác định đây là yêu cầu phân tích số và chuyển đến BatCucLinhSoAgent
4. BatCucLinhSoAgent chuyển yêu cầu đến PhoneNumberAgent
5. PhoneNumberAgent sử dụng các tools từ thư viện batcuclinhso_analysis:
   - number_analyzer.py để phân tích các cặp số
   - energy_calculator.py để tính điểm và năng lượng
   - recommendation_engine.py để tạo đề xuất
6. Kết quả được trả về BatCucLinhSoAgent
7. BatCucLinhSoAgent xử lý và bổ sung giải thích
8. Kết quả được trả về RootAgent và cuối cùng về cho người dùng

### 3.2. Thanh toán

1. Người dùng chọn gói dịch vụ và phương thức thanh toán
2. Request gửi đến RootAgent và được chuyển đến PaymentAgent
3. PaymentAgent chuyển yêu cầu đến SubscriptionAgent nếu cần
4. PaymentAgent sử dụng payment_processor.py để xử lý giao dịch
5. Người dùng được chuyển đến trang thanh toán
6. Sau khi thanh toán thành công, webhook gọi về hệ thống
7. PaymentAgent sử dụng quota_manager.py để cập nhật thông tin người dùng và quota

## 4. Tích hợp Frontend

Frontend test là ứng dụng web đơn giản cho phép kiểm thử các API của hệ thống:
- Cấu hình linh hoạt URL base cho API
- Hiển thị endpoints rõ ràng trên mỗi tab
- Các form dễ dàng nhập liệu và kiểm thử
- Hiển thị kết quả JSON dễ đọc

## 5. Kế hoạch phát triển

Hệ thống sẽ được phát triển theo các giai đoạn:
1. Xây dựng Root Agent và cơ chế điều hướng
2. Triển khai BatCucLinhSo Agent với các sub-agent và công cụ phân tích cơ bản
3. Triển khai User Agent với các sub-agent và hệ thống xác thực
4. Triển khai Payment Agent với các sub-agent và tích hợp thanh toán
5. Tối ưu hóa và mở rộng tính năng 