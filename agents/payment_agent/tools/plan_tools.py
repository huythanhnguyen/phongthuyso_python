"""
Plan Tools Module

Module chứa các công cụ quản lý kế hoạch thanh toán cho Payment Agent
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from phongthuyso_python.agents.payment_agent.models import Plan, PlanType

# Mock plans data
mock_plans = {
    "free": {
        "id": "free",
        "name": "Miễn phí",
        "type": "free",
        "price": 0,
        "currency": "VND",
        "interval": "month",
        "description": "Gói dùng thử miễn phí",
        "features": ["Phân tích cơ bản số điện thoại", "5 lần phân tích/ngày"],
        "quota": 5,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    "basic": {
        "id": "basic",
        "name": "Cơ bản",
        "type": "basic",
        "price": 99000,
        "currency": "VND",
        "interval": "month",
        "description": "Gói cơ bản cho người dùng cá nhân",
        "features": ["Phân tích đầy đủ số điện thoại", "Phân tích CCCD", "50 lần phân tích/tháng"],
        "quota": 50,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    "premium": {
        "id": "premium",
        "name": "Cao cấp",
        "type": "premium",
        "price": 199000,
        "currency": "VND",
        "interval": "month",
        "description": "Gói cao cấp cho người dùng chuyên nghiệp",
        "features": ["Tất cả tính năng của gói Cơ bản", "Phân tích STK ngân hàng", "Phân tích mật khẩu", "200 lần phân tích/tháng"],
        "quota": 200,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
}


def get_all_plans() -> List[Dict[str, Any]]:
    """
    Get all available plans.
    
    Returns:
        List[Dict[str, Any]]: Danh sách tất cả các gói dịch vụ
    """
    return list(mock_plans.values())


def get_plan_by_id(plan_id: str) -> Dict[str, Any]:
    """
    Get plan by ID.
    
    Args:
        plan_id (str): ID của gói dịch vụ
        
    Returns:
        Dict[str, Any]: Thông tin gói dịch vụ
        
    Raises:
        HTTPException: Nếu không tìm thấy gói dịch vụ
    """
    if plan_id not in mock_plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return mock_plans[plan_id] 