"""
Conversation Manager Tool - Công cụ quản lý trò chuyện

Tool này hỗ trợ quản lý lịch sử và luồng trò chuyện giữa người dùng và agent.
"""

import time
import logging
from typing import Dict, Any, List, Optional, Union

# Google ADK imports
from google.adk.tools import FunctionTool


class ConversationManager(FunctionTool):
    """Tool quản lý trò chuyện"""
    
    def __init__(self):
        """Khởi tạo Conversation Manager Tool"""
        # Define the conversation_manager_function
        def conversation_manager_function(action: str, session_id: str, message: Optional[Dict[str, Any]] = None, limit: Optional[int] = None) -> Dict[str, Any]:
            """Quản lý lịch sử và luồng trò chuyện
            
            Args:
                action: Hành động cần thực hiện: add_message, get_history, clear_history
                session_id: ID của phiên trò chuyện
                message: Tin nhắn cần thêm vào lịch sử (chỉ cần khi action=add_message)
                limit: Số lượng tin nhắn tối đa trả về (chỉ cần khi action=get_history)
                
            Returns:
                Dict[str, Any]: Kết quả của hành động, bao gồm:
                    success: Trạng thái thành công
                    history: Lịch sử trò chuyện (nếu có)
                    error: Thông báo lỗi nếu có
            """
            # Validate action
            if action not in ["add_message", "get_history", "clear_history"]:
                return {
                    "success": False,
                    "error": f"Hành động không hợp lệ: {action}"
                }
                
            # Validate message for add_message
            if action == "add_message" and not message:
                return {
                    "success": False,
                    "error": "Thiếu tham số message cho hành động add_message"
                }
                
            # Execute the corresponding action
            if action == "add_message":
                return self.add_message(session_id, message)
            elif action == "get_history":
                return self.get_history(session_id, limit)
            elif action == "clear_history":
                return self.clear_history(session_id)
        
        # Initialize FunctionTool with the function
        super().__init__(func=conversation_manager_function)
        
        # Memory lưu trữ lịch sử trò chuyện theo session
        self.conversation_memory = {}
    
    async def add_message(self, session_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Thêm tin nhắn vào lịch sử
        
        Args:
            session_id: ID của phiên trò chuyện
            message: Tin nhắn cần thêm
            
        Returns:
            Dict[str, Any]: Kết quả thêm tin nhắn
        """
        # Khởi tạo lịch sử cho session nếu chưa có
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = []
        
        # Thêm timestamp nếu chưa có
        if "timestamp" not in message:
            message["timestamp"] = time.time()
        
        # Thêm tin nhắn vào lịch sử
        self.conversation_memory[session_id].append(message)
        
        return {
            "success": True,
            "history": self.conversation_memory[session_id]
        }
    
    async def get_history(self, session_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """Lấy lịch sử trò chuyện
        
        Args:
            session_id: ID của phiên trò chuyện
            limit: Số lượng tin nhắn tối đa trả về
            
        Returns:
            Dict[str, Any]: Lịch sử trò chuyện
        """
        # Kiểm tra xem session có tồn tại không
        if session_id not in self.conversation_memory:
            return {
                "success": True,
                "history": []
            }
        
        # Lấy lịch sử
        history = self.conversation_memory[session_id]
        
        # Giới hạn số lượng tin nhắn nếu có yêu cầu
        if limit and limit > 0:
            history = history[-limit:]
        
        return {
            "success": True,
            "history": history
        }
    
    async def clear_history(self, session_id: str) -> Dict[str, Any]:
        """Xóa lịch sử trò chuyện
        
        Args:
            session_id: ID của phiên trò chuyện
            
        Returns:
            Dict[str, Any]: Kết quả xóa lịch sử
        """
        # Xóa lịch sử
        if session_id in self.conversation_memory:
            self.conversation_memory[session_id] = []
        
        return {
            "success": True,
            "history": []
        }
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số
            
        Returns:
            Dict[str, Any]: Kết quả của hành động
        """
        action = kwargs.get("action")
        session_id = kwargs.get("session_id")
        
        if not action:
            return {
                "success": False,
                "error": "Thiếu tham số action"
            }
        
        if not session_id:
            return {
                "success": False,
                "error": "Thiếu tham số session_id"
            }
        
        # Thực hiện hành động tương ứng
        if action == "add_message":
            message = kwargs.get("message")
            if not message:
                return {
                    "success": False,
                    "error": "Thiếu tham số message cho hành động add_message"
                }
            return await self.add_message(session_id, message)
        
        elif action == "get_history":
            limit = kwargs.get("limit")
            return await self.get_history(session_id, limit)
        
        elif action == "clear_history":
            return await self.clear_history(session_id)
        
        else:
            return {
                "success": False,
                "error": f"Hành động không hợp lệ: {action}"
            } 