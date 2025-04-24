"""
Common utility functions for phongthuyso_python
"""

import re
from typing import List

def extract_digits(text: str) -> str:
    """
    Trích xuất chỉ các chữ số từ một chuỗi văn bản
    
    Args:
        text: Chuỗi văn bản cần trích xuất
        
    Returns:
        Chuỗi chỉ chứa các chữ số
    """
    if not text:
        return ""
    return re.sub(r'[^0-9]', '', text)

def normalize_phone_number(phone: str) -> str:
    """
    Chuẩn hóa số điện thoại về dạng tiêu chuẩn
    
    Args:
        phone: Số điện thoại cần chuẩn hóa
        
    Returns:
        Số điện thoại đã chuẩn hóa
    """
    # Chỉ giữ lại các chữ số
    digits = extract_digits(phone)
    
    # Chuyển +84 về 0
    if digits.startswith("84") and len(digits) > 9:
        digits = "0" + digits[2:]
        
    return digits

def split_into_pairs(digits: str) -> List[str]:
    """
    Chia một chuỗi số thành các cặp
    
    Args:
        digits: Chuỗi số cần chia
        
    Returns:
        Danh sách các cặp số
    """
    pairs = []
    for i in range(0, len(digits) - 1, 2):
        pairs.append(digits[i:i+2])
    
    # Nếu có số lẻ ở cuối
    if len(digits) % 2 != 0:
        pairs.append(digits[-1])
        
    return pairs 