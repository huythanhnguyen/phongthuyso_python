"""
Root Agent Module

Cung cấp RootAgent - agent chính của hệ thống, điều phối các yêu cầu đến các agent chuyên biệt.
"""

from typing import Dict, Any, Optional

from phongthuyso_python.agents.agent_types import AgentType
from phongthuyso_python.agents.base_agent import BaseAgent


class RootAgent(BaseAgent):
    """
    Root Agent - Agent chính của hệ thống
    
    Điều phối các yêu cầu từ người dùng đến các agent chuyên biệt.
    """
    
    def __init__(self, name: str, agent_type: AgentType):
        """
        Khởi tạo RootAgent
        
        Args:
            name (str): Tên của agent
            agent_type (AgentType): Loại agent
        """
        super().__init__(name, agent_type)
        self.agents = {}
    
    def register_agent(self, agent):
        """
        Đăng ký một agent với RootAgent
        
        Args:
            agent (BaseAgent): Agent cần đăng ký
        """
        self.agents[agent.agent_type] = agent
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Xử lý yêu cầu từ người dùng
        
        Args:
            request (Dict[str, Any]): Yêu cầu từ người dùng
            
        Returns:
            Dict[str, Any]: Kết quả xử lý
        """
        message = request.get("message", "")
        context = request.get("context", {})
        
        # Phân tích yêu cầu để xác định agent phù hợp
        agent_type = self._determine_agent_type(message, context)
        
        if agent_type and agent_type in self.agents:
            # Chuyển yêu cầu đến agent phù hợp
            return await self.agents[agent_type].handle_request(request)
        
        # Xử lý mặc định nếu không tìm thấy agent phù hợp
        response = self.process_message(message, context)
        
        return {
            "agent": self.name,
            "status": "success",
            "content": response,
            "metadata": {}
        }
    
    def process_message(self, message: str, context: Dict[str, Any]) -> str:
        """
        Xử lý tin nhắn từ người dùng
        
        Args:
            message (str): Tin nhắn của người dùng
            context (Dict[str, Any]): Ngữ cảnh của tin nhắn
            
        Returns:
            str: Phản hồi của agent
        """
        return f"Xin chào! Tôi là {self.name}. Bạn có thể hỏi tôi về phong thủy số."
    
    def _determine_agent_type(self, message: str, context: Dict[str, Any]) -> Optional[AgentType]:
        """
        Xác định loại agent phù hợp để xử lý yêu cầu
        
        Args:
            message (str): Tin nhắn của người dùng
            context (Dict[str, Any]): Ngữ cảnh của tin nhắn
            
        Returns:
            Optional[AgentType]: Loại agent phù hợp hoặc None nếu không xác định được
        """
        # Logic đơn giản: nếu message là số điện thoại, sử dụng BatCucLinhSoAgent
        if message.isdigit() or (message.startswith('0') and message[1:].isdigit()):
            return AgentType.BAT_CUC_LINH_SO
        
        # Các trường hợp khác, sử dụng mặc định
        return None


# Tạo singleton instance
root_agent = RootAgent("Root Agent", AgentType.ROOT) 