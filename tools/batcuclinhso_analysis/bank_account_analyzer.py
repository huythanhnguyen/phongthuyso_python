"""
Tool để phân tích số tài khoản ngân hàng dựa trên phương pháp Bát Cục Linh Số
"""

from google.adk.tools import FunctionTool
from typing import Dict, Any, List, Optional
from utils.common import extract_digits

def bank_account_analyzer(account_number: str) -> Dict[str, Any]:
    """
    Phân tích số tài khoản ngân hàng dựa trên phương pháp Bát Cục Linh Số.
    
    Args:
        account_number (str): Số tài khoản cần phân tích
        
    Returns:
        Dict[str, Any]: Kết quả phân tích số tài khoản
    """
    if not account_number:
        raise ValueError("Số tài khoản không được để trống")
    
    # Chỉ lấy các chữ số trong số tài khoản
    digits = extract_digits(account_number)
    
    if not digits:
        raise ValueError("Số tài khoản phải chứa ít nhất một chữ số")
    
    # Tính tổng các chữ số
    digit_sum = sum(int(d) for d in digits)
    energy_number = digit_sum % 9 or 9
    
    # Phân tích ngũ hành
    five_elements_map = {
        1: "Thủy",
        2: "Thổ",
        3: "Mộc",
        4: "Kim",
        5: "Thổ",
        6: "Kim",
        7: "Thủy",
        8: "Mộc",
        9: "Hỏa"
    }
    
    # Đếm tần suất các chữ số
    digit_frequency = {str(i): digits.count(str(i)) for i in range(10)}
    
    # Xác định các cặp số đặc biệt
    special_pairs = [
        ('6', '8'), # Tấn Lộc - Vượng Tài
        ('8', '9'), # Tài Lộc - Tài Thành
        ('9', '6'), # Thành Tấn - Công Thành
        ('1', '6'), # Nguyên Tấn - Thủy Sinh Mộc
        ('2', '8'), # Địa Tài - Thổ Sinh Kim
        ('3', '9'), # Sinh Thành - Mộc Sinh Hỏa
        ('4', '6')  # Kim sinh Thủy
    ]
    
    found_pairs = []
    for pair in special_pairs:
        for i in range(len(digits) - 1):
            if digits[i] == pair[0] and digits[i+1] == pair[1]:
                found_pairs.append(f"{pair[0]}{pair[1]}")
    
    # Ý nghĩa năng lượng số
    energy_meanings = {
        1: "Chủ động, sáng tạo, khởi đầu mới, độc lập",
        2: "Hợp tác, cân bằng, kiên nhẫn, bền bỉ",
        3: "Phát triển, mở rộng, linh hoạt, sáng tạo",
        4: "Ổn định, chắc chắn, kỷ luật, xây dựng",
        5: "Thay đổi, linh hoạt, tự do, phiêu lưu",
        6: "Hài hòa, trách nhiệm, phụng sự, cống hiến",
        7: "Phân tích, chiêm nghiệm, trí tuệ, tâm linh",
        8: "Thịnh vượng, quyền lực, thành tựu, vật chất",
        9: "Hoàn thành, viên mãn, lý tưởng, nhân đạo"
    }
    
    # Đánh giá mức độ may mắn
    lucky_numbers = ['6', '8', '9']
    unlucky_numbers = ['4', '7']
    
    lucky_count = sum(digits.count(d) for d in lucky_numbers)
    unlucky_count = sum(digits.count(d) for d in unlucky_numbers)
    
    lucky_ratio = lucky_count / len(digits) if len(digits) > 0 else 0
    
    # Đánh giá mức độ thuận lợi
    if lucky_ratio >= 0.5:
        prosperity_level = "Rất tốt"
    elif lucky_ratio >= 0.3:
        prosperity_level = "Tốt"
    elif lucky_ratio >= 0.2:
        prosperity_level = "Trung bình"
    else:
        prosperity_level = "Ít thuận lợi"
    
    # Kết quả phân tích
    return {
        "success": True,
        "accountNumber": account_number,
        "analysis": {
            "energyNumber": energy_number,
            "element": five_elements_map[energy_number],
            "energyMeaning": energy_meanings[energy_number],
            "digitFrequency": digit_frequency,
            "specialPairs": found_pairs,
            "prosperityLevel": prosperity_level,
            "recommendation": f"Số tài khoản này mang năng lượng số {energy_number} ({five_elements_map[energy_number]}), {energy_meanings[energy_number].lower()}.",
            "luckyCount": lucky_count,
            "unluckyCount": unlucky_count
        }
    }

# Tạo Function Tool
bank_account_analyzer_tool = FunctionTool(bank_account_analyzer) 