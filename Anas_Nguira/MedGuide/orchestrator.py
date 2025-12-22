from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from llm_esprit import EspritLLM
from agents.retriever_chroma import ChromaRetriever
from dotenv import load_dotenv
import os

# ======================================================
#  Charger clé API depuis .env
# ======================================================
load_dotenv()
API_KEY = os.getenv("ESPRIT_API_KEY")

# ======================================================
#  Initialisation du LLM universitaire
# ======================================================
llm = EspritLLM(api_key=API_KEY)

# ======================================================
#  Mémoire conversationnelle
# ======================================================
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    return_messages=True
)

# ======================================================
#  Sous-agent CLARIFIER : quand la question est vague
# ======================================================
clarifier_template = """
Tu es un assistant médical tunisien appelé Clarifier.
Ta mission est d'aider le patient à mieux formuler sa demande.
Quand la question est vague, tu dois :

 Reformuler brièvement ce que la personne semble vouloir dire.
 Poser 3 à 5 questions fermées (OUI/NON ou choix simples) pour préciser :
   - la localisation de la douleur
   - la durée
   - les symptômes associés
   - les antécédents
 Donner une règle de sécurité : quand consulter ou appeler le 190.

Historique :
{chat_history}

Question floue :
{question}

Réponds en français simple et clair, sans jargon médical inutile.
"""

clarifier_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=clarifier_template
)

clarifier_chain = LLMChain(
    llm=llm,
    prompt=clarifier_prompt,
    memory=memory
)

# ======================================================
#  Chaîne principale (Cardio / Neuro)
# ======================================================
doctor_template = """
Tu es Dr. {specialty_cap}, un assistant médical tunisien spécialisé en {specialty}.
Voici le contexte des échanges précédents :
{chat_history}

Contexte scientifique (issu de documents médicaux) :
{context}

Question actuelle :
{question}

Réponds de manière claire, médicale et bienveillante.
Indique les points de vigilance, les gestes à éviter et rappelle toujours d’appeler le 190 en cas de danger vital.
"""

doctor_prompt = PromptTemplate(
    input_variables=["specialty", "specialty_cap", "context", "question", "chat_history"],
    template=doctor_template
)

doctor_chain = LLMChain(
    llm=llm,
    prompt=doctor_prompt,
    memory=memory
)

# ======================================================
#  Initialisation des retrievers (Chroma)
# ======================================================
cardio = ChromaRetriever("cardio")
neuro = ChromaRetriever("neuro")

# ======================================================
#  Routage vers la spécialité
# ======================================================
def route_specialty(query):
    q = query.lower()
    if any(w in q for w in ["coeur", "cardiaque", "thorax", "infarctus", "palpitations"]):
        return "cardio"
    elif any(w in q for w in ["cerveau", "tête", "parole", "avc", "vertige", "engourdissement"]):
        return "neuro"
    else:
        return "cardio"

# ======================================================
#  Détection des requêtes floues
# ======================================================
def is_underspecified(query: str, docs) -> bool:
    """Détecte si la question est trop vague ou mal définie"""
    # Si le texte est trop court ou ne correspond à rien dans la base
    if len(query.strip()) < 10:
        return True
    if not docs or len(docs) == 0:
        return True
    # Vérifie si le contenu trouvé est peu pertinent
    joined_docs = " ".join(docs).lower()
    vague_terms = ["mal", "douleur", "problème", "ça fait mal", "je ne sais pas"]
    if any(v in query.lower() for v in vague_terms) and len(joined_docs) < 100:
        return True
    return False

# ======================================================
#  Fonction principale
# ======================================================
def generate_answer(query):
    # Déterminer la spécialité
    spec = route_specialty(query)
    retriever = cardio if spec == "cardio" else neuro

    # Récupération des documents contextuels
    docs = retriever.retrieve(query)
    context = "\n".join(d for sublist in docs for d in (sublist if isinstance(sublist, list) else [sublist]))


    # Vérifie si la question est floue
    if is_underspecified(query, docs):
        clarif = clarifier_chain.invoke({"question": query})
        return {"specialty": "clarifier", "answer": clarif["text"]}

    # Sinon : réponse médicale normale
    answer = doctor_chain.invoke({
        "specialty": spec,
        "specialty_cap": spec.capitalize(),
        "context": context,
        "question": query
    })

    return {"specialty": spec, "answer": answer["text"]}
