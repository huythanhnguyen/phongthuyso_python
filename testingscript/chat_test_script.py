#!/usr/bin/env python3
"""
Script kiểm thử chức năng chat của ứng dụng
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Thông tin tài khoản test
TEST_EMAIL = "thanh@123.com"
TEST_PASSWORD = "123456"

def get_auth_token(base_url="http://localhost:8000"):
    """Lấy token xác thực từ API"""
    print("Đang lấy token xác thực...")
    
    login_data = {
        "username": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        response = requests.post(f"{base_url}/api/user/token", data=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Đăng nhập thành công: {response.status_code}")
            return token
        else:
            print(f"❌ Đăng nhập thất bại: {response.status_code}")
            print(f"❌ Lỗi: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Lỗi kết nối đến API: {str(e)}")
        return None

def test_chat_api(token=None, base_url="http://localhost:8000"):
    """Kiểm tra API chat"""
    print("\n==== KIỂM TRA CHỨC NĂNG CHAT ====")
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    # Tạo các câu hỏi để kiểm tra
    test_messages = [
        "Xin chào, tôi muốn phân tích số điện thoại 0912345678",
        "Phân tích mối quan hệ giữa ngũ hành và số điện thoại",
        "Tôi muốn biết số nào là số may mắn cho tôi"
    ]
    
    session_id = None
    
    for i, message in enumerate(test_messages):
        print(f"\nGửi câu hỏi {i+1}: {message}")
        
        try:
            # Gửi tin nhắn chat
            request_body = {
                "message": message,
                "context": {
                    "session_id": session_id 
                }
            }
            
            response = requests.post(
                f"{base_url}/api/chat",
                headers={**headers, "Content-Type": "application/json"},
                json=request_body
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Gửi tin nhắn thành công: {response.status_code}")
                print(f"✅ Phản hồi từ agent: {data.get('agent')}")
                
                # Lưu session_id nếu có
                if data.get("metadata") and data.get("metadata").get("session_id"):
                    session_id = data.get("metadata").get("session_id")
                    print(f"✅ Session ID: {session_id}")
                
                # Hiển thị một phần nội dung phản hồi
                content = data.get("content", "")
                if len(content) > 100:
                    content = content[:100] + "..."
                print(f"✅ Nội dung: {content}")
            else:
                print(f"❌ Gửi tin nhắn thất bại: {response.status_code}")
                print(f"❌ Lỗi: {response.text}")
        except Exception as e:
            print(f"❌ Lỗi kết nối đến API chat: {str(e)}")
        
        # Chờ giữa các lần gọi API
        time.sleep(1)
    
    print("\n==== KẾT QUẢ ====")
    print(f"✓ Đã kiểm tra {len(test_messages)} tin nhắn chat")
    if session_id:
        print(f"✓ Session ID: {session_id}")
    print("===================")

def main():
    print("=== SCRIPT KIỂM TRA CHỨC NĂNG CHAT ===")
    
    # Kiểm tra kết nối đến server
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Kết nối đến server thành công")
        else:
            print("❌ Kết nối đến server thất bại")
            print("Hãy đảm bảo server đang chạy với lệnh: python run_app_with_seed.py")
            return
    except:
        print("❌ Không thể kết nối đến server")
        print("Hãy đảm bảo server đang chạy với lệnh: python run_app_with_seed.py")
        return
    
    # Lấy token xác thực
    token = get_auth_token()
    
    # Kiểm tra chức năng chat
    test_chat_api(token)
    
    print("\n=== HOÀN THÀNH ===")

if __name__ == "__main__":
    main() 