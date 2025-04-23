"""
Agent Types Enum.

This module defines the different types of agents available in the system.
"""

from enum import Enum, auto


class AgentType(Enum):
    """Enum representing the different types of agents in the system."""
    ROOT = auto()
    BAT_CUC_LINH_SO = auto()
    PAYMENT = auto()
    USER = auto() 