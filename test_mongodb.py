"""
MongoDB Connection Test Script

Script để kiểm tra kết nối đến MongoDB.
"""

import asyncio
import os
import sys

# Import các module cần thiết
from shared_libraries.database.mongodb import get_database, close_connection
from shared_libraries.logger import get_logger

# Cấu hình logger
logger = get_logger("test_mongodb_connection")

async def test_connection():
    """Kiểm tra kết nối đến MongoDB"""
    try:
        logger.info("Bắt đầu kiểm tra kết nối MongoDB...")
        
        # Kết nối và lấy danh sách collection
        db = await get_database()
        collections = await db.list_collection_names()
        
        logger.info(f"Kết nối thành công! Các collection có sẵn: {collections}")
        
        # Tạo một collection test nếu chưa tồn tại
        if "test_collection" not in collections:
            logger.info("Tạo collection test...")
            await db.create_collection("test_collection")
            logger.info("Đã tạo collection test thành công!")
        
        # Thêm một document test
        test_collection = db["test_collection"]
        result = await test_collection.insert_one({"test": "data", "timestamp": "now"})
        
        logger.info(f"Đã thêm document test với ID: {result.inserted_id}")
        
        # Đọc document test
        test_doc = await test_collection.find_one({"test": "data"})
        logger.info(f"Đọc document test: {test_doc}")
        
        # Xóa document test
        await test_collection.delete_one({"test": "data"})
        logger.info("Đã xóa document test")
        
        logger.info("Kiểm tra kết nối MongoDB thành công!")
    except Exception as e:
        logger.error(f"Lỗi khi kiểm tra kết nối MongoDB: {e}")
    finally:
        # Đóng kết nối
        await close_connection()
        logger.info("Đã đóng kết nối MongoDB")

if __name__ == "__main__":
    # Chạy kiểm tra kết nối
    asyncio.run(test_connection()) 