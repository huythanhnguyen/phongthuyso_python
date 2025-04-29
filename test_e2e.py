#!/usr/bin/env python3
"""
Script test end-to-end quá trình đăng nhập và sử dụng API chat
"""

import asyncio
import httpx
import json
import time
from urllib.parse import urljoin
from pprint import pprint

BASE_URL = "http://localhost:8000"

async def test_login_and_chat():
    """Test đăng nhập và gửi tin nhắn chat"""
    
    print("=== BẮT ĐẦU KIỂM TRA END-TO-END ===")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Đăng nhập
        login_endpoint = urljoin(BASE_URL, "/api/user/token")
        print(f"\n[1] Đăng nhập vào hệ thống với tài khoản thanh@124.com...")
        
        try:
            login_data = {
                "username": "thanh@124.com",
                "password": "123456"
            }
            
            login_response = await client.post(
                login_endpoint, 
                data=login_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                access_token = login_result.get("access_token")
                print(f"Đăng nhập thành công! Đã nhận được token.")
                print(f"Thông tin người dùng: {login_result.get('user', {}).get('fullname')}")
            else:
                print(f"Đăng nhập thất bại! Status code: {login_response.status_code}")
                print(f"Lỗi: {login_response.text}")
                # Tiếp tục mà không cần token trong trường hợp lỗi đăng nhập
                access_token = None
        except Exception as e:
            print(f"Lỗi khi đăng nhập: {e}")
            access_token = None
        
        # Tạo header với token nếu đăng nhập thành công
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        # Gửi tin nhắn chat
        chat_endpoint = urljoin(BASE_URL, "/api/chat")
        print(f"\n[2] Gửi tin nhắn chat...")
        
        try:
            chat_data = {
                "message": "Phân tích số điện thoại 0912345678 giúp tôi",
                "context": {"test": True}
            }
            
            chat_response = await client.post(
                chat_endpoint,
                json=chat_data,
                headers=headers
            )
            
            if chat_response.status_code == 200:
                chat_result = chat_response.json()
                print(f"Gửi tin nhắn thành công!")
                print("\nPhản hồi từ hệ thống:")
                pprint(chat_result)
            else:
                print(f"Gửi tin nhắn thất bại! Status code: {chat_response.status_code}")
                print(f"Lỗi: {chat_response.text}")
        except Exception as e:
            print(f"Lỗi khi gửi tin nhắn: {e}")
        
        # Thử nhận phản hồi streaming
        stream_endpoint = urljoin(BASE_URL, "/api/chat")
        print(f"\n[3] Thử nghiệm API streaming...")
        
        try:
            session_id = "test_" + str(int(time.time()))
            stream_url = f"{stream_endpoint}?session_id={session_id}&message=Phân tích số điện thoại 0912345678"
            
            print(f"Đang kết nối đến {stream_url}...")
            async with client.stream("GET", stream_url, headers=headers) as stream:
                print("Kết nối streaming thành công! Đang nhận dữ liệu...")
                
                chunk_count = 0
                async for chunk in stream.aiter_text():
                    # Check if chunk contains data
                    if chunk.strip().startswith("data:"):
                        chunk_count += 1
                        data_content = chunk.replace("data:", "").strip()
                        
                        try:
                            message_data = json.loads(data_content)
                            is_final = message_data.get("is_final", False)
                            
                            print(f"\nChunk {chunk_count}:")
                            print(f"Agent: {message_data.get('agent', 'Unknown')}")
                            print(f"Content: {message_data.get('content', '')}")
                            print(f"Is Final: {is_final}")
                            
                            # Dừng sau 5 chunks hoặc khi nhận được tin nhắn cuối cùng để tránh chờ quá lâu
                            if chunk_count >= 5 or is_final:
                                break
                        except json.JSONDecodeError:
                            print(f"Chunk không hợp lệ: {data_content}")
                
                print(f"\nĐã nhận {chunk_count} chunks từ stream API")
                
        except Exception as e:
            print(f"Lỗi khi kết nối streaming: {e}")
    
    print("\n=== KẾT THÚC KIỂM TRA END-TO-END ===")

if __name__ == "__main__":
    asyncio.run(test_login_and_chat()) 