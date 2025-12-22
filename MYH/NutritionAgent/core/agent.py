"""
Main NutritionAgent class - orchestrates all subgraphs and manages conversation flow
"""

import os
import joblib
import chromadb
from typing import Dict, Any, Optional
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph, START, END

from models.state_models import GlobalState
from config.settings import Settings
from config.llm_config import LLMConfig
from subgraphs.decomposer import DecomposerSubgraph
from subgraphs.diagnosis import DiagnosisSubgraph
from subgraphs.nutrition import NutritionSubgraph
from subgraphs.message_style import MessageStyleSubgraph
from subgraphs.memory_router import MemoryRouter
from utils.memory import session_manager
from utils.data_processing import normalize_units, predict_metr_ir, calculate_ir_risk

class NutritionAgent:
    """
    Main agent class that orchestrates all subgraphs for insulin resistance 
    health assessment and nutrition guidance
    """
    
    def __init__(self):
        """Initialize the NutritionAgent with all required components"""
        self.settings = Settings()
        self.llm_clients = LLMConfig.create_llm_clients()
        
        # Initialize ML components
        self._init_ml_components()
        
        # Initialize subgraphs
        self.decomposer = DecomposerSubgraph()
        self.diagnosis = DiagnosisSubgraph(self.pipeline, self.collection)
        self.nutrition = NutritionSubgraph()
        self.message_style = MessageStyleSubgraph()
        self.memory_router = MemoryRouter()
        
        # Build main orchestrator graph
        self.graph = self._build_orchestrator_graph()
    
    def _init_ml_components(self):
        """Initialize ML pipeline and ChromaDB with error handling"""
        # Initialize ML pipeline
        try:
            if os.path.exists(self.settings.get_pipeline_path()):
                self.pipeline = joblib.load(self.settings.get_pipeline_path())
            else:
                print(f"Warning: Pipeline file not found at {self.settings.get_pipeline_path()}")
                self.pipeline = None
        except Exception as e:
            print(f"Error loading pipeline: {e}")
            self.pipeline = None
        
        # Skip ChromaDB initialization due to compatibility issues on Windows
        print("Warning: Skipping ChromaDB initialization due to compatibility issues")
        print("The system will run with limited symptom analysis capabilities")
        self.collection = None
    
    def _build_orchestrator_graph(self) -> StateGraph:
        """Build the main orchestrator graph"""
        builder = StateGraph(GlobalState)
        
        # Add nodes
        builder.add_node("decomposer", self._run_decomposer)
        builder.add_node("memory_router", self._run_memory_router)
        builder.add_node("diagnosis", self._run_diagnosis)
        builder.add_node("nutrition", self._run_nutrition)
        builder.add_node("polish", self._run_polish)
        
        # Decomposer is ALWAYS first
        builder.add_edge(START, "decomposer")
        
        # Always route to memory router after decomposer
        builder.add_edge("decomposer", "memory_router")
        
        # Memory-aware conditional routing
        builder.add_conditional_edges(
            "memory_router",
            self._memory_router_conditional,
            {
                "diagnosis": "diagnosis",
                "nutrition": "nutrition", 
                "polish": "polish"
            }
        )
        
        # After diagnosis -> check if nutrition needed, otherwise polish
        builder.add_conditional_edges(
            "diagnosis",
            self._should_continue_to_nutrition,
            {
                "nutrition": "nutrition",
                "polish": "polish"
            }
        )
        
        # After nutrition -> always polish
        builder.add_edge("nutrition", "polish")
        
        # Final polish
        builder.add_edge("polish", END)
        
        return builder.compile()
    
    def _run_decomposer(self, state: GlobalState) -> Dict[str, Any]:
        """Run decomposer subgraph"""
        subgraph_input = {
            "messages": [],
            "decompositions": [],
            "last_decomposition": "",
            "input": state["inquiry"]
        }
        
        result = self.decomposer.invoke(subgraph_input)
        
        node_states = state.get("subgraphs_states", {})
        node_states["decomposer"] = result
        
        return {
            "decomposition": result.get("last_decomposition", ""),
            "subgraphs_states": node_states,
            "messages": [AIMessage(content="Decomposition completed")]
        }
    
    def _run_memory_router(self, state: GlobalState) -> Dict[str, Any]:
        """Run memory-aware router"""
        return self.memory_router.route(state)
    
    def _run_diagnosis(self, state: GlobalState) -> Dict[str, Any]:
        """Run diagnosis subgraph"""
        # Get existing health profile from memory
        memory = state.get("conversation_memory", {})
        existing_profile = memory.get("user_health_profile", {})
        
        subgraph_input = {
            "vars": existing_profile.copy(),  # Start with existing health data
            "symptoms": [],
            "metr_ir": None,
            "symptom_scores": {},
            "logging": [],
            "final_output": "",
            "orchestrator_response": {},
            "router_next": None,
            "input": state["inquiry"],
            "ready": False
        }
        
        subgraph_result = self.diagnosis.invoke(subgraph_input)
        
        node_states = state.get("subgraphs_states", {})
        node_states["diagnosis"] = subgraph_result
        
        # Extract diagnosis result
        diagnosis_output = subgraph_result.get("final_output", {})
        if isinstance(diagnosis_output, dict):
            diagnosis_text = f"Risk Level: {diagnosis_output.get('risk_level', 'Unknown')}\n"
            diagnosis_text += f"Interpretation: {diagnosis_output.get('interpretation', 'No interpretation available')}"
        else:
            diagnosis_text = str(diagnosis_output)
        
        # Update memory with new health profile and diagnosis
        updated_memory = memory.copy()
        updated_memory["user_health_profile"] = subgraph_result.get("vars", existing_profile)
        updated_memory["last_diagnosis_result"] = diagnosis_output
        updated_memory["diagnosis_completed"] = bool(diagnosis_output)
        
        return {
            "diagnosis_result": diagnosis_text,
            "subgraphs_states": node_states,
            "conversation_memory": updated_memory,
            "messages": [AIMessage(content="Diagnosis subgraph completed")]
        }
    
    def _run_nutrition(self, state: GlobalState) -> Dict[str, Any]:
        """Run nutrition subgraph"""
        subgraph_input = {
            "toon_data": state["inquiry"],
            "metabolic_context": "insulin_resistant",
            "messages": [],
            "interpretation": "",
            "classifier_decision": ""
        }
        
        subgraph_result = self.nutrition.invoke(subgraph_input)
        
        node_states = state.get("subgraphs_states", {})
        node_states["nutrition"] = subgraph_result
        
        return {
            "nutrition_result": subgraph_result.get("interpretation", "No nutrition advice available"),
            "subgraphs_states": node_states,
            "messages": [AIMessage(content="Nutrition subgraph completed")]
        }
    
    def _run_polish(self, state: GlobalState) -> Dict[str, Any]:
        """Run polish subgraph to generate final response"""
        # Check if we have a guidance message from memory router
        memory_routing = state.get("memory_routing", {})
        guidance_message = memory_routing.get("guidance_message", "")
        
        if guidance_message:
            # Direct guidance message - no need for complex processing
            return {
                "final_response": guidance_message,
                "messages": [AIMessage(content="Provided guidance message")]
            }
        
        # Regular polish processing for diagnosis/nutrition results
        combined_text = f"""
DIAGNOSIS:
{state.get("diagnosis_result", "N/A")}

NUTRITION:
{state.get("nutrition_result", "N/A")}
"""
        
        # Determine intent and tone based on routing context
        memory_routing = state.get("memory_routing", {})
        current_intent = memory_routing.get("current_intent", "general")
        
        if current_intent == "out_of_context":
            intent = "warn"
            tone = "professional"
        elif current_intent in ["health", "nutrition"]:
            intent = "explain"
            tone = "friendly"
        else:
            intent = "guide"
            tone = "friendly"
        
        subgraph_input = {
            "intent": intent,
            "tone": tone, 
            "source_text": combined_text,
            "output_text": "",
            "messages": []
        }
        
        subgraph_result = self.message_style.invoke(subgraph_input)
        
        node_states = state.get("subgraphs_states", {})
        node_states["polish"] = subgraph_result
        
        return {
            "final_response": subgraph_result.get("output_text", "No response generated"),
            "subgraphs_states": node_states,
            "messages": [AIMessage(content="Final response polished")]
        }
    
    def _memory_router_conditional(self, state: GlobalState) -> str:
        """Conditional edge function for memory-aware routing"""
        return self.memory_router.get_routing_decision(state)
    
    def _should_continue_to_nutrition(self, state: GlobalState) -> str:
        """Determine if we should continue to nutrition after diagnosis"""
        memory_routing = state.get("memory_routing", {})
        current_intent = memory_routing.get("current_intent", "")
        
        # Continue to nutrition if user had nutrition intent or if it's a comprehensive assessment
        if current_intent in ["nutrition", "general"] or memory_routing.get("confidence", 0) < 0.7:
            return "nutrition"
        else:
            return "polish"
    
    def process_query(self, user_input: str, session_id: str = "default") -> str:
        """
        Main method to process user queries
        
        Args:
            user_input: User's message/inquiry
            session_id: Session identifier for memory persistence
            
        Returns:
            Final polished response
        """
        try:
            # Get or create session memory
            conversation_memory = session_manager.get_or_create_session(session_id)
            
            initial_state = {
                "inquiry": user_input,
                "diagnosis_result": None,
                "nutrition_result": None,
                "final_response": None,
                "decomposition": None,
                "subgraphs_states": {},
                "messages": [],
                "conversation_memory": conversation_memory,
                "memory_routing": {}
            }
            
            result = self.graph.invoke(initial_state)
            
            # Update session memory
            updated_memory = result.get("conversation_memory", conversation_memory)
            session_manager.update_session(session_id, updated_memory)
            
            return result.get("final_response", "I apologize, but I couldn't generate a response. Please try again.")
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I encountered an error while processing your request. Please try again."
    
    def validate_setup(self) -> Dict[str, Any]:
        """Validate that all components are properly set up"""
        validation_results = {
            "pipeline_loaded": self.pipeline is not None,
            "chromadb_loaded": self.collection is not None,
            "llm_clients_loaded": len(self.llm_clients) > 0,
            "settings_valid": True
        }
        
        # Add path validation
        path_validation = self.settings.validate_paths()
        validation_results.update(path_validation)
        
        return validation_results