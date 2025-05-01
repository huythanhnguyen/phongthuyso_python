"""
Root Agent Module

Cung cấp RootAgent - agent chính của hệ thống, sử dụng Google ADK để điều phối các yêu cầu.
"""

from google.adk.agents import Agent
from google.genai.types import GenerateContentConfig

# Import các prompts
from .prompts.adk_prompts import ROOT_AGENT_INSTR

# Import các sub-agent
from agents.batcuclinh_so_agent.agent import batcuclinh_so_agent
from agents.payment_agent.agent import payment_agent
from agents.user_agent.agent import user_agent

# Import các AgentTool thay vì hàm trực tiếp
from agents.tools.memory import memorize_tool, recall_tool, record_conversation_tool, get_conversation_history_tool, _load_precreated_itinerary
from agents.tools.mongodb_tools import find_user_tool, find_phone_analysis_tool, save_phone_analysis_tool, get_user_subscription_tool

# Tạo root agent
root_agent = Agent(
    model="gemini-2.0-flash-001",
    name="root_agent",
    description="Agent chính của hệ thống Phong Thủy Số, điều phối các yêu cầu đến các agent chuyên biệt",
    instruction=ROOT_AGENT_INSTR,
    tools=[
        # Memory tools
        memorize_tool,
        recall_tool,
        record_conversation_tool,
        get_conversation_history_tool,
        
        # MongoDB tools
        find_user_tool,
        find_phone_analysis_tool,
        save_phone_analysis_tool,
        get_user_subscription_tool
    ],
    sub_agents=[
        batcuclinh_so_agent,
        payment_agent,
        user_agent
    ],
    before_agent_callback=_load_precreated_itinerary,
    generate_content_config=GenerateContentConfig(
        temperature=0.2,
        top_p=0.8
    )
) 