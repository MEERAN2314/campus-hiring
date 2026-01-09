# Testing Guide

## Manual Testing Checklist

### 1. Authentication Flow

**Register as Recruiter:**
- [ ] Navigate to /register
- [ ] Select "Recruiter" user type
- [ ] Fill form with valid data
- [ ] Submit and verify redirect to recruiter dashboard
- [ ] Verify token stored in localStorage
- [ ] Check navbar shows user name and logout button

**Register as Candidate:**
- [ ] Navigate to /register
- [ ] Select "Student/Candidate" user type
- [ ] Fill form with valid data
- [ ] Submit and verify redirect to candidate dashboard
- [ ] Verify token stored in localStorage

**Login:**
- [ ] Navigate to /login
- [ ] Enter valid credentials
- [ ] Verify successful login and redirect
- [ ] Try invalid credentials - should show error
- [ ] Verify token persistence across page refresh

**Logout:**
- [ ] Click logout button
- [ ] Verify redirect to home page
- [ ] Verify token removed from localStorage
- [ ] Try accessing protected routes - should redirect to login

### 2. Recruiter Flow

**Create Job:**
- [ ] Login as recruiter
- [ ] Click "Create New Job"
- [ ] Fill all required fields
- [ ] Submit and verify job appears in list
- [ ] Verify job status is "draft"

**Generate Assessment:**
- [ ] Click "Create Assessment" on a job
- [ ] Wait for AI generation (30-60 seconds)
- [ ] Verify assessment created successfully
- [ ] Check questions are relevant to job
- [ ] Verify mix of MCQ, coding, and descriptive questions

**Publish Job:**
- [ ] Click "Publish Job" on job with assessment
- [ ] Verify status changes to "active"
- [ ] Verify job appears in public job listings

**View Candidates:**
- [ ] After candidates apply and complete assessments
- [ ] Click "View Candidates" on job
- [ ] Verify candidates are ranked by score
- [ ] Check AI reasoning is displayed
- [ ] Verify skill scores are shown

**Shortlist/Reject:**
- [ ] Click "Shortlist" on a candidate
- [ ] Verify status changes to "shortlisted"
- [ ] Click "Reject" on a candidate
- [ ] Verify status changes to "rejected"

### 3. Candidate Flow

**Browse Jobs:**
- [ ] Navigate to /jobs
- [ ] Verify active jobs are displayed
- [ ] Test search functionality
- [ ] Test filter by job type
- [ ] Click on a job to view details

**Apply to Job:**
- [ ] Login as candidate
- [ ] View job details
- [ ] Click "Apply Now"
- [ ] Verify application created
- [ ] Check application appears in dashboard
- [ ] Try applying again - should show error

**Take Assessment:**
- [ ] Click "Start Assessment" on application
- [ ] Verify assessment loads with questions
- [ ] Answer MCQ questions
- [ ] Write code for coding questions
- [ ] Answer descriptive questions
- [ ] Navigate between questions
- [ ] Submit assessment
- [ ] Verify submission confirmation

**View Results:**
- [ ] Wait for evaluation (1-2 minutes)
- [ ] Click "View Results"
- [ ] Verify overall score is displayed
- [ ] Check skill breakdown chart
- [ ] Verify strengths are listed
- [ ] Check improvement areas
- [ ] Verify learning resources are provided
- [ ] Check personalized improvement plan

### 4. UI/UX Testing

**Responsive Design:**
- [ ] Test on desktop (1920x1080)
- [ ] Test on laptop (1366x768)
- [ ] Test on tablet (768x1024)
- [ ] Test on mobile (375x667)
- [ ] Verify all elements are accessible
- [ ] Check navigation menu on mobile

**Animations:**
- [ ] Verify smooth page transitions
- [ ] Check button hover effects
- [ ] Test card hover animations
- [ ] Verify loading states
- [ ] Check progress indicators

**Theme:**
- [ ] Verify blue and white color scheme
- [ ] Check professional appearance
- [ ] Verify consistent styling
- [ ] Test contrast for readability

### 5. API Testing

**Authentication Endpoints:**
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User",
    "user_type": "candidate",
    "college_name": "Test College"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
```

**Job Endpoints:**
```bash
# List jobs
curl http://localhost:8000/api/jobs

# Get job details
curl http://localhost:8000/api/jobs/{job_id}

# Create job (requires auth)
curl -X POST http://localhost:8000/api/jobs \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer",
    "job_type": "technical",
    "description": "Looking for developers",
    "required_skills": ["Python", "JavaScript"],
    "experience_level": "Fresher",
    "location": "Remote",
    "vacancies": 5,
    "target_colleges": []
  }'
```

### 6. AI Testing

**Assessment Generation:**
- [ ] Create jobs with different skill sets
- [ ] Verify questions match job requirements
- [ ] Check question difficulty distribution
- [ ] Verify coding questions have test cases
- [ ] Check MCQ options are relevant

**Code Evaluation:**
- [ ] Submit correct code - should get high score
- [ ] Submit incorrect code - should get low score
- [ ] Submit inefficient code - should note in feedback
- [ ] Submit unreadable code - should mention readability
- [ ] Check feedback is constructive

**Feedback Generation:**
- [ ] Verify feedback is personalized
- [ ] Check learning resources are relevant
- [ ] Verify improvement plan is actionable
- [ ] Check positive messaging
- [ ] Verify next steps are clear

### 7. Performance Testing

**Load Testing:**
- [ ] Create 10 jobs simultaneously
- [ ] Have 50 candidates apply to same job
- [ ] Submit 20 assessments concurrently
- [ ] Monitor response times
- [ ] Check database performance

**Stress Testing:**
- [ ] Generate 100 assessments
- [ ] Process 100 evaluations
- [ ] Monitor memory usage
- [ ] Check for memory leaks
- [ ] Verify system stability

### 8. Security Testing

**Authentication:**
- [ ] Try accessing protected routes without token
- [ ] Try using expired token
- [ ] Try using invalid token
- [ ] Verify password is hashed in database
- [ ] Check JWT expiration works

**Authorization:**
- [ ] Candidate tries to access recruiter routes
- [ ] Recruiter tries to access other recruiter's data
- [ ] Try to view other user's results
- [ ] Verify proper access control

**Input Validation:**
- [ ] Submit empty forms
- [ ] Submit invalid email formats
- [ ] Submit SQL injection attempts
- [ ] Submit XSS payloads
- [ ] Verify all inputs are sanitized

### 9. Error Handling

**Network Errors:**
- [ ] Disconnect internet during API call
- [ ] Verify error message is shown
- [ ] Check graceful degradation

**Database Errors:**
- [ ] Stop MongoDB
- [ ] Try to perform operations
- [ ] Verify error handling
- [ ] Restart MongoDB and verify recovery

**AI Errors:**
- [ ] Use invalid API key
- [ ] Exceed API quota
- [ ] Verify fallback mechanisms
- [ ] Check error messages

### 10. Integration Testing

**End-to-End Flow:**
1. [ ] Recruiter registers
2. [ ] Recruiter creates job
3. [ ] AI generates assessment
4. [ ] Recruiter publishes job
5. [ ] Candidate registers
6. [ ] Candidate applies to job
7. [ ] Candidate takes assessment
8. [ ] AI evaluates submission
9. [ ] Candidate views results
10. [ ] Recruiter views rankings
11. [ ] Recruiter shortlists candidate

## Automated Testing

### Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=app tests/

# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/
```

### Test Structure

```
tests/
├── test_auth.py          # Authentication tests
├── test_jobs.py          # Job CRUD tests
├── test_assessments.py   # Assessment tests
├── test_applications.py  # Application tests
├── test_submissions.py   # Submission tests
├── test_results.py       # Results tests
└── test_ai.py           # AI service tests
```

### Example Test

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_candidate():
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "test123",
        "full_name": "Test User",
        "user_type": "candidate",
        "college_name": "Test College"
    })
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_login():
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## Performance Benchmarks

### Expected Performance

- **Page Load**: < 2 seconds
- **API Response**: < 500ms
- **Assessment Generation**: 30-60 seconds
- **Evaluation**: 30-60 seconds per candidate
- **Database Query**: < 100ms
- **Concurrent Users**: 100+

### Monitoring

```bash
# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/jobs

# Monitor Celery tasks
celery -A app.celery_worker inspect active

# Monitor MongoDB
mongostat

# Monitor Redis
redis-cli info stats
```

## Bug Reporting

When reporting bugs, include:

1. **Steps to reproduce**
2. **Expected behavior**
3. **Actual behavior**
4. **Screenshots/videos**
5. **Browser/OS**
6. **Error messages**
7. **Console logs**

## Test Data

### Sample Users

**Recruiter:**
- Email: recruiter@test.com
- Password: test123
- Company: Test Company

**Candidate:**
- Email: student@test.com
- Password: test123
- College: Test University

### Sample Job

```json
{
  "title": "Full Stack Developer",
  "job_type": "technical",
  "description": "Looking for full-stack developers with Python and React experience",
  "required_skills": ["Python", "JavaScript", "React", "MongoDB"],
  "experience_level": "Fresher",
  "location": "Remote",
  "vacancies": 5
}
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      mongodb:
        image: mongo:7.0
        ports:
          - 27017:27017
      
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest tests/ -v --cov=app
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Quality Metrics

### Code Coverage Target
- Overall: > 80%
- Critical paths: > 95%
- AI services: > 70%

### Code Quality
- Pylint score: > 8.0
- No critical security issues
- All tests passing
- Documentation complete

## Testing Checklist Summary

- [ ] All authentication flows work
- [ ] Recruiter can create and manage jobs
- [ ] AI generates relevant assessments
- [ ] Candidates can apply and take assessments
- [ ] AI evaluation produces accurate results
- [ ] Feedback is personalized and helpful
- [ ] UI is responsive on all devices
- [ ] Animations are smooth
- [ ] API endpoints work correctly
- [ ] Security measures are effective
- [ ] Performance meets benchmarks
- [ ] Error handling is graceful
- [ ] Integration flow works end-to-end

---

**Happy Testing! 🧪**
