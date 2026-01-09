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
        # Fallback models in case primary fails
        self.fallback_models = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-flash",
            "gemini-1.5-pro"
        ]
    
    async def generate_assessment(self, job_data: dict) -> dict:
        """Generate assessment questions based on job requirements"""
        
        is_technical = job_data.get('job_type') == 'technical'
        num_questions = 15 if is_technical else 13
        
        prompt = f"""You are an expert technical recruiter and assessment designer. Create a comprehensive assessment for the following job role.

Job Title: {job_data['title']}
Job Type: {job_data['job_type']}
Required Skills: {', '.join(job_data['required_skills'])}
Experience Level: {job_data['experience_level']}
Job Description: {job_data['description']}

Create exactly {num_questions} questions as follows:
- 10 MCQ questions (3 easy, 4 medium, 3 hard) - questions q1 to q10
{'- 2 coding problems (1 medium, 1 hard) - questions q11 to q12' if is_technical else ''}
- 3 situational/behavioral questions (medium difficulty) - questions q{'13' if is_technical else '11'} to q{num_questions}

CRITICAL: You MUST generate ALL {num_questions} questions. Do not skip any question.

For MCQ questions (q1-q10):
- question_id: "q1", "q2", "q3", etc.
- type: "mcq"
- question_text: The actual question
- difficulty: "easy", "medium", or "hard"
- points: 5 for easy, 7 for medium, 10 for hard
- options: Array of 4 options with option_id "a", "b", "c", "d"
- correct_option_id: The correct option
- skill_tags: Array of relevant skills
- ai_rationale: Why this question is important

For coding questions (q11-q12, only if technical):
- question_id: "q11", "q12"
- type: "coding"
- question_text: The coding problem description
- difficulty: "medium" or "hard"
- points: 15 for medium, 20 for hard
- test_cases: Array of 2-3 test cases with input and expected_output
- starter_code: Python code template
- language: "python"
- skill_tags: Array of relevant skills
- ai_rationale: Why this problem is important

For situational questions:
- question_id: "q{'13' if is_technical else '11'}", "q{'14' if is_technical else '12'}", "q{'15' if is_technical else '13'}"
- type: "situational"
- question_text: The situational question
- difficulty: "medium"
- points: 10
- skill_tags: Array of soft skills
- ai_rationale: What this assesses

Return ONLY valid JSON with NO markdown formatting, NO code blocks, NO explanations:
{{
    "questions": [
        // ALL {num_questions} questions here
    ],
    "total_points": 100,
    "estimated_duration": 60
}}

Start generating now. Remember: {num_questions} questions total."""
        
        # Try primary model first, then fallbacks
        models_to_try = [self.model] + [m for m in self.fallback_models if m != self.model]
        
        for model_name in models_to_try:
            try:
                logger.info(f"Generating assessment for {job_data['title']} using model: {model_name}")
                
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=8000,  # Increased for more questions
                    )
                )
                response_text = response.text
                
                logger.info(f"Received response of length: {len(response_text)}")
                
                # Clean response and parse JSON
                response_text = response_text.strip()
                
                # Remove markdown code blocks if present
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                elif response_text.startswith("```"):
                    response_text = response_text[3:]
                
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                
                response_text = response_text.strip()
                
                # Try to parse JSON
                result = json.loads(response_text)
                
                # Validate we got enough questions
                num_generated = len(result.get('questions', []))
                logger.info(f"Generated {num_generated} questions with {model_name}")
                
                if num_generated < 5:
                    logger.warning(f"Only got {num_generated} questions from {model_name}, trying next model...")
                    continue  # Try next model
                
                # Ensure total_points is set
                if 'total_points' not in result:
                    result['total_points'] = sum(q.get('points', 5) for q in result['questions'])
                
                # Ensure estimated_duration is set
                if 'estimated_duration' not in result:
                    result['estimated_duration'] = 60
                
                logger.info(f"Successfully generated assessment with {num_generated} questions using {model_name}")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error with {model_name}: {e}")
                if 'response_text' in locals():
                    logger.error(f"Response text: {response_text[:500]}...")
                continue  # Try next model
            except Exception as e:
                logger.error(f"Error with {model_name}: {e}")
                continue  # Try next model
        
        # If all models failed, use comprehensive fallback
        logger.warning("All AI models failed, using comprehensive fallback assessment")
        return self._get_comprehensive_fallback_assessment(job_data)
    
    def _get_fallback_assessment(self, job_data: dict) -> dict:
        """Simple fallback assessment if AI generation fails"""
        logger.warning("Using simple fallback assessment")
        return self._get_comprehensive_fallback_assessment(job_data)
    
    def _get_comprehensive_fallback_assessment(self, job_data: dict) -> dict:
        """Comprehensive fallback assessment with multiple questions"""
        is_technical = job_data.get('job_type') == 'technical'
        skills = job_data.get('required_skills', ['General Skills'])
        
        questions = []
        
        # MCQ Questions (10 questions)
        mcq_questions = [
            {
                "question_id": "q1",
                "type": "mcq",
                "question_text": f"What is your experience level with {skills[0] if skills else 'this technology'}?",
                "difficulty": "easy",
                "points": 5,
                "options": [
                    {"option_id": "a", "text": "No experience"},
                    {"option_id": "b", "text": "Basic knowledge"},
                    {"option_id": "c", "text": "Intermediate"},
                    {"option_id": "d", "text": "Expert"}
                ],
                "correct_option_id": "c",
                "skill_tags": skills[:2],
                "ai_rationale": "Assessing baseline knowledge"
            },
            {
                "question_id": "q2",
                "type": "mcq",
                "question_text": "How many years of professional experience do you have?",
                "difficulty": "easy",
                "points": 5,
                "options": [
                    {"option_id": "a", "text": "Less than 1 year"},
                    {"option_id": "b", "text": "1-2 years"},
                    {"option_id": "c", "text": "3-5 years"},
                    {"option_id": "d", "text": "More than 5 years"}
                ],
                "correct_option_id": "a",
                "skill_tags": ["Experience"],
                "ai_rationale": "Understanding experience level"
            },
            {
                "question_id": "q3",
                "type": "mcq",
                "question_text": "Which best describes your learning approach?",
                "difficulty": "easy",
                "points": 5,
                "options": [
                    {"option_id": "a", "text": "Self-taught through online resources"},
                    {"option_id": "b", "text": "Formal education and courses"},
                    {"option_id": "c", "text": "On-the-job training"},
                    {"option_id": "d", "text": "Combination of all above"}
                ],
                "correct_option_id": "d",
                "skill_tags": ["Learning"],
                "ai_rationale": "Assessing learning mindset"
            },
            {
                "question_id": "q4",
                "type": "mcq",
                "question_text": f"What is the primary use case for {skills[0] if skills else 'this technology'}?",
                "difficulty": "medium",
                "points": 7,
                "options": [
                    {"option_id": "a", "text": "Web development"},
                    {"option_id": "b", "text": "Data analysis"},
                    {"option_id": "c", "text": "Mobile development"},
                    {"option_id": "d", "text": "All of the above"}
                ],
                "correct_option_id": "d",
                "skill_tags": skills[:2],
                "ai_rationale": "Testing practical knowledge"
            },
            {
                "question_id": "q5",
                "type": "mcq",
                "question_text": "How do you stay updated with technology trends?",
                "difficulty": "medium",
                "points": 7,
                "options": [
                    {"option_id": "a", "text": "Reading blogs and articles"},
                    {"option_id": "b", "text": "Attending conferences"},
                    {"option_id": "c", "text": "Online courses and tutorials"},
                    {"option_id": "d", "text": "All of the above"}
                ],
                "correct_option_id": "d",
                "skill_tags": ["Continuous Learning"],
                "ai_rationale": "Assessing growth mindset"
            },
            {
                "question_id": "q6",
                "type": "mcq",
                "question_text": "What is your preferred development methodology?",
                "difficulty": "medium",
                "points": 7,
                "options": [
                    {"option_id": "a", "text": "Agile/Scrum"},
                    {"option_id": "b", "text": "Waterfall"},
                    {"option_id": "c", "text": "Kanban"},
                    {"option_id": "d", "text": "Flexible based on project"}
                ],
                "correct_option_id": "d",
                "skill_tags": ["Methodology"],
                "ai_rationale": "Understanding work approach"
            },
            {
                "question_id": "q7",
                "type": "mcq",
                "question_text": "How do you handle tight deadlines?",
                "difficulty": "medium",
                "points": 7,
                "options": [
                    {"option_id": "a", "text": "Prioritize tasks and focus on critical items"},
                    {"option_id": "b", "text": "Work longer hours"},
                    {"option_id": "c", "text": "Ask for help from team"},
                    {"option_id": "d", "text": "All of the above"}
                ],
                "correct_option_id": "d",
                "skill_tags": ["Time Management"],
                "ai_rationale": "Assessing pressure handling"
            },
            {
                "question_id": "q8",
                "type": "mcq",
                "question_text": "What is your approach to debugging?",
                "difficulty": "hard",
                "points": 10,
                "options": [
                    {"option_id": "a", "text": "Use print statements"},
                    {"option_id": "b", "text": "Use debugging tools"},
                    {"option_id": "c", "text": "Review code systematically"},
                    {"option_id": "d", "text": "Combination of methods"}
                ],
                "correct_option_id": "d",
                "skill_tags": ["Problem Solving"],
                "ai_rationale": "Testing debugging skills"
            },
            {
                "question_id": "q9",
                "type": "mcq",
                "question_text": "How do you ensure code quality?",
                "difficulty": "hard",
                "points": 10,
                "options": [
                    {"option_id": "a", "text": "Write unit tests"},
                    {"option_id": "b", "text": "Code reviews"},
                    {"option_id": "c", "text": "Follow coding standards"},
                    {"option_id": "d", "text": "All of the above"}
                ],
                "correct_option_id": "d",
                "skill_tags": ["Code Quality"],
                "ai_rationale": "Assessing quality mindset"
            },
            {
                "question_id": "q10",
                "type": "mcq",
                "question_text": "What is your experience with version control?",
                "difficulty": "hard",
                "points": 10,
                "options": [
                    {"option_id": "a", "text": "Basic Git commands"},
                    {"option_id": "b", "text": "Branching and merging"},
                    {"option_id": "c", "text": "Advanced workflows"},
                    {"option_id": "d", "text": "Expert level"}
                ],
                "correct_option_id": "c",
                "skill_tags": ["Version Control"],
                "ai_rationale": "Testing collaboration skills"
            }
        ]
        
        questions.extend(mcq_questions)
        
        # Coding Questions (only for technical roles)
        if is_technical:
            coding_questions = [
                {
                    "question_id": "q11",
                    "type": "coding",
                    "question_text": "Write a function to reverse a string without using built-in reverse methods.",
                    "difficulty": "medium",
                    "points": 15,
                    "test_cases": [
                        {"input": "hello", "expected_output": "olleh", "is_hidden": False},
                        {"input": "world", "expected_output": "dlrow", "is_hidden": False},
                        {"input": "python", "expected_output": "nohtyp", "is_hidden": True}
                    ],
                    "starter_code": "def reverse_string(s):\n    # Write your code here\n    pass",
                    "language": "python",
                    "skill_tags": skills[:2],
                    "ai_rationale": "Testing basic programming logic"
                },
                {
                    "question_id": "q12",
                    "type": "coding",
                    "question_text": "Write a function to find the sum of all even numbers in a list.",
                    "difficulty": "hard",
                    "points": 20,
                    "test_cases": [
                        {"input": "[1, 2, 3, 4, 5, 6]", "expected_output": "12", "is_hidden": False},
                        {"input": "[10, 15, 20, 25]", "expected_output": "30", "is_hidden": False},
                        {"input": "[1, 3, 5, 7]", "expected_output": "0", "is_hidden": True}
                    ],
                    "starter_code": "def sum_even_numbers(numbers):\n    # Write your code here\n    pass",
                    "language": "python",
                    "skill_tags": skills[:2],
                    "ai_rationale": "Testing problem-solving ability"
                }
            ]
            questions.extend(coding_questions)
        
        # Situational Questions (3 questions)
        situational_start = 13 if is_technical else 11
        situational_questions = [
            {
                "question_id": f"q{situational_start}",
                "type": "situational",
                "question_text": "Describe a challenging project you worked on and how you overcame the obstacles.",
                "difficulty": "medium",
                "points": 10,
                "skill_tags": ["Problem Solving", "Communication"],
                "ai_rationale": "Assessing problem-solving and communication"
            },
            {
                "question_id": f"q{situational_start + 1}",
                "type": "situational",
                "question_text": "How do you handle disagreements with team members about technical decisions?",
                "difficulty": "medium",
                "points": 10,
                "skill_tags": ["Teamwork", "Communication"],
                "ai_rationale": "Testing collaboration skills"
            },
            {
                "question_id": f"q{situational_start + 2}",
                "type": "situational",
                "question_text": "Tell us about a time when you had to learn a new technology quickly. How did you approach it?",
                "difficulty": "medium",
                "points": 10,
                "skill_tags": ["Learning Agility", "Adaptability"],
                "ai_rationale": "Assessing learning ability"
            }
        ]
        questions.extend(situational_questions)
        
        total_points = sum(q['points'] for q in questions)
        
        return {
            "questions": questions,
            "total_points": total_points,
            "estimated_duration": 60
        }


gemini_service = GeminiService()
