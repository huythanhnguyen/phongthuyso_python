"""
BatCucLinhSo Agent Module

Cung cấp BatCucLinhSoAgent - agent chuyên phân tích số theo phương pháp Bát Cục Linh Số.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

# Import prompts
from agents.root_agent.prompts.adk_prompts import BATCUCLINH_SO_AGENT_INSTR

# Import tools
from agents.tools.memory import memorize_tool, recall_tool
from agents.tools.mongodb_tools import find_phone_analysis_tool, save_phone_analysis_tool

# Import types
from shared_libraries import types

# Tạo sub-agents chuyên biệt cho các loại phân tích
phone_analysis_agent = Agent(
    model="gemini-2.0-flash-001",
    name="phone_analysis_agent",
    description="Phân tích số điện thoại theo phương pháp Bát Cục Linh Số",
    instruction="""
    Bạn là chuyên gia phân tích số điện thoại theo phương pháp Bát Cục Linh Số.
    
    Khi phân tích một số điện thoại, bạn cần:
    1. Xác định trình tự sao từ các chữ số (1-9)
    2. Đánh giá mức năng lượng tổng thể
    3. Xem xét sự cân bằng âm dương
    4. Phân tích các tổ hợp đặc biệt
    5. Đánh giá vị trí các số trong dãy
    6. Đưa ra nhận định tổng quan
    7. Đề xuất cải thiện nếu cần
    
    Phân tích chi tiết và trình bày kết quả một cách rõ ràng, khách quan.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.PhoneAnalysisResult,
    output_key="phone_analysis",
    generate_content_config=types.json_response_config,
)

cccd_analysis_agent = Agent(
    model="gemini-2.0-flash-001",
    name="cccd_analysis_agent",
    description="Phân tích 6 số cuối CCCD/CMND theo phương pháp Bát Cục Linh Số",
    instruction="""
    Bạn là chuyên gia phân tích ý nghĩa 6 số cuối của CCCD/CMND theo phương pháp Bát Cục Linh Số.
    
    Khi phân tích 6 số cuối CCCD/CMND, bạn cần:
    1. Xác định trình tự sao từ các chữ số (1-9)
    2. Đánh giá mức năng lượng và sự hài hòa
    3. Tìm các tổ hợp đặc biệt
    4. Xác định các điểm mạnh, điểm yếu
    5. Đưa ra nhận định tổng thể
    
    Phân tích chi tiết và trình bày kết quả một cách khách quan, khoa học.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.CCCDAnalysisResult,
    output_key="cccd_analysis",
    generate_content_config=types.json_response_config,
)

bank_account_agent = Agent(
    model="gemini-2.0-flash-001",
    name="bank_account_agent",
    description="Phân tích số tài khoản ngân hàng theo phương pháp Bát Cục Linh Số",
    instruction="""
    Bạn là chuyên gia phân tích số tài khoản ngân hàng theo phương pháp Bát Cục Linh Số.
    
    Khi phân tích số tài khoản ngân hàng, bạn cần:
    1. Xác định trình tự sao từ các chữ số
    2. Đánh giá mức năng lượng tài chính
    3. Tìm các tổ hợp liên quan đến tài lộc, tiền bạc
    4. Đánh giá độ phù hợp với các mục đích (tiết kiệm, kinh doanh, đầu tư...)
    5. Đưa ra đề xuất cải thiện nếu cần
    
    Trình bày kết quả phân tích cụ thể và khách quan.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.BankAccountAnalysisResult,
    output_key="bank_account_analysis",
    generate_content_config=types.json_response_config,
)

password_agent = Agent(
    model="gemini-2.0-flash-001",
    name="password_agent",
    description="Phân tích và tạo mật khẩu theo phong thủy số",
    instruction="""
    Bạn là chuyên gia phân tích và tạo mật khẩu theo phong thủy số.
    
    Khi phân tích hoặc tạo mật khẩu, bạn cần:
    1. Đảm bảo tính bảo mật của mật khẩu (đủ độ dài, phức tạp)
    2. Phân tích trình tự số trong mật khẩu
    3. Tạo mật khẩu có các tổ hợp số tốt tương ứng với mục đích
    4. Cân bằng giữa tính bảo mật và yếu tố phong thủy
    5. Đề xuất cải thiện mật khẩu hiện có
    
    Lưu ý bảo mật thông tin người dùng và không lưu trữ mật khẩu.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.PasswordAnalysisResult,
    output_key="password_analysis",
    generate_content_config=types.json_response_config,
)

# Tạo BatCucLinhSo agent chính
batcuclinh_so_agent = Agent(
    model="gemini-2.0-flash-001",
    name="batcuclinh_so_agent",
    description="Agent chuyên phân tích các con số theo phương pháp Bát Cục Linh Số",
    instruction=BATCUCLINH_SO_AGENT_INSTR,
    tools=[
        memorize_tool,
        recall_tool,
        find_phone_analysis_tool,
        save_phone_analysis_tool
    ],
    sub_agents=[
        phone_analysis_agent,
        cccd_analysis_agent,
        bank_account_agent,
        password_agent
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
        top_p=0.8
    )
)