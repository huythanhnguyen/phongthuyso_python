"""
Password Sub-Agent for BatCucLinhSoAgent
"""

import random
import string
from typing import Any, Dict, List

from ...shared_libraries.models import PasswordRequest
from ...shared_libraries.logger import get_logger
from ...tools.batcuclinhso_analysis.number_analyzer import analyze_number_string
from ...tools.batcuclinhso_analysis.fengshui_data import NUMBER_PAIRS_MEANING, SINGLE_NUMBER_MEANING

class PasswordAgent:
    """
    Handles generation and analysis of passwords based on Feng Shui and security.
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def generate_password(self, request: PasswordRequest) -> Dict[str, Any]:
        """
        Tạo mật khẩu theo phong thủy số học và yêu cầu bảo mật.
        
        Args:
            request (PasswordRequest): Yêu cầu tạo mật khẩu.
            
        Returns:
            Dict[str, Any]: Mật khẩu được tạo kèm phân tích.
        """
        self.logger.info(f"Tạo mật khẩu cho mục đích: {request.purpose}, độ dài tối thiểu: {request.min_length}")
        
        # --- Password Generation Logic --- 
        password_length = max(request.min_length, 10) # Ensure minimum reasonable length
        chars = list(string.ascii_letters + string.digits)
        if request.require_special_chars:
            chars.extend(list("!@#$%^&*()"))

        # Attempt to incorporate good feng shui digits/pairs
        good_pairs = [p for p, info in NUMBER_PAIRS_MEANING.items() if info["score"] >= 7]
        good_digits = [d for d, info in SINGLE_NUMBER_MEANING.items() if info["score"] >= 7]
        
        password = ""
        attempts = 0
        max_attempts = 10

        while attempts < max_attempts:
            attempts += 1
            # Start with some good feng shui elements if possible
            current_password_parts = []
            feng_shui_elements_count = 0
            if good_pairs and random.random() < 0.8: # 80% chance to add a good pair
                 current_password_parts.append(random.choice(good_pairs))
                 feng_shui_elements_count += 2
            elif good_digits and random.random() < 0.5: # 50% chance to add a good digit
                current_password_parts.append(random.choice(good_digits))
                feng_shui_elements_count += 1
            
            # Add random characters to meet length
            remaining_length = password_length - len("".join(current_password_parts))
            if remaining_length > 0:
                current_password_parts.extend(random.choices(chars, k=remaining_length))
            
            # Shuffle to mix elements
            random.shuffle(current_password_parts)
            password = "".join(current_password_parts)

            # Validate generated password against requirements
            meets_requirements = True
            if request.require_numbers and not any(c.isdigit() for c in password):
                meets_requirements = False
            if request.require_special_chars and not any(c in "!@#$%^&*()" for c in password):
                meets_requirements = False
            # Add checks for uppercase/lowercase if needed
            # if request.require_uppercase and not any(c.isupper() for c in password):
            #     meets_requirements = False 
            # if request.require_lowercase and not any(c.islower() for c in password):
            #     meets_requirements = False 
                
            if meets_requirements:
                break # Found a suitable password
        else:
             # Fallback if requirements hard to meet after attempts (e.g., length 1, require all)
             self.logger.warning("Could not meet all password requirements after multiple attempts, returning best effort.")
             # Simple fallback: just generate random chars of required length
             password = ''.join(random.choices(chars, k=password_length))
             # Manual fixup might be needed here in complex cases

        # --- Analysis --- 
        feng_shui_analysis = self._analyze_password_fengshui(password)
        strength_analysis = self._evaluate_password_strength(password)
        
        return {
            "password": password,
            "strength": strength_analysis,
            "feng_shui_analysis": feng_shui_analysis,
            "recommendation": "Mật khẩu này kết hợp các nguyên tắc bảo mật và phong thủy số học. Điểm phong thủy dựa trên các chữ số có trong mật khẩu."
        }

    def _analyze_password_fengshui(self, password: str) -> Dict[str, Any]:
        """
        Phân tích mật khẩu theo phong thủy (sử dụng number_analyzer tool).
        """
        digits = ''.join(c for c in password if c.isdigit())
        
        if not digits:
            return {
                "score": 5.0, # Neutral score if no digits
                "pairs_analysis": [],
                "analysis": "Mật khẩu không chứa số nên không có giá trị phong thủy số học."
            }
        
        analysis_result = analyze_number_string(digits)
        avg_score = analysis_result["total_score"]
        
        analysis_text = f"Điểm phong thủy số học (dựa trên các chữ số): {avg_score:.1f}/10."
        if analysis_result["pairs_analysis"]:
             good_fengshui_pairs = [p["pair"] for p in analysis_result["pairs_analysis"] if p["score"] >= 7]
             bad_fengshui_pairs = [p["pair"] for p in analysis_result["pairs_analysis"] if p["score"] < 5]
             if good_fengshui_pairs:
                 analysis_text += f" Chứa cặp số tốt: {', '.join(good_fengshui_pairs)}."
             if bad_fengshui_pairs:
                  analysis_text += f" Chứa cặp số cần lưu ý: {', '.join(bad_fengshui_pairs)}."

        return {
            "score": avg_score,
            "pairs_analysis": analysis_result["pairs_analysis"],
            "analysis": analysis_text
        }

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
            "score": score, # Max score could be 5 based on this logic
            "strength": strength,
            "feedback": feedback
        } 