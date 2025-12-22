import chromadb
from chromadb.utils import embedding_functions

class ChromaRetriever:
    def __init__(self, specialty):
        self.specialty = specialty
        self.client = chromadb.PersistentClient(path="chroma_db")
        self.embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.collection = self.client.get_collection(
            name=specialty, embedding_function=self.embedder
        )

    def retrieve(self, query, k=3):
        """
        Retourne une liste plate de documents texte.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            include=["documents"]
        )
        # results["documents"] est une liste de listes
        docs_nested = results["documents"] or [[]]
        docs = docs_nested[0] if len(docs_nested) > 0 else []
        return docs
