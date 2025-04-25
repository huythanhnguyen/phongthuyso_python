#!/usr/bin/env python3
"""
Script để chạy ứng dụng với dữ liệu mẫu
"""

import os
import sys
import uuid
import json
import hashlib
from datetime import datetime, timedelta

# Import các thành phần cần thiết từ main
from main import (
    app, 
    mock_users, 
    mock_plans, 
    mock_subscriptions, 
    get_password_hash
)

def create_test_user():
    """Tạo người dùng test"""
    email = "thanh@123.com"
    password = "123456"
    fullname = "Thanh Test"
    
    # Kiểm tra xem đã có người dùng chưa
    if email in mock_users:
        print(f"✅ Người dùng {email} đã tồn tại")
        return mock_users[email]
    
    # Tạo ID người dùng
    user_id = str(uuid.uuid4())
    
    # Hash mật khẩu
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Tạo dữ liệu người dùng
    user_data = {
        "id": user_id,
        "email": email,
        "fullname": fullname,
        "hashed_password": hashed_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True,
        "is_premium": True,
        "quota_remaining": 100
    }
    
    # Thêm vào mock database
    mock_users[email] = user_data
    
    # Tạo đăng ký premium
    subscription_id = str(uuid.uuid4())
    end_date = datetime.now() + timedelta(days=30)
    
    subscription_data = {
        "id": subscription_id,
        "user_id": user_id,
        "plan_id": "premium",
        "status": "active",
        "start_date": datetime.now(),
        "end_date": end_date,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True,
        "auto_renew": True
    }
    
    mock_subscriptions[subscription_id] = subscription_data
    
    print(f"✅ Đã tạo người dùng test: {email} / {password}")
    print(f"✅ Người dùng có quyền Premium, quota: {user_data['quota_remaining']}")
    
    return user_data

def print_test_info():
    """In thông tin test cho người dùng"""
    print("\n===== THÔNG TIN TEST =====")
    print("API URL: http://localhost:8000")
    print("Frontend test page: frontend_test/frontend_demo.html")
    print("Tài khoản test: thanh@123.com / 123456")
    print("========================\n")

# Tạo người dùng test trước khi chạy ứng dụng
print("=== KHỞI TẠO SERVER VỚI DỮ LIỆU MẪU ===")
user = create_test_user()
print_test_info()

# Chạy ứng dụng
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 