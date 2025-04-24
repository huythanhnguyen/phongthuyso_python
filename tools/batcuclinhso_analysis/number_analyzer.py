"""
Number Analyzer Tool

Provides functions for analyzing number strings based on Feng Shui principles.
"""

from typing import Dict, List, Any

# Import the Feng Shui data (relative import is correct here)
from .fengshui_data import NUMBER_PAIRS_MEANING, SINGLE_NUMBER_MEANING

def analyze_number_string(number_string: str) -> Dict[str, Any]:
    """
    Analyzes a string of digits based on Bat Cuc Linh So pairs.

    Args:
        number_string: The string of digits to analyze.

    Returns:
        A dictionary containing:
        - 'pairs_analysis': A list of dictionaries, each detailing a pair.
        - 'total_score': The average score of all analyzed pairs.
        - 'luck_level': A textual description of the luck level.
    """
    digits_only = ''.join(filter(str.isdigit, number_string))
    if not digits_only:
        return {
            "pairs_analysis": [],
            "total_score": 0.0,
            "luck_level": "Không xác định (không có số)"
        }

    pairs_analysis = []
    for i in range(len(digits_only) - 1):
        pair = digits_only[i:i+2]
        if pair in NUMBER_PAIRS_MEANING:
            info = NUMBER_PAIRS_MEANING[pair]
            pairs_analysis.append({
                "pair": pair,
                "position": i + 1,
                "name": info["name"],
                "meaning": info["meaning"],
                "score": info["score"]
            })
        else:
            # Fallback to single digit analysis if pair not found
            # Ensure digits exist in SINGLE_NUMBER_MEANING before accessing
            digit1_info = SINGLE_NUMBER_MEANING.get(pair[0])
            digit2_info = SINGLE_NUMBER_MEANING.get(pair[1])

            if digit1_info and digit2_info:
                avg_score = (digit1_info["score"] + digit2_info["score"]) / 2
                meaning = f"Kết hợp {pair[0]} ({digit1_info['meaning']}) và {pair[1]} ({digit2_info['meaning']})"
                name = "Cặp số thông thường"
            else:
                # Handle case where one or both digits are not in the database (should not happen with 0-9)
                avg_score = 5.0 # Default score
                meaning = f"Không thể phân tích cặp số {pair} chi tiết."
                name = "Cặp số không xác định"

            pairs_analysis.append({
                "pair": pair,
                "position": i + 1,
                "name": name,
                "meaning": meaning,
                "score": avg_score
            })

    if not pairs_analysis:
        # Handle single digit numbers if applicable
        if len(digits_only) == 1 and digits_only in SINGLE_NUMBER_MEANING:
             single_info = SINGLE_NUMBER_MEANING[digits_only]
             total_score = float(single_info["score"])
             # Append a pseudo-analysis for consistency
             pairs_analysis.append({
                 "pair": digits_only, 
                 "position": 1,
                 "name": "Số đơn",
                 "meaning": single_info["meaning"],
                 "score": total_score
             })
        else:
             total_score = 0.0 
    else:        
        total_score = sum(pair["score"] for pair in pairs_analysis) / len(pairs_analysis)

    # Determine luck level based on score
    if total_score >= 8:
        luck_level = "Rất tốt"
    elif total_score >= 7:
        luck_level = "Tốt"
    elif total_score >= 6:
        luck_level = "Khá"
    elif total_score >= 5:
        luck_level = "Trung bình"
    else:
        luck_level = "Kém"

    return {
        "pairs_analysis": pairs_analysis,
        "total_score": round(total_score, 2),
        "luck_level": luck_level
    } 