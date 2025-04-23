"""
Agent Router Tool - Công cụ chuyển hướng yêu cầu đến agent phù hợp

Tool này chuyển hướng yêu cầu từ Root Agent đến các Expert Agent
phù hợp dựa trên phân tích ý định và context.
"""

import logging
from typing import Dict, Any, List, Optional
from enum import Enum

# Google ADK imports
from google.adk.tools import FunctionTool

# Local imports
from python_adk.agents.root_agent.tools.intent_classifier import AgentType


class AgentRouter(FunctionTool):
    """Tool chuyển hướng yêu cầu đến agent phù hợp"""
    
    def __init__(self):
        """Khởi tạo Agent Router Tool"""
        # Define the route_to_agent_function
        def route_to_agent_function(agent_type: str, request: str, session_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
            """Chuyển hướng yêu cầu đến agent phù hợp
            
            Args:
                agent_type: Loại agent cần chuyển hướng đến
                request: Nội dung yêu cầu cần chuyển hướng
                session_id: ID của phiên trò chuyện
                context: Context của cuộc trò chuyện
                
            Returns:
                Dict[str, Any]: Kết quả chuyển hướng yêu cầu, bao gồm:
                    success: Trạng thái thành công
                    agent_type: Loại agent đã chuyển hướng đến
                    response: Phản hồi từ agent (nếu có)
                    error: Thông báo lỗi nếu có
            """
            # Validate agent_type
            try:
                agent_type_enum = AgentType(agent_type)
            except ValueError:
                return {
                    "success": False,
                    "agent_type": agent_type,
                    "response": f"Loại agent không hợp lệ: {agent_type}",
                    "error": f"Invalid agent type: {agent_type}"
                }
            
            # Route the request
            return self.route_to_agent(agent_type_enum, request, session_id, context)
        
        # Initialize FunctionTool with the function
        super().__init__(func=route_to_agent_function)
        
        # Khởi tạo logger
        self.logger = logging.getLogger("AgentRouter")
        
        # Các agent đã đăng ký (sẽ được cập nhật bởi Root Agent)
        self.registered_agents = {}
    
    def register_agent(self, agent_type: AgentType, agent: Any) -> None:
        """Đăng ký agent với router
        
        Args:
            agent_type: Loại agent
            agent: Instance của agent
        """
        self.registered_agents[agent_type] = agent
        self.logger.info(f"Đã đăng ký {agent_type} Agent với Router")
    
    async def route_to_agent(self, agent_type: AgentType, request: str, session_id: str, 
                          context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Chuyển hướng yêu cầu đến agent phù hợp
        
        Args:
            agent_type: Loại agent
            request: Nội dung yêu cầu
            session_id: ID phiên trò chuyện
            context: Context bổ sung (optional)
            
        Returns:
            Dict[str, Any]: Kết quả từ agent
        """
        self.logger.info(f"Chuyển hướng yêu cầu đến {agent_type} Agent")
        
        # Kiểm tra xem agent đã được đăng ký chưa
        if agent_type not in self.registered_agents:
            error_msg = f"Agent loại {agent_type} chưa được đăng ký"
            self.logger.error(error_msg)
            return {
                "success": False,
                "agent_type": agent_type,
                "response": f"Rất tiếc, hiện tại không thể xử lý yêu cầu này vì {error_msg}. Vui lòng thử lại sau.",
                "error": error_msg
            }
        
        try:
            # Lấy agent từ registry
            agent = self.registered_agents[agent_type]
            
            # Xử lý yêu cầu bằng agent
            response = await agent.process_message(request)
            
            return {
                "success": True,
                "agent_type": agent_type,
                "response": response,
                "error": None
            }
        except Exception as e:
            error_msg = f"Lỗi khi xử lý yêu cầu với {agent_type} Agent: {str(e)}"
            self.logger.error(error_msg)
            return {
                "success": False,
                "agent_type": agent_type,
                "response": f"Rất tiếc, đã xảy ra lỗi khi xử lý yêu cầu của bạn. Vui lòng thử lại sau.",
                "error": error_msg
            }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số
            
        Returns:
            Dict[str, Any]: Kết quả routing
        """
        agent_type = kwargs.get("agent_type")
        request = kwargs.get("request")
        session_id = kwargs.get("session_id")
        context = kwargs.get("context", {})
        
        # Validate agent_type
        try:
            agent_type_enum = AgentType(agent_type)
        except ValueError:
            return {
                "success": False,
                "agent_type": agent_type,
                "response": f"Loại agent không hợp lệ: {agent_type}",
                "error": f"Invalid agent type: {agent_type}"
            }
        
        # Chuyển hướng yêu cầu
        return await self.route_to_agent(agent_type_enum, request, session_id, context) 