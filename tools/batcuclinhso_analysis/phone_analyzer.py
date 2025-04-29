"""
Phone Analyzer: Tool để phân tích số điện thoại theo phương pháp Bát Cục Linh Số
Chuyển đổi thành MCP server để sử dụng với Model Context Protocol
"""

import re
import asyncio
import sys
from typing import Dict, Any, List, Optional, Union

# Sử dụng Google ADK FunctionTool
from google.adk.tools import FunctionTool

from constants.bat_tinh import BAT_TINH
from constants.combinations import COMBINATIONS
from constants.digit_meanings import DIGIT_MEANINGS
from constants.response_factors import RESPONSE_FACTORS

# Import các thư viện cần thiết nếu có
try:
    from model_context_protocol import (
        Application,
        InitializationOptions,
        StdioServerConnector,
        build_schema_from_function,
        ToolDefinition,
        ToolParameterDefinition,
        NotificationOptions
    )
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Cảnh báo: Không thể import model_context_protocol. MCP server sẽ không khả dụng.")
    print("Đề xuất: Cài đặt model_context_protocol để sử dụng MCP server.")

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
            # Chuẩn hóa số điện thoại
            phone_number = PhoneAnalyzer._normalize_phone_number(phone_number)
            
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

            # Tính toán điểm số tổng
            total_score = sum(item.get("energy", 0) for item in analysis if isinstance(item.get("energy"), (int, float)))
            if total_score > 0:
                total_score = min(10, total_score / len(analysis) * 2.5)
            else:
                total_score = 5.0

            # Xác định cấp độ may mắn
            if total_score >= 8.5:
                luck_level = "Rất tốt"
            elif total_score >= 7:
                luck_level = "Tốt"
            elif total_score >= 5:
                luck_level = "Trung bình"
            else:
                luck_level = "Cần cải thiện"

            return {
                "phone_number": phone_number,
                "network_code": network_code,
                "subscriber_number": subscriber_number,
                "analysis": analysis,
                "pairs_analysis": analysis,  # Alias cho backward compatibility
                "combinations": combinations,
                "purpose": purpose,
                "total_score": total_score,
                "luck_level": luck_level
            }
        except Exception as e:
            raise ValueError(f"Error analyzing phone number: {str(e)}")

    @staticmethod
    def analyze_last_three_digits(phone_number: str) -> str:
        """Phân tích ý nghĩa của 3 số cuối trong số điện thoại"""
        try:
            # Chuẩn hóa số điện thoại 
            phone_number = PhoneAnalyzer._normalize_phone_number(phone_number)
            
            if not phone_number.isdigit() or len(phone_number) < 3:
                return "Số điện thoại không hợp lệ"
                
            last_three = phone_number[-3:]
            
            # Phân tích các cặp số cuối
            analysis = []
            for i in range(len(last_three) - 1):
                pair = last_three[i:i+2]
                for digit in pair:
                    if digit in DIGIT_MEANINGS:
                        analysis.append(f"Số {digit}: {DIGIT_MEANINGS[digit]}")
            
            # Phân tích tổng của 3 số cuối
            total = sum(int(digit) for digit in last_three)
            
            return f"Ba số cuối {last_three} có tổng là {total}. " + " ".join(analysis)
        except Exception as e:
            return f"Không thể phân tích 3 số cuối: {str(e)}"

    @staticmethod
    def analyze_last_five_digits(phone_number: str) -> str:
        """Phân tích ý nghĩa của 5 số cuối trong số điện thoại"""
        try:
            # Chuẩn hóa số điện thoại
            phone_number = PhoneAnalyzer._normalize_phone_number(phone_number)
            
            if not phone_number.isdigit() or len(phone_number) < 5:
                return "Số điện thoại không hợp lệ"
                
            last_five = phone_number[-5:]
            
            # Phân tích các cặp số
            analysis = []
            for i in range(0, len(last_five) - 1, 2):
                pair = last_five[i:i+2]
                for tinh, info in BAT_TINH.items():
                    if pair in info["numbers"]:
                        analysis.append(f"Cặp số {pair} thuộc {info['name']}: {info['description']}")
                        break
            
            return f"Năm số cuối {last_five}. " + " ".join(analysis)
        except Exception as e:
            return f"Không thể phân tích 5 số cuối: {str(e)}"

    @staticmethod
    def get_phone_recommendations(score: float, pairs_analysis: List[Dict[str, Any]]) -> List[str]:
        """Tạo các khuyến nghị dựa trên phân tích số điện thoại"""
        recommendations = []
        
        # Nếu điểm tổng thể thấp
        if score < 6:
            recommendations.append("Số điện thoại này có điểm phong thủy thấp, nên cân nhắc thay đổi nếu có thể.")
        
        # Tìm cặp số Tuyệt Mệnh
        has_bad_pair = False
        for pair in pairs_analysis:
            # Bỏ qua nếu pair không phải là dict
            if not isinstance(pair, dict):
                continue
                
            # Xác định tên của cặp số từ các key khác nhau
            pair_name = None
            if "name" in pair:
                pair_name = pair.get("name")
            elif "tinh" in pair:
                pair_name = pair.get("tinh")
                
            if not pair_name:
                continue
                
            if pair_name == "Tuyệt Mệnh" or pair_name == "TUYET_MENH":
                # Lấy giá trị cặp số từ nhiều key khác nhau có thể
                pair_value = None
                if "number" in pair:
                    pair_value = pair.get("number")
                elif "originalPair" in pair:
                    pair_value = pair.get("originalPair")
                elif "pair" in pair:
                    pair_value = pair.get("pair")
                else:
                    pair_value = "không xác định"
                    
                position_info = f"vị trí {pair.get('position', '')}" if pair.get("position") else ""
                recommendations.append(f"Cặp số {pair_value} {position_info} là Tuyệt Mệnh, nên tránh.")
                has_bad_pair = True
        
        # Nếu điểm cao và không có cặp xấu
        if score >= 8 and not has_bad_pair:
            recommendations.append("Đây là số điện thoại có phong thủy rất tốt, nên giữ lại.")
        elif score >= 7 and not has_bad_pair:
             recommendations.append("Đây là số điện thoại có phong thủy tốt.")

        # Nếu có nhiều cặp số tốt
        good_pairs_count = 0
        for pair in pairs_analysis:
            if not isinstance(pair, dict):
                continue
                
            # Xử lý được nhiều dạng dữ liệu khác nhau
            pair_score = 0
            if "score" in pair and isinstance(pair["score"], (int, float)):
                pair_score = pair["score"]
            elif "energy" in pair and isinstance(pair["energy"], (int, float)):
                pair_score = pair["energy"]
                
            if pair_score >= 8 or pair_score >= 3:
                good_pairs_count += 1
                
        if good_pairs_count >= 3:
            recommendations.append(f"Số điện thoại có {good_pairs_count} cặp số tốt, rất hợp phong thủy.")
        
        if not recommendations: # Default recommendation if none triggered
            recommendations.append("Đánh giá phong thủy dựa trên điểm số và các cặp số cụ thể.")
            
        return recommendations

    @staticmethod
    def suggest_phone_numbers(purpose: str, preferred_digits: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Đề xuất số điện thoại phù hợp với mục đích sử dụng"""
        # Đây là một hàm đơn giản để mock dữ liệu, trong thực tế nên triển khai thuật toán thực sự
        purpose_lower = purpose.lower()
        
        # Các số mẫu với đặc điểm phong thủy tốt cho các mục đích khác nhau
        sample_phones = {
            "kinh doanh": [
                "0918666888", "0917888999", "0909789789", "0908168168", "0907168168"
            ],
            "cá nhân": [
                "0918339339", "0917868868", "0909969969", "0908558558", "0907668668"
            ],
            "tài lộc": [
                "0919678678", "0918939939", "0917828828", "0909989989", "0908369369"
            ],
            "sự nghiệp": [
                "0919838838", "0918668668", "0917828868", "0909989889", "0908168689"
            ],
            "tình duyên": [
                "0919168168", "0918939839", "0917828238", "0909989639", "0908369968"
            ]
        }
        
        # Chọn danh sách số phù hợp với mục đích
        matching_phones = []
        for key, phones in sample_phones.items():
            if key in purpose_lower or purpose_lower in key:
                matching_phones.extend(phones)
                
        if not matching_phones:
            # Mặc định nếu không tìm thấy mục đích
            matching_phones = sample_phones["cá nhân"]
        
        # Lọc theo các chữ số ưa thích nếu có
        if preferred_digits and len(preferred_digits) > 0:
            filtered_phones = []
            for phone in matching_phones:
                if any(digit in phone for digit in preferred_digits):
                    filtered_phones.append(phone)
            if filtered_phones:
                matching_phones = filtered_phones
        
        # Phân tích các số điện thoại được chọn
        suggestions = []
        for phone in matching_phones[:5]:  # Giới hạn 5 gợi ý
            analysis = PhoneAnalyzer.analyze_phone_number(phone, purpose)
            
            suggestions.append({
                "phone_number": phone,
                "feng_shui_score": analysis["total_score"],
                "purpose_match_score": 8.5,  # Điểm mặc định cho phù hợp mục đích
                "combined_score": (analysis["total_score"] + 8.5) / 2,
                "summary": f"Số {phone} điểm phong thủy {analysis['total_score']:.1f}/10, phù hợp mục đích {purpose}."
            })
            
        # Sắp xếp theo điểm tổng hợp
        suggestions.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return suggestions

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

# Tạo Function Tools cho ADK
phone_analyzer_tool = FunctionTool(PhoneAnalyzer.analyze_phone_number)
last_three_analyzer_tool = FunctionTool(PhoneAnalyzer.analyze_last_three_digits)
last_five_analyzer_tool = FunctionTool(PhoneAnalyzer.analyze_last_five_digits)
phone_recommendations_tool = FunctionTool(PhoneAnalyzer.get_phone_recommendations)
suggest_phone_numbers_tool = FunctionTool(PhoneAnalyzer.suggest_phone_numbers)

def phone_analyzer(phone_number: str, purpose: Optional[str] = None) -> Dict[str, Any]:
    """Phân tích số điện thoại theo phương pháp Bát Cục Linh Số.
    
    Args:
        phone_number: Số điện thoại cần phân tích. Phải là 10 chữ số.
        purpose: Mục đích sử dụng số điện thoại (tùy chọn).
        
    Returns:
        Kết quả phân tích chi tiết.
    """
    return PhoneAnalyzer.analyze_phone_number(phone_number, purpose)

# Khởi tạo MCP server nếu module được chạy trực tiếp
if __name__ == "__main__" and MCP_AVAILABLE:
    async def run_server() -> None:
        """Khởi động MCP server để cung cấp công cụ phân tích số điện thoại"""
        print("Đang khởi động MCP server cho công cụ phân tích số điện thoại...")
        
        # Định nghĩa các công cụ
        tools = [
            ToolDefinition(
                name="analyze_phone_number",
                description="Phân tích số điện thoại theo phương pháp Bát Cục Linh Số",
                parameters={
                    "phone_number": ToolParameterDefinition(
                        type="string",
                        description="Số điện thoại cần phân tích"
                    ),
                    "purpose": ToolParameterDefinition(
                        type="string", 
                        description="Mục đích sử dụng số điện thoại",
                        required=False
                    )
                },
                handler=PhoneAnalyzer.analyze_phone_number
            ),
            ToolDefinition(
                name="analyze_last_three_digits",
                description="Phân tích ý nghĩa của 3 số cuối của số điện thoại",
                parameters={
                    "phone_number": ToolParameterDefinition(
                        type="string",
                        description="Số điện thoại cần phân tích"
                    )
                },
                handler=PhoneAnalyzer.analyze_last_three_digits
            ),
            ToolDefinition(
                name="analyze_last_five_digits",
                description="Phân tích ý nghĩa của 5 số cuối của số điện thoại",
                parameters={
                    "phone_number": ToolParameterDefinition(
                        type="string",
                        description="Số điện thoại cần phân tích"
                    )
                },
                handler=PhoneAnalyzer.analyze_last_five_digits
            ),
            ToolDefinition(
                name="get_phone_recommendations",
                description="Tạo khuyến nghị dựa trên phân tích số điện thoại",
                parameters={
                    "score": ToolParameterDefinition(
                        type="number",
                        description="Điểm phong thủy của số điện thoại"
                    ),
                    "pairs_analysis": ToolParameterDefinition(
                        type="array",
                        description="Phân tích từng cặp số trong số điện thoại"
                    )
                },
                handler=PhoneAnalyzer.get_phone_recommendations
            ),
            ToolDefinition(
                name="suggest_phone_numbers",
                description="Đề xuất số điện thoại phù hợp với mục đích sử dụng",
                parameters={
                    "purpose": ToolParameterDefinition(
                        type="string",
                        description="Mục đích sử dụng số điện thoại"
                    ),
                    "preferred_digits": ToolParameterDefinition(
                        type="array",
                        description="Các chữ số ưa thích",
                        required=False
                    )
                },
                handler=PhoneAnalyzer.suggest_phone_numbers
            )
        ]
        
        # Khởi tạo MCP Application
        app = Application(
            name="PhoneAnalyzerMCP",
            description="MCP Server cung cấp công cụ phân tích số điện thoại theo Bát Cục Linh Số",
            tools=tools
        )
        
        # Kết nối stdin/stdout cho MCP
        connector = StdioServerConnector()
        read_stream, write_stream = await connector.connect()
        
        print("Đã kết nối luồng I/O, bắt đầu quá trình bắt tay MCP...")
        
        # Chạy server
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,  # Sử dụng tên đã định nghĩa ở trên
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        print("MCP Server đã hoàn thành.")

    # Chạy MCP server
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nMCP Server dừng do người dùng hủy.")
    except Exception as e:
        print(f"MCP Server gặp lỗi: {e}")
    finally:
        print("MCP Server đã kết thúc.")
elif __name__ == "__main__":
    print("Không thể khởi động MCP server vì thiếu model_context_protocol.")
    print("Vẫn có thể sử dụng các công cụ phân tích trực tiếp qua FunctionTool.")
    sys.exit(1) 