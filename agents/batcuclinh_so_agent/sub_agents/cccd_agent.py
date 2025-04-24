"""
CCCD Sub-Agent for BatCucLinhSoAgent
"""

from typing import Any, Dict, List

from shared_libraries.models import CCCDAnalysisRequest
from shared_libraries.logger import get_logger
# Assuming specific analyzer is used
# from tools.batcuclinhso_analysis.number_analyzer import analyze_number_string
from tools.batcuclinhso_analysis.cccd_analyzer import cccd_analyzer # Tên hàm chính xác
# No direct data import needed if only using analyzer

class CCCDAgent:
    """
    Handles analysis related to CCCD numbers.
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    async def analyze_cccd(self, request: CCCDAnalysisRequest) -> Dict[str, Any]:
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
        analysis_result = cccd_analyzer(last_digits) # <-- Sử dụng tên hàm chính xác
        
        # Thêm các trường cần thiết để tương thích với kết quả mong đợi
        if "analysis" in analysis_result:
            analysis_result["pairs_analysis"] = analysis_result["analysis"]
        if "total_score" not in analysis_result:
            analysis_result["total_score"] = 7.0  # Điểm mặc định
        if "luck_level" not in analysis_result:
            analysis_result["luck_level"] = "Tốt"  # Cấp độ may mắn mặc định
        
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
            
        # Log để gỡ lỗi
        self.logger.debug(f"Cấu trúc dữ liệu pairs_analysis: {pairs_analysis}")
        
        # Xử lý trường hợp pairs_analysis không phải là danh sách
        if not isinstance(pairs_analysis, list):
            self.logger.warning(f"pairs_analysis không phải là list: {type(pairs_analysis)}")
            return "Không thể đưa ra ý nghĩa tổng thể do định dạng dữ liệu không hợp lệ."
            
        # Xử lý trường hợp danh sách rỗng
        if not pairs_analysis:
            return "Không thể đưa ra ý nghĩa tổng thể do không có dữ liệu phân tích cặp số."
            
        # Tìm cặp số có điểm cao nhất và thấp nhất
        # Xử lý mọi trường hợp cấu trúc dữ liệu có thể có
        try:
            # Hàm hỗ trợ trích xuất điểm số từ phân tích
            def get_score_from_pair(pair):
                if not isinstance(pair, dict):
                    return 0
                # Thử lấy điểm số từ nhiều trường khác nhau
                if 'score' in pair and isinstance(pair['score'], (int, float)):
                    return pair['score']
                elif 'energy' in pair and isinstance(pair['energy'], (int, float)):
                    return pair['energy']
                elif 'value' in pair and isinstance(pair['value'], (int, float)):
                    return pair['value']
                return 0
                
            valid_pairs = [p for p in pairs_analysis if isinstance(p, dict)]
            if not valid_pairs:
                return "Không thể xác định cặp số tốt nhất/kém nhất do định dạng dữ liệu."
                
            max_pair = max(valid_pairs, key=get_score_from_pair)
            min_pair = min(valid_pairs, key=get_score_from_pair)
        except Exception as e:
            self.logger.error(f"Lỗi khi xác định cặp số tốt/kém: {str(e)}")
            return "Không thể xác định cặp số tốt nhất/kém nhất."

        # Lấy thông tin của cặp số với xử lý tất cả các trường hợp trường có thể có
        max_number = max_pair.get("number", max_pair.get("originalPair", max_pair.get("pair", "")))
        max_name = max_pair.get("name", max_pair.get("tinh", max_pair.get("element", "")))
        max_meaning = max_pair.get("meaning", max_pair.get("description", max_pair.get("interpretation", "")))
        max_position = max_pair.get("position", "")
        
        min_number = min_pair.get("number", min_pair.get("originalPair", min_pair.get("pair", "")))
        min_name = min_pair.get("name", min_pair.get("tinh", min_pair.get("element", "")))
        min_meaning = min_pair.get("meaning", min_pair.get("description", min_pair.get("interpretation", "")))

        # Đảm bảo có giá trị mặc định nếu không có thông tin
        if not max_number: max_number = "không xác định"
        if not max_name: max_name = "không xác định"
        if not min_number: min_number = "không xác định"
        if not min_name: min_name = "không xác định"

        if score >= 8:
            return f"6 số cuối CCCD có phong thủy rất tốt. Đặc biệt, cặp số {max_number} ({max_name}) mang lại nhiều may mắn về {max_meaning.lower() if max_meaning else 'các lĩnh vực'}."
        elif score >= 7:
            return f"6 số cuối CCCD có phong thủy tốt. Cặp số {max_number} ({max_name}) là điểm sáng, trong khi cặp số {min_number} ({min_name}) có thể cần lưu ý."
        elif score >= 6:
            return f"6 số cuối CCCD có phong thủy khá. Có sự cân bằng giữa các cặp số, với cặp số {max_number} mang lại ảnh hưởng tích cực."
        elif score >= 5:
            return f"6 số cuối CCCD có phong thủy trung bình. Cặp số {min_number} ({min_name}) có thể gây ảnh hưởng tiêu cực nên cần lưu ý."
        else:
            return f"6 số cuối CCCD có phong thủy kém. Đặc biệt cặp số {min_number} ({min_name}) cần được lưu ý." 