"""
User Tools

Các công cụ xử lý thông tin người dùng.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from agents.user_agent.models import User, UserCreate, UserUpdate
from .auth_tools import get_password_hash

# Mock database cho development
mock_users = {}
mock_api_keys = {}


def create_user(user_create: Any) -> Dict[str, Any]:
    """
    Tạo người dùng mới.
    """
    if not hasattr(user_create, 'email') or get_user_by_email(user_create.email):
        return {"error": "Email already registered"}
    
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user_create.password if hasattr(user_create, 'password') else "")
    
    user_data = {
        "id": user_id,
        "email": user_create.email,
        "fullname": user_create.fullname if hasattr(user_create, 'fullname') else "",
        "hashed_password": hashed_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True,
        "is_premium": False,
        "quota_remaining": 5  # Default quota
    }
    
    mock_users[user_create.email] = user_data
    
    return {**user_data, "hashed_password": ""}


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin người dùng theo email.
    """
    return mock_users.get(email)


def update_user(email: str, user_update: Any) -> Dict[str, Any]:
    """
    Cập nhật thông tin người dùng.
    """
    if email not in mock_users:
        return {"error": "User not found"}
    
    user_data = mock_users[email]
    
    if hasattr(user_update, 'fullname') and user_update.fullname:
        user_data["fullname"] = user_update.fullname
    
    if hasattr(user_update, 'email') and user_update.email and user_update.email != email:
        if user_update.email in mock_users:
            return {"error": "Email already registered"}
        
        # Copy to new email key
        mock_users[user_update.email] = user_data
        del mock_users[email]
        user_data["email"] = user_update.email
    
    if hasattr(user_update, 'password') and user_update.password:
        user_data["hashed_password"] = get_password_hash(user_update.password)
    
    user_data["updated_at"] = datetime.now()
    
    return {**user_data, "hashed_password": ""}


def validate_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    """
    Validate API key.
    
    Args:
        api_key (str): API key cần xác thực
        
    Returns:
        Optional[Dict[str, Any]]: Thông tin API key nếu hợp lệ, None nếu không hợp lệ
    """
    for key_id, key_data in mock_api_keys.items():
        if key_data["key"] == api_key and key_data["is_active"]:
            # Cập nhật last_used_at
            key_data["last_used_at"] = datetime.now()
            
            # Kiểm tra xem key đã hết hạn chưa
            if key_data.get("expires_at") and key_data["expires_at"] < datetime.now():
                return None
                
            # Lấy thông tin user
            user_id = key_data["user_id"]
            for email, user in mock_users.items():
                if user["id"] == user_id and user["is_active"]:
                    return key_data
            
            return None
            
    return None


def get_all_users() -> List[Dict[str, Any]]:
    """
    Get all users.
    
    Returns:
        List[Dict[str, Any]]: Danh sách tất cả người dùng
    """
    return [{**user, "hashed_password": ""} for user in mock_users.values()] 