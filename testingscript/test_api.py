"""
Test API - Phong Thuy So

File này chứa các test case để kiểm tra các endpoint của API Phong Thuy So.
"""

import json
import unittest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch
import requests

from main import app

class TestPhongThuyAPI(unittest.TestCase):
    """Test cases cho các endpoint của API Phong Thuy So."""

    def setUp(self):
        """Thiết lập môi trường test."""
        self.client = TestClient(app)
        self.test_user = {
            "email": "test@example.com",
            "fullname": "Test User",
            "password": "password123"
        }
        self.test_api_key = {
            "name": "Test API Key"
        }
        self.test_payment = {
            "plan_id": "basic",
            "payment_method": "credit_card",
            "amount": 99000,
            "currency": "VND"
        }
        # Đăng ký user mới cho mỗi test
        self.register_test_user()

    def register_test_user(self):
        """Đăng ký user test."""
        try:
            self.client.post("/api/user/register", json=self.test_user)
        except Exception:
            pass  # Có thể user đã tồn tại
    
    def get_access_token(self):
        """Lấy access token."""
        response = self.client.post(
            "/api/user/token",
            data={
                "username": self.test_user["email"],
                "password": self.test_user["password"]
            }
        )
        return response.json().get("access_token", "")

    def test_health_check(self):
        """Test endpoint kiểm tra sức khỏe của API."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("version", data)

    def test_get_agents(self):
        """Test endpoint lấy danh sách các agent."""
        response = self.client.get("/agents")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("agents", data)
        self.assertIsInstance(data["agents"], list)
        
    def test_analyze_number_valid(self):
        """Test phân tích số điện thoại hợp lệ."""
        response = self.client.get("/analyze_number?number=0123456789")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("metadata", data)
        self.assertIn("master_number", data["metadata"])
        
    def test_analyze_number_with_user_data(self):
        """Test phân tích số điện thoại với dữ liệu người dùng."""
        user_data = json.dumps({"name": "Test User", "dob": "1990-01-01"})
        response = self.client.get(f"/analyze_number?number=0123456789&user_data={user_data}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        
    def test_analyze_number_missing_parameter(self):
        """Test phân tích số điện thoại không có tham số bắt buộc."""
        response = self.client.get("/analyze_number")
        self.assertEqual(response.status_code, 422)  # FastAPI trả về 422 cho validation error
        
    def test_analyze_number_invalid_user_data(self):
        """Test phân tích số điện thoại với dữ liệu người dùng không hợp lệ."""
        response = self.client.get("/analyze_number?number=0123456789&user_data=invalid_json")
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["status"], "error")
        
    def test_root_endpoint(self):
        """Test endpoint root."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
    def test_chat_post(self):
        """Test gửi tin nhắn đến agent."""
        chat_data = {
            "message": "Phong thủy số điện thoại 0123456789 như thế nào?",
            "context": {
                "user_id": "user123",
                "session_id": "session456"
            }
        }
        response = self.client.post("/api/chat", json=chat_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
        self.assertIn("content", data)
        self.assertIn("agent", data)
        
    @patch("fastapi.BackgroundTasks.add_task")
    def test_chat_get(self, mock_add_task):
        """Test nhận phản hồi streaming từ agent."""
        response = self.client.get("/api/chat?session_id=session456")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers["content-type"].startswith("text/event-stream"))
        
    def test_chat_get_missing_session_id(self):
        """Test nhận phản hồi streaming không có session_id."""
        response = self.client.get("/api/chat")
        self.assertEqual(response.status_code, 422)
        
    def test_upload_file(self):
        """Test upload file."""
        # Tạo một file test để upload
        test_file_content = b"test file content"
        test_file_path = "test_upload.txt"
        
        try:
            with open(test_file_path, "wb") as f:
                f.write(test_file_content)
                
            with open(test_file_path, "rb") as f:
                files = {"file": ("test_file.txt", f, "text/plain")}
                metadata = json.dumps({"description": "Test file"})
                response = self.client.post(
                    "/api/upload",
                    files=files,
                    data={"type": "text", "metadata": metadata}
                )
                
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["status"], "success")
            self.assertIn("file_id", data)
            self.assertIn("file_url", data)
            
        finally:
            # Dọn dẹp file test
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
                
    def test_upload_file_no_file(self):
        """Test upload không có file."""
        response = self.client.post("/api/upload")
        self.assertEqual(response.status_code, 422)

    # User endpoint tests
    def test_register_user(self):
        """Test đăng ký người dùng."""
        new_user = {
            "email": f"newuser{os.urandom(4).hex()}@example.com",
            "fullname": "New Test User",
            "password": "password123"
        }
        response = self.client.post("/api/user/register", json=new_user)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], new_user["email"])
        self.assertEqual(data["fullname"], new_user["fullname"])
        self.assertTrue(data["is_active"])
        self.assertFalse(data["is_premium"])

    def test_login_user(self):
        """Test đăng nhập người dùng."""
        response = self.client.post(
            "/api/user/token",
            data={
                "username": self.test_user["email"],
                "password": self.test_user["password"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")
        self.assertIn("user", data)

    def test_get_current_user(self):
        """Test lấy thông tin người dùng hiện tại."""
        token = self.get_access_token()
        response = self.client.get(
            "/api/user/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email"], self.test_user["email"])

    def test_update_user(self):
        """Test cập nhật thông tin người dùng."""
        token = self.get_access_token()
        update_data = {"fullname": "Updated Name"}
        response = self.client.put(
            "/api/user/me",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["fullname"], update_data["fullname"])

    # API Key tests
    def test_create_api_key(self):
        """Test tạo API key."""
        token = self.get_access_token()
        response = self.client.post(
            "/api/apikeys",
            json=self.test_api_key,
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], self.test_api_key["name"])
        self.assertTrue(data["key"].startswith("pts_"))
        self.assertTrue(data["is_active"])

    def test_list_api_keys(self):
        """Test lấy danh sách API key."""
        token = self.get_access_token()
        # Tạo một API key trước
        self.client.post(
            "/api/apikeys",
            json=self.test_api_key,
            headers={"Authorization": f"Bearer {token}"}
        )
        response = self.client.get(
            "/api/apikeys",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    # Payment tests
    def test_list_plans(self):
        """Test lấy danh sách các gói dịch vụ."""
        response = self.client.get("/api/payment/plans")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)
        # Kiểm tra có các gói cơ bản
        plan_ids = [plan["id"] for plan in data]
        for expected_plan in ["free", "basic", "premium"]:
            self.assertIn(expected_plan, plan_ids)

    def test_get_plan(self):
        """Test lấy thông tin chi tiết của một gói dịch vụ."""
        response = self.client.get("/api/payment/plans/basic")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "basic")
        self.assertIn("price", data)
        self.assertIn("features", data)

    def test_create_payment(self):
        """Test tạo một thanh toán mới."""
        token = self.get_access_token()
        response = self.client.post(
            "/api/payment",
            json=self.test_payment,
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["plan_id"], self.test_payment["plan_id"])
        self.assertEqual(data["amount"], self.test_payment["amount"])
        self.assertEqual(data["status"], "completed")
        self.assertIsNotNone(data["transaction_id"])

    def test_get_payment_history(self):
        """Test lấy lịch sử thanh toán."""
        token = self.get_access_token()
        # Tạo một thanh toán trước
        self.client.post(
            "/api/payment",
            json=self.test_payment,
            headers={"Authorization": f"Bearer {token}"}
        )
        response = self.client.get(
            "/api/payment/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertTrue(len(data) > 0)

    def test_get_active_subscription(self):
        """Test lấy thông tin gói đăng ký hiện tại."""
        token = self.get_access_token()
        # Tạo một thanh toán trước để có subscription
        self.client.post(
            "/api/payment",
            json=self.test_payment,
            headers={"Authorization": f"Bearer {token}"}
        )
        response = self.client.get(
            "/api/payment/subscription",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["plan_id"], self.test_payment["plan_id"])
        self.assertEqual(data["status"], "active")
        self.assertTrue(data["is_active"])
        

def test_phone_analysis():
    """Test phân tích số điện thoại"""
    url = f"{BASE_URL}/analyze_number"
    params = {"number": "0912345678"}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
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
    
    try:
        response = requests.post(url, json=data)
        print(f"Status code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Lỗi: {str(e)}")

def test_chat_api_cccd():
    """Test API chat với 6 số cuối CCCD"""
    url = f"{BASE_URL}/api/chat"
    data = {
        "message": "Phân tích CCCD 123456",
        "context": {
            "request_agent": "BAT_CUC_LINH_SO"
        }
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    print("\n--- Test phân tích số điện thoại qua /analyze_number ---")
    test_phone_analysis()
    
    print("\n--- Test phân tích số điện thoại qua /api/chat ---")
    test_chat_api_phone()
    
    print("\n--- Test phân tích CCCD qua /api/chat ---")
    test_chat_api_cccd() 