"""
Agent Types Module

This module defines the AgentType enum to avoid circular imports between agent modules.
"""

from enum import Enum


class AgentType(str, Enum):
    """Các loại agent trong hệ thống"""
    ROOT = "root"
    BAT_CUC_LINH_SO = "batcuclinh_so"
    PAYMENT = "payment"
    USER = "user"

    def __str__(self):
        return self.value 