"""
Types Module for ADK

Module định nghĩa các schema output cho ADK agents.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from google.genai.types import GenerateContentConfig

# Cấu hình cho JSON response
json_response_config = GenerateContentConfig(
    temperature=0.1,
    top_p=0.8,
    response_mime_type="application/json"
)

# Output Schema cho BatCucLinhSo Agent
class PhoneAnalysisResult(BaseModel):
    """Kết quả phân tích số điện thoại"""
    phone_number: str = Field(..., description="Số điện thoại được phân tích")
    star_sequence: List[int] = Field(..., description="Trình tự sao (1-9)")
    energy_level: Dict[str, Any] = Field(..., description="Mức độ năng lượng")
    balance: str = Field(..., description="Mức độ cân bằng")
    star_combinations: List[str] = Field(..., description="Các tổ hợp sao")
    key_combinations: List[str] = Field(..., description="Các tổ hợp quan trọng")
    dangerous_combinations: List[str] = Field(..., description="Các tổ hợp nguy hiểm")
    key_positions: Dict[str, str] = Field(..., description="Vị trí quan trọng")
    recommendations: List[str] = Field(..., description="Các đề xuất cải thiện")
    overall_score: int = Field(..., description="Điểm đánh giá tổng thể (1-10)")
    suitability: Dict[str, int] = Field(..., description="Độ phù hợp cho các mục đích")

class CCCDAnalysisResult(BaseModel):
    """Kết quả phân tích số CCCD"""
    cccd_number: str = Field(..., description="6 số cuối CCCD được phân tích")
    star_sequence: List[int] = Field(..., description="Trình tự sao (1-9)")
    energy_level: str = Field(..., description="Mức độ năng lượng")
    key_combinations: List[str] = Field(..., description="Các tổ hợp quan trọng")
    overall_assessment: str = Field(..., description="Đánh giá tổng thể")
    recommendations: List[str] = Field(..., description="Các đề xuất")

class BankAccountAnalysisResult(BaseModel):
    """Kết quả phân tích số tài khoản ngân hàng"""
    account_number: str = Field(..., description="Số tài khoản được phân tích")
    bank_name: Optional[str] = Field(None, description="Tên ngân hàng")
    star_sequence: List[int] = Field(..., description="Trình tự sao (1-9)")
    energy_level: str = Field(..., description="Mức độ năng lượng")
    key_combinations: List[str] = Field(..., description="Các tổ hợp quan trọng")
    purpose_fit: Dict[str, int] = Field(..., description="Độ phù hợp cho mục đích sử dụng")
    recommendations: List[str] = Field(..., description="Các đề xuất")

class PasswordAnalysisResult(BaseModel):
    """Kết quả phân tích mật khẩu"""
    password: str = Field(..., description="Mật khẩu được phân tích hoặc tạo")
    energy_level: str = Field(..., description="Mức độ năng lượng")
    strength: str = Field(..., description="Độ mạnh của mật khẩu")
    security_score: int = Field(..., description="Điểm bảo mật (1-10)")
    phong_thuy_score: int = Field(..., description="Điểm phong thủy (1-10)")
    recommendations: List[str] = Field(..., description="Các đề xuất cải thiện")

# Output Schema cho Payment Agent
class SubscriptionInfo(BaseModel):
    """Thông tin gói dịch vụ"""
    plan_name: str = Field(..., description="Tên gói dịch vụ")
    price: float = Field(..., description="Giá (VND)")
    features: Dict[str, Any] = Field(..., description="Các tính năng và giới hạn")
    duration: str = Field(..., description="Thời hạn")

class UserQuota(BaseModel):
    """Quota người dùng"""
    user_id: str = Field(..., description="ID người dùng")
    subscription_plan: str = Field(..., description="Gói dịch vụ hiện tại")
    remaining_quotas: Dict[str, int] = Field(..., description="Quota còn lại cho các dịch vụ")
    expiry_date: str = Field(..., description="Ngày hết hạn")

class PaymentResult(BaseModel):
    """Kết quả xử lý thanh toán"""
    transaction_id: str = Field(..., description="ID giao dịch")
    status: str = Field(..., description="Trạng thái giao dịch")
    amount: float = Field(..., description="Số tiền")
    plan: str = Field(..., description="Gói dịch vụ")
    payment_method: str = Field(..., description="Phương thức thanh toán")
    timestamp: str = Field(..., description="Thời gian thực hiện")

# Output Schema cho User Agent
class UserProfile(BaseModel):
    """Thông tin người dùng"""
    user_id: str = Field(..., description="ID người dùng")
    email: str = Field(..., description="Email")
    name: Optional[str] = Field(None, description="Tên hiển thị")
    subscription_plan: str = Field(..., description="Gói dịch vụ hiện tại")
    registration_date: str = Field(..., description="Ngày đăng ký")

class APIKey(BaseModel):
    """Thông tin API key"""
    key_id: str = Field(..., description="ID của key")
    key_prefix: str = Field(..., description="Phần prefix của key")
    created_at: str = Field(..., description="Ngày tạo")
    last_used: Optional[str] = Field(None, description="Lần sử dụng cuối")
    permissions: List[str] = Field(..., description="Các quyền của key")

class LoginResult(BaseModel):
    """Kết quả đăng nhập"""
    status: str = Field(..., description="Trạng thái đăng nhập")
    user_id: Optional[str] = Field(None, description="ID người dùng")
    session_token: Optional[str] = Field(None, description="Token phiên")
    expiry: Optional[str] = Field(None, description="Thời gian hết hạn")

# Schema cho Travel Planner
class RoomsSelection(BaseModel):
    """Room selection for a hotel"""
    selected_room: str
    price: float
    check_in_date: str
    check_out_date: str
    persons: int
    room_amenities: List[str]

class HotelsSelection(BaseModel):
    """Hotels selection results"""
    selected_hotel: str
    location: str
    price_range: str
    rating: float 
    available_room_types: List[str]
    amenities: List[str]

class SeatsSelection(BaseModel):
    """Seat selection for a flight"""
    selected_seat: str
    seat_type: str
    price: float
    location: str

class FlightsSelection(BaseModel):
    """Flight selection results"""
    selected_flight: str
    departure: str
    arrival: str
    departure_time: str
    arrival_time: str
    price: float
    airline: str
    
class ItineraryDay(BaseModel):
    """A day in the itinerary"""
    date: str
    activities: List[Dict[str, Any]]
    accommodation: Optional[Dict[str, Any]] = None
    transportation: Optional[Dict[str, Any]] = None
    
class Itinerary(BaseModel):
    """Complete travel itinerary"""
    destination: str
    start_date: str
    end_date: str
    traveler_count: int
    days: List[ItineraryDay]
    total_budget: float 