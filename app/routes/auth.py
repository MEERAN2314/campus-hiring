from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserCreate, UserLogin, User, UserResponse, Token
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.database import get_database
from app.utils.helpers import generate_id
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """Register a new user"""
    db = get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    user_dict = user_data.model_dump(exclude={"password"})
    user_dict.update({
        "_id": generate_id(),
        "hashed_password": get_password_hash(user_data.password),
        "profile_complete": bool(user_data.company_name or user_data.college_name),
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    # Insert user
    await db.users.insert_one(user_dict)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_data.email, "user_type": user_data.user_type.value}
    )
    
    # Prepare response
    user_response = UserResponse(
        id=user_dict["_id"],
        email=user_dict["email"],
        full_name=user_dict["full_name"],
        user_type=user_dict["user_type"],
        phone=user_dict.get("phone"),
        company_name=user_dict.get("company_name"),
        college_name=user_dict.get("college_name"),
        skills=user_dict.get("skills", []),
        profile_complete=user_dict["profile_complete"],
        created_at=user_dict["created_at"]
    )
    
    return Token(access_token=access_token, user=user_response)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """Login user"""
    db = get_database()
    
    # Find user
    user = await db.users.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user["email"], "user_type": user["user_type"]}
    )
    
    # Prepare response
    user_response = UserResponse(
        id=user["_id"],
        email=user["email"],
        full_name=user["full_name"],
        user_type=user["user_type"],
        phone=user.get("phone"),
        company_name=user.get("company_name"),
        college_name=user.get("college_name"),
        skills=user.get("skills", []),
        profile_complete=user.get("profile_complete", False),
        created_at=user["created_at"]
    )
    
    return Token(access_token=access_token, user=user_response)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(db=Depends(get_database)):
    """Get current user information"""
    # This would need the current user from token
    # Simplified for now
    pass
