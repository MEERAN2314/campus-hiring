# HireWave - Test Data Reference

## Overview
This document provides a quick reference for all sample data seeded into the database for testing purposes.

## How to Seed Data

```bash
# Run the seed script
python3 seed_data.py
```

**Note:** This will clear existing sample data and insert fresh test data.

---

## 🔐 Test Credentials

**All passwords are:** `password123`

---

## 👔 Recruiter Accounts (5 Companies)

| Email | Company | Jobs Posted |
|-------|---------|-------------|
| recruiter@techcorp.com | TechCorp Solutions | 3 jobs |
| hr@innovateai.com | InnovateAI Labs | 2 jobs |
| talent@cloudnine.com | CloudNine Technologies | 3 jobs |
| hiring@datastream.io | DataStream Analytics | 2 jobs |
| careers@fintech.com | FinTech Innovations | 2 jobs |

### Company Details

**TechCorp Solutions**
- Full Stack Developer - San Francisco (Remote) - $80K-$100K
- Frontend Developer - Remote - $70K-$90K
- Product Manager - New York (Hybrid) - $75K-$95K

**InnovateAI Labs**
- Machine Learning Engineer - Boston (Hybrid) - $90K-$120K
- Backend Developer - Seattle (Remote) - $85K-$105K

**CloudNine Technologies**
- DevOps Engineer - Austin (Remote) - $85K-$110K
- Mobile App Developer - Los Angeles (Remote) - $75K-$95K
- Quality Assurance Engineer - Remote - $65K-$85K

**DataStream Analytics**
- Data Analyst - Chicago (Hybrid) - $65K-$85K
- Business Analyst - Denver (Hybrid) - $70K-$90K

**FinTech Innovations**
- Cybersecurity Analyst - New York (Hybrid) - $80K-$100K
- UI/UX Designer - San Francisco (Remote) - $70K-$90K

---

## 🎓 Candidate Accounts (12 Students)

| Email | Name | College | Key Skills |
|-------|------|---------|------------|
| john.doe@university.edu | John Doe | MIT | Python, JavaScript, React, Node.js, MongoDB |
| jane.smith@university.edu | Jane Smith | Stanford University | Java, Spring Boot, MySQL, AWS, Docker |
| alex.kumar@university.edu | Alex Kumar | UC Berkeley | Python, Machine Learning, TensorFlow, Data Science |
| emily.brown@university.edu | Emily Brown | Harvard University | React, TypeScript, GraphQL, UI/UX Design |
| david.lee@university.edu | David Lee | Carnegie Mellon | C++, System Design, Algorithms, Distributed Systems |
| sophia.garcia@university.edu | Sophia Garcia | Georgia Tech | Python, Django, PostgreSQL, REST APIs, Git |
| ryan.patel@university.edu | Ryan Patel | University of Michigan | JavaScript, Vue.js, Node.js, Express, MongoDB |
| olivia.wilson@university.edu | Olivia Wilson | Cornell University | Data Analysis, Python, Pandas, SQL, Tableau |
| ethan.rodriguez@university.edu | Ethan Rodriguez | University of Texas | Cybersecurity, Network Security, Ethical Hacking, Linux |
| ava.thompson@university.edu | Ava Thompson | University of Washington | Mobile Development, React Native, iOS, Android, Flutter |
| noah.jackson@university.edu | Noah Jackson | Duke University | DevOps, Kubernetes, Docker, CI/CD, Jenkins |
| mia.white@university.edu | Mia White | Northwestern University | Product Management, Agile, Scrum, JIRA, Analytics |

---

## 💼 Job Listings (12 Positions)

### Technical Roles (9)

1. **Full Stack Developer** - TechCorp Solutions
   - Skills: Python, JavaScript, React, Node.js, MongoDB
   - Location: San Francisco, CA (Remote)
   - Salary: $80,000 - $100,000

2. **Machine Learning Engineer** - InnovateAI Labs
   - Skills: Python, Machine Learning, TensorFlow, PyTorch, Data Science
   - Location: Boston, MA (Hybrid)
   - Salary: $90,000 - $120,000

3. **Frontend Developer** - TechCorp Solutions
   - Skills: React, TypeScript, JavaScript, CSS, HTML
   - Location: Remote
   - Salary: $70,000 - $90,000

4. **Backend Developer** - InnovateAI Labs
   - Skills: Java, Spring Boot, MySQL, AWS, Docker
   - Location: Seattle, WA (Remote)
   - Salary: $85,000 - $105,000

5. **DevOps Engineer** - CloudNine Technologies
   - Skills: DevOps, Kubernetes, Docker, CI/CD, AWS
   - Location: Austin, TX (Remote)
   - Salary: $85,000 - $110,000

6. **Data Analyst** - DataStream Analytics
   - Skills: Data Analysis, Python, SQL, Tableau, Excel
   - Location: Chicago, IL (Hybrid)
   - Salary: $65,000 - $85,000

7. **Mobile App Developer** - CloudNine Technologies
   - Skills: React Native, iOS, Android, JavaScript, Mobile Development
   - Location: Los Angeles, CA (Remote)
   - Salary: $75,000 - $95,000

8. **Cybersecurity Analyst** - FinTech Innovations
   - Skills: Cybersecurity, Network Security, Ethical Hacking, Linux, Security Tools
   - Location: New York, NY (Hybrid)
   - Salary: $80,000 - $100,000

9. **Quality Assurance Engineer** - CloudNine Technologies
   - Skills: QA Testing, Selenium, Test Automation, Manual Testing, Bug Tracking
   - Location: Remote
   - Salary: $65,000 - $85,000

### Non-Technical Roles (3)

10. **Product Manager** - TechCorp Solutions
    - Skills: Product Management, Agile, Communication, Strategy, Analytics
    - Location: New York, NY (Hybrid)
    - Salary: $75,000 - $95,000

11. **Business Analyst** - DataStream Analytics
    - Skills: Business Analysis, Requirements Gathering, Communication, Problem Solving, Documentation
    - Location: Denver, CO (Hybrid)
    - Salary: $70,000 - $90,000

12. **UI/UX Designer** - FinTech Innovations
    - Skills: UI/UX Design, Figma, User Research, Prototyping, Design Thinking
    - Location: San Francisco, CA (Remote)
    - Salary: $70,000 - $90,000

---

## 🎯 Testing Scenarios

### Scenario 1: Recruiter Creates Assessment
1. Login as: `recruiter@techcorp.com`
2. Go to "My Jobs"
3. Click "Create Assessment" on any job
4. Wait for AI to generate questions
5. Review and publish the job

### Scenario 2: Candidate Applies to Job
1. Login as: `john.doe@university.edu`
2. Browse available jobs
3. Apply to "Full Stack Developer" position
4. Take the assessment
5. View results and feedback

### Scenario 3: Multiple Candidates Apply
1. Have 3-4 different candidates apply to the same job
2. Each takes the assessment
3. Login as recruiter to view ranked candidates
4. See AI reasoning for rankings
5. Shortlist top candidates

### Scenario 4: Skill Matching
- **John Doe** (Python, JavaScript, React) → Perfect for Full Stack Developer
- **Alex Kumar** (ML, TensorFlow) → Perfect for ML Engineer
- **Emily Brown** (React, TypeScript, UI/UX) → Perfect for Frontend Developer
- **Jane Smith** (Java, Spring Boot, AWS) → Perfect for Backend Developer
- **Noah Jackson** (DevOps, Kubernetes) → Perfect for DevOps Engineer

### Scenario 5: Cross-Company Testing
1. Login as different recruiters
2. Each creates assessments for their jobs
3. Candidates apply to multiple companies
4. Compare evaluation quality across companies

---

## 📊 Data Statistics

- **Total Recruiters:** 5
- **Total Candidates:** 12
- **Total Jobs:** 12
- **Technical Jobs:** 9
- **Non-Technical Jobs:** 3
- **Companies:** 5
- **Universities:** 10
- **Average Vacancies per Job:** 2
- **Salary Range:** $65K - $120K

---

## 🔄 Resetting Data

To reset and reseed the database:

```bash
# Clear and reseed
python3 seed_data.py

# This will:
# 1. Delete all sample users (recruiter_* and candidate_*)
# 2. Delete all sample jobs (job_*)
# 3. Insert fresh data
```

**Note:** This only affects sample data. Real user data is preserved.

---

## 🚀 Quick Start Testing Flow

1. **Seed the database:**
   ```bash
   python3 seed_data.py
   ```

2. **Start the application:**
   ```bash
   ./run.sh
   ```

3. **Start Celery worker:**
   ```bash
   ./run_celery.sh
   ```

4. **Test as Recruiter:**
   - Login: `recruiter@techcorp.com` / `password123`
   - Create assessment for a job
   - Publish the job

5. **Test as Candidate:**
   - Login: `john.doe@university.edu` / `password123`
   - Apply to the published job
   - Take the assessment
   - View results

6. **View Rankings:**
   - Login back as recruiter
   - View candidates for the job
   - See AI rankings and reasoning

---

## 💡 Tips for Testing

1. **Use different skill sets** - Each candidate has unique skills matching different jobs
2. **Test AI evaluation** - Submit different quality answers to see AI scoring
3. **Compare rankings** - Have multiple candidates apply to see ranking logic
4. **Test feedback** - Check personalized feedback for each candidate
5. **Try both job types** - Test technical and non-technical assessments
6. **Test filters** - Use job search and filtering features
7. **Mobile testing** - Test responsive design on different devices

---

## 🐛 Troubleshooting

**Issue: Seed script fails**
- Check MongoDB connection in `.env`
- Ensure database name is correct
- Verify network access in MongoDB Atlas

**Issue: Jobs not showing**
- Verify jobs have `status: "active"`
- Check if logged in as correct user type
- Clear browser cache

**Issue: Assessment not generating**
- Check Gemini API key in `.env`
- Verify API quota limits
- Check application logs

---

## 📝 Notes

- All sample data uses predictable IDs (recruiter_001, candidate_001, job_001, etc.)
- Passwords are intentionally simple for testing (`password123`)
- Skills are carefully matched to job requirements for realistic testing
- Salary ranges are based on 2024 market rates for fresh graduates
- All jobs are set to "active" status for immediate testing

---

**Happy Testing!** 🎉

For questions or issues, check the main README.md or QUICKSTART.md files.
