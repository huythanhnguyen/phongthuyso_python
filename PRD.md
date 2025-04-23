# PRD: Kiến trúc đa tác tử (Multi-Agent) cho Phong Thủy Số Python

## Tổng quan

Tài liệu này mô tả chi tiết thiết kế và triển khai kiến trúc đa tác tử (multi-agent) cho ứng dụng Phong Thủy Số, sử dụng Google Agent Development Kit (ADK) để tăng cường khả năng phân tích và tương tác của hệ thống.

## Mục tiêu

1. **Nâng cao trải nghiệm người dùng**:
   - Tạo hệ thống trò chuyện thông minh và trực quan
   - Hỗ trợ nhiều loại input (văn bản, hình ảnh, giọng nói)
   - Cung cấp phân tích sâu và toàn diện về số học phong thủy

2. **Cải thiện kiến trúc hệ thống**:
   - Xây dựng backend thuần túy bằng Python
   - Kiến trúc microservices dựa trên agents
   - Tăng khả năng mở rộng và linh hoạt của hệ thống
   - Cải thiện hiệu suất và độ tin cậy

3. **Mở rộng chức năng**:
   - Hỗ trợ phân tích nhiều loại số (điện thoại, CCCD, STK ngân hàng, mật khẩu)
   - Tích hợp thanh toán và quản lý người dùng
   - Hỗ trợ việc tạo API keys để tích hợp với các website khác

## Kiến trúc

### Tổng quan kiến trúc

Hệ thống sẽ sử dụng kiến trúc hoàn toàn dựa trên Python với Google ADK:

```
┌─────────────┐     ┌───────────────┐     ┌───────────────┐
│   Frontend  │────▶│  FastAPI API  │────▶│  ADK Agents   │
│   (Vue.js)  │◀────│   (Python)    │◀────│   (Python)    │
└─────────────┘     └───────────────┘     └───────────────┘
                           │                     │
                           ▼                     ▼
                    ┌──────────────┐     ┌───────────────┐
                    │   Database   │     │ Model Context │
                    │  (MongoDB)   │     │   Protocol    │
                    └──────────────┘     └───────────────┘
```

### Hệ thống Agents

Hệ thống sẽ triển khai một kiến trúc đa tác tử gồm:

1. **Root Agent**
   - **Mục đích**: Đóng vai trò như một điều phối viên chính, phân tích ý định của người dùng và chuyển hướng đến các agent chuyên biệt
   - **Khả năng**: Hiểu ngôn ngữ tự nhiên, quản lý luồng hội thoại, duy trì context
   - **Tương tác**: Giao tiếp trực tiếp với người dùng và các agent khác

2. **BatCucLinhSo Agent**
   - **Mục đích**: Chuyên phân tích số điện thoại, CCCD, STK ngân hàng theo phương pháp Bát Cục Linh Số
   - **Khả năng**: Phân tích chi tiết, đưa ra lời khuyên, giải thích ý nghĩa
   - **Nguyên lý phân tích Bát Cục Linh Số**:

     Bát Cục Linh Số là phương pháp phân tích năng lượng của các con số dựa trên 8 loại sao chính - 4 cát tinh và 4 hung tinh:

     **4 Cát Tinh (Sao Tốt):**
     1. **Sinh Khí**: 
        - Cặp số: 14, 41, 67, 76, 39, 93, 28, 82
        - Đặc tính: Vui vẻ, quý nhân, dẫn đạo lực
        - Lĩnh vực phù hợp: Phát triển, tăng trưởng, quý nhân giúp đỡ
        - Mức năng lượng: 1-4 (tùy cặp số)

     2. **Thiên Y**: 
        - Cặp số: 13, 31, 68, 86, 49, 94, 27, 72
        - Đặc tính: Tiền tài, tình cảm, hồi báo
        - Lĩnh vực phù hợp: Tài chính, tình cảm, sức khỏe
        - Mức năng lượng: 1-4 (tùy cặp số)

     3. **Diên Niên**: 
        - Cặp số: 19, 91, 78, 87, 34, 43, 26, 62
        - Đặc tính: Năng lực chuyên nghiệp, công việc
        - Lĩnh vực phù hợp: Sự nghiệp, lãnh đạo, phát triển chuyên môn
        - Mức năng lượng: 1-4 (tùy cặp số)

     4. **Phục Vị**: 
        - Cặp số: 11, 22, 33, 44, 66, 77, 88, 99
        - Đặc tính: Chịu đựng, khó thay đổi
        - Đặc điểm: Theo hung thì hung, theo cát thì cát (có thể tốt hoặc xấu tùy tổ hợp)
        - Mức năng lượng: 1-4 (tùy cặp số)

     **4 Hung Tinh (Sao Xấu):**
     1. **Họa Hại**: 
        - Cặp số: 17, 71, 89, 98, 46, 64, 23, 32
        - Đặc tính: Khẩu tài, chi tiêu lớn, thị phi
        - Cảnh báo: Cãi vã, kiện tụng, phá tài, bệnh tật
        - Mức năng lượng: 1-4 (tùy cặp số)

     2. **Lục Sát**: 
        - Cặp số: 16, 61, 47, 74, 38, 83, 92, 29
        - Đặc tính: Giao tế, phục vụ, cửa hàng, nữ nhân
        - Cảnh báo: Tình cảm không ổn định, u buồn, trầm cảm
        - Mức năng lượng: 1-4 (tùy cặp số)

     3. **Ngũ Quỷ**: 
        - Cặp số: 18, 81, 79, 97, 36, 63, 24, 42
        - Đặc tính: Trí óc, biến động, không ổn định, tư duy
        - Cảnh báo: Thay đổi liên tục, tiểu nhân, khó quản lý tài chính
        - Mức năng lượng: 1-4 (tùy cặp số)

     4. **Tuyệt Mệnh**: 
        - Cặp số: 12, 21, 69, 96, 84, 48, 73, 37
        - Đặc tính: Dốc sức, đầu tư, hành động, phá tài
        - Cảnh báo: Dễ phá tài, gặp tai nạn, sức khỏe không tốt
        - Mức năng lượng: 1-4 (tùy cặp số)

     **Quy tắc phân tích chính:**

     1.0 **Chuẩn hóa và Lựa chọn các số ngẫu nhiên**: loại bỏ các khoảng trắng hoặc kí tự đặc biệt, loại bỏ các số format như số 0 ở đâu của số điện thoại (hoặc số nhà mạng nếu có yêu cầu), loại bỏ các số vùng miền giới tính trong căn cước công dân...
     1.1 **Tách thành cặp số**: Số điện thoại/CCCD/STK được tách thành các cặp số liền kề
        - Ví dụ: 0123456789 →  12, 23, 34, 45, 56, 67, 78, 89

     2. **Xác định thuộc tính sao**: Mỗi cặp số tương ứng với một sao (cát hoặc hung)

     3. **Đánh giá mức năng lượng**: Mỗi cặp số có mức năng lượng từ 1-4 (1: yếu, 4: mạnh)

     4. **Phân tích tổ hợp sao**: 
        - Tra cứu trong constants/bat_tinh.py
        - Tra tổ hợp trong constants/combinations.py

     5. **Xử lý số 0 và 5**: 
        - Số 0: Thường làm biến chất sao (hóa hung) - tra trong bat_tinh.py
        - Số 5: Tăng cường năng lượng của sao (cộng thêm 1 nếu có 1 số)

     6. **Đánh giá**:
        - Đánh giá dựa vào từng case cụ thể theo tool
 

     **Ứng dụng theo loại phân tích:**

     1. **Phân tích Số Điện Thoại**:
        1.1. Loại bỏ các khoảng trắng hoặc kí tự đặc biệt, loại bỏ các số format như số 0 ở đầu của số điện thoại
        - Tách thành các cặp sao (bộ 2 số hoặc các bộ số dài hơn nếu có số 0,5)
        - Phân tích các vị trí trọng yếu: 3 số cuối hoặc sao cuối (nếu sao cuối có bao gồm số 0,5)
        - Các vị trí quan trọng 1,3,5 từ bên phải, đọc ý nghĩa theo meaning 
        - Phân tích các biến hóa dựa vào các cặp sao liền kề nhau (ý nghĩa tại combinations.py)
        1.2 Đưa vào LLM để tổng hợp và phân tích


     2. **Phân tích CCCD**:
        - Tập trung vào 6 số cuối (phần số ngẫu nhiên)
        - Xác định ảnh hưởng đến vận mệnh và các khía cạnh cuộc sống
        - Đưa ra lời khuyên về việc nên/không nên làm với CCCD này

     3. **Phân tích STK Ngân Hàng**:
        - Đặc biệt chú trọng đến 4 số cuối
        - Đánh giá mức độ phù hợp với mục đích tài chính
        - Phân tích theo các mục đích: kinh doanh, tiết kiệm, đầu tư, cá nhân

     4. **Phân tích Mật Khẩu**:
        - Phân tích các cặp số trong mật khẩu
        - Đánh giá tác động của các con số đến bảo mật và năng lượng
        - Đề xuất điều chỉnh để cải thiện cả bảo mật và phong thủy

     **Công cụ (Tools):**
     - `PhoneAnalyzer`: Phân tích số điện thoại theo nguyên lý Bát Cục Linh Số
     - `CCCDAnalyzer`: Phân tích số CCCD theo quy tắc phong thủy
     - `BankAccountAnalyzer`: Phân tích STK ngân hàng
     - `PasswordAnalyzer`: Đánh giá mật khẩu
     - `RecommendationEngine`: Đưa ra lời khuyên dựa trên kết quả phân tích

3. **Payment Agent**
   - **Mục đích**: Xử lý các giao dịch thanh toán
   - **Khả năng**: Thanh toán, nâng cấp tài khoản, kiểm tra quota
   - **Tools**: Xử lý thanh toán, quản lý subscription, kiểm tra hạn mức

4. **User Agent**
   - **Mục đích**: Quản lý thông tin người dùng
   - **Khả năng**: Đăng ký, đăng nhập, cập nhật profile, quản lý API keys
   - **Tools**: Quản lý tài khoản, tạo API key, xem lịch sử

### Giao tiếp giữa các Agents

Hệ thống sẽ sử dụng Agent-to-Agent (A2A) Protocol của Google ADK để cho phép các agent giao tiếp với nhau:

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  Root Agent │────▶│ BatCucLinhSo │────▶│     Tasks     │
│             │◀────│     Agent    │◀────│               │
└─────────────┘     └──────────────┘     └───────────────┘
       │                   │                     │
       │                   │                     │
       ▼                   ▼                     ▼
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│   Messages  │────▶│   Artifacts  │────▶│   Resources   │
│             │◀────│              │◀────│               │
└─────────────┘     └──────────────┘     └───────────────┘
```

Các thành phần chính:

1. **Tasks**: Đại diện cho các nhiệm vụ cần hoàn thành
2. **Messages**: Giao tiếp giữa các agent
3. **Artifacts**: Dữ liệu chia sẻ giữa các agent
4. **Resources**: Tài nguyên được quản lý bởi Model Context Protocol (MCP)

### Model Context Protocol (MCP)

MCP sẽ được triển khai để quản lý tập trung các prompt, cấu hình mô hình và resources:

```
┌─────────────────────────────────────────────────────────┐
│                   MCP Server                            │
├─────────────┬──────────────┬───────────────────────────┤
│  Templates  │  Parameters  │         Resources         │
├─────────────┼──────────────┼───────────────────────────┤
│ Root Agent  │ Root Agent   │ - Base Prompts           │
│ Prompts     │ Config       │ - System Instructions     │
├─────────────┼──────────────┼───────────────────────────┤
│ BatCucLinhSo│ BatCucLinhSo │ - Phone Analysis Rules   │
│ Prompts     │ Config       │ - CCCD Analysis Data     │
├─────────────┼──────────────┼───────────────────────────┤
│ Payment     │ Payment      │ - Payment Instructions   │
│ Prompts     │ Config       │ - Plan Details           │
├─────────────┼──────────────┼───────────────────────────┤
│ User Agent  │ User Agent   │ - Account Management     │
│ Prompts     │ Config       │ - API Key Instructions   │
└─────────────┴──────────────┴───────────────────────────┘
```

## Chức năng chi tiết

### 1. Root Agent

**Chức năng chính**:
- Xử lý input từ người dùng (văn bản, giọng nói, hình ảnh)
- Phân tích ý định của người dùng
- Điều phối luồng hội thoại và chuyển đến agent thích hợp
- Quản lý context của cuộc trò chuyện
- Tổng hợp phản hồi từ các agent khác

**Tools**:
- `IntentClassifier`: Phân loại ý định người dùng
- `ConversationManager`: Quản lý luồng trò chuyện
- `ContextTracker`: Theo dõi và duy trì context
- `AgentRouter`: Chuyển hướng đến agent phù hợp

### 2. BatCucLinhSo Agent

**Chức năng chính**:
- Phân tích số điện thoại theo phương pháp Bát Cục Linh Số
- Phân tích số CCCD theo quy tắc phong thủy
- Đánh giá STK ngân hàng
- Phân tích và đề xuất cải thiện mật khẩu
- Giải thích ý nghĩa và đưa ra lời khuyên

**Công cụ (Tools):**
- `PhoneAnalyzer`: Phân tích số điện thoại theo nguyên lý Bát Cục Linh Số
- `CCCDAnalyzer`: Phân tích số CCCD theo quy tắc phong thủy
- `BankAccountAnalyzer`: Phân tích STK ngân hàng
- `PasswordAnalyzer`: Đánh giá mật khẩu
- `RecommendationEngine`: Đưa ra lời khuyên dựa trên kết quả phân tích

### 3. Payment Agent

**Chức năng chính**:
- Xử lý các giao dịch thanh toán
- Quản lý subscription và plan
- Kiểm tra và cập nhật quota
- Thông báo về tình trạng thanh toán

**Tools**:
- `PaymentProcessor`: Xử lý thanh toán
- `SubscriptionManager`: Quản lý gói dịch vụ
- `QuotaChecker`: Kiểm tra hạn mức
- `NotificationSender`: Gửi thông báo

### 4. User Agent

**Chức năng chính**:
- Quản lý thông tin tài khoản người dùng
- Xử lý đăng ký và đăng nhập
- Quản lý API keys
- Theo dõi lịch sử người dùng

**Tools**:
- `AccountManager`: Quản lý tài khoản
- `ApiKeyGenerator`: Tạo và quản lý API keys
- `HistoryTracker`: Theo dõi lịch sử
- `PreferenceManager`: Quản lý tùy chọn

## API Endpoints

```
/api/chat
  POST: Gửi tin nhắn tới hệ thống agents
  GET: Nhận phản hồi từ agents (Streaming)

/api/upload
  POST: Upload file (hình ảnh, PDF, âm thanh)

/api/user
  GET: Lấy thông tin người dùng
  POST: Tạo tài khoản mới
  PUT: Cập nhật thông tin

/api/payment
  GET: Kiểm tra trạng thái thanh toán
  POST: Khởi tạo thanh toán

/api/apikeys
  GET: Lấy danh sách API keys
  POST: Tạo API key mới
  DELETE: Xóa API key

/api/analysis
  GET: Lấy lịch sử phân tích
  POST: Yêu cầu phân tích mới
```

## Session Management

Hệ thống sẽ triển khai hai loại session service:

1. **InMemorySessionService**: Sử dụng cho môi trường phát triển
   - Lưu trữ session in-memory
   - Không lưu trữ lâu dài

2. **MongoDBSessionService**: Sử dụng cho môi trường production
   - Lưu trữ session trong MongoDB
   - Hỗ trợ persistence và scale-out

**Cấu trúc Session**:
```json
{
  "sessionId": "string",
  "userId": "string",
  "createdAt": "timestamp",
  "updatedAt": "timestamp",
  "expiresAt": "timestamp",
  "context": {
    "conversationHistory": [...],
    "userPreferences": {...},
    "lastAnalysis": {...}
  },
  "state": {
    "currentAgent": "string",
    "currentTask": "string",
    "pendingActions": [...]
  }
}
```

## Câu trả lời mẫu

Hệ thống sẽ có khả năng cung cấp các loại phân tích sau:

### Phân tích số điện thoại

```
Số điện thoại: 0912.345.678

Phân tích:
- Năm sinh (Lộ): 9 (1+2+3+4+5=15, 1+5=6)
- Phân tích theo Bát Cục Linh Số:
  * Cặp số 91: Mệnh có Phúc, vận khí tốt
  * Cặp số 23: Hoạnh tài, may mắn về tiền bạc
  * Cặp số 45: Hỗ trợ công việc, sự nghiệp phát triển
  * Cặp số 67: Tình cảm thuận lợi, hạnh phúc gia đình
  * Cặp số 78: Sức khỏe tốt, tránh được bệnh tật

Đánh giá: ★★★★☆ (4/5)
- Ưu điểm: Số điện thoại có năng lượng tích cực, hỗ trợ cho sự nghiệp và tài lộc.
- Hạn chế: Thiếu yếu tố hỗ trợ học vấn và phát triển bản thân.

Lời khuyên: Số điện thoại này phù hợp với người làm kinh doanh, tài chính.
```

### Phân tích CCCD

```
Số CCCD: 001202012345

Phân tích:
- Mã tỉnh/thành: 001 (Hà Nội)
- Mã giới tính và năm sinh: 2 (Nữ, sinh 2002)
- Số ngẫu nhiên: 012345

Phân tích theo Bát Cục Linh Số:
- Tổng: 1+2+0+2+0+1+2+3+4+5=20 => 2+0=2 (Số 2 - Thổ)
- Cặp số 00: Thể hiện sự chăm chỉ, kiên nhẫn
- Cặp số 12: Thông minh, sáng tạo
- Cặp số 02: Khả năng hòa đồng tốt
- Cặp số 01: Người tiên phong, dám nghĩ dám làm

Đánh giá: ★★★★★ (5/5)
- Ưu điểm: Số CCCD này mang đến may mắn về học vấn và sự nghiệp.
- Tương thích nghề nghiệp: Giáo dục, nghiên cứu, tư vấn.

Lời khuyên: Số CCCD này rất tốt, không cần thay đổi.
```

### Phân tích STK ngân hàng

```
Số tài khoản: 1903 2468 1357

Phân tích:
- Tổng: 1+9+0+3+2+4+6+8+1+3+5+7=49 => 4+9=13 => 1+3=4 (Số 4 - Hỏa)
- Cặp số 19: Vượng Tài, thuận lợi về tiền bạc
- Cặp số 03: Phát triển bền vững
- Cặp số 24: Ổn định và tăng trưởng
- Cặp số 68: Phát tài, phát lộc
- Cặp số 13: Khởi đầu mới mẻ
- Cặp số 57: Biến đổi tích cực

Đánh giá: ★★★★★ (5/5)
- Ưu điểm: Số tài khoản có tính chất thu hút tài lộc rất mạnh.
- Đặc điểm: Thích hợp cho tài khoản tiết kiệm và đầu tư.

Lời khuyên: Nên sử dụng số tài khoản này cho mục đích tiết kiệm và đầu tư dài hạn.
```

## Yêu cầu kỹ thuật

### Backend Python (ADK)

- **Google ADK**: Agent Development Kit
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Motor**: Async MongoDB driver
- **aiohttp**: Async HTTP client
- **Langchain**: LLM utilities
- **Pillow**: Xử lý hình ảnh
- **PyTorch**: Machine learning

### DevOps

- **Docker**: Containerization
- **Docker Compose**: Development environment
- **GitHub Actions**: CI/CD
- **Prometheus/Grafana**: Monitoring
- **ELK Stack**: Logging
- **Google Cloud Run**: Serverless deployment

## Triển khai

### Giai đoạn 1: Setup môi trường (Tuần 1-2)

- Cài đặt Google ADK
- Tạo các service cơ bản
- Triển khai MCP server
- Thiết lập CI/CD pipeline

### Giai đoạn 2: Phát triển Root Agent (Tuần 3-4)

- Triển khai Root Agent
- Xây dựng FastAPI endpoints
- Xây dựng cơ chế routing
- Thiết lập conversation management

### Giai đoạn 3: Phát triển BatCucLinhSo Agent (Tuần 5-7)

- Triển khai BatCucLinhSo Agent
- Phát triển các tools phân tích
- Tích hợp với Root Agent
- Triển khai testing và evaluation

### Giai đoạn 4: Phát triển User và Payment Agents (Tuần 8-10)

- Triển khai User Agent
- Triển khai Payment Agent
- Tích hợp với Root Agent
- Kiểm thử end-to-end

### Giai đoạn 5: Testing và Optimization (Tuần 11-12)

- End-to-end testing
- Performance optimization
- Security testing
- Beta deployment

## Đánh giá và KPIs

### User Experience KPIs

- **Satisfaction Score**: > 4.5/5.0
- **Response Time**: < 2 giây cho 95% truy vấn
- **Conversation Success Rate**: > 90%
- **Error Rate**: < 5%

### Technical KPIs

- **Agent Accuracy**: > 95% cho phân tích số
- **API Response Time**: < 500ms
- **System Uptime**: > 99.9%
- **Resource Utilization**: < 70% CPU/Memory

### Business KPIs

- **Conversion Rate**: > 5% miễn phí -> trả phí
- **User Retention**: > 70% sau 30 ngày
- **Average Revenue Per User**: Tăng 20%
- **API Usage**: > 100K calls/tháng

## Rủi ro và biện pháp giảm thiểu

| Rủi ro | Mức độ | Tác động | Biện pháp giảm thiểu |
|--------|--------|----------|----------------------|
| Độ chính xác của Agent | Cao | Cao | Extensive testing, Human-in-the-loop evaluation |
| Tốc độ phản hồi | Trung bình | Cao | Caching, Async processing, Response streaming |
| Bảo mật dữ liệu | Cao | Cao | Encryption, Access control, Audit trails |
| Chi phí vận hành | Trung bình | Trung bình | Resource optimization, Caching, Rate limiting |

## Kết luận

Kiến trúc đa tác tử (multi-agent) sử dụng Google ADK sẽ nâng cao đáng kể khả năng của ứng dụng Phong Thủy Số, mang lại trải nghiệm người dùng tốt hơn, và tạo nền tảng cho việc mở rộng chức năng trong tương lai. Việc tích hợp A2A Protocol và MCP cung cấp một kiến trúc linh hoạt và dễ bảo trì, đồng thời FastAPI đảm bảo backend hiệu năng cao và dễ dàng mở rộng. 