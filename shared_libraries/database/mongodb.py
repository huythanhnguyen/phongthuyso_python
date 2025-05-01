"""
MongoDB Connection Module

Module này cung cấp các hàm để kết nối và thao tác với MongoDB.
"""

import os
import sys
import logging
import time
import asyncio
from typing import Optional, Dict, Any
from urllib.parse import quote_plus
from functools import lru_cache

# Thêm thư mục gốc vào sys.path để có thể import shared_libraries
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout
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

# MongoDB client options để tối ưu kết nối
MONGODB_OPTIONS = {
    "serverSelectionTimeoutMS": 3000,    # Giảm thời gian chọn server
    "connectTimeoutMS": 5000,            # Giảm timeout kết nối
    "socketTimeoutMS": 15000,            # Giảm timeout socket
    "maxPoolSize": 50,                   # Tăng pool size cho nhiều request
    "minPoolSize": 10,                   # Tăng kết nối tối thiểu
    "maxIdleTimeMS": 60000,              # Tăng thời gian idle
    "waitQueueTimeoutMS": 3000,          # Giảm thời gian chờ kết nối
    "heartbeatFrequencyMS": 10000,       # Giảm thời gian kiểm tra heartbeat
    "retryWrites": True,                 # Tự động thử lại các thao tác ghi khi thất bại
    "w": "majority",                     # Đảm bảo ghi vào đa số các node
    "readPreference": "secondaryPreferred", # Đọc từ secondary khi có thể
    "retryReads": True,                  # Tự động thử lại khi đọc lỗi
    "appName": "PhongThuySoApp"          # Tên ứng dụng để dễ theo dõi
}

# Biến toàn cục để lưu trữ kết nối
_mongodb_client: Optional[AsyncIOMotorClient] = None
_mongodb_db: Optional[AsyncIOMotorDatabase] = None

# Biến toàn cục để theo dõi kết nối
_connection_attempts = 0
_last_connection_time = 0
_max_retry_attempts = 3
_retry_delay_base = 1  # Thời gian cơ bản giữa các lần retry (giây)

async def get_database() -> AsyncIOMotorDatabase:
    """
    Lấy đối tượng database MongoDB với cơ chế retry.
    
    Returns:
        AsyncIOMotorDatabase: Đối tượng database MongoDB
    """
    global _mongodb_client, _mongodb_db, _connection_attempts, _last_connection_time
    
    if _mongodb_db is None or _connection_attempts >= _max_retry_attempts:
        retry_count = 0
        while retry_count < _max_retry_attempts:
            try:
                logger.info(f"Đang kết nối tới MongoDB (lần thử {retry_count + 1})...")
                
                # Đảm bảo chỉ tạo client mới khi cần
                if _mongodb_client is None:
                    # Thêm timestamp để track thời gian kết nối
                    _last_connection_time = time.time()
                    logger.debug(f"Sử dụng connection string: {MONGODB_URI}")
                    _mongodb_client = AsyncIOMotorClient(MONGODB_URI, **MONGODB_OPTIONS)
                
                # Thử ping server để đảm bảo kết nối hoạt động
                await _mongodb_client.admin.command('ping')
                    
                # Lấy đối tượng database
                _mongodb_db = _mongodb_client[DEFAULT_DB_NAME]
                _connection_attempts = 0  # Reset số lần thử kết nối
                
                logger.info(f"Kết nối thành công tới database: {DEFAULT_DB_NAME}")
                return _mongodb_db
                
            except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout) as e:
                retry_count += 1
                _connection_attempts += 1
                
                # Tính thời gian chờ theo phương pháp exponential backoff
                retry_delay = _retry_delay_base * (2 ** (retry_count - 1))
                
                logger.warning(f"Lỗi kết nối MongoDB (lần {retry_count}): {e}. Thử lại sau {retry_delay}s")
                
                # Đóng client cũ nếu có
                if _mongodb_client:
                    _mongodb_client.close()
                    _mongodb_client = None
                
                if retry_count < _max_retry_attempts:
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"Đã thử kết nối {_max_retry_attempts} lần nhưng thất bại")
                    raise
            
            except Exception as e:
                logger.error(f"Lỗi không xác định khi kết nối tới MongoDB: {e}")
                raise
    
    return _mongodb_db

# Thêm cache cho đối tượng database
cache_ttl = 60 * 60  # Cache sẽ hết hạn sau 1 giờ
@lru_cache(maxsize=1)
async def get_cached_database() -> AsyncIOMotorDatabase:
    """
    Lấy đối tượng database MongoDB với cache để giảm thiểu chi phí kết nối.
    
    Returns:
        AsyncIOMotorDatabase: Đối tượng database MongoDB đã được cache
    """
    return await get_database()

# Đối tượng db để sử dụng trực tiếp
db = None

async def init_db():
    """Khởi tạo kết nối database khi ứng dụng khởi động"""
    global db
    db = await get_database()
    
    # Tạo các collection cần thiết nếu chưa tồn tại
    collections = await db.list_collection_names()
    
    # Collection user
    if "user" not in collections:
        logger.info("Tạo collection 'user'...")
        await db.create_collection("user")
        # Tạo index cho email để tìm kiếm nhanh và đảm bảo unique
        await db.user.create_index("email", unique=True)
        logger.info("Đã tạo collection 'user' thành công")
    
    # Collection subscription
    if "subscription" not in collections:
        logger.info("Tạo collection 'subscription'...")
        await db.create_collection("subscription")
        # Tạo index cho user_id để tìm kiếm nhanh
        await db.subscription.create_index("user_id")
        logger.info("Đã tạo collection 'subscription' thành công")
    
    # Collection phoneAnalysis - lưu kết quả phân tích số điện thoại
    if "phoneAnalysis" not in collections:
        logger.info("Tạo collection 'phoneAnalysis'...")
        await db.create_collection("phoneAnalysis")
        # Tạo index để tìm kiếm nhanh theo userId và phoneNumber
        await db.phoneAnalysis.create_index([("userId", 1), ("phoneNumber", 1)])
        # Tạo index theo thời gian tạo để sắp xếp theo thời gian
        await db.phoneAnalysis.create_index([("createdAt", -1)])
        # Thêm index ttl để tự động xóa các bản ghi cũ (sau 90 ngày)
        await db.phoneAnalysis.create_index([("createdAt", 1)], expireAfterSeconds=7776000)
        logger.info("Đã tạo collection 'phoneAnalysis' thành công")
    
    return db

async def close_connection():
    """Đóng kết nối tới MongoDB"""
    global _mongodb_client
    
    if _mongodb_client:
        logger.info("Đóng kết nối tới MongoDB...")
        _mongodb_client.close()
        _mongodb_client = None
        logger.info("Đã đóng kết nối tới MongoDB")

async def execute_with_retry(operation, *args, **kwargs):
    """
    Thực thi một operation MongoDB với cơ chế retry
    
    Args:
        operation: Hàm MongoDB cần thực thi
        *args, **kwargs: Tham số cho hàm
        
    Returns:
        Any: Kết quả của operation
    """
    retry_count = 0
    last_exception = None
    
    while retry_count < _max_retry_attempts:
        try:
            return await operation(*args, **kwargs)
        except (ConnectionFailure, ServerSelectionTimeoutError, NetworkTimeout) as e:
            retry_count += 1
            retry_delay = _retry_delay_base * (2 ** (retry_count - 1))  # Exponential backoff
            
            logger.warning(f"Lỗi khi thực thi MongoDB operation: {e}. Thử lại lần {retry_count} sau {retry_delay}s")
            last_exception = e
            
            if retry_count < _max_retry_attempts:
                await asyncio.sleep(retry_delay)
            else:
                logger.error(f"Đã thử lại {_max_retry_attempts} lần nhưng thất bại: {e}")
                raise last_exception
        except Exception as e:
            logger.error(f"Lỗi không xác định khi thực thi MongoDB operation: {e}")
            raise
    
    if last_exception:
        raise last_exception
    raise Exception("Lỗi không xác định trong quá trình retry") 