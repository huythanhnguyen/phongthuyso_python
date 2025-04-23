"""
API Key Tools Module

Module chứa các công cụ quản lý API keys cho User Agent
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from phongthuyso_python.agents.user_agent.models import ApiKeyCreate
from phongthuyso_python.agents.user_agent.tools.user_tools import mock_api_keys


def create_api_key(user_id: str, api_key_create: ApiKeyCreate) -> Dict[str, Any]:
    """
    Create a new API key.
    
    Args:
        user_id (str): ID của người dùng
        api_key_create (ApiKeyCreate): Thông tin API key cần tạo
        
    Returns:
        Dict[str, Any]: Thông tin API key đã tạo
    """
    api_key_id = str(uuid.uuid4())
    api_key = f"pts_{uuid.uuid4().hex}"
    
    api_key_data = {
        "id": api_key_id,
        "key": api_key,
        "name": api_key_create.name,
        "user_id": user_id,
        "created_at": datetime.now(),
        "expires_at": api_key_create.expires_at,
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
    List all API keys for a user.
    
    Args:
        user_id (str): ID của người dùng
        
    Returns:
        List[Dict[str, Any]]: Danh sách API key của người dùng
    """
    return [key for key in mock_api_keys.values() if key["user_id"] == user_id]


def delete_api_key(key_id: str, user_id: str) -> Dict[str, str]:
    """
    Delete an API key.
    
    Args:
        key_id (str): ID của API key
        user_id (str): ID của người dùng
        
    Returns:
        Dict[str, str]: Thông báo kết quả
    """
    if key_id not in mock_api_keys:
        raise HTTPException(status_code=404, detail="API key not found")
    
    if mock_api_keys[key_id]["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this API key")
    
    del mock_api_keys[key_id]
    
    return {"message": "API key deleted successfully"} 