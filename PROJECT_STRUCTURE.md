# HireWave - Project Structure

## Overview
AI-powered recruitment platform with intelligent assessments, real-time evaluation, and personalized candidate feedback.

## Directory Structure

```
hirewave/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Configuration management
│   ├── database.py               # MongoDB connection & setup
│   ├── celery_worker.py          # Celery tasks for async processing
│   │
│   ├── models/                   # Pydantic data models
│   │   ├── __init__.py
│   │   ├── user.py               # User, authentication models
│   │   ├── job.py                # Job posting models
│   │   ├── assessment.py         # Assessment & question models
│   │   ├── application.py        # Application models
│   │   ├── submission.py         # Assessment submission models
│   │   └── result.py             # Evaluation result models
│   │
│   ├── routes/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication (login, register)
│   │   ├── jobs.py               # Job CRUD operations
│   │   ├── assessments.py        # Assessment creation & retrieval
│   │   ├── applications.py       # Job applications
│   │   ├── submissions.py        # Assessment submissions
│   │   └── results.py            # Results & rankings
│   │
│   ├── ai/                       # AI/ML services
│   │   ├── __init__.py
│   │   ├── gemini_service.py     # AI assessment generation
│   │   └── evaluation_service.py # AI evaluation & feedback
│   │
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       ├── auth.py               # JWT, password hashing
│       └── helpers.py            # Helper functions
│
├── templates/                    # Jinja2 HTML templates
│   ├── base.html                 # Base template
│   ├── index.html                # Home page
│   ├── login.html                # Login page
│   ├── register.html             # Registration page
│   ├── dashboard.html            # Candidate dashboard
│   ├── jobs.html                 # Job listings
│   ├── job_detail.html           # Job details
│   ├── assessment.html           # Assessment taking page
│   ├── results.html              # Results & feedback page
│   ├── recruiter_jobs.html       # Recruiter job management
│   └── recruiter_candidates.html # Candidate rankings
│
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css             # Main stylesheet (blue/white theme)
│   └── js/
│       └── main.js               # Main JavaScript
│
├── uploads/                      # File uploads (resumes, etc.)
│   └── .gitkeep
│
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── Dockerfile                    # Docker container definition
├── docker-compose.yml            # Docker Compose configuration
├── requirements.txt              # Python dependencies
├── Makefile                      # Build automation
├── setup.py                      # Setup script
├── run.sh                        # Run application script
├── run_celery.sh                 # Run Celery worker script
├── README.md                     # Project documentation
├── DEPLOYMENT.md                 # Deployment guide
└── PROJECT_STRUCTURE.md          # This file

```

## Key Components

### Backend (FastAPI)

**app/main.py**
- FastAPI application initialization
- Route registration
- Middleware configuration
- Frontend route handlers

**app/config.py**
- Environment variable management
- Application settings
- Configuration validation

**app/database.py**
- MongoDB connection
- Database initialization
- Index creation

**app/celery_worker.py**
- Async task processing
- Assessment evaluation
- AI integration for background jobs

### AI Services

**app/ai/gemini_service.py**
- LangChain + Gemini integration
- Intelligent assessment generation
- Role-specific question creation

**app/ai/evaluation_service.py**
- Code quality analysis
- Behavioral assessment
- Personalized feedback generation
- AI reasoning & ranking

### Data Models

**User Types:**
- Candidate (students)
- Recruiter (companies)
- Campus Admin
- System Admin

**Core Entities:**
- Jobs (postings)
- Assessments (questions)
- Applications (candidate applications)
- Submissions (assessment answers)
- Results (evaluation & feedback)

### Frontend

**Templates:**
- Jinja2 server-side rendering
- Responsive design
- Blue & white professional theme

**JavaScript:**
- Vanilla JS (no frameworks)
- API integration
- Real-time updates
- Form handling

**CSS:**
- Custom CSS (no frameworks)
- Fluid animations
- Mobile-first responsive design
- Professional modern layout

## Data Flow

### Recruiter Flow
1. Register/Login → Create Job → Generate AI Assessment → Publish Job
2. View Applications → Review AI Rankings → Shortlist/Reject Candidates

### Candidate Flow
1. Register/Login → Browse Jobs → Apply to Job
2. Take Assessment → Submit Answers → View Results & Feedback

### AI Evaluation Flow
1. Candidate submits assessment
2. Celery task triggered (async)
3. AI evaluates each answer:
   - MCQ: Correct/incorrect
   - Coding: Correctness, efficiency, readability
   - Descriptive: Relevance, communication, critical thinking
4. Generate skill scores
5. Create personalized feedback report
6. Generate AI reasoning for ranking
7. Store results in database
8. Notify candidate

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login user
- GET `/api/auth/me` - Get current user

### Jobs
- POST `/api/jobs` - Create job (recruiter)
- GET `/api/jobs` - List jobs
- GET `/api/jobs/{id}` - Get job details
- PUT `/api/jobs/{id}` - Update job
- DELETE `/api/jobs/{id}` - Delete job
- POST `/api/jobs/{id}/publish` - Publish job

### Assessments
- POST `/api/assessments` - Create assessment (AI-generated)
- GET `/api/assessments/{id}` - Get assessment
- GET `/api/assessments/job/{job_id}` - Get assessment by job

### Applications
- POST `/api/applications` - Apply to job
- GET `/api/applications` - List applications
- GET `/api/applications/{id}` - Get application
- POST `/api/applications/{id}/shortlist` - Shortlist candidate
- POST `/api/applications/{id}/reject` - Reject candidate

### Submissions
- POST `/api/submissions` - Submit assessment
- POST `/api/submissions/start/{application_id}` - Start assessment
- GET `/api/submissions/{id}` - Get submission

### Results
- GET `/api/results/application/{application_id}` - Get result
- GET `/api/results/job/{job_id}/rankings` - Get ranked results
- GET `/api/results/{id}` - Get specific result

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11+** - Programming language
- **Motor** - Async MongoDB driver
- **Celery** - Distributed task queue
- **Redis** - Cache & message broker

### AI/ML
- **LangChain** - LLM orchestration
- **Google Gemini 2.0 Flash** - AI model
- **langchain-google-genai** - Gemini integration

### Database
- **MongoDB Atlas** - NoSQL database
- **Redis** - In-memory data store

### Frontend
- **Jinja2** - Template engine
- **Custom CSS** - Styling
- **Vanilla JavaScript** - Client-side logic

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Git** - Version control

## Features Implemented

### AI-Powered Smart Features ✓
- Intelligent question generation
- Code quality analysis (correctness, efficiency, readability)
- Behavioral assessment
- Resume intelligence (structure ready)
- Predictive success scoring
- Bias detection

### Exceptional Candidate Experience ✓
- Personalized feedback reports
- Skill gap visualization
- Learning resource recommendations
- Improvement plans with timelines
- Encouraging messages
- Next steps guidance

### Core Functionality ✓
- Multi-role support (technical & non-technical)
- Real-time assessment monitoring (structure ready)
- Interactive code playground
- Comprehensive analytics dashboard
- Automated shortlisting
- Email notifications (structure ready)

### Design & UX ✓
- Blue & white professional theme
- Fluid animations
- Responsive design (mobile, tablet, desktop)
- Modern card-based layouts
- Smooth transitions
- Loading states & skeleton screens

## Security Features

- JWT-based authentication
- Password hashing (bcrypt)
- Input validation (Pydantic)
- CORS configuration
- SQL injection prevention (NoSQL)
- XSS protection
- Rate limiting (ready to implement)

## Performance Optimizations

- Database indexing
- Async operations
- Connection pooling
- Caching with Redis
- Background task processing
- Lazy loading

## Testing Strategy

- Unit tests for models
- Integration tests for API endpoints
- End-to-end tests for user flows
- Load testing for scalability
- AI evaluation accuracy testing

## Future Enhancements

- Video interview analysis
- Live coding sessions
- Practice mode for candidates
- AI career coach chatbot
- Advanced analytics dashboard
- Mobile app
- Multi-language support
- Integration with ATS systems
- Blockchain-based certificates

## Development Workflow

1. **Setup**: `python3 setup.py`
2. **Configure**: Edit `.env` file
3. **Run**: `./run.sh` (FastAPI) + `./run_celery.sh` (Celery)
4. **Test**: Access http://localhost:8000
5. **Deploy**: `docker-compose up --build`

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Write tests
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
- GitHub Issues
- Documentation
- Email support

---

Built with ❤️ for fair and intelligent hiring
