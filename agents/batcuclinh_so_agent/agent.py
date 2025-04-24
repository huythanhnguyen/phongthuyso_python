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
        
        # Define tools 
        agent_tools = [
            FunctionTool(self.process_request) 
        ]
        
        # Call BaseAgent constructor
        super().__init__(
            name=name,
            model_name=model_name,
            instruction=instruction,
            tools=agent_tools 
        )

    async def process_request(self, request: BatCucLinhSoRequest) -> Dict[str, Any]:
        """
        Phân tích loại yêu cầu và điều phối đến sub-agent phù hợp.
        
        Args:
            request: Yêu cầu phân tích (Phone, CCCD, Bank, Password).
            
        Returns:
            Kết quả từ sub-agent tương ứng.
        """
        self.logger.info(f"BatCucLinhSoAgent nhận yêu cầu loại: {type(request).__name__}")

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

# Instantiate the agent for easy import by root_agent
# Ensure python_adk path is correct for your project structure
# Example:
# from python_adk.agents.batcuclinh_so_agent.agent import BatCucLinhSoAgent
# batcuclinh_so_agent = BatCucLinhSoAgent()
# --- Remove direct instantiation if handled by a registry --- 
# batcuclinh_so_agent = BatCucLinhSoAgent()