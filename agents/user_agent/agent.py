"""
User Agent Implementation

Triển khai UserAgent - Agent quản lý thông tin người dùng.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer

from phongthuyso_python.agents.agent_types import AgentType
from phongthuyso_python.agents.base_agent import BaseAgent
from phongthuyso_python.agents.user_agent.models import (
    ApiKey, ApiKeyCreate, Token, TokenData, User, UserCreate, UserUpdate
)
from phongthuyso_python.agents.user_agent.tools import (
    create_access_token, create_api_key, create_user, decode_token, 
    delete_api_key, get_user_by_email, list_user_api_keys, 
    update_user, validate_api_key, verify_password
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/token")


# Tạo một agent kế thừa từ BaseAgent
class UserAgent(BaseAgent):
    """
    User Agent - Agent quản lý thông tin người dùng
    """
    
    def __init__(self, name: str = "User Agent"):
        """
        Khởi tạo User Agent
        
        Args:
            name (str): Tên của agent
        """
        super().__init__(name=name, agent_type=AgentType.USER)
    
    async def register_user(self, user_create: UserCreate) -> Dict[str, Any]:
        """
        Đăng ký người dùng mới
        
        Args:
            user_create (UserCreate): Thông tin người dùng mới
            
        Returns:
            Dict[str, Any]: Thông tin người dùng đã đăng ký
        """
        user_data = create_user(user_create)
        
        return user_data
    
    async def login_user(self, username: str, password: str) -> Token:
        """
        Đăng nhập người dùng
        
        Args:
            username (str): Email của người dùng
            password (str): Mật khẩu
            
        Returns:
            Token: Token JWT và thông tin người dùng
        """
        user = get_user_by_email(username)
        if not user or not verify_password(password, user.get("hashed_password", "")):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(
            data={"sub": user["email"]},
            expires_delta=60 * 60 * 24 * 30  # 30 days
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {**user, "hashed_password": ""}
        }
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
        """
        Lấy thông tin người dùng hiện tại từ token
        
        Args:
            token (str): Token JWT
            
        Returns:
            Dict[str, Any]: Thông tin người dùng
        """
        payload = decode_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        username = payload.get("sub")
        user = get_user_by_email(username)
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    
    async def get_current_active_user(
        self, current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """
        Kiểm tra người dùng đang hoạt động
        
        Args:
            current_user (Dict[str, Any]): Thông tin người dùng hiện tại
            
        Returns:
            Dict[str, Any]: Thông tin người dùng nếu đang hoạt động
        """
        if not current_user.get("is_active", False):
            raise HTTPException(status_code=400, detail="Inactive user")
        
        return current_user
    
    async def update_user_info(
        self, email: str, user_update: UserUpdate
    ) -> Dict[str, Any]:
        """
        Cập nhật thông tin người dùng
        
        Args:
            email (str): Email của người dùng
            user_update (UserUpdate): Thông tin cần cập nhật
            
        Returns:
            Dict[str, Any]: Thông tin người dùng đã cập nhật
        """
        return update_user(email, user_update)
    
    async def validate_api_key_header(
        self, api_key: str = Header(None, convert_underscores=False)
    ) -> Optional[Dict[str, Any]]:
        """
        Xác thực API key từ header
        
        Args:
            api_key (str): API key
            
        Returns:
            Optional[Dict[str, Any]]: Thông tin API key nếu hợp lệ
        """
        if not api_key:
            return None
            
        return validate_api_key(api_key)
    
    async def create_new_api_key(
        self, user_id: str, api_key_create: ApiKeyCreate
    ) -> Dict[str, Any]:
        """
        Tạo API key mới
        
        Args:
            user_id (str): ID của người dùng
            api_key_create (ApiKeyCreate): Thông tin API key cần tạo
            
        Returns:
            Dict[str, Any]: Thông tin API key đã tạo
        """
        return create_api_key(user_id, api_key_create)
    
    async def get_user_api_keys(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Lấy danh sách API key của người dùng
        
        Args:
            user_id (str): ID của người dùng
            
        Returns:
            List[Dict[str, Any]]: Danh sách API key
        """
        return list_user_api_keys(user_id)
    
    async def delete_user_api_key(self, key_id: str, user_id: str) -> Dict[str, str]:
        """
        Xóa API key
        
        Args:
            key_id (str): ID của API key
            user_id (str): ID của người dùng
            
        Returns:
            Dict[str, str]: Thông báo kết quả
        """
        return delete_api_key(key_id, user_id)
    
    def process_message(self, message: str, context: Dict[str, Any]) -> str:
        """
        Xử lý tin nhắn từ người dùng
        
        Args:
            message (str): Tin nhắn của người dùng
            context (Dict[str, Any]): Ngữ cảnh của tin nhắn
            
        Returns:
            str: Phản hồi của agent
        """
        # Log the message
        self.update_context("last_message", message)
        self.update_context("last_context", context)
        
        # Return a simple response for now
        return f"User Agent đã nhận tin nhắn: {message}"
        

# Create an instance of the UserAgent
user_agent = UserAgent() 