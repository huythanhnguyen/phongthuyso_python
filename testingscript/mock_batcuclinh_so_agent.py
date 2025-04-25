#!/usr/bin/env python3
"""
Mock BatCucLinhSoAgent for testing

Lưu ý: Đây là phiên bản mock KHÔNG được sử dụng trong môi trường production
Tuân thủ cursor rule #2: Phải xác định nguyên nhân gốc rễ của lỗi và sửa chúng,
không phải tạo mock để lấp lỗ hổng
"""

import logging
from typing import Dict, Any, Optional

from agents.base_agent import BaseAgent
from agents.agent_types import AgentType
from shared_libraries.logger import get_logger

class MockBatCucLinhSoAgent(BaseAgent):
    """
    Mock BatCucLinhSoAgent - Phiên bản đơn giản cho mục đích kiểm thử
    """
    
    def __init__(self, name: str = "Mock BatCucLinhSo Agent", model_name: str = "gemini-2.0-flash"):
        """Khởi tạo agent"""
        super().__init__(name=name, agent_type=AgentType.BAT_CUC_LINH_SO, model_name=model_name, instruction="Test")
        self.logger = get_logger(name)
        self.logger.info(f"Initialized {name}")
    
    async def process_request(self, request_data: Any) -> Dict[str, Any]:
        """
        Phương thức chính để xử lý các yêu cầu liên quan đến bát cục linh số
        
        Args:
            request_data: Có thể là PhoneAnalysisRequest, CCCDAnalysisRequest, hoặc các loại request khác
            
        Returns:
            Dict chứa phản hồi với nội dung phân tích
        """
        self.logger.info(f"Processing request: {request_data}")
        
        # Xử lý yêu cầu phân tích số điện thoại
        if hasattr(request_data, "phone_number"):
            return await self._analyze_phone_number(request_data.phone_number)
        
        # Xử lý yêu cầu phân tích CCCD
        elif hasattr(request_data, "cccd_number"):
            return await self._analyze_cccd(request_data.cccd_number)
        
        # Xử lý yêu cầu phân tích số tài khoản ngân hàng
        elif hasattr(request_data, "bank_account"):
            return await self._analyze_bank_account(request_data.bank_account)
        
        # Xử lý yêu cầu phân tích mật khẩu
        elif hasattr(request_data, "password"):
            return await self._analyze_password(request_data.password)
        
        # Xử lý yêu cầu từ chat
        elif isinstance(request_data, dict) and 'message' in request_data:
            message = request_data.get('message', '')
            context = request_data.get('context', {})
            
            # Tìm số điện thoại trong tin nhắn
            import re
            phone_numbers = re.findall(r'0\d{9}', message)
            
            if phone_numbers:
                result = await self._analyze_phone_number(phone_numbers[0])
                result["metadata"] = context
                return result
            else:
                return {
                    "agent": self.name,
                    "status": "success",
                    "content": "Vui lòng cung cấp số điện thoại để tôi có thể phân tích",
                    "metadata": context
                }
        
        # Trường hợp không hỗ trợ
        self.logger.warning(f"Unsupported request type: {type(request_data)}")
        return {
            "agent": self.name,
            "status": "error",
            "content": f"Loại yêu cầu không được hỗ trợ: {type(request_data).__name__}"
        }
    
    async def _analyze_phone_number(self, phone_number: str) -> Dict[str, Any]:
        """Phân tích số điện thoại"""
        self.logger.info(f"Analyzing phone number: {phone_number}")
        
        # Phân tích và tạo phản hồi
        response_content = f"Phân tích số điện thoại {phone_number}:\n\n"
        
        # Tính tổng các chữ số
        total = sum(int(digit) for digit in phone_number if digit.isdigit())
        response_content += f"Tổng các chữ số: {total}\n"
        
        # Phân tích ngũ hành
        response_content += "Phân tích ngũ hành:\n"
        
        # Kiểm tra các cặp số đặc biệt
        pairs = [(phone_number[i], phone_number[i+1]) for i in range(0, len(phone_number)-1, 2)]
        response_content += f"Các cặp số: {pairs}\n"
        
        # Phân tích tính tương hợp
        response_content += "Đánh giá tổng thể: "
        if total % 10 in [6, 8, 9]:
            response_content += "Số điện thoại này mang lại may mắn và tài lộc."
        elif total % 10 in [1, 3, 5]:
            response_content += "Số điện thoại này mang năng lượng trung bình, khá cân bằng."
        else:
            response_content += "Số điện thoại này có một số yếu tố cần lưu ý, nên cân nhắc khi sử dụng lâu dài."
        
        return {
            "agent": self.name,
            "status": "success",
            "content": response_content
        }
    
    async def _analyze_cccd(self, cccd_number: str) -> Dict[str, Any]:
        """Phân tích số CCCD"""
        response_content = f"Phân tích số CCCD {cccd_number}:\n\n"
        response_content += "Đây là số CCCD hợp với những người mệnh Thủy và Kim."
        
        return {
            "agent": self.name,
            "status": "success",
            "content": response_content
        }
    
    async def _analyze_bank_account(self, bank_account: str) -> Dict[str, Any]:
        """Phân tích số tài khoản ngân hàng"""
        response_content = f"Phân tích số tài khoản {bank_account}:\n\n"
        response_content += "Số tài khoản này có nhiều số 8 và 9, thuận lợi cho việc tích lũy tài chính."
        
        return {
            "agent": self.name,
            "status": "success", 
            "content": response_content
        }
    
    async def _analyze_password(self, password: str) -> Dict[str, Any]:
        """Phân tích mật khẩu"""
        response_content = f"Phân tích mật khẩu của bạn:\n\n"
        response_content += "Mật khẩu này có sự kết hợp tốt giữa các con số và chữ cái, mang lại sự hài hòa."
        
        return {
            "agent": self.name,
            "status": "success",
            "content": response_content
        } 