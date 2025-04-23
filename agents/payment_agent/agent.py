"""
Payment Agent Implementation

Triển khai PaymentAgent - Agent xử lý thanh toán.
"""

from typing import Any, Dict

from python_adk.agents.base_agent import BaseAgent
from python_adk.agents.root_agent.agent import AgentType
from python_adk.prompt import get_agent_prompt

# Tạo một agent kế thừa từ BaseAgent
class PaymentAgent(BaseAgent):
    """
    Payment Agent - Agent xử lý thanh toán
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash", name: str = "payment_agent"):
        """
        Khởi tạo Payment Agent
        
        Args:
            model_name (str): Tên model sử dụng cho agent
            name (str): Tên của agent
        """
        # Lấy prompt làm instruction
        instruction = get_agent_prompt(AgentType.PAYMENT)
        
        # Gọi constructor của BaseAgent
        super().__init__(
            name=name,
            model_name=model_name,
            instruction=instruction
        )

# Tạo instance của PaymentAgent
payment_agent = PaymentAgent() 