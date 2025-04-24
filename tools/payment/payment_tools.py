"""
Payment Tools Module

Module chứa các công cụ quản lý thanh toán cho Payment Agent
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import HTTPException
from agents.payment_agent.models import Payment, PaymentCreate
from .plan_tools import get_plan_by_id

# Mock payments data
mock_payments = {}


def create_payment(
    user_id: str, payment_create: PaymentCreate
) -> Dict[str, Any]:
    """
    Create a new payment.
    
    Args:
        user_id (str): ID của người dùng
        payment_create (PaymentCreate): Thông tin thanh toán cần tạo
        
    Returns:
        Dict[str, Any]: Thông tin thanh toán đã tạo
        
    Raises:
        HTTPException: Nếu có lỗi xảy ra
    """
    # Validate plan exists
    plan = get_plan_by_id(payment_create.plan_id)
    
    # Validate payment amount
    if payment_create.amount != plan["price"]:
        raise HTTPException(status_code=400, detail="Invalid payment amount")
    
    # Create payment
    payment_id = str(uuid.uuid4())
    payment_data = {
        "id": payment_id,
        "user_id": user_id,
        "plan_id": payment_create.plan_id,
        "payment_method": payment_create.payment_method,
        "amount": payment_create.amount,
        "currency": payment_create.currency,
        "status": "pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "transaction_id": None
    }
    
    mock_payments[payment_id] = payment_data
    
    # For demo purposes, immediately complete the payment
    payment_data["status"] = "completed"
    payment_data["transaction_id"] = f"txn_{uuid.uuid4().hex}"
    payment_data["updated_at"] = datetime.now()
    
    return payment_data


def get_payment_by_id(payment_id: str) -> Dict[str, Any]:
    """
    Get payment by ID.
    
    Args:
        payment_id (str): ID của thanh toán
        
    Returns:
        Dict[str, Any]: Thông tin thanh toán
        
    Raises:
        HTTPException: Nếu không tìm thấy thanh toán
    """
    if payment_id not in mock_payments:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return mock_payments[payment_id]


def get_user_payments(user_id: str) -> List[Dict[str, Any]]:
    """
    Get all payments for a user.
    
    Args:
        user_id (str): ID của người dùng
        
    Returns:
        List[Dict[str, Any]]: Danh sách thanh toán của người dùng
    """
    return [
        payment for payment in mock_payments.values()
        if payment["user_id"] == user_id
    ]


def get_all_payments() -> List[Dict[str, Any]]:
    """
    Get all payments.
    
    Returns:
        List[Dict[str, Any]]: Danh sách tất cả thanh toán
    """
    return list(mock_payments.values()) 