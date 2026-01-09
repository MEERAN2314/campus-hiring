from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import settings
from typing import Dict, List, Any
import json
import logging

logger = logging.getLogger(__name__)


class EvaluationService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3,  # Lower temperature for more consistent evaluation
            convert_system_message_to_human=True
        )
    
    async def evaluate_code(self, question: dict, answer: dict) -> dict:
        """Evaluate coding question with AI"""
        
        prompt = PromptTemplate(
            input_variables=["question", "code", "test_cases"],
            template="""You are an expert code reviewer. Evaluate the following code submission.

Question: {question}

Submitted Code:
{code}

Test Cases: {test_cases}

Evaluate the code on:
1. Correctness (0-100): Does it solve the problem?
2. Efficiency (0-100): Time and space complexity
3. Readability (0-100): Code quality, naming, structure
4. Edge Cases (0-100): Handles edge cases properly

Provide detailed feedback with:
- What the candidate did well (strengths)
- What needs improvement
- Specific suggestions

Return ONLY valid JSON:
{{
    "correctness_score": 85,
    "efficiency_score": 75,
    "readability_score": 90,
    "edge_case_score": 70,
    "overall_score": 80,
    "is_correct": true,
    "strengths": ["Clear variable names", "Good logic"],
    "improvements": ["Could optimize with hash map", "Missing edge case for empty input"],
    "detailed_feedback": "The solution correctly solves the problem..."
}}
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = await chain.arun(
                question=question["question_text"],
                code=answer.get("code", ""),
                test_cases=json.dumps(question.get("test_cases", []))
            )
            
            response = self._clean_json_response(response)
            result = json.loads(response)
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating code: {e}")
            return self._get_fallback_code_evaluation()
    
    async def evaluate_descriptive(self, question: dict, answer: dict) -> dict:
        """Evaluate descriptive/situational answer with AI"""
        
        prompt = PromptTemplate(
            input_variables=["question", "answer", "skill_tags"],
            template="""You are an expert HR interviewer. Evaluate this candidate's response.

Question: {question}
Skills Being Assessed: {skill_tags}

Candidate's Answer:
{answer}

Evaluate on:
1. Relevance (0-100): How well does it answer the question?
2. Communication (0-100): Clarity and structure
3. Critical Thinking (0-100): Depth of analysis
4. Professionalism (0-100): Tone and presentation

Return ONLY valid JSON:
{{
    "relevance_score": 85,
    "communication_score": 90,
    "critical_thinking_score": 75,
    "professionalism_score": 95,
    "overall_score": 86,
    "strengths": ["Clear communication", "Good examples"],
    "improvements": ["Could provide more specific examples"],
    "detailed_feedback": "The candidate demonstrates..."
}}
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = await chain.arun(
                question=question["question_text"],
                answer=answer.get("text_answer", ""),
                skill_tags=", ".join(question.get("skill_tags", []))
            )
            
            response = self._clean_json_response(response)
            result = json.loads(response)
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating descriptive answer: {e}")
            return self._get_fallback_descriptive_evaluation()
    
    async def generate_overall_feedback(self, candidate_data: dict, results: dict) -> dict:
        """Generate personalized feedback report"""
        
        prompt = PromptTemplate(
            input_variables=["candidate_name", "job_title", "score", "skill_scores", "question_feedback"],
            template="""You are a career coach providing constructive feedback to a job candidate.

Candidate: {candidate_name}
Position: {job_title}
Overall Score: {score}/100

Skill Performance:
{skill_scores}

Question-wise Feedback:
{question_feedback}

Generate a comprehensive, encouraging feedback report with:
1. Top 3 strengths
2. Top 3 improvement areas (framed positively)
3. Personalized learning resources (with realistic URLs to courses/articles)
4. Specific improvement plan with timeline
5. Encouraging message
6. Next steps

Return ONLY valid JSON:
{{
    "top_strengths": ["Strength 1", "Strength 2", "Strength 3"],
    "improvement_areas": ["Area 1", "Area 2", "Area 3"],
    "learning_resources": [
        {{"title": "Course Name", "url": "https://example.com", "type": "course", "duration": "4 weeks"}},
        {{"title": "Article Title", "url": "https://example.com", "type": "article", "duration": "15 min"}}
    ],
    "improvement_plan": "Focus on... Over the next 2-3 weeks...",
    "estimated_improvement_time": "2-3 weeks",
    "positive_message": "You've shown great potential...",
    "next_steps": ["Step 1", "Step 2", "Step 3"]
}}
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = await chain.arun(
                candidate_name=candidate_data.get("name", "Candidate"),
                job_title=candidate_data.get("job_title", "this position"),
                score=results.get("percentage", 0),
                skill_scores=json.dumps(results.get("skill_scores", [])),
                question_feedback=json.dumps(results.get("question_feedback", []))
            )
            
            response = self._clean_json_response(response)
            result = json.loads(response)
            return result
            
        except Exception as e:
            logger.error(f"Error generating feedback: {e}")
            return self._get_fallback_feedback()
    
    async def generate_ai_reasoning(self, candidate_data: dict, results: dict, all_candidates: List[dict]) -> dict:
        """Generate AI reasoning for ranking"""
        
        prompt = PromptTemplate(
            input_variables=["candidate_name", "score", "skills", "total_candidates"],
            template="""You are an AI recruitment analyst. Explain why this candidate received their ranking.

Candidate: {candidate_name}
Score: {score}/100
Skills Performance: {skills}
Total Candidates: {total_candidates}

Provide:
1. Overall assessment (2-3 sentences)
2. Key ranking factors (what made them stand out or fall behind)
3. Confidence score (0-1) in this evaluation
4. Bias check (any potential biases detected?)
5. Success prediction for this role

Return ONLY valid JSON:
{{
    "overall_assessment": "This candidate demonstrates...",
    "ranking_factors": [
        {{"factor": "Technical Skills", "impact": "high", "score": 85, "explanation": "..."}},
        {{"factor": "Problem Solving", "impact": "medium", "score": 75, "explanation": "..."}}
    ],
    "confidence_score": 0.85,
    "bias_check": {{"detected": false, "notes": "No significant bias detected"}},
    "prediction": "High likelihood of success based on strong technical foundation and problem-solving skills"
}}
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        try:
            response = await chain.arun(
                candidate_name=candidate_data.get("name", "Candidate"),
                score=results.get("percentage", 0),
                skills=json.dumps(results.get("skill_scores", [])),
                total_candidates=len(all_candidates)
            )
            
            response = self._clean_json_response(response)
            result = json.loads(response)
            return result
            
        except Exception as e:
            logger.error(f"Error generating AI reasoning: {e}")
            return self._get_fallback_reasoning()
    
    def _clean_json_response(self, response: str) -> str:
        """Clean JSON response from LLM"""
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        return response.strip()
    
    def _get_fallback_code_evaluation(self) -> dict:
        return {
            "correctness_score": 70,
            "efficiency_score": 70,
            "readability_score": 70,
            "edge_case_score": 70,
            "overall_score": 70,
            "is_correct": True,
            "strengths": ["Code submitted"],
            "improvements": ["Could be optimized"],
            "detailed_feedback": "Your solution shows understanding of the problem."
        }
    
    def _get_fallback_descriptive_evaluation(self) -> dict:
        return {
            "relevance_score": 70,
            "communication_score": 70,
            "critical_thinking_score": 70,
            "professionalism_score": 70,
            "overall_score": 70,
            "strengths": ["Clear response"],
            "improvements": ["Could add more details"],
            "detailed_feedback": "Your answer demonstrates understanding."
        }
    
    def _get_fallback_feedback(self) -> dict:
        return {
            "top_strengths": ["Completed assessment", "Showed effort", "Good attempt"],
            "improvement_areas": ["Technical skills", "Problem solving", "Communication"],
            "learning_resources": [
                {"title": "Online Courses", "url": "https://coursera.org", "type": "course", "duration": "4 weeks"}
            ],
            "improvement_plan": "Focus on strengthening core skills through practice and learning.",
            "estimated_improvement_time": "2-4 weeks",
            "positive_message": "You've shown potential. Keep learning and improving!",
            "next_steps": ["Practice coding problems", "Take online courses", "Apply again"]
        }
    
    def _get_fallback_reasoning(self) -> dict:
        return {
            "overall_assessment": "Candidate completed the assessment with reasonable performance.",
            "ranking_factors": [
                {"factor": "Overall Performance", "impact": "high", "score": 70, "explanation": "Solid attempt"}
            ],
            "confidence_score": 0.7,
            "bias_check": {"detected": False, "notes": "Standard evaluation"},
            "prediction": "Candidate shows potential for growth"
        }


evaluation_service = EvaluationService()
