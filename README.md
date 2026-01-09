# Campus Hiring Platform

An AI-powered recruitment platform that automates end-to-end campus hiring with intelligent assessment creation, evaluation, and candidate feedback.

## Features

### AI-Powered Smart Features
- **Intelligent Question Generation**: Auto-generate role-specific assessments using Gemini AI
- **Code Quality Analysis**: Deep analysis of coding solutions (correctness, efficiency, readability)
- **Behavioral Assessment**: AI evaluation of soft skills from written responses
- **Resume Intelligence**: Auto-extract skills and match candidates to roles
- **Predictive Success Score**: AI predicts job fit based on comprehensive analysis
- **Bias Detection**: Identifies and flags potential bias in evaluation

### Exceptional Candidate Experience
- **Personalized Feedback Reports**: Detailed improvement plans for all candidates
- **Skill Gap Visualization**: Beautiful charts showing strengths and growth areas
- **Practice Mode**: Students can practice before real assessments
- **AI Career Coach**: Chatbot assistance for role/company questions
- **Progress Tracking**: Visual journey from application to result

### Core Functionality
- Multi-role support (technical & non-technical)
- Real-time assessment monitoring
- Interactive code playground
- Comprehensive analytics dashboard
- Automated shortlisting and notifications
- Export reports (PDF/Excel)

## Tech Stack

- **Backend**: FastAPI + Python
- **AI**: LangChain + Google Gemini 2.0 Flash
- **Database**: MongoDB Atlas
- **Cache/Queue**: Redis + Celery
- **Frontend**: Jinja2 + Custom CSS + Vanilla JavaScript
- **Real-time**: WebSockets

## Setup

### Prerequisites
- Python 3.11+
- MongoDB Atlas account (free tier available)
- Redis
- Google Gemini API Key

### Local Development

1. Clone the repository
```bash
git clone <repository-url>
cd campus-hiring
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment
```bash
cp .env.example .env
# Edit .env with your MongoDB Atlas connection string and API keys
```

**MongoDB Atlas Setup:**
- Sign up at https://cloud.mongodb.com
- Create a free M0 cluster
- Create database user
- Whitelist your IP (Network Access)
- Get connection string and add to .env

5. Run the application
```bash
uvicorn app.main:app --reload
```

6. Run Celery worker (in separate terminal)
```bash
celery -A app.celery_worker worker --loglevel=info
```

### Docker Deployment

```bash
docker-compose up --build
```

Access the application at `http://localhost:8000`

## Project Structure

```
campus-hiring/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── database.py             # MongoDB connection
│   ├── celery_worker.py        # Celery tasks
│   ├── models/                 # Pydantic models
│   ├── routes/                 # API endpoints
│   ├── services/               # Business logic
│   ├── ai/                     # AI/LangChain integration
│   └── utils/                  # Utilities
├── templates/                  # Jinja2 templates
├── static/                     # CSS, JS, images
├── uploads/                    # File uploads
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## License

MIT License
