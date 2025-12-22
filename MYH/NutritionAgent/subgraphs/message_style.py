"""
Message styling subgraph for response polishing and tone adjustment
"""

from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from models.state_models import MessageStyleState
from config.llm_config import LLMConfig

class MessageStyleSubgraph:
    """Handles message polishing and tone adjustment for final responses"""
    
    def __init__(self):
        self.llm = LLMConfig.get_client("message_polish")
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the message styling subgraph"""
        builder = StateGraph(MessageStyleState)
        
        # Add single node for message polishing
        builder.add_node("polish_message", self._generate_polished_message)
        
        # Simple linear flow
        builder.add_edge(START, "polish_message")
        builder.add_edge("polish_message", END)
        
        return builder.compile()
    
    def _generate_polished_message(self, state: MessageStyleState) -> Dict[str, Any]:
        """Transform internal text into polished user-facing message"""
        prompt = f"""
You are a skilled support communicator.

Your task is to transform INTERNAL SUPPORT TEXT into a USER-FACING MESSAGE.

INTENT: {state['intent']}
TONE: {state['tone']}

INTERNAL TEXT:
{state['source_text']}

RULES:
- Do NOT mention "documentation", "internal notes", or system details
- Do NOT add new technical facts
- Keep the message human, clear, and empathetic
- Match the intent precisely:
    • explain → clarify calmly
    • summarize → short and focused
    • warn → clear, direct, respectful
    • guide → step-by-step but friendly
- Match the tone naturally (do not exaggerate)

OUTPUT:
Return ONLY the final message.
"""

        response = self.llm.invoke([HumanMessage(content=prompt)])
        print(response)
        return {
            "output_text": response.content.strip(),
            "messages": [AIMessage(content="Polished support message generated")]
        }
    
    def invoke(self, state: MessageStyleState) -> MessageStyleState:
        """Invoke the message styling subgraph"""
        return self.graph.invoke(state)