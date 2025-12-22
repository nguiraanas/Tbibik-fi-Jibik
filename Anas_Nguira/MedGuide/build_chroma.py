import os
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ===========================================================
# 🧹 1️⃣ Fonction de nettoyage du texte brut
# ===========================================================
def clean_text(text: str) -> str:
    """
    Nettoie le texte médical : supprime espaces inutiles, retours à la ligne
    et caractères spéciaux redondants.
    """
    text = text.replace("\t", " ").replace("\r", " ")
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip()

# ===========================================================
# 🧩 2️⃣ Fonction principale : création des collections Chroma
# ===========================================================
def build_collection(specialty: str):
    print(f"\n📘 Construction de la collection pour {specialty} ...")

    # ---- 1. Initialiser ChromaDB local
    client = chromadb.PersistentClient(path="chroma_db")

    # ---- 2. Définir la fonction d’embedding
    embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ---- 3. Créer ou récupérer la collection
    collection = client.get_or_create_collection(
        name=specialty,
        embedding_function=embedder
    )

    # ---- 4. Charger le texte brut de la spécialité
    data_path = f"agents/{specialty}/data/{specialty}_docs.txt"
    if not os.path.exists(data_path):
        print(f"⚠️  Fichier introuvable : {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # ---- 5. Nettoyer le texte
    clean = clean_text(raw_text)

    # ---- 6. Découpage avancé avec RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=100,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""],
        length_function=len
    )
    chunks = text_splitter.split_text(clean)

    print(f"→ {len(chunks)} chunks générés pour {specialty}")

    # ---- 7. Ajouter les chunks dans Chroma
    collection.add(
        documents=chunks,
        ids=[f"{specialty}_{i}" for i in range(len(chunks))],
        metadatas=[{"specialty": specialty, "chunk": i} for i in range(len(chunks))]
    )

    print(f"✅ Collection '{specialty}' mise à jour ({len(chunks)} chunks)")

# ===========================================================
# 🚀 3️⃣ Point d’entrée principal
# ===========================================================
if __name__ == "__main__":
    # Créer le dossier Chroma s’il n’existe pas
    os.makedirs("chroma_db", exist_ok=True)

    # Liste des spécialités à indexer
    specialties = ["cardio", "neuro"]

    for sp in specialties:
        build_collection(sp)

    print("\n🎉 Indexation terminée avec succès !")
