#!/usr/bin/env python3
"""
Script kiểm thử frontend và khắc phục lỗi phát sinh
"""

import os
import sys
import json
import requests
from pathlib import Path

# Kiểm tra và sửa lỗi import module
def fix_import_issues():
    print("Đang kiểm tra và sửa lỗi import module...")
    
    # Fix lỗi import validate_api_key từ tools.user.api_key_tools
    api_key_tools_path = Path("tools/user/api_key_tools.py")
    if api_key_tools_path.exists():
        with open(api_key_tools_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "validate_api_key" in content:
            print("✅ Hàm validate_api_key đã tồn tại trong api_key_tools.py")
        else:
            print("❌ Không tìm thấy hàm validate_api_key trong api_key_tools.py")
            print("Đang tạo hàm validate_api_key...")
            
            validate_function = """
def validate_api_key(api_key: str) -> Optional[Dict[str, Any]]:
    \"\"\"
    Xác thực API key.
    \"\"\"
    for key_data in mock_api_keys.values():
        if key_data["key"] == api_key and key_data["is_active"]:
            # Kiểm tra xem key đã hết hạn chưa
            if key_data.get("expires_at") and key_data["expires_at"] < datetime.now():
                return None
                
            # Cập nhật last_used_at
            key_data["last_used_at"] = datetime.now()
            
            return {
                "is_valid": True,
                "user_id": key_data["user_id"],
                "key_id": key_data["id"],
                "scopes": []  # Placeholder cho scopes nếu cần
            }
    
    return None
"""
            with open(api_key_tools_path, "a", encoding="utf-8") as f:
                f.write(validate_function)
            print("✅ Đã thêm hàm validate_api_key vào api_key_tools.py")

    # Kiểm tra các import trong apikey_agent.py
    apikey_agent_path = Path("agents/user_agent/sub_agents/apikey_agent.py")
    if apikey_agent_path.exists():
        with open(apikey_agent_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "from tools.user.api_key_tools import" in content and "validate_api_key" in content:
            print("✅ Import validate_api_key trong apikey_agent.py đã tồn tại")
        else:
            print("❌ Lỗi import validate_api_key trong apikey_agent.py")
            # Sửa import statement
            fixed_content = content.replace(
                "from tools.user.api_key_tools import (",
                "from tools.user.api_key_tools import (\n    validate_api_key,"
            )
            with open(apikey_agent_path, "w", encoding="utf-8") as f:
                f.write(fixed_content)
            print("✅ Đã sửa import statement trong apikey_agent.py")

# Kiểm tra API endpoint
def test_api_endpoints():
    print("\nĐang kiểm tra API endpoints...")
    base_url = "http://localhost:8000"
    
    # Kiểm tra health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print(f"✅ Endpoint /health: {response.status_code}")
        else:
            print(f"❌ Endpoint /health: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi kết nối đến /health: {str(e)}")
    
    # Kiểm tra đăng nhập
    try:
        login_data = {
            "username": "thanh@123.com",
            "password": "123456"
        }
        response = requests.post(f"{base_url}/api/user/token", data=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Đăng nhập thành công: {response.status_code}")
            print(f"✅ Token: {token[:10]}...")
            
            # Kiểm tra thông tin người dùng với token
            headers = {"Authorization": f"Bearer {token}"}
            user_response = requests.get(f"{base_url}/api/user/me", headers=headers)
            if user_response.status_code == 200:
                print(f"✅ Lấy thông tin người dùng: {user_response.status_code}")
                print(f"✅ Thông tin: {user_response.json().get('email')}")
            else:
                print(f"❌ Lấy thông tin người dùng: {user_response.status_code}")
        else:
            print(f"❌ Đăng nhập thất bại: {response.status_code}")
            print(f"❌ Lỗi: {response.text}")
            print("=> Hãy chạy seed_data.py để tạo tài khoản test")
    except Exception as e:
        print(f"❌ Lỗi kết nối đến /api/user/token: {str(e)}")

def open_frontend():
    print("\nĐang mở frontend test page...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_path = os.path.join(script_dir, "frontend_test", "frontend_demo.html")
    
    if not os.path.exists(frontend_path):
        print(f"❌ Không tìm thấy file frontend_demo.html tại {frontend_path}")
        return
        
    if sys.platform == "win32":
        os.system(f'start "" "{frontend_path}"')
    elif sys.platform == "darwin":  # macOS
        os.system(f'open "{frontend_path}"')
    else:  # Linux
        os.system(f'xdg-open "{frontend_path}"')
    
    print(f"✅ Đã mở frontend test page: {frontend_path}")

if __name__ == "__main__":
    print("=== SCRIPT KIỂM THỬ FRONTEND VÀ SỬA LỖI ===")
    fix_import_issues()
    test_api_endpoints()
    open_frontend()
    print("\n=== HOÀN THÀNH ===")
    print("Mở trình duyệt và kiểm tra các chức năng trong frontend test page")
    print("Tài khoản test: thanh@123.com / 123456") 