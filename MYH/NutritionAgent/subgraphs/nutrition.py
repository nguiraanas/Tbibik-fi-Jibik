"""
Nutrition subgraph for dietary advice and meal suggestions
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from models.state_models import SubgraphState
from models.pydantic_models import DishSuggestion, DishAdvice
from config.llm_config import LLMConfig

class NutritionSubgraph:
    """Handles nutrition guidance and meal suggestions for insulin resistance"""
    
    def __init__(self):
        self.llm = LLMConfig.get_client("nutrition")
        self.model_suggest = self.llm.with_structured_output(DishSuggestion)
        self.model_advise = self.llm.with_structured_output(DishAdvice)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the nutrition subgraph"""
        builder = StateGraph(SubgraphState)
        
        # Add nodes
        builder.add_node("classifier", self._classifier)
        builder.add_node("suggest_dish", self._suggest_dish)
        builder.add_node("give_advice", self._give_advice)
        
        # Define edges
        builder.add_edge(START, "classifier")
        
        # Conditional routing based on classification
        builder.add_conditional_edges(
            "classifier",
            lambda state: state["classifier_decision"],
            {
                "suggest_dish": "suggest_dish",
                "give_advice": "give_advice",
            }
        )
        
        builder.add_edge("suggest_dish", END)
        builder.add_edge("give_advice", END)
        
        return builder.compile()
    
    def _classifier(self, state: SubgraphState) -> Dict[str, Any]:
        """Classify user intent for nutrition advice"""
        text = state["toon_data"].lower()

        # Explicit intent → suggestion (highest priority)
        suggest_triggers = [
            "give me", "suggest", "recommend", "dish", "idea",
            "for my case", "adapt", "version", "cool", "healthier"
        ]

        if any(t in text for t in suggest_triggers):
            return {"classifier_decision": "suggest_dish"}

        # Explicit advice intent
        advice_triggers = [
            "is it ok", "should i", "advice", "healthy",
            "bad for me", "good for me"
        ]

        if any(t in text for t in advice_triggers):
            return {"classifier_decision": "give_advice"}

        # Fallback → LLM intent resolution (only if ambiguous)
        response = self.llm.invoke([
            HumanMessage(content=f"""
            Determine the user's intent.

            Text: "{state['toon_data']}"

            Respond with ONLY:
            - suggest_dish
            - give_advice
            """)
        ])

        decision = response.content.strip()
        return {"classifier_decision": decision}
    
    def _suggest_dish(self, state: SubgraphState) -> Dict[str, Any]:
        """Suggest IR-safe dish"""
        result = self.model_suggest.invoke([
            HumanMessage(content=f"""
            User metabolic profile: insulin resistance.
            TOON data: {state['toon_data']}

            Constraints:
            - Low glycemic load
            - Avoid refined carbs & sugar
            - Net carbs < 30g
            - Include protein & fiber
            - Calories 300–500

            Suggest ONE adapted dish.
            """)
        ])

        return {
            "interpretation": (
                f"SUGGESTION: {result.dish_name} "
                f"({result.total_calories} cal, "
                f"{result.net_carbs}g net carbs) — {result.reason}"
            ),
            "messages": [
                AIMessage(content=f"Structured suggestion:\n{result.model_dump_json(indent=2)}")
            ]
        }
    
    def _give_advice(self, state: SubgraphState) -> Dict[str, Any]:
        """Give nutrition advice with mitigation strategies"""
        result = self.model_advise.invoke([
            HumanMessage(content=f"""
            User metabolic profile: insulin resistance.
            TOON data mentions eating: {state['toon_data']}

            Rules:
            - Be honest about glycemic risk
            - No shaming
            - Provide mitigation strategies
            """)
        ])

        return {
            "interpretation": (
                f"ADVICE: {result.advice} "
                f"(glycemic risk: {result.glycemic_risk}, "
                f"~{result.calorie_estimate} cal)"
            ),
            "messages": [
                AIMessage(content=f"Structured advice:\n{result.model_dump_json(indent=2)}")
            ]
        }
    
    def invoke(self, state: SubgraphState) -> SubgraphState:
        """Invoke the nutrition subgraph"""
        return self.graph.invoke(state)