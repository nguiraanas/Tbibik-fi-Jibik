"""
Full-featured chat interface for NutritionAgent
"""

import sys
from datetime import datetime
from typing import Optional

from core.agent import NutritionAgent
from utils.memory import get_conversation_summary, clear_conversation_memory

class ChatInterface:
    """Full-featured chat interface with rich formatting and commands"""
    
    def __init__(self, agent: Optional[NutritionAgent] = None):
        self.agent = agent or NutritionAgent()
        self.session_id = f"chat_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.conversation_count = 0
        
    def print_header(self):
        """Print welcome header"""
        print("=" * 70)
        print("🏥 INSULIN RESISTANCE HEALTH AGENT 🏥")
        print("=" * 70)
        print("Welcome! I'm your AI health assistant specialized in insulin resistance.")
        print("I can help with:")
        print("  • Health risk assessment")
        print("  • Symptom analysis") 
        print("  • Nutritional guidance")
        print("  • General health questions")
        print()
        print("💡 Tips:")
        print("  • Share your age, weight, height, waist size for better assessment")
        print("  • Describe any symptoms you're experiencing")
        print("  • Ask for meal suggestions or dietary advice")
        print("  • Type 'help' for commands, 'quit' to exit")
        print("=" * 70)
        print()

    def print_help(self):
        """Print help information"""
        print("\n📋 AVAILABLE COMMANDS:")
        print("  help     - Show this help message")
        print("  summary  - Show conversation summary")
        print("  clear    - Clear conversation memory")
        print("  validate - Check system setup")
        print("  quit     - Exit the chat")
        print("  exit     - Exit the chat")
        print()
        print("📝 EXAMPLE QUESTIONS:")
        print("  • I'm 45, male, 180 lbs, 5'8\", waist 38 inches, feeling tired")
        print("  • What should I eat for breakfast?")
        print("  • I have blurry vision and frequent urination")
        print("  • What does insulin resistance mean?")
        print("  • Can you suggest a low-carb dinner?")
        print()

    def print_summary(self):
        """Print conversation summary"""
        try:
            summary = get_conversation_summary(self.session_id)
            print("\n📊 CONVERSATION SUMMARY:")
            print(f"  Session ID: {self.session_id}")
            print(f"  Turns: {self.conversation_count}")
            print(f"  Diagnosis Completed: {'✅' if summary['diagnosis_completed'] else '❌'}")
            print(f"  Health Profile Items: {summary['health_profile_completeness']}")
            print(f"  Recent Intents: {', '.join(summary['recent_intents']) if summary['recent_intents'] else 'None'}")
            
            if summary['last_diagnosis']:
                print(f"  Last Risk Level: {summary['last_diagnosis'].get('risk_level', 'Unknown')}")
            print()
        except Exception as e:
            print(f"❌ Error getting summary: {e}\n")

    def clear_memory(self):
        """Clear conversation memory"""
        try:
            clear_conversation_memory(self.session_id)
            self.conversation_count = 0
            print("🧹 Conversation memory cleared. Starting fresh!\n")
        except Exception as e:
            print(f"❌ Error clearing memory: {e}\n")
    
    def validate_system(self):
        """Validate system setup"""
        try:
            validation = self.agent.validate_setup()
            print("\n🔧 SYSTEM VALIDATION:")
            print(f"  Pipeline Loaded: {'✅' if validation['pipeline_loaded'] else '❌'}")
            print(f"  ChromaDB Loaded: {'✅' if validation['chromadb_loaded'] else '❌'}")
            print(f"  LLM Clients: {'✅' if validation['llm_clients_loaded'] else '❌'}")
            print(f"  Pipeline File Exists: {'✅' if validation['pipeline_exists'] else '❌'}")
            print(f"  ChromaDB Exists: {'✅' if validation['chroma_db_exists'] else '❌'}")
            print(f"  Pipeline Path: {validation['pipeline_path']}")
            print(f"  ChromaDB Path: {validation['chroma_db_path']}")
            print()
        except Exception as e:
            print(f"❌ Error validating system: {e}\n")

    def format_response(self, response: str) -> str:
        """Format agent response for better readability"""
        if not response:
            return "❌ No response received."
        
        # Add some visual formatting
        formatted = f"🤖 Agent: {response}"
        return formatted

    def get_user_input(self) -> str:
        """Get user input with prompt"""
        try:
            user_input = input("👤 You: ").strip()
            return user_input
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Take care of your health!")
            sys.exit(0)
        except EOFError:
            print("\n\n👋 Goodbye! Take care of your health!")
            sys.exit(0)

    def process_command(self, user_input: str) -> bool:
        """Process special commands. Returns True if command was processed."""
        command = user_input.lower()
        
        if command in ['quit', 'exit']:
            print("\n👋 Thank you for using the Insulin Resistance Agent!")
            print("Remember: This tool is for educational purposes only.")
            print("Always consult with healthcare professionals for medical advice.")
            return True
            
        elif command == 'help':
            self.print_help()
            return False
            
        elif command == 'summary':
            self.print_summary()
            return False
            
        elif command == 'clear':
            self.clear_memory()
            return False
        
        elif command == 'validate':
            self.validate_system()
            return False
            
        return False

    def run_conversation(self):
        """Main conversation loop"""
        self.print_header()
        
        while True:
            try:
                # Get user input
                user_input = self.get_user_input()
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Process commands
                if self.process_command(user_input):
                    break
                
                # Show thinking indicator
                print("🤔 Thinking...")
                
                # Get agent response
                try:
                    response = self.agent.process_query(user_input, self.session_id)
                    self.conversation_count += 1
                    
                    # Format and display response
                    formatted_response = self.format_response(response)
                    print(f"\n{formatted_response}\n")
                    
                except Exception as e:
                    print(f"❌ Error getting response: {e}")
                    print("Please try again or type 'help' for assistance.\n")
                
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("Please try again.\n")