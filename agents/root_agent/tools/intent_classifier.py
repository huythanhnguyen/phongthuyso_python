"""
Intent Classifier Tool - Công cụ phân loại ý định của người dùng

Tool này phân tích nội dung tin nhắn của người dùng để xác định 
agent phù hợp để xử lý yêu cầu.
"""

import re
from typing import Dict, Any, List
from enum import Enum

# Google ADK imports
from google.adk.tools import FunctionTool


class AgentType(str, Enum):
    """Các loại agent được hỗ trợ trong hệ thống"""
    BAT_CUC_LINH_SO = "batcuclinh_so"
    PAYMENT = "payment"
    USER = "user"
    UNKNOWN = "unknown"


class IntentClassifier(FunctionTool):
    """Tool phân loại ý định người dùng"""
    
    def __init__(self):
        """Khởi tạo Intent Classifier Tool"""
        # Define the analyze_intent_function
        def analyze_intent_function(message: str) -> Dict[str, Any]:
            """Phân tích nội dung tin nhắn để xác định agent phù hợp
            
            Args:
                message: Nội dung tin nhắn cần phân tích
                
            Returns:
                Dict[str, Any]: Kết quả phân tích ý định, bao gồm:
                    agent_type: Loại agent phù hợp
                    confidence: Độ tin cậy của kết quả phân loại (0-1)
                    keywords: Các từ khóa được nhận diện
            """
            return self.analyze_intent(message)
        
        # Initialize FunctionTool with the function
        super().__init__(func=analyze_intent_function)
        
        # Từ khóa cho BatCucLinhSoAgent
        self.batcuclinh_so_keywords = [
            "số điện thoại", "điện thoại", "sđt", "sim", "số sim", 
            "cccd", "căn cước", "căn cước công dân", "cmnd", "chứng minh", 
            "ngân hàng", "số tài khoản", "stk", "tài khoản", "mật khẩu", 
            "password", "bát cực", "phong thủy", "linh số", "bát trạch", 
            "phân tích số", "đánh giá số", "phong thủy số"
        ]
        
        # Từ khóa cho PaymentAgent
        self.payment_keywords = [
            "thanh toán", "nạp tiền", "gói dịch vụ", "mua gói", "subscription", 
            "gia hạn", "upgrade", "nâng cấp", "hóa đơn", "giá tiền", "chi phí", 
            "premium", "vip", "momo", "vnpay", "zalopay", "payos", "banking", 
            "ngân hàng", "thẻ visa", "thẻ mastercard", "thẻ atm", "thẻ tín dụng"
        ]
        
        # Từ khóa cho UserAgent
        self.user_keywords = [
            "tài khoản", "đăng ký", "đăng nhập", "login", "signup", "register", 
            "profile", "hồ sơ", "thông tin cá nhân", "mật khẩu", "đổi mật khẩu", 
            "quên mật khẩu", "khôi phục", "xóa tài khoản", "cập nhật", "update", 
            "xác thực", "api key", "token", "logout", "đăng xuất"
        ]
    
    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """Phân tích ý định của người dùng từ tin nhắn
        
        Args:
            message: Nội dung tin nhắn cần phân tích
            
        Returns:
            Dict[str, Any]: Kết quả phân tích ý định
        """
        message = message.lower()
        
        # Phát hiện từ khóa
        batcuc_score, batcuc_keywords = self._detect_keywords(message, self.batcuclinh_so_keywords)
        payment_score, payment_keywords = self._detect_keywords(message, self.payment_keywords)
        user_score, user_keywords = self._detect_keywords(message, self.user_keywords)
        
        # Tìm loại agent có điểm cao nhất
        max_score = max(batcuc_score, payment_score, user_score)
        
        # Xác định agent phù hợp
        if max_score == 0:
            agent_type = AgentType.UNKNOWN
            keywords = []
            confidence = 0.0
        elif max_score == batcuc_score:
            agent_type = AgentType.BAT_CUC_LINH_SO
            keywords = batcuc_keywords
            confidence = batcuc_score / len(message.split())
        elif max_score == payment_score:
            agent_type = AgentType.PAYMENT
            keywords = payment_keywords
            confidence = payment_score / len(message.split())
        else:
            agent_type = AgentType.USER
            keywords = user_keywords
            confidence = user_score / len(message.split())
        
        # Chuẩn hóa độ tin cậy (0-1)
        confidence = min(1.0, confidence * 3)  # Nhân 3 để tăng độ tin cậy
        
        return {
            "agent_type": agent_type,
            "confidence": confidence,
            "keywords": keywords
        }
    
    def _detect_keywords(self, message: str, keywords: List[str]) -> tuple:
        """Phát hiện từ khóa trong tin nhắn
        
        Args:
            message: Tin nhắn cần phân tích
            keywords: Danh sách từ khóa cần phát hiện
            
        Returns:
            tuple: (điểm số, danh sách từ khóa phát hiện được)
        """
        score = 0
        detected_keywords = []
        
        for keyword in keywords:
            if keyword in message:
                score += 1
                detected_keywords.append(keyword)
        
        return score, detected_keywords
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Thực thi tool với tham số từ ADK
        
        Args:
            **kwargs: Tham số, bao gồm message
            
        Returns:
            Dict[str, Any]: Kết quả phân tích ý định
        """
        message = kwargs.get("message", "")
        return await self.analyze_intent(message) 