"""
Intent analysis and assessment utilities
"""

from typing import Dict, Any
from config.settings import Settings

def extract_intent_from_decomposition(decomposition: str) -> str:
    """
    Extract primary intent from TOON decomposition
    
    Args:
        decomposition: TOON formatted decomposition string
        
    Returns:
        Intent category: health|nutrition|followup|general|out_of_context
    """
    if not decomposition:
        return "general"
    
    decomposition_lower = decomposition.lower()
    
    # Out of context indicators (check first)
    out_of_context_keywords = [
        "weather", "sports", "politics", "entertainment", "technology", "travel",
        "shopping", "games", "movies", "music", "news", "stock", "investment",
        "programming", "software", "computer", "phone", "car", "fashion"
    ]
    
    # Health/medical intent indicators
    health_keywords = [
        "symptom", "tired", "fatigue", "thirst", "urination", "vision",
        "weight", "waist", "health", "risk", "diabetes", "insulin",
        "blood", "glucose", "medical", "doctor", "diagnosis", "pain",
        "ache", "feel", "body", "physical"
    ]
    
    # Nutrition intent indicators  
    nutrition_keywords = [
        "food", "eat", "meal", "diet", "nutrition", "recipe", "cook",
        "breakfast", "lunch", "dinner", "snack", "ingredient", "calorie",
        "carb", "protein", "sugar", "fat", "fiber"
    ]
    
    # Follow-up intent indicators
    followup_keywords = [
        "what does", "explain", "mean", "clarify", "more about",
        "tell me", "understand", "how", "why", "what is"
    ]
    
    # Check for out of context first
    if any(keyword in decomposition_lower for keyword in out_of_context_keywords):
        return "out_of_context"
    elif any(keyword in decomposition_lower for keyword in health_keywords):
        return "health"
    elif any(keyword in decomposition_lower for keyword in nutrition_keywords):
        return "nutrition"  
    elif any(keyword in decomposition_lower for keyword in followup_keywords):
        return "followup"
    else:
        return "general"

def assess_diagnosis_status(memory: Dict[str, Any], state: Dict[str, Any]) -> str:
    """
    Assess the current diagnosis completion status
    
    Args:
        memory: Conversation memory
        state: Current global state
        
    Returns:
        Status: none|partial|complete
    """
    # Check if diagnosis was explicitly completed
    if memory.get("diagnosis_completed", False):
        return "complete"
    
    # Check if we have a recent diagnosis result
    if state.get("diagnosis_result") or memory.get("last_diagnosis_result"):
        return "complete"
    
    # Check if we have sufficient health profile data
    health_profile = memory.get("user_health_profile", {})
    required_vars = Settings.REQUIRED_VARS
    
    available_vars = len(set(health_profile.keys()) & required_vars)
    
    if available_vars >= 3:
        return "partial"
    elif available_vars >= 1:
        return "partial"
    else:
        return "none"

def assess_data_sufficiency(memory: Dict[str, Any], current_intent: str) -> Dict[str, str]:
    """
    Assess if we have sufficient data for diagnosis or nutrition advice
    
    Args:
        memory: Conversation memory
        current_intent: Current user intent
        
    Returns:
        Dictionary with sufficiency assessment for diagnosis and nutrition
    """
    health_profile = memory.get("user_health_profile", {})
    required_vars = Settings.REQUIRED_VARS
    
    # Count available health variables
    available_vars = sum(1 for var in required_vars if var in health_profile and health_profile[var] is not None)
    
    # Assess diagnosis data sufficiency
    if available_vars >= Settings.DIAGNOSIS_SUFFICIENT_VARS:
        diagnosis_sufficiency = "sufficient"
    elif available_vars >= Settings.DIAGNOSIS_PARTIAL_VARS:
        diagnosis_sufficiency = "partial"
    else:
        diagnosis_sufficiency = "insufficient"
    
    # Assess nutrition data sufficiency
    has_diagnosis = memory.get("diagnosis_completed", False)
    has_symptoms = len(memory.get("conversation_history", [])) > 0
    
    if has_diagnosis or available_vars >= Settings.NUTRITION_SUFFICIENT_VARS:
        nutrition_sufficiency = "sufficient"
    elif available_vars >= Settings.NUTRITION_PARTIAL_VARS or has_symptoms:
        nutrition_sufficiency = "partial"
    else:
        nutrition_sufficiency = "insufficient"
    
    return {
        "diagnosis": diagnosis_sufficiency,
        "nutrition": nutrition_sufficiency,
        "available_health_vars": available_vars,
        "total_required_vars": len(required_vars)
    }

def assess_context_appropriateness(decomposition: str, user_input: str) -> str:
    """
    Assess if the question is within the agent's scope
    
    Args:
        decomposition: TOON decomposition
        user_input: Original user input
        
    Returns:
        Appropriateness: appropriate|out_of_context|unclear
    """
    if not decomposition or not user_input:
        return "unclear"
    
    # Health and medical context keywords
    health_keywords = [
        "health", "medical", "symptom", "tired", "fatigue", "thirst", "urination", 
        "vision", "weight", "waist", "diabetes", "insulin", "blood", "glucose",
        "risk", "diagnosis", "doctor", "medication", "treatment", "pain", "ache"
    ]
    
    # Nutrition context keywords
    nutrition_keywords = [
        "food", "eat", "meal", "diet", "nutrition", "recipe", "cook", "breakfast",
        "lunch", "dinner", "snack", "ingredient", "calorie", "carb", "protein",
        "sugar", "fat", "fiber", "vitamin", "supplement"
    ]
    
    # General health education keywords
    education_keywords = [
        "what is", "explain", "how does", "why", "meaning", "definition",
        "understand", "learn", "information", "help", "advice"
    ]
    
    # Out of context indicators
    out_of_context_keywords = [
        "weather", "sports", "politics", "entertainment", "technology", "travel",
        "shopping", "games", "movies", "music", "news", "stock", "investment"
    ]
    
    text_lower = f"{decomposition} {user_input}".lower()
    
    # Check for out of context content
    if any(keyword in text_lower for keyword in out_of_context_keywords):
        return "out_of_context"
    
    # Check for appropriate context
    if any(keyword in text_lower for keyword in health_keywords + nutrition_keywords + education_keywords):
        return "appropriate"
    
    # If unclear, lean towards appropriate for health-related agent
    return "unclear"