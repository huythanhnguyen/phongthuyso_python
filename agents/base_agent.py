"""
Base Agent Module.

This module defines the BaseAgent class that all other agents inherit from.
"""

import abc
import logging
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from .agent_types import AgentType


class AgentResponse(BaseModel):
    """Model for agent responses."""
    content: str
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(abc.ABC):
    """Base class for all agents in the system."""

    def __init__(self, name: str, agent_type: AgentType):
        """Initialize the base agent.

        Args:
            name: The name of the agent.
            agent_type: The type of the agent.
        """
        self.name = name
        self.agent_type = agent_type
        self.logger = logging.getLogger(f"agent.{name}")

    @abc.abstractmethod
    async def process(self, message: str, context: Optional[Dict[str, Any]] = None) -> AgentResponse:
        """Process a message and return a response.

        Args:
            message: The message to process.
            context: Optional context information.

        Returns:
            An AgentResponse containing the processed result.
        """
        pass

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an incoming request.

        Args:
            request: The request data.

        Returns:
            The response data.
        """
        message = request.get("message", "")
        context = request.get("context", {})
        
        try:
            self.logger.info(f"Processing message: {message[:50]}...")
            response = await self.process(message, context)
            
            return {
                "status": "success",
                "agent": self.name,
                "content": response.content,
                "metadata": response.metadata or {}
            }
        except Exception as e:
            self.logger.exception(f"Error processing message: {e}")
            
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e),
                "content": "Sorry, I encountered an error while processing your request."
            }

    def __str__(self) -> str:
        """Return a string representation of the agent.

        Returns:
            A string representation.
        """
        return f"{self.name} ({self.agent_type.name})" 