from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from app.models.job import JobCreate, JobUpdate, Job, JobResponse, JobStatus
from app.utils.auth import get_current_recruiter, get_current_user
from app.database import get_database
from app.utils.helpers import generate_id
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/jobs", tags=["Jobs"])
security = HTTPBearer(auto_error=False)  # Make auth optional


async def get_optional_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Get current user if authenticated, None otherwise"""
    if credentials:
        from app.utils.auth import decode_access_token
        try:
            return decode_access_token(credentials.credentials)
        except:
            return None
    return None


@router.post("", response_model=Job, status_code=status.HTTP_201_CREATED)
async def create_job(job_data: JobCreate, current_user=Depends(get_current_recruiter)):
    """Create a new job posting"""
    db = get_database()
    
    # Get recruiter info
    user = await db.users.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create job document
    job_dict = job_data.model_dump()
    job_dict.update({
        "_id": generate_id(),
        "company_id": user["_id"],
        "company_name": user.get("company_name", "Company"),
        "status": JobStatus.DRAFT,
        "assessment_id": None,
        "applications_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    await db.jobs.insert_one(job_dict)
    
    return Job(**job_dict)


@router.get("", response_model=List[Job])
async def list_jobs(
    status: str = None,
    job_type: str = None,
    skip: int = 0,
    limit: int = 20,
    current_user=Depends(get_optional_current_user)
):
    """List all jobs (filtered for candidates, all for recruiters)"""
    db = get_database()
    
    query = {}
    
    # If user is authenticated
    if current_user:
        # If candidate, only show active jobs
        if current_user.user_type == "candidate":
            query["status"] = JobStatus.ACTIVE.value
        else:
            # Recruiter sees their own jobs
            user = await db.users.find_one({"email": current_user.email})
            if user:
                query["company_id"] = user["_id"]
    else:
        # Not authenticated - show only active jobs
        query["status"] = JobStatus.ACTIVE.value
    
    if status:
        query["status"] = status
    if job_type:
        query["job_type"] = job_type
    
    jobs = await db.jobs.find(query).sort("created_at", -1).skip(skip).limit(limit).to_list(limit)
    
    return [Job(**job) for job in jobs]


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str, current_user=Depends(get_optional_current_user)):
    """Get job details"""
    db = get_database()
    
    job = await db.jobs.find_one({"_id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # If not authenticated or candidate, only show active jobs
    if not current_user or current_user.user_type == "candidate":
        if job.get("status") != JobStatus.ACTIVE.value:
            raise HTTPException(status_code=404, detail="Job not found")
    
    return Job(**job)


@router.put("/{job_id}", response_model=Job)
async def update_job(
    job_id: str,
    job_update: JobUpdate,
    current_user=Depends(get_current_recruiter)
):
    """Update job details"""
    db = get_database()
    
    # Get user
    user = await db.users.find_one({"email": current_user.email})
    
    # Check if job exists and belongs to user
    job = await db.jobs.find_one({"_id": job_id, "company_id": user["_id"]})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update job
    update_data = {k: v for k, v in job_update.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.jobs.update_one({"_id": job_id}, {"$set": update_data})
    
    updated_job = await db.jobs.find_one({"_id": job_id})
    return Job(**updated_job)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: str, current_user=Depends(get_current_recruiter)):
    """Delete a job"""
    db = get_database()
    
    user = await db.users.find_one({"email": current_user.email})
    
    job = await db.jobs.find_one({"_id": job_id, "company_id": user["_id"]})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    await db.jobs.delete_one({"_id": job_id})
    
    return None


@router.post("/{job_id}/publish", response_model=Job)
async def publish_job(job_id: str, current_user=Depends(get_current_recruiter)):
    """Publish a job (make it active)"""
    db = get_database()
    
    user = await db.users.find_one({"email": current_user.email})
    
    job = await db.jobs.find_one({"_id": job_id, "company_id": user["_id"]})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if assessment exists
    if not job.get("assessment_id"):
        raise HTTPException(
            status_code=400,
            detail="Cannot publish job without assessment. Create assessment first."
        )
    
    await db.jobs.update_one(
        {"_id": job_id},
        {"$set": {"status": JobStatus.ACTIVE.value, "updated_at": datetime.utcnow()}}
    )
    
    updated_job = await db.jobs.find_one({"_id": job_id})
    return Job(**updated_job)
