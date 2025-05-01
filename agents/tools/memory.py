"""
Memory Tool

Công cụ lưu trữ và truy xuất thông tin phân tích trước đó.
"""

from typing import Dict, Any, Optional, List
import logging
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import Agent
from datetime import datetime
from shared_libraries.logger import get_logger

# Khởi tạo logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lưu trữ dữ liệu trong bộ nhớ
_memory: Dict[str, Any] = {
    "phone_analysis": {},
    "cccd_analysis": {},
    "bank_account_analysis": {},
    "password_analysis": {},
    "user_preferences": {},
    "conversation_history": []
}

def memorize(key: str, value: Any) -> Dict[str, Any]:
    """
    Lưu trữ thông tin vào bộ nhớ.
    
    Args:
        key: Khóa để lưu trữ dữ liệu.
        value: Giá trị để lưu trữ.
        
    Returns:
        Dict với status và message.
    """
    logger.info(f"Memorizing {key}: {value}")
    _memory[key] = value
    return {"status": "success", "message": f"Đã ghi nhớ {key}"}

def recall(key: str) -> Dict[str, Any]:
    """
    Truy xuất thông tin từ bộ nhớ.
    
    Args:
        key: Khóa để truy xuất.
        
    Returns:
        Dict với status và data hoặc error_message.
    """
    logger.info(f"Recalling {key}")
    if key in _memory:
        return {"status": "success", "data": _memory[key]}
    return {"status": "error", "error_message": f"Không tìm thấy thông tin cho {key}"}

def record_conversation(user_input: str, agent_response: str) -> Dict[str, Any]:
    """
    Ghi lại một lượt hội thoại.
    
    Args:
        user_input: Đầu vào từ người dùng.
        agent_response: Phản hồi từ agent.
        
    Returns:
        Dict với status và message.
    """
    logger.info(f"Recording conversation - User: {user_input}")
    _memory["conversation_history"].append({
        "user": user_input,
        "agent": agent_response
    })
    return {"status": "success", "message": "Đã ghi lại hội thoại"}

def get_conversation_history(limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Lấy lịch sử hội thoại.
    
    Args:
        limit: Số lượng lượt hội thoại gần nhất muốn lấy.
        
    Returns:
        Dict với status và history.
    """
    logger.info(f"Getting conversation history (limit={limit})")
    history = _memory["conversation_history"]
    if limit is not None and limit > 0:
        history = history[-limit:]
    return {"status": "success", "history": history}

def _load_precreated_itinerary():
    """
    Callback để tải itinerary đã tạo trước đó.
    Ở đây chỉ làm giả cho phù hợp với ADK.
    """
    # Trong hệ thống thật, có thể tải từ database
    return {}

# Tạo các FunctionTool thay vì dùng Agent
from google.adk.tools import FunctionTool

memorize_tool = FunctionTool(func=memorize)
recall_tool = FunctionTool(func=recall)
record_conversation_tool = FunctionTool(func=record_conversation)
get_conversation_history_tool = FunctionTool(func=get_conversation_history) 