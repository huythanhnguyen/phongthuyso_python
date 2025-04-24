"""
Password Sub-Agent for BatCucLinhSoAgent
"""

import random
import string
from typing import Any, Dict, List

from shared_libraries.models import PasswordRequest
from shared_libraries.logger import get_logger
from tools.batcuclinhso_analysis.password_analyzer import analyze_password_fengshui_logic, generate_fengshui_password
from tools.batcuclinhso_analysis.fengshui_data import NUMBER_PAIRS_MEANING, SINGLE_NUMBER_MEANING

class PasswordAgent:
    """
    Handles generation and analysis of passwords based on Feng Shui and security.
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def generate_password(self, request: PasswordRequest) -> Dict[str, Any]:
        """
        Tạo mật khẩu theo phong thủy số học và yêu cầu bảo mật.
        (Delegates to generate_fengshui_password tool)
        """
        self.logger.info(f"Tạo mật khẩu cho mục đích: {request.purpose}, độ dài tối thiểu: {request.min_length}")
        
        # Delegate password generation to the tool
        generated_data = generate_fengshui_password(request)
        
        # Perform analysis using other tools/methods
        password = generated_data.get("password", "") # Get password from tool result
        if not password:
             return {"error": "Password generation failed."} # Handle error from tool
             
        strength_analysis = self._evaluate_password_strength(password)
        feng_shui_analysis = self._analyze_password_fengshui(password)
        
        # Combine results
        return {
            "password": password,
            "strength": strength_analysis,
            "feng_shui_analysis": feng_shui_analysis,
            "recommendation": generated_data.get("recommendation", "Mật khẩu được tạo.")
        }
        # --- Removed old generation logic now in tool --- 

    def _analyze_password_fengshui(self, password: str) -> Dict[str, Any]:
        """
        Phân tích mật khẩu theo phong thủy (sử dụng password_analyzer tool).
        """
        # Delegate to the specific tool function
        return analyze_password_fengshui_logic(password)
        # --- Removed old logic now in tool --- 

    def _evaluate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Đánh giá độ mạnh của mật khẩu.
        """
        score = 0
        feedback = []

        # Length
        length = len(password)
        if length >= 12:
            score += 2
            feedback.append("Độ dài tốt (>= 12).")
        elif length >= 8:
            score += 1
            feedback.append("Độ dài khá (>= 8).")
        else:
             feedback.append("Độ dài yếu (< 8).")

        # Character types
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        types_count = sum([has_upper, has_lower, has_digit, has_special])
        
        if types_count == 4:
            score += 3
            feedback.append("Đa dạng ký tự (Chữ hoa, chữ thường, số, ký tự đặc biệt).")
        elif types_count == 3:
            score += 2
            feedback.append("Khá đa dạng ký tự (3 loại).")
        elif types_count == 2:
            score += 1
            feedback.append("Ít đa dạng ký tự (2 loại).")
        else:
             feedback.append("Rất ít đa dạng ký tự (chỉ 1 loại).")

        # Strength level
        if score >= 4: # >=12 length + 3 types OR >=8 length + 4 types
            strength = "Mạnh"
        elif score >= 2: # >=8 length + 2 types OR <8 length + 4 types etc.
            strength = "Trung bình"
        else:
            strength = "Yếu"
            
        # Check for common patterns (basic)
        # TODO: Add more sophisticated checks if needed (e.g., dictionary words, sequences)
        if password.lower() in ["password", "123456", "qwerty"]:
             strength = "Rất yếu"
             feedback.append("Mật khẩu rất phổ biến.")

        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        } 