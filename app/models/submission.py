from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class Answer(BaseModel):
    question_id: str
    question_type: str
    
    # For MCQ
    selected_option_id: Optional[str] = None
    
    # For Coding
    code: Optional[str] = None
    language: Optional[str] = None
    
    # For Descriptive/Situational
    text_answer: Optional[str] = None
    
    # Metadata
    time_spent_seconds: int = 0
    attempt_count: int = 1


class SubmissionBase(BaseModel):
    application_id: str
    assessment_id: str
    candidate_id: str
    answers: List[Answer]


class SubmissionCreate(SubmissionBase):
    pass


class Submission(SubmissionBase):
    id: str = Field(alias="_id")
    started_at: datetime
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    total_time_seconds: int
    is_practice: bool = False

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
