"""
Profile Sub-Agent for UserAgent
"""

from typing import Any, Dict

# Corrected imports
from agents.user_agent.models import UserUpdate
from shared_libraries.logger import get_logger
# Update tool import path
from tools.user.user_tools import update_user 

class ProfileAgent:
    """
    Handles user profile management.
    """
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("ProfileAgent initialized.")

    async def update_user_profile(self, email: str, user_update: UserUpdate) -> Dict[str, Any]:
        """
        Cập nhật thông tin hồ sơ người dùng.
        
        Args:
            email (str): Email của người dùng để xác định.
            user_update (UserUpdate): Dữ liệu cần cập nhật.
            
        Returns:
            Dict[str, Any]: Hồ sơ người dùng đã được cập nhật.
        """
        self.logger.info(f"Updating profile for user: {email}")
        # Delegate to the update_user tool/function
        # Note: The original UserAgent method didn't check ownership, 
        # potentially add checks here or in the tool.
        updated_user = update_user(email, user_update)
        return updated_user

    async def get_user_profile(self, email: str) -> Dict[str, Any]:
        """
        Lấy thông tin hồ sơ người dùng.
        (Placeholder - Assumes a get_user tool/function exists)
        """
        self.logger.info(f"Getting profile for user: {email}")
        # from ..tools import get_user_by_email # Assuming this exists
        # user = get_user_by_email(email) 
        # if not user:
        #     raise HTTPException(status_code=404, detail="User not found")
        # return user # Return relevant profile fields
        return {"email": email, "full_name": "Dummy User", "is_active": True} # Placeholder
        
    # Add other profile-related methods (e.g., change_password if not handled by auth) 