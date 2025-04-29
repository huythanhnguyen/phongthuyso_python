#!/usr/bin/env python3
"""
Script kiểm tra danh sách người dùng trong MongoDB
"""

import asyncio
from pprint import pprint
import os
import sys

# Thêm thư mục gốc vào sys.path để import được các module từ project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def check_mongodb_users():
    """Kết nối tới MongoDB và hiển thị danh sách người dùng"""
    
    print("=== KIỂM TRA DANH SÁCH NGƯỜI DÙNG TRONG MONGODB ===")
    
    try:
        # Import module database từ project
        from shared_libraries.database.mongodb import init_db, get_database, close_connection
        
        # Khởi tạo kết nối MongoDB
        print("Đang kết nối tới MongoDB...")
        db = await init_db()
        print("Kết nối thành công!")
        
        # Kiểm tra danh sách collections
        collection_names = await db.list_collection_names()
        print(f"\nDanh sách collections: {collection_names}")
        
        # Chọn collection "user" 
        users_collection_name = "user"
        if users_collection_name not in collection_names:
            print(f"Không tìm thấy collection '{users_collection_name}'!")
            print("\nDanh sách collections có sẵn:")
            for name in collection_names:
                print(f"- {name}")
            return
            
        # Lấy collection users
        users_collection = db[users_collection_name]
        
        # Đếm số lượng người dùng
        user_count = await users_collection.count_documents({})
        print(f"\nSố lượng người dùng trong collection '{users_collection_name}': {user_count}")
        
        # Lấy danh sách người dùng
        print("\nDanh sách người dùng:")
        
        users_cursor = users_collection.find({})
        users = await users_cursor.to_list(length=100)
        
        if users:
            for i, user in enumerate(users):
                print(f"\n--- Người dùng {i+1} ---")
                # Loại bỏ mật khẩu trước khi hiển thị
                if "hashed_password" in user:
                    user["hashed_password"] = "***HIDDEN***"
                pprint(user)
        else:
            print(f"Không có người dùng nào trong collection '{users_collection_name}'!")
        
        # Đóng kết nối MongoDB
        await close_connection()
        print("\nĐã đóng kết nối MongoDB!")
        
    except Exception as e:
        print(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()
        
    print("\n=== KẾT THÚC KIỂM TRA ===")

if __name__ == "__main__":
    asyncio.run(check_mongodb_users()) 