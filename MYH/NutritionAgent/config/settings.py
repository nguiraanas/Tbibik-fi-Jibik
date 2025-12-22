"""
Configuration settings for the NutritionAgent system
"""

import os
from typing import Set
from pathlib import Path

class Settings:
    """Global configuration settings"""
    
    # File paths
    BASE_DIR = Path(__file__).parent.parent.parent
    PIPELINE_PATH = BASE_DIR / "Agent" / "Diagnosis" / "pipeline.pkl"
    CHROMA_DB_PATH = BASE_DIR / "Agent" / "Diagnosis" / "ir_embeddings_db2"
    
    # Required health variables for diagnosis
    REQUIRED_VARS: Set[str] = {"age", "weight", "height", "waist", "gender"}
    
    # Data sufficiency thresholds
    DIAGNOSIS_SUFFICIENT_VARS = 4  # Need 4+ variables for sufficient diagnosis
    DIAGNOSIS_PARTIAL_VARS = 2     # Need 2+ variables for partial diagnosis
    NUTRITION_SUFFICIENT_VARS = 3  # Need 3+ variables for sufficient nutrition advice
    NUTRITION_PARTIAL_VARS = 1     # Need 1+ variables for partial nutrition advice
    
    # Memory management
    MAX_CONVERSATION_HISTORY = 10  # Keep last 10 interactions
    MAX_INTENT_HISTORY = 5         # Keep last 5 intents
    
    # Model settings
    DEFAULT_MODEL = "gemma3:4b"
    
    # Symptom scoring parameters
    SYMPTOM_TOP_K = 3
    SYMPTOM_SIMILARITY_THRESHOLD = 0.45
    
    # METS-IR risk thresholds
    METS_IR_LOW_THRESHOLD = 35
    METS_IR_HIGH_THRESHOLD = 50
    
    @classmethod
    def get_pipeline_path(cls) -> str:
        """Get pipeline path as string"""
        return str(cls.PIPELINE_PATH)
    
    @classmethod
    def get_chroma_db_path(cls) -> str:
        """Get ChromaDB path as string"""
        return str(cls.CHROMA_DB_PATH)
    
    @classmethod
    def validate_paths(cls) -> dict:
        """Validate that required files exist"""
        return {
            "pipeline_exists": cls.PIPELINE_PATH.exists(),
            "chroma_db_exists": cls.CHROMA_DB_PATH.exists(),
            "pipeline_path": str(cls.PIPELINE_PATH),
            "chroma_db_path": str(cls.CHROMA_DB_PATH)
        }