"""
Phone Analysis Database Service

Module cung cấp các hàm để lưu trữ và truy xuất kết quả phân tích số điện thoại từ MongoDB.
Phối hợp với phone_analyzer.py để tạo thành bộ công cụ phân tích số điện thoại hoàn chỉnh.
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

# Thêm đường dẫn gốc vào sys.path để import được các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from shared_libraries.models import PhoneAnalysis, PhoneAnalysisResult
from shared_libraries.database.mongodb import db
from shared_libraries.logger import get_logger

# Cấu hình logging
logger = get_logger(__name__)

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
        # Kiểm tra xem đã có phân tích cho số điện thoại này của user chưa
        existing_analysis = await db.phoneAnalysis.find_one({
            "userId": user_id,
            "phoneNumber": phone_number
        })
        
        if existing_analysis:
            # Cập nhật phân tích hiện có
            logger.info(f"Cập nhật phân tích hiện có cho số {phone_number}")
            result = await db.phoneAnalysis.update_one(
                {"_id": existing_analysis["_id"]},
                {"$set": {
                    "result": analysis_result,
                    "geminiResponse": gemini_response,
                    "createdAt": datetime.now()
                }}
            )
            return str(existing_analysis["_id"])
        else:
            # Tạo phân tích mới
            logger.info(f"Tạo phân tích mới cho số {phone_number}")
            
            # Chuẩn bị dữ liệu
            analysis_data = {
                "userId": user_id,
                "phoneNumber": phone_number,
                "result": analysis_result,
                "geminiResponse": gemini_response,
                "createdAt": datetime.now()
            }
            
            # Lưu vào database
            result = await db.phoneAnalysis.insert_one(analysis_data)
            return str(result.inserted_id)
            
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
        result = await db.phoneAnalysis.find_one({
            "userId": user_id,
            "phoneNumber": phone_number
        })
        
        if result:
            # Chuyển ObjectId thành string để serialize được
            result["_id"] = str(result["_id"])
            return result
        return None
        
    except Exception as e:
        logger.error(f"Lỗi khi lấy phân tích số điện thoại: {e}")
        return None

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
        cursor = db.phoneAnalysis.find({"userId": user_id})
        
        # Sắp xếp theo thời gian giảm dần (mới nhất trước)
        cursor.sort("createdAt", -1)
        
        # Giới hạn số lượng kết quả
        cursor.skip(skip).limit(limit)
        
        results = await cursor.to_list(length=limit)
        
        # Chuyển ObjectId thành string để serialize được
        for result in results:
            result["_id"] = str(result["_id"])
            
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
        result = await db.phoneAnalysis.delete_one({
            "userId": user_id,
            "phoneNumber": phone_number
        })
        
        return result.deleted_count > 0
        
    except Exception as e:
        logger.error(f"Lỗi khi xóa phân tích số điện thoại: {e}")
        return False 