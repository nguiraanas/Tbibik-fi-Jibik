import httpx
from openai import OpenAI
from langchain.llms.base import LLM
from typing import Optional, List, Any
from dotenv import load_dotenv
import os



class EspritLLM(LLM):
    """LLM wrapper compatible LangChain pour le modèle hébergé à Esprit."""

    model: str = "hosted_vllm/Llama-3.1-70B-Instruct"
    temperature: float = 0.7
    max_tokens: int = 500
    top_p: float = 0.9
    api_key: str = ""
    base_url: str = "https://tokenfactory.esprit.tn/api"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        http_client = httpx.Client(verify=False)
        load_dotenv()  # charge automatiquement le fichier .env
        api_key = os.getenv("ESPRIT_API_KEY")
        client = OpenAI(
            api_key=api_key,
            base_url=self.base_url,
            http_client=http_client
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"""
                    Tu es un agent médical tunisien spécialisé.
                    Ta mission est d analyser les informations du patient selon ta spécialité
                    et de formuler des recommandations informatives, sécurisées et professionnelles.

                    RÈGLES :
                    1. Tu n établis pas de diagnostic définitif.
                    2. Tu fournis des explications basées sur des connaissances médicales validées.
                    3. Si les informations sont insuffisantes, pose des questions ciblées avant de conclure.
                    4. Tu n inventes aucun fait médical.
                    5. Tu restes concis, structuré et clair.

                    FORMAT DE RÉPONSE :
                    - Analyse selon ta spécialité
                    - Risques potentiels
                    
                    - Questions à poser si nécessaire
                    - Recommandation générale (sans remplacer un médecin)
                    """
                    },
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p
        )
        return response.choices[0].message.content

    @property
    def _llm_type(self) -> str:
        return "esprit_llm"
