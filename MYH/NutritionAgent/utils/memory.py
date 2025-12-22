"""
Memory management utilities for conversation persistence
"""

import pandas as pd
from typing import Dict, Any, List
from models.state_models import ConversationMemory

class SessionManager:
    """Manages conversation sessions and persistent memory"""
    
    def __init__(self):
        self.sessions = {}  # session_id -> ConversationMemory
    
    def get_or_create_session(self, session_id: str = "default") -> ConversationMemory:
        """Get existing session or create new one"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "diagnosis_completed": False,
                "last_diagnosis_result": None,
                "user_health_profile": {},
                "conversation_history": [],
                "intent_history": [],
                "session_context": {}
            }
        return self.sessions[session_id]
    
    def update_session(self, session_id: str, memory: ConversationMemory):
        """Update session memory"""
        self.sessions[session_id] = memory
    
    def clear_session(self, session_id: str):
        """Clear session memory"""
        if session_id in self.sessions:
            del self.sessions[session_id]

# Global session manager instance
session_manager = SessionManager()

def update_conversation_memory(
    current_memory: Dict[str, Any], 
    user_input: str, 
    intent: str,
    routing_decision: str
) -> ConversationMemory:
    """Update conversation memory with current interaction"""
    from config.settings import Settings
    
    # Initialize memory if empty
    if not current_memory:
        current_memory = {
            "diagnosis_completed": False,
            "last_diagnosis_result": None,
            "user_health_profile": {},
            "conversation_history": [],
            "intent_history": [],
            "session_context": {}
        }
    
    # Add current interaction to history
    interaction = {
        "user_input": user_input,
        "intent": intent,
        "routing_decision": routing_decision,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    
    history = current_memory.get("conversation_history", [])
    history.append(interaction)
    
    # Keep only last N interactions to manage memory
    if len(history) > Settings.MAX_CONVERSATION_HISTORY:
        history = history[-Settings.MAX_CONVERSATION_HISTORY:]
    
    # Update intent history
    intent_history = current_memory.get("intent_history", [])
    intent_history.append(intent)
    if len(intent_history) > Settings.MAX_INTENT_HISTORY:
        intent_history = intent_history[-Settings.MAX_INTENT_HISTORY:]
    
    return {
        "diagnosis_completed": current_memory.get("diagnosis_completed", False),
        "last_diagnosis_result": current_memory.get("last_diagnosis_result"),
        "user_health_profile": current_memory.get("user_health_profile", {}),
        "conversation_history": history,
        "intent_history": intent_history,
        "session_context": current_memory.get("session_context", {})
    }

def clear_conversation_memory(session_id: str = "default"):
    """Clear conversation memory for a session"""
    session_manager.clear_session(session_id)

def get_conversation_summary(session_id: str = "default") -> Dict[str, Any]:
    """Get summary of conversation for a session"""
    memory = session_manager.get_or_create_session(session_id)
    return {
        "diagnosis_completed": memory.get("diagnosis_completed", False),
        "health_profile_completeness": len(memory.get("user_health_profile", {})),
        "conversation_turns": len(memory.get("conversation_history", [])),
        "recent_intents": memory.get("intent_history", [])[-3:],
        "last_diagnosis": memory.get("last_diagnosis_result")
    }