"""
Pydantic Models Module

Module chứa các Pydantic models dùng cho xác thực dữ liệu và typing.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator


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