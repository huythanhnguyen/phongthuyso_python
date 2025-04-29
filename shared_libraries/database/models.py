"""
Database Models Module

Module chứa các hàm tiện ích để thao tác với các collection trong MongoDB.
"""

import os
import sys
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

# Thêm thư mục gốc vào sys.path để có thể import shared_libraries
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from motor.motor_asyncio import AsyncIOMotorCollection
from shared_libraries.logger import get_logger
from shared_libraries.database.mongodb import get_database

# Cấu hình logging
logger = get_logger(__name__)

# Tên các collection
USERS_COLLECTION = "users"
SESSIONS_COLLECTION = "sessions"
ANALYSES_COLLECTION = "analyses"
PAYMENTS_COLLECTION = "payments"
SUBSCRIPTIONS_COLLECTION = "subscriptions"
PLANS_COLLECTION = "plans"
API_KEYS_COLLECTION = "api_keys"

# Hàm utility tổng quát
async def insert_one(collection_name: str, document: Dict[str, Any]) -> str:
    """
    Chèn một document vào collection.
    
    Args:
        collection_name: Tên collection
        document: Document để chèn
        
    Returns:
        str: ID của document đã chèn
    """
    try:
        db = await get_database()
        collection = db[collection_name]
        
        # Thêm ID nếu chưa có
        if "_id" not in document:
            document["_id"] = str(uuid.uuid4())
            
        # Thêm timestamp nếu chưa có
        if "created_at" not in document:
            document["created_at"] = datetime.now()
        if "updated_at" not in document:
            document["updated_at"] = datetime.now()
            
        result = await collection.insert_one(document)
        return document["_id"]
    except Exception as e:
        logger.error(f"Lỗi khi chèn document vào {collection_name}: {e}")
        raise

async def find_one(collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Tìm một document trong collection.
    
    Args:
        collection_name: Tên collection
        query: Truy vấn tìm kiếm
        
    Returns:
        Optional[Dict[str, Any]]: Document tìm thấy hoặc None
    """
    try:
        db = await get_database()
        collection = db[collection_name]
        return await collection.find_one(query)
    except Exception as e:
        logger.error(f"Lỗi khi tìm document trong {collection_name}: {e}")
        raise

async def find_many(
    collection_name: str, 
    query: Dict[str, Any],
    limit: int = 0,
    skip: int = 0,
    sort: Optional[List[tuple]] = None
) -> List[Dict[str, Any]]:
    """
    Tìm nhiều document trong collection.
    
    Args:
        collection_name: Tên collection
        query: Truy vấn tìm kiếm
        limit: Số lượng document tối đa trả về
        skip: Số lượng document bỏ qua
        sort: Danh sách các tuple (field, direction) để sắp xếp
        
    Returns:
        List[Dict[str, Any]]: Danh sách document tìm thấy
    """
    try:
        db = await get_database()
        collection = db[collection_name]
        
        cursor = collection.find(query)
        
        if limit > 0:
            cursor = cursor.limit(limit)
        if skip > 0:
            cursor = cursor.skip(skip)
        if sort:
            cursor = cursor.sort(sort)
            
        return await cursor.to_list(length=None)
    except Exception as e:
        logger.error(f"Lỗi khi tìm nhiều document trong {collection_name}: {e}")
        raise

async def update_one(
    collection_name: str,
    query: Dict[str, Any],
    update: Dict[str, Any],
    upsert: bool = False
) -> bool:
    """
    Cập nhật một document trong collection.
    
    Args:
        collection_name: Tên collection
        query: Truy vấn tìm kiếm
        update: Dữ liệu cập nhật
        upsert: Thêm mới nếu không tìm thấy
        
    Returns:
        bool: True nếu thành công, False nếu không
    """
    try:
        db = await get_database()
        collection = db[collection_name]
        
        # Tự động thêm updated_at
        if "$set" in update:
            update["$set"]["updated_at"] = datetime.now()
        else:
            update["$set"] = {"updated_at": datetime.now()}
            
        result = await collection.update_one(query, update, upsert=upsert)
        return result.modified_count > 0 or (upsert and result.upserted_id is not None)
    except Exception as e:
        logger.error(f"Lỗi khi cập nhật document trong {collection_name}: {e}")
        raise

async def delete_one(collection_name: str, query: Dict[str, Any]) -> bool:
    """
    Xóa một document trong collection.
    
    Args:
        collection_name: Tên collection
        query: Truy vấn tìm kiếm
        
    Returns:
        bool: True nếu thành công, False nếu không
    """
    try:
        db = await get_database()
        collection = db[collection_name]
        result = await collection.delete_one(query)
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Lỗi khi xóa document trong {collection_name}: {e}")
        raise

# Các hàm tiện ích cho từng collection
# Users
async def create_user(user_data: Dict[str, Any]) -> str:
    """Tạo người dùng mới"""
    return await insert_one(USERS_COLLECTION, user_data)

async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Lấy thông tin người dùng theo ID"""
    return await find_one(USERS_COLLECTION, {"_id": user_id})

async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Lấy thông tin người dùng theo email"""
    return await find_one(USERS_COLLECTION, {"email": email})

async def update_user(user_id: str, update_data: Dict[str, Any]) -> bool:
    """Cập nhật thông tin người dùng"""
    return await update_one(USERS_COLLECTION, {"_id": user_id}, {"$set": update_data})

# Sessions
async def create_session(session_data: Dict[str, Any]) -> str:
    """Tạo phiên mới"""
    return await insert_one(SESSIONS_COLLECTION, session_data)

async def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Lấy thông tin phiên theo ID"""
    return await find_one(SESSIONS_COLLECTION, {"_id": session_id})

async def update_session(session_id: str, update_data: Dict[str, Any]) -> bool:
    """Cập nhật thông tin phiên"""
    return await update_one(SESSIONS_COLLECTION, {"_id": session_id}, {"$set": update_data})

async def delete_session(session_id: str) -> bool:
    """Xóa phiên"""
    return await delete_one(SESSIONS_COLLECTION, {"_id": session_id})

# Analyses
async def create_analysis(analysis_data: Dict[str, Any]) -> str:
    """Tạo bản phân tích mới"""
    return await insert_one(ANALYSES_COLLECTION, analysis_data)

async def get_analyses_by_user(user_id: str, limit: int = 10, skip: int = 0) -> List[Dict[str, Any]]:
    """Lấy danh sách phân tích của người dùng"""
    return await find_many(
        ANALYSES_COLLECTION,
        {"user_id": user_id},
        limit=limit,
        skip=skip,
        sort=[("created_at", -1)]
    )

# API Keys
async def create_api_key(api_key_data: Dict[str, Any]) -> str:
    """Tạo API key mới"""
    return await insert_one(API_KEYS_COLLECTION, api_key_data)

async def get_api_key(key: str) -> Optional[Dict[str, Any]]:
    """Lấy thông tin API key"""
    return await find_one(API_KEYS_COLLECTION, {"key": key})

async def get_api_keys_by_user(user_id: str) -> List[Dict[str, Any]]:
    """Lấy danh sách API key của người dùng"""
    return await find_many(API_KEYS_COLLECTION, {"user_id": user_id})

async def delete_api_key(key_id: str) -> bool:
    """Xóa API key"""
    return await delete_one(API_KEYS_COLLECTION, {"_id": key_id})

# Payments and Subscriptions
async def create_payment(payment_data: Dict[str, Any]) -> str:
    """Tạo thanh toán mới"""
    return await insert_one(PAYMENTS_COLLECTION, payment_data)

async def get_payments_by_user(user_id: str) -> List[Dict[str, Any]]:
    """Lấy lịch sử thanh toán của người dùng"""
    return await find_many(PAYMENTS_COLLECTION, {"user_id": user_id}, sort=[("created_at", -1)])

async def create_subscription(subscription_data: Dict[str, Any]) -> str:
    """Tạo gói đăng ký mới"""
    return await insert_one(SUBSCRIPTIONS_COLLECTION, subscription_data)

async def get_active_subscription(user_id: str) -> Optional[Dict[str, Any]]:
    """Lấy gói đăng ký đang hoạt động của người dùng"""
    return await find_one(
        SUBSCRIPTIONS_COLLECTION,
        {
            "user_id": user_id,
            "is_active": True,
            "status": "active"
        }
    )

async def update_subscription(subscription_id: str, update_data: Dict[str, Any]) -> bool:
    """Cập nhật thông tin gói đăng ký"""
    return await update_one(
        SUBSCRIPTIONS_COLLECTION,
        {"_id": subscription_id},
        {"$set": update_data}
    ) 