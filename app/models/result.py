from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SkillScore(BaseModel):
    skill_name: str
    score: float  # 0-100
    level: str  # "beginner", "intermediate", "advanced"
    feedback: str


class QuestionEvaluation(BaseModel):
    question_id: str
    question_type: str
    points_earned: float
    max_points: int
    is_correct: bool
    
    # Detailed feedback
    correctness_score: Optional[float] = None  # For coding
    efficiency_score: Optional[float] = None  # For coding
    readability_score: Optional[float] = None  # For coding
    
    ai_feedback: str
    strengths: List[str] = []
    improvements: List[str] = []


class FeedbackReport(BaseModel):
    overall_score: float  # 0-100
    percentile: Optional[float] = None
    
    # Skill breakdown
    skill_scores: List[SkillScore]
    
    # Strengths and weaknesses
    top_strengths: List[str]
    improvement_areas: List[str]
    
    # Personalized recommendations
    learning_resources: List[Dict[str, str]]  # {"title": "", "url": "", "type": ""}
    improvement_plan: str
    estimated_improvement_time: str
    
    # Encouragement
    positive_message: str
    next_steps: List[str]


class AIReasoning(BaseModel):
    overall_assessment: str
    ranking_factors: List[Dict[str, Any]]
    confidence_score: float  # 0-1
    bias_check: Dict[str, Any]
    prediction: str  # Success prediction


class ResultBase(BaseModel):
    submission_id: str
    application_id: str
    candidate_id: str
    assessment_id: str


class ResultCreate(ResultBase):
    pass


class Result(ResultBase):
    id: str = Field(alias="_id")
    
    # Scores
    total_score: float
    max_score: int
    percentage: float
    
    # Question-wise evaluation
    question_evaluations: List[QuestionEvaluation]
    
    # AI Analysis
    ai_reasoning: AIReasoning
    feedback_report: FeedbackReport
    
    # Ranking
    rank: Optional[int] = None
    total_candidates: Optional[int] = None
    
    # Status
    is_shortlisted: bool = False
    recruiter_notes: Optional[str] = None
    
    # Timestamps
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
