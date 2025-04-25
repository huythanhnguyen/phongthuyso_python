#!/usr/bin/env python3
"""
Script kiểm thử chức năng chat của ứng dụng
"""

import json
import requests
import time

# URL cơ sở của API
BASE_URL = "http://localhost:8000"

# Thông tin tài khoản test 
TEST_EMAIL = "thanh@123.com"
TEST_PASSWORD = "123456"

def get_auth_token():
    """Lấy token xác thực từ API"""
    print("\n=== ĐĂNG NHẬP ===")
    
    try:
        # Tạo form data
        form_data = {
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        # Đăng nhập để lấy token
        response = requests.post(
            f"{BASE_URL}/api/user/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=form_data
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"✅ Đăng nhập thành công, token: {token[:20]}...")
            return token
        else:
            print(f"❌ Đăng nhập thất bại: {response.status_code}")
            print(f"❌ Lỗi: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Lỗi kết nối khi đăng nhập: {str(e)}")
        return None

def test_chat_api(token):
    """Kiểm tra API chat"""
    print("\n==== KIỂM TRA CHỨC NĂNG CHAT ====")
    
    if not token:
        print("❌ Không có token xác thực, bỏ qua kiểm tra chat")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Tạo các câu hỏi để kiểm tra
    test_messages = [
        "Xin chào, tôi muốn phân tích số điện thoại 0912345678",
        "Phân tích mối quan hệ giữa ngũ hành và số điện thoại",
        "Tôi muốn biết số nào là số may mắn cho tôi"
    ]
    
    session_id = None
    success_count = 0
    
    for i, message in enumerate(test_messages):
        print(f"\n=========== TEST MESSAGE {i+1} ===========")
        print(f"Message: {message}")
        
        try:
            # Tạo request body
            request_body = {
                "message": message,
                "context": {
                    "session_id": session_id,
                    "test_id": i+1
                }
            }
            
            print(f"Request body: {json.dumps(request_body)}")
            
            # Gửi tin nhắn và nhận response
            response = requests.post(
                f"{BASE_URL}/api/chat",
                headers=headers,
                json=request_body
            )
            
            print(f"Status code: {response.status_code}")
            print(f"Raw response: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("\nJSON Response:")
                    print(json.dumps(data, indent=2))
                    
                    # Lưu session_id từ metadata
                    if data.get("metadata") and data.get("metadata").get("session_id"):
                        session_id = data.get("metadata").get("session_id")
                    
                    success_count += 1
                    
                except json.JSONDecodeError:
                    print(f"❌ Lỗi parse JSON: {response.text}")
                
            else:
                print(f"❌ Gửi tin nhắn thất bại: {response.status_code}")
                print(f"❌ Lỗi: {response.text}")
                
        except Exception as e:
            print(f"❌ Lỗi kết nối đến API chat: {str(e)}")
        
        print("=" * 40)
        # Chờ giữa các lần gọi API
        time.sleep(1)
    
    print("\n==== KẾT QUẢ ====")
    print(f"✓ Đã kiểm tra {len(test_messages)} tin nhắn chat")
    print(f"✓ Thành công: {success_count}/{len(test_messages)}")
    print("=" * 40)

def main():
    print("=== SCRIPT KIỂM TRA CHỨC NĂNG CHAT ===")
    
    # Kiểm tra kết nối đến server
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Kết nối đến server thành công")
        else:
            print("❌ Kết nối đến server thất bại")
            print("Hãy đảm bảo server đang chạy")
            return
    except:
        print("❌ Không thể kết nối đến server")
        print("Hãy đảm bảo server đang chạy")
        return
    
    # Lấy token xác thực
    token = get_auth_token()
    
    # Kiểm tra chức năng chat
    test_chat_api(token)
    
    print("\n=== HOÀN THÀNH ===")

if __name__ == "__main__":
    main() 