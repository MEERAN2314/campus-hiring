from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class QuestionType(str, Enum):
    MCQ = "mcq"
    CODING = "coding"
    DESCRIPTIVE = "descriptive"
    SITUATIONAL = "situational"


class MCQOption(BaseModel):
    option_id: str
    text: str


class TestCase(BaseModel):
    input: str
    expected_output: str
    is_hidden: bool = False


class Question(BaseModel):
    question_id: str
    type: QuestionType
    question_text: str
    difficulty: str  # "easy", "medium", "hard"
    points: int
    
    # For MCQ
    options: Optional[List[MCQOption]] = None
    correct_option_id: Optional[str] = None
    
    # For Coding
    test_cases: Optional[List[TestCase]] = None
    starter_code: Optional[str] = None
    language: Optional[str] = None  # "python", "javascript", etc.
    
    # AI metadata
    skill_tags: List[str] = []
    ai_rationale: Optional[str] = None  # Why this question was chosen


class AssessmentConfig(BaseModel):
    duration_minutes: int = 60
    total_points: int = 100
    passing_score: int = 60
    randomize_questions: bool = False
    show_results_immediately: bool = False
    allow_practice_mode: bool = True


class AssessmentBase(BaseModel):
    job_id: str
    title: str
    description: str
    questions: List[Question]
    config: AssessmentConfig


class AssessmentCreate(BaseModel):
    job_id: str
    auto_generate: bool = True
    custom_instructions: Optional[str] = None


class Assessment(AssessmentBase):
    id: str = Field(alias="_id")
    created_by: str
    is_ai_generated: bool = True
    generation_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
        by_alias = False  # Use 'id' in JSON output instead of '_id'
