"""
Subscription Tools Module

Module chứa các công cụ quản lý đăng ký cho Payment Agent
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from agents.payment_agent.models import Subscription
from .plan_tools import get_plan_by_id

# Mock subscriptions data
mock_subscriptions = {}


def create_subscription(
    user_id: str, plan_id: str, auto_renew: bool = False
) -> Dict[str, Any]:
    """
    Create a new subscription.
    
    Args:
        user_id (str): ID của người dùng
        plan_id (str): ID của gói dịch vụ
        auto_renew (bool): Tự động gia hạn
        
    Returns:
        Dict[str, Any]: Thông tin đăng ký đã tạo
    """
    # Validate plan exists
    plan = get_plan_by_id(plan_id)
    
    # Create subscription
    subscription_id = str(uuid.uuid4())
    
    # Calculate end date based on plan interval
    now = datetime.now()
    if plan["interval"] == "month":
        end_date = now.replace(month=now.month + 1)
    elif plan["interval"] == "year":
        end_date = now.replace(year=now.year + 1)
    else:
        end_date = now.replace(month=now.month + 1)  # Default to monthly
    
    subscription_data = {
        "id": subscription_id,
        "user_id": user_id,
        "plan_id": plan_id,
        "status": "active",
        "start_date": now,
        "end_date": end_date,
        "created_at": now,
        "updated_at": now,
        "is_active": True,
        "auto_renew": auto_renew
    }
    
    mock_subscriptions[subscription_id] = subscription_data
    
    return subscription_data


def get_user_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get the active subscription for a user.
    
    Args:
        user_id (str): ID của người dùng
        
    Returns:
        Optional[Dict[str, Any]]: Thông tin đăng ký đang hoạt động hoặc None
    """
    for subscription in mock_subscriptions.values():
        if (subscription["user_id"] == user_id and 
            subscription["is_active"] and 
            subscription["status"] == "active"):
            return subscription
    
    return None


def update_subscription(
    subscription_id: str, plan_id: Optional[str] = None, 
    status: Optional[str] = None, auto_renew: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update a subscription.
    
    Args:
        subscription_id (str): ID của đăng ký
        plan_id (Optional[str]): ID của gói dịch vụ mới
        status (Optional[str]): Trạng thái mới
        auto_renew (Optional[bool]): Tự động gia hạn
        
    Returns:
        Dict[str, Any]: Thông tin đăng ký đã cập nhật
        
    Raises:
        HTTPException: Nếu không tìm thấy đăng ký
    """
    if subscription_id not in mock_subscriptions:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    subscription = mock_subscriptions[subscription_id]
    
    if plan_id:
        # Validate plan exists
        plan = get_plan_by_id(plan_id)
        subscription["plan_id"] = plan_id
        
        # Update end date based on new plan
        now = datetime.now()
        if plan["interval"] == "month":
            subscription["end_date"] = now.replace(month=now.month + 1)
        elif plan["interval"] == "year":
            subscription["end_date"] = now.replace(year=now.year + 1)
    
    if status:
        subscription["status"] = status
        subscription["is_active"] = status == "active"
    
    if auto_renew is not None:
        subscription["auto_renew"] = auto_renew
    
    subscription["updated_at"] = datetime.now()
    
    return subscription 