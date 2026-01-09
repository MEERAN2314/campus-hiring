from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import settings
import json
import logging

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )
    
    async def generate_assessment(self, job_data: dict) -> dict:
        """Generate assessment questions based on job requirements"""
        
        prompt = PromptTemplate(
            input_variables=["job_title", "job_type", "skills", "experience_level", "description"],
            template="""You are an expert technical recruiter and assessment designer. Create a comprehensive assessment for the following job role.

Job Title: {job_title}
Job Type: {job_type}
Required Skills: {skills}
Experience Level: {experience_level}
Job Description: {description}

Generate a balanced assessment with:
- 10 MCQ questions (mix of easy, medium, hard)
- 2 coding problems (1 medium, 1 hard) if technical role
- 3 situational/behavioral questions

For each question, provide:
1. Question text
2. Difficulty level
3. Points (easy=5, medium=10, hard=15)
4. For MCQ: 4 options with correct answer
5. For coding: test cases and starter code
6. Skill tags
7. Rationale for why this question is relevant

Return ONLY valid JSON in this exact format:
{{
    "questions": [
        {{
            "question_id": "q1",
            "type": "mcq",
            "question_text": "...",
            "difficulty": "easy",
            "points": 5,
            "options": [
                {{"option_id": "a", "text": "..."}},
                {{"option_id": "b", "text": "..."}},
                {{"option_id": "c", "text": "..."}},
                {{"option_id": "d", "text": "..."}}
            ],
            "correct_option_id": "a",
            "skill_tags": ["skill1", "skill2"],
            "ai_rationale": "..."
        }},
        {{
            "question_id": "q2",
            "type": "coding",
            "question_text": "...",
            "difficulty": "medium",
            "points": 10,
            "test_cases": [
                {{"input": "...", "expected_output": "...", "is_hidden": false}}
            ],
            "starter_code": "def solution():\\n    pass",
            "language": "python",
            "skill_tags": ["skill1"],
            "ai_rationale": "..."
        }}
    ],
    "total_points": 100,
    "estimated_duration": 60
}}
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = await chain.arun(
                job_title=job_data["title"],
                job_type=job_data["job_type"],
                skills=", ".join(job_data["required_skills"]),
                experience_level=job_data["experience_level"],
                description=job_data["description"]
            )
            
            # Clean response and parse JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            result = json.loads(response)
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
