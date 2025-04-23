"""
Các hằng số tổ hợp sao chuyển đổi từ combinations.js sang Python
"""

# Định nghĩa trực tiếp COMBINATIONS trong Python
COMBINATIONS = {
    # Tổ hợp Sinh Khí
    "SINH_KHI_SINH_KHI": {
        "name": "Sinh Khí + Sinh Khí",
        "description": "Quý nhân tăng cường, vận may nhân đôi",
        "detailedDescription": """Khi hai sao Sinh Khí kết hợp với nhau, tạo thành tổ hợp mạnh mẽ về quý nhân và vận may.
- Quý nhân trợ giúp tăng cường gấp đôi
- Vận may về tài chính và sự nghiệp nhân đôi
- Tính cách lạc quan, nhìn đời tích cực
- Dễ gặp được nhiều cơ hội tốt
- Tình cảm thuận lợi, hạnh phúc
- Sức khỏe tốt, ít bệnh tật"""
    },
    
    "SINH_KHI_THIEN_Y": {
        "name": "Sinh Khí + Thiên Y",
        "description": "Quý nhân mang tài lộc",
        "detailedDescription": """Khi Sinh Khí kết hợp với Thiên Y, tạo thành tổ hợp mạnh về quý nhân và tài lộc.
- Quý nhân không chỉ giúp đỡ mà còn mang lại tài lộc
- Vận may về tài chính tăng cường
- Tính cách vừa lạc quan vừa thông minh
- Dễ gặp được cơ hội làm ăn tốt
- Tình cảm vừa hạnh phúc vừa ổn định
- Sức khỏe tốt, ít bệnh tật"""
    },
    
    # Tổ hợp Thiên Y
    "THIEN_Y_THIEN_Y": {
        "name": "Thiên Y + Thiên Y",
        "description": "Tài lộc nhân đôi, phú quý song toàn",
        "detailedDescription": """Khi hai sao Thiên Y kết hợp với nhau, tạo thành tổ hợp mạnh mẽ về tài lộc.
- Tài lộc tăng cường gấp đôi
- Vận may về tiền bạc nhân đôi
- Tính cách thông minh, thiện lương
- Dễ gặp được nhiều cơ hội làm ăn
- Tình cảm ổn định, hạnh phúc
- Sức khỏe tốt, ít bệnh tật"""
    },
    
    "THIEN_Y_DIEN_NIEN": {
        "name": "Thiên Y + Diên Niên",
        "description": "Tài lộc đi đôi với sự nghiệp",
        "detailedDescription": """Khi Thiên Y kết hợp với Diên Niên, tạo thành tổ hợp mạnh về tài lộc và sự nghiệp.
- Tài lộc đi đôi với sự nghiệp phát triển
- Vận may về công việc và tiền bạc
- Tính cách vừa thông minh vừa có trách nhiệm
- Dễ gặp được cơ hội thăng tiến
- Tình cảm ổn định, hạnh phúc
- Sức khỏe tốt, ít bệnh tật"""
    },
    
    # Tổ hợp Diên Niên
    "DIEN_NIEN_DIEN_NIEN": {
        "name": "Diên Niên + Diên Niên",
        "description": "Sự nghiệp thăng tiến, quyền lực tăng cường",
        "detailedDescription": """Khi hai sao Diên Niên kết hợp với nhau, tạo thành tổ hợp mạnh mẽ về sự nghiệp.
- Sự nghiệp thăng tiến nhanh chóng
- Quyền lực và địa vị tăng cường
- Tính cách kiên định, có trách nhiệm
- Dễ đạt được thành công trong công việc
- Tình cảm ổn định, hạnh phúc
- Sức khỏe tốt, ít bệnh tật"""
    },
    
    "DIEN_NIEN_PHUC_VI": {
        "name": "Diên Niên + Phục Vị",
        "description": "Sự nghiệp ổn định, bền vững",
        "detailedDescription": """Khi Diên Niên kết hợp với Phục Vị, tạo thành tổ hợp mạnh về sự ổn định.
- Sự nghiệp phát triển ổn định
- Công việc bền vững, lâu dài
- Tính cách vừa kiên định vừa nhẫn nại
- Dễ duy trì được thành công
- Tình cảm ổn định, hạnh phúc
- Sức khỏe tốt, ít bệnh tật"""
    },
    
    # Tổ hợp Phục Vị
    "PHUC_VI_PHUC_VI": {
        "name": "Phục Vị + Phục Vị",
        "description": "Ổn định nhân đôi, bền vững lâu dài",
        "detailedDescription": """Khi hai sao Phục Vị kết hợp với nhau, tạo thành tổ hợp mạnh mẽ về sự ổn định.
- Sự ổn định tăng cường gấp đôi
- Cuộc sống bền vững, lâu dài
- Tính cách nhẫn nại, kiên trì
- Dễ duy trì được thành công
- Tình cảm ổn định, hạnh phúc
- Sức khỏe tốt, ít bệnh tật"""
    },
    
    "PHUC_VI_HOA_HAI": {
        "name": "Phục Vị + Họa Hại",
        "description": "Ổn định bị phá vỡ, khó khăn xuất hiện",
        "detailedDescription": """Khi Phục Vị kết hợp với Họa Hại, tạo thành tổ hợp không tốt.
- Sự ổn định bị phá vỡ
- Khó khăn và trở ngại xuất hiện
- Tính cách vừa nhẫn nại vừa hay lo lắng
- Dễ gặp phải rắc rối
- Tình cảm không ổn định
- Sức khỏe cần chú ý"""
    },
    
    # Tổ hợp Họa Hại
    "HOA_HAI_HOA_HAI": {
        "name": "Họa Hại + Họa Hại",
        "description": "Tai họa nhân đôi, khó khăn chồng chất",
        "detailedDescription": """Khi hai sao Họa Hại kết hợp với nhau, tạo thành tổ hợp rất xấu.
- Tai họa và khó khăn nhân đôi
- Dễ gặp phải nhiều rắc rối
- Tính cách hay lo lắng, bi quan
- Dễ gặp phải thất bại
- Tình cảm không ổn định
- Sức khỏe kém, dễ bệnh tật"""
    },
    
    "HOA_HAI_LUC_SAT": {
        "name": "Họa Hại + Lục Sát",
        "description": "Tai họa và mâu thuẫn cùng lúc",
        "detailedDescription": """Khi Họa Hại kết hợp với Lục Sát, tạo thành tổ hợp rất xấu.
- Tai họa đi đôi với mâu thuẫn
- Dễ gặp phải tranh chấp
- Tính cách vừa lo lắng vừa nóng nảy
- Dễ gặp phải thất bại
- Tình cảm không ổn định
- Sức khỏe kém, dễ bệnh tật"""
    },
    
    # Tổ hợp Lục Sát
    "LUC_SAT_LUC_SAT": {
        "name": "Lục Sát + Lục Sát",
        "description": "Mâu thuẫn nhân đôi, xung đột tăng cường",
        "detailedDescription": """Khi hai sao Lục Sát kết hợp với nhau, tạo thành tổ hợp rất xấu.
- Mâu thuẫn và xung đột nhân đôi
- Dễ gặp phải tranh chấp
- Tính cách nóng nảy, dễ nổi giận
- Dễ gặp phải thất bại
- Tình cảm không ổn định
- Sức khỏe kém, dễ bệnh tật"""
    },
    
    "LUC_SAT_NGU_QUY": {
        "name": "Lục Sát + Ngũ Quỷ",
        "description": "Mâu thuẫn và tai họa cùng lúc",
        "detailedDescription": """Khi Lục Sát kết hợp với Ngũ Quỷ, tạo thành tổ hợp rất xấu.
- Mâu thuẫn đi đôi với tai họa
- Dễ gặp phải rắc rối nghiêm trọng
- Tính cách vừa nóng nảy vừa bi quan
- Dễ gặp phải thất bại
- Tình cảm không ổn định
- Sức khỏe kém, dễ bệnh tật"""
    },
    
    # Tổ hợp Ngũ Quỷ
    "NGU_QUY_NGU_QUY": {
        "name": "Ngũ Quỷ + Ngũ Quỷ",
        "description": "Tai họa nhân đôi, xui xẻo tăng cường",
        "detailedDescription": """Khi hai sao Ngũ Quỷ kết hợp với nhau, tạo thành tổ hợp rất xấu.
- Tai họa và xui xẻo nhân đôi
- Dễ gặp phải nhiều chuyện không may
- Tính cách bi quan, lo lắng
- Dễ gặp phải thất bại
- Tình cảm không ổn định
- Sức khỏe kém, dễ bệnh tật"""
    },
    
    "NGU_QUY_TUYET_MENH": {
        "name": "Ngũ Quỷ + Tuyệt Mệnh",
        "description": "Tai họa và tuyệt vọng cùng lúc",
        "detailedDescription": """Khi Ngũ Quỷ kết hợp với Tuyệt Mệnh, tạo thành tổ hợp rất xấu.
- Tai họa đi đôi với tuyệt vọng
- Dễ rơi vào tình trạng bế tắc
- Tính cách vừa bi quan vừa lo lắng
- Dễ gặp phải thất bại
- Tình cảm không ổn định
- Sức khỏe kém, dễ bệnh tật"""
    },
    
    # Tổ hợp Tuyệt Mệnh
    "TUYET_MENH_TUYET_MENH": {
        "name": "Tuyệt Mệnh + Tuyệt Mệnh",
        "description": "Tuyệt vọng nhân đôi, bế tắc tăng cường",
        "detailedDescription": """Khi hai sao Tuyệt Mệnh kết hợp với nhau, tạo thành tổ hợp rất xấu.
- Tuyệt vọng và bế tắc nhân đôi
- Dễ rơi vào tình trạng khó khăn
- Tính cách bi quan, lo lắng
- Dễ gặp phải thất bại
- Tình cảm không ổn định
- Sức khỏe kém, dễ bệnh tật"""
    },
    
    "TUYET_MENH_SINH_KHI": {
        "name": "Tuyệt Mệnh + Sinh Khí",
        "description": "Tuyệt vọng được cứu vãn bởi quý nhân",
        "detailedDescription": """Khi Tuyệt Mệnh kết hợp với Sinh Khí, tạo thành tổ hợp có thể cứu vãn.
- Tuyệt vọng có thể được cứu vãn
- Quý nhân có thể giúp đỡ
- Tính cách vừa bi quan vừa lạc quan
- Có cơ hội vượt qua khó khăn
- Tình cảm có thể ổn định
- Sức khỏe có thể cải thiện"""
    }
} 