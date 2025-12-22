"""
LLM configuration and client management
"""

from langchain_openai import ChatOpenAI
from typing import Dict, Any
import httpx

http_client = httpx.Client() # Désactive la vérification du certificat TLS/SSL
class LLMConfig:
    """LLM configuration and client factory"""
    
    # OpenAI API configuration
    OPENAI_API_KEY = 'sk-43eda59307484be7b7511ba8ce5be9fe'
    OPENAI_BASE_URL = 'https://tokenfactory.esprit.tn/api'
    OPENAI_MODEL = "hosted_vllm/Llama-3.1-70B-Instruct"
    LLMS = None
    
    def __init__():
        LLMConfig.create_llm_clients()
    
    @staticmethod
    def create_llm_clients() -> Dict[str, ChatOpenAI]:
        """Create OpenAI LLM clients for different tasks"""
        LLMConfig.LLMS= {
            "decomposer": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0.1,
                http_client=http_client
            ),
            "extractor": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0.1,
                http_client=http_client
            ),
            "logger": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0.1,
                http_client=http_client
            ),
            "state_fixer": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0.1,
                http_client=http_client
            ),
            "mets_ir_explainer": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0.1,
                http_client=http_client
            ),
            "risk_fusion": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0.1,
                http_client=http_client
            ),
            "nutrition": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0
            ),
            "message_polish": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0.45
            ),
            "memory_router": ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0.2
            )
        }

    @staticmethod
    def get_client(client_name: str) -> ChatOpenAI:
        """Get a specific LLM client"""
        clients = LLMConfig.LLMS
        if client_name not in clients:
            raise ValueError(f"Unknown LLM client: {client_name}")
        return clients[client_name]

    @staticmethod
    def validate_openai_connection() -> bool:
        """Validate that OpenAI API is accessible"""
        try:
            test_client = ChatOpenAI(
                model=LLMConfig.OPENAI_MODEL,
                api_key=LLMConfig.OPENAI_API_KEY,
                base_url=LLMConfig.OPENAI_BASE_URL,
                temperature=0
            )
            test_client.invoke("test")
            return True
        except Exception:
            return False