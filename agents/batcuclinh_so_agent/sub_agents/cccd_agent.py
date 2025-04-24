"""
CCCD Sub-Agent for BatCucLinhSoAgent
"""

from typing import Any, Dict, List

from shared_libraries.models import CCCDAnalysisRequest
from shared_libraries.logger import get_logger
# Assuming specific analyzer is used
# from tools.batcuclinhso_analysis.number_analyzer import analyze_number_string
from tools.batcuclinhso_analysis.cccd_analyzer import analyze_cccd_logic # Example name
# No direct data import needed if only using analyzer

class CCCDAgent:
    """
    Handles analysis related to CCCD numbers.
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def analyze_cccd(self, request: CCCDAnalysisRequest) -> Dict[str, Any]:
        """
        Phân tích 6 số cuối của CCCD theo nguyên lý Bát Cực Linh Số
        
        Args:
            request (CCCDAnalysisRequest): Yêu cầu phân tích 6 số cuối CCCD
            
        Returns:
            Dict[str, Any]: Kết quả phân tích chi tiết
        """
        last_digits = request.cccd_last_digits
        # Basic validation
        if not last_digits or not last_digits.isdigit() or len(last_digits) != 6:
             self.logger.warning(f"Invalid CCCD last digits format: {last_digits}")
             # Return an error structure or raise an exception
             return {
                 "error": "Định dạng 6 số cuối CCCD không hợp lệ.",
                 "cccd_last_digits": last_digits,
                 "pairs_analysis": [],
                 "total_score": 0,
                 "luck_level": "Không xác định",
                 "overall_meaning": "Không thể phân tích do định dạng không hợp lệ."
             }
             
        self.logger.info(f"Phân tích CCCD: {last_digits}")
        
        # Use the specific cccd analyzer tool
        # analysis_result = analyze_number_string(last_digits) <-- OLD
        analysis_result = analyze_cccd_logic(last_digits) # <-- NEW (example)
        
        # Ý nghĩa tổng thể
        overall_meaning = self._get_cccd_overall_meaning(analysis_result["pairs_analysis"], analysis_result["total_score"])
        
        return {
            "cccd_last_digits": last_digits,
            "pairs_analysis": analysis_result["pairs_analysis"],
            "total_score": analysis_result["total_score"],
            "luck_level": analysis_result["luck_level"],
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
        if not pairs_analysis:
            return "Không thể đưa ra ý nghĩa tổng thể do thiếu dữ liệu phân tích."
            
        # Tìm cặp số có điểm cao nhất và thấp nhất
        # Handle empty list case for max/min
        try:
            max_pair = max(pairs_analysis, key=lambda x: x["score"])
            min_pair = min(pairs_analysis, key=lambda x: x["score"])
        except ValueError: # If pairs_analysis is empty
             return "Không thể xác định cặp số tốt nhất/kém nhất."

        if score >= 8:
            return f"6 số cuối CCCD ({max_pair['pair']}...) có phong thủy rất tốt. Đặc biệt, cặp số {max_pair['pair']} ({max_pair['name']}) ở vị trí {max_pair['position']} mang lại nhiều may mắn về {max_pair['meaning'].lower()}."
        elif score >= 7:
            return f"6 số cuối CCCD ({min_pair['pair']}...) có phong thủy tốt. Cặp số {max_pair['pair']} ({max_pair['name']}) là điểm sáng, trong khi cặp số {min_pair['pair']} ({min_pair['name']}) có thể cần lưu ý."
        elif score >= 6:
            return f"6 số cuối CCCD ({max_pair['pair']}...) có phong thủy khá. Có sự cân bằng giữa các cặp số, với cặp số {max_pair['pair']} mang lại ảnh hưởng tích cực."
        elif score >= 5:
            return f"6 số cuối CCCD ({min_pair['pair']}...) có phong thủy trung bình. Cặp số {min_pair['pair']} ({min_pair['name']}) có thể gây ảnh hưởng tiêu cực nên cần lưu ý."
        else:
            return f"6 số cuối CCCD ({min_pair['pair']}...) có phong thủy kém. Đặc biệt cặp số {min_pair['pair']} ({min_pair['name']}) ở vị trí {min_pair['position']} cần được lưu ý." 