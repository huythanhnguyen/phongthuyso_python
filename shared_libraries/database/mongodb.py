"""
MongoDB Connection Module

Module này cung cấp các hàm để kết nối và thao tác với MongoDB.
"""

import os
import sys
import logging
from typing import Optional
from urllib.parse import quote_plus

# Thêm thư mục gốc vào sys.path để có thể import shared_libraries
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from shared_libraries.logger import get_logger

# Cấu hình logging
logger = get_logger(__name__)

# MongoDB connection string từ môi trường hoặc trực tiếp từ tham số
MONGODB_URI = os.environ.get(
    "MONGODB_URI", 
    "mongodb+srv://hihuythanh:Thanh%401984@cluster0.tp90k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# Tên database mặc định
DEFAULT_DB_NAME = os.environ.get("MONGODB_DB_NAME", "phongthuyso")

# Biến toàn cục để lưu trữ kết nối
_mongodb_client: Optional[AsyncIOMotorClient] = None
_mongodb_db: Optional[AsyncIOMotorDatabase] = None

async def get_database() -> AsyncIOMotorDatabase:
    """
    Lấy đối tượng database MongoDB.
    
    Returns:
        AsyncIOMotorDatabase: Đối tượng database MongoDB
    """
    global _mongodb_client, _mongodb_db
    
    if _mongodb_db is None:
        try:
            logger.info("Đang kết nối tới MongoDB...")
            
            # Mở kết nối mới nếu chưa tồn tại
            if _mongodb_client is None:
                logger.debug(f"Sử dụng connection string: {MONGODB_URI}")
                _mongodb_client = AsyncIOMotorClient(MONGODB_URI)
                
            # Lấy đối tượng database
            _mongodb_db = _mongodb_client[DEFAULT_DB_NAME]
            
            logger.info(f"Kết nối thành công tới database: {DEFAULT_DB_NAME}")
        except Exception as e:
            logger.error(f"Lỗi khi kết nối tới MongoDB: {e}")
            raise
    
    return _mongodb_db

# Đối tượng db để sử dụng trực tiếp
db = None

async def init_db():
    """Khởi tạo kết nối database khi ứng dụng khởi động"""
    global db
    db = await get_database()
    return db

async def close_connection():
    """Đóng kết nối tới MongoDB"""
    global _mongodb_client
    
    if _mongodb_client:
        logger.info("Đóng kết nối tới MongoDB...")
        _mongodb_client.close()
        _mongodb_client = None
        logger.info("Đã đóng kết nối tới MongoDB") 