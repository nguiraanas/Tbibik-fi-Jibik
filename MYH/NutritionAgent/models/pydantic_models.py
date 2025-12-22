"""
Pydantic models for structured LLM outputs
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Literal

# ===============================================
# DIAGNOSIS SUBGRAPH MODELS
# ===============================================

class ExtractedInfo(BaseModel):
    """Model for extracted health information"""
    vars: Dict[str, Any]
    symptoms: List[str]

class LoggingOutput(BaseModel):
    """Model for conversation logging"""
    type: str
    times_asked: int

class StateFixerOutput(BaseModel):
    """Model for normalized health variables"""
    vars: Dict[str, Any]

class METSIROutput(BaseModel):
    """Model for METS-IR interpretation"""
    response: str

class DiagnosisOutput(BaseModel):
    """Model for final diagnosis output"""
    risk_level: str
    dominant_factor: str
    interpretation: str
    note: str

# ===============================================
# MEMORY ROUTER MODELS
# ===============================================

class MemoryRoutingOutput(BaseModel):
    """Model for memory-aware routing decisions"""
    current_intent: str = Field(description="Current user intent")
    intent_changed: bool = Field(description="Whether intent changed from previous")
    diagnosis_status: Literal["none", "partial", "complete"] = Field(description="Diagnosis completion status")
    routing_decision: str = Field(description="Next node to route to")
    confidence: float = Field(description="Confidence in routing decision")
    reasoning: str = Field(description="Explanation of routing logic")

# ===============================================
# NUTRITION SUBGRAPH MODELS
# ===============================================

class DishSuggestion(BaseModel):
    """Model for dish suggestions"""
    dish_name: str = Field(description="Dish name")
    ingredients: List[str] = Field(description="Ingredients list")
    total_calories: int = Field(description="Calories per serving")
    net_carbs: int = Field(description="Estimated net carbs in grams")
    protein: int = Field(description="Protein in grams")
    fiber: int = Field(description="Fiber in grams")
    reason: str = Field(description="Why this dish fits insulin resistance")

class DishAdvice(BaseModel):
    """Model for dietary advice"""
    advice: str = Field(description="Main advice")
    glycemic_risk: Literal["low", "moderate", "high"]
    improvements: List[str] = Field(description="Mitigation suggestions")
    calorie_estimate: int = Field(description="Estimated calories")