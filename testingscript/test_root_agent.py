#!/usr/bin/env python3
"""
Script kiểm tra trực tiếp chức năng process_direct_root_request của RootAgent
"""

import os
import sys
import json
import inspect
import asyncio
from pprint import pprint

# Tạo một instance mới của RootAgent
from agents.root_agent import RootAgent

async def test_root_agent():
    # Tạo một instance mới, không sử dụng instance từ main để tránh các vấn đề về cache
    root_agent = RootAgent(name="Test Root Agent")
    
    # In thông tin về phương thức process_direct_root_request
    print("=== THÔNG TIN PHƯƠNG THỨC ===")
    print(f"Method signature: {inspect.signature(root_agent.process_direct_root_request)}")
    print(f"Method source: \n{inspect.getsource(root_agent.process_direct_root_request)}")
    
    # Tạo các test message
    test_messages = [
        "Xin chào, tôi muốn phân tích số điện thoại 0912345678",
        "Phân tích mối quan hệ giữa ngũ hành và số điện thoại",
        "Tôi muốn biết số nào là số may mắn cho tôi"
    ]
    
    # Test từng tin nhắn
    for i, message in enumerate(test_messages):
        print(f"\n=== TEST MESSAGE {i+1} ===")
        print(f"Message: {message}")
        
        # Tạo request
        request = {
            "message": message,
            "context": {"test": True}
        }
        
        # Gọi phương thức process_direct_root_request
        response = await root_agent.process_direct_root_request(request)
        
        # In kết quả
        print("Response:")
        pprint(response)

if __name__ == "__main__":
    # Chạy hàm test
    asyncio.run(test_root_agent()) 