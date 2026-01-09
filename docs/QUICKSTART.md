# Quick Start Guide

Get HireWave running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account ([Sign up free](https://www.mongodb.com/cloud/atlas/register))
- Redis (or use Docker)
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

## Option 1: Docker (Recommended)

The fastest way to get started:

```bash
# 1. Clone the repository
git clone <repository-url>
cd hirewave

# 2. Create .env file
cp .env.example .env

# 3. Edit .env and add your Gemini API key
nano .env  # or use your favorite editor
# Set: GOOGLE_API_KEY=your-actual-api-key-here

# 4. Start everything with Docker
docker-compose up --build
```

That's it! Access the application at **http://localhost:8000**

## Option 2: Local Development

### Step 1: Setup

```bash
# Clone repository
git clone <repository-url>
cd hirewave

# Run setup script
python3 setup.py
```

### Step 2: Configure

Edit `.env` file:
```bash
GOOGLE_API_KEY=your-gemini-api-key-here
MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=hirewave
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=change-this-to-a-random-secret-key
```

**Get MongoDB Atlas Connection String:**
1. Go to [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a free cluster (if you haven't)
3. Click "Connect" → "Connect your application"
4. Copy the connection string
5. Replace `<username>`, `<password>`, and `<cluster>` with your values

### Step 3: Start Services

**Terminal 1 - Redis:**
```bash
redis-server
```

**Terminal 2 - FastAPI:**
```bash
./run.sh
```

**Terminal 3 - Celery Worker:**
```bash
./run_celery.sh
```

Note: MongoDB Atlas is cloud-hosted, so no local MongoDB needed!

### Step 4: Access Application

Open your browser: **http://localhost:8000**

## First Steps

### 1. Register as Recruiter

1. Go to http://localhost:8000/register
2. Select "Recruiter"
3. Fill in details:
   - Name: Test Recruiter
   - Email: recruiter@test.com
   - Password: test123
   - Company: Test Company
4. Click Register

### 2. Create a Job

1. You'll be redirected to recruiter dashboard
2. Click "Create New Job"
3. Fill in job details:
   - Title: Software Engineer
   - Type: Technical
   - Description: Looking for full-stack developers
   - Skills: Python, JavaScript, React
   - Location: Remote
4. Click Create

### 3. Generate AI Assessment

1. Click "Create Assessment" on your job
2. Wait for AI to generate questions (30-60 seconds)
3. Review the generated assessment
4. Click "Publish Job"

### 4. Register as Candidate

1. Open new incognito window or logout
2. Go to http://localhost:8000/register
3. Select "Student/Candidate"
4. Fill in details:
   - Name: Test Student
   - Email: student@test.com
   - Password: test123
   - College: Test University
5. Click Register

### 5. Apply to Job

1. Go to Jobs page
2. Click on the Software Engineer job
3. Click "Apply Now"
4. You'll be redirected to dashboard

### 6. Take Assessment

1. Click "Start Assessment" on your application
2. Answer the questions:
   - MCQ questions
   - Coding problems
   - Situational questions
3. Click "Submit Assessment"

### 7. View Results

1. Wait 1-2 minutes for AI evaluation
2. Click "View Results"
3. See your:
   - Overall score
   - Skill breakdown
   - Personalized feedback
   - Learning recommendations

### 8. View Rankings (as Recruiter)

1. Login as recruiter
2. Go to your job
3. Click "View Candidates"
4. See AI-ranked candidates with:
   - Scores
   - Skill analysis
   - AI confidence
   - Shortlist/Reject options

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### MongoDB Connection Error
- Verify your MongoDB Atlas connection string is correct
- Check username and password are properly URL-encoded
- Ensure your IP address is whitelisted in Atlas (Network Access)
- Verify the cluster is running in Atlas dashboard

### Redis Connection Error
```bash
# Check if Redis is running
ps aux | grep redis

# Start Redis
redis-server
```

### Celery Not Processing Tasks
```bash
# Check Celery worker logs
# Make sure Redis is running
# Restart Celery worker
```

### AI Generation Fails
- Verify GOOGLE_API_KEY is correct
- Check API quota limits
- Review application logs

## Common Commands

```bash
# Start application
make run

# Start Celery worker
make celery

# Start with Docker
make docker-up

# Stop Docker
make docker-down

# Clean temporary files
make clean

# View all commands
make help
```

## Project Structure

```
hirewave/
├── app/              # Backend code
├── templates/        # HTML templates
├── static/           # CSS, JS, images
├── uploads/          # File uploads
├── .env             # Configuration
└── docker-compose.yml
```

## Key Features to Try

### For Recruiters
- ✅ Create jobs with AI-generated assessments
- ✅ View AI-ranked candidates
- ✅ See detailed evaluation reasoning
- ✅ Shortlist/reject candidates
- ✅ Export reports

### For Candidates
- ✅ Browse and apply to jobs
- ✅ Take interactive assessments
- ✅ Get personalized feedback
- ✅ See skill gap analysis
- ✅ Receive learning recommendations

### AI Features
- ✅ Intelligent question generation
- ✅ Code quality analysis
- ✅ Behavioral assessment
- ✅ Bias detection
- ✅ Predictive success scoring

## Next Steps

1. **Customize**: Edit templates and styles
2. **Extend**: Add new features
3. **Deploy**: Follow DEPLOYMENT.md
4. **Scale**: Add more workers, use load balancer

## Getting Help

- 📖 Read full documentation: README.md
- 🚀 Deployment guide: DEPLOYMENT.md
- 🏗️ Project structure: PROJECT_STRUCTURE.md
- 🐛 Report issues: GitHub Issues

## Demo Credentials

For quick testing:

**Recruiter:**
- Email: recruiter@test.com
- Password: test123

**Candidate:**
- Email: student@test.com
- Password: test123

## Tips

1. **Use Docker** for easiest setup
2. **Check logs** if something doesn't work
3. **Wait for AI** - evaluation takes 30-60 seconds
4. **Try different roles** - recruiter vs candidate experience
5. **Explore API docs** - http://localhost:8000/api/docs

## Performance

- Assessment generation: ~30-60 seconds
- Evaluation per candidate: ~30-60 seconds
- Concurrent users: 100+ (with proper scaling)
- Database: MongoDB (scalable)
- Caching: Redis (fast)

## Security Notes

⚠️ **For Production:**
- Change all default passwords
- Use strong JWT_SECRET_KEY
- Enable HTTPS
- Configure CORS properly
- Set up firewall
- Regular backups

## Success!

If you see the home page at http://localhost:8000, you're all set! 🎉

Start by registering as a recruiter and creating your first AI-powered assessment.

---

**Need help?** Check the full documentation or open an issue on GitHub.
