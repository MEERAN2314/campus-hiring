from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from typing import List
from app.models.application import ApplicationCreate, Application, ApplicationStatus
from app.utils.auth import get_current_candidate, get_current_recruiter, get_current_user
from app.database import get_database
from app.utils.helpers import generate_id
from app.utils.email import email_service
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("", response_model=Application, status_code=status.HTTP_201_CREATED)
async def apply_to_job(
    application_data: ApplicationCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_candidate)
):
    """Apply to a job"""
    db = get_database()
    
    # Get candidate info
    user = await db.users.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get job
    job = await db.jobs.find_one({"_id": application_data.job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job["status"] != "active":
        raise HTTPException(status_code=400, detail="Job is not active")
    
    # Check if already applied
    existing = await db.applications.find_one({
        "job_id": application_data.job_id,
        "candidate_id": user["_id"]
    })
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    
    # Create application
    application_dict = {
        "_id": generate_id(),
        "job_id": application_data.job_id,
        "candidate_id": user["_id"],
        "candidate_name": user["full_name"],
        "candidate_email": user["email"],
        "candidate_college": user.get("college_name"),
        "status": ApplicationStatus.APPLIED.value,
        "resume_url": user.get("resume_url"),
        "applied_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    await db.applications.insert_one(application_dict)
    
    # Update job applications count
    await db.jobs.update_one(
        {"_id": application_data.job_id},
        {"$inc": {"applications_count": 1}}
    )
    
    # Send email notifications in background
    try:
        # Email to candidate
        background_tasks.add_task(
            email_service.send_application_confirmation,
            user["email"],
            user["full_name"],
            job["title"],
            job["company_name"]
        )
        
        # Email to recruiter
        recruiter = await db.users.find_one({"_id": job["company_id"]})
        if recruiter:
            background_tasks.add_task(
                email_service.send_new_application_notification,
                recruiter["email"],
                recruiter["full_name"],
                user["full_name"],
                job["title"],
                user.get("skills", [])
            )
        
        logger.info(f"Email notifications queued for application {application_dict['_id']}")
    except Exception as e:
        logger.error(f"Error queuing email notifications: {e}")
        # Don't fail the application if email fails
    
    return Application(**application_dict)


@router.get("", response_model=List[Application])
async def list_applications(
    job_id: str = None,
    status: str = None,
    skip: int = 0,
    limit: int = 50,
    current_user=Depends(get_current_user)
):
    """List applications (candidate sees their own, recruiter sees all for their jobs)"""
    db = get_database()
    
    query = {}
    
    if current_user.user_type == "candidate":
        # Candidate sees their own applications
        user = await db.users.find_one({"email": current_user.email})
        query["candidate_id"] = user["_id"]
    else:
        # Recruiter sees applications for their jobs
        if job_id:
            # Verify job belongs to recruiter
            user = await db.users.find_one({"email": current_user.email})
            job = await db.jobs.find_one({"_id": job_id, "company_id": user["_id"]})
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")
            query["job_id"] = job_id
        else:
            # Get all jobs by this recruiter
            user = await db.users.find_one({"email": current_user.email})
            jobs = await db.jobs.find({"company_id": user["_id"]}).to_list(None)
            job_ids = [job["_id"] for job in jobs]
            query["job_id"] = {"$in": job_ids}
    
    if status:
        query["status"] = status
    
    applications = await db.applications.find(query).sort("applied_at", -1).skip(skip).limit(limit).to_list(limit)
    
    return [Application(**app) for app in applications]


@router.get("/{application_id}", response_model=Application)
async def get_application(application_id: str, current_user=Depends(get_current_user)):
    """Get application details"""
    db = get_database()
    
    application = await db.applications.find_one({"_id": application_id})
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Verify access
    user = await db.users.find_one({"email": current_user.email})
    if current_user.user_type == "candidate":
        if application["candidate_id"] != user["_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        # Verify job belongs to recruiter
        job = await db.jobs.find_one({"_id": application["job_id"], "company_id": user["_id"]})
        if not job:
            raise HTTPException(status_code=403, detail="Access denied")
    
    return Application(**application)


@router.post("/{application_id}/shortlist", response_model=Application)
async def shortlist_application(
    application_id: str,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_recruiter)
):
    """Shortlist an application"""
    db = get_database()
    
    application = await db.applications.find_one({"_id": application_id})
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Verify job belongs to recruiter
    user = await db.users.find_one({"email": current_user.email})
    job = await db.jobs.find_one({"_id": application["job_id"], "company_id": user["_id"]})
    if not job:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Update application status
    await db.applications.update_one(
        {"_id": application_id},
        {"$set": {"status": ApplicationStatus.SHORTLISTED.value, "updated_at": datetime.now(timezone.utc)}}
    )
    
    # Update result
    await db.results.update_one(
        {"application_id": application_id},
        {"$set": {"is_shortlisted": True}}
    )
    
    # Send shortlist notification email
    try:
        background_tasks.add_task(
            email_service.send_shortlist_notification,
            application["candidate_email"],
            application["candidate_name"],
            job["title"],
            job["company_name"]
        )
        logger.info(f"Shortlist notification queued for {application['candidate_email']}")
    except Exception as e:
        logger.error(f"Error queuing shortlist email: {e}")
    
    updated_application = await db.applications.find_one({"_id": application_id})
    return Application(**updated_application)


@router.post("/{application_id}/reject", response_model=Application)
async def reject_application(
    application_id: str,
    background_tasks: BackgroundTasks,
    current_user=Depends(get_current_recruiter)
):
    """Reject an application"""
    db = get_database()
    
    application = await db.applications.find_one({"_id": application_id})
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Verify job belongs to recruiter
    user = await db.users.find_one({"email": current_user.email})
    job = await db.jobs.find_one({"_id": application["job_id"], "company_id": user["_id"]})
    if not job:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Update application status
    await db.applications.update_one(
        {"_id": application_id},
        {"$set": {"status": ApplicationStatus.REJECTED.value, "updated_at": datetime.now(timezone.utc)}}
    )
    
    # Note: You can add rejection email here if needed
    # background_tasks.add_task(email_service.send_rejection_email, ...)
    
    updated_application = await db.applications.find_one({"_id": application_id})
    return Application(**updated_application)
