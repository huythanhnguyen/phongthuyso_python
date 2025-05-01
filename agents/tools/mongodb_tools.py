"""
MongoDB Tools

Công cụ tương tác với MongoDB trong Google ADK.
"""

from typing import Dict, Any, List, Optional
from google.adk.tools import FunctionTool

# Giả lập dữ liệu để phát triển
mock_users = {
    "user@example.com": {
        "_id": "user123",
        "email": "user@example.com", 
        "name": "Nguyễn Văn A",
        "phone": "0123456789",
        "created_at": "2024-01-01T00:00:00Z"
    }
}

mock_phone_analyses = {
    "0123456789": {
        "_id": "analysis123",
        "userId": "user123",
        "phoneNumber": "0123456789",
        "result": {"score": 85, "luck_level": "good"},
        "createdAt": "2024-01-01T00:00:00Z"
    }
}

mock_subscriptions = {
    "user123": {
        "_id": "sub123",
        "userId": "user123",
        "planId": "premium",
        "expiresAt": "2025-01-01T00:00:00Z",
        "createdAt": "2024-01-01T00:00:00Z"
    }
}

async def find_user(email: str) -> Dict[str, Any]:
    """
    Tìm kiếm người dùng theo email.
    
    Args:
        email (str): Email của người dùng
        
    Returns:
        Dict[str, Any]: Thông tin người dùng
    """
    if email in mock_users:
        return {
            "status": "success",
            "message": "Đã tìm thấy người dùng",
            "user": mock_users[email]
        }
    else:
        return {
            "status": "error",
            "message": "Không tìm thấy người dùng",
            "user": None
        }

async def find_phone_analysis(phone_number: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Tìm kiếm phân tích số điện thoại.
    
    Args:
        phone_number (str): Số điện thoại cần tìm
        user_id (Optional[str]): ID của người dùng (nếu có)
        
    Returns:
        Dict[str, Any]: Kết quả phân tích
    """
    if phone_number in mock_phone_analyses:
        analysis = mock_phone_analyses[phone_number]
        
        # Kiểm tra user_id nếu được cung cấp
        if user_id and analysis["userId"] != user_id:
            return {
                "status": "error",
                "message": "Không tìm thấy phân tích số điện thoại cho người dùng này",
                "analysis": None
            }
            
        return {
            "status": "success",
            "message": "Đã tìm thấy phân tích số điện thoại",
            "analysis": analysis
        }
    else:
        return {
            "status": "error",
            "message": "Không tìm thấy phân tích số điện thoại",
            "analysis": None
        }

async def save_phone_analysis(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Lưu kết quả phân tích số điện thoại.
    
    Args:
        analysis_data (Dict[str, Any]): Dữ liệu phân tích
        
    Returns:
        Dict[str, Any]: Kết quả lưu
    """
    phone_number = analysis_data.get("phoneNumber")
    user_id = analysis_data.get("userId")
    
    if not phone_number or not user_id:
        return {
            "status": "error",
            "message": "Thiếu thông tin số điện thoại hoặc ID người dùng",
            "id": None
        }
    
    # Kiểm tra xem đã có phân tích tương tự chưa
    if phone_number in mock_phone_analyses:
        # Cập nhật phân tích hiện có
        mock_phone_analyses[phone_number].update(analysis_data)
        
        return {
            "status": "success",
            "message": "Đã cập nhật phân tích số điện thoại",
            "updated": True,
            "id": mock_phone_analyses[phone_number]["_id"]
        }
    else:
        # Tạo phân tích mới
        import uuid
        import datetime
        
        analysis_id = str(uuid.uuid4())
        analysis_data["_id"] = analysis_id
        analysis_data["createdAt"] = datetime.datetime.now().isoformat()
        
        mock_phone_analyses[phone_number] = analysis_data
        
        return {
            "status": "success",
            "message": "Đã lưu phân tích số điện thoại mới",
            "updated": False,
            "id": analysis_id
        }

async def get_user_subscription(user_id: str) -> Dict[str, Any]:
    """
    Lấy thông tin gói đăng ký của người dùng.
    
    Args:
        user_id (str): ID của người dùng
        
    Returns:
        Dict[str, Any]: Thông tin gói đăng ký
    """
    if user_id in mock_subscriptions:
        return {
            "status": "success",
            "message": "Đã tìm thấy thông tin gói đăng ký",
            "subscription": mock_subscriptions[user_id]
        }
    else:
        return {
            "status": "error",
            "message": "Không tìm thấy thông tin gói đăng ký",
            "subscription": None
        }

# Tạo FunctionTool để đăng ký các hàm
find_user_tool = FunctionTool(func=find_user)
find_phone_analysis_tool = FunctionTool(func=find_phone_analysis)
save_phone_analysis_tool = FunctionTool(func=save_phone_analysis)
get_user_subscription_tool = FunctionTool(func=get_user_subscription) 