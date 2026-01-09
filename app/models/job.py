from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class JobType(str, Enum):
    TECHNICAL = "technical"
    NON_TECHNICAL = "non_technical"


class JobStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"


class JobBase(BaseModel):
    title: str
    description: str
    job_type: JobType
    required_skills: List[str]
    experience_level: str  # "fresher", "0-2 years", etc.
    location: str
    salary_range: Optional[str] = None
    vacancies: int = 1
    target_colleges: List[str] = []


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    experience_level: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    vacancies: Optional[int] = None
    target_colleges: Optional[List[str]] = None
    status: Optional[JobStatus] = None


class Job(JobBase):
    id: str = Field(alias="_id")
    company_id: str
    company_name: str
    status: JobStatus = JobStatus.DRAFT
    assessment_id: Optional[str] = None
    applications_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class JobResponse(JobBase):
    id: str
    company_name: str
    status: JobStatus
    assessment_id: Optional[str] = None
    applications_count: int
    created_at: datetime

    class Config:
        from_attributes = True
