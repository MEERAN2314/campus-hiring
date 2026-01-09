from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from app.models.assessment import AssessmentCreate, Assessment
from app.utils.auth import get_current_recruiter, get_current_user
from app.database import get_database
from app.utils.helpers import generate_id
from app.ai.gemini_service import gemini_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.post("", response_model=Assessment, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment_data: AssessmentCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_recruiter)
):
    """Create assessment for a job (AI-generated or custom)"""
    db = get_database()
    
    # Get user
    user = await db.users.find_one({"email": current_user.email})
    
    # Get job
    job = await db.jobs.find_one({"_id": assessment_data.job_id, "company_id": user["_id"]})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if assessment already exists
    existing = await db.assessments.find_one({"job_id": assessment_data.job_id})
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Assessment already exists for this job"
        )
    
    if assessment_data.auto_generate:
        # Generate assessment with AI
        logger.info(f"Generating AI assessment for job {assessment_data.job_id}")
        
        try:
            ai_result = await gemini_service.generate_assessment({
                "title": job["title"],
                "job_type": job["job_type"],
                "required_skills": job["required_skills"],
                "experience_level": job["experience_level"],
                "description": job["description"]
            })
            
            # Create assessment document
            assessment_dict = {
                "_id": generate_id(),
                "job_id": assessment_data.job_id,
                "title": f"Assessment for {job['title']}",
                "description": f"AI-generated assessment covering {', '.join(job['required_skills'])}",
                "questions": ai_result["questions"],
                "config": {
                    "duration_minutes": ai_result.get("estimated_duration", 60),
                    "total_points": ai_result.get("total_points", 100),
                    "passing_score": 60,
                    "randomize_questions": False,
                    "show_results_immediately": False,
                    "allow_practice_mode": True
                },
                "created_by": user["_id"],
                "is_ai_generated": True,
                "generation_metadata": {
                    "model": "gemini-2.0-flash-exp",
                    "generated_at": datetime.utcnow().isoformat(),
                    "custom_instructions": assessment_data.custom_instructions
                },
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
        except Exception as e:
            logger.error(f"Error generating assessment: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate assessment: {str(e)}"
            )
    else:
        # Manual assessment creation (placeholder)
        raise HTTPException(
            status_code=400,
            detail="Manual assessment creation not yet implemented"
        )
    
    # Insert assessment
    await db.assessments.insert_one(assessment_dict)
    
    # Update job with assessment_id
    await db.jobs.update_one(
        {"_id": assessment_data.job_id},
        {"$set": {"assessment_id": assessment_dict["_id"], "updated_at": datetime.utcnow()}}
    )
    
    return Assessment(**assessment_dict)


@router.get("/{assessment_id}", response_model=Assessment)
async def get_assessment(assessment_id: str, current_user=Depends(get_current_user)):
    """Get assessment details"""
    db = get_database()
    
    assessment = await db.assessments.find_one({"_id": assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # If candidate, hide correct answers
    if current_user.user_type == "candidate":
        for question in assessment["questions"]:
            if "correct_option_id" in question:
                del question["correct_option_id"]
    
    return Assessment(**assessment)


@router.get("/job/{job_id}", response_model=Assessment)
async def get_assessment_by_job(job_id: str, current_user=Depends(get_current_user)):
    """Get assessment for a specific job"""
    db = get_database()
    
    assessment = await db.assessments.find_one({"job_id": job_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found for this job")
    
    # If candidate, hide correct answers
    if current_user.user_type == "candidate":
        for question in assessment["questions"]:
            if "correct_option_id" in question:
                del question["correct_option_id"]
    
    return Assessment(**assessment)
