# NutritionAgent Project Structure

## Overview

This document describes the structured architecture of the NutritionAgent project, which was refactored from a monolithic `insulin_resistance_agent.py` file into a well-organized, modular system.

## Architecture Principles

### 1. **Separation of Concerns**
- Each module has a single, well-defined responsibility
- Configuration, models, business logic, and interfaces are separated
- Subgraphs are isolated and independently testable

### 2. **Modularity**
- Components can be imported and used independently
- Easy to extend with new subgraphs or utilities
- Clear dependency management

### 3. **Maintainability**
- Code is organized by functionality
- Clear naming conventions
- Comprehensive documentation

### 4. **Testability**
- Each module can be tested in isolation
- Mock-friendly interfaces
- Validation utilities built-in

## Directory Structure Explained

### `/config/` - Configuration Management
```
config/
├── settings.py      # Global constants, file paths, thresholds
└── llm_config.py    # LLM client factory and configuration
```

**Purpose**: Centralized configuration management
- **settings.py**: All configurable parameters in one place
- **llm_config.py**: LLM client creation and validation

### `/core/` - Core Business Logic
```
core/
├── agent.py           # Main NutritionAgent orchestrator class
└── session_manager.py # Session management (re-export from utils)
```

**Purpose**: Main application logic and orchestration
- **agent.py**: Primary class that coordinates all subgraphs
- **session_manager.py**: Convenience re-export for session management

### `/models/` - Data Schemas
```
models/
├── state_models.py     # TypedDict schemas for graph states
└── pydantic_models.py  # Pydantic models for LLM structured outputs
```

**Purpose**: Type safety and data validation
- **state_models.py**: Graph state schemas using TypedDict
- **pydantic_models.py**: Structured LLM output validation

### `/subgraphs/` - Processing Modules
```
subgraphs/
├── decomposer.py      # Message semantic decomposition
├── memory_router.py   # Intelligent conversation routing
├── diagnosis.py       # Health assessment (TODO: full implementation)
├── nutrition.py       # Nutrition guidance (TODO: full implementation)
└── message_style.py   # Response polishing (TODO: full implementation)
```

**Purpose**: Specialized processing components
- Each subgraph handles a specific aspect of the conversation
- Can be developed and tested independently
- Easy to add new subgraphs

### `/utils/` - Utility Functions
```
utils/
├── memory.py           # Session and conversation memory management
├── data_processing.py  # ML models and data transformation
├── intent_analysis.py  # Intent extraction and assessment
└── routing_logic.py    # Routing decision algorithms
```

**Purpose**: Reusable utility functions
- **memory.py**: Session management and conversation persistence
- **data_processing.py**: ML pipeline, unit conversion, risk calculation
- **intent_analysis.py**: Intent classification and context assessment
- **routing_logic.py**: Smart routing decision logic

### `/interfaces/` - User Interaction
```
interfaces/
├── chat_interface.py   # Full-featured chat with commands
└── simple_chat.py      # Minimal chat for testing
```

**Purpose**: User interaction layers
- **chat_interface.py**: Rich interface with help, summary, validation
- **simple_chat.py**: Minimal interface for quick testing

## Key Design Patterns

### 1. **Factory Pattern**
- `LLMConfig.create_llm_clients()` creates all LLM clients
- Centralized client management and configuration

### 2. **Strategy Pattern**
- Different routing strategies in `routing_logic.py`
- Pluggable intent analysis methods

### 3. **Observer Pattern**
- Memory system tracks conversation state changes
- Session manager observes and persists state

### 4. **Facade Pattern**
- `NutritionAgent` class provides simple interface to complex system
- Hides subgraph complexity from users

## Data Flow Architecture

```
User Input
    ↓
NutritionAgent.process_query()
    ↓
Decomposer Subgraph (semantic analysis)
    ↓
Memory Router (intelligent routing)
    ↓
[Diagnosis | Nutrition | Polish] Subgraph
    ↓
Response Polishing
    ↓
Session Memory Update
    ↓
Final Response
```

## Extension Points

### Adding New Subgraphs

1. **Create subgraph class** in `/subgraphs/`
```python
class NewSubgraph:
    def __init__(self):
        self.llm = LLMConfig.get_client("new_client")
        self.graph = self._build_graph()
    
    def invoke(self, state):
        return self.graph.invoke(state)
```

2. **Add to main agent** in `/core/agent.py`
```python
def __init__(self):
    self.new_subgraph = NewSubgraph()

def _build_orchestrator_graph(self):
    builder.add_node("new_node", self._run_new_subgraph)
```

3. **Update routing logic** in `/utils/routing_logic.py`

### Adding New Utilities

1. **Create utility module** in `/utils/`
2. **Add to `__init__.py`** for easy importing
3. **Update dependencies** in other modules

### Adding New Models

1. **Add state models** to `/models/state_models.py`
2. **Add Pydantic models** to `/models/pydantic_models.py`
3. **Update `__init__.py`** exports

## Configuration Management

### Environment-Specific Settings

```python
# In settings.py
class Settings:
    # Development
    PIPELINE_PATH = "dev/pipeline.pkl"
    
    # Production  
    PIPELINE_PATH = os.getenv("PIPELINE_PATH", "prod/pipeline.pkl")
```

### LLM Configuration

```python
# In llm_config.py
class LLMConfig:
    @staticmethod
    def create_llm_clients():
        model = os.getenv("LLM_MODEL", "gemma3:4b")
        return {
            "decomposer": ChatOllama(model=model, temperature=0.1),
            # ...
        }
```

## Testing Strategy

### Unit Testing
- Test each utility function independently
- Mock LLM clients for consistent testing
- Validate data models with sample data

### Integration Testing
- Test subgraph interactions
- Validate memory persistence
- Test routing decisions

### System Testing
- End-to-end conversation flows
- Performance testing with real data
- Error handling and recovery

## Deployment Considerations

### Package Installation
```bash
pip install -e .  # Development
pip install nutrition-agent  # Production
```

### Configuration
- Set environment variables for paths
- Validate setup with `--validate` flag
- Monitor LLM client connections

### Monitoring
- Log conversation flows
- Track routing decisions
- Monitor memory usage

## Migration from Monolithic Code

### Benefits Achieved

1. **Maintainability**: Code is easier to understand and modify
2. **Testability**: Components can be tested in isolation
3. **Extensibility**: New features can be added without affecting existing code
4. **Reusability**: Utilities can be used across different components
5. **Debugging**: Issues can be isolated to specific modules

### Backward Compatibility

The `run_insulin_resistance_agent()` function is maintained for backward compatibility:

```python
def run_insulin_resistance_agent(user_input: str, session_id: str = "default") -> str:
    agent = NutritionAgent()
    return agent.process_query(user_input, session_id)
```

## Future Enhancements

### Completed Features

1. **Complete Subgraph Implementation** ✅
   - Full diagnosis subgraph with all nodes (info extraction, state fixing, METS-IR calculation, symptom scoring, orchestration)
   - Complete nutrition subgraph with meal planning (classification, dish suggestions, dietary advice)
   - Advanced message styling with tone adaptation (intent-based polishing, tone matching)

### Planned Features

2. **Enhanced Memory System**
   - Persistent storage (database integration)
   - Cross-session learning
   - User preference tracking

3. **Advanced Analytics**
   - Conversation flow analysis
   - Performance metrics
   - User satisfaction tracking

4. **API Integration**
   - REST API endpoints
   - WebSocket support for real-time chat
   - Integration with health platforms

### Technical Improvements

1. **Performance Optimization**
   - Async processing for LLM calls
   - Caching for frequent queries
   - Batch processing for multiple users

2. **Robustness**
   - Circuit breaker pattern for LLM failures
   - Graceful degradation
   - Comprehensive error handling

3. **Security**
   - Input validation and sanitization
   - Rate limiting
   - Data privacy compliance

This structured approach provides a solid foundation for building a production-ready, maintainable, and extensible AI health assistant system.