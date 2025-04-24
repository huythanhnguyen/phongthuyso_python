"""
Bank Account Sub-Agent for BatCucLinhSoAgent
"""

from typing import Any, Dict, List, Optional

from shared_libraries.models import BankAccountRequest
from shared_libraries.logger import get_logger
# Import Feng Shui data directly as logic is tightly coupled here
from tools.batcuclinhso_analysis.fengshui_data import NUMBER_PAIRS_MEANING
# Assuming specific suggester tool is used
from tools.batcuclinhso_analysis.bank_account_suggester import suggest_bank_account_pairs # Example name

class BankAccountAgent:
    """
    Handles analysis and suggestions related to bank account numbers.
    Focuses on suggesting good ending pairs based on purpose.
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def analyze_bank_account(self, request: BankAccountRequest) -> Dict[str, Any]:
        """
        Đề xuất các cặp số cuối phù hợp cho số tài khoản ngân hàng.
        (Now uses the suggester tool)
        """
        self.logger.info(f"Đề xuất cặp số cuối STK cho mục đích: {request.purpose}, Ngân hàng: {request.bank_name}")
        
        # Delegate to the specific suggester tool
        suggestion_result = suggest_bank_account_pairs(request.purpose, request.preferred_digits, request.bank_name)
        
        # Return the result from the tool (adjust structure if needed)
        return suggestion_result

        # --- Removed old logic now handled by the tool --- 
        # suggested_pairs = []
        # purpose_lower = request.purpose.lower()
        # ... (rest of old logic)

        # Define purpose mappings to good pairs
        purpose_pair_map = {
            ("kinh doanh", "tài chính", "công ty"): [
                {"pair": "38", "name": "Phát Tài", "score": 9},
                {"pair": "83", "name": "Phát Tài", "score": 9},
                {"pair": "28", "name": "Sinh Khí", "score": 8.5}
            ],
            ("tiết kiệm", "đầu tư", "tích lũy"): [
                {"pair": "37", "name": "Diên Niên", "score": 8},
                {"pair": "73", "name": "Diên Niên", "score": 8},
                {"pair": "82", "name": "Sinh Khí", "score": 8.5}
            ],
             ("cá nhân", "tiêu dùng"): [
                {"pair": "46", "name": "Thiên Y", "score": 7.5},
                {"pair": "64", "name": "Thiên Y", "score": 7.5},
                {"pair": "19", "name": "Đường Quan", "score": 8}
            ]
        }

        # General good pairs as fallback
        general_good_pairs = [
             {"pair": "38", "name": "Phát Tài", "score": 9},
             {"pair": "28", "name": "Sinh Khí", "score": 8.5},
             {"pair": "19", "name": "Đường Quan", "score": 8}
        ]

        # Find matching pairs based on purpose
        found_purpose_match = False
        for keywords, pairs in purpose_pair_map.items():
             if any(keyword in purpose_lower for keyword in keywords):
                 suggested_pairs.extend(pairs)
                 found_purpose_match = True
                 break # Assume first match is primary purpose
        
        # Use general good pairs if no specific purpose matched
        if not found_purpose_match:
             suggested_pairs.extend(general_good_pairs)
        
        # Add pairs containing preferred digits, if any
        if request.preferred_digits:
            added_preferred = set() # Avoid duplicates if preferred digit is in multiple good pairs
            for digit in request.preferred_digits:
                if not digit.isdigit(): continue # Skip non-digits

                # Find good pairs (score >= 7) containing this digit
                pairs_with_digit = [
                    {"pair": p, **info} 
                    for p, info in NUMBER_PAIRS_MEANING.items() 
                    if digit in p and info["score"] >= 7
                ]
                
                if pairs_with_digit:
                    # Add the best scoring pair containing the preferred digit
                    best_pair_for_digit = max(pairs_with_digit, key=lambda x: x["score"])
                    if best_pair_for_digit["pair"] not in added_preferred:
                        suggested_pairs.append(best_pair_for_digit)
                        added_preferred.add(best_pair_for_digit["pair"])
        
        # Sort by score and get unique pairs
        suggested_pairs.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        unique_pairs_result = []
        seen_pairs = set()
        for pair_info in suggested_pairs:
            pair_code = pair_info.get("pair")
            if pair_code and pair_code not in seen_pairs:
                seen_pairs.add(pair_code)
                # Add meaning from the main db if missing (e.g., from purpose map)
                if "meaning" not in pair_info and pair_code in NUMBER_PAIRS_MEANING:
                    pair_info["meaning"] = NUMBER_PAIRS_MEANING[pair_code]["meaning"]
                unique_pairs_result.append(pair_info)
        
        return {
            "purpose": request.purpose,
            "bank_name": request.bank_name,
            "suggested_pairs": unique_pairs_result[:5],  # Return top 5 unique suggestions
            "recommendations": [
                f"Nên ưu tiên chọn số tài khoản tại {request.bank_name or 'ngân hàng'} kết thúc bằng một trong các cặp số: {', '.join(p['pair'] for p in unique_pairs_result[:3])}...",
                "Kết hợp các cặp số tốt liên tiếp (nếu có thể) sẽ tăng cường năng lượng tích cực.",
                "Tránh các cặp số Tuyệt Mệnh (47, 74) trong số tài khoản."
            ]
        } 