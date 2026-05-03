import logging
import os
import json
from typing import List, Dict, Any, Optional
import openai

logger = logging.getLogger(__name__)


class LLMService:
    """Handles LLM interactions for structured response generation."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize LLM service.
        
        Args:
            model_name: Name of OpenAI model to use.
        """
        self.model_name = model_name
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize OpenAI client with environment variables."""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                logger.warning("OPENAI_API_KEY environment variable not found")
                self.client = None
                return
            
            self.client = openai.OpenAI(api_key=api_key)
            logger.info(f"OpenAI client initialized with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            self.client = None
    
    def generate_structured_response(self, query: str, context_schemes: List[Dict[str, Any]], 
                              user_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate structured response using LLM with retrieved context.
        
        Args:
            query: User's search query.
            context_schemes: List of relevant schemes from RAG.
            user_profile: Optional user profile information.
            
        Returns:
            Structured response with scheme recommendations.
        """
        try:
            if not self.client:
                logger.error("OpenAI client not initialized")
                return self._get_fallback_response(query)
            
            # Create context from retrieved schemes
            context_text = self._create_context_text(context_schemes)
            
            # Create system prompt
            system_prompt = self._create_system_prompt()
            
            # Create user prompt with context and query
            user_prompt = self._create_user_prompt(query, context_text, user_profile)
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000,
                response_format={"type": "json_object"}
            )
            
            # Parse structured response
            content = response.choices[0].message.content
            
            try:
                structured_response = json.loads(content)
                logger.info(f"Generated structured LLM response")
                return structured_response
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse LLM response as JSON: {e}")
                return self._get_fallback_response(query)
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return self._get_fallback_response(query)
    
    def _create_context_text(self, context_schemes: List[Dict[str, Any]]) -> str:
        """
        Create context text from retrieved schemes.
        
        Args:
            context_schemes: List of scheme dictionaries.
            
        Returns:
            Formatted context text.
        """
        if not context_schemes:
            return "No specific schemes found in the database."
        
        context_parts = []
        for i, scheme in enumerate(context_schemes[:5]):  # Limit to top 5 for context
            context_parts.append(f"""
Scheme {i+1}: {scheme.get('scheme_name', 'Unknown')}
- Category: {scheme.get('category', 'N/A')}
- State: {scheme.get('state', 'N/A')}
- Description: {scheme.get('description', 'N/A')[:200]}...
- Benefits: {scheme.get('benefits', 'N/A')[:150]}...
- Eligibility: {', '.join(scheme.get('eligibility_criteria', []))[:200]}...
- Income Limit: ₹{scheme.get('income_limit', 'N/A'):,} per year
- Application: {scheme.get('application_process', 'N/A')[:200]}...
            """)
        
        return "\n".join(context_parts)
    
    def _create_system_prompt(self) -> str:
        """
        Create system prompt for the LLM.
        
        Returns:
            System prompt string.
        """
        return """You are a helpful government scheme advisor assistant. Your task is to analyze the provided context about government schemes and user query to generate personalized recommendations.

Rules:
1. Use ONLY the information provided in the context
2. Do not hallucinate or make up information not present in the context
3. Focus on eligibility criteria, benefits, and application process
4. Generate structured JSON response with the exact format specified
5. If information is insufficient, clearly state what additional details are needed
6. Be concise but comprehensive
7. Always prioritize schemes that best match the user's needs
8. Include confidence scores based on relevance to query

Response Format:
{
  "schemes": [
    {
      "name": "exact scheme name from context",
      "why_eligible": "clear explanation of eligibility",
      "benefits": "key benefits from context",
      "how_to_apply": "step-by-step application process",
      "documents": ["document1", "document2"],
      "confidence_score": 0.85
    }
  ]
}"""
    
    def _create_user_prompt(self, query: str, context_text: str, 
                        user_profile: Optional[Dict[str, Any]]) -> str:
        """
        Create user prompt with context and query.
        
        Args:
            query: User's search query.
            context_text: Context from retrieved schemes.
            user_profile: Optional user profile.
            
        Returns:
            User prompt string.
        """
        profile_text = ""
        if user_profile:
            profile_parts = []
            if user_profile.get('age'):
                profile_parts.append(f"Age: {user_profile['age']}")
            if user_profile.get('income'):
                profile_parts.append(f"Income: ₹{user_profile['income']:,}")
            if user_profile.get('state'):
                profile_parts.append(f"State: {user_profile['state']}")
            if user_profile.get('occupation'):
                profile_parts.append(f"Occupation: {user_profile['occupation']}")
            if user_profile.get('education'):
                profile_parts.append(f"Education: {user_profile['education']}")
            
            profile_text = "\nUser Profile:\n" + "\n".join(profile_parts) if profile_parts else ""
        
        return f"""Query: {query}

{profile_text}

Context Information:
{context_text}

Based on the context and user information, please provide personalized scheme recommendations in the specified JSON format. Focus on schemes that best match the user's query and profile."""
    
    def _get_fallback_response(self, query: str) -> Dict[str, Any]:
        """
        Get fallback response when LLM is unavailable.
        
        Args:
            query: User's query.
            
        Returns:
            Fallback structured response.
        """
        return {
            "schemes": [
                {
                    "name": "National Scholarship Portal",
                    "why_eligible": "Students with good academic records and meeting income criteria can apply for various scholarships",
                    "benefits": "Financial assistance for education covering tuition fees and maintenance allowances",
                    "how_to_apply": "Register on scholarships.gov.in, select relevant schemes, and submit applications with required documents",
                    "documents": ["Aadhaar card", "Mark sheets", "Income certificate", "Bank account details"],
                    "confidence_score": 0.75
                }
            ],
            "fallback": True,
            "message": "LLM service unavailable - showing general recommendations"
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the LLM model.
        
        Returns:
            Dictionary containing model information.
        """
        return {
            'model_name': self.model_name,
            'client_initialized': self.client is not None,
            'api_key_configured': bool(os.getenv('OPENAI_API_KEY')) if self.client else False
        }
