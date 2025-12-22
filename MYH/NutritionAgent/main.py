"""
Main entry point for NutritionAgent
"""

import sys
import argparse
from core.agent import NutritionAgent
from interfaces.chat_interface import ChatInterface
from interfaces.simple_chat import SimpleChatInterface

def main():
    """Main entry point with command line argument parsing"""
    parser = argparse.ArgumentParser(description="Insulin Resistance Health Agent")
    parser.add_argument(
        "--interface", 
        choices=["full", "simple"], 
        default="full",
        help="Choose interface type (default: full)"
    )
    parser.add_argument(
        "--validate", 
        action="store_true",
        help="Validate system setup and exit"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Process a single query and exit"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize agent
        print("Initializing NutritionAgent...")
        agent = NutritionAgent()
        
        # Validate setup if requested
        if args.validate:
            validation = agent.validate_setup()
            print("\n🔧 SYSTEM VALIDATION:")
            for key, value in validation.items():
                status = "✅" if value else "❌"
                print(f"  {key}: {status} {value}")
            return
        
        # Process single query if provided
        if args.query:
            response = agent.process_query(args.query)
            print(f"\nResponse: {response}")
            return
        
        # Start interactive interface
        if args.interface == "simple":
            interface = SimpleChatInterface(agent)
            interface.run()
        else:
            interface = ChatInterface(agent)
            interface.run_conversation()
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Take care of your health!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()