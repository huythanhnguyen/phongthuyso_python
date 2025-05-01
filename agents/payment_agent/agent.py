"""
Payment Agent Module

Cung cấp PaymentAgent - agent xử lý các vấn đề thanh toán và gói dịch vụ.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import GenerateContentConfig

# Import prompts
from agents.root_agent.prompts.adk_prompts import PAYMENT_AGENT_INSTR

# Import tools
from agents.tools.memory import memorize_tool, recall_tool
from agents.tools.mongodb_tools import find_user_tool, get_user_subscription_tool

# Import types
from shared_libraries import types

# Tạo sub-agents chuyên biệt cho các loại dịch vụ thanh toán
subscription_agent = Agent(
    model="gemini-2.0-flash-001",
    name="subscription_agent",
    description="Quản lý và tư vấn về các gói dịch vụ Phong Thủy Số",
    instruction="""
    Bạn là chuyên gia tư vấn các gói dịch vụ Phong Thủy Số.
    
    Nhiệm vụ của bạn:
    1. Cung cấp thông tin chi tiết về các gói dịch vụ
    2. So sánh ưu nhược điểm giữa các gói
    3. Tư vấn gói phù hợp với nhu cầu người dùng
    4. Giải thích các tính năng và giới hạn của mỗi gói
    
    Các gói hiện có:
    - FREE: 2 lần phân tích số điện thoại/ngày, không có các tính năng khác
    - BASIC (99.000đ/tháng): 10 lần phân tích số điện thoại/ngày, 5 lần phân tích CCCD
    - PREMIUM (199.000đ/tháng): Không giới hạn phân tích số điện thoại, 10 lần phân tích CCCD, 5 lần phân tích tài khoản ngân hàng
    - VIP (399.000đ/tháng): Tất cả tính năng không giới hạn + ưu tiên hỗ trợ
    
    Cung cấp thông tin đầy đủ, chính xác và tư vấn phù hợp với nhu cầu của người dùng.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.SubscriptionInfo,
    output_key="subscription_info",
    generate_content_config=types.json_response_config,
)

quota_agent = Agent(
    model="gemini-2.0-flash-001",
    name="quota_agent",
    description="Kiểm tra và báo cáo quotas của người dùng",
    instruction="""
    Bạn là chuyên gia kiểm tra quota sử dụng của người dùng.
    
    Nhiệm vụ của bạn:
    1. Xác định gói dịch vụ hiện tại của người dùng
    2. Kiểm tra số lần sử dụng còn lại cho mỗi loại dịch vụ
    3. Đưa ra cảnh báo nếu quota sắp hết
    4. Tư vấn nâng cấp gói dịch vụ khi cần thiết
    
    Cung cấp thông tin chi tiết và chính xác về quota còn lại của người dùng.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.UserQuota,
    output_key="user_quota",
    generate_content_config=types.json_response_config,
)

payment_processing_agent = Agent(
    model="gemini-2.0-flash-001",
    name="payment_processing_agent",
    description="Xử lý các giao dịch thanh toán",
    instruction="""
    Bạn là chuyên gia xử lý thanh toán.
    
    Nhiệm vụ của bạn:
    1. Hướng dẫn quy trình thanh toán
    2. Giải thích các phương thức thanh toán khả dụng
    3. Trợ giúp xử lý các vấn đề thanh toán
    4. Xác nhận trạng thái giao dịch
    
    Phương thức thanh toán:
    - Thẻ tín dụng/ghi nợ
    - Chuyển khoản ngân hàng
    - Ví điện tử (MoMo, ZaloPay, VNPay)
    
    Đảm bảo hướng dẫn rõ ràng, chi tiết và hỗ trợ người dùng hoàn tất giao dịch.
    """,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    output_schema=types.PaymentResult,
    output_key="payment_result",
    generate_content_config=types.json_response_config,
)

# Tạo Payment agent chính
payment_agent = Agent(
    model="gemini-2.0-flash-001",
    name="payment_agent",
    description="Agent quản lý thanh toán và gói dịch vụ Phong Thủy Số",
    instruction=PAYMENT_AGENT_INSTR,
    tools=[
        memorize_tool,
        recall_tool,
        find_user_tool,
        get_user_subscription_tool
    ],
    sub_agents=[
        subscription_agent,
        quota_agent,
        payment_processing_agent
    ],
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
        top_p=0.8
    )
) 