"""
Root Agent Module

Cung cấp RootAgent - agent chính của hệ thống, điều phối các yêu cầu đến các agent chuyên biệt.
"""

from typing import Dict, Any, Optional, Type

# Corrected imports
from agents.agent_types import AgentType
from agents.base_agent import BaseAgent
from shared_libraries.logger import get_logger
# Import specific request models passed from the API layer
from shared_libraries.models import (
    BatCuLinhSoRequest, # Union of all BCLS requests
    PaymentRequest,     # Union of all Payment requests
    SubscriptionRequest,
    UserManagementRequest # Union of Auth/Profile/APIKey requests 
    # ... add other top-level request types if needed
)
# Import the prompt string
from .prompts.system_prompt import SYSTEM_PROMPT

# Import agent instances (assuming a registry or direct imports)
# This is complex, ideally use a registry pattern
# from .registry import get_agent_instance 

class RootAgent(BaseAgent):
    """
    Root Agent - Agent chính của hệ thống.
    Acts as a dispatcher based on pre-determined target agent and typed request.
    """
    
    def __init__(self, name: str = "Root Agent", model_name: str = "gemini-2.0-flash"):
        """
        Khởi tạo RootAgent.
        Removed agent registration here - should be handled externally.
        """
        # Adapt BaseAgent initialization as needed
        super().__init__(name=name, model_name=model_name, instruction=SYSTEM_PROMPT) 
        self.logger = get_logger(name)
        # self.agents registry might be populated externally or passed in
        self.agents: Dict[AgentType, BaseAgent] = {} 

    def register_agent(self, agent_type: AgentType, agent_instance: BaseAgent):
        """
        Registers a specific agent instance. Called externally.
        """
        self.logger.info(f"Registering agent: {agent_type.name}")
        self.agents[agent_type] = agent_instance

    async def route_request(self, target_agent_type: AgentType, request_data: Any) -> Dict[str, Any]:
        """
        Routes a pre-validated, typed request to the target agent's processing method.
        This method is intended to be called by the API layer/router.
        
        Args:
            target_agent_type (AgentType): The specific agent to handle the request.
            request_data (Any): The Pydantic model instance for the request.
            
        Returns:
            Dict[str, Any]: Kết quả xử lý từ agent chuyên biệt.
        """
        self.logger.info(f"Routing request of type {type(request_data).__name__} to {target_agent_type.name}")
        
        target_agent = self.agents.get(target_agent_type)
        
        if not target_agent:
            self.logger.error(f"Target agent {target_agent_type.name} not registered.")
            return {"error": f"Agent {target_agent_type.name} not available."}
            
        # --- Call the appropriate processing method based on agent type --- 
        try:
            if target_agent_type == AgentType.BAT_CUC_LINH_SO:
                # Assuming BatCucLinhSoAgent has a process_request method
                if hasattr(target_agent, 'process_request') and callable(target_agent.process_request):
                    # Ensure request_data is the correct type (e.g., BatCuLinhSoRequest union)
                    return await target_agent.process_request(request_data)
                else:
                     raise NotImplementedError(f"{target_agent_type.name} does not have a process_request method.")

            elif target_agent_type == AgentType.PAYMENT:
                # Assuming PaymentAgent has specific methods based on request type
                if hasattr(target_agent, 'process_payment_request') and isinstance(request_data, PaymentRequest):
                    return await target_agent.process_payment_request(request_data)
                elif hasattr(target_agent, 'process_subscription_request') and isinstance(request_data, SubscriptionRequest):
                    return await target_agent.process_subscription_request(request_data)
                else:
                    raise NotImplementedError(f"No handler for {type(request_data).__name__} in {target_agent_type.name}.")

            elif target_agent_type == AgentType.USER:
                # UserAgent likely handles requests via specific methods matching API routes
                # The API layer should call the specific method directly (e.g., UserAgent.login_user)
                # This route_request might not be the best fit for UserAgent's FastAPI integration.
                # Returning error here, assuming UserAgent methods are called directly.
                self.logger.warning(f"Routing to UserAgent via route_request is not standard. Call specific methods directly.")
                return {"error": "UserAgent methods should be called directly from API routes."}
            
            # Add other agent types here (e.g., ROOT for direct processing)
            elif target_agent_type == AgentType.ROOT:
                 return await self.process_direct_root_request(request_data)
                 
            else:
                self.logger.error(f"Routing logic not implemented for agent type: {target_agent_type.name}")
                return {"error": f"Cannot route to agent type: {target_agent_type.name}"}

        except Exception as e:
            self.logger.exception(f"Error processing request in {target_agent_type.name}: {e}")
            return {"error": f"An internal error occurred while processing the request in {target_agent_type.name}.", "detail": str(e)}

    async def process_direct_root_request(self, request_data: Any) -> Dict[str, Any]:
        """
        Handles requests explicitly targeted at the RootAgent itself.
        (Placeholder - Add any logic RootAgent should handle directly)
        """
        self.logger.info(f"Processing direct request: {request_data}")
        # Example: return status, help info, etc.
        return {
            "agent": self.name,
            "status": "success",
            "content": f"Root Agent received direct request: {request_data}. No specific action defined.",
            "metadata": {}
        }

    # Removed _determine_agent_type method
    # Removed old handle_request method
    # Removed old process_message method (use process_direct_root_request)

# --- Singleton Instantiation --- 
# This might be better handled by a dependency injection framework or registry
# root_agent = RootAgent()

# --- Example Usage (External Registration) --- 
# root_agent.register_agent(AgentType.BAT_CUC_LINH_SO, batcuclinh_so_agent_instance)
# root_agent.register_agent(AgentType.PAYMENT, payment_agent_instance)
# root_agent.register_agent(AgentType.USER, user_agent_instance) 