"""
Phone Analyzer: Tool để phân tích số điện thoại theo phương pháp Bát Cục Linh Số
"""

import re
from typing import Dict, Any, List, Optional
# Sử dụng Google ADK FunctionTool
from google.adk.tools import FunctionTool
import os
from python_adk.constants.bat_tinh import BAT_TINH
from python_adk.constants.combinations import COMBINATIONS
from python_adk.constants.digit_meanings import DIGIT_MEANINGS
from python_adk.constants.response_factors import RESPONSE_FACTORS

class PhoneAnalyzer:
    """Class để phân tích số điện thoại theo phương pháp Bát Cục Linh Số"""
    
    @staticmethod
    def analyze_phone_number(phone_number: str, purpose: Optional[str] = None) -> Dict[str, Any]:
        """Phân tích số điện thoại theo phương pháp Bát Cục Linh Số để xác định ý nghĩa phong thủy
        
        Sử dụng tool này khi người dùng yêu cầu phân tích số điện thoại theo phong thủy hoặc muốn biết ý nghĩa của số điện thoại.
        
        Args:
            phone_number: Số điện thoại cần phân tích. Có thể chứa các ký tự đặc biệt như dấu cách, dấu gạch ngang.
            purpose: Mục đích sử dụng số điện thoại (ví dụ: kinh doanh, cá nhân, tài lộc, tình cảm, sự nghiệp). Có thể bỏ trống.
            
        Returns:
            Dict[str, Any]: Kết quả phân tích, bao gồm:
                - success (bool): Trạng thái thành công của việc phân tích
                - message (str): Thông báo lỗi nếu có
                - analysis (Dict): Kết quả phân tích chi tiết nếu thành công, bao gồm:
                    - starSequence: Danh sách các ngôi sao được ánh xạ từ các cặp số
                    - energyLevel: Mức năng lượng tổng hợp
                    - balance: Sự cân bằng âm dương
                    - starCombinations: Các tổ hợp sao liền kề
                    - keyPositions: Các vị trí đặc biệt trong số điện thoại
        """
        try:
            # Validate phone number
            if not phone_number.isdigit() or len(phone_number) != 10:
                raise ValueError("Invalid phone number format. Must be 10 digits.")

            # Extract relevant numbers
            network_code = phone_number[0:3]
            subscriber_number = phone_number[3:10]

            # Calculate Bát Tinh numbers
            bat_tinh_numbers = []
            for i in range(0, 10, 2):
                pair = phone_number[i:i+2]
                bat_tinh_numbers.append(pair)

            # Analyze each pair
            analysis = []
            for number in bat_tinh_numbers:
                for tinh, info in BAT_TINH.items():
                    if number in info["numbers"]:
                        analysis.append({
                            "number": number,
                            "tinh": tinh,
                            "name": info["name"],
                            "description": info["description"],
                            "energy": info["energy"],
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

            return {
                "phone_number": phone_number,
                "network_code": network_code,
                "subscriber_number": subscriber_number,
                "analysis": analysis,
                "combinations": combinations,
                "purpose": purpose
            }
        except Exception as e:
            raise ValueError(f"Error analyzing phone number: {str(e)}")

    @staticmethod
    def _normalize_phone_number(phone: str) -> str:
        """Chuẩn hóa số điện thoại về dạng không có ký tự đặc biệt"""
        # Bỏ tất cả các ký tự không phải số
        normalized = re.sub(r'[^0-9]', '', phone)
        
        # Chuyển +84 về 0
        if normalized.startswith("84") and len(normalized) > 9:
            normalized = "0" + normalized[2:]
            
        return normalized
    
    @staticmethod
    def _get_star_level(energy: int) -> str:
        if energy >= 4:
            return "VERY_HIGH"
        elif energy == 3:
            return "HIGH"
        elif energy == 2:
            return "MEDIUM"
        return "LOW"

    @staticmethod
    def _generate_pairs(digits: str) -> List[str]:
        pairs: List[str] = []
        i = 0
        while i < len(digits) - 1:
            if digits[i] in ("0", "5"):
                i += 1
                continue
            if digits[i+1] not in ("0", "5"):
                pairs.append(digits[i:i+2])
                i += 1
            else:
                j = i + 1
                group = digits[i]
                while j < len(digits) and digits[j] in ("0", "5"):
                    group += digits[j]
                    j += 1
                if j < len(digits):
                    group += digits[j]
                    j += 1
                pairs.append(group)
                i = j - 1
        # xử lý nhóm cuối
        if pairs:
            last = pairs[-1]
            if len(last) > 1 and last[0] not in ("0", "5") and all(c in ("0","5") for c in last[1:]):
                trailing = last[1:]
                pairs[-1] = last[0] + trailing
        return pairs
    
    @staticmethod
    def _map_to_star_sequence(normalized: str) -> List[Dict[str, Any]]:
        pairs = PhoneAnalyzer._generate_pairs(normalized)
        zero_count = normalized.count("0")
        five_count = normalized.count("5")
        special_attr = ""
        special_effect = ""
        if zero_count:
            special_attr = "zero"
            special_effect = "Số 0 làm giảm năng lượng của các sao"
        if five_count:
            special_attr = f"{special_attr}_five" if special_attr else "five"
            msg = "Số 5 tăng cường năng lượng của các sao"
            special_effect = f"{special_effect}, {msg}" if special_effect else msg
        sequence: List[Dict[str,Any]] = []
        for pair in pairs:
            zeroes = pair.count("0")
            fives = pair.count("5")
            clean = "".join(d for d in pair if d not in ("0","5"))
            star_key, star_obj = None, None
            for k,v in BAT_TINH.items():
                if clean in v.get("numbers",[]):
                    star_key, star_obj = k, v
                    break
            base_energy = star_obj.get("energy", {}).get(clean, 1) if star_obj else 1
            energy_level = max(1, base_energy + fives - zeroes)
            level = PhoneAnalyzer._get_star_level(energy_level)
            response_factor = RESPONSE_FACTORS.get("STAR_RESPONSE_FACTORS", {}).get(star_key, 1)
            weighted = energy_level
            adjusted = weighted * response_factor
            sequence.append({
                "originalPair": pair,
                "mappedPair": clean,
                "star": star_key or "UNKNOWN",
                "name": star_obj.get("name", "") if star_obj else "",
                "nature": star_obj.get("nature", "") if star_obj else "",
                "level": level,
                "energyLevel": energy_level,
                "baseEnergyLevel": base_energy,
                "specialAttribute": special_attr,
                "specialEffect": special_effect,
                "detailedDescription": star_obj.get("detailedDescription", "") if star_obj else "",
                "description": star_obj.get("description", "") if star_obj else "",
                "isZeroVariant": zeroes > 0,
                "zeroCount": zeroes,
                "fiveCount": fives,
                "weightedEnergy": weighted,
                "responseFactor": response_factor,
                "adjustedEnergy": adjusted
            })
        return sequence

    @staticmethod
    def _analyze_purpose_compatibility(star_sequence: List[Dict[str, Any]], purpose: str) -> Dict[str, Any]:
        """Phân tích độ phù hợp với mục đích sử dụng"""
        # Các mục đích phổ biến
        purposes = {
            "business": {
                "name": "Kinh doanh",
                "favorable_stars": ["THIEN_Y", "DIEN_NIEN"],
                "unfavorable_stars": ["TUYET_MENH", "NGU_QUY"]
            },
            "personal": {
                "name": "Cá nhân",
                "favorable_stars": ["SINH_KHI", "THIEN_Y"],
                "unfavorable_stars": ["HOA_HAI", "LUC_SAT"]
            },
            "wealth": {
                "name": "Tài lộc",
                "favorable_stars": ["THIEN_Y", "SINH_KHI"],
                "unfavorable_stars": ["TUYET_MENH", "NGU_QUY"]
            }
        }
        
        # Lấy thông tin mục đích
        purpose_info = purposes.get(purpose.lower())
        if not purpose_info:
            return None
            
        # Đếm số sao thuận lợi và bất lợi
        favorable_count = sum(1 for star in star_sequence if star["star"] in purpose_info["favorable_stars"])
        unfavorable_count = sum(1 for star in star_sequence if star["star"] in purpose_info["unfavorable_stars"])
        
        # Tính điểm phù hợp
        total_stars = len(star_sequence)
        compatibility_score = (favorable_count - unfavorable_count) / total_stars if total_stars > 0 else 0
        
        # Xác định mức độ phù hợp
        if compatibility_score >= 0.5:
            compatibility_level = "Rất phù hợp"
        elif compatibility_score >= 0:
            compatibility_level = "Phù hợp"
        elif compatibility_score >= -0.5:
            compatibility_level = "Không phù hợp"
        else:
            compatibility_level = "Rất không phù hợp"
        
        return {
            "purpose": purpose_info["name"],
            "favorable_stars": purpose_info["favorable_stars"],
            "unfavorable_stars": purpose_info["unfavorable_stars"],
            "favorable_count": favorable_count,
            "unfavorable_count": unfavorable_count,
            "compatibility_score": compatibility_score,
            "compatibility_level": compatibility_level
        }

def phone_analyzer(phone_number: str, purpose: Optional[str] = None) -> Dict[str, Any]:
    """Phân tích số điện thoại theo phương pháp Bát Cục Linh Số.
    
    Args:
        phone_number: Số điện thoại cần phân tích. Phải là 10 chữ số.
        purpose: Mục đích sử dụng số điện thoại (tùy chọn).
        
    Returns:
        Kết quả phân tích chi tiết.
    """
    return PhoneAnalyzer.analyze_phone_number(phone_number, purpose)

# Tạo Function Tool
phone_analyzer_tool = FunctionTool(phone_analyzer) 