#!/usr/bin/env python3
"""
Script để chạy ứng dụng với debug level cao
"""

import os
import sys
import uuid
import hashlib
import logging
from datetime import datetime, timedelta

# Cấu hình logging trước khi import các module khác
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("run_app_debug")

logger.debug("Bắt đầu khởi động ứng dụng trong chế độ debug")

# Import các thành phần cần thiết từ main
from main import (
    app, 
    mock_users, 
    mock_plans, 
    mock_subscriptions, 
    get_password_hash,
    root_agent
)

logger.debug(f"Đã import RootAgent: {root_agent}")
logger.debug(f"RootAgent.__dict__: {dir(root_agent)}")
logger.debug(f"process_direct_root_request method: {getattr(root_agent, 'process_direct_root_request', None)}")

def create_test_user():
    """Tạo người dùng test"""
    email = "thanh@123.com"
    password = "123456"
    fullname = "Thanh Test"
    
    # Kiểm tra xem đã có người dùng chưa
    if email in mock_users:
        logger.info(f"✅ Người dùng {email} đã tồn tại")
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
    
    logger.info(f"✅ Đã tạo người dùng test: {email} / {password}")
    logger.info(f"✅ Người dùng có quyền Premium, quota: {user_data['quota_remaining']}")
    
    return user_data

def print_test_info():
    """In thông tin test cho người dùng"""
    logger.info("\n===== THÔNG TIN TEST =====")
    logger.info("API URL: http://localhost:8000")
    logger.info("Frontend test page: frontend_test/frontend_demo.html")
    logger.info("Tài khoản test: thanh@123.com / 123456")
    logger.info("========================\n")

# Tạo người dùng test trước khi chạy ứng dụng
logger.info("=== KHỞI TẠO SERVER VỚI DỮ LIỆU MẪU (DEBUG MODE) ===")
user = create_test_user()
print_test_info()

# Chạy ứng dụng với reload=False để buộc phải load lại toàn bộ code
if __name__ == "__main__":
    import uvicorn
    logger.info("Khởi động server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, log_level="debug") 