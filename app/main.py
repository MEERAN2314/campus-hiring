from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, jobs, assessments, applications, submissions, results
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered campus recruitment platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Database events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    logger.info("Starting up application...")
    await connect_to_mongo()
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    logger.info("Shutting down application...")
    await close_mongo_connection()
    logger.info("Application shut down successfully")


# Include API routers
app.include_router(auth.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(assessments.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(submissions.router, prefix="/api")
app.include_router(results.router, prefix="/api")


# Frontend routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Register page"""
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page - redirects based on user type"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/recruiter/dashboard", response_class=HTMLResponse)
async def recruiter_dashboard(request: Request):
    """Recruiter dashboard page"""
    return templates.TemplateResponse("recruiter_dashboard.html", {"request": request})


@app.get("/jobs", response_class=HTMLResponse)
async def jobs_page(request: Request):
    """Jobs listing page - redirects based on user type"""
    return templates.TemplateResponse("jobs_redirect.html", {"request": request})


@app.get("/candidate/jobs", response_class=HTMLResponse)
async def candidate_jobs_page(request: Request):
    """Candidate jobs listing page"""
    return templates.TemplateResponse("jobs.html", {"request": request})


@app.get("/jobs/{job_id}", response_class=HTMLResponse)
async def job_detail_page(request: Request, job_id: str):
    """Job detail page"""
    return templates.TemplateResponse("job_detail.html", {"request": request, "job_id": job_id})


@app.get("/assessment/{application_id}", response_class=HTMLResponse)
async def assessment_page(request: Request, application_id: str):
    """Assessment taking page"""
    return templates.TemplateResponse("assessment.html", {"request": request, "application_id": application_id})


@app.get("/results/{application_id}", response_class=HTMLResponse)
async def results_page(request: Request, application_id: str):
    """Results page"""
    return templates.TemplateResponse("results.html", {"request": request, "application_id": application_id})


@app.get("/recruiter/jobs", response_class=HTMLResponse)
async def recruiter_jobs(request: Request):
    """Recruiter jobs management"""
    return templates.TemplateResponse("recruiter_jobs.html", {"request": request})


@app.get("/recruiter/candidates/{job_id}", response_class=HTMLResponse)
async def recruiter_candidates(request: Request, job_id: str):
    """Recruiter candidates view"""
    return templates.TemplateResponse("recruiter_candidates.html", {"request": request, "job_id": job_id})


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "app": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
