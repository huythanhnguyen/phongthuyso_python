"""
Main Entry Point

Điểm vào chính của ứng dụng Phong Thủy Số.
"""

import os
import sys
import argparse
import logging
from typing import Dict, Optional, Any

from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Import the root agent instance directly
from python_adk.agents import root_agent
from python_adk.shared_libraries.logger import get_logger

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Phong Thủy Số API",
    description="API cho ứng dụng phân tích phong thủy số học",
    version="0.1.0"
)

def configure_logging():
    """Cấu hình logging cho ứng dụng"""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # Cấu hình cơ bản cho logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "app.log")),
            logging.StreamHandler(sys.stdout)
        ]
    )


def configure_gemini(api_key: Optional[str] = None):
    """
    Cấu hình Gemini API
    
    Args:
        api_key (Optional[str]): API key cho Gemini, nếu không cung cấp sẽ lấy từ môi trường
    """
    # Lấy API key từ môi trường nếu không được cung cấp
    if not api_key:
        # Ưu tiên lấy từ GOOGLE_API_KEY
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # Nếu không tìm thấy, thử lấy từ GEMINI_API_KEY
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")
        
    if not api_key:
        raise ValueError("Không tìm thấy API key. Vui lòng cung cấp GOOGLE_API_KEY hoặc GEMINI_API_KEY trong môi trường hoặc trực tiếp.")
    
    # Cấu hình Gemini
    genai.configure(api_key=api_key)


def run_interactive_shell(model_name: str):
    """
    Chạy shell tương tác với agent
    
    Args:
        model_name (str): Tên model Gemini sử dụng
    """
    logger = get_logger("InteractiveShell")
    logger.info(f"Khởi động shell tương tác với model {model_name}")
    
    # Sử dụng root_agent đã được khởi tạo
    # Lưu ý: model_name từ command line hiện không được sử dụng để cấu hình lại root_agent
    # Nếu cần cấu hình model động, cần cơ chế khác.
    
    print("\n===== Phong Thủy Số - Interactive Shell =====")
    print("Nhập 'exit' hoặc 'quit' để thoát\n")
    
    while True:
        try:
            # Nhận input từ người dùng
            user_input = input("\nBạn: ")
            
            # Kiểm tra thoát
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Tạm biệt!")
                break
            
            # Xử lý input với Root Agent (instance đã import)
            # Lưu ý: Phương thức 'run' không tồn tại trên GeminiAgent, sử dụng 'invoke'
            # Xử lý input với Root Agent
            response = root_agent.invoke(user_input)
            
            # Hiển thị phản hồi
            print(f"\nPhong Thủy Số: {response}")
            
        except KeyboardInterrupt:
            print("\nTạm biệt!")
            break
        except Exception as e:
            logger.error(f"Lỗi: {e}")
            print(f"\nCó lỗi xảy ra: {e}")


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Phong Thủy Số - Ứng dụng phân tích phong thủy số học")
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="gemini-1.5-pro",
        help="Model Gemini sử dụng (mặc định: gemini-1.5-pro)"
    )
    
    parser.add_argument(
        "--api-key", 
        type=str, 
        help="Google API key cho Gemini (nếu không cung cấp, sẽ lấy từ GOOGLE_API_KEY hoặc GEMINI_API_KEY trong môi trường)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point của ứng dụng"""
    # Load environment variables
    load_dotenv()
    
    # Cấu hình logging
    configure_logging()
    
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        # Cấu hình Gemini
        configure_gemini(api_key=args.api_key)
        
        # Kiểm tra nếu đang chạy trong môi trường có thể tương tác
        import sys
        import os
        
        # Kiểm tra nếu stdin được kết nối với terminal (interactive)
        is_interactive = os.isatty(sys.stdin.fileno()) if hasattr(sys.stdin, 'fileno') else False
        
        if is_interactive:
            # Chỉ chạy shell nếu đang trong môi trường tương tác
            run_interactive_shell(model_name=args.model)
        else:
            # Nếu không phải môi trường tương tác (ví dụ: Render), chạy FastAPI app
            logger = get_logger("Main")
            logger.info("Khởi động trong môi trường không tương tác. Bắt đầu FastAPI app...")
            
            # Lấy port từ biến môi trường hoặc sử dụng port mặc định
            port = int(os.environ.get("PORT", 10000))
            
            # Log thông tin về port
            logger.info(f"Khởi động FastAPI app trên port {port}")
            print(f"Ứng dụng khởi động trên port {port}...")
            
            # Chạy FastAPI app với Uvicorn
            uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        
    except Exception as e:
        logging.error(f"Lỗi khi khởi động ứng dụng: {e}")
        print(f"Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Định nghĩa các models cho API
class UserMessage(BaseModel):
    """Model cho user message trong API"""
    message: Optional[str] = None  # Make it optional since we might get 'text' instead
    text: Optional[str] = None  # Thêm field text để tương thích với frontend
    sessionId: Optional[str] = None  # Thêm field sessionId
    session_id: Optional[str] = None  # Thêm field session_id để tương thích với Node.js API
    user_id: Optional[str] = None     # Thêm field user_id để tương thích với Node.js API
    metadata: Optional[Dict[str, Any]] = None  # Thêm field metadata
    stream: Optional[bool] = False    # Thêm field stream cho streaming API

class AgentResponse(BaseModel):
    """Model cho response từ agent trong API"""
    response: str
    text: Optional[str] = None  # Thêm field text để tương thích với frontend
    success: bool = True
    agent_type: str = "root"  # Thêm field agent_type để tương thích với Node.js API

class ChatSession(BaseModel):
    """Model cho chat session"""
    sessionId: str
    session_id: Optional[str] = None  # Thêm field session_id để tương thích với Node.js API

# --- API Routes ---
# Endpoint /chat cho Node.js API Gateway
@app.post("/chat")
async def chat_endpoint(user_message: UserMessage):
    """
    Endpoint chính cho Node.js API Gateway
    """
    try:
        # Log the request
        logger = get_logger("API")
        logger.info(f"Nhận API request từ Node.js: {user_message.message or user_message.text}")
        
        # Gọi root agent để xử lý tin nhắn
        message_text = user_message.message or user_message.text or ""
        response = root_agent.invoke(message_text)
        
        # Trả về response theo format mà Node.js API Gateway mong đợi
        return {
            "response": response,
            "success": True,
            "agent_type": "root"
        }
    except Exception as e:
        logger.error(f"Lỗi xử lý API request: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý request: {str(e)}")

# Endpoint /chat/stream cho Node.js API Gateway
@app.post("/chat/stream")
async def chat_stream_endpoint(user_message: UserMessage):
    """
    Endpoint stream cho Node.js API Gateway
    """
    from fastapi.responses import StreamingResponse
    import json
    import asyncio
    
    try:
        # Log the request
        logger = get_logger("API")
        logger.info(f"Nhận stream request từ Node.js: {user_message.message or user_message.text}")
        
        # Gọi root agent để xử lý tin nhắn
        message_text = user_message.message or user_message.text or ""
        response = root_agent.invoke(message_text)
        
        # Giả lập streaming bằng cách chia nhỏ phản hồi
        async def fake_stream():
            # Chia phản hồi thành các chunk nhỏ
            chunk_size = 10  # Số ký tự mỗi chunk
            for i in range(0, len(response), chunk_size):
                chunk = response[i:i+chunk_size]
                # Format theo định dạng SSE mà Node.js đang mong đợi
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                await asyncio.sleep(0.05)  # Tạm dừng để giả lập stream
            
            # Gửi sự kiện hoàn thành
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
        
        # Trả về streaming response
        return StreamingResponse(
            fake_stream(),
            media_type="text/event-stream"
        )
    except Exception as e:
        logger.error(f"Lỗi xử lý stream request: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý request: {str(e)}")

# Thêm route /agent/chat để tương thích với frontend
@app.post("/agent/chat", response_model=ChatSession)
async def create_chat_session():
    """
    Tạo phiên chat mới
    """
    try:
        # Generate a simple session ID
        import uuid
        session_id = str(uuid.uuid4())
        
        # Log the session creation
        logger = get_logger("API")
        logger.info(f"Tạo phiên chat mới: {session_id}")
        
        # Return the session ID
        return ChatSession(sessionId=session_id, session_id=session_id)
    except Exception as e:
        logger.error(f"Lỗi tạo phiên chat: {e}")
        # Return a JSON response rather than raising an HTTPException
        return {"error": "Đã xảy ra lỗi khi xử lý tin nhắn", "detail": str(e)}

# Thêm route /agent/stream để tương thích với frontend
@app.post("/agent/stream")
async def stream_chat(user_message: UserMessage):
    """
    Endpoint cho phép chat với agent và nhận response dạng stream
    """
    try:
        # Log the request
        logger = get_logger("API")
        logger.info(f"Nhận stream request: {user_message.message or user_message.text}")
        
        # Kiểm tra session ID
        if not user_message.sessionId and not user_message.session_id:
            logger.error("Không có phiên chat trong request")
            return {"error": "Không có phiên chat. Vui lòng tạo phiên mới."}
        
        # Extract message
        message_text = user_message.message or user_message.text or ""
        
        # Gọi root agent để xử lý tin nhắn
        try:
            response = root_agent.invoke(message_text)
            # Trả về response dạng JSON
            return {"text": response, "done": True}
        except Exception as agent_error:
            logger.error(f"Lỗi khi gọi agent: {agent_error}")
            return {"error": f"Lỗi khi gọi agent: {str(agent_error)}", "done": True}
            
    except Exception as e:
        logger.error(f"Lỗi xử lý stream request: {e}")
        # Return a JSON response rather than raising an HTTPException
        return {"error": "Đã xảy ra lỗi khi xử lý tin nhắn", "detail": str(e)}

# Thêm route /query để tương thích với frontend cũ
@app.post("/query")
async def legacy_query(user_message: UserMessage):
    """
    Endpoint cũ cho phép query agent
    """
    try:
        # Extract message text from either message or text field
        message_text = user_message.message or user_message.text or ""
        response = root_agent.invoke(message_text)
        return {"response": response}
    except Exception as e:
        logger.error(f"Lỗi xử lý query request: {e}")
        raise HTTPException(status_code=500, detail=f"Đã xảy ra lỗi khi xử lý tin nhắn")

# Thêm API version prefix
@app.post("/api/v2/agent/chat", response_model=ChatSession)
async def create_chat_session_v2():
    """
    Alias cho /agent/chat với prefix API v2
    """
    return await create_chat_session()

@app.post("/api/v2/agent/stream")
async def stream_chat_v2(user_message: UserMessage):
    """
    Alias cho /agent/stream với prefix API v2
    """
    return await stream_chat(user_message)

@app.get("/")
async def root():
    """
    Root endpoint, trả về thông tin cơ bản về API
    """
    return {
        "name": "Phong Thủy Số API",
        "version": "0.1.0",
        "description": "API cho ứng dụng phân tích phong thủy số học",
        "endpoints": {
            "/api/chat": "Gửi tin nhắn đến agent và nhận phản hồi",
            "/agent/chat": "Tạo phiên chat mới",
            "/agent/stream": "Gửi tin nhắn và nhận phản hồi dạng stream",
            "/health": "Kiểm tra trạng thái hoạt động của API"
        }
    }

@app.get("/health")
async def health_check():
    """
    Endpoint kiểm tra trạng thái hoạt động của ứng dụng.
    Sử dụng bởi Docker healthcheck.
    """
    return {"status": "healthy", "version": "0.1.0"}

# Giữ lại /api/chat endpoint cho direct access
@app.post("/api/chat", response_model=AgentResponse)
async def chat_with_agent(user_message: UserMessage):
    """
    Endpoint cho phép chat với agent thông qua API request trực tiếp
    """
    try:
        # Log the request
        logger = get_logger("API")
        logger.info(f"Nhận API request trực tiếp: {user_message.message or user_message.text}")
        
        # Gọi root agent để xử lý tin nhắn
        message_text = user_message.message or user_message.text or ""
        response = root_agent.invoke(message_text)
        
        # Trả về response
        return AgentResponse(response=response, text=response)
    except Exception as e:
        logger.error(f"Lỗi xử lý API request: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý request: {str(e)}") 
