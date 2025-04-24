"""
Agent Registry Module

Module quản lý việc đăng ký và khởi tạo các agent trong hệ thống.
"""

from typing import Dict, List, Optional

from agents.agent_types import AgentType
from agents.base_agent import BaseAgent


class AgentRegistry:
    """
    Class quản lý việc đăng ký và khởi tạo các agent trong hệ thống
    """
    
    def __init__(self):
        """Khởi tạo AgentRegistry"""
        self.agents = {}
    
    def register_agent(self, agent: BaseAgent) -> None:
        """
        Đăng ký một agent
        
        Args:
            agent (BaseAgent): Agent cần đăng ký
        """
        self.agents[agent.agent_type] = agent
    
    def get_agent_by_type(self, agent_type: AgentType) -> Optional[BaseAgent]:
        """
        Lấy agent theo loại
        
        Args:
            agent_type (AgentType): Loại agent cần lấy
            
        Returns:
            Optional[BaseAgent]: Agent được yêu cầu hoặc None nếu không tìm thấy
        """
        return self.agents.get(agent_type)
    
    def list_agents(self) -> List[BaseAgent]:
        """
        Lấy danh sách tất cả các agent đã đăng ký
        
        Returns:
            List[BaseAgent]: Danh sách các agent
        """
        return list(self.agents.values()) 