"""
Phone Number Sub-Agent for BatCucLinhSoAgent sử dụng Model Context Protocol (MCP)
"""

from typing import Any, Dict, List, Optional, Tuple
import asyncio
import logging
from contextlib import AsyncExitStack

from shared_libraries.models import PhoneAnalysisRequest
from shared_libraries.logger import get_logger

# Import MCP tools
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

class PhoneNumberAgent:
    """
    Xử lý phân tích và đề xuất liên quan đến số điện thoại 
    sử dụng MCP tools từ thư mục batcuclinhso_analysis
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.mcp_tools = None
        self.exit_stack = None
        self.initialized = False
        
    async def _get_mcp_tools_async(self) -> Tuple[List[Any], AsyncExitStack]:
        """
        Khởi tạo và trả về danh sách MCP tools và exit stack
        Theo hướng dẫn MCP chính thức: tools và exit_stack nên được tạo cùng nhau
        """
        self.logger.info("Khởi tạo MCP toolset cho phân tích số điện thoại")
        
        # Đúng theo hướng dẫn, tạo stack và lấy tools trong cùng một hàm
        tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command='python',
                args=[
                    '-m', 'tools.batcuclinhso_analysis.phone_analyzer', 
                ],
            )
        )
        
        self.logger.info(f"Đã khởi tạo {len(tools)} MCP tools cho phân tích số điện thoại")
        return tools, exit_stack

    async def initialize(self):
        """
        Khởi tạo kết nối đến MCP server phân tích số điện thoại
        Tuân thủ theo mẫu trong tài liệu MCP
        """
        if self.initialized:
            self.logger.info("MCP tools đã được khởi tạo trước đó")
            return
            
        try:
            # Tạo mới exit stack
            self.exit_stack = AsyncExitStack()
            
            # Lấy MCP tools và quản lý exit stack của chúng
            tools, tools_exit_stack = await self._get_mcp_tools_async()
            
            # Đăng ký exit stack của tools trong exit stack chính
            await self.exit_stack.enter_async_context(tools_exit_stack)
            
            # Lưu lại tools để sử dụng sau này
            self.mcp_tools = tools
            self.initialized = True
            
            self.logger.info(f"Khởi tạo thành công MCP tools: {len(tools)} công cụ sẵn sàng")
        except Exception as e:
            self.logger.error(f"Lỗi khi khởi tạo MCP tools: {str(e)}")
            if self.exit_stack:
                await self.exit_stack.aclose()
                self.exit_stack = None
            raise e

    async def cleanup(self):
        """
        Đóng kết nối đến MCP server
        Đảm bảo giải phóng tài nguyên
        """
        if self.exit_stack:
            self.logger.info("Đang đóng kết nối MCP server và giải phóng tài nguyên...")
            await self.exit_stack.aclose()
            self.exit_stack = None
            self.mcp_tools = None
            self.initialized = False
            self.logger.info("Đã đóng kết nối MCP server thành công")

    async def analyze_phone(self, request: PhoneAnalysisRequest) -> Dict[str, Any]:
        """
        Phân tích số điện thoại theo nguyên lý Bát Cực Linh Số sử dụng MCP tools
        
        Args:
            request (PhoneAnalysisRequest): Yêu cầu phân tích số điện thoại
            
        Returns:
            Dict[str, Any]: Kết quả phân tích chi tiết
        """
        phone_number = request.phone_number
        self.logger.info(f"Phân tích số điện thoại: {phone_number}")
        
        # Đảm bảo MCP tools đã được khởi tạo
        if not self.initialized:
            await self.initialize()
            
        if not self.mcp_tools:
            self.logger.error("MCP tools chưa được khởi tạo thành công")
            return self._get_default_analysis(phone_number)
        
        try:
            # Tìm công cụ phân tích số điện thoại trong danh sách MCP tools
            phone_analyzer_tool = next(
                (tool for tool in self.mcp_tools if tool.name == "analyze_phone_number"), 
                None
            )
            
            if not phone_analyzer_tool:
                self.logger.error("Không tìm thấy công cụ analyze_phone_number trong MCP tools")
                return self._get_default_analysis(phone_number)
                
            # Gọi công cụ MCP để phân tích số điện thoại
            analysis_result = await phone_analyzer_tool.invoke(phone_number=phone_number)
            
            # Xử lý phân tích 3 số cuối sử dụng MCP tool nếu có
            last_three_digits_tool = next(
                (tool for tool in self.mcp_tools if tool.name == "analyze_last_three_digits"), 
                None
            )
            
            if last_three_digits_tool:
                last_three_analysis = await last_three_digits_tool.invoke(phone_number=phone_number)
            else:
                last_three_analysis = "Chưa có phân tích chi tiết cho 3 số cuối"
                
            # Xử lý phân tích 5 số cuối sử dụng MCP tool nếu có  
            last_five_digits_tool = next(
                (tool for tool in self.mcp_tools if tool.name == "analyze_last_five_digits"), 
                None
            )
            
            if last_five_digits_tool:
                last_five_analysis = await last_five_digits_tool.invoke(phone_number=phone_number)
            else:
                last_five_analysis = "Chưa có phân tích chi tiết cho 5 số cuối"
            
            # Đảm bảo các trường cần thiết tồn tại
            if "total_score" not in analysis_result:
                analysis_result["total_score"] = 7.5  # Điểm mặc định
                
            if "luck_level" not in analysis_result:
                analysis_result["luck_level"] = "Tốt"  # Cấp độ may mắn mặc định
                
            if "pairs_analysis" not in analysis_result and "analysis" in analysis_result:
                analysis_result["pairs_analysis"] = analysis_result["analysis"]
            
            # Thêm trường 'pair' cho mỗi phần tử trong pairs_analysis
            if "pairs_analysis" in analysis_result:
                for pair_item in analysis_result["pairs_analysis"]:
                    # Sử dụng number hoặc originalPair làm trường pair
                    if "number" in pair_item:
                        pair_item["pair"] = pair_item["number"]
                    elif "originalPair" in pair_item:
                        pair_item["pair"] = pair_item["originalPair"]
                    else:
                        pair_item["pair"] = "N/A"  # Giá trị mặc định nếu không có thông tin
            
            # Lấy khuyến nghị từ MCP tool nếu có
            recommendation_tool = next(
                (tool for tool in self.mcp_tools if tool.name == "get_phone_recommendations"), 
                None
            )
            
            if recommendation_tool:
                recommendations = await recommendation_tool.invoke(
                    score=analysis_result.get("total_score", 7.5),
                    pairs_analysis=analysis_result.get("pairs_analysis", [])
                )
            else:
                # Fallback nếu không có MCP tool tương ứng
                recommendations = [
                    "Đánh giá phong thủy dựa trên điểm số và các cặp số cụ thể.",
                    f"Điểm tổng thể: {analysis_result.get('total_score', 7.5)}/10"
                ]
            
            return {
                "phone_number": phone_number,
                "pairs_analysis": analysis_result.get("pairs_analysis", []),
                "total_score": analysis_result.get("total_score", 7.5),
                "luck_level": analysis_result.get("luck_level", "Tốt"),
                "last_three_digit_analysis": last_three_analysis,
                "last_five_digit_analysis": last_five_analysis,
                "recommendations": recommendations
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi khi phân tích số điện thoại: {str(e)}")
            # Trả về giá trị mặc định nếu có lỗi
            return self._get_default_analysis(phone_number)

    def _get_default_analysis(self, phone_number: str) -> Dict[str, Any]:
        """Trả về phân tích mặc định nếu có lỗi"""
        return {
            "phone_number": phone_number,
            "pairs_analysis": [],
            "total_score": 5.0,
            "luck_level": "Trung bình",
            "last_three_digit_analysis": "Không thể phân tích",
            "last_five_digit_analysis": "Không thể phân tích",
            "recommendations": ["Không thể đưa ra khuyến nghị do lỗi khi phân tích số điện thoại"]
        }

    async def suggest_phone(self, purpose: str, preferred_digits: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Đề xuất số điện thoại phù hợp với mục đích sử dụng công cụ MCP
        
        Args:
            purpose (str): Mục đích sử dụng số điện thoại
            preferred_digits (Optional[List[str]]): Các chữ số ưa thích
            
        Returns:
            List[Dict[str, Any]]: Danh sách số điện thoại đề xuất kèm phân tích
        """
        self.logger.info(f"Đề xuất số điện thoại cho mục đích: {purpose}")
        
        # Đảm bảo MCP tools đã được khởi tạo
        if not self.initialized:
            await self.initialize()
            
        if not self.mcp_tools:
            self.logger.error("MCP tools chưa được khởi tạo thành công")
            return self._get_default_suggestions()
        
        try:
            # Tìm công cụ đề xuất số điện thoại trong danh sách MCP tools
            suggest_phone_tool = next(
                (tool for tool in self.mcp_tools if tool.name == "suggest_phone_numbers"), 
                None
            )
            
            if not suggest_phone_tool:
                self.logger.error("Không tìm thấy công cụ suggest_phone_numbers trong MCP tools")
                return self._get_default_suggestions()
            
            # Gọi công cụ MCP để đề xuất số điện thoại
            suggestions = await suggest_phone_tool.invoke(
                purpose=purpose,
                preferred_digits=preferred_digits if preferred_digits else []
            )
            
            return suggestions[:5]  # Trả về 5 đề xuất tốt nhất
            
        except Exception as e:
            self.logger.error(f"Lỗi khi đề xuất số điện thoại: {str(e)}")
            return self._get_default_suggestions()

    def _get_default_suggestions(self) -> List[Dict[str, Any]]:
        """Trả về đề xuất mặc định nếu có lỗi"""
        # Mẫu số điện thoại (mặc định nếu MCP tool không hoạt động)
        sample_phones = [
            "0901234567",
            "0912345678",
            "0923456789"
        ]
        
        suggestions = []
        for phone in sample_phones:
            suggestions.append({
                "phone_number": phone,
                "feng_shui_score": 7.0,
                "purpose_match_score": 6.0,
                "combined_score": 6.5,
                "summary": f"Số {phone} được đề xuất mặc định do lỗi phân tích."
            })
        
        return suggestions
        
    async def __aenter__(self):
        """Hỗ trợ sử dụng phong cách async with"""
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Đảm bảo dọn dẹp tài nguyên khi kết thúc phiên với with"""
        await self.cleanup() 