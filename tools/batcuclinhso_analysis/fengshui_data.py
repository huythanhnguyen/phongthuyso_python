"""
Feng Shui Data Module

Stores the core data for Bat Cuc Linh So analysis.
"""

# Các cặp số theo Bát Cực Linh Số và ý nghĩa
NUMBER_PAIRS_MEANING = {
    "19": {"name": "Đường Quan", "meaning": "Tốt cho công danh sự nghiệp", "score": 8},
    "91": {"name": "Đường Quan", "meaning": "Tốt cho công danh sự nghiệp", "score": 8},
    "28": {"name": "Sinh Khí", "meaning": "Tốt cho sức khỏe và phát triển", "score": 9},
    "82": {"name": "Sinh Khí", "meaning": "Tốt cho sức khỏe và phát triển", "score": 9},
    "37": {"name": "Diên Niên", "meaning": "Ổn định, bền vững", "score": 7},
    "73": {"name": "Diên Niên", "meaning": "Ổn định, bền vững", "score": 7},
    "46": {"name": "Thiên Y", "meaning": "Tốt cho sức khỏe, học tập", "score": 8},
    "64": {"name": "Thiên Y", "meaning": "Tốt cho sức khỏe, học tập", "score": 8},
    "38": {"name": "Phát Tài", "meaning": "Tốt cho tiền bạc, kinh doanh", "score": 9},
    "83": {"name": "Phát Tài", "meaning": "Tốt cho tiền bạc, kinh doanh", "score": 9},
    "29": {"name": "Thiên Mã", "meaning": "Tốt cho di chuyển, giao tiếp", "score": 8},
    "92": {"name": "Thiên Mã", "meaning": "Tốt cho di chuyển, giao tiếp", "score": 8},
    "47": {"name": "Tuyệt Mệnh", "meaning": "Xấu, nên tránh", "score": 2},
    "74": {"name": "Tuyệt Mệnh", "meaning": "Xấu, nên tránh", "score": 2},
    "39": {"name": "Khả Ái", "meaning": "Tốt cho tình cảm, hôn nhân", "score": 8},
    "93": {"name": "Khả Ái", "meaning": "Tốt cho tình cảm, hôn nhân", "score": 8},
}

# Ý nghĩa của các số đơn
SINGLE_NUMBER_MEANING = {
    "0": {"meaning": "Trung tính, gắn liền với khả năng tiếp thu, tích lũy", "score": 5},
    "1": {"meaning": "Tượng trưng cho sự khởi đầu, tiên phong, độc lập", "score": 7},
    "2": {"meaning": "Tượng trưng cho sự hài hòa, hợp tác, kiên nhẫn", "score": 6},
    "3": {"meaning": "Tượng trưng cho sự sáng tạo, biểu đạt, giao tiếp", "score": 7},
    "4": {"meaning": "Tượng trưng cho sự ổn định, thực tế, kiên định", "score": 5},
    "5": {"meaning": "Tượng trưng cho sự tự do, thay đổi, khám phá", "score": 7},
    "6": {"meaning": "Tượng trưng cho sự hài hòa, cân bằng, trách nhiệm", "score": 6},
    "7": {"meaning": "Tượng trưng cho sự phân tích, trí tuệ, tâm linh", "score": 6},
    "8": {"meaning": "Tượng trưng cho sự phát đạt, quyền lực, thành công", "score": 8},
    "9": {"meaning": "Tượng trưng cho sự hoàn thành, lý tưởng, nhân đạo", "score": 7},
} 