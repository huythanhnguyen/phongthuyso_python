"""
BatCucLinhSo Agent Implementation

Triển khai BatCucLinhSoAgent - Agent chính điều phối phân tích phong thủy số.
"""

from typing import Any, Dict, Union

from google.adk.tools import FunctionTool # Keep for now, might remove later

from agents.base_agent import BaseAgent
from prompt import get_agent_prompt # Assuming get_agent_prompt is in project root's prompt.py
from shared_libraries.logger import get_logger
from shared_libraries.models import (
    PhoneAnalysisRequest,
    CCCDAnalysisRequest,
    BankAccountRequest,
    PasswordRequest,
    # Define a base request or use Union for type hint
    BatCucLinhSoRequest # Assuming a Union or Base class exists
)

# Import Sub-Agents
from .sub_agents.phone_number_agent import PhoneNumberAgent
from .sub_agents.cccd_agent import CCCDAgent
from .sub_agents.bank_account_agent import BankAccountAgent
from .sub_agents.password_agent import PasswordAgent

# Import AgentType for prompt lookup
from agents.agent_types import AgentType
# Import the prompt string
from .prompts.system_prompt import SYSTEM_PROMPT

class BatCucLinhSoAgent(BaseAgent):
    """
    BatCucLinhSo Agent - Điều phối viên cho các sub-agent phân tích số.
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash", name: str = "bat_cuc_linh_so_agent"):
        """
        Khởi tạo BatCucLinhSo Agent và các sub-agent của nó.
        """
        self.logger = get_logger(name)
        instruction = SYSTEM_PROMPT # Use the imported prompt
        
        # Instantiate Sub-Agents
        self.phone_agent = PhoneNumberAgent()
        self.cccd_agent = CCCDAgent()
        self.bank_account_agent = BankAccountAgent()
        self.password_agent = PasswordAgent()
        
        # Call BaseAgent constructor
        super().__init__(
            name=name,
            agent_type=AgentType.BAT_CUC_LINH_SO,
            model_name=model_name,
            instruction=instruction
        )

    async def process_request(self, request: BatCucLinhSoRequest) -> Dict[str, Any]:
        """
        Phân tích loại yêu cầu và điều phối đến sub-agent phù hợp.
        
        Args:
            request: Yêu cầu phân tích (Phone, CCCD, Bank, Password) hoặc dict từ API chat.
            
        Returns:
            Kết quả từ sub-agent tương ứng.
        """
        self.logger.info(f"BatCucLinhSoAgent nhận yêu cầu loại: {type(request).__name__}")

        # Xử lý yêu cầu từ chat API (dict)
        if isinstance(request, dict):
            return await self._process_dict_request(request)

        # Xử lý các loại yêu cầu từ mô hình cụ thể
        if isinstance(request, PhoneAnalysisRequest):
            # Check if it's analysis or suggestion based on request fields? 
            # For now, assume analyze_phone exists. Need refinement.
            if hasattr(request, 'phone_number') and request.phone_number: # Basic check for analysis
                return self.phone_agent.analyze_phone(request)
            elif hasattr(request, 'purpose'): # Basic check for suggestion
                # Assuming suggest_phone takes purpose and optional digits from the request object
                return self.phone_agent.suggest_phone(request.purpose, getattr(request, 'preferred_digits', None)) # TODO: Adjust suggest_phone signature or request model
            else:
                self.logger.error("Không xác định được hành động cho PhoneAnalysisRequest")
                return {"error": "Hành động không xác định cho yêu cầu điện thoại."}

        elif isinstance(request, CCCDAnalysisRequest):
            # Ensure the cccd_agent instance is used
            return await self.cccd_agent.analyze_cccd(request) # Added await if analyze_cccd is async
            
        elif isinstance(request, BankAccountRequest):
             # Ensure the bank_account_agent instance is used
            return await self.bank_account_agent.analyze_bank_account(request) # Added await if analyze_bank_account is async
            
        elif isinstance(request, PasswordRequest):
             # Ensure the password_agent instance is used
            return await self.password_agent.generate_password(request) # Added await if generate_password is async
            
        else:
            self.logger.error(f"Loại yêu cầu không được hỗ trợ: {type(request).__name__}")
            return {"error": f"Loại yêu cầu không được hỗ trợ: {type(request).__name__}"}

    async def _process_dict_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Xử lý yêu cầu dạng dict từ chat API
        
        Args:
            request: Dict chứa message và context
            
        Returns:
            Dict[str, Any]: Kết quả xử lý
        """
        message = request.get('message', '')
        context = request.get('context', {})
        
        self.logger.info(f"Xử lý tin nhắn: {message}")
        
        try:
            # Phân tích tin nhắn để xác định loại yêu cầu
            import re
            
            # Xử lý yêu cầu phân tích số điện thoại
            if any(keyword in message.lower() for keyword in ['số điện thoại', 'sđt', 'phong thủy số', 'phân tích số']):
                # Tìm số điện thoại trong tin nhắn
                phone_match = re.search(r'0\d{9}', message)
                if phone_match:
                    phone_number = phone_match.group(0)
                    self.logger.info(f"Tìm thấy số điện thoại: {phone_number}")
                    # Tạo request phân tích số điện thoại
                    phone_request = PhoneAnalysisRequest(
                        phone_number=phone_number,
                        request_type="phone_analysis",
                        user_id=context.get('user_id'),
                        context=context
                    )
                    result = self.phone_agent.analyze_phone(phone_request)
                    return {
                        "agent": self.name,
                        "status": "success",
                        "content": f"Phân tích số điện thoại {phone_number}:\n\nĐiểm tổng thể: {result.get('total_score', 'N/A')}/10\nMức độ may mắn: {result.get('luck_level', 'N/A')}\n\nKhuyến nghị:\n- " + "\n- ".join(result.get('recommendations', ['Không có khuyến nghị'])),
                        "metadata": context
                    }
            
            # Xử lý yêu cầu phân tích CCCD
            if any(keyword in message.lower() for keyword in ['cccd', 'căn cước', 'cmnd']):
                # Tìm 6 số cuối của CCCD trong tin nhắn
                cccd_match = re.search(r'\d{6}', message)
                if cccd_match:
                    cccd_digits = cccd_match.group(0)
                    self.logger.info(f"Tìm thấy mã CCCD: {cccd_digits}")
                    # Tạo request phân tích CCCD
                    cccd_request = CCCDAnalysisRequest(
                        cccd_last_digits=cccd_digits,
                        request_type="cccd_analysis",
                        user_id=context.get('user_id'),
                        context=context
                    )
                    result = await self.cccd_agent.analyze_cccd(cccd_request)
                    return {
                        "agent": self.name,
                        "status": "success",
                        "content": f"Phân tích 6 số cuối của CCCD {cccd_digits}:\n\nĐiểm tổng thể: {result.get('total_score', 'N/A')}/10\nMức độ may mắn: {result.get('luck_level', 'N/A')}\n\nÝ nghĩa tổng thể:\n{result.get('overall_meaning', 'Không có thông tin')}",
                        "metadata": context
                    }
            
            # Xử lý yêu cầu về tài khoản ngân hàng
            if any(keyword in message.lower() for keyword in ['tài khoản', 'ngân hàng', 'stk']):
                # Tạo request về tài khoản ngân hàng
                purpose = "cá nhân"  # Mặc định
                bank_name = "VCB"    # Mặc định
                
                # Trích xuất thông tin từ tin nhắn (đơn giản)
                if "kinh doanh" in message.lower():
                    purpose = "kinh doanh"
                elif "tiết kiệm" in message.lower() or "đầu tư" in message.lower():
                    purpose = "tiết kiệm"
                
                # Kiểm tra ngân hàng
                bank_match = re.search(r'(VCB|TCB|ACB|MB|VPB|SHB)', message, re.IGNORECASE)
                if bank_match:
                    bank_name = bank_match.group(0).upper()
                
                bank_request = BankAccountRequest(
                    purpose=purpose,
                    bank_name=bank_name,
                    request_type="bank_account_analysis",
                    user_id=context.get('user_id'),
                    context=context
                )
                result = await self.bank_account_agent.analyze_bank_account(bank_request)
                return {
                    "agent": self.name,
                    "status": "success",
                    "content": f"Đề xuất cặp số cuối tài khoản ngân hàng {bank_name} cho mục đích {purpose}:\n\n" + "\n".join([f"- Cặp số {p.get('pair')}: {p.get('meaning')}" for p in result.get('suggested_pairs', [])[:3]]) + "\n\nKhuyến nghị: " + result.get('recommendations', ['Không có khuyến nghị'])[0],
                    "metadata": context
                }
        except Exception as e:
            self.logger.error(f"Lỗi xử lý yêu cầu dict: {str(e)}")
            
        # Trả về phản hồi mặc định nếu không xác định được loại yêu cầu cụ thể
        return {
            "agent": self.name,
            "status": "success",
            "content": "Tôi là Bát Cực Linh Số Agent, chuyên phân tích phong thủy số. Bạn có thể nhờ tôi phân tích số điện thoại, CCCD, tài khoản ngân hàng hoặc tạo mật khẩu phong thủy. Vui lòng đề cập cụ thể đến số điện thoại, 6 số cuối CCCD, hoặc yêu cầu về tài khoản ngân hàng trong tin nhắn của bạn.",
            "metadata": context
        }

# Instantiate the agent for easy import by root_agent
# Đã thay đổi tên project trong các imports
# Example:
# from agents.batcuclinh_so_agent.agent import BatCucLinhSoAgent
# --- Remove direct instantiation if handled by a registry --- 
# batcuclinh_so_agent = BatCucLinhSoAgent()