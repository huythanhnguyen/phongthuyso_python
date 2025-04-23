"""
Payment Agent Models Module

Module chứa các model cho Payment Agent
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel


class PlanType(str, Enum):
    """Subscription plan types."""
    
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class Plan(BaseModel):
    """Subscription plan model."""
    
    id: str
    name: str
    type: PlanType
    price: float
    currency: str = "VND"
    interval: str = "month"
    description: str
    features: List[str]
    quota: int
    created_at: datetime
    updated_at: datetime


class PaymentCreate(BaseModel):
    """Model for creating a payment."""
    
    plan_id: str
    payment_method: str
    amount: float
    currency: str = "VND"


class Payment(BaseModel):
    """Payment model."""
    
    id: str
    user_id: str
    plan_id: str
    payment_method: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    updated_at: datetime
    transaction_id: Optional[str] = None


class Subscription(BaseModel):
    """Subscription model."""
    
    id: str
    user_id: str
    plan_id: str
    status: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
    is_active: bool
    auto_renew: bool 