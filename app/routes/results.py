from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.result import Result
from app.utils.auth import get_current_user, get_current_recruiter
from app.database import get_database

router = APIRouter(prefix="/results", tags=["Results"])


@router.get("/application/{application_id}", response_model=Result)
async def get_result_by_application(
    application_id: str,
    current_user=Depends(get_current_user)
):
    """Get result for an application"""
    db = get_database()
    
    # Get application
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
    
    # Get result
    result = await db.results.find_one({"application_id": application_id})
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Result not yet available. Assessment is being evaluated."
        )
    
    return Result(**result)


@router.get("/job/{job_id}/rankings")
async def get_job_rankings(
    job_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_recruiter)
):
    """Get ranked results for a job with candidate names"""
    db = get_database()
    
    # Verify job belongs to recruiter
    user = await db.users.find_one({"email": current_user.email})
    job = await db.jobs.find_one({"_id": job_id, "company_id": user["_id"]})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get all applications for this job
    applications = await db.applications.find({"job_id": job_id}).to_list(None)
    application_ids = [app["_id"] for app in applications]
    
    # Get results and sort by percentage
    results = await db.results.find(
        {"application_id": {"$in": application_ids}}
    ).sort("percentage", -1).skip(skip).limit(limit).to_list(limit)
    
    # Add rank and fetch candidate names
    for idx, result in enumerate(results, start=skip + 1):
        result["rank"] = idx
        result["total_candidates"] = len(application_ids)
        
        # Fetch candidate name
        candidate = await db.users.find_one({"_id": result["candidate_id"]})
        if candidate:
            result["candidate_name"] = candidate.get("name", "Unknown")
            result["candidate_email"] = candidate.get("email", "")
        else:
            result["candidate_name"] = "Unknown"
            result["candidate_email"] = ""
    
    # Update ranks in database
    for result in results:
        await db.results.update_one(
            {"_id": result["_id"]},
            {"$set": {"rank": result["rank"], "total_candidates": result["total_candidates"]}}
        )
    
    # Convert to dict for JSON response (bypass Pydantic model)
    return results


@router.get("/{result_id}", response_model=Result)
async def get_result(result_id: str, current_user=Depends(get_current_user)):
    """Get specific result"""
    db = get_database()
    
    result = await db.results.find_one({"_id": result_id})
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Verify access
    user = await db.users.find_one({"email": current_user.email})
    if current_user.user_type == "candidate":
        if result["candidate_id"] != user["_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
    else:
        # Verify through application and job
        application = await db.applications.find_one({"_id": result["application_id"]})
        if application:
            job = await db.jobs.find_one({"_id": application["job_id"], "company_id": user["_id"]})
            if not job:
                raise HTTPException(status_code=403, detail="Access denied")
    
    return Result(**result)
