# Testing Guide - Campus Hiring Platform

## Quick Testing Flow

### Step 1: Seed the Database

```bash
python seed_data.py
```

This creates:
- 2 Recruiter accounts
- 5 Candidate accounts  
- 5 Job postings (without assessments)

### Step 2: Login as Recruiter

**Credentials:**
- Email: `recruiter@techcorp.com`
- Password: `password123`

### Step 3: Create AI Assessment for a Job

1. Go to "Recruiter Dashboard" or `/recruiter/jobs`
2. You'll see your jobs listed
3. Click **"Create Assessment"** on any job
4. Wait 30-60 seconds for AI to generate questions
5. Once created, click **"Publish Job"**

**Important:** Jobs must have assessments before candidates can apply and take tests!

### Step 4: Login as Candidate

**Credentials:**
- Email: `john.doe@university.edu`
- Password: `password123`

(Or use any of the other 4 candidate accounts)

### Step 5: Browse and Apply to Jobs

1. Go to "Jobs" page
2. Browse available jobs
3. Click "View Details" on a job
4. Click "Apply Now"

### Step 6: Take Assessment

1. Go to "Dashboard"
2. Find your application
3. Click "Start Assessment"
4. Answer the questions:
   - MCQ questions
   - Coding problems
   - Situational questions
5. Click "Submit Assessment"

### Step 7: View Results

1. Wait 1-2 minutes for AI evaluation
2. Go to Dashboard
3. Click "View Results"
4. See your:
   - Overall score
   - Skill breakdown
   - Personalized feedback
   - Learning recommendations

### Step 8: View Rankings (as Recruiter)

1. Login as recruiter again
2. Go to your job
3. Click "View Candidates"
4. See AI-ranked candidates with detailed analysis

---

## Test Accounts

### Recruiters

| Email | Password | Company |
|-------|----------|---------|
| recruiter@techcorp.com | password123 | TechCorp Solutions |
| hr@innovateai.com | password123 | InnovateAI Labs |

### Candidates

| Email | Password | College |
|-------|----------|---------|
| john.doe@university.edu | password123 | MIT |
| jane.smith@university.edu | password123 | Stanford University |
| alex.kumar@university.edu | password123 | UC Berkeley |
| emily.brown@university.edu | password123 | Harvard University |
| david.lee@university.edu | password123 | Carnegie Mellon |

---

## Sample Jobs Created

1. **Full Stack Developer** - TechCorp Solutions
2. **Machine Learning Engineer** - InnovateAI Labs
3. **Frontend Developer** - TechCorp Solutions
4. **Backend Developer** - InnovateAI Labs
5. **Product Manager** - TechCorp Solutions

---

## Common Issues

### "Error loading assessment"
**Cause:** Job doesn't have an assessment yet
**Solution:** Login as recruiter and create assessment for that job

### "Job not found" when clicking View Details
**Cause:** Job ID not properly passed
**Solution:** Restart the application (already fixed in code)

### "Assessment not available"
**Cause:** Recruiter hasn't created assessment yet
**Solution:** Create assessment as recruiter first

### AI generation takes too long
**Cause:** Gemini API processing
**Solution:** Wait 30-60 seconds, it's normal

### No jobs showing for candidates
**Cause:** Jobs are in "draft" status
**Solution:** Recruiter must publish jobs after creating assessments

---

## Testing Checklist

### Recruiter Flow
- [ ] Login as recruiter
- [ ] View jobs dashboard
- [ ] Create AI assessment for a job
- [ ] Verify assessment was created
- [ ] Publish the job
- [ ] Wait for candidate applications
- [ ] View candidate rankings
- [ ] Shortlist a candidate
- [ ] Reject a candidate

### Candidate Flow
- [ ] Login as candidate
- [ ] Browse jobs
- [ ] View job details
- [ ] Apply to a job
- [ ] Start assessment
- [ ] Answer MCQ questions
- [ ] Solve coding problem
- [ ] Answer situational question
- [ ] Submit assessment
- [ ] Wait for evaluation
- [ ] View results
- [ ] Check feedback report
- [ ] Review learning resources

### AI Features to Test
- [ ] Assessment generation (role-specific questions)
- [ ] Code evaluation (correctness, efficiency, readability)
- [ ] Behavioral assessment
- [ ] Personalized feedback
- [ ] AI reasoning for rankings
- [ ] Skill gap analysis
- [ ] Learning resource recommendations

---

## Demo Script (10 minutes)

### Part 1: Recruiter Creates Job & Assessment (3 min)
1. Login as recruiter
2. Show jobs dashboard
3. Click "Create Assessment" on a job
4. Show AI generating questions
5. Publish the job

### Part 2: Candidate Takes Assessment (3 min)
1. Login as candidate
2. Browse and apply to job
3. Start assessment
4. Show different question types
5. Submit assessment

### Part 3: View Results & Rankings (4 min)
1. Show candidate results page (WOW FACTOR!)
   - Overall score with animation
   - Skill breakdown
   - Personalized feedback
   - Learning resources
2. Switch to recruiter view
3. Show candidate rankings
4. Show AI reasoning
5. Demonstrate shortlist/reject

---

## Tips for Best Demo

1. **Pre-create assessments** before demo to save time
2. **Have multiple browser windows** ready (recruiter + candidate)
3. **Highlight the feedback page** - it's the unique feature
4. **Emphasize AI reasoning** - shows transparency
5. **Show the smooth animations** - professional UX
6. **Mention scalability** - production-ready architecture

---

## Troubleshooting

### Application won't start
```bash
# Check if all dependencies are installed
pip install -r requirements.txt

# Check if .env is configured
cat .env | grep GOOGLE_API_KEY
cat .env | grep MONGODB_URL
```

### Database connection fails
```bash
# Verify MongoDB Atlas connection string
# Check IP whitelist in Atlas
# Ensure database user has permissions
```

### Celery worker not processing
```bash
# Make sure Redis is running
redis-cli ping

# Restart Celery worker
./run_celery.sh
```

---

## Next Steps After Testing

1. Create more sample data if needed
2. Test edge cases
3. Check responsive design on mobile
4. Verify all animations work
5. Test error handling
6. Prepare demo talking points
7. Practice the 10-minute demo flow

---

**Happy Testing! 🚀**
