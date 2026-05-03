import logging
from typing import List, Dict, Any, Optional
from .retriever_service import RetrieverService

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for generating enhanced scheme recommendations."""
    
    def __init__(self):
        """Initialize recommendation service."""
        self.retriever_service = RetrieverService()
    
    def generate_personalized_recommendations(self, user_profile: Dict[str, Any], 
                                          max_recommendations: int = 5) -> Dict[str, Any]:
        """
        Generate personalized scheme recommendations based on user profile.
        
        Args:
            user_profile: User's profile information.
            max_recommendations: Maximum number of recommendations.
            
        Returns:
            Dictionary with personalized recommendations.
        """
        try:
            logger.info(f"Generating personalized recommendations for user profile: {user_profile}")
            
            # Initialize RAG system
            self.retriever_service.initialize()
            
            # Create search query based on user profile
            search_query = self._create_profile_based_query(user_profile)
            
            # Search for relevant schemes
            search_results = self.retriever_service.search(
                query=search_query,
                top_k=max_recommendations,
                user_profile=user_profile
            )
            
            # Enhance results with additional analysis
            enhanced_recommendations = self._enhance_recommendations(search_results, user_profile)
            
            return {
                "success": True,
                "message": f"Generated {len(enhanced_recommendations)} personalized recommendations",
                "recommendations": enhanced_recommendations,
                "total_recommendations": len(enhanced_recommendations),
                "search_query": search_query,
                "user_profile": user_profile
            }
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {
                "success": False,
                "message": "Failed to generate recommendations",
                "error": str(e)
            }
    
    def _create_profile_based_query(self, user_profile: Dict[str, Any]) -> str:
        """
        Create search query based on user profile.
        
        Args:
            user_profile: User profile information.
            
        Returns:
            Search query string.
        """
        query_parts = []
        
        # Add age-based terms
        age = user_profile.get('age')
        if age:
            if age < 18:
                query_parts.append("student schemes")
            elif age < 30:
                query_parts.append("youth schemes")
            elif age < 60:
                query_parts.append("adult schemes")
        
        # Add income-based terms
        income = user_profile.get('income')
        if income:
            if income < 200000:
                query_parts.append("low income schemes")
            elif income < 500000:
                query_parts.append("middle income schemes")
            else:
                query_parts.append("high income schemes")
        
        # Add education-based terms
        education = user_profile.get('education', '').lower()
        if 'graduate' in education or 'postgraduate' in education:
            query_parts.append("professional schemes")
        elif 'college' in education or 'engineering' in education:
            query_parts.append("technical schemes")
        
        # Add occupation-based terms
        occupation = user_profile.get('occupation', '').lower()
        if 'student' in occupation:
            query_parts.append("educational schemes")
        elif 'farmer' in occupation or 'agriculture' in occupation:
            query_parts.append("agricultural schemes")
        elif 'business' in occupation or 'self-employed' in occupation:
            query_parts.append("business schemes")
        
        # Add state-specific terms
        state = user_profile.get('state', '')
        if state:
            query_parts.append(f"schemes in {state}")
        
        # Combine all query parts
        base_query = " ".join(query_parts)
        
        return f"personalized government schemes for {base_query}"
    
    def _enhance_recommendations(self, search_results: List[Dict[str, Any]], 
                             user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Enhance search results with additional analysis and personalization.
        
        Args:
            search_results: Raw search results from RAG.
            user_profile: User profile information.
            
        Returns:
            Enhanced recommendations with additional metadata.
        """
        enhanced_recommendations = []
        
        for result in search_results:
            enhanced_result = result.copy()
            
            # Calculate eligibility score based on user profile
            eligibility_score = self._calculate_eligibility_score(result, user_profile)
            
            # Calculate benefit alignment score
            benefit_score = self._calculate_benefit_alignment(result, user_profile)
            
            # Calculate overall recommendation score
            overall_score = (eligibility_score + benefit_score) / 2
            
            # Add personalized reasoning
            reasoning = self._generate_personalized_reasoning(result, user_profile, eligibility_score, benefit_score)
            
            # Add application priority
            priority = self._determine_application_priority(result, user_profile)
            
            # Add next steps
            next_steps = self._generate_next_steps(result, user_profile)
            
            # Enhance the result
            enhanced_result.update({
                'eligibility_score': round(eligibility_score, 2),
                'benefit_score': round(benefit_score, 2),
                'overall_score': round(overall_score, 2),
                'personalized_reasoning': reasoning,
                'application_priority': priority,
                'next_steps': next_steps,
                'recommendation_strength': self._get_recommendation_strength(overall_score)
            })
            
            enhanced_recommendations.append(enhanced_result)
        
        # Sort by overall score
        enhanced_recommendations.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return enhanced_recommendations
    
    def _calculate_eligibility_score(self, result: Dict[str, Any], user_profile: Dict[str, Any]) -> float:
        """Calculate how well the scheme matches user's eligibility criteria."""
        score = 0.5  # Base score
        
        # Age matching
        user_age = user_profile.get('age')
        if user_age and result.get('category') == 'education':
            if 18 <= user_age <= 25:
                score += 0.3
            elif 26 <= user_age <= 35:
                score += 0.2
        
        # Income matching
        user_income = user_profile.get('income')
        income_limit = result.get('income_limit')
        if user_income and income_limit:
            if user_income <= income_limit:
                score += 0.3
        
        # State matching
        user_state = user_profile.get('state')
        scheme_state = result.get('state')
        if user_state and scheme_state:
            if user_state == scheme_state or scheme_state == 'All India':
                score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_benefit_alignment(self, result: Dict[str, Any], user_profile: Dict[str, Any]) -> float:
        """Calculate how well scheme benefits align with user needs."""
        score = 0.5  # Base score
        
        # Category alignment
        user_needs = self._extract_user_needs(user_profile)
        category = result.get('category', '').lower()
        
        if 'education' in user_needs and 'education' in category:
            score += 0.3
        elif 'healthcare' in user_needs and 'healthcare' in category:
            score += 0.3
        elif 'housing' in user_needs and 'housing' in category:
            score += 0.3
        elif 'agriculture' in user_needs and 'agriculture' in category:
            score += 0.3
        
        return min(score, 1.0)
    
    def _extract_user_needs(self, user_profile: Dict[str, Any]) -> List[str]:
        """Extract user needs from profile."""
        needs = []
        
        # Extract from occupation
        occupation = user_profile.get('occupation', '').lower()
        if 'student' in occupation:
            needs.append('education')
        elif 'farmer' in occupation:
            needs.append('agriculture')
        elif 'business' in occupation:
            needs.append('business')
        
        # Extract from education
        education = user_profile.get('education', '').lower()
        if 'college' in education or 'university' in education:
            needs.append('education')
        
        # Extract from age
        age = user_profile.get('age', 0)
        if age < 30:
            needs.append('youth_support')
        
        # Extract from income level
        income = user_profile.get('income', 0)
        if income < 300000:
            needs.append('financial_assistance')
        
        return needs
    
    def _generate_personalized_reasoning(self, result: Dict[str, Any], user_profile: Dict[str, Any], 
                                       eligibility_score: float, benefit_score: float) -> str:
        """Generate personalized reasoning for recommendation."""
        reasons = []
        
        # Eligibility reasoning
        if eligibility_score >= 0.8:
            reasons.append(f"You meet the eligibility criteria based on your age ({user_profile.get('age')}), income, and state")
        elif eligibility_score >= 0.6:
            reasons.append(f"You partially meet the eligibility criteria, particularly for your age ({user_profile.get('age')}) and income level")
        else:
            reasons.append(f"This scheme may have some eligibility requirements that don't perfectly match your profile")
        
        # Benefit reasoning
        if benefit_score >= 0.8:
            reasons.append(f"The benefits align well with your needs in {user_profile.get('occupation', 'general')}")
        elif benefit_score >= 0.6:
            reasons.append(f"The benefits provide moderate value for your situation")
        else:
            reasons.append("The benefits may not fully address your specific needs")
        
        return ". ".join(reasons)
    
    def _determine_application_priority(self, result: Dict[str, Any], user_profile: Dict[str, Any]) -> str:
        """Determine application priority based on urgency and match."""
        score = (result.get('eligibility_score', 0) + result.get('benefit_score', 0)) / 2
        
        if score >= 0.8:
            return "high"
        elif score >= 0.6:
            return "medium"
        else:
            return "low"
    
    def _generate_next_steps(self, result: Dict[str, Any], user_profile: Dict[str, Any]) -> List[str]:
        """Generate next steps for application."""
        steps = []
        
        # Common steps
        steps.append("Gather required documents (Aadhaar card, income certificate, etc.)")
        steps.append(f"Visit {result.get('official_link', 'official website')} for detailed information")
        steps.append("Check application deadlines and submission dates")
        
        # Profile-specific steps
        user_income = user_profile.get('income', 0)
        if user_income < 300000:
            steps.append("Consider applying for income certificate if required")
        
        user_education = user_profile.get('education', '')
        if 'college' in user_education or 'university' in user_education:
            steps.append("Obtain academic transcripts and certificates")
        
        return steps
    
    def _get_recommendation_strength(self, score: float) -> str:
        """Get recommendation strength based on score."""
        if score >= 0.8:
            return "strong"
        elif score >= 0.6:
            return "moderate"
        else:
            return "weak"
