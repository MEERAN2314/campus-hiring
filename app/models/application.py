from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    ASSESSMENT_PENDING = "assessment_pending"
    ASSESSMENT_COMPLETED = "assessment_completed"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"


class ApplicationBase(BaseModel):
    job_id: str
    candidate_id: str


class ApplicationCreate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: str = Field(alias="_id")
    candidate_name: str
    candidate_email: str
    candidate_college: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.APPLIED
    resume_url: Optional[str] = None
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    assessment_started_at: Optional[datetime] = None
    assessment_completed_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
