#!/usr/bin/env python3
"""
Script tạo tài khoản test để sử dụng trong quá trình kiểm thử end-to-end
"""

import asyncio
import httpx
from pprint import pprint

BASE_URL = "http://localhost:8000"

async def create_test_user():
    """Tạo người dùng test"""
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Đăng ký người dùng
        register_url = f"{BASE_URL}/api/user/register"
        
        user_data = {
            "email": "thanh@124.com",
            "name": "Thanh Test",
            "password": "123456"
        }
        
        print(f"Đang tạo người dùng test với email {user_data['email']}...")
        
        try:
            response = await client.post(register_url, json=user_data)
            
            if response.status_code == 200:
                result = response.json()
                print("Tạo người dùng thành công!")
                pprint(result)
            else:
                print(f"Không thể tạo người dùng, mã lỗi: {response.status_code}")
                print(f"Nội dung lỗi: {response.text}")
                
                if response.status_code == 400 and "already registered" in response.text:
                    print("Người dùng có thể đã tồn tại, tiếp tục với tài khoản hiện có.")
        except Exception as e:
            print(f"Lỗi khi tạo người dùng: {e}")

if __name__ == "__main__":
    asyncio.run(create_test_user()) 