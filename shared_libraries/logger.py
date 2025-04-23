"""
Logger Utility Module

Module cung cấp các chức năng ghi log thống nhất cho toàn bộ hệ thống.
"""

import logging
import os
from datetime import datetime

class Logger:
    """
    Lớp Logger để quản lý các log trong hệ thống
    """
    
    def __init__(self, name, log_level=logging.INFO, log_to_file=False, log_dir="logs"):
        """
        Khởi tạo logger
        
        Args:
            name (str): Tên của logger
            log_level (int): Mức độ log (mặc định: logging.INFO)
            log_to_file (bool): Có ghi log ra file hay không
            log_dir (str): Thư mục chứa file log
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Định dạng log
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (nếu được yêu cầu)
        if log_to_file:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            log_file = os.path.join(
                log_dir, 
                f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
            )
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """Ghi log debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Ghi log info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Ghi log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Ghi log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Ghi log critical message"""
        self.logger.critical(message)

def get_logger(name, log_level=logging.INFO, log_to_file=False):
    """
    Hàm tiện ích để lấy instance logger
    
    Args:
        name (str): Tên của logger
        log_level (int): Mức độ log
        log_to_file (bool): Có ghi log ra file hay không
        
    Returns:
        Logger: Instance logger đã được cấu hình
    """
    return Logger(name, log_level, log_to_file) 