"""
Authentication Tools

Các công cụ xử lý xác thực người dùng.
"""

import base64
import hashlib
import json
import time
from typing import Any, Dict, Optional


def get_password_hash(password: str) -> str:
    """
    Tạo hash cho mật khẩu.
    
    Args:
        password (str): Mật khẩu cần hash
        
    Returns:
        str: Chuỗi hash của mật khẩu
    """
    # Trong thực tế nên sử dụng thư viện mã hóa như passlib
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Xác minh mật khẩu.
    
    Args:
        plain_password (str): Mật khẩu plain text
        hashed_password (str): Mật khẩu đã hash
        
    Returns:
        bool: True nếu mật khẩu khớp, False nếu không khớp
    """
    return get_password_hash(plain_password) == hashed_password


def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """
    Tạo token JWT.
    
    Args:
        data (Dict[str, Any]): Dữ liệu cần encode
        expires_delta (Optional[int], optional): Thời gian token hết hạn tính bằng giây
        
    Returns:
        str: Token JWT
    """
    # Giả lập JWT trong phiên bản demo
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": time.time() + expires_delta})
    
    encoded_jwt = base64.b64encode(json.dumps(to_encode).encode()).decode()
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Giải mã token JWT.
    
    Args:
        token (str): Token JWT cần decode
        
    Returns:
        Optional[Dict[str, Any]]: Dữ liệu đã decode hoặc None nếu decode thất bại
    """
    try:
        decoded = base64.b64decode(token).decode()
        return json.loads(decoded)
    except Exception:
        return None 