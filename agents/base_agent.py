"""
Base Agent Module

Module cung cấp lớp cơ sở cho tất cả các agent trong hệ thống.
"""

import abc
from typing import Any, Dict, List, Optional

from .agent_types import AgentType


class BaseAgent:
    """
    Lớp cơ sở cho tất cả các agent chuyên biệt trong hệ thống Phong Thủy Số.
    """

    def __init__(
        self,
        name: str,
        agent_type: Optional[AgentType] = None,
        model_name: Optional[str] = None,
        instruction: Optional[str] = None,
    ):
        """
        Khởi tạo BaseAgent
        
        Args:
            name (str): Tên của agent
            agent_type (AgentType, optional): Loại agent
            model_name (str, optional): Tên model để sử dụng
            instruction (str, optional): Hướng dẫn hệ thống cho model
        """
        self.name = name
        self.agent_type = agent_type
        self.model_name = model_name
        self.instruction = instruction
        
        # Các thuộc tính mở rộng 
        self.current_context: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
    
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
        
        # Xử lý yêu cầu
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
        # Đây là phương thức cơ bản, cần được ghi đè ở các lớp con
        return f"Agent {self.name} đã nhận tin nhắn: {message}"
    
    def update_context(self, key: str, value: Any) -> None:
        """
        Cập nhật context của agent
        
        Args:
            key (str): Khóa của context
            value (Any): Giá trị cần lưu
        """
        self.current_context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """
        Lấy giá trị từ context
        
        Args:
            key (str): Khóa cần lấy
            default (Any, optional): Giá trị mặc định nếu không tìm thấy
            
        Returns:
            Any: Giá trị tương ứng với khóa hoặc giá trị mặc định
        """
        return self.current_context.get(key, default)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}" 