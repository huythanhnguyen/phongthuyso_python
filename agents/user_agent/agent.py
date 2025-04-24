"""
User Agent Implementation

Triển khai UserAgent - Agent quản lý thông tin người dùng.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer

from python_adk.agents.agent_types import AgentType
from python_adk.agents.base_agent import BaseAgent
from python_adk.agents.user_agent.models import (
    ApiKey, ApiKeyCreate, Token, TokenData, User, UserCreate, UserUpdate
)
from python_adk.agents.user_agent.tools import (
    create_access_token, create_user, decode_token, 
    get_user_by_email, verify_password
)
from python_adk.shared_libraries.logger import get_logger

from .sub_agents.profile_agent import ProfileAgent
from .sub_agents.apikey_agent import APIKeyAgent

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/token")


# Tạo một agent kế thừa từ BaseAgent
class UserAgent(BaseAgent):
    """
    User Agent - Quản lý người dùng, xác thực và điều phối profile/API keys.
    """
    
    def __init__(self, name: str = "User Agent"):
        """
        Khởi tạo User Agent và các sub-agent.
        """
        # Ensure BaseAgent is initialized correctly (adapt if BaseAgent structure changed)
        super().__init__(name=name) # Assuming BaseAgent __init__ takes name
        self.logger = get_logger(name)
        
        # Instantiate Sub-Agents
        self.profile_agent = ProfileAgent()
        self.apikey_agent = APIKeyAgent()
        
        self.logger.info("UserAgent initialized with ProfileAgent and APIKeyAgent.")

    # --- Authentication Methods --- 
    async def register_user(self, user_create: UserCreate) -> Dict[str, Any]:
        """
        Đăng ký người dùng mới.
        """
        self.logger.info(f"Registering new user: {user_create.email}")
        # Uses the create_user tool
        user_data = create_user(user_create)
        return user_data
    
    async def login_user(self, username: str, password: str) -> Token:
        """
        Đăng nhập người dùng.
        """
        self.logger.info(f"Attempting login for user: {username}")
        # Uses get_user_by_email and verify_password tools
        user = get_user_by_email(username)
        if not user or not verify_password(password, user.get("hashed_password", "")):
            self.logger.warning(f"Login failed for user: {username}")
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        self.logger.info(f"Login successful for user: {username}")
        # Uses create_access_token tool
        access_token = create_access_token(
            data={"sub": user["email"], "user_id": user.get("id")}, # Include user_id if available/needed
            expires_delta=60 * 60 * 24 * 30  # 30 days
        )
        
        # Return user info without sensitive data
        user_info = {k: v for k, v in user.items() if k != 'hashed_password'}
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_info 
        }
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
        """
        FastAPI Dependency: Lấy thông tin người dùng hiện tại từ token.
        """
        # Uses decode_token and get_user_by_email tools
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
        
        # Return user info without sensitive data
        user_info = {k: v for k, v in user.items() if k != 'hashed_password'}
        return user_info
    
    async def get_current_active_user(
        self, current_user: Dict[str, Any] = Depends(get_current_user)
    ) -> Dict[str, Any]:
        """
        FastAPI Dependency: Lấy người dùng đang hoạt động.
        """
        # This depends on the output of get_current_user
        if not current_user.get("is_active", False):
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    # --- Routing to ProfileAgent --- 
    async def update_user_profile(self, email: str, user_update: UserUpdate, 
                                  current_user: Dict[str, Any] = Depends(get_current_active_user)
                                 ) -> Dict[str, Any]:
        """
        Endpoint Logic: Cập nhật hồ sơ người dùng (đã xác thực).
        """
        # Authorization check: User can only update their own profile
        if current_user.get("email") != email:
             raise HTTPException(status_code=403, detail="Not authorized to update this user profile")
             
        # Delegate to ProfileAgent
        return await self.profile_agent.update_user_profile(email, user_update)

    async def get_user_profile(self, email: str, 
                               current_user: Dict[str, Any] = Depends(get_current_active_user)
                              ) -> Dict[str, Any]:
        """
        Endpoint Logic: Lấy hồ sơ người dùng (đã xác thực).
        """
         # Authorization check: User can only get their own profile (or implement admin logic)
        if current_user.get("email") != email:
             raise HTTPException(status_code=403, detail="Not authorized to view this user profile")
        
        # Delegate to ProfileAgent (using placeholder implementation for now)
        return await self.profile_agent.get_user_profile(email)
        
    # --- Routing to APIKeyAgent --- 
    async def create_api_key(self, api_key_create: ApiKeyCreate,
                             current_user: Dict[str, Any] = Depends(get_current_active_user)
                            ) -> Dict[str, Any]:
        """
        Endpoint Logic: Tạo API key mới cho người dùng hiện tại.
        """
        user_id = current_user.get("id") # Assuming user_id is in the token/user object
        if not user_id:
             raise HTTPException(status_code=400, detail="User ID not found for API key creation")
             
        return await self.apikey_agent.create_api_key_for_user(user_id, api_key_create)

    async def get_api_keys(self, current_user: Dict[str, Any] = Depends(get_current_active_user)
                          ) -> List[Dict[str, Any]]:
        """
        Endpoint Logic: Lấy danh sách API key của người dùng hiện tại.
        """
        user_id = current_user.get("id")
        if not user_id:
             raise HTTPException(status_code=400, detail="User ID not found")
        return await self.apikey_agent.list_api_keys_for_user(user_id)

    async def delete_api_key(self, key_id: str, 
                             current_user: Dict[str, Any] = Depends(get_current_active_user)
                            ) -> Dict[str, str]:
        """
        Endpoint Logic: Xóa API key của người dùng hiện tại.
        """
        user_id = current_user.get("id")
        if not user_id:
             raise HTTPException(status_code=400, detail="User ID not found")
        # The apikey_agent method uses the user_id to ensure ownership before deleting
        return await self.apikey_agent.delete_api_key_for_user(key_id, user_id)
        
    # --- API Key Validation (delegated, potentially used as dependency) ---
    async def validate_api_key(self, api_key: str = Header(None, alias="X-API-Key", convert_underscores=False)
         ) -> Optional[Dict[str, Any]]:
         """
         FastAPI Dependency: Validates API key from header via APIKeyAgent.
         Raises HTTPException 401 if invalid/missing.
         """
         # Delegate to the dependency-like method in APIKeyAgent
         return await self.apikey_agent.get_validated_key_from_header(api_key)
    
    # Removed original process_message method, as agent interaction 
    # is likely handled via specific methods/routes now.

# Create an instance of the UserAgent
# user_agent = UserAgent() # Remove direct instantiation if handled by registry 