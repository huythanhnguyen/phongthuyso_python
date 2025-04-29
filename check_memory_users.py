#!/usr/bin/env python3
"""
Script kiểm tra danh sách người dùng trong bộ nhớ của ứng dụng (mock_users)
"""

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000"

def check_memory_users():
    """Kiểm tra danh sách người dùng trong bộ nhớ thông qua API"""
    
    print("=== KIỂM TRA NGƯỜI DÙNG TRONG BỘ NHỚ ===")
    
    # 1. Đăng nhập với tài khoản đã biết
    try:
        print("\n[1] Đăng nhập với tài khoản thanh@124.com...")
        login_url = f"{BASE_URL}/api/user/token"
        login_data = {
            "username": "thanh@124.com",
            "password": "123456"
        }
        
        login_response = requests.post(
            login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result.get("access_token")
            print("Đăng nhập thành công!")
            print(f"Thông tin người dùng: {login_result['user']['fullname']}")
            
            # 2. Truy cập API /api/user/me để lấy thông tin người dùng hiện tại
            print("\n[2] Lấy thông tin người dùng hiện tại...")
            me_url = f"{BASE_URL}/api/user/me"
            me_response = requests.get(
                me_url,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if me_response.status_code == 200:
                user_info = me_response.json()
                print("Thông tin người dùng hiện tại:")
                pprint(user_info)
            else:
                print(f"Không thể lấy thông tin người dùng: {me_response.status_code}")
                print(me_response.text)
            
            # 3. Nếu người dùng có quyền admin (không có trong thiết kế hiện tại)
            # Có thể tạo thêm endpoint để liệt kê tất cả người dùng
            # Hiện tại chúng ta không có endpoint này
            
        else:
            print(f"Đăng nhập thất bại: {login_response.status_code}")
            print(login_response.text)
    
    except Exception as e:
        print(f"Lỗi khi kiểm tra người dùng: {e}")
    
    print("\n=== KẾT THÚC KIỂM TRA ===")

if __name__ == "__main__":
    check_memory_users() 