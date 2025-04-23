"""
Context Tracker Tool - Công cụ theo dõi ngữ cảnh hội thoại

Tool này quản lý và theo dõi ngữ cảnh (context) của cuộc trò chuyện,
lưu trữ và truy xuất thông tin quan trọng giữa các lượt tương tác.
"""

from typing import Dict, Any, List, Optional
import time
import json
import logging

# Google ADK imports
from google.adk.tools import FunctionTool


class ContextTracker(FunctionTool):
    """Tool theo dõi ngữ cảnh hội thoại"""
    
    def __init__(self):
        """Khởi tạo Context Tracker Tool"""
        # Define the function for FunctionTool signature
        def context_tracker_function(
            action: str,
            session_id: str,
            context_data: Optional[Dict[str, Any]] = None,
            key: Optional[str] = None
        ) -> Dict[str, Any]:
            """
            Theo dõi ngữ cảnh (context) của cuộc trò chuyện.

            Args:
                action: Hành động cần thực hiện: update, get, clear.
                session_id: ID của phiên trò chuyện.
                context_data: Dữ liệu context cần cập nhật (cho action=update).
                key: Khóa cụ thể trong context (cho action=get).
            Returns:
                Dict[str, Any]: Kết quả của hành động.
            """
            if action == "update":
                return self.update_context(session_id, context_data)
            elif action == "get":
                return self.get_context(session_id, key)
            elif action == "clear":
                return self.clear_context(session_id)
            else:
                return {"success": False, "error": f"Hành động không hợp lệ: {action}"}

        # Initialize FunctionTool with only the function
        super().__init__(func=context_tracker_function)
        
        # Lưu trữ context theo session
        self.contexts = {}
        self.logger = logging.getLogger("ContextTracker")
    
    async def update_context(self, session_id: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cập nhật context cho một phiên
        
        Args:
            session_id: ID của phiên trò chuyện
            context_data: Dữ liệu context cần cập nhật
            
        Returns:
            Dict[str, Any]: Kết quả cập nhật
        """
        # Khởi tạo context cho session nếu chưa có
        if session_id not in self.contexts:
            self.contexts[session_id] = {
                "last_updated": time.time()
            }
        
        # Cập nhật context với dữ liệu mới
        self.contexts[session_id].update(context_data)
        self.contexts[session_id]["last_updated"] = time.time()
        
        self.logger.debug(f"Cập nhật context cho session {session_id}")
        
        return {
            "success": True,
            "context": self.contexts[session_id]
        }
    
    async def get_context(self, session_id: str, key: Optional[str] = None) -> Dict[str, Any]:
        """Lấy context của một phiên
        
        Args:
            session_id: ID của phiên trò chuyện
            key: Khóa cụ thể trong context cần lấy (optional)
            
        Returns:
            Dict[str, Any]: Context
        """
        # Kiểm tra xem session có tồn tại không
        if session_id not in self.contexts:
            return {
                "success": True,
                "context": {}
            }
        
        # Lấy toàn bộ context hoặc giá trị cụ thể
        if key:
            value = self.contexts[session_id].get(key)
            return {
                "success": True,
                "context": {key: value}
            }
        else:
            return {
                "success": True,
                "context": self.contexts[session_id]
            }
    
    async def clear_context(self, session_id: str) -> Dict[str, Any]:
        """Xóa context của một phiên
        
        Args:
            session_id: ID của phiên trò chuyện
            
        Returns:
            Dict[str, Any]: Kết quả xóa
        """
        # Xóa context
        if session_id in self.contexts:
            self.contexts[session_id] = {
                "last_updated": time.time()
            }
        
        return {
            "success": True,
            "context": {}
        }