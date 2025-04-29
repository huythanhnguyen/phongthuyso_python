#!/usr/bin/env python3
"""
Script kiểm tra phân tích số điện thoại qua 2 cách khác nhau
"""

import asyncio
import httpx
import json
from pprint import pprint

BASE_URL = "http://localhost:8000"
PHONE_NUMBER = "0931328208"

async def login():
    """Đăng nhập để lấy access token"""
    print("\n=== ĐĂNG NHẬP ===")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        login_endpoint = f"{BASE_URL}/api/user/token"
        
        # Sử dụng thông tin tài khoản đã tạo
        login_data = {
            "username": "thanh@124.com",
            "password": "123456"
        }
        
        try:
            login_response = await client.post(
                login_endpoint, 
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                access_token = login_result.get("access_token")
                print(f"Đăng nhập thành công! Đã nhận được token.")
                return access_token
            else:
                print(f"Đăng nhập thất bại! Status code: {login_response.status_code}")
                print(f"Lỗi: {login_response.text}")
                return None
        except Exception as e:
            print(f"Lỗi khi đăng nhập: {e}")
            return None

async def test_analyze_number(access_token=None):
    """Phân tích số điện thoại qua endpoint analyze_number"""
    
    print("\n=== PHÂN TÍCH QUA ENDPOINT ANALYZE_NUMBER ===")
    
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{BASE_URL}/analyze_number?number={PHONE_NUMBER}"
        print(f"Đang gửi yêu cầu tới: {url}")
        
        try:
            response = await client.get(url, headers=headers)
            
            print(f"Trạng thái: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("\nKết quả phân tích:")
                pprint(result)
            else:
                print(f"Lỗi: {response.text}")
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu: {e}")

async def test_chat_api(access_token=None):
    """Phân tích số điện thoại qua API chat"""
    
    print("\n=== PHÂN TÍCH QUA API CHAT (STREAMING) ===")
    
    headers = {}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        session_id = "test_session"
        # Đảm bảo message rõ ràng chỉ định số điện thoại cần phân tích
        message = f"Phân tích số điện thoại {PHONE_NUMBER} theo phong thủy"
        url = f"{BASE_URL}/api/chat?session_id={session_id}&message={message}"
        
        print(f"Đang kết nối đến: {url}")
        
        try:
            async with client.stream("GET", url, headers=headers) as stream:
                print("Kết nối thành công! Đang nhận phản hồi...\n")
                
                chunk_count = 0
                result = ""
                
                async for chunk in stream.aiter_text():
                    if chunk.strip().startswith("data:"):
                        chunk_count += 1
                        data_content = chunk.replace("data:", "").strip()
                        
                        try:
                            message_data = json.loads(data_content)
                            is_final = message_data.get("is_final", False)
                            content = message_data.get("content", "")
                            
                            print(f"Chunk {chunk_count}:")
                            print(f"Agent: {message_data.get('agent', 'Unknown')}")
                            print(f"Content: {content}")
                            print(f"Is Final: {is_final}\n")
                            
                            result += content + " "
                            
                            if is_final:
                                break
                        except json.JSONDecodeError:
                            print(f"Chunk không hợp lệ: {data_content}")
                
                print(f"Đã nhận {chunk_count} chunks từ stream API")
                print("\nKết quả phân tích tổng hợp:")
                print(result)
                
        except Exception as e:
            print(f"Lỗi khi kết nối streaming: {e}")

async def test_post_chat_api(access_token=None):
    """Phân tích số điện thoại qua POST API chat"""
    
    print("\n=== PHÂN TÍCH QUA POST API CHAT ===")
    
    headers = {
        "Content-Type": "application/json"
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        url = f"{BASE_URL}/api/chat"
        
        chat_data = {
            "message": f"Phân tích chi tiết số điện thoại {PHONE_NUMBER} theo Bát Cục Linh Số",
            "context": {"test": True}
        }
        
        print(f"Đang gửi yêu cầu POST tới: {url}")
        
        try:
            response = await client.post(url, json=chat_data, headers=headers)
            
            print(f"Trạng thái: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("\nKết quả phân tích:")
                pprint(result)
            else:
                print(f"Lỗi: {response.text}")
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu: {e}")

async def main():
    """Hàm chính để chạy cả 3 kiểm tra"""
    access_token = await login()
    await test_analyze_number(access_token)
    await test_chat_api(access_token)
    await test_post_chat_api(access_token)

if __name__ == "__main__":
    asyncio.run(main()) 