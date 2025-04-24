"""
Phone Number Sub-Agent for BatCucLinhSoAgent
"""

from typing import Any, Dict, List, Optional

# Import base agent, models, logger, tools etc. as needed
# from agents.base_agent import BaseAgent # If inheriting
# Corrected imports (relative paths adjusted)
from shared_libraries.models import PhoneAnalysisRequest
from shared_libraries.logger import get_logger # Assuming logger setup
# Assuming specific analyzers are now used instead of generic number_analyzer
# from tools.batcuclinhso_analysis.number_analyzer import analyze_number_string
from tools.batcuclinhso_analysis.phone_analyzer import analyze_phone_logic # Example name
from tools.batcuclinhso_analysis.fengshui_data import NUMBER_PAIRS_MEANING # For purpose matching

class PhoneNumberAgent:
    """
    Handles analysis and suggestions related to phone numbers.
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        # Potentially initialize tools or data specific to phone analysis here

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
        
        # Use the specific phone analyzer tool
        analysis_result = analyze_phone_logic(phone_number)
        
        # Ý nghĩa 3 số cuối (Placeholder - Implement specific logic here)
        last_three_analysis = "Chưa có phân tích chi tiết cho 3 số cuối"
        
        # Ý nghĩa 5 số cuối (Placeholder - Implement specific logic here)
        last_five_analysis = "Chưa có phân tích chi tiết cho 5 số cuối"
        
        return {
            "phone_number": phone_number,
            "pairs_analysis": analysis_result["pairs_analysis"],
            "total_score": analysis_result["total_score"],
            "luck_level": analysis_result["luck_level"],
            "last_three_digit_analysis": last_three_analysis,
            "last_five_digit_analysis": last_five_analysis,
            "recommendations": self._get_phone_recommendations(analysis_result["total_score"], analysis_result["pairs_analysis"])
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
        has_bad_pair = False
        for pair in pairs_analysis:
            if pair["name"] == "Tuyệt Mệnh":
                recommendations.append(f"Cặp số {pair['pair']} ở vị trí {pair['position']} là Tuyệt Mệnh, nên tránh.")
                has_bad_pair = True
        
        # Nếu điểm cao và không có cặp xấu
        if score >= 8 and not has_bad_pair:
            recommendations.append("Đây là số điện thoại có phong thủy rất tốt, nên giữ lại.")
        elif score >= 7 and not has_bad_pair:
             recommendations.append("Đây là số điện thoại có phong thủy tốt.")

        # Nếu có nhiều cặp số tốt
        good_pairs_count = sum(1 for pair in pairs_analysis if pair["score"] >= 8)
        if good_pairs_count >= 3:
            recommendations.append(f"Số điện thoại có {good_pairs_count} cặp số tốt, rất hợp phong thủy.")
        
        if not recommendations: # Default recommendation if none triggered
            recommendations.append("Đánh giá phong thủy dựa trên điểm số và các cặp số cụ thể.")
            
        return recommendations
        
    def suggest_phone(self, purpose: str, preferred_digits: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Đề xuất số điện thoại phù hợp với mục đích
        
        Args:
            purpose (str): Mục đích sử dụng số điện thoại
            preferred_digits (Optional[List[str]]): Các chữ số ưa thích (Not implemented yet)
            
        Returns:
            List[Dict[str, Any]]: Danh sách số điện thoại đề xuất kèm phân tích
        """
        self.logger.info(f"Đề xuất số điện thoại cho mục đích: {purpose}")
        
        # --- Placeholder for actual generation logic --- 
        # Mẫu số điện thoại (sẽ thay bằng thuật toán thực tế)
        # TODO: Implement actual phone number generation based on purpose/preferred_digits
        sample_phones = [
            "0901234567",
            "0912345678",
            "0923456789",
            "0934567890",
            "0945678901"
        ]
        # --- End Placeholder ---
        
        suggestions = []
        for phone in sample_phones:
            # Use internal analyze_phone (or just analyze_number_string if full analysis not needed)
            analysis_result = analyze_phone_logic(phone)
            feng_shui_score = analysis_result["total_score"]
            
            # Tính mức độ phù hợp với mục đích
            purpose_match_score = self._calculate_purpose_match(phone, purpose)
            
            suggestions.append({
                "phone_number": phone,
                "feng_shui_score": feng_shui_score,
                "purpose_match_score": purpose_match_score,
                "combined_score": round((feng_shui_score + purpose_match_score) / 2, 2),
                "summary": f"Số {phone} điểm phong thủy {feng_shui_score:.1f}/10, phù hợp mục đích {purpose_match_score:.1f}/10."
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
        digits_only = ''.join(filter(str.isdigit, phone))
        if not digits_only:
            return 0.0
            
        # Điểm cơ bản
        score = 5.0 # Start from neutral
        
        # Define purpose keywords and associated good pairs
        purpose_map = {
            ("kinh doanh", "tài chính", "công ty"): ["Phát Tài", "Sinh Khí"],
            ("sự nghiệp", "công việc", "thăng tiến"): ["Đường Quan", "Sinh Khí"],
            ("học tập", "giáo dục", "nghiên cứu"): ["Thiên Y", "Diên Niên"],
            ("tình cảm", "gia đình", "hôn nhân"): ["Khả Ái", "Diên Niên"],
            ("sức khỏe", "y tế"): ["Thiên Y", "Sinh Khí"],
        }
        
        relevant_good_pairs = set()
        for keywords, pairs in purpose_map.items():
            if any(keyword in purpose_lower for keyword in keywords):
                relevant_good_pairs.update(pairs)

        # Kiểm tra từng cặp số có phù hợp với mục đích không
        pair_score_bonus = 0
        num_pairs = 0
        for i in range(len(digits_only) - 1):
            pair = digits_only[i:i+2]
            num_pairs += 1
            if pair in NUMBER_PAIRS_MEANING:
                info = NUMBER_PAIRS_MEANING[pair]
                if info["name"] in relevant_good_pairs:
                    pair_score_bonus += 0.75 # Increase bonus for relevant good pairs
                elif info["name"] == "Tuyệt Mệnh":
                    score -= 1.5 # Increase penalty for bad pairs
        
        # Normalize pair bonus by number of pairs and add to score
        if num_pairs > 0:
             score += (pair_score_bonus / num_pairs) * 5 # Scale bonus to max 5 points
             
        # Check last digit bonus (simplified)
        last_digit = digits_only[-1]
        if any(keyword in purpose_lower for keyword in ("kinh doanh", "tài chính")) and last_digit in ["8", "9"]:
            score += 0.5
        elif any(keyword in purpose_lower for keyword in ("sức khỏe",)) and last_digit in ["6", "9"]:
            score += 0.5

        # Giới hạn điểm (1-10)
        return round(min(max(score, 1.0), 10.0), 1) 