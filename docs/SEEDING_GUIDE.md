# Database Seeding Guide

## Overview
HireWave provides multiple ways to seed your database with sample data for testing.

## Methods

### Method 1: Interactive Seeding (Recommended)
**Asks for confirmation before clearing data**

```bash
python3 seed_data.py
```

**What it does:**
1. Shows warning about data deletion
2. Asks for confirmation (yes/no)
3. Clears ALL existing data if confirmed
4. Inserts fresh sample data
5. Shows summary of inserted data

**Use when:**
- You want to be careful about data deletion
- First time seeding
- Production-like environment

---

### Method 2: Force Seeding (Quick)
**Clears data immediately with 3-second countdown**

```bash
python3 seed_force.py
```

**What it does:**
1. Shows 3-second countdown
2. Clears ALL data automatically
3. Inserts fresh sample data
4. No confirmation needed

**Use when:**
- Development environment
- Quick testing
- You're sure you want to reset

---

### Method 3: Shell Script (Easiest)
**Interactive menu to choose mode**

```bash
./seed.sh
```

**What it does:**
1. Checks prerequisites (.env, Python)
2. Asks which mode (Interactive or Force)
3. Runs selected seeding method
4. Shows next steps

**Use when:**
- You want a guided experience
- Not sure which method to use
- Want automatic validation

---

## What Gets Cleared

⚠️ **ALL of these collections are completely cleared:**

- ✅ Users (recruiters and candidates)
- ✅ Jobs
- ✅ Assessments
- ✅ Applications
- ✅ Submissions
- ✅ Results

**Nothing is preserved!**

---

## What Gets Created

### 5 Recruiters
| Email | Company | Password |
|-------|---------|----------|
| recruiter@techcorp.com | TechCorp Solutions | password123 |
| hr@innovateai.com | InnovateAI Labs | password123 |
| talent@cloudnine.com | CloudNine Technologies | password123 |
| hiring@datastream.io | DataStream Analytics | password123 |
| careers@fintech.com | FinTech Innovations | password123 |

### 12 Candidates
| Email | College | Skills |
|-------|---------|--------|
| john.doe@university.edu | MIT | Full Stack |
| jane.smith@university.edu | Stanford | Backend/Cloud |
| alex.kumar@university.edu | UC Berkeley | ML/AI |
| emily.brown@university.edu | Harvard | Frontend/Design |
| david.lee@university.edu | Carnegie Mellon | Systems |
| sophia.garcia@university.edu | Georgia Tech | Python/Django |
| ryan.patel@university.edu | U Michigan | JavaScript/Vue |
| olivia.wilson@university.edu | Cornell | Data Analysis |
| ethan.rodriguez@university.edu | UT Austin | Cybersecurity |
| ava.thompson@university.edu | U Washington | Mobile Dev |
| noah.jackson@university.edu | Duke | DevOps |
| mia.white@university.edu | Northwestern | Product Mgmt |

### 12 Jobs
- Full Stack Developer (TechCorp)
- Machine Learning Engineer (InnovateAI)
- Frontend Developer (TechCorp)
- Backend Developer (InnovateAI)
- Product Manager (TechCorp)
- DevOps Engineer (CloudNine)
- Data Analyst (DataStream)
- Mobile App Developer (CloudNine)
- Cybersecurity Analyst (FinTech)
- Business Analyst (DataStream)
- UI/UX Designer (FinTech)
- Quality Assurance Engineer (CloudNine)

---

## Step-by-Step Usage

### Quick Start (Force Mode)
```bash
# 1. Make scripts executable (already done)
chmod +x seed.sh seed_force.py

# 2. Run force seed
python3 seed_force.py

# 3. Wait for 3-second countdown
# 4. Data is cleared and reseeded
# 5. Done!
```

### Safe Start (Interactive Mode)
```bash
# 1. Run interactive seed
python3 seed_data.py

# 2. Read the warning
# 3. Type 'yes' to confirm
# 4. Data is cleared and reseeded
# 5. Done!
```

### Guided Start (Shell Script)
```bash
# 1. Run shell script
./seed.sh

# 2. Choose mode (1 or 2)
# 3. Follow prompts
# 4. Done!
```

---

## Expected Output

### Successful Seeding:
```
============================================================
HireWave - Database Seeding
============================================================

📡 Connecting to MongoDB...
✓ Connected to MongoDB successfully

🗑️  Clearing ALL existing data...
   ✓ Cleared 5 documents from users
   ✓ Cleared 12 documents from jobs
   ✓ Cleared 3 documents from assessments
   ✓ Cleared 8 documents from applications
   ✓ Cleared 5 documents from submissions
   ✓ Cleared 5 documents from results
✓ All existing data cleared

👔 Inserting sample recruiters...
✓ Inserted 5 recruiters
   - Sarah Johnson (recruiter@techcorp.com) - TechCorp Solutions
   - Michael Chen (hr@innovateai.com) - InnovateAI Labs
   ...

🎓 Inserting sample candidates...
✓ Inserted 12 candidates
   - John Doe (john.doe@university.edu) - MIT
   - Jane Smith (jane.smith@university.edu) - Stanford
   ...

💼 Inserting sample jobs...
✓ Inserted 12 jobs
   - Full Stack Developer at TechCorp Solutions
   - Machine Learning Engineer at InnovateAI Labs
   ...

============================================================
✅ Database seeding completed successfully!
============================================================

📊 Summary:
   Recruiters: 5
   Candidates: 12
   Jobs: 12

🔐 Test Credentials:
   All passwords: password123
   
   Recruiter: recruiter@techcorp.com
   Candidate: john.doe@university.edu
```

---

## Troubleshooting

### Error: "Failed to connect to MongoDB"
**Solution:**
1. Check `.env` file has correct `MONGODB_URL`
2. Verify MongoDB Atlas is running
3. Check IP whitelist in MongoDB Atlas
4. Verify database user credentials

### Error: "Permission denied"
**Solution:**
```bash
chmod +x seed.sh seed_force.py seed_data.py
```

### Error: "Module not found"
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt
```

### Warning: "Cleared 0 documents"
**This is normal if:**
- First time seeding
- Database was already empty
- Previous seed failed

---

## After Seeding

### 1. Start the Application
```bash
./run.sh
```

### 2. Start Celery Worker
```bash
./run_celery.sh
```

### 3. Test Login

**As Recruiter:**
- Email: `recruiter@techcorp.com`
- Password: `password123`
- Should see recruiter dashboard

**As Candidate:**
- Email: `john.doe@university.edu`
- Password: `password123`
- Should see candidate dashboard

### 4. Test Features

**Recruiter Flow:**
1. View jobs → Should see 3 jobs from TechCorp
2. Create assessment for a job
3. Publish job
4. View candidates (after candidates apply)

**Candidate Flow:**
1. Browse jobs → Should see 12 active jobs
2. Apply to a job
3. Take assessment
4. View results

---

## Best Practices

### Development
- ✅ Use force seeding for quick resets
- ✅ Seed often to test with fresh data
- ✅ Don't worry about data loss

### Testing
- ✅ Use interactive seeding
- ✅ Verify data before clearing
- ✅ Document any custom test data

### Production
- ❌ **NEVER run seeding scripts!**
- ❌ These scripts delete ALL data
- ❌ Use proper data migration instead

---

## Automation

### Add to package.json (if using Node)
```json
{
  "scripts": {
    "seed": "python3 seed_data.py",
    "seed:force": "python3 seed_force.py"
  }
}
```

### Add to Makefile
```makefile
seed:
	python3 seed_data.py

seed-force:
	python3 seed_force.py

reset: seed-force
	@echo "Database reset complete!"
```

### CI/CD Integration
```yaml
# .github/workflows/test.yml
- name: Seed test database
  run: python3 seed_force.py
```

---

## Quick Reference

| Command | Confirmation | Speed | Use Case |
|---------|-------------|-------|----------|
| `python3 seed_data.py` | Yes | Normal | Safe, first time |
| `python3 seed_force.py` | 3s countdown | Fast | Quick reset |
| `./seed.sh` | Menu choice | Normal | Guided |

---

## Summary

✅ **Interactive Mode**: Safe, asks confirmation
✅ **Force Mode**: Fast, 3-second countdown
✅ **Shell Script**: Guided, menu-driven
✅ **All modes**: Clear ALL data, insert fresh samples
✅ **Result**: 5 recruiters, 12 candidates, 12 jobs

**Remember**: All passwords are `password123` for testing!

---

For more details, see `TEST_DATA_REFERENCE.md`
