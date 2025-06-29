"""
Pydantic Models Module

Module chứa các Pydantic models dùng cho xác thực dữ liệu và typing.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ServiceType(str, Enum):
    """Các loại dịch vụ hệ thống hỗ trợ"""
    PHONE_ANALYSIS = "phone_analysis"
    CCCD_ANALYSIS = "cccd_analysis"
    BANK_ACCOUNT_ANALYSIS = "bank_account_analysis"
    PASSWORD_GENERATION = "password_generation"


class UserRole(str, Enum):
    """Các vai trò người dùng trong hệ thống"""
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class SubscriptionPlan(str, Enum):
    """Các gói dịch vụ"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    VIP = "vip"


class BatCucLinhSoRequest(BaseModel):
    """Model cơ sở cho các yêu cầu phân tích Bát Cục Linh Số"""
    request_type: ServiceType
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class BatCuLinhSoResponse(BaseModel):
    """Model cơ sở cho các phản hồi phân tích Bát Cục Linh Số"""
    status: str = "success"
    message: str
    analysis: Dict[str, Any]
    recommendations: List[str]
    metadata: Optional[Dict[str, Any]] = None


class PhoneAnalysisRequest(BatCucLinhSoRequest):
    """Model cho yêu cầu phân tích số điện thoại"""
    phone_number: str = Field(..., description="Số điện thoại cần phân tích")
    request_type: ServiceType = ServiceType.PHONE_ANALYSIS
    
    @validator("phone_number")
    def validate_phone_number(cls, v):
        """Xác thực định dạng số điện thoại"""
        if not v.isdigit():
            raise ValueError("Số điện thoại chỉ được chứa chữ số")
        if len(v) not in [10, 11]:
            raise ValueError("Số điện thoại phải có 10 hoặc 11 chữ số")
        return v


class CCCDAnalysisRequest(BatCucLinhSoRequest):
    """Model cho yêu cầu phân tích CCCD"""
    cccd_last_digits: str = Field(..., description="6 chữ số cuối của CCCD cần phân tích")
    request_type: ServiceType = ServiceType.CCCD_ANALYSIS
    
    @validator("cccd_last_digits")
    def validate_cccd_last_digits(cls, v):
        """Xác thực định dạng 6 số cuối CCCD"""
        if not v.isdigit():
            raise ValueError("Dãy số chỉ được chứa chữ số")
        if len(v) != 6:
            raise ValueError("Phải nhập đúng 6 chữ số cuối của CCCD")
        return v


class BankAccountRequest(BatCucLinhSoRequest):
    """Model cho yêu cầu phân tích hoặc đề xuất số tài khoản ngân hàng"""
    purpose: str = Field(..., description="Mục đích sử dụng tài khoản")
    bank_name: Optional[str] = Field(None, description="Tên ngân hàng (không bắt buộc)")
    preferred_digits: Optional[List[str]] = Field(None, description="Các chữ số ưa thích (không bắt buộc)")
    request_type: ServiceType = ServiceType.BANK_ACCOUNT_ANALYSIS


class PasswordRequest(BatCucLinhSoRequest):
    """Model cho yêu cầu tạo hoặc phân tích mật khẩu theo phong thủy"""
    purpose: str = Field(..., description="Mục đích sử dụng mật khẩu")
    keywords: Optional[List[str]] = Field(None, description="Các từ khóa liên quan (không bắt buộc)")
    min_length: Optional[int] = Field(8, description="Độ dài tối thiểu của mật khẩu")
    require_special_chars: Optional[bool] = Field(True, description="Yêu cầu ký tự đặc biệt")
    require_numbers: Optional[bool] = Field(True, description="Yêu cầu chữ số")
    request_type: ServiceType = ServiceType.PASSWORD_GENERATION


class UserProfile(BaseModel):
    """Model thông tin người dùng"""
    user_id: str
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    subscription_plan: SubscriptionPlan = SubscriptionPlan.FREE
    remaining_quotas: Dict[ServiceType, int] = Field(default_factory=dict)
    created_at: str
    last_login: Optional[str] = None


class ServiceUsageHistory(BaseModel):
    """Model lịch sử sử dụng dịch vụ"""
    usage_id: str
    user_id: str
    service_type: ServiceType
    timestamp: str
    input_data: Dict[str, Any]
    result_summary: str


class PaymentTransaction(BaseModel):
    """Model giao dịch thanh toán"""
    transaction_id: str
    user_id: str
    amount: float
    subscription_plan: SubscriptionPlan
    payment_method: str
    status: str
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


class SessionData(BaseModel):
    """Model dữ liệu phiên làm việc"""
    session_id: str
    user_id: Optional[str] = None
    is_authenticated: bool = False
    current_context: Dict[str, Any] = Field(default_factory=dict)
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    last_activity: str


class PaymentRequest(BaseModel):
    """Model cho yêu cầu thanh toán"""
    plan_id: str
    payment_method: str
    amount: float
    currency: str = "VND"
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class SubscriptionRequest(BaseModel):
    """Model cho yêu cầu đăng ký gói dịch vụ"""
    plan_id: str
    user_id: Optional[str] = None
    auto_renew: bool = True
    metadata: Optional[Dict[str, Any]] = None


class UserManagementRequest(BaseModel):
    """Model cho yêu cầu quản lý người dùng"""
    action: str  # login, register, update, delete
    email: Optional[str] = None
    password: Optional[str] = None
    fullname: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class PhoneAnalysisResult(BaseModel):
    """Model chi tiết kết quả phân tích số điện thoại"""
    starSequence: List[Any] = []
    energyLevel: Dict[str, Any] = {}
    balance: Optional[str] = None
    starCombinations: List[Any] = []
    keyCombinations: List[Any] = []
    dangerousCombinations: List[Any] = []
    keyPositions: Dict[str, Any] = {}
    last3DigitsAnalysis: Dict[str, Any] = {}
    specialAttribute: Optional[str] = None


class PhoneAnalysis(BaseModel):
    """Model lưu trữ kết quả phân tích số điện thoại"""
    userId: str
    phoneNumber: str
    result: PhoneAnalysisResult
    geminiResponse: Optional[str] = None
    createdAt: datetime = Field(default_factory=datetime.now)
    
    class Config:
        schema_extra = {
            "example": {
                "userId": "dd060dde-80a4-4a08-b114-fe600f3967bb",
                "phoneNumber": "0987654321",
                "result": {
                    "starSequence": [9, 8, 7, 6, 5, 4, 3, 2, 1],
                    "energyLevel": {"overall": "cao", "chi_tiết": {}},
                    "balance": "rất cân bằng",
                    "starCombinations": ["9-8: Cát tinh"],
                    "keyCombinations": ["4-3-2: Thành công"],
                    "dangerousCombinations": [],
                    "keyPositions": {"đầu": "tốt", "giữa": "tốt", "cuối": "tốt"},
                    "last3DigitsAnalysis": {"ý nghĩa": "may mắn"},
                    "specialAttribute": "Số quý nhân phù trợ"
                },
                "geminiResponse": "Đây là số điện thoại có năng lượng cao...",
                "createdAt": "2025-04-29T13:00:00.000Z"
            }
        }


class ChatMessage(BaseModel):
    """Model tin nhắn trong cuộc trò chuyện"""
    content: str
    role: str = "user"  # user, assistant, system
    timestamp: Optional[datetime] = None
    message_id: Optional[str] = None
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        return v or datetime.utcnow()


class ChatContext(BaseModel):
    """Model context của cuộc trò chuyện"""
    conversation_id: Optional[str] = None
    messages: List[ChatMessage] = []
    user_id: Optional[str] = None
    conversation_state: Optional[Dict[str, Any]] = {}
    user_preferences: Optional[Dict[str, Any]] = {}
    last_analysis: Optional[Dict[str, Any]] = None
    
    def dict(self):
        return {
            "conversation_id": self.conversation_id,
            "messages": [msg.dict() for msg in self.messages],
            "user_id": self.user_id,
            "conversation_state": self.conversation_state,
            "user_preferences": self.user_preferences,
            "last_analysis": self.last_analysis
        }


class AnalysisResult(BaseModel):
    """Model kết quả phân tích"""
    analysis_type: str  # phone, cccd, bank_account, password
    result: Dict[str, Any]
    score: Optional[float] = None
    recommendations: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Định nghĩa index khi được sử dụng trong MongoDB
# db.phoneAnalysis.createIndex({ userId: 1, phoneNumber: 1 })
# db.phoneAnalysis.createIndex({ createdAt: -1 }) 