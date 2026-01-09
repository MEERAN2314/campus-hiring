from celery import Celery
from app.config import settings
from app.ai.evaluation_service import evaluation_service
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.assessment import QuestionType
from app.utils.helpers import calculate_percentage
import asyncio
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery(
    "campus_hiring",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


def get_db():
    """Get database connection for Celery tasks"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    return client[settings.MONGODB_DB_NAME]


@celery_app.task(name="evaluate_submission")
def evaluate_submission_task(submission_id: str):
    """Async task to evaluate a submission"""
    return asyncio.run(evaluate_submission(submission_id))


async def evaluate_submission(submission_id: str):
    """Evaluate submission with AI"""
    db = get_db()
    
    try:
        # Get submission
        submission = await db.submissions.find_one({"_id": submission_id})
        if not submission:
            logger.error(f"Submission {submission_id} not found")
            return {"error": "Submission not found"}
        
        # Get assessment
        assessment = await db.assessments.find_one({"_id": submission["assessment_id"]})
        if not assessment:
            logger.error(f"Assessment {submission['assessment_id']} not found")
            return {"error": "Assessment not found"}
        
        # Get application
        application = await db.applications.find_one({"_id": submission["application_id"]})
        if not application:
            logger.error(f"Application {submission['application_id']} not found")
            return {"error": "Application not found"}
        
        # Get job
        job = await db.jobs.find_one({"_id": application["job_id"]})
        
        # Evaluate each answer
        question_evaluations = []
        total_score = 0
        skill_scores_dict = {}
        
        for answer in submission["answers"]:
            # Find corresponding question
            question = next(
                (q for q in assessment["questions"] if q["question_id"] == answer["question_id"]),
                None
            )
            
            if not question:
                continue
            
            evaluation = await evaluate_answer(question, answer)
            question_evaluations.append(evaluation)
            
            total_score += evaluation["points_earned"]
            
            # Aggregate skill scores
            for skill in question.get("skill_tags", []):
                if skill not in skill_scores_dict:
                    skill_scores_dict[skill] = {"total": 0, "count": 0, "max": 0}
                skill_scores_dict[skill]["total"] += evaluation["points_earned"]
                skill_scores_dict[skill]["count"] += 1
                skill_scores_dict[skill]["max"] += question["points"]
        
        # Calculate skill scores
        skill_scores = []
        for skill, data in skill_scores_dict.items():
            score = (data["total"] / data["max"] * 100) if data["max"] > 0 else 0
            level = "advanced" if score >= 80 else "intermediate" if score >= 60 else "beginner"
            skill_scores.append({
                "skill_name": skill,
                "score": round(score, 2),
                "level": level,
                "feedback": f"Scored {round(score, 2)}% in {skill}"
            })
        
        # Calculate overall metrics
        max_score = assessment["config"]["total_points"]
        percentage = calculate_percentage(total_score, max_score)
        
        # Generate AI reasoning
        candidate_data = {
            "name": application["candidate_name"],
            "job_title": job["title"] if job else "Position"
        }
        
        results_data = {
            "percentage": percentage,
            "skill_scores": skill_scores,
            "question_feedback": [
                {
                    "question": q["question_text"],
                    "feedback": e["ai_feedback"]
                }
                for q, e in zip(assessment["questions"], question_evaluations)
            ]
        }
        
        # Get all candidates for ranking context
        all_applications = await db.applications.find({"job_id": application["job_id"]}).to_list(None)
        
        ai_reasoning = await evaluation_service.generate_ai_reasoning(
            candidate_data,
            results_data,
            all_applications
        )
        
        # Generate feedback report
        feedback_report = await evaluation_service.generate_overall_feedback(
            candidate_data,
            results_data
        )
        
        # Create result document
        result = {
            "_id": f"result_{submission_id}",
            "submission_id": submission_id,
            "application_id": submission["application_id"],
            "candidate_id": submission["candidate_id"],
            "assessment_id": submission["assessment_id"],
            "total_score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "question_evaluations": question_evaluations,
            "ai_reasoning": ai_reasoning,
            "feedback_report": {
                **feedback_report,
                "overall_score": percentage,
                "skill_scores": skill_scores,
                "percentile": None  # Will be calculated after all submissions
            },
            "is_shortlisted": False,
            "evaluated_at": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        
        # Save result
        await db.results.insert_one(result)
        
        # Update application status
        await db.applications.update_one(
            {"_id": submission["application_id"]},
            {
                "$set": {
                    "status": "under_review",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        logger.info(f"Successfully evaluated submission {submission_id}")
        return {"success": True, "result_id": result["_id"]}
        
    except Exception as e:
        logger.error(f"Error evaluating submission {submission_id}: {e}")
        return {"error": str(e)}


async def evaluate_answer(question: dict, answer: dict) -> dict:
    """Evaluate a single answer"""
    question_type = question["type"]
    
    if question_type == QuestionType.MCQ.value:
        # MCQ evaluation
        is_correct = answer.get("selected_option_id") == question.get("correct_option_id")
        points_earned = question["points"] if is_correct else 0
        
        return {
            "question_id": question["question_id"],
            "question_type": question_type,
            "points_earned": points_earned,
            "max_points": question["points"],
            "is_correct": is_correct,
            "ai_feedback": "Correct answer!" if is_correct else "Incorrect. Review this topic.",
            "strengths": ["Quick response"] if is_correct else [],
            "improvements": [] if is_correct else ["Review the concept"]
        }
    
    elif question_type == QuestionType.CODING.value:
        # AI code evaluation
        eval_result = await evaluation_service.evaluate_code(question, answer)
        
        # Calculate points based on AI scores
        correctness_weight = 0.4
        efficiency_weight = 0.3
        readability_weight = 0.2
        edge_case_weight = 0.1
        
        weighted_score = (
            eval_result["correctness_score"] * correctness_weight +
            eval_result["efficiency_score"] * efficiency_weight +
            eval_result["readability_score"] * readability_weight +
            eval_result["edge_case_score"] * edge_case_weight
        )
        
        points_earned = (weighted_score / 100) * question["points"]
        
        return {
            "question_id": question["question_id"],
            "question_type": question_type,
            "points_earned": round(points_earned, 2),
            "max_points": question["points"],
            "is_correct": eval_result["is_correct"],
            "correctness_score": eval_result["correctness_score"],
            "efficiency_score": eval_result["efficiency_score"],
            "readability_score": eval_result["readability_score"],
            "ai_feedback": eval_result["detailed_feedback"],
            "strengths": eval_result["strengths"],
            "improvements": eval_result["improvements"]
        }
    
    else:
        # Descriptive/Situational evaluation
        eval_result = await evaluation_service.evaluate_descriptive(question, answer)
        
        weighted_score = (
            eval_result["relevance_score"] * 0.3 +
            eval_result["communication_score"] * 0.3 +
            eval_result["critical_thinking_score"] * 0.25 +
            eval_result["professionalism_score"] * 0.15
        )
        
        points_earned = (weighted_score / 100) * question["points"]
        
        return {
            "question_id": question["question_id"],
            "question_type": question_type,
            "points_earned": round(points_earned, 2),
            "max_points": question["points"],
            "is_correct": weighted_score >= 60,
            "ai_feedback": eval_result["detailed_feedback"],
            "strengths": eval_result["strengths"],
            "improvements": eval_result["improvements"]
        }
