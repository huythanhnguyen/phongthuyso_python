"""
Tool để gợi ý số tài khoản ngân hàng dựa trên phương pháp Bát Cục Linh Số
"""

from google.adk.tools import FunctionTool
from typing import Dict, Any, List, Optional
import random
import re

def bank_account_suggester(
    bank_code: str,
    prefix: Optional[str] = None,
    length: Optional[int] = None,
    purpose: str = "personal"
) -> Dict[str, Any]:
    """
    Gợi ý số tài khoản ngân hàng may mắn dựa trên phương pháp Bát Cục Linh Số.
    
    Args:
        bank_code (str): Mã ngân hàng (VCB, TCB, ACB, v.v.)
        prefix (str, optional): Tiền tố cố định của số tài khoản
        length (int, optional): Độ dài mong muốn của số tài khoản
        purpose (str): Mục đích sử dụng tài khoản (personal, business, savings, v.v.)
        
    Returns:
        Dict[str, Any]: Kết quả gợi ý với danh sách các số tài khoản may mắn
    """
    if not bank_code:
        raise ValueError("Mã ngân hàng không được để trống")
    
    # Chuẩn hóa bank_code
    bank_code = bank_code.upper()
    
    # Xác định độ dài mặc định dựa trên ngân hàng
    bank_lengths = {
        "VCB": 13,  # Vietcombank
        "TCB": 14,  # Techcombank
        "ACB": 13,  # Asia Commercial Bank
        "BIDV": 14, # BIDV
        "VTB": 13,  # Vietinbank
        "TPB": 12,  # TPBank
        "MB": 13,   # MB Bank
        "OCB": 15,  # OCB
        "SHB": 13,  # SHB
        "MSB": 13   # Maritime Bank
    }
    
    # Xác định độ dài của số tài khoản
    if not length:
        length = bank_lengths.get(bank_code, 13)
    
    # Xác định tiền tố mặc định nếu không cung cấp
    if not prefix:
        prefix = ""
    
    # Kiểm tra tiền tố chỉ chứa chữ số
    if not re.match(r'^\d*$', prefix):
        raise ValueError("Tiền tố phải chỉ chứa chữ số")
    
    # Xác định độ dài phần còn lại cần tạo
    remaining_length = length - len(prefix)
    
    if remaining_length <= 0:
        raise ValueError("Tiền tố đã dài bằng hoặc vượt quá độ dài yêu cầu")
    
    # Các chữ số may mắn trong phong thủy
    lucky_digits = ['6', '8', '9']
    neutral_digits = ['0', '1', '2', '3', '5']
    unlucky_digits = ['4', '7']
    
    # Các mẫu số tài khoản may mắn
    lucky_patterns = [
        "68",  # Tấn Lộc - Vượng Tài
        "89",  # Tài Lộc - Tài Thành
        "96",  # Thành Tấn - Công Thành
        "16",  # Nguyên Tấn - Thủy Sinh Mộc
        "28",  # Địa Tài - Thổ Sinh Kim
        "39",  # Sinh Thành - Mộc Sinh Hỏa
        "168", # Lộc Phát - Phát Tài
        "688", # Lộc Phát Phát
        "869", # Tài Lộc Phát
        "986"  # Cửu Phát Lộc
    ]
    
    # Xác định số lượng may mắn và trung tính dựa vào mục đích
    purpose_weights = {
        "personal": (0.5, 0.4, 0.1),   # (may mắn, trung tính, xui)
        "business": (0.7, 0.25, 0.05), # Tài khoản kinh doanh cần nhiều số may mắn
        "savings": (0.6, 0.35, 0.05),  # Tài khoản tiết kiệm
        "investment": (0.8, 0.15, 0.05) # Tài khoản đầu tư
    }
    
    lucky_weight, neutral_weight, unlucky_weight = purpose_weights.get(purpose.lower(), (0.5, 0.4, 0.1))
    
    # Sinh ngẫu nhiên các số tài khoản may mắn
    result_accounts = []
    for _ in range(5):  # Tạo 5 gợi ý
        account = prefix
        
        # Thêm mẫu may mắn vào giữa
        if remaining_length > 4:
            pattern = random.choice(lucky_patterns)
            if len(pattern) <= remaining_length - 2:
                # Vị trí chèn mẫu
                insert_pos = random.randint(0, remaining_length - len(pattern))
                
                # Tạo phần còn lại
                for i in range(remaining_length):
                    if i == insert_pos:
                        account += pattern
                        i += len(pattern) - 1
                    else:
                        r = random.random()
                        if r < lucky_weight:
                            account += random.choice(lucky_digits)
                        elif r < lucky_weight + neutral_weight:
                            account += random.choice(neutral_digits)
                        else:
                            account += random.choice(unlucky_digits)
            else:
                # Nếu mẫu quá dài, sử dụng cách thông thường
                for _ in range(remaining_length):
                    r = random.random()
                    if r < lucky_weight:
                        account += random.choice(lucky_digits)
                    elif r < lucky_weight + neutral_weight:
                        account += random.choice(neutral_digits)
                    else:
                        account += random.choice(unlucky_digits)
        else:
            # Nếu số còn lại ngắn, chỉ dùng số may mắn
            for _ in range(remaining_length):
                account += random.choice(lucky_digits)
        
        # Kiểm tra và cắt nếu vượt quá độ dài
        if len(account) > length:
            account = account[:length]
        
        # Tính năng lượng số
        digit_sum = sum(int(d) for d in account)
        energy_number = digit_sum % 9 or 9
        
        result_accounts.append({
            "accountNumber": account,
            "energyNumber": energy_number
        })
    
    # Kết quả gợi ý
    return {
        "success": True,
        "suggestions": result_accounts,
        "bank": bank_code,
        "purpose": purpose
    }

# Tạo Function Tool
bank_account_suggester_tool = FunctionTool(bank_account_suggester) 