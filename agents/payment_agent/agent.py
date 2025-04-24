"""
Payment Agent Implementation

Triển khai PaymentAgent - Agent xử lý thanh toán.
"""

from typing import Any, Dict

# Corrected imports
from agents.base_agent import BaseAgent
from agents.agent_types import AgentType
from shared_libraries.logger import get_logger

# Import the sub-agent (relative path is fine here)
from .sub_agents.subscription_agent import SubscriptionAgent

# Import request models
from shared_libraries.models import (
    PaymentRequest, # e.g., process_payment, create_checkout_session
    SubscriptionRequest # e.g., get_status, update_plan
)

# Import payment tools from the correct location
from tools.payment.payment_tools import create_payment # Example tool
from tools.payment.subscription_tools import get_user_active_subscription, update_subscription # Corrected import

# Import the prompt string
from .prompts.system_prompt import SYSTEM_PROMPT

# Tạo một agent kế thừa từ BaseAgent
class PaymentAgent(BaseAgent):
    """
    Payment Agent - Agent xử lý thanh toán và điều phối subscription.
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash", name: str = "payment_agent"):
        """
        Khởi tạo Payment Agent và SubscriptionAgent sub-agent.
        """
        self.logger = get_logger(name)
        instruction = SYSTEM_PROMPT
        
        # Instantiate Sub-Agent
        self.subscription_agent = SubscriptionAgent()
        
        # TODO: Define tools for payment processing (e.g., using FunctionTool)
        # Example tool registration (replace with actual payment methods)
        # agent_tools = [FunctionTool(self.process_payment)] 
        agent_tools = [] # No tools defined yet
        
        # Gọi constructor của BaseAgent
        super().__init__(
            name=name,
            model_name=model_name,
            instruction=instruction,
            tools=agent_tools
        )

    def process_payment_request(self, request: PaymentRequest) -> Dict[str, Any]:
        """
        Handles direct payment processing requests.
        (Placeholder Implementation)
        """
        self.logger.info(f"Processing payment request: {request}")
        # TODO: Implement logic using payment tools (e.g., call Stripe API via create_payment)
        # result = create_payment(request.user_id, request.payment_data)
        return {"status": "payment_processed", "transaction_id": "dummy_txn_123"} # Placeholder
        
    def process_subscription_request(self, request: SubscriptionRequest) -> Dict[str, Any]:
        """
        Routes subscription-related requests to SubscriptionAgent.
        """
        self.logger.info(f"Routing subscription request to SubscriptionAgent: {request}")
        # Example routing based on request type or attributes
        if hasattr(request, 'user_id') and hasattr(request, 'new_plan_id'):
            # return self.subscription_agent.update_subscription(request.user_id, request.new_plan_id)
            return update_subscription(request.user_id, request.new_plan_id) # Call tool directly
        elif hasattr(request, 'user_id'):
            # return self.subscription_agent.get_subscription_status(request.user_id)
            return get_user_active_subscription(request.user_id) # Call tool directly with corrected function name
        else:
            self.logger.error(f"Unknown subscription request type: {request}")
            return {"error": "Unknown subscription request type"}

    # Other methods related to payment processing, webhook handling etc.

# Tạo instance của PaymentAgent
# payment_agent = PaymentAgent() # Remove direct instantiation if handled by registry 