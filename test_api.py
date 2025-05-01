import requests
import json

BASE_URL = "http://localhost:8000"

def test_login():
    """Test đăng nhập và xác thực token"""
    print("=== TEST ĐĂNG NHẬP VÀ XÁC THỰC ===")
    
    # 1. Đăng nhập
    print("\n1. Test đăng nhập:")
    login_data = {
        "username": "testuser@example.com",
        "password": "123456"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/user/token",
            data=login_data
        )
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            token = response.json()["access_token"]
            
            # 2. Test xác thực token
            print("\n2. Test xác thực token:")
            headers = {"Authorization": f"Bearer {token}"}
            
            me_response = requests.get(
                f"{BASE_URL}/api/user/me",
                headers=headers
            )
            
            print(f"Status code: {me_response.status_code}")
            print(f"Response: {json.dumps(me_response.json(), indent=2)}")
            
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    test_login() 