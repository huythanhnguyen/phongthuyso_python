"""
Authentication Tools

Các công cụ xử lý xác thực người dùng.
"""

import base64
import hashlib
import json
import time
from typing import Any, Dict, Optional
import jwt
from datetime import datetime, timedelta

# Khóa bí mật để ký JWT
SECRET_KEY = "your-256-bit-secret"  # Trong thực tế nên lưu trong biến môi trường
ALGORITHM = "HS256"

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
    # Trong thực tế nên sử dụng thư viện mã hóa như passlib
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """
    Tạo token JWT.
    
    Args:
        data (Dict[str, Any]): Dữ liệu cần encode
        expires_delta (Optional[int], optional): Thời gian token hết hạn tính bằng giây
        
    Returns:
        str: Token JWT
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
    except Exception:
        return None 