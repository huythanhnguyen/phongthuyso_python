"""
Utilities Module

Module cung cấp các tiện ích và hàm trợ giúp được sử dụng rộng rãi trong hệ thống.
"""

import json
import os
import re
import time
from typing import Any, Dict, List, Optional, Union


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Đọc và parse nội dung từ file JSON.
    
    Args:
        file_path (str): Đường dẫn đến file JSON
        
    Returns:
        Dict[str, Any]: Dữ liệu JSON đã được parse
        
    Raises:
        FileNotFoundError: Nếu file không tồn tại
        json.JSONDecodeError: Nếu file không phải định dạng JSON hợp lệ
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"File không phải là JSON hợp lệ: {file_path}", "", 0)


def save_json_file(data: Dict[str, Any], file_path: str, indent: int = 2) -> None:
    """
    Lưu dữ liệu vào file JSON.
    
    Args:
        data (Dict[str, Any]): Dữ liệu cần lưu
        file_path (str): Đường dẫn đến file JSON
        indent (int, optional): Số khoảng trắng để căn lề JSON. Mặc định là 2.
    """
    # Tạo thư mục nếu chưa tồn tại
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)


def clean_text(text: str) -> str:
    """
    Làm sạch chuỗi văn bản, loại bỏ các ký tự đặc biệt và khoảng trắng dư thừa.
    
    Args:
        text (str): Chuỗi văn bản cần làm sạch
        
    Returns:
        str: Chuỗi văn bản đã được làm sạch
    """
    # Loại bỏ ký tự đặc biệt
    text = re.sub(r'[^\w\s]', '', text)
    # Chuẩn hóa khoảng trắng
    text = re.sub(r'\s+', ' ', text)
    # Cắt khoảng trắng ở đầu và cuối
    return text.strip()


def retry_with_backoff(max_retries: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0):
    """
    Decorator thực hiện retry với backoff khi hàm gặp exception.
    
    Args:
        max_retries (int): Số lần retry tối đa. Mặc định là 3.
        initial_delay (float): Thời gian delay ban đầu (giây). Mặc định là 1.0.
        backoff_factor (float): Hệ số nhân cho delay. Mặc định là 2.0.
        
    Returns:
        function: Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                        delay *= backoff_factor
            
            raise last_exception
        return wrapper
    return decorator


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Chia một danh sách thành các phần nhỏ hơn với kích thước cố định.
    
    Args:
        lst (List[Any]): Danh sách cần chia
        chunk_size (int): Kích thước của mỗi phần
        
    Returns:
        List[List[Any]]: Danh sách các phần đã được chia
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def deep_get(dictionary: Dict[str, Any], keys: Union[str, List[str]], default: Any = None) -> Any:
    """
    Truy cập an toàn vào một giá trị lồng nhau trong dictionary.
    
    Args:
        dictionary (Dict[str, Any]): Dictionary cần truy cập
        keys (Union[str, List[str]]): Key hoặc chuỗi keys lồng nhau
        default (Any, optional): Giá trị mặc định nếu không tìm thấy. Mặc định là None.
        
    Returns:
        Any: Giá trị được tìm thấy hoặc giá trị mặc định
    """
    if isinstance(keys, str):
        keys = keys.split('.')
        
    temp_dict = dictionary
    for key in keys:
        try:
            temp_dict = temp_dict[key]
        except (KeyError, TypeError):
            return default
    
    return temp_dict 