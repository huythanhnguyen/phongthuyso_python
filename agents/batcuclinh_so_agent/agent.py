"""
BatCucLinhSo Agent Implementation

Triển khai BatCucLinhSoAgent - Agent phân tích phong thủy số học.
"""

from typing import Any, Dict, List, Optional, Set, Union

# Import AgentTool từ google.adk.tools.agent_tool
from google.adk.tools import FunctionTool # Import FunctionTool

# Import agent_tool và agent_tool_registry từ root_agent để sử dụng implement mới
# from python_adk.agents.root_agent.agent import AgentType # Chỉ import AgentType
from python_adk.agents.base_agent import BaseAgent # Import BaseAgent để gọi super
from python_adk.prompt import get_agent_prompt
from python_adk.shared_libraries.logger import get_logger
from python_adk.shared_libraries.models import (
    PhoneAnalysisRequest,
    CCCDAnalysisRequest,
    BankAccountRequest,
    PasswordRequest
)

class BatCucLinhSoAgent(BaseAgent):
    """
    BatCucLinhSo Agent - Agent chuyên biệt phân tích phong thủy số học
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash", name: str = "bat_cuc_linh_so_agent"):
        """
        Khởi tạo BatCucLinhSo Agent
        
        Args:
            model_name (str): Tên model sử dụng cho agent
            name (str): Tên của agent
        """
        # Import AgentType from the new module
        from python_adk.agents.agent_types import AgentType
        # Lấy prompt làm instruction
        instruction = get_agent_prompt(AgentType.BATCUCLINH_SO)
        
        # Khởi tạo cơ sở dữ liệu phong thủy số học TRƯỚC khi gọi super
        self._init_fengshui_database()
        
        # Tạo danh sách tools từ các phương thức của class
        agent_tools = [
            FunctionTool(self.analyze_phone),
            FunctionTool(self.analyze_cccd),
            FunctionTool(self.suggest_phone),
            FunctionTool(self.analyze_bank_account),
            FunctionTool(self.generate_password)
        ]
        
        # Gọi constructor của BaseAgent, truyền tools vào
        super().__init__(
            name=name,
            model_name=model_name,
            instruction=instruction,
            tools=agent_tools # Truyền danh sách tools
        )
    
    def _init_fengshui_database(self) -> None:
        """Khởi tạo cơ sở dữ liệu phong thủy số học"""
        # Các cặp số theo Bát Cực Linh Số và ý nghĩa
        self.number_pairs_meaning = {
            "19": {"name": "Đường Quan", "meaning": "Tốt cho công danh sự nghiệp", "score": 8},
            "91": {"name": "Đường Quan", "meaning": "Tốt cho công danh sự nghiệp", "score": 8},
            "28": {"name": "Sinh Khí", "meaning": "Tốt cho sức khỏe và phát triển", "score": 9},
            "82": {"name": "Sinh Khí", "meaning": "Tốt cho sức khỏe và phát triển", "score": 9},
            "37": {"name": "Diên Niên", "meaning": "Ổn định, bền vững", "score": 7},
            "73": {"name": "Diên Niên", "meaning": "Ổn định, bền vững", "score": 7},
            "46": {"name": "Thiên Y", "meaning": "Tốt cho sức khỏe, học tập", "score": 8},
            "64": {"name": "Thiên Y", "meaning": "Tốt cho sức khỏe, học tập", "score": 8},
            "38": {"name": "Phát Tài", "meaning": "Tốt cho tiền bạc, kinh doanh", "score": 9},
            "83": {"name": "Phát Tài", "meaning": "Tốt cho tiền bạc, kinh doanh", "score": 9},
            "29": {"name": "Thiên Mã", "meaning": "Tốt cho di chuyển, giao tiếp", "score": 8},
            "92": {"name": "Thiên Mã", "meaning": "Tốt cho di chuyển, giao tiếp", "score": 8},
            "47": {"name": "Tuyệt Mệnh", "meaning": "Xấu, nên tránh", "score": 2},
            "74": {"name": "Tuyệt Mệnh", "meaning": "Xấu, nên tránh", "score": 2},
            "39": {"name": "Khả Ái", "meaning": "Tốt cho tình cảm, hôn nhân", "score": 8},
            "93": {"name": "Khả Ái", "meaning": "Tốt cho tình cảm, hôn nhân", "score": 8},
        }
        
        # Ý nghĩa của các số đơn
        self.single_number_meaning = {
            "0": {"meaning": "Trung tính, gắn liền với khả năng tiếp thu, tích lũy", "score": 5},
            "1": {"meaning": "Tượng trưng cho sự khởi đầu, tiên phong, độc lập", "score": 7},
            "2": {"meaning": "Tượng trưng cho sự hài hòa, hợp tác, kiên nhẫn", "score": 6},
            "3": {"meaning": "Tượng trưng cho sự sáng tạo, biểu đạt, giao tiếp", "score": 7},
            "4": {"meaning": "Tượng trưng cho sự ổn định, thực tế, kiên định", "score": 5},
            "5": {"meaning": "Tượng trưng cho sự tự do, thay đổi, khám phá", "score": 7},
            "6": {"meaning": "Tượng trưng cho sự hài hòa, cân bằng, trách nhiệm", "score": 6},
            "7": {"meaning": "Tượng trưng cho sự phân tích, trí tuệ, tâm linh", "score": 6},
            "8": {"meaning": "Tượng trưng cho sự phát đạt, quyền lực, thành công", "score": 8},
            "9": {"meaning": "Tượng trưng cho sự hoàn thành, lý tưởng, nhân đạo", "score": 7},
        }
    
    def analyze_phone(self, request: PhoneAnalysisRequest) -> Dict[str, Any]:
        """
        Phân tích số điện thoại theo nguyên lý Bát Cực Linh Số
        
        Args:
            request (PhoneAnalysisRequest): Yêu cầu phân tích số điện thoại
            
        Returns:
            Dict[str, Any]: Kết quả phân tích chi tiết
        """
        phone_number = request.phone_number
        self.logger.info(f"Phân tích số điện thoại: {phone_number}")
        
        # Phân tích từng cặp số
        pairs_analysis = []
        for i in range(0, len(phone_number) - 1):
            pair = phone_number[i:i+2]
            if pair in self.number_pairs_meaning:
                info = self.number_pairs_meaning[pair]
                pairs_analysis.append({
                    "pair": pair,
                    "position": i + 1,
                    "name": info["name"],
                    "meaning": info["meaning"],
                    "score": info["score"]
                })
            else:
                # Nếu không có trong cơ sở dữ liệu, phân tích dựa trên số đơn
                digit1 = self.single_number_meaning[pair[0]]
                digit2 = self.single_number_meaning[pair[1]]
                avg_score = (digit1["score"] + digit2["score"]) / 2
                
                pairs_analysis.append({
                    "pair": pair,
                    "position": i + 1,
                    "name": "Cặp số thông thường",
                    "meaning": f"Kết hợp {pair[0]} ({digit1['meaning']}) và {pair[1]} ({digit2['meaning']})",
                    "score": avg_score
                })
        
        # Tính điểm tổng thể
        total_score = sum(pair["score"] for pair in pairs_analysis) / len(pairs_analysis)
        
        # Xác định mức độ may mắn
        if total_score >= 8:
            luck_level = "Rất tốt"
        elif total_score >= 7:
            luck_level = "Tốt"
        elif total_score >= 6:
            luck_level = "Khá"
        elif total_score >= 5:
            luck_level = "Trung bình"
        else:
            luck_level = "Kém"
        
        # Ý nghĩa 3 số cuối
        last_three = phone_number[-3:]
        last_three_analysis = "Chưa có phân tích chi tiết cho 3 số cuối"
        
        # Ý nghĩa 5 số cuối
        last_five = phone_number[-5:]
        last_five_analysis = "Chưa có phân tích chi tiết cho 5 số cuối"
        
        return {
            "phone_number": phone_number,
            "pairs_analysis": pairs_analysis,
            "total_score": total_score,
            "luck_level": luck_level,
            "last_three_digit_analysis": last_three_analysis,
            "last_five_digit_analysis": last_five_analysis,
            "recommendations": self._get_phone_recommendations(total_score, pairs_analysis)
        }
    
    def _get_phone_recommendations(self, score: float, pairs_analysis: List[Dict[str, Any]]) -> List[str]:
        """
        Tạo các khuyến nghị dựa trên phân tích số điện thoại
        
        Args:
            score (float): Điểm tổng thể
            pairs_analysis (List[Dict[str, Any]]): Phân tích từng cặp số
            
        Returns:
            List[str]: Danh sách các khuyến nghị
        """
        recommendations = []
        
        # Nếu điểm tổng thể thấp
        if score < 6:
            recommendations.append("Số điện thoại này có điểm phong thủy thấp, nên cân nhắc thay đổi nếu có thể.")
        
        # Tìm cặp số Tuyệt Mệnh
        for pair in pairs_analysis:
            if pair["name"] == "Tuyệt Mệnh":
                recommendations.append(f"Cặp số {pair['pair']} ở vị trí {pair['position']} là Tuyệt Mệnh, nên tránh.")
        
        # Nếu điểm cao
        if score >= 8:
            recommendations.append("Đây là số điện thoại có phong thủy rất tốt, nên giữ lại.")
        
        # Nếu có nhiều cặp số tốt
        good_pairs = [pair for pair in pairs_analysis if pair["score"] >= 8]
        if len(good_pairs) >= 3:
            recommendations.append(f"Số điện thoại có {len(good_pairs)} cặp số tốt, rất hợp phong thủy.")
        
        return recommendations
    
    def analyze_cccd(self, request: CCCDAnalysisRequest) -> Dict[str, Any]:
        """
        Phân tích 6 số cuối của CCCD theo nguyên lý Bát Cực Linh Số
        
        Args:
            request (CCCDAnalysisRequest): Yêu cầu phân tích 6 số cuối CCCD
            
        Returns:
            Dict[str, Any]: Kết quả phân tích chi tiết
        """
        last_digits = request.cccd_last_digits
        self.logger.info(f"Phân tích CCCD: {last_digits}")
        
        # Phân tích từng cặp số
        pairs_analysis = []
        for i in range(0, len(last_digits) - 1, 2):
            pair = last_digits[i:i+2]
            if pair in self.number_pairs_meaning:
                info = self.number_pairs_meaning[pair]
                pairs_analysis.append({
                    "pair": pair,
                    "position": (i // 2) + 1,
                    "name": info["name"],
                    "meaning": info["meaning"],
                    "score": info["score"]
                })
            else:
                # Nếu không có trong cơ sở dữ liệu, phân tích dựa trên số đơn
                digit1 = self.single_number_meaning[pair[0]]
                digit2 = self.single_number_meaning[pair[1]]
                avg_score = (digit1["score"] + digit2["score"]) / 2
                
                pairs_analysis.append({
                    "pair": pair,
                    "position": (i // 2) + 1,
                    "name": "Cặp số thông thường",
                    "meaning": f"Kết hợp {pair[0]} ({digit1['meaning']}) và {pair[1]} ({digit2['meaning']})",
                    "score": avg_score
                })
        
        # Tính điểm tổng thể
        total_score = sum(pair["score"] for pair in pairs_analysis) / len(pairs_analysis)
        
        # Xác định mức độ may mắn
        if total_score >= 8:
            luck_level = "Rất tốt"
        elif total_score >= 7:
            luck_level = "Tốt"
        elif total_score >= 6:
            luck_level = "Khá"
        elif total_score >= 5:
            luck_level = "Trung bình"
        else:
            luck_level = "Kém"
        
        # Ý nghĩa tổng thể
        overall_meaning = self._get_cccd_overall_meaning(pairs_analysis, total_score)
        
        return {
            "cccd_last_digits": last_digits,
            "pairs_analysis": pairs_analysis,
            "total_score": total_score,
            "luck_level": luck_level,
            "overall_meaning": overall_meaning
        }
    
    def _get_cccd_overall_meaning(self, pairs_analysis: List[Dict[str, Any]], score: float) -> str:
        """
        Tạo ý nghĩa tổng thể dựa trên phân tích CCCD
        
        Args:
            pairs_analysis (List[Dict[str, Any]]): Phân tích từng cặp số
            score (float): Điểm tổng thể
            
        Returns:
            str: Ý nghĩa tổng thể
        """
        # Tìm cặp số có điểm cao nhất và thấp nhất
        max_pair = max(pairs_analysis, key=lambda x: x["score"])
        min_pair = min(pairs_analysis, key=lambda x: x["score"])
        
        if score >= 8:
            return f"CCCD của bạn có phong thủy rất tốt. Đặc biệt, cặp số {max_pair['pair']} ({max_pair['name']}) ở vị trí {max_pair['position']} mang lại nhiều may mắn về {max_pair['meaning'].lower()}."
        elif score >= 7:
            return f"CCCD của bạn có phong thủy tốt. Cặp số {max_pair['pair']} ({max_pair['name']}) là điểm sáng, trong khi cặp số {min_pair['pair']} có thể cần lưu ý."
        elif score >= 6:
            return f"CCCD của bạn có phong thủy khá. Có sự cân bằng giữa các cặp số, với cặp số {max_pair['pair']} mang lại ảnh hưởng tích cực."
        elif score >= 5:
            return f"CCCD của bạn có phong thủy trung bình. Cặp số {min_pair['pair']} có thể gây ảnh hưởng tiêu cực nên cần lưu ý."
        else:
            return f"CCCD của bạn có phong thủy kém. Đặc biệt cặp số {min_pair['pair']} ({min_pair['name']}) ở vị trí {min_pair['position']} cần được lưu ý."
    
    def suggest_phone(self, purpose: str, preferred_digits: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Đề xuất số điện thoại phù hợp với mục đích
        
        Args:
            purpose (str): Mục đích sử dụng số điện thoại
            preferred_digits (Optional[List[str]]): Các chữ số ưa thích
            
        Returns:
            List[Dict[str, Any]]: Danh sách số điện thoại đề xuất kèm phân tích
        """
        self.logger.info(f"Đề xuất số điện thoại cho mục đích: {purpose}")
        
        # Mẫu số điện thoại (sẽ thay bằng thuật toán thực tế)
        sample_phones = [
            "0901234567",
            "0912345678",
            "0923456789",
            "0934567890",
            "0945678901"
        ]
        
        # Phân tích và đề xuất số điện thoại
        suggestions = []
        for phone in sample_phones:
            analysis = self.analyze_phone(PhoneAnalysisRequest(phone_number=phone))
            
            # Tính mức độ phù hợp với mục đích
            purpose_match_score = self._calculate_purpose_match(phone, purpose)
            
            suggestions.append({
                "phone_number": phone,
                "total_score": analysis["total_score"],
                "purpose_match_score": purpose_match_score,
                "combined_score": (analysis["total_score"] + purpose_match_score) / 2,
                "summary": f"Số điện thoại {phone} có điểm phong thủy {analysis['total_score']:.1f}/10, phù hợp {purpose_match_score:.1f}/10 cho mục đích {purpose}"
            })
        
        # Sắp xếp theo điểm tổng hợp
        suggestions.sort(key=lambda x: x["combined_score"], reverse=True)
        
        return suggestions[:5]  # Trả về 5 đề xuất tốt nhất
    
    def _calculate_purpose_match(self, phone: str, purpose: str) -> float:
        """
        Tính điểm phù hợp với mục đích
        
        Args:
            phone (str): Số điện thoại
            purpose (str): Mục đích sử dụng
            
        Returns:
            float: Điểm phù hợp (0-10)
        """
        purpose_lower = purpose.lower()
        
        # Điểm cơ bản
        score = 7.0
        
        # Kiểm tra từng cặp số có phù hợp với mục đích không
        for i in range(len(phone) - 1):
            pair = phone[i:i+2]
            if pair in self.number_pairs_meaning:
                info = self.number_pairs_meaning[pair]
                
                # Kinh doanh, tài chính
                if "kinh doanh" in purpose_lower or "tài chính" in purpose_lower or "công ty" in purpose_lower:
                    if info["name"] in ["Phát Tài", "Sinh Khí"]:
                        score += 0.5
                
                # Sự nghiệp, công việc
                elif "sự nghiệp" in purpose_lower or "công việc" in purpose_lower or "thăng tiến" in purpose_lower:
                    if info["name"] in ["Đường Quan", "Sinh Khí"]:
                        score += 0.5
                
                # Học tập
                elif "học tập" in purpose_lower or "giáo dục" in purpose_lower or "nghiên cứu" in purpose_lower:
                    if info["name"] in ["Thiên Y", "Diên Niên"]:
                        score += 0.5
                
                # Tình cảm, gia đình
                elif "tình cảm" in purpose_lower or "gia đình" in purpose_lower or "hôn nhân" in purpose_lower:
                    if info["name"] in ["Khả Ái", "Diên Niên"]:
                        score += 0.5
                
                # Sức khỏe
                elif "sức khỏe" in purpose_lower or "y tế" in purpose_lower:
                    if info["name"] in ["Thiên Y", "Sinh Khí"]:
                        score += 0.5
                
                # Trừ điểm cho Tuyệt Mệnh
                if info["name"] == "Tuyệt Mệnh":
                    score -= 1.0
        
        # Kiểm tra số cuối
        if "kinh doanh" in purpose_lower and phone[-1] in ["8", "9"]:
            score += 0.5
        elif "sức khỏe" in purpose_lower and phone[-1] in ["6", "9"]:
            score += 0.5
        
        # Giới hạn điểm
        return min(max(score, 1.0), 10.0)
    
    def analyze_bank_account(self, request: BankAccountRequest) -> Dict[str, Any]:
        """
        Phân tích hoặc đề xuất số tài khoản ngân hàng
        
        Args:
            request (BankAccountRequest): Yêu cầu phân tích/đề xuất số tài khoản
            
        Returns:
            Dict[str, Any]: Kết quả phân tích hoặc đề xuất
        """
        self.logger.info(f"Phân tích/đề xuất số tài khoản ngân hàng cho mục đích: {request.purpose}")
        
        # Đề xuất các cặp số cuối cho số tài khoản
        suggested_pairs = []
        
        # Tìm các cặp số phù hợp với mục đích
        purpose_lower = request.purpose.lower()
        
        if "kinh doanh" in purpose_lower or "tài chính" in purpose_lower:
            suggested_pairs.extend([
                {"pair": "38", "name": "Phát Tài", "meaning": "Rất tốt cho kinh doanh và tài chính", "score": 9},
                {"pair": "83", "name": "Phát Tài", "meaning": "Rất tốt cho kinh doanh và tài chính", "score": 9},
                {"pair": "28", "name": "Sinh Khí", "meaning": "Mang lại sự phát triển bền vững", "score": 8.5}
            ])
        elif "tiết kiệm" in purpose_lower or "đầu tư" in purpose_lower:
            suggested_pairs.extend([
                {"pair": "37", "name": "Diên Niên", "meaning": "Ổn định, tích lũy lâu dài", "score": 8},
                {"pair": "73", "name": "Diên Niên", "meaning": "Ổn định, tích lũy lâu dài", "score": 8},
                {"pair": "82", "name": "Sinh Khí", "meaning": "Tăng trưởng bền vững", "score": 8.5}
            ])
        elif "cá nhân" in purpose_lower or "tiêu dùng" in purpose_lower:
            suggested_pairs.extend([
                {"pair": "46", "name": "Thiên Y", "meaning": "Thuận lợi cho chi tiêu cá nhân", "score": 7.5},
                {"pair": "64", "name": "Thiên Y", "meaning": "Thuận lợi cho chi tiêu cá nhân", "score": 7.5},
                {"pair": "19", "name": "Đường Quan", "meaning": "Tốt cho quản lý tài chính cá nhân", "score": 8}
            ])
        else:
            # Mục đích khác, đề xuất các cặp số tốt chung
            suggested_pairs.extend([
                {"pair": "38", "name": "Phát Tài", "meaning": "Tốt cho tài chính", "score": 9},
                {"pair": "28", "name": "Sinh Khí", "meaning": "Tốt cho phát triển", "score": 8.5},
                {"pair": "19", "name": "Đường Quan", "meaning": "Tốt cho quản lý", "score": 8}
            ])
        
        # Nếu người dùng có số ưa thích, kiểm tra và điều chỉnh
        if request.preferred_digits:
            for digit in request.preferred_digits:
                pairs_with_digit = [pair for pair in self.number_pairs_meaning.keys() 
                                if digit in pair and self.number_pairs_meaning[pair]["score"] >= 7]
                
                if pairs_with_digit:
                    best_pair = max(pairs_with_digit, 
                                    key=lambda p: self.number_pairs_meaning[p]["score"])
                    
                    suggested_pairs.append({
                        "pair": best_pair,
                        "name": self.number_pairs_meaning[best_pair]["name"],
                        "meaning": self.number_pairs_meaning[best_pair]["meaning"],
                        "score": self.number_pairs_meaning[best_pair]["score"]
                    })
        
        # Sắp xếp theo điểm cao nhất
        suggested_pairs.sort(key=lambda x: x["score"], reverse=True)
        
        # Lọc ra các cặp unique
        unique_pairs = []
        seen_pairs = set()
        for pair in suggested_pairs:
            if pair["pair"] not in seen_pairs:
                seen_pairs.add(pair["pair"])
                unique_pairs.append(pair)
        
        return {
            "purpose": request.purpose,
            "bank_name": request.bank_name,
            "suggested_pairs": unique_pairs[:5],  # Trả về 5 cặp số tốt nhất
            "recommendations": [
                "Số tài khoản ngân hàng nên kết thúc bằng một trong các cặp số đề xuất",
                "Nếu có thể, nên chọn số tài khoản có nhiều cặp số tốt liên tiếp",
                "Tránh các cặp số Tuyệt Mệnh (47, 74) trong số tài khoản"
            ]
        }
    
    def generate_password(self, request: PasswordRequest) -> Dict[str, Any]:
        """
        Tạo mật khẩu theo phong thủy số học
        
        Args:
            request (PasswordRequest): Yêu cầu tạo mật khẩu
            
        Returns:
            Dict[str, Any]: Mật khẩu được tạo kèm phân tích
        """
        self.logger.info(f"Tạo mật khẩu cho mục đích: {request.purpose}")
        
        import random
        import string
        
        # Các cặp số tốt theo phong thủy
        good_pairs = [pair for pair, info in self.number_pairs_meaning.items() 
                    if info["score"] >= 7]
        
        # Các chữ số riêng lẻ tốt
        good_digits = [digit for digit, info in self.single_number_meaning.items() 
                     if info["score"] >= 7]
        
        # Sinh mật khẩu
        password_length = max(request.min_length, 8)
        
        # Tạo base password từ từ khóa người dùng nếu có
        base_password = ""
        if request.keywords:
            for keyword in request.keywords:
                if len(keyword) >= 3:
                    base_password += keyword[:3]
            
            # Chuẩn hóa base password
            base_password = base_password.lower()
            if len(base_password) > password_length // 2:
                base_password = base_password[:password_length // 2]
        
        # Thêm các cặp số tốt
        digits_to_add = ""
        for _ in range(2):  # Thêm 2 cặp số tốt
            digits_to_add += random.choice(good_pairs)
        
        # Tính cần thêm bao nhiêu ký tự nữa
        remaining_chars = password_length - len(base_password) - len(digits_to_add)
        
        # Thêm các ký tự đặc biệt nếu cần
        special_chars = ""
        if request.require_special_chars and remaining_chars > 0:
            special_chars = random.choice("!@#$%^&*")
            remaining_chars -= 1
        
        # Thêm các ký tự ngẫu nhiên cho đủ độ dài
        random_chars = ""
        if remaining_chars > 0:
            random_chars = ''.join(random.choice(string.ascii_letters) 
                                  for _ in range(remaining_chars))
        
        # Kết hợp các phần và xáo trộn
        password_parts = list(base_password + digits_to_add + special_chars + random_chars)
        random.shuffle(password_parts)
        password = ''.join(password_parts)
        
        # Đảm bảo mật khẩu có đủ các yêu cầu
        if request.require_numbers and not any(c.isdigit() for c in password):
            # Thay thế một ký tự ngẫu nhiên bằng số
            replace_index = random.randint(0, len(password) - 1)
            password_list = list(password)
            password_list[replace_index] = random.choice(good_digits)
            password = ''.join(password_list)
        
        if request.require_special_chars and not any(c in string.punctuation for c in password):
            # Thay thế một ký tự ngẫu nhiên bằng ký tự đặc biệt
            replace_index = random.randint(0, len(password) - 1)
            password_list = list(password)
            password_list[replace_index] = random.choice("!@#$%^&*")
            password = ''.join(password_list)
        
        # Phân tích phong thủy của mật khẩu
        feng_shui_analysis = self._analyze_password_fengshui(password)
        
        return {
            "password": password,
            "strength": self._evaluate_password_strength(password),
            "feng_shui_analysis": feng_shui_analysis,
            "recommendation": "Mật khẩu này kết hợp các nguyên tắc bảo mật và phong thủy số học."
        }
    
    def _analyze_password_fengshui(self, password: str) -> Dict[str, Any]:
        """
        Phân tích mật khẩu theo phong thủy
        
        Args:
            password (str): Mật khẩu cần phân tích
            
        Returns:
            Dict[str, Any]: Kết quả phân tích
        """
        # Tách các số trong mật khẩu
        digits = ''.join(c for c in password if c.isdigit())
        
        # Nếu không có số, trả về phân tích cơ bản
        if not digits:
            return {
                "score": 6.0,
                "analysis": "Mật khẩu không chứa số nên không có giá trị phong thủy số học. Bạn nên thêm các cặp số tốt."
            }
        
        # Phân tích các cặp số
        pairs_analysis = []
        for i in range(len(digits) - 1):
            pair = digits[i:i+2]
            if pair in self.number_pairs_meaning:
                info = self.number_pairs_meaning[pair]
                pairs_analysis.append({
                    "pair": pair,
                    "name": info["name"],
                    "meaning": info["meaning"],
                    "score": info["score"]
                })
        
        # Tính điểm trung bình
        if pairs_analysis:
            avg_score = sum(pair["score"] for pair in pairs_analysis) / len(pairs_analysis)
        else:
            # Nếu chỉ có 1 số, tính điểm dựa trên số đó
            if len(digits) == 1 and digits[0] in self.single_number_meaning:
                avg_score = self.single_number_meaning[digits[0]]["score"]
            else:
                avg_score = 5.0  # Điểm trung bình nếu không đánh giá được
        
        return {
            "score": avg_score,
            "pairs_analysis": pairs_analysis,
            "analysis": "Mật khẩu này có điểm phong thủy số học là {:.1f}/10".format(avg_score)
        }
    
    def _evaluate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Đánh giá độ mạnh của mật khẩu
        
        Args:
            password (str): Mật khẩu cần đánh giá
            
        Returns:
            Dict[str, Any]: Kết quả đánh giá
        """
        import string
        
        # Tính điểm
        score = 0
        
        # Độ dài
        if len(password) >= 12:
            score += 3
        elif len(password) >= 8:
            score += 2
        else:
            score += 1
        
        # Các loại ký tự
        if any(c.isupper() for c in password):
            score += 1
        if any(c.islower() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in string.punctuation for c in password):
            score += 1
        
        # Đánh giá
        if score >= 6:
            strength = "Mạnh"
        elif score >= 4:
            strength = "Trung bình"
        else:
            strength = "Yếu"
        
        return {
            "score": score,
            "max_score": 7,
            "strength": strength
        }

# Instantiate the agent for easy import by root_agent
batcuclinh_so_agent = BatCucLinhSoAgent()