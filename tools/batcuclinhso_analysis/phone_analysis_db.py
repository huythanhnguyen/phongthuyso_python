"""
Phone Analysis Database Service

Module cung cấp các hàm để lưu trữ và truy xuất kết quả phân tích số điện thoại từ MongoDB.
Phối hợp với phone_analyzer.py để tạo thành bộ công cụ phân tích số điện thoại hoàn chỉnh.
"""

import os
import sys
import logging
import time
import hashlib
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from functools import lru_cache

# Thêm đường dẫn gốc vào sys.path để import được các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared_libraries.models import PhoneAnalysis, PhoneAnalysisResult
from shared_libraries.database.mongodb import db, get_cached_database, execute_with_retry
from shared_libraries.logger import get_logger

# Cấu hình logging
logger = get_logger(__name__)

# Cấu hình cache
CACHE_TTL = 3600  # Thời gian cache hết hạn (1 giờ)
CACHE_SIZE = 500  # Số lượng kết quả tối đa trong cache

# Dictionary để lưu trữ cache in-memory
_memory_cache = {}

async def save_phone_analysis(user_id: str, phone_number: str, 
                              analysis_result: Dict[str, Any], 
                              gemini_response: Optional[str] = None) -> str:
    """
    Lưu kết quả phân tích số điện thoại vào database.
    
    Args:
        user_id: ID của người dùng
        phone_number: Số điện thoại được phân tích
        analysis_result: Kết quả phân tích chi tiết
        gemini_response: Phản hồi từ Gemini (không bắt buộc)
        
    Returns:
        str: ID của document đã lưu
    """
    try:
        start_time = time.time()
        phone_number = "".join(filter(str.isdigit, phone_number))

        # Kiểm tra xem đã có phân tích cho số điện thoại này của user chưa
        existing_analysis = await execute_with_retry(
            db.phoneAnalysis.find_one, {"userId": user_id, "phoneNumber": phone_number}
        )
        if existing_analysis:
            logger.info(f"Cập nhật phân tích hiện có cho số {phone_number}")
            await execute_with_retry(
                db.phoneAnalysis.update_one,
                {"_id": existing_analysis["_id"]},
                {"$set": {
                    "result": analysis_result,
                    "geminiResponse": gemini_response,
                    "createdAt": datetime.now(),
                    "updatedAt": datetime.now()
                }}
            )
            doc_id = str(existing_analysis["_id"])
        else:
            logger.info(f"Tạo phân tích mới cho số {phone_number}")
            analysis_data = {
                "userId": user_id,
                "phoneNumber": phone_number,
                "result": analysis_result,
                "geminiResponse": gemini_response,
                "createdAt": datetime.now(),
                "updatedAt": datetime.now()
            }
            result = await execute_with_retry(db.phoneAnalysis.insert_one, analysis_data)
            doc_id = str(result.inserted_id)
        invalidate_phone_analysis_cache(user_id, phone_number)
        elapsed = time.time() - start_time
        logger.debug(f"Lưu phân tích mất {elapsed:.3f}s")
        return doc_id
    except Exception as e:
        logger.error(f"Lỗi khi lưu phân tích số điện thoại: {e}")
        raise

async def get_phone_analysis(user_id: str, phone_number: str) -> Optional[Dict[str, Any]]:
    """
    Lấy kết quả phân tích số điện thoại từ database.
    
    Args:
        user_id: ID của người dùng
        phone_number: Số điện thoại cần lấy kết quả
        
    Returns:
        Optional[Dict[str, Any]]: Kết quả phân tích nếu tìm thấy, None nếu không có
    """
    try:
        phone_number = "".join(filter(str.isdigit, phone_number))
        start_time = time.time()
        result = await execute_with_retry(
            db.phoneAnalysis.find_one, {"userId": user_id, "phoneNumber": phone_number}
        )
        if result:
            result["_id"] = str(result["_id"])
            elapsed = time.time() - start_time
            logger.debug(f"Lấy phân tích từ DB mất {elapsed:.3f}s")
            return result
        return None
    except Exception as e:
        logger.error(f"Lỗi khi lấy phân tích số điện thoại: {e}")
        return None

def get_cache_key(user_id: str, phone_number: str) -> str:
    """Tạo key cho cache từ user_id và phone_number"""
    phone_number = "".join(filter(str.isdigit, phone_number))
    return f"phone_analysis:{user_id}:{phone_number}"

async def get_cached_phone_analysis(user_id: str, phone_number: str) -> Optional[Dict[str, Any]]:
    """
    Lấy kết quả phân tích số điện thoại từ cache hoặc database.
    
    Args:
        user_id: ID của người dùng
        phone_number: Số điện thoại cần lấy kết quả
        
    Returns:
        Optional[Dict[str, Any]]: Kết quả phân tích nếu tìm thấy, None nếu không có
    """
    phone_number = "".join(filter(str.isdigit, phone_number))
    cache_key = get_cache_key(user_id, phone_number)
    cached_data = _memory_cache.get(cache_key)
    if cached_data:
        cached_time, cached_result = cached_data
        if time.time() - cached_time < CACHE_TTL:
            logger.debug(f"Cache hit for {cache_key}")
            return cached_result
        else:
            del _memory_cache[cache_key]
    start_time = time.time()
    result = await get_phone_analysis(user_id, phone_number)
    if result:
        _memory_cache[cache_key] = (time.time(), result)
        if len(_memory_cache) > CACHE_SIZE:
            sorted_cache = sorted(_memory_cache.items(), key=lambda x: x[1][0])
            items_to_remove = sorted_cache[:int(CACHE_SIZE * 0.2)]
            for key, _ in items_to_remove:
                del _memory_cache[key]
    elapsed = time.time() - start_time
    logger.debug(f"Cache miss for {cache_key}, retrieval took {elapsed:.3f}s")
    return result

def invalidate_phone_analysis_cache(user_id: str, phone_number: str):
    """
    Xóa cache khi có cập nhật phân tích.
    
    Args:
        user_id: ID của người dùng
        phone_number: Số điện thoại cần xóa cache
    """
    phone_number = "".join(filter(str.isdigit, phone_number))
    cache_key = get_cache_key(user_id, phone_number)
    if cache_key in _memory_cache:
        del _memory_cache[cache_key]
        logger.debug(f"Invalidated cache for {cache_key}")

async def get_user_analyses(user_id: str, limit: int = 10, skip: int = 0) -> List[Dict[str, Any]]:
    """
    Lấy danh sách các phân tích của một người dùng.
    
    Args:
        user_id: ID của người dùng
        limit: Số lượng kết quả tối đa
        skip: Số lượng kết quả bỏ qua (dùng cho phân trang)
        
    Returns:
        List[Dict[str, Any]]: Danh sách kết quả phân tích
    """
    try:
        start_time = time.time()
        projection = {
            "userId": 1, 
            "phoneNumber": 1, 
            "createdAt": 1, 
            "updatedAt": 1,
            "result.total_score": 1,
            "result.luck_level": 1
        }
        cursor = db.phoneAnalysis.find(
            {"userId": user_id},
            projection=projection
        )
        cursor.sort("createdAt", -1)
        cursor.skip(skip).limit(limit)
        results = await execute_with_retry(cursor.to_list, length=limit)
        for result in results:
            result["_id"] = str(result["_id"])
        elapsed = time.time() - start_time
        logger.debug(f"Lấy danh sách phân tích mất {elapsed:.3f}s")
        return results
    except Exception as e:
        logger.error(f"Lỗi khi lấy danh sách phân tích: {e}")
        return []

async def delete_phone_analysis(user_id: str, phone_number: str) -> bool:
    """
    Xóa một phân tích số điện thoại.
    
    Args:
        user_id: ID của người dùng
        phone_number: Số điện thoại cần xóa phân tích
        
    Returns:
        bool: True nếu xóa thành công, False nếu thất bại
    """
    try:
        phone_number = "".join(filter(str.isdigit, phone_number))
        result = await execute_with_retry(
            db.phoneAnalysis.delete_one,
            {"userId": user_id, "phoneNumber": phone_number}
        )
        invalidate_phone_analysis_cache(user_id, phone_number)
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Lỗi khi xóa phân tích số điện thoại: {e}")
        return False 