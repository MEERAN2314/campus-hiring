from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from app.models.submission import SubmissionCreate, Submission
from app.utils.auth import get_current_candidate
from app.database import get_database
from app.utils.helpers import generate_id
from app.celery_worker import evaluate_submission_task
from datetime import datetime

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post("", response_model=Submission, status_code=status.HTTP_201_CREATED)
async def submit_assessment(
    submission_data: SubmissionCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_candidate)
):
    """Submit assessment answers"""
    db = get_database()
    
    # Get user
    user = await db.users.find_one({"email": current_user.email})
    
    # Get application
    application = await db.applications.find_one({
        "_id": submission_data.application_id,
        "candidate_id": user["_id"]
    })
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check if already submitted
    existing = await db.submissions.find_one({
        "application_id": submission_data.application_id,
        "is_practice": False
    })
    if existing:
        raise HTTPException(status_code=400, detail="Assessment already submitted")
    
    # Get assessment
    assessment = await db.assessments.find_one({"_id": submission_data.assessment_id})
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Calculate total time
    if application.get("assessment_started_at"):
        total_time = int((datetime.utcnow() - application["assessment_started_at"]).total_seconds())
    else:
        total_time = sum(answer.time_spent_seconds for answer in submission_data.answers)
    
    # Create submission
    submission_dict = {
        "_id": generate_id(),
        "application_id": submission_data.application_id,
        "assessment_id": submission_data.assessment_id,
        "candidate_id": user["_id"],
        "answers": [answer.model_dump() for answer in submission_data.answers],
        "started_at": application.get("assessment_started_at", datetime.utcnow()),
        "submitted_at": datetime.utcnow(),
        "total_time_seconds": total_time,
        "is_practice": False
    }
    
    await db.submissions.insert_one(submission_dict)
    
    # Update application status
    await db.applications.update_one(
        {"_id": submission_data.application_id},
        {
            "$set": {
                "status": "assessment_completed",
                "assessment_completed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Trigger async evaluation
    evaluate_submission_task.delay(submission_dict["_id"])
    
    return Submission(**submission_dict)


@router.post("/start/{application_id}")
async def start_assessment(application_id: str, current_user=Depends(get_current_candidate)):
    """Mark assessment as started"""
    db = get_database()
    
    user = await db.users.find_one({"email": current_user.email})
    
    application = await db.applications.find_one({
        "_id": application_id,
        "candidate_id": user["_id"]
    })
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update application
    await db.applications.update_one(
        {"_id": application_id},
        {
            "$set": {
                "status": "assessment_pending",
                "assessment_started_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    return {"message": "Assessment started", "started_at": datetime.utcnow()}


@router.get("/{submission_id}", response_model=Submission)
async def get_submission(submission_id: str, current_user=Depends(get_current_candidate)):
    """Get submission details"""
    db = get_database()
    
    user = await db.users.find_one({"email": current_user.email})
    
    submission = await db.submissions.find_one({
        "_id": submission_id,
        "candidate_id": user["_id"]
    })
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return Submission(**submission)
