"""
Agent Registry Module

Module quản lý việc đăng ký và khởi tạo các agent trong hệ thống.
Sử dụng Singleton pattern để đảm bảo chỉ có một registry được sử dụng trong toàn bộ ứng dụng.
"""

from typing import Dict, Optional, Type

from python_adk.agents.base_agent import BaseAgent
from python_adk.agents.root_agent.agent import AgentType, root_agent
from python_adk.agents.batcuclinh_so_agent import BatCucLinhSoAgent
from python_adk.agents.payment_agent import PaymentAgent
from python_adk.agents.user_agent import UserAgent
from python_adk.shared_libraries.logger import get_logger


class AgentRegistry:
    """
    Singleton class quản lý việc đăng ký và khởi tạo các agent trong hệ thống
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super(AgentRegistry, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Khởi tạo AgentRegistry"""
        if not self._initialized:
            self.logger = get_logger("AgentRegistry", log_to_file=True)
            self.agent_classes: Dict[AgentType, Type[BaseAgent]] = {}
            self.agent_instances: Dict[AgentType, BaseAgent] = {}
            
            # Đăng ký các agent mặc định
            self._register_default_agents()
            
            self._initialized = True
    
    def _register_default_agents(self) -> None:
        """Đăng ký các lớp agent mặc định"""
        # Sử dụng root_agent đã được tạo thay vì đăng ký lớp
        self.agent_instances[AgentType.ROOT] = root_agent
        
        self.register_agent_class(AgentType.BATCUCLINH_SO, BatCucLinhSoAgent)
        self.register_agent_class(AgentType.PAYMENT, PaymentAgent)
        self.register_agent_class(AgentType.USER, UserAgent)
        
        self.logger.info("Đã đăng ký các agent mặc định")
    
    def register_agent_class(self, agent_type: AgentType, agent_class: Type[BaseAgent]) -> None:
        """
        Đăng ký một lớp agent
        
        Args:
            agent_type (AgentType): Loại agent
            agent_class (Type[BaseAgent]): Lớp agent cần đăng ký
        """
        self.agent_classes[agent_type] = agent_class
        self.logger.info(f"Đã đăng ký lớp agent: {agent_type} -> {agent_class.__name__}")
    
    def get_agent(self, agent_type: AgentType, model_name: Optional[str] = None) -> BaseAgent:
        """
        Lấy instance của agent theo loại
        
        Args:
            agent_type (AgentType): Loại agent cần lấy
            model_name (Optional[str]): Tên model sử dụng cho agent (nếu cần)
            
        Returns:
            BaseAgent | GeminiAgent: Instance của agent được yêu cầu
            
        Raises:
            ValueError: Nếu loại agent không được đăng ký
        """
        # Nếu là RootAgent, trả về instance đã tạo
        # if agent_type == AgentType.ROOT:
        #     return root_agent
            
        # Kiểm tra nếu đã có instance
        if agent_type in self.agent_instances:
            return self.agent_instances[agent_type]
        
        # Kiểm tra nếu lớp agent đã được đăng ký
        if agent_type not in self.agent_classes:
            self.logger.error(f"Không tìm thấy agent: {agent_type}")
            raise ValueError(f"Agent type not registered: {agent_type}")
        
        # Tạo instance mới
        agent_class = self.agent_classes[agent_type]
        
        if model_name:
            agent = agent_class(model_name=model_name)
        else:
            agent = agent_class()
        
        # Lưu instance vào cache
        self.agent_instances[agent_type] = agent
        
        self.logger.info(f"Đã khởi tạo agent: {agent_type}")
        
        # Bỏ đăng ký với RootAgent, việc này giờ được làm khi khởi tạo RootAgent
        # root_agent.register_agent(agent_type, agent)
        
        return agent
    
    def clear_instances(self) -> None:
        """Xóa tất cả các instance đã tạo ngoại trừ RootAgent"""
        # Giữ lại RootAgent
        root = self.agent_instances.get(AgentType.ROOT)
        self.agent_instances.clear()
        
        # Khôi phục RootAgent
        if root:
            self.agent_instances[AgentType.ROOT] = root
            
        self.logger.info("Đã xóa tất cả các instance agent (ngoại trừ RootAgent)")


# Singleton instance để sử dụng toàn cục
agent_registry = AgentRegistry() 