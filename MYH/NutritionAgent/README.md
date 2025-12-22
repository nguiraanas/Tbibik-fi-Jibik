# NutritionAgent

A comprehensive AI-powered system for insulin resistance risk assessment and nutritional guidance using LangGraph and multi-agent architecture.

## Project Structure

```
NutritionAgent/
├── __init__.py                 # Package initialization and main API
├── main.py                     # Main entry point with CLI
├── setup.py                    # Package setup configuration
├── requirements.txt            # Dependencies
├── README.md                   # This file
│
├── config/                     # Configuration modules
│   ├── __init__.py
│   ├── settings.py             # Global settings and constants
│   └── llm_config.py           # LLM client configuration
│
├── core/                       # Core agent functionality
│   ├── __init__.py
│   ├── agent.py                # Main NutritionAgent class
│   └── session_manager.py      # Session management
│
├── models/                     # Data models and schemas
│   ├── __init__.py
│   ├── state_models.py         # TypedDict state schemas
│   └── pydantic_models.py      # Pydantic models for LLM outputs
│
├── subgraphs/                  # Individual subgraph implementations
│   ├── __init__.py
│   ├── decomposer.py           # Message decomposition subgraph
│   ├── memory_router.py        # Memory-aware routing
│   ├── diagnosis.py            # Health assessment subgraph
│   ├── nutrition.py            # Nutrition guidance subgraph
│   └── message_style.py        # Response polishing subgraph
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── memory.py               # Memory management utilities
│   ├── data_processing.py      # ML and data processing functions
│   ├── intent_analysis.py      # Intent extraction and assessment
│   └── routing_logic.py        # Routing decision logic
│
└── interfaces/                 # User interfaces
    ├── __init__.py
    ├── chat_interface.py       # Full-featured chat interface
    └── simple_chat.py          # Minimal chat interface
```

## Installation

### From Source

```bash
# Clone the repository
git clone <repository-url>
cd NutritionAgent

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Using pip (when published)

```bash
pip install nutrition-agent
```

## Quick Start

### Command Line Interface

```bash
# Full-featured interface (default)
python -m NutritionAgent.main

# Simple interface
python -m NutritionAgent.main --interface simple

# Validate system setup
python -m NutritionAgent.main --validate

# Process single query
python -m NutritionAgent.main --query "I'm 45, feeling tired, what should I eat?"
```

### Programmatic Usage

```python
from NutritionAgent import NutritionAgent

# Initialize agent
agent = NutritionAgent()

# Process queries
response = agent.process_query("I'm 45 years old, feeling tired after meals")
print(response)

# Use with session management
session_id = "user_123"
response1 = agent.process_query("I'm 45, male, 180 lbs", session_id)
response2 = agent.process_query("What should I eat for breakfast?", session_id)
```

### Using Interfaces

```python
from NutritionAgent.interfaces import ChatInterface, SimpleChatInterface

# Full-featured interface
chat = ChatInterface()
chat.run_conversation()

# Simple interface
simple_chat = SimpleChatInterface()
simple_chat.run()
```

## Configuration

### File Paths

Update paths in `NutritionAgent/config/settings.py`:

```python
class Settings:
    PIPELINE_PATH = "path/to/your/pipeline.pkl"
    CHROMA_DB_PATH = "path/to/your/chromadb"
```

### LLM Configuration

Modify LLM settings in `NutritionAgent/config/llm_config.py`:

```python
class LLMConfig:
    @staticmethod
    def create_llm_clients():
        return {
            "decomposer": ChatOllama(model="gemma3:4b", temperature=0.1),
            # ... other clients
        }
```

## Architecture

### Core Components

1. **NutritionAgent**: Main orchestrator class
2. **Memory Router**: Intelligent routing based on conversation history
3. **Subgraphs**: Specialized processing modules
4. **Session Manager**: Persistent conversation memory
5. **Interfaces**: User interaction layers

### Data Flow

```
User Input → Decomposer → Memory Router → [Diagnosis|Nutrition|Polish] → Final Response
                            ↑
                    Conversation Memory
```

### Memory System

- **Session Persistence**: Maintains conversation state across interactions
- **Health Profile**: Accumulates user health data over time
- **Intent Tracking**: Monitors conversation flow and intent changes
- **Smart Routing**: Routes based on context and data sufficiency

## Development

### Adding New Subgraphs

1. Create subgraph class in `subgraphs/`
2. Implement required methods
3. Register in main agent
4. Add routing logic

### Extending Functionality

1. **New Models**: Add to `models/pydantic_models.py`
2. **New Utilities**: Add to appropriate `utils/` module
3. **New Interfaces**: Add to `interfaces/`
4. **Configuration**: Update `config/settings.py`

### Testing

```bash
# Run validation
python -m NutritionAgent.main --validate

# Test with sample queries
python -m NutritionAgent.main --query "test query"

# Interactive testing
python -m NutritionAgent.main --interface simple
```

## API Reference

### Main Classes

#### NutritionAgent

```python
class NutritionAgent:
    def __init__(self)
    def process_query(self, user_input: str, session_id: str = "default") -> str
    def validate_setup(self) -> Dict[str, Any]
```

#### ChatInterface

```python
class ChatInterface:
    def __init__(self, agent: Optional[NutritionAgent] = None)
    def run_conversation(self)
    def print_help(self)
    def print_summary(self)
```

### Utility Functions

```python
# Memory management
from NutritionAgent.utils.memory import (
    clear_conversation_memory,
    get_conversation_summary
)

# Data processing
from NutritionAgent.utils.data_processing import (
    normalize_units,
    calculate_ir_risk
)
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes following project structure
4. Add tests if applicable
5. Submit pull request

## License

MIT License - see LICENSE file for details.

## Support

- Check system validation: `python -m NutritionAgent.main --validate`
- Review configuration in `config/settings.py`
- Ensure Ollama is running with required models
- Verify file paths for ML pipeline and ChromaDB

## Disclaimer

This software is for educational and research purposes only. It is not intended to diagnose, treat, cure, or prevent any disease. Always consult with qualified healthcare professionals for medical advice.