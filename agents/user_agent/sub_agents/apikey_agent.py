"""
API Key Sub-Agent for UserAgent
"""

from typing import Any, Dict, List, Optional
from fastapi import Header, HTTPException # For dependency injection if needed directly

# Corrected imports
from shared_libraries.models import ApiKeyCreate
from shared_libraries.logger import get_logger
# Update tool import paths
from tools.user.api_key_tools import (
    create_api_key, 
    delete_api_key, 
    list_user_api_keys, 
    validate_api_key
)

class APIKeyAgent:
    """
    Handles API key management: creation, validation, listing, deletion.
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("APIKeyAgent initialized.")

    async def create_api_key_for_user(self, user_id: str, api_key_create: ApiKeyCreate) -> Dict[str, Any]:
        """
        Tạo API key mới cho người dùng.
        """
        self.logger.info(f"Creating API key for user: {user_id}, name: {api_key_create.name}")
        # Add potential checks here (e.g., limit number of keys per user)
        new_key = create_api_key(user_id, api_key_create)
        return new_key

    async def list_api_keys_for_user(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Liệt kê các API key của người dùng.
        """
        self.logger.info(f"Listing API keys for user: {user_id}")
        keys = list_user_api_keys(user_id)
        # Consider filtering sensitive info like the key itself before returning
        return keys

    async def delete_api_key_for_user(self, key_id: str, user_id: str) -> Dict[str, str]:
        """
        Xóa API key của người dùng.
        (Ensures user owns the key before deletion - handled in tool)
        """
        self.logger.info(f"Deleting API key: {key_id} for user: {user_id}")
        result = delete_api_key(key_id, user_id)
        return result
        
    async def validate_key(self, api_key_value: str) -> Optional[Dict[str, Any]]:
        """
        Xác thực một API key.
        """
        self.logger.debug(f"Validating API key ending with: ...{api_key_value[-4:] if api_key_value else 'N/A'}")
        # Delegate to the validation tool
        validation_result = validate_api_key(api_key_value)
        # Potentially add rate limiting checks here based on validation_result (e.g., user_id)
        return validation_result

    # --- Dependency-like method for FastAPI integration (optional) ---
    # This allows injecting API key validation logic easily into FastAPI endpoints
    # It mirrors the original validate_api_key_header but calls the internal method.
    async def get_validated_key_from_header(
        self, api_key: str = Header(None, alias="X-API-Key", convert_underscores=False) # Use alias for standard header name
    ) -> Optional[Dict[str, Any]]:
        """
        FastAPI Dependency: Validates API key from 'X-API-Key' header.
        Raises HTTPException 401 if invalid or missing.
        """
        if not api_key:
             raise HTTPException(
                 status_code=401,
                 detail="API Key required in X-API-Key header",
             )
        
        validation_result = await self.validate_key(api_key)
        
        if not validation_result or not validation_result.get("is_valid"):
             raise HTTPException(
                 status_code=401,
                 detail="Invalid or expired API Key",
             )
             
        # Optionally check for required scopes/permissions here
        # if not check_scopes(validation_result.get("scopes", []), required_scopes):
        #     raise HTTPException(status_code=403, detail="Insufficient permissions")
            
        self.logger.info(f"API Key validated successfully for user: {validation_result.get('user_id')}")
        return validation_result # Returns key info (user_id, scopes, etc.) 