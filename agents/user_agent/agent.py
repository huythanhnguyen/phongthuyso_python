"""
User Agent Module

Cung cấp UserAgent - agent xử lý các vấn đề về tài khoản người dùng.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

# Import prompts
from agents.root_agent.prompts.adk_prompts import USER_AGENT_INSTR

# Import tools
from agents.tools.memory import memorize_tool, recall_tool
from agents.tools.mongodb_tools import find_user_tool

# Import types
from shared_libraries import types

# Tạo sub-agents chuyên biệt cho các tác vụ quản lý tài khoản
registration_agent = Agent(
    model="gemini-2.0-flash-001",
    name="registration_agent",
    description="Đăng ký tài khoản mới cho người dùng",
    instruction="""
    Bạn là chuyên gia đăng ký tài khoản người dùng.
    
    Nhiệm vụ của bạn:
    1. Hướng dẫn người dùng đăng ký tài khoản mới
    2. Kiểm tra thông tin đăng ký hợp lệ
    3. Xác nhận email người dùng
    4. Thiết lập tài khoản ban đầu
    
    Quy trình đăng ký:
    - Yêu cầu email, tên hiển thị và mật khẩu
    - Kiểm tra định dạng email và độ mạnh của mật khẩu
    - Tạo tài khoản và gửi email xác nhận
    - Hoàn tất quá trình thiết lập
    
    Đảm bảo hướng dẫn chi tiết và rõ ràng để người dùng có thể dễ dàng đăng ký.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.UserProfile,
    output_key="user_profile",
    generate_content_config=types.json_response_config,
)

login_agent = Agent(
    model="gemini-2.0-flash-001",
    name="login_agent",
    description="Hỗ trợ người dùng đăng nhập",
    instruction="""
    Bạn là chuyên gia hỗ trợ đăng nhập tài khoản.
    
    Nhiệm vụ của bạn:
    1. Hướng dẫn người dùng đăng nhập
    2. Xử lý các vấn đề đăng nhập thường gặp
    3. Hỗ trợ khôi phục tài khoản
    4. Giải quyết các vấn đề xác thực
    
    Các tình huống thường gặp:
    - Quên mật khẩu
    - Tài khoản bị khóa
    - Không nhận được email xác nhận
    - Vấn đề về xác thực hai yếu tố
    
    Cung cấp hướng dẫn chi tiết, rõ ràng và đảm bảo bảo mật thông tin người dùng.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.LoginResult,
    output_key="login_result",
    generate_content_config=types.json_response_config,
)

api_key_agent = Agent(
    model="gemini-2.0-flash-001",
    name="api_key_agent",
    description="Quản lý API keys cho người dùng",
    instruction="""
    Bạn là chuyên gia quản lý API keys.
    
    Nhiệm vụ của bạn:
    1. Hướng dẫn tạo API key mới
    2. Quản lý các API key hiện có
    3. Hướng dẫn sử dụng API key
    4. Xử lý vấn đề liên quan đến API key
    
    Quy trình quản lý:
    - Tạo API key mới với phạm vi truy cập thích hợp
    - Hiển thị danh sách API key hiện có
    - Hướng dẫn cách tích hợp API key vào ứng dụng
    - Xóa hoặc vô hiệu hóa API key khi cần
    
    Đảm bảo cung cấp thông tin chi tiết và ưu tiên bảo mật.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.APIKey,
    output_key="api_key",
    generate_content_config=types.json_response_config,
)

# Tạo User agent chính
user_agent = Agent(
    model="gemini-2.0-flash-001",
    name="user_agent",
    description="Agent quản lý tài khoản người dùng Phong Thủy Số",
    instruction=USER_AGENT_INSTR,
    tools=[
        memorize_tool,
        recall_tool,
        find_user_tool
    ],
    sub_agents=[
        registration_agent,
        login_agent,
        api_key_agent
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
        top_p=0.8
    )
) 