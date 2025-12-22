"""
NutritionAgent - Insulin Resistance Health Assessment and Nutrition Guidance System

A comprehensive AI-powered system for insulin resistance risk assessment and 
nutritional guidance using LangGraph and multi-agent architecture.
"""

from .core.agent import NutritionAgent
from .core.session_manager import SessionManager
from .utils.memory import clear_conversation_memory, get_conversation_summary

__version__ = "1.0.0"
__author__ = "Nutrition Agent Team"

# Main API exports
__all__ = [
    "NutritionAgent",
    "SessionManager", 
    "clear_conversation_memory",
    "get_conversation_summary"
]

# Convenience function for backward compatibility
def run_insulin_resistance_agent(user_input: str, session_id: str = "default") -> str:
    """
    Convenience function for backward compatibility
    
    Args:
        user_input: User's message/inquiry
        session_id: Session identifier for memory persistence
        
    Returns:
        Final polished response
    """
    agent = NutritionAgent()
    return agent.process_query(user_input, session_id)