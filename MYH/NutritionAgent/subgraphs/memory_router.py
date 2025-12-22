"""
Memory-aware routing subgraph for intelligent conversation flow
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage

from models.state_models import GlobalState
from models.pydantic_models import MemoryRoutingOutput
from config.llm_config import LLMConfig
from utils.intent_analysis import (
    extract_intent_from_decomposition,
    assess_diagnosis_status,
    assess_data_sufficiency,
    assess_context_appropriateness
)
from utils.routing_logic import determine_routing_with_guidance
from utils.memory import update_conversation_memory

class MemoryRouter:
    """Handles memory-aware routing decisions based on conversation context"""
    
    def __init__(self):
        self.llm = LLMConfig.get_client("memory_router")
    
    def route(self, state: GlobalState) -> Dict[str, Any]:
        """
        Memory-aware routing node that considers conversation history,
        data sufficiency, and context appropriateness for intelligent routing decisions.
        """
        current_decomposition = state.get("decomposition", "")
        memory = state.get("conversation_memory", {})
        previous_routing = state.get("memory_routing", {})
        user_input = state.get("inquiry", "")
        
        # Extract current intent from decomposition
        current_intent = extract_intent_from_decomposition(current_decomposition)
        
        # Get previous intent
        previous_intent = previous_routing.get("current_intent")
        intent_changed = current_intent != previous_intent if previous_intent else False
        
        # Assess diagnosis status and data sufficiency
        diagnosis_status = assess_diagnosis_status(memory, state)
        data_sufficiency = assess_data_sufficiency(memory, current_intent)
        context_appropriateness = assess_context_appropriateness(current_decomposition, user_input)
        
        # Enhanced routing logic with data sufficiency and context checks
        routing_decision, guidance_message = determine_routing_with_guidance(
            current_intent=current_intent,
            diagnosis_status=diagnosis_status,
            data_sufficiency=data_sufficiency,
            context_appropriateness=context_appropriateness,
            memory=memory,
            user_input=user_input,
            decomposition=current_decomposition
        )
        
        # Build context for LLM routing decision (for complex cases)
        if routing_decision == "llm_decide":
            routing_prompt = f"""
You are a memory-aware conversation router for a medical AI system.

CURRENT SITUATION:
- User Input: "{user_input}"
- Decomposition: {current_decomposition}
- Current Intent: {current_intent}
- Previous Intent: {previous_intent}
- Intent Changed: {intent_changed}

CONVERSATION MEMORY:
- Diagnosis Completed: {memory.get('diagnosis_completed', False)}
- Has Health Profile: {bool(memory.get('user_health_profile', {}))}
- Previous Interactions: {len(memory.get('conversation_history', []))}
- Diagnosis Status: {diagnosis_status}

DATA SUFFICIENCY:
- For Diagnosis: {data_sufficiency.get('diagnosis', 'unknown')}
- For Nutrition: {data_sufficiency.get('nutrition', 'unknown')}

CONTEXT APPROPRIATENESS: {context_appropriateness}

ROUTING OPTIONS:
1. "diagnosis" - For health assessment, symptom analysis, risk calculation
2. "nutrition" - For dietary advice, meal suggestions, food questions  
3. "polish" - For general questions, clarifications, guidance, or insufficient data

ENHANCED ROUTING LOGIC:
- If insufficient data for diagnosis but health intent → route to "polish" with guidance
- If insufficient data for nutrition but nutrition intent → route to "polish" with guidance  
- If out of context question → route to "polish" with limitation explanation
- If diagnosis incomplete AND health-related intent AND sufficient data → route to "diagnosis"
- If diagnosis complete AND nutrition intent AND sufficient data → route to "nutrition"
- If general question or diagnosis complete → route to "polish"

Provide routing decision with confidence score and reasoning.

Output format:
{{
  "current_intent": "health|nutrition|general|followup|out_of_context",
  "intent_changed": true/false,
  "diagnosis_status": "none|partial|complete", 
  "routing_decision": "diagnosis|nutrition|polish",
  "confidence": 0.0-1.0,
  "reasoning": "explanation of routing decision"
}}
"""

            try:
                result = self.llm.with_structured_output(MemoryRoutingOutput).invoke(routing_prompt)
                routing_decision = result.routing_decision
                reasoning = result.reasoning
                confidence = result.confidence
            except Exception as e:
                print(f"LLM routing error: {e}")
                routing_decision = "polish"
                reasoning = "Fallback to polish due to LLM error"
                confidence = 0.3
        else:
            reasoning = guidance_message
            confidence = 0.8
        
        # Update memory with current interaction
        updated_memory = update_conversation_memory(
            memory, 
            user_input, 
            current_intent,
            routing_decision
        )
        
        # Add guidance message to state if routing to polish for guidance
        guidance_context = ""
        if routing_decision == "polish" and guidance_message:
            guidance_context = guidance_message
        
        return {
            "memory_routing": {
                "current_intent": current_intent,
                "previous_intent": previous_intent,
                "intent_changed": intent_changed,
                "diagnosis_status": diagnosis_status,
                "routing_decision": routing_decision,
                "confidence": confidence,
                "memory_context": reasoning,
                "guidance_message": guidance_context
            },
            "conversation_memory": updated_memory,
            "messages": [AIMessage(content=f"Memory routing: {reasoning}")]
        }
    
    def get_routing_decision(self, state: GlobalState) -> str:
        """Get the routing decision from memory routing state"""
        return state.get("memory_routing", {}).get("routing_decision", "polish")