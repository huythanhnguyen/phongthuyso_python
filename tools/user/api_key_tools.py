"""
API Key Tools

Các công cụ xử lý API key.
"""

import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from agents.user_agent.models import ApiKeyCreate

# Mock database cho development
mock_api_keys = {}

def create_api_key(user_id: str, api_key_create: Any) -> Dict[str, Any]:
    """
    Tạo API key mới.
    """
    api_key_id = str(uuid.uuid4())
    api_key = f"pts_{uuid.uuid4().hex}"
    
    expires_at = None
    if hasattr(api_key_create, 'expires_at') and api_key_create.expires_at:
        expires_at = api_key_create.expires_at
    
    api_key_data = {
        "id": api_key_id,
        "key": api_key,
        "name": api_key_create.name if hasattr(api_key_create, 'name') else "API Key",
        "user_id": user_id,
        "created_at": datetime.now(),
        "expires_at": expires_at,
        "last_used_at": None,
        "is_active": True
    }
    
    mock_api_keys[api_key_id] = api_key_data
    
    return api_key_data

def get_api_key(key_id: str) -> Optional[Dict[str, Any]]:
    """
    Get API key by ID.
    
    Args:
        key_id (str): ID của API key
        
    Returns:
        Optional[Dict[str, Any]]: Thông tin API key hoặc None nếu không tìm thấy
    """
    return mock_api_keys.get(key_id)

def list_user_api_keys(user_id: str) -> List[Dict[str, Any]]:
    """
    Lấy danh sách API key của người dùng.
    """
    return [
        key for key in mock_api_keys.values()
        if key["user_id"] == user_id
    ]

def delete_api_key(key_id: str, user_id: str) -> Dict[str, str]:
    """
    Xóa API key.
    """
    if key_id not in mock_api_keys:
        return {"message": "API key not found"}
    
    if mock_api_keys[key_id]["user_id"] != user_id:
        return {"message": "Not authorized to delete this API key"}
    
    del mock_api_keys[key_id]
    
    return {"message": "API key deleted successfully"}

def validate_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    """
    Xác thực API key.
    """
    for key_data in mock_api_keys.values():
        if key_data["key"] == api_key and key_data["is_active"]:
            # Kiểm tra xem key đã hết hạn chưa
            if key_data.get("expires_at") and key_data["expires_at"] < datetime.now():
                return None
                
            # Cập nhật last_used_at
            key_data["last_used_at"] = datetime.now()
            
            return {
                "is_valid": True,
                "user_id": key_data["user_id"],
                "key_id": key_data["id"],
                "scopes": []  # Placeholder cho scopes nếu cần
            }
    
    return None 