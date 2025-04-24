"""
Tool để phân tích mật khẩu dựa trên phương pháp Bát Cục Linh Số
"""

from google.adk.tools import FunctionTool
from typing import Dict, Any, List, Optional
from utils.common import extract_digits

def password_analyzer(password: str) -> Dict[str, Any]:
    """
    Phân tích mật khẩu dựa trên phương pháp Bát Cục Linh Số.
    
    Args:
        password (str): Mật khẩu cần phân tích
        
    Returns:
        Dict[str, Any]: Kết quả phân tích mật khẩu
    """
    if not password:
        raise ValueError("Mật khẩu không được để trống")
    
    # Tách các chữ số và các ký tự đặc biệt
    digits = extract_digits(password)
    characters = ''.join([c for c in password if not c.isdigit()])
    
    # Cơ bản phân tích
    digit_count = len(digits)
    char_count = len(characters)
    length = len(password)
    is_secure = length >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)
    
    # Phân tích theo Bát Cục Linh Số
    energy = sum(int(d) for d in digits) if digits else 0
    energy_score = energy % 9 or 9
    
    energy_meanings = {
        1: "Thuộc hành Thủy, biểu thị sự khởi đầu, nguồn gốc, và tính đơn lẻ",
        2: "Thuộc hành Thổ, biểu thị sự cân bằng, hài hòa và tính song song",
        3: "Thuộc hành Mộc, biểu thị sự phát triển, tăng trưởng và tính sáng tạo",
        4: "Thuộc hành Kim, biểu thị sự ổn định, vững chắc và tính kỷ luật",
        5: "Thuộc hành Thổ, biểu thị sự thay đổi, linh hoạt và biến đổi không ngừng",
        6: "Thuộc hành Kim, biểu thị sự hài hòa, yên bình và tính cống hiến",
        7: "Thuộc hành Thủy, biểu thị sự bí ẩn, trực giác và tính tâm linh",
        8: "Thuộc hành Mộc, biểu thị sự phát đạt, thịnh vượng và tính bền vững",
        9: "Thuộc hành Hỏa, biểu thị sự viên mãn, hoàn thành và tính lý tưởng"
    }
    
    # Kết quả phân tích
    return {
        "success": True,
        "password": "***" + password[-3:] if len(password) > 3 else "***",
        "analysis": {
            "length": length,
            "digitCount": digit_count,
            "characterCount": char_count,
            "isSecure": is_secure,
            "energyNumber": energy_score,
            "energyMeaning": energy_meanings.get(energy_score, "Không xác định"),
            "recommendations": [
                "Mật khẩu nên có ít nhất 8 ký tự" if length < 8 else "Độ dài mật khẩu tốt",
                "Nên kết hợp cả chữ và số" if not (any(c.isdigit() for c in password) and any(c.isalpha() for c in password)) else "Kết hợp chữ và số tốt",
                "Nên thêm ký tự đặc biệt" if not any(not c.isalnum() for c in password) else "Có ký tự đặc biệt là tốt",
                f"Mật khẩu mang năng lượng số {energy_score}, {energy_meanings.get(energy_score, '')}"
            ]
        }
    }

# Tạo Function Tool
password_analyzer_tool = FunctionTool(password_analyzer) 