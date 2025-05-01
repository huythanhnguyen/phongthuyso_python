"""
Main FastAPI Application Module - Simple Version

This module initializes a simple FastAPI application for Phong Thuy So
"""

import json
import logging
import os
import uuid
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, Query, Request, UploadFile, Depends, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

# Khởi tạo các biến môi trường
env_mode = os.environ.get("ENV_MODE", "dev")
port = int(os.environ.get("PORT", 8000))

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO if env_mode == "prod" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Mô phỏng agent system nếu không có Google ADK
# Cấu trúc mô phỏng (Mock)
class MockAgent:
    """Mock agent cho môi trường dev"""
    def __init__(self, name="Mock Agent"):
        self.name = name
        self.sub_agents = {}
        
    async def route_request(self, target_agent_type=None, request_data=None):
        """Mô phỏng xử lý request"""
        return {
            "agent": self.name,
            "status": "success",
            "content": f"Đây là phản hồi mô phỏng từ {self.name}",
            "metadata": {"request": request_data}
        }
        
    async def process_direct_root_request(self, request_data=None):
        """Mô phỏng xử lý request trực tiếp"""
        return {
            "agent": self.name,
            "status": "success",
            "content": f"Đây là phản hồi mô phỏng trực tiếp từ {self.name}",
            "metadata": {"request": request_data}
        }
        
    def register_agent(self, agent_type, agent):
        """Đăng ký sub-agent"""
        self.sub_agents[agent_type] = agent
        
# Tạm thời bỏ qua các import của agent system vì đang gặp vấn đề
# Các import này sẽ được khôi phục khi cấu trúc agent được sửa đúng
# Import Agent System
try:
    # Thử import các agent từ file
    from agents.root_agent.agent import root_agent
    from agents.agent_types import AgentType
    from agents.batcuclinh_so_agent.agent import batcuclinh_so_agent
    from agents.payment_agent.agent import payment_agent
    from agents.user_agent.agent import user_agent
    
    HAS_REAL_AGENTS = True
    logger.info("Loaded real agent system")
except ImportError as e:
    # Nếu không import được, sử dụng mock agent
    from agents.agent_types import AgentType
    
    # Tạo mock agents
    root_agent = MockAgent(name="Root Agent")
    batcuclinh_so_agent = MockAgent(name="BatCucLinhSo Agent")
    payment_agent = MockAgent(name="Payment Agent")
    user_agent = MockAgent(name="User Agent")
    
    # Đăng ký sub-agent
    root_agent.register_agent(AgentType.BAT_CUC_LINH_SO, batcuclinh_so_agent)
    root_agent.register_agent(AgentType.PAYMENT, payment_agent)
    root_agent.register_agent(AgentType.USER, user_agent)
    
    HAS_REAL_AGENTS = False
    logger.warning(f"Using mock agents due to import error: {e}")

# Import request/response models from shared_libraries
try:
    from shared_libraries.models import (
        BatCucLinhSoRequest,
        PhoneAnalysisRequest,
        CCCDAnalysisRequest,
        BankAccountRequest,
        PasswordRequest,
        PaymentRequest,
        SubscriptionRequest
    )
except ImportError:
    # Tạo các class mô phỏng nếu không import được
    class BaseRequest(BaseModel):
        """Lớp cơ sở cho request"""
        pass
        
    class BatCucLinhSoRequest(BaseRequest):
        """Mô phỏng request BatCucLinhSo"""
        pass
        
    class PhoneAnalysisRequest(BaseRequest):
        """Mô phỏng request PhoneAnalysis"""
        phone_number: str
        
    class CCCDAnalysisRequest(BaseRequest):
        """Mô phỏng request CCCDAnalysis"""
        cccd_number: str
        
    class BankAccountRequest(BaseRequest):
        """Mô phỏng request BankAccount"""
        account_number: str
        
    class PasswordRequest(BaseRequest):
        """Mô phỏng request Password"""
        password: str
        
    class PaymentRequest(BaseRequest):
        """Mô phỏng request Payment"""
        amount: float
        
    class SubscriptionRequest(BaseRequest):
        """Mô phỏng request Subscription"""
        plan_id: str
        
    logger.warning("Using mock request models due to import error")

# Định nghĩa lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Phong Thuy API")
    
    # Khởi tạo kết nối MongoDB
    try:
        from shared_libraries.database.mongodb import init_db
        await init_db()
        logger.info("Đã khởi tạo kết nối MongoDB thành công")
    except Exception as e:
        logger.error(f"Lỗi khi khởi tạo kết nối MongoDB: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Phong Thuy API")
    
    # Đóng kết nối MongoDB
    try:
        from shared_libraries.database.mongodb import close_connection
        await close_connection()
        logger.info("Đã đóng kết nối MongoDB thành công")
    except Exception as e:
        logger.error(f"Lỗi khi đóng kết nối MongoDB: {e}")

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Phong Thuy API",
    description="API for Phong Thuy So Bot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các origin
    allow_credentials=False,  # Không sử dụng credentials
    allow_methods=["*"],  # Cho phép tất cả các HTTP methods
    allow_headers=["*"],  # Cho phép tất cả các headers
    expose_headers=["*"],  # Expose tất cả các headers
)

# Thiết lập OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/user/token")

# Thêm static files và templates
templates_path = os.path.join(os.path.dirname(__file__), "templates")
static_path = os.path.join(os.path.dirname(__file__), "static")

try:
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    templates = Jinja2Templates(directory=templates_path)
    logger.info(f"Mounted static files from {static_path} and templates from {templates_path}")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")
    templates = None

# Tạo thư mục uploads nếu chưa tồn tại
uploads_path = os.path.join(static_path, "uploads")
os.makedirs(uploads_path, exist_ok=True)

# Models
class ProcessMessageRequest(BaseModel):
    """Request model for processing a message."""
    
    message: str
    context: Optional[Dict[str, Any]] = None


class ProcessMessageResponse(BaseModel):
    """Response model for a processed message."""
    
    agent: str
    status: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ChatRequest(BaseModel):
    """Request model for chat."""
    
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response model for chat."""
    
    agent: str
    status: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    is_final: bool = True


# User Models
class UserBase(BaseModel):
    """Base user model."""
    
    email: EmailStr
    fullname: str


class UserCreate(BaseModel):
    """Model for user creation."""
    
    name: str
    email: EmailStr
    password: str
    phoneNumber: Optional[str] = None


class UserUpdate(BaseModel):
    """Model for user update."""
    
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(BaseModel):
    """User model."""
    
    id: Optional[str] = None
    name: str
    email: EmailStr
    role: str = "user"
    phoneNumber: Optional[str] = None
    remainingQuestions: int = 0
    isPremium: bool = False
    createdAt: datetime
    lastLogin: Optional[datetime] = None
    # Không trả về password
    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """Token data model."""
    
    username: str
    exp: Optional[int] = None


class Token(BaseModel):
    """Authentication token model."""
    
    access_token: str
    token_type: str
    user: User


# API Key Models
class ApiKeyCreate(BaseModel):
    """Model for API key creation."""
    
    name: str
    expires_at: Optional[datetime] = None


class ApiKey(BaseModel):
    """API key model."""
    
    id: str
    key: str
    name: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    is_active: bool


# Payment Models
class PlanType(str, Enum):
    """Subscription plan types."""
    
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class Plan(BaseModel):
    """Subscription plan model."""
    
    id: str
    name: str
    type: PlanType
    price: float
    currency: str = "VND"
    interval: str = "month"
    description: str
    features: List[str]
    quota: int
    created_at: datetime
    updated_at: datetime


class PaymentCreate(BaseModel):
    """Model for creating a payment."""
    
    plan_id: str
    payment_method: str
    amount: float
    currency: str = "VND"


class Payment(BaseModel):
    """Payment model."""
    
    id: str
    user_id: str
    plan_id: str
    payment_method: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    updated_at: datetime
    transaction_id: Optional[str] = None


class Subscription(BaseModel):
    """Subscription model."""
    
    id: str
    user_id: str
    plan_id: str
    status: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
    is_active: bool
    auto_renew: bool


# Mock database for development
mock_users = {}
mock_api_keys = {}
mock_payments = {}
mock_subscriptions = {}
mock_plans = {
    "free": {
        "id": "free",
        "name": "Miễn phí",
        "type": "free",
        "price": 0,
        "currency": "VND",
        "interval": "month",
        "description": "Gói dùng thử miễn phí",
        "features": ["Phân tích cơ bản số điện thoại", "5 lần phân tích/ngày"],
        "quota": 5,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    "basic": {
        "id": "basic",
        "name": "Cơ bản",
        "type": "basic",
        "price": 99000,
        "currency": "VND",
        "interval": "month",
        "description": "Gói cơ bản cho người dùng cá nhân",
        "features": ["Phân tích đầy đủ số điện thoại", "Phân tích CCCD", "50 lần phân tích/tháng"],
        "quota": 50,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    "premium": {
        "id": "premium",
        "name": "Cao cấp",
        "type": "premium",
        "price": 199000,
        "currency": "VND",
        "interval": "month",
        "description": "Gói cao cấp cho người dùng chuyên nghiệp",
        "features": ["Tất cả tính năng của gói Cơ bản", "Phân tích STK ngân hàng", "Phân tích mật khẩu", "200 lần phân tích/tháng"],
        "quota": 200,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
}

# Security utilities
def get_password_hash(password: str) -> str:
    """Generate password hash."""
    # Trong thực tế nên sử dụng thư viện mã hóa như passlib
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    return get_password_hash(plain_password) == hashed_password


def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Create JWT token."""
    # Giả lập JWT trong phiên bản demo
    import time
    import base64
    import json
    
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": time.time() + expires_delta})
    
    encoded_jwt = base64.b64encode(json.dumps(to_encode).encode()).decode()
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode JWT token."""
    try:
        import base64
        import json
        
        decoded = base64.b64decode(token).decode()
        return json.loads(decoded)
    except Exception:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from token."""
    from shared_libraries.database.mongodb import db
    
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    user = await db.user.find_one({"email": username})
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Check if user is active."""
    # Kiểm tra trường is_active nếu có, nếu không thì mặc định là True
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def validate_api_key(api_key: str = Header(..., convert_underscores=False)) -> Dict[str, Any]:
    """Validate API key."""
    try:
        from shared_libraries.database.mongodb import db
        # Tìm apikey trong database
        key_data = await db.apikey.find_one({"key": api_key, "is_active": True})
        
        if key_data:
            # Cập nhật last_used_at
            await db.apikey.update_one(
                {"_id": key_data["_id"]},
                {"$set": {"last_used_at": datetime.now()}}
            )
            
            # Kiểm tra xem key đã hết hạn chưa
            if key_data.get("expires_at") and key_data["expires_at"] < datetime.now():
                raise HTTPException(status_code=401, detail="API key expired")
                
            # Lấy thông tin user
            user = await db.user.find_one({"id": key_data["user_id"]})
            if not user or not user.get("is_active", False):
                raise HTTPException(status_code=401, detail="User not active")
                
            return key_data
        
        # Fallback vào mock_api_keys cho môi trường dev/test
        for key_id, key_info in mock_api_keys.items():
            if key_info["key"] == api_key and key_info["is_active"]:
                # Cập nhật last_used_at
                key_info["last_used_at"] = datetime.now()
                
                # Kiểm tra xem key đã hết hạn chưa
                if key_info.get("expires_at") and key_info["expires_at"] < datetime.now():
                    raise HTTPException(status_code=401, detail="API key expired")
                    
                # Lấy thông tin user
                user = mock_users.get(key_info["user_id"])
                if not user or not user.get("is_active", False):
                    raise HTTPException(status_code=401, detail="User not active")
                    
                return key_info
            
        raise HTTPException(status_code=401, detail="Invalid API key")
    except Exception as e:
        logger.error(f"Error validating API key: {e}")
        raise HTTPException(status_code=401, detail="Invalid API key")


# User endpoints
@app.post("/api/user/register", response_model=User)
async def register_user(user: UserCreate):
    """Register a new user."""
    from shared_libraries.database.mongodb import db
    
    # Hiển thị dữ liệu để debug
    logger.info(f"Register request data: {user.dict()}")
    
    existing_user = await db.user.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    
    user_data = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "password": hashed_password,  # Lưu password đã hash, không phải password gốc
        "role": "user",
        "phoneNumber": user.phoneNumber,
        "remainingQuestions": mock_plans["free"]["quota"],
        "isPremium": False,
        "createdAt": datetime.now(),
        "lastLogin": None
    }
    
    logger.info(f"Creating user with data: {user_data}")
    
    await db.user.insert_one(user_data)
    
    # Tạo subscription miễn phí
    subscription_id = str(uuid.uuid4())
    subscription_data = {
        "id": subscription_id,
        "user_id": user_id,
        "plan_id": "free",
        "status": "active",
        "start_date": datetime.now(),
        "end_date": datetime.now().replace(month=datetime.now().month + 1),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True,
        "auto_renew": False
    }
    
    await db.subscription.insert_one(subscription_data)
    
    # Trả về user không có password
    user_data_to_return = user_data.copy()
    user_data_to_return.pop("password", None)
    
    return user_data_to_return


@app.post("/api/user/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login to get access token."""
    from shared_libraries.database.mongodb import db
    
    logger.info(f"Login attempt for username: {form_data.username}")
    
    # Tìm user trong MongoDB
    user = await db.user.find_one({"email": form_data.username})
    
    if not user:
        logger.warning(f"User not found: {form_data.username}")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Kiểm tra password
    stored_password = user.get("password", "")
    if not verify_password(form_data.password, stored_password):
        logger.warning(f"Invalid password for user: {form_data.username}")
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cập nhật thời gian đăng nhập gần nhất
    await db.user.update_one(
        {"email": form_data.username},
        {"$set": {"lastLogin": datetime.now()}}
    )
    
    # Tạo access token
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=60 * 60 * 24 * 30  # 30 days
    )
    
    # Đảm bảo không trả về password
    user_without_password = {k: v for k, v in user.items() if k != "password"}
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_without_password
    }


@app.get("/api/user/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return {**current_user, "hashed_password": ""}


@app.put("/api/user/me", response_model=User)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update user information."""
    from shared_libraries.database.mongodb import db
    
    # Lấy user hiện tại từ MongoDB
    user_data = await db.user.find_one({"email": current_user["email"]})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = {}
    
    if user_update.fullname:
        update_data["fullname"] = user_update.fullname
    
    if user_update.email and user_update.email != current_user["email"]:
        # Kiểm tra email mới đã tồn tại chưa
        existing_user = await db.user.find_one({"email": user_update.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        update_data["email"] = user_update.email
    
    if user_update.password:
        update_data["hashed_password"] = get_password_hash(user_update.password)
    
    update_data["updated_at"] = datetime.now()
    
    # Cập nhật trong MongoDB
    await db.user.update_one(
        {"email": current_user["email"]},
        {"$set": update_data}
    )
    
    # Lấy dữ liệu user đã cập nhật
    updated_user = await db.user.find_one({"email": user_update.email if user_update.email else current_user["email"]})
    return {**updated_user, "hashed_password": ""}


# API Keys endpoints
@app.post("/api/apikeys", response_model=ApiKey)
async def create_api_key(
    api_key_create: ApiKeyCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new API key."""
    api_key_id = str(uuid.uuid4())
    api_key = f"pts_{uuid.uuid4().hex}"
    
    api_key_data = {
        "id": api_key_id,
        "key": api_key,
        "name": api_key_create.name,
        "user_id": current_user["id"],
        "created_at": datetime.now(),
        "expires_at": api_key_create.expires_at,
        "last_used_at": None,
        "is_active": True
    }
    
    mock_api_keys[api_key_id] = api_key_data
    
    return api_key_data


@app.get("/api/apikeys", response_model=List[ApiKey])
async def list_api_keys(current_user: User = Depends(get_current_active_user)):
    """List all API keys for the current user."""
    user_api_keys = [
        key for key in mock_api_keys.values() 
        if key["user_id"] == current_user["id"]
    ]
    
    return user_api_keys


@app.delete("/api/apikeys/{api_key_id}", response_model=Dict[str, str])
async def delete_api_key(
    api_key_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete an API key."""
    if api_key_id not in mock_api_keys:
        raise HTTPException(status_code=404, detail="API key not found")
    
    if mock_api_keys[api_key_id]["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this API key")
    
    del mock_api_keys[api_key_id]
    
    return {"message": "API key deleted successfully"}


# Routes
@app.get("/", include_in_schema=False)
async def read_root(request: Request):
    """Root endpoint that renders the home page."""
    if templates:
        return templates.TemplateResponse(
            "index.html", {"request": request, "version": app.version}
        )
    else:
        return {"message": "Welcome to Phong Thuy API", "version": app.version}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": app.version}


@app.get("/agents")
async def get_agents():
    """Get the list of available agents."""
    return {
        "agents": [
            {
                "name": "Root Agent",
                "type": "root",
                "description": "Agent chính điều phối các yêu cầu",
                "sub_agents": [
                    {"name": "BatCucLinhSo Agent", "type": "batcuclinh_so"},
                    {"name": "Payment Agent", "type": "payment"},
                    {"name": "User Agent", "type": "user"}
                ]
            }
        ]
    }


@app.get("/analyze_number")
async def analyze_number(
    number: str = Query(..., description="The phone number to analyze"),
    user_data: Optional[str] = Query(None, description="Additional user data in JSON format"),
    current_user: Optional[User] = Depends(get_current_user),
    api_key: Optional[str] = Header(None, convert_underscores=False)
):
    """Analyze a phone number."""
    # Authenticate with either user session or API key
    user = None
    if current_user:
        user = current_user
    elif api_key:
        key_data = None
        try:
            key_data = await validate_api_key(api_key)
            user = mock_users.get(key_data["user_id"])
        except HTTPException:
            pass
    
    # Check if user exists and has quota
    if user:
        # Check quota
        if user["remainingQuestions"] <= 0:
            raise HTTPException(
                status_code=402,
                detail="Quota exceeded. Please upgrade your subscription."
            )
        
        # Reduce quota
        user["remainingQuestions"] -= 1
    
    # Phân tích số điện thoại bằng BatCucLinhSoAgent
    try:
        user_data_dict = {}
        if user_data:
            try:
                user_data_dict = json.loads(user_data)
            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=400, 
                    content={
                        "status": "error", 
                        "detail": "Invalid JSON format for user_data"
                    }
                )

        # Tạo request model
        phone_request = PhoneAnalysisRequest(
            phone_number=number,
            **user_data_dict  # Thêm các trường bổ sung nếu có
        )
        
        # Gọi trực tiếp đến BatCucLinhSoAgent hoặc thông qua RootAgent
        # Phương pháp 1: Sử dụng RootAgent để điều hướng
        response = await root_agent.route_request(
            target_agent_type=AgentType.BAT_CUC_LINH_SO,
            request_data=phone_request
        )
        
        # Thêm thông tin user vào metadata nếu cần
        if "metadata" not in response:
            response["metadata"] = {}
            
        if user:
            response["metadata"]["user_info"] = {
                "email": user["email"], 
                "remainingQuestions": user["remainingQuestions"]
            }
        
        # Lưu kết quả phân tích vào MongoDB nếu user đã đăng nhập
        if user:
            try:
                # Import service phân tích từ thư mục batcuclinhso_analysis
                from tools.batcuclinhso_analysis.phone_analysis_db import save_phone_analysis
                
                # Chuẩn bị dữ liệu kết quả phân tích
                analysis_result = {
                    "starSequence": response.get("analysis", {}).get("star_sequence", []),
                    "energyLevel": response.get("analysis", {}).get("energy_level", {}),
                    "balance": response.get("analysis", {}).get("balance", ""),
                    "starCombinations": response.get("analysis", {}).get("star_combinations", []),
                    "keyCombinations": response.get("analysis", {}).get("key_combinations", []),
                    "dangerousCombinations": response.get("analysis", {}).get("dangerous_combinations", []),
                    "keyPositions": response.get("analysis", {}).get("key_positions", {}),
                    "last3DigitsAnalysis": response.get("analysis", {}).get("last_3_digits", {}),
                    "specialAttribute": response.get("analysis", {}).get("special_attribute", "")
                }
                
                # Lấy phản hồi từ API
                gemini_response = response.get("message", "")
                
                # Lưu vào database
                analysis_id = await save_phone_analysis(
                    user_id=user["id"],
                    phone_number=number,
                    analysis_result=analysis_result,
                    gemini_response=gemini_response
                )
                
                # Thêm ID phân tích vào response
                response["metadata"]["analysis_id"] = analysis_id
                logger.info(f"Đã lưu phân tích số {number} với ID: {analysis_id}")
                
            except Exception as e:
                logger.error(f"Lỗi khi lưu phân tích số điện thoại: {e}")
                # Không raise exception ở đây, chỉ log lỗi và tiếp tục trả về kết quả
                
        return response
        
    except Exception as e:
        logger.exception(f"Error analyzing number: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error", 
                "detail": str(e)
            }
        )


@app.post("/api/chat")
async def post_chat(
    request: ChatRequest,
    current_user: Optional[User] = Depends(get_current_user),
    api_key: Optional[str] = Header(None, convert_underscores=False)
):
    """Send a message to the agent system."""
    # Authenticate with either user session or API key
    user = None
    if current_user:
        user = current_user
    elif api_key:
        key_data = None
        try:
            key_data = await validate_api_key(api_key)
            user = mock_users.get(key_data["user_id"])
        except HTTPException:
            pass
    
    # Check if user exists and has quota
    if user:
        # Check quota
        if user["remainingQuestions"] <= 0:
            raise HTTPException(
                status_code=402,
                detail="Quota exceeded. Please upgrade your subscription."
            )
        
        # Reduce quota
        user["remainingQuestions"] -= 1
    
    # Xử lý chat thông qua RootAgent
    try:
        message = request.message
        context = request.context or {}
        
        # Thêm thông tin user vào context nếu có
        if user:
            context["user_id"] = user["id"]
            context["user_email"] = user["email"]
            context["is_premium"] = user.get("isPremium", False)
        
        # Tạo request cho RootAgent
        direct_root_request = {
            "message": message,
            "context": context
        }
        
        # Kiểm tra nếu request chỉ định agent cụ thể
        target_agent_type = None
        request_agent = context.get("request_agent")
        if request_agent:
            try:
                target_agent_type = AgentType[request_agent]
                logger.info(f"Routing to specific agent: {target_agent_type.name}")
            except (KeyError, ValueError):
                logger.warning(f"Invalid agent type specified: {request_agent}")
        
        # Định tuyến request đến agent cụ thể nếu được chỉ định
        if target_agent_type:
            response = await root_agent.route_request(
                target_agent_type=target_agent_type,
                request_data=direct_root_request
            )
        else:
            # Gọi trực tiếp đến RootAgent
            response = await root_agent.process_direct_root_request(direct_root_request)
        
        # Đảm bảo response có đúng format
        if not isinstance(response, dict):
            response = {
                "agent": "Root Agent",
                "status": "success",
                "content": str(response),
                "metadata": context
            }
        
        # Đảm bảo response có các trường bắt buộc
        if "agent" not in response:
            response["agent"] = "Root Agent"
        if "status" not in response:
            response["status"] = "success"
        if "content" not in response:
            response["content"] = "Không có nội dung phản hồi"
        if "metadata" not in response:
            response["metadata"] = {}
        
        # Thêm thông tin user vào metadata
        if user:
            response["metadata"]["user_info"] = {
                "email": user["email"], 
                "remainingQuestions": user["remainingQuestions"]
            }
            
        return response
        
    except Exception as e:
        logger.exception(f"Error processing chat: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error", 
                "detail": str(e)
            }
        )


async def stream_response(session_id: str, message: Optional[str] = None, user_id: Optional[str] = None):
    """Generate streaming responses."""
    try:
        # Sử dụng message từ parameter nếu có
        default_message = "Phân tích số điện thoại của tôi một cách chi tiết"
        message = message or default_message
        
        # Nếu session_id khác "unknown", cố gắng lấy message từ session
        if session_id != "unknown" and not message:
            try:
                # TODO: Lấy tin nhắn từ session database
                pass
            except Exception as e:
                logger.warning(f"Không thể lấy tin nhắn từ session {session_id}: {e}")
        
        # Tạo context với các tham số cần thiết
        context = {
            "session_id": session_id,
            "streaming": True
        }
        
        # Thêm user_id vào context nếu có
        if user_id:
            context["user_id"] = user_id
            
        # Tạo request
        streaming_request = {
            "message": message,
            "context": context
        }
        
        # Chuẩn bị phản hồi khởi đầu
        initial_response = {
            "agent": "Root Agent",
            "status": "streaming",
            "content": "Đang xử lý yêu cầu của bạn...",
            "is_final": False
        }
        yield f"data: {json.dumps(initial_response)}\n\n"
        
        # Sử dụng process_direct_root_request
        response = await root_agent.process_direct_root_request(streaming_request)
        
        # Đảm bảo response có đúng format
        if not isinstance(response, dict):
            response = {
                "agent": "Root Agent",
                "status": "success", 
                "content": str(response),
                "metadata": {}
            }
        
        # Lấy nội dung phản hồi để chia thành các phần
        content = response.get("content", "")
        if content:
            # Chia nội dung thành các phần để tạo hiệu ứng streaming
            # Chia theo câu
            sentences = [s.strip() for s in content.split(".") if s.strip()]
            
            # Nếu không có câu nào, tạo một câu đơn
            if not sentences:
                sentences = [content]
            
            # Gửi từng câu như một chunk
            for i, sentence in enumerate(sentences):
                # Thêm dấu chấm vào cuối câu nếu không phải câu cuối
                if i < len(sentences) - 1:
                    sentence += "."
                
                # Tạo chunk
                chunk = {
                    "agent": response.get("agent", "Root Agent"),
                    "status": "streaming",
                    "content": sentence,
                    "is_final": (i == len(sentences) - 1)
                }
                
                # Gửi chunk
                yield f"data: {json.dumps(chunk)}\n\n"
                
                # Chờ một chút để mô phỏng streaming
                await asyncio.sleep(0.2)
            
            # Gửi phản hồi cuối cùng
            final_response = {
                "agent": response.get("agent", "Root Agent"),
                "status": "success",
                "content": content,
                "metadata": response.get("metadata", {}),
                "is_final": True
            }
            yield f"data: {json.dumps(final_response)}\n\n"
        else:
            # Nếu không có nội dung, gửi thông báo lỗi
            error_response = {
                "agent": "System",
                "status": "error",
                "content": "Không nhận được nội dung phản hồi",
                "is_final": True
            }
            yield f"data: {json.dumps(error_response)}\n\n"
            
    except Exception as e:
        logger.exception(f"Error in streaming: {e}")
        error_response = {
            "agent": "System",
            "status": "error",
            "content": str(e),
            "is_final": True
        }
        yield f"data: {json.dumps(error_response)}\n\n"


@app.get("/api/chat")
async def get_chat(
    background_tasks: BackgroundTasks,
    session_id: str = Query(..., description="Session ID for the chat"),
    message: Optional[str] = Query(None, description="Optional message for the chat"),
    user_id: Optional[str] = Query(None, description="Optional user ID")
):
    """Get streaming responses from the agent system."""
    # Có thể lưu message và context vào session storage ở đây
    # Trong thực tế, có thể thực hiện kiểm tra quota và xác thực
    
    return StreamingResponse(
        stream_response(session_id, message, user_id),
        media_type="text/event-stream"
    )


@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    type: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
):
    """Upload a file (image, PDF, audio)."""
    try:
        # Validate file type if provided
        if type:
            valid_types = ["image", "pdf", "audio", "text"]
            if type not in valid_types:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "detail": f"Invalid file type. Must be one of: {', '.join(valid_types)}"
                    }
                )
        
        # Parse metadata if provided
        metadata_dict = {}
        if metadata:
            try:
                metadata_dict = json.loads(metadata)
            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status": "error",
                        "detail": "Invalid JSON format for metadata"
                    }
                )
        
        # Generate a unique file ID
        file_id = f"f{uuid.uuid4().hex[:6]}"
        
        # Get the file extension
        _, extension = os.path.splitext(file.filename)
        if not extension:
            extension = ".bin"  # Default extension if none provided
        
        # Create the new filename
        new_filename = f"{file_id}{extension}"
        file_path = os.path.join(uploads_path, new_filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        
        # Generate file URL
        file_url = f"/static/uploads/{new_filename}"
        
        # Create response with file metadata
        return {
            "status": "success",
            "file_id": file_id,
            "file_url": file_url,
            "metadata": {
                "file_type": type or "unknown",
                "file_size": os.path.getsize(file_path),
                "upload_date": datetime.now().isoformat(),
                "original_filename": file.filename,
                **metadata_dict
            }
        }
        
    except Exception as e:
        logger.exception(f"Error uploading file: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "detail": str(e)
            }
        )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "detail": str(exc)},
    )


# For local development
if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting Phong Thuy API server in {env_mode} mode on port {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

# Payment endpoints
@app.get("/api/payment/plans", response_model=List[Plan])
async def list_plans():
    """List all available subscription plans."""
    return list(mock_plans.values())


@app.get("/api/payment/plans/{plan_id}", response_model=Plan)
async def get_plan(plan_id: str):
    """Get details of a specific plan."""
    if plan_id not in mock_plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return mock_plans[plan_id]


@app.post("/api/payment", response_model=Payment)
async def create_payment(
    payment_create: PaymentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new payment."""
    if payment_create.plan_id not in mock_plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    plan = mock_plans[payment_create.plan_id]
    
    if payment_create.amount != plan["price"]:
        raise HTTPException(status_code=400, detail="Invalid payment amount")
    
    payment_id = str(uuid.uuid4())
    payment_data = {
        "id": payment_id,
        "user_id": current_user["id"],
        "plan_id": payment_create.plan_id,
        "payment_method": payment_create.payment_method,
        "amount": payment_create.amount,
        "currency": payment_create.currency,
        "status": "pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "transaction_id": None
    }
    
    mock_payments[payment_id] = payment_data
    
    # In a real implementation, this would trigger payment processing
    # For the demo, we'll just complete the payment immediately
    payment_data["status"] = "completed"
    payment_data["transaction_id"] = f"txn_{uuid.uuid4().hex}"
    payment_data["updated_at"] = datetime.now()
    
    # Create or update subscription
    existing_subscription = None
    for sub in mock_subscriptions.values():
        if sub["user_id"] == current_user["id"] and sub["is_active"]:
            existing_subscription = sub
            break
    
    if existing_subscription:
        # Update existing subscription
        existing_subscription["plan_id"] = plan["id"]
        existing_subscription["status"] = "active"
        existing_subscription["updated_at"] = datetime.now()
        
        # Extend end date
        if plan["interval"] == "month":
            existing_subscription["end_date"] = existing_subscription["end_date"].replace(
                month=existing_subscription["end_date"].month + 1
            )
        elif plan["interval"] == "year":
            existing_subscription["end_date"] = existing_subscription["end_date"].replace(
                year=existing_subscription["end_date"].year + 1
            )
    else:
        # Create new subscription
        subscription_id = str(uuid.uuid4())
        end_date = datetime.now()
        
        if plan["interval"] == "month":
            end_date = end_date.replace(month=end_date.month + 1)
        elif plan["interval"] == "year":
            end_date = end_date.replace(year=end_date.year + 1)
            
        subscription_data = {
            "id": subscription_id,
            "user_id": current_user["id"],
            "plan_id": plan["id"],
            "status": "active",
            "start_date": datetime.now(),
            "end_date": end_date,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_active": True,
            "auto_renew": True
        }
        mock_subscriptions[subscription_id] = subscription_data
    
    # Update user status and quota
    user_data = mock_users[current_user["email"]]
    user_data["isPremium"] = plan["type"] != "free"
    user_data["remainingQuestions"] = plan["quota"]
    user_data["updated_at"] = datetime.now()
    
    return payment_data


@app.get("/api/payment/history", response_model=List[Payment])
async def get_payment_history(current_user: User = Depends(get_current_active_user)):
    """Get payment history for the current user."""
    user_payments = [
        payment for payment in mock_payments.values()
        if payment["user_id"] == current_user["id"]
    ]
    
    return user_payments


@app.get("/api/payment/subscription", response_model=Optional[Subscription])
async def get_active_subscription(current_user: User = Depends(get_current_active_user)):
    """Get the active subscription for the current user."""
    for subscription in mock_subscriptions.values():
        if (subscription["user_id"] == current_user["id"] and 
            subscription["is_active"] and 
            subscription["status"] == "active"):
            return subscription
    
    return None


# Cập nhật route để lấy lịch sử phân tích
@app.get("/api/phone-analysis/history", response_model=List[Dict[str, Any]])
async def get_phone_analysis_history(
    limit: int = Query(10, description="Số lượng kết quả tối đa", ge=1, le=100),
    skip: int = Query(0, description="Số lượng kết quả bỏ qua", ge=0),
    current_user: User = Depends(get_current_active_user)
):
    """Lấy lịch sử phân tích số điện thoại của người dùng."""
    try:
        from tools.batcuclinhso_analysis.phone_analysis_db import get_user_analyses
        
        # Lấy danh sách phân tích từ database
        analyses = await get_user_analyses(user_id=current_user["id"], limit=limit, skip=skip)
        
        return analyses
    except Exception as e:
        logger.exception(f"Lỗi khi lấy lịch sử phân tích: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi lấy lịch sử phân tích: {str(e)}"
        )

# Cập nhật route để lấy chi tiết một phân tích
@app.get("/api/phone-analysis/{phone_number}", response_model=Dict[str, Any])
async def get_phone_analysis_detail(
    phone_number: str,
    current_user: User = Depends(get_current_active_user)
):
    """Lấy chi tiết phân tích của một số điện thoại."""
    try:
        from tools.batcuclinhso_analysis.phone_analysis_db import get_phone_analysis
        
        # Làm sạch số điện thoại, loại bỏ khoảng trắng và ký tự đặc biệt
        phone_number = "".join(char for char in phone_number if char.isdigit())
        
        # Lấy phân tích từ database
        analysis = await get_phone_analysis(user_id=current_user["id"], phone_number=phone_number)
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail=f"Không tìm thấy phân tích cho số điện thoại {phone_number}"
            )
            
        return analysis
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Lỗi khi lấy chi tiết phân tích: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi lấy chi tiết phân tích: {str(e)}"
        )

# Thêm endpoint API cho BatCucLinhSoAgent
@app.post("/api/batcuclinh_so/analyze_phone")
async def analyze_phone(
    request: PhoneAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: Optional[User] = Depends(get_current_user),
    api_key: Optional[str] = Header(None, convert_underscores=False),
    response: Response = None
):
    """Phân tích số điện thoại sử dụng BatCucLinhSoAgent."""
    try:
        # Kiểm tra xác thực - hoặc thông qua current_user hoặc api_key
        user = None
        if current_user:
            user = current_user
        elif api_key:
            try:
                user = await validate_api_key(api_key)
            except HTTPException as e:
                raise e
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Bạn cần đăng nhập hoặc cung cấp API key"
            )
    
        # Kiểm tra quota nếu cần
        if user and 'remainingQuestions' in user and user['remainingQuestions'] <= 0 and not user.get('isPremium', False):
            raise HTTPException(
                status_code=402,
                detail="Bạn đã hết số lần phân tích. Vui lòng nâng cấp tài khoản."
            )
        
        # Chuẩn hóa số điện thoại, loại bỏ khoảng trắng và ký tự đặc biệt
        phone_number = "".join(char for char in request.phone_number if char.isdigit())
        
        # Kiểm tra định dạng số điện thoại
        if not phone_number or len(phone_number) < 9 or len(phone_number) > 12:
            raise HTTPException(
                status_code=400,
                detail="Định dạng số điện thoại không hợp lệ. Số điện thoại phải có từ 9-12 chữ số."
            )
        
        try:
            from tools.batcuclinhso_analysis.phone_analysis_db import get_cached_phone_analysis
            
            # Kiểm tra cache trước khi phân tích
            cached_result = await get_cached_phone_analysis(user["id"], phone_number)
            if cached_result:
                if response:
                    response.headers["X-Cache"] = "HIT"
                logger.info(f"Cache hit for phone analysis: {phone_number}")
                return cached_result["result"]
            
            if response:
                response.headers["X-Cache"] = "MISS"
            logger.info(f"Cache miss for phone analysis: {phone_number}")
            
        except Exception as e:
            logger.warning(f"Lỗi khi kiểm tra cache: {e}")
            # Tiếp tục xử lý nếu có lỗi với cache
    
        try:
            # Gọi trực tiếp đến BatCucLinhSoAgent
            response_data = await root_agent.route_request(
                target_agent_type=AgentType.BAT_CUC_LINH_SO,
                request_data=request
            )
            
            # Lưu kết quả vào database trong background
            from tools.batcuclinhso_analysis.phone_analysis_db import save_phone_analysis
            
            background_tasks.add_task(
                save_phone_analysis, 
                user_id=user["id"], 
                phone_number=phone_number, 
                analysis_result=response_data,
                gemini_response=response_data.get("geminiResponse", None)
            )
            
            # Giảm quota nếu cần
            if user and 'remainingQuestions' in user and not user.get('isPremium', False):
                user['remainingQuestions'] -= 1
                
                # Cập nhật quota trong database
                background_tasks.add_task(
                    update_user_quota,
                    user_id=user["id"],
                    remaining_questions=user['remainingQuestions']
                )
            
            return response_data
            
        except Exception as e:
            logger.exception(f"Lỗi khi phân tích số điện thoại: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Lỗi khi phân tích số điện thoại: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Lỗi không xác định khi phân tích số điện thoại: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi không xác định: {str(e)}"
        ) 

# Hàm cập nhật quota người dùng
async def update_user_quota(user_id: str, remaining_questions: int = None):
    """Cập nhật số lượng câu hỏi còn lại của người dùng."""
    try:
        if not user_id:
            logger.warning("Không thể cập nhật quota: Thiếu user_id")
            return

        # Import db từ shared_libraries 
        from shared_libraries.database.mongodb import db
            
        # Nếu không chỉ định remaining_questions, giảm đi 1
        update_data = {}
        if remaining_questions is not None:
            update_data["remainingQuestions"] = remaining_questions
        else:
            # Sử dụng $inc để giảm giá trị an toàn
            update_data = {"$inc": {"remainingQuestions": -1}}
        
        # Cập nhật trong database
        result = await db.user.update_one(
            {"_id": user_id},
            {"$set": update_data} if remaining_questions is not None else update_data
        )
        
        if result.modified_count == 0:
            logger.warning(f"Không thể cập nhật quota cho user {user_id}")
        else:
            logger.debug(f"Đã cập nhật quota cho user {user_id}: remaining={remaining_questions}")
            
    except Exception as e:
        logger.error(f"Lỗi khi cập nhật quota người dùng: {e}") 
