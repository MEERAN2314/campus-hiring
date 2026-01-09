from google import genai
from google.genai import types
from app.config import settings
import json
import logging

logger = logging.getLogger(__name__)

# Configure Gemini client
client = None
if settings.GOOGLE_API_KEY:
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)


class GeminiService:
    def __init__(self):
        self.client = client
        self.model = settings.GEMINI_MODEL
    
    async def generate_assessment(self, job_data: dict) -> dict:
        """Generate assessment questions based on job requirements"""
        
        is_technical = job_data.get('job_type') == 'technical'
        
        prompt = f"""You are an expert technical recruiter and assessment designer. Create a comprehensive assessment for the following job role.

Job Title: {job_data['title']}
Job Type: {job_data['job_type']}
Required Skills: {', '.join(job_data['required_skills'])}
Experience Level: {job_data['experience_level']}
Job Description: {job_data['description']}

Create exactly {'15 questions' if is_technical else '13 questions'} as follows:
- 10 MCQ questions (3 easy, 4 medium, 3 hard)
{'- 2 coding problems (1 medium, 1 hard)' if is_technical else ''}
- 3 situational/behavioral questions (medium difficulty)

IMPORTANT: Generate ALL questions. Do not skip any.

For MCQ questions:
- question_id: "q1", "q2", etc.
- type: "mcq"
- 4 options with option_id: "a", "b", "c", "d"
- Specify correct_option_id

For coding questions (if technical):
- question_id: "q11", "q12"
- type: "coding"
- Include 2-3 test cases
- Provide starter_code in Python
- language: "python"

For situational questions:
- question_id: "q13", "q14", "q15" (or "q11", "q12", "q13" for non-technical)
- type: "situational"

Return ONLY valid JSON (no markdown, no explanation):
{{
    "questions": [
        {{
            "question_id": "q1",
            "type": "mcq",
            "question_text": "What is the primary purpose of Python's GIL (Global Interpreter Lock)?",
            "difficulty": "easy",
            "points": 5,
            "options": [
                {{"option_id": "a", "text": "To prevent memory leaks"}},
                {{"option_id": "b", "text": "To ensure thread safety"}},
                {{"option_id": "c", "text": "To improve performance"}},
                {{"option_id": "d", "text": "To manage garbage collection"}}
            ],
            "correct_option_id": "b",
            "skill_tags": ["Python", "Concurrency"],
            "ai_rationale": "Tests understanding of Python internals"
        }}
    ],
    "total_points": 100,
    "estimated_duration": 60
}}

Generate ALL {15 if is_technical else 13} questions now."""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            response_text = response.text
            
            # Clean response and parse JSON
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            result = json.loads(response_text)
            
            # Validate we got enough questions
            if len(result.get('questions', [])) < 5:
                logger.warning(f"Only got {len(result.get('questions', []))} questions, using fallback")
                return self._get_fallback_assessment(job_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating assessment: {e}")
            # Return fallback assessment
            return self._get_fallback_assessment(job_data)
    
    def _get_fallback_assessment(self, job_data: dict) -> dict:
        """Fallback assessment if AI generation fails"""
        return {
            "questions": [
                {
                    "question_id": "q1",
                    "type": "mcq",
                    "question_text": f"What is your experience with {job_data['required_skills'][0] if job_data['required_skills'] else 'this technology'}?",
                    "difficulty": "easy",
                    "points": 5,
                    "options": [
                        {"option_id": "a", "text": "No experience"},
                        {"option_id": "b", "text": "Basic knowledge"},
                        {"option_id": "c", "text": "Intermediate"},
                        {"option_id": "d", "text": "Expert"}
                    ],
                    "correct_option_id": "c",
                    "skill_tags": job_data['required_skills'][:2],
                    "ai_rationale": "Assessing baseline knowledge"
                }
            ],
            "total_points": 100,
            "estimated_duration": 60
        }


gemini_service = GeminiService()
