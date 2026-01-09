#!/usr/bin/env python3
"""
Project Verification Script
Checks if all required files and components are in place
"""

import os
import sys
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ MISSING {description}: {filepath}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ MISSING {description}: {dirpath}")
        return False

def count_files(pattern):
    """Count files matching pattern"""
    return len(list(Path('.').rglob(pattern)))

def main():
    print("=" * 60)
    print("Campus Hiring Platform - Project Verification")
    print("=" * 60)
    
    all_good = True
    
    # Check core directories
    print("\n📁 Checking Directories...")
    all_good &= check_directory("app", "App directory")
    all_good &= check_directory("app/models", "Models directory")
    all_good &= check_directory("app/routes", "Routes directory")
    all_good &= check_directory("app/ai", "AI directory")
    all_good &= check_directory("app/utils", "Utils directory")
    all_good &= check_directory("templates", "Templates directory")
    all_good &= check_directory("static", "Static directory")
    all_good &= check_directory("static/css", "CSS directory")
    all_good &= check_directory("static/js", "JS directory")
    all_good &= check_directory("uploads", "Uploads directory")
    
    # Check core Python files
    print("\n🐍 Checking Core Python Files...")
    all_good &= check_file("app/__init__.py", "App init")
    all_good &= check_file("app/main.py", "Main application")
    all_good &= check_file("app/config.py", "Configuration")
    all_good &= check_file("app/database.py", "Database")
    all_good &= check_file("app/celery_worker.py", "Celery worker")
    
    # Check models
    print("\n📊 Checking Models...")
    all_good &= check_file("app/models/__init__.py", "Models init")
    all_good &= check_file("app/models/user.py", "User model")
    all_good &= check_file("app/models/job.py", "Job model")
    all_good &= check_file("app/models/assessment.py", "Assessment model")
    all_good &= check_file("app/models/application.py", "Application model")
    all_good &= check_file("app/models/submission.py", "Submission model")
    all_good &= check_file("app/models/result.py", "Result model")
    
    # Check routes
    print("\n🛣️  Checking Routes...")
    all_good &= check_file("app/routes/__init__.py", "Routes init")
    all_good &= check_file("app/routes/auth.py", "Auth routes")
    all_good &= check_file("app/routes/jobs.py", "Jobs routes")
    all_good &= check_file("app/routes/assessments.py", "Assessments routes")
    all_good &= check_file("app/routes/applications.py", "Applications routes")
    all_good &= check_file("app/routes/submissions.py", "Submissions routes")
    all_good &= check_file("app/routes/results.py", "Results routes")
    
    # Check AI services
    print("\n🤖 Checking AI Services...")
    all_good &= check_file("app/ai/__init__.py", "AI init")
    all_good &= check_file("app/ai/gemini_service.py", "Gemini service")
    all_good &= check_file("app/ai/evaluation_service.py", "Evaluation service")
    
    # Check utilities
    print("\n🔧 Checking Utilities...")
    all_good &= check_file("app/utils/__init__.py", "Utils init")
    all_good &= check_file("app/utils/auth.py", "Auth utils")
    all_good &= check_file("app/utils/helpers.py", "Helper utils")
    
    # Check templates
    print("\n📄 Checking Templates...")
    all_good &= check_file("templates/base.html", "Base template")
    all_good &= check_file("templates/index.html", "Index template")
    all_good &= check_file("templates/login.html", "Login template")
    all_good &= check_file("templates/register.html", "Register template")
    all_good &= check_file("templates/dashboard.html", "Dashboard template")
    all_good &= check_file("templates/jobs.html", "Jobs template")
    all_good &= check_file("templates/job_detail.html", "Job detail template")
    all_good &= check_file("templates/assessment.html", "Assessment template")
    all_good &= check_file("templates/results.html", "Results template")
    all_good &= check_file("templates/recruiter_jobs.html", "Recruiter jobs template")
    all_good &= check_file("templates/recruiter_candidates.html", "Recruiter candidates template")
    
    # Check static files
    print("\n🎨 Checking Static Files...")
    all_good &= check_file("static/css/style.css", "Main stylesheet")
    all_good &= check_file("static/js/main.js", "Main JavaScript")
    
    # Check configuration files
    print("\n⚙️  Checking Configuration...")
    all_good &= check_file(".env.example", "Environment example")
    all_good &= check_file(".gitignore", "Git ignore")
    all_good &= check_file("requirements.txt", "Requirements")
    all_good &= check_file("Dockerfile", "Dockerfile")
    all_good &= check_file("docker-compose.yml", "Docker Compose")
    
    # Check scripts
    print("\n📜 Checking Scripts...")
    all_good &= check_file("setup.py", "Setup script")
    all_good &= check_file("run.sh", "Run script")
    all_good &= check_file("run_celery.sh", "Celery script")
    all_good &= check_file("Makefile", "Makefile")
    
    # Check documentation
    print("\n📚 Checking Documentation...")
    all_good &= check_file("README.md", "README")
    all_good &= check_file("QUICKSTART.md", "Quick start guide")
    all_good &= check_file("DEPLOYMENT.md", "Deployment guide")
    all_good &= check_file("PROJECT_STRUCTURE.md", "Project structure")
    all_good &= check_file("TESTING.md", "Testing guide")
    all_good &= check_file("PROJECT_SUMMARY.md", "Project summary")
    
    # Count files
    print("\n📊 File Statistics...")
    py_files = count_files("*.py")
    html_files = count_files("*.html")
    css_files = count_files("*.css")
    js_files = count_files("*.js")
    md_files = count_files("*.md")
    
    print(f"   Python files: {py_files}")
    print(f"   HTML files: {html_files}")
    print(f"   CSS files: {css_files}")
    print(f"   JavaScript files: {js_files}")
    print(f"   Markdown files: {md_files}")
    print(f"   Total: {py_files + html_files + css_files + js_files + md_files}")
    
    # Check if .env exists
    print("\n🔐 Environment Configuration...")
    if os.path.exists(".env"):
        print("✓ .env file exists")
        print("⚠️  Remember to set GOOGLE_API_KEY in .env")
    else:
        print("⚠️  .env file not found - run: cp .env.example .env")
        print("⚠️  Then set GOOGLE_API_KEY in .env")
    
    # Final summary
    print("\n" + "=" * 60)
    if all_good:
        print("✅ All required files are present!")
        print("=" * 60)
        print("\n🚀 Next Steps:")
        print("1. Copy .env.example to .env: cp .env.example .env")
        print("2. Edit .env and add your GOOGLE_API_KEY")
        print("3. Start with Docker: docker-compose up --build")
        print("   OR")
        print("   Start locally: ./run.sh (and ./run_celery.sh in another terminal)")
        print("\n📖 Read QUICKSTART.md for detailed instructions")
        return 0
    else:
        print("❌ Some files are missing!")
        print("=" * 60)
        print("\nPlease check the missing files above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
