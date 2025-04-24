import requests
import json
import uuid
import time

BASE_URL = "http://localhost:8000"
TOKEN = None

def setup():
    """Tạo người dùng và lấy token"""
    global TOKEN
    
    # Tạo email ngẫu nhiên để đảm bảo luôn tạo người dùng mới
    random_email = f"test{uuid.uuid4().hex[:8]}@example.com"
    
    # Đăng ký người dùng
    register_url = f"{BASE_URL}/api/user/register"
    register_data = {
        "email": random_email,
        "fullname": "Test User",
        "password": "password123"
    }
    
    try:
        response = requests.post(register_url, json=register_data)
        print(f"Đăng ký: Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Người dùng mới: {random_email}")
            
            # Đăng nhập với người dùng mới
            login_url = f"{BASE_URL}/api/user/token"
            login_data = {
                "username": random_email,
                "password": "password123"
            }
            
            response = requests.post(login_url, data=login_data)
            print(f"Đăng nhập: Status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                TOKEN = data.get("access_token")
                print(f"Đã lấy token: {TOKEN[:10]}...")
                # Thông tin quota ban đầu
                print(f"Quota ban đầu: {data['user'].get('quota_remaining', 'N/A')}")
            else:
                print("Không thể lấy token")
        else:
            print(f"Không thể đăng ký: {response.text}")
    
    except Exception as e:
        print(f"Lỗi setup: {str(e)}")

def check_user_quota():
    """Kiểm tra quota còn lại của người dùng"""
    if not TOKEN:
        print("Không có token, không thể kiểm tra quota")
        return
        
    url = f"{BASE_URL}/api/user/me"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Quota còn lại: {data.get('quota_remaining', 'N/A')}")
        else:
            print(f"Không thể lấy thông tin người dùng: {response.status_code}")
    except Exception as e:
        print(f"Lỗi kiểm tra quota: {str(e)}")

def test_phone_analysis():
    """Test phân tích số điện thoại"""
    url = f"{BASE_URL}/analyze_number"
    params = {"number": "0912345678"}
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        print(f"Status code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        # Kiểm tra quota sau khi gọi API
        check_user_quota()
    except Exception as e:
        print(f"Lỗi: {str(e)}")

def test_chat_api_phone():
    """Test API chat với số điện thoại"""
    url = f"{BASE_URL}/api/chat"
    data = {
        "message": "Phân tích số điện thoại 0912345678",
        "context": {
            "request_agent": "BAT_CUC_LINH_SO"
        }
    }
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        # Kiểm tra quota sau khi gọi API
        check_user_quota()
    except Exception as e:
        print(f"Lỗi: {str(e)}")

def test_chat_api_cccd():
    """Test API chat với 6 số cuối CCCD"""
    url = f"{BASE_URL}/api/chat"
    data = {
        "message": "Phân tích CCCD với 6 số cuối là 123456",
        "context": {
            "request_agent": "BAT_CUC_LINH_SO"
        }
    }
    headers = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Status code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        # Kiểm tra quota sau khi gọi API
        check_user_quota()
    except Exception as e:
        print(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    print("\n--- Setup xác thực ---")
    setup()
    
    print("\n--- Test phân tích số điện thoại qua /analyze_number ---")
    test_phone_analysis()
    time.sleep(1)  # Đợi một chút giữa các request
    
    print("\n--- Test phân tích số điện thoại qua /api/chat ---")
    test_chat_api_phone()
    time.sleep(1)  # Đợi một chút giữa các request
    
    print("\n--- Test phân tích CCCD qua /api/chat ---")
    test_chat_api_cccd() 