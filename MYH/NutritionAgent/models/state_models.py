"""
State models for the NutritionAgent system using TypedDict
"""

from typing_extensions import TypedDict, Annotated
from typing import Dict, Any, List, Optional, Literal
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage

# ===============================================
# MEMORY SYSTEM STATES
# ===============================================

class ConversationMemory(TypedDict):
    """Persistent memory across conversation turns"""
    diagnosis_completed: bool
    last_diagnosis_result: Optional[Dict[str, Any]]
    user_health_profile: Dict[str, Any]  # Accumulated health data
    conversation_history: List[Dict[str, Any]]  # Previous interactions
    intent_history: List[str]  # Track intent changes
    session_context: Dict[str, Any]  # Session-level context

class MemoryState(TypedDict):
    """State for memory-aware routing node"""
    current_intent: str
    previous_intent: Optional[str]
    intent_changed: bool
    diagnosis_status: Literal["none", "partial", "complete"]
    routing_decision: str
    confidence: float
    memory_context: str
    guidance_message: str  # Added for guidance messages

# ===============================================
# GLOBAL ORCHESTRATOR STATE
# ===============================================

class GlobalState(TypedDict):
    inquiry: str
    diagnosis_result: Optional[str]
    nutrition_result: Optional[str]
    final_response: Optional[str]
    decomposition: Optional[str]
    subgraphs_states: Dict[str, dict]
    messages: Annotated[List[AIMessage | HumanMessage], "append"]
    # Enhanced with memory system
    conversation_memory: ConversationMemory
    memory_routing: MemoryState

# ===============================================
# SUBGRAPH STATES
# ===============================================

class InquiryState(TypedDict):
    """State for decomposer subgraph"""
    messages: Annotated[list[BaseMessage], "append"]
    input: str
    decompositions: Annotated[list[str], "append"]
    last_decomposition: str

class DiagnosisGraphState(TypedDict):
    """State for diagnosis subgraph"""
    vars: Dict[str, Any]
    symptoms: List[str]
    metr_ir: Optional[float]
    symptom_scores: Dict[str, Any]
    logging: List[Dict[str, Any]]
    final_output: str
    orchestrator_response: Dict[str, Any]
    router_next: Optional[str]
    input: str
    ready: bool

class SubgraphState(TypedDict):
    """State for nutrition subgraph"""
    toon_data: str
    metabolic_context: Literal["insulin_resistant"]
    messages: Annotated[List[AIMessage | HumanMessage], "append"]
    interpretation: str
    classifier_decision: str

class MessageStyleState(TypedDict):
    """State for message styling subgraph"""
    intent: Literal["explain", "summarize", "warn", "guide"]
    tone: Literal["friendly", "professional", "urgent", "casual"]
    source_text: str
    output_text: str
    messages: Annotated[list[AIMessage | HumanMessage], "append"]