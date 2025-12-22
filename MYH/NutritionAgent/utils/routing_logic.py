"""
Routing logic and decision making utilities
"""

from typing import Dict, Any, Tuple

def determine_routing_with_guidance(
    current_intent: str,
    diagnosis_status: str,
    data_sufficiency: Dict[str, str],
    context_appropriateness: str,
    memory: Dict[str, Any],
    user_input: str,
    decomposition: str
) -> Tuple[str, str]:
    """
    Determine routing decision and guidance message based on multiple factors
    
    Args:
        current_intent: Extracted user intent
        diagnosis_status: Current diagnosis completion status
        data_sufficiency: Assessment of available data
        context_appropriateness: Whether question is in scope
        memory: Conversation memory
        user_input: Original user input
        decomposition: TOON decomposition
        
    Returns:
        Tuple of (routing_decision, guidance_message)
    """
    
    # Handle out of context questions
    if context_appropriateness == "out_of_context":
        guidance = (
            "I'm specialized in insulin resistance health assessment and nutrition guidance. "
            "I can help with health risk evaluation, symptom analysis, dietary advice, and "
            "general questions about insulin resistance and metabolic health. "
            "I'm not able to assist with topics outside of health and nutrition."
        )
        return "polish", guidance
    
    # Handle health/diagnosis intent
    if current_intent == "health":
        if data_sufficiency["diagnosis"] == "insufficient":
            guidance = (
                "I'd love to help with your health assessment! To provide accurate insulin resistance "
                "risk evaluation, I need some basic information about you. Please share: "
                "your age, weight, height, waist circumference, and gender. "
                "You can also mention any symptoms you're experiencing like fatigue, thirst, "
                "frequent urination, or vision changes."
            )
            return "polish", guidance
        elif data_sufficiency["diagnosis"] == "partial":
            # Let diagnosis subgraph handle partial data and ask for missing info
            return "diagnosis", "Proceeding with partial health data"
        else:
            # Sufficient data for diagnosis
            return "diagnosis", "Sufficient data for health assessment"
    
    # Handle nutrition intent
    elif current_intent == "nutrition":
        if data_sufficiency["nutrition"] == "insufficient":
            guidance = (
                "I can provide nutrition guidance for insulin resistance! However, to give you "
                "the most relevant dietary advice, it would be helpful to know a bit about your "
                "health profile first. You can share your age, weight, activity level, or any "
                "health conditions. Alternatively, you can ask general questions about "
                "insulin-resistant friendly foods, meal ideas, or dietary principles."
            )
            return "polish", guidance
        else:
            # Sufficient or partial data for nutrition advice
            return "nutrition", "Providing nutrition guidance"
    
    # Handle follow-up questions
    elif current_intent == "followup":
        if diagnosis_status == "none" and not memory.get("conversation_history"):
            guidance = (
                "I'm here to help! I specialize in insulin resistance health assessment and "
                "nutrition guidance. You can ask me to:\n"
                "• Assess your insulin resistance risk (share your age, weight, height, waist size)\n"
                "• Analyze symptoms (fatigue, thirst, vision changes, etc.)\n"
                "• Suggest healthy meals and dietary advice\n"
                "• Explain insulin resistance and metabolic health concepts\n"
                "What would you like to know about?"
            )
            return "polish", guidance
        else:
            # Has context for follow-up
            return "polish", "Answering follow-up question with context"
    
    # Handle general questions
    elif current_intent == "general":
        if context_appropriateness == "unclear":
            guidance = (
                "I'm your insulin resistance health assistant! I can help you with:\n"
                "• Health risk assessment and symptom analysis\n"
                "• Personalized nutrition and meal suggestions\n"
                "• Education about insulin resistance and metabolic health\n"
                "• Dietary guidance for better blood sugar management\n\n"
                "What specific aspect of insulin resistance or metabolic health "
                "would you like to explore?"
            )
            return "polish", guidance
        else:
            return "polish", "Handling general health question"
    
    # Default case - let LLM decide
    return "llm_decide", ""

def simple_intent_routing(decomposition: str) -> str:
    """
    Fallback simple routing based on decomposition
    
    Args:
        decomposition: TOON decomposition string
        
    Returns:
        Routing decision: diagnosis|nutrition|polish
    """
    if not decomposition:
        return "polish"
    
    decomposition_lower = decomposition.lower()
    
    if any(word in decomposition_lower for word in ["health", "symptom", "tired", "risk"]):
        return "diagnosis"
    elif any(word in decomposition_lower for word in ["food", "nutrition", "meal", "eat"]):
        return "nutrition"
    else:
        return "polish"