#!/usr/bin/env python3
"""
Script để thêm dữ liệu mẫu vào cơ sở dữ liệu giả lập
"""

import os
import sys
import uuid
from datetime import datetime, timedelta

# Thêm thư mục gốc vào path để import được các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import mock_users, mock_plans, mock_subscriptions, get_password_hash

def create_test_user():
    # Thông tin người dùng test
    email = "thanh@123.com"
    password = "123456"
    fullname = "Thanh Test"
    
    # Kiểm tra xem user đã tồn tại chưa
    if email in mock_users:
        print(f"✅ Người dùng {email} đã tồn tại")
        return mock_users[email]
        
    # Tạo ID người dùng
    user_id = str(uuid.uuid4())
    
    # Hash mật khẩu
    hashed_password = get_password_hash(password)
    
    # Tạo dữ liệu người dùng
    user_data = {
        "id": user_id,
        "email": email,
        "fullname": fullname,
        "hashed_password": hashed_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True,
        "is_premium": True,  # Đặt thành premium
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
        "plan_id": "premium",  # Sử dụng gói premium
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

if __name__ == "__main__":
    print("=== THÊM DỮ LIỆU MẪU ===")
    user = create_test_user()
    print("=== HOÀN THÀNH ===") 