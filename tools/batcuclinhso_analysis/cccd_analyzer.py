"""
CCCD Analyzer Tool for Bát Cục Linh Số method
"""

from google.adk.tools import FunctionTool
from typing import Dict, Any, Optional
from constants.bat_tinh import BAT_TINH
from constants.combinations import COMBINATIONS

def cccd_analyzer(cccd_number: str, purpose: Optional[str] = None) -> Dict[str, Any]:
    """Phân tích số CCCD theo phương pháp Bát Cục Linh Số.
    
    Args:
        cccd_number: Số CCCD cần phân tích. Phải là 12 chữ số.
        purpose: Mục đích sử dụng (tùy chọn).
        
    Returns:
        Kết quả phân tích chi tiết.
    """
    try:
        # Validate CCCD number
        # Nếu là 6 số cuối, thêm 6 số đầu giả định
        if len(cccd_number) == 6 and cccd_number.isdigit():
            cccd_number = "199901" + cccd_number  # Thêm một ngày sinh giả định
        
        if not cccd_number.isdigit() or len(cccd_number) != 12:
            raise ValueError("Invalid CCCD number format. Must be 12 digits.")

        # Extract relevant numbers
        birth_year = int(cccd_number[0:4])
        birth_month = int(cccd_number[4:6])
        birth_day = int(cccd_number[6:8])
        last_four = cccd_number[8:12]

        # Calculate Bát Tinh numbers
        bat_tinh_numbers = []
        for i in range(0, 12, 2):
            pair = cccd_number[i:i+2]
            bat_tinh_numbers.append(pair)

        # Analyze each pair
        analysis = []
        total_energy = 0
        for number in bat_tinh_numbers:
            for tinh, info in BAT_TINH.items():
                if number in info["numbers"]:
                    pair_energy = info["energy"].get(number, 2)
                    total_energy += pair_energy
                    analysis.append({
                        "number": number,
                        "tinh": tinh,
                        "name": info["name"],
                        "description": info["description"],
                        "energy": pair_energy,
                        "position": info["position"],
                        "nature": info["nature"]
                    })
                    break

        # Analyze combinations
        combinations = []
        for i in range(len(analysis) - 1):
            current = analysis[i]
            next_tinh = analysis[i + 1]
            combination_key = f"{current['tinh']}_{next_tinh['tinh']}"
            
            if combination_key in COMBINATIONS:
                combinations.append({
                    "numbers": f"{current['number']}-{next_tinh['number']}",
                    "combination": combination_key,
                    "description": COMBINATIONS[combination_key]["description"],
                    "detailed_description": COMBINATIONS[combination_key]["detailedDescription"]
                })

        # Tính toán tổng điểm và mức may mắn
        avg_energy = total_energy / len(analysis) if analysis else 0
        total_score = min(10, max(1, avg_energy * 2))  # Chuyển đổi năng lượng sang thang điểm 1-10
        
        # Xác định mức may mắn dựa trên tổng điểm
        luck_level = "Tốt"
        if total_score >= 8:
            luck_level = "Rất tốt"
        elif total_score >= 6:
            luck_level = "Tốt"
        elif total_score >= 4:
            luck_level = "Trung bình"
        else:
            luck_level = "Kém"

        result = {
            "cccd_number": cccd_number,
            "birth_date": {
                "year": birth_year,
                "month": birth_month,
                "day": birth_day
            },
            "last_four": last_four,
            "analysis": analysis,
            "combinations": combinations,
            "purpose": purpose,
            "total_score": total_score,
            "luck_level": luck_level
        }
        
        return result
    except Exception as e:
        raise ValueError(f"Error analyzing CCCD number: {str(e)}")

# Tạo Function Tool
cccd_analyzer_tool = FunctionTool(cccd_analyzer) 