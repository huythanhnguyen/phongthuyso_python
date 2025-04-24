"""
Logger Module

Module chứa các tiện ích log cho ứng dụng.
"""

import logging
import os
from typing import Optional

def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Tạo và trả về logger với tên và cấp độ cụ thể.
    
    Args:
        name (str): Tên của logger
        level (Optional[int]): Cấp độ log. Nếu None, sẽ dùng cấp độ mặc định
        
    Returns:
        logging.Logger: Logger đã cấu hình
    """
    logger = logging.getLogger(name)
    
    # Thiết lập cấp độ log
    if level is None:
        env_mode = os.environ.get("ENV_MODE", "dev")
        level = logging.INFO if env_mode == "prod" else logging.DEBUG
    
    logger.setLevel(level)
    
    # Tạo handler nếu chưa có
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger 