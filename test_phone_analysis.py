#!/usr/bin/env python3
"""
Script kiểm tra chức năng phân tích số điện thoại thông qua RootAgent và BatCucLinhSoAgent
"""

import json
import requests
import asyncio
import logging
import time
from typing import Optional, Dict, Any

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("test_phone_analysis")

# URL cơ sở của API
BASE_URL = "http://localhost:8000"

# Thông tin tài khoản test 
TEST_EMAIL = "thanh@123.com"
TEST_PASSWORD = "123456"

def get_auth_token() -> Optional[str]:
    """Lấy token xác thực từ API"""
    logger.info("=== ĐĂNG NHẬP ===")
    
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
            logger.info(f"✅ Đăng nhập thành công, token: {token[:20]}...")
            return token
        else:
            logger.error(f"❌ Đăng nhập thất bại: {response.status_code}")
            logger.error(f"❌ Lỗi: {response.text}")
            return None
    except Exception as e:
        logger.error(f"❌ Lỗi kết nối khi đăng nhập: {str(e)}")
        return None

def test_phone_analysis_direct(token: str) -> bool:
    """
    Kiểm tra phân tích số điện thoại trực tiếp qua endpoint /analyze_number
    
    Tuân thủ quy tắc cursor.rule, không sử dụng mock data và tận dụng API hiện có
    """
    logger.info("\n==== KIỂM TRA PHÂN TÍCH SỐ ĐIỆN THOẠI TRỰC TIẾP ====")
    
    if not token:
        logger.error("❌ Không có token xác thực, bỏ qua kiểm tra")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Các số điện thoại cần kiểm tra
    test_numbers = [
        "0912345678",
        "0987654321",
        "0369876543"
    ]
    
    success_count = 0
    
    for i, number in enumerate(test_numbers):
        logger.info(f"\n=== TEST NUMBER {i+1}: {number} ===")
        
        try:
            # Gọi API phân tích số điện thoại
            response = requests.get(
                f"{BASE_URL}/analyze_number",
                headers=headers,
                params={"number": number}
            )
            
            logger.info(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info("JSON Response:")
                    logger.info(json.dumps(data, indent=2))
                    
                    # Kiểm tra nội dung phản hồi
                    if data.get("status") == "success" and data.get("content"):
                        logger.info(f"✅ Phân tích thành công: {data.get('content')[:100]}...")
                        success_count += 1
                    else:
                        logger.warning(f"⚠️ Phản hồi không có nội dung phân tích")
                    
                except json.JSONDecodeError:
                    logger.error(f"❌ Lỗi parse JSON: {response.text}")
                
            else:
                logger.error(f"❌ Gọi API thất bại: {response.status_code}")
                logger.error(f"❌ Lỗi: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ Lỗi kết nối đến API: {str(e)}")
        
        logger.info("=" * 50)
        # Chờ giữa các lần gọi API
        time.sleep(1)
    
    logger.info("\n==== KẾT QUẢ PHÂN TÍCH SỐ ĐIỆN THOẠI TRỰC TIẾP ====")
    logger.info(f"✓ Đã kiểm tra {len(test_numbers)} số điện thoại")
    logger.info(f"✓ Thành công: {success_count}/{len(test_numbers)}")
    logger.info("=" * 50)
    
    return success_count == len(test_numbers)

def test_phone_analysis_via_chat(token: str) -> bool:
    """
    Kiểm tra phân tích số điện thoại gián tiếp qua chat API
    
    Tuân thủ quy tắc cursor.rule, tận dụng endpoint chat API có sẵn
    """
    logger.info("\n==== KIỂM TRA PHÂN TÍCH SỐ ĐIỆN THOẠI QUA CHAT ====")
    
    if not token:
        logger.error("❌ Không có token xác thực, bỏ qua kiểm tra")
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Các câu hỏi chứa số điện thoại
    test_messages = [
        "Xin chào, tôi muốn phân tích số điện thoại 0912345678",
        "Phân tích ý nghĩa của số 0987654321 theo phong thủy",
        "Số 0369876543 có hợp mệnh của tôi không?"
    ]
    
    session_id = None
    success_count = 0
    
    for i, message in enumerate(test_messages):
        logger.info(f"\n=== TEST MESSAGE {i+1} ===")
        logger.info(f"Message: {message}")
        
        try:
            # Tạo request body
            request_body = {
                "message": message,
                "context": {
                    "session_id": session_id,
                    "test_id": i+1,
                    "request_agent": "BAT_CUC_LINH_SO"  # Yêu cầu RootAgent định tuyến tới BatCucLinhSoAgent
                }
            }
            
            # Gửi tin nhắn và nhận response
            response = requests.post(
                f"{BASE_URL}/api/chat",
                headers=headers,
                json=request_body
            )
            
            logger.info(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info("JSON Response:")
                    logger.info(json.dumps(data, indent=2))
                    
                    # Lưu session_id từ metadata
                    if data.get("metadata") and data.get("metadata").get("session_id"):
                        session_id = data.get("metadata").get("session_id")
                    
                    # Kiểm tra nội dung phản hồi
                    if data.get("content") and "điện thoại" in data.get("content", "").lower():
                        logger.info(f"✅ Phản hồi có nội dung phân tích số điện thoại")
                        success_count += 1
                    else:
                        logger.warning(f"⚠️ Phản hồi không có nội dung phân tích số điện thoại")
                    
                except json.JSONDecodeError:
                    logger.error(f"❌ Lỗi parse JSON: {response.text}")
                
            else:
                logger.error(f"❌ Gửi tin nhắn thất bại: {response.status_code}")
                logger.error(f"❌ Lỗi: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ Lỗi kết nối đến API chat: {str(e)}")
        
        logger.info("=" * 50)
        # Chờ giữa các lần gọi API
        time.sleep(1)
    
    logger.info("\n==== KẾT QUẢ PHÂN TÍCH QUA CHAT ====")
    logger.info(f"✓ Đã kiểm tra {len(test_messages)} tin nhắn")
    logger.info(f"✓ Thành công: {success_count}/{len(test_messages)}")
    logger.info("=" * 50)
    
    return success_count == len(test_messages)

def main():
    """Hàm chính thực thi các bài kiểm tra"""
    logger.info("=== SCRIPT KIỂM TRA PHÂN TÍCH SỐ ĐIỆN THOẠI ===")
    
    # Kiểm tra kết nối đến server
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            logger.info("✅ Kết nối đến server thành công")
        else:
            logger.error("❌ Kết nối đến server thất bại")
            logger.error("Hãy đảm bảo server đang chạy")
            return
    except Exception as e:
        logger.error(f"❌ Không thể kết nối đến server: {str(e)}")
        logger.error("Hãy đảm bảo server đang chạy")
        return
    
    # Lấy token xác thực
    token = get_auth_token()
    
    # Chạy các bài kiểm tra
    direct_test_result = test_phone_analysis_direct(token)
    chat_test_result = test_phone_analysis_via_chat(token)
    
    # Tổng hợp kết quả
    logger.info("\n=== TỔNG HỢP KẾT QUẢ ===")
    logger.info(f"✓ Phân tích số trực tiếp: {'Thành công' if direct_test_result else 'Thất bại'}")
    logger.info(f"✓ Phân tích số qua chat: {'Thành công' if chat_test_result else 'Thất bại'}")
    
    if direct_test_result and chat_test_result:
        logger.info("✅ TẤT CẢ CÁC BÀI KIỂM TRA ĐỀU THÀNH CÔNG")
    else:
        logger.warning("⚠️ MỘT SỐ BÀI KIỂM TRA THẤT BẠI")
    
    logger.info("=== HOÀN THÀNH ===")

if __name__ == "__main__":
    main() 