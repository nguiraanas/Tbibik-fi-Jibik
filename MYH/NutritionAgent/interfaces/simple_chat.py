"""
Simple chat interface for NutritionAgent
"""

import uuid
from typing import Optional

from core.agent import NutritionAgent

class SimpleChatInterface:
    """Minimal chat interface for quick testing"""
    
    def __init__(self, agent: Optional[NutritionAgent] = None):
        self.agent = agent or NutritionAgent()
        self.session_id = str(uuid.uuid4())[:8]  # Short session ID
    
    def run(self):
        """Simple conversation loop"""
        print("🏥 Insulin Resistance Agent - Simple Chat")
        print("Type 'quit' to exit")
        print("-" * 50)
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                # Exit condition
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Get response from agent
                print("Agent: ", end="", flush=True)
                response = self.agent.process_query(user_input, self.session_id)
                print(response)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")