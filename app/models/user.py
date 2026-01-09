from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserType(str, Enum):
    ADMIN = "admin"
    RECRUITER = "recruiter"
    CANDIDATE = "candidate"
    CAMPUS_ADMIN = "campus_admin"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    user_type: UserType
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    company_name: Optional[str] = None  # For recruiters
    college_name: Optional[str] = None  # For candidates/campus admins
    skills: Optional[List[str]] = []  # For candidates
    resume_url: Optional[str] = None  # For candidates


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str
    company_name: Optional[str] = None
    college_name: Optional[str] = None
    skills: List[str] = []
    resume_url: Optional[str] = None
    profile_complete: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserResponse(UserBase):
    id: str
    company_name: Optional[str] = None
    college_name: Optional[str] = None
    skills: List[str] = []
    profile_complete: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None
    user_type: Optional[str] = None
