from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS  # Or use your preferred vectorstore
from langchain.embeddings import HuggingFaceEmbeddings  # Assuming open-source embeddings
from langchain.document_loaders import DirectoryLoader, PyPDFLoader  # Adjust for your article formats
from langchain.text_splitter import RecursiveCharacterTextSplitter
import httpx
import json
import os
from typing import Dict
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from datetime import datetime  # CELLE-CI MANQUAIT !
import uuid
import time   # <--- IMPORTANT : ajouté
from fastapi import BackgroundTasks
from rapport_designe import generate_beautiful_report

# Import your EspritLLM
from llm_esprit import EspritLLM  # Replace with the actual module where EspritLLM is defined

app = FastAPI()

# Setup embeddings (using open-source, since your LLM is university-hosted)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load articles for RAG (assume articles are in a directory 'articles/' with PDFs or text files)
# You can adjust the loader based on your file types
loader = DirectoryLoader("articles/", glob="**/*.pdf", loader_cls=PyPDFLoader)  # Or TextLoader for txt
documents = loader.load()

# Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create vectorstore (FAISS for local, or use Pinecone/Chroma if cloud)
vectorstore = FAISS.from_documents(texts, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # Retrieve top 3 relevant docs

# Initialize LLM
llm = EspritLLM(temperature=0.25, max_tokens=500, top_p=0.9)

# Setup memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# RAG chain for text queries
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a dermatological assistant. Answer based on the following context from articles: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}")
])

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough(), "chat_history": lambda x: memory.chat_memory.messages}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# For image analysis to report generation
report_prompt = ChatPromptTemplate.from_template(
    """Based on the following image analysis JSON, generate a detailed dermatological report:
    {analysis_json}
    
    Report should include:
    - Summary of tissue percentages
    - Potential implications (e.g., healing stage based on fibrin, granulation, callus)
    - Recommendations
    """
)

report_chain = report_prompt | llm | StrOutputParser()

class ChatRequest(BaseModel):
    message: str

# Endpoint for text-based chat
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Run RAG chain with memory
        response = rag_chain.invoke(request.message)
        
        # Save to memory
        memory.chat_memory.add_user_message(request.message)
        memory.chat_memory.add_ai_message(response)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint for image upload (handles image, calls your model pipeline, generates report)
# === ENDPOINT FINAL (version qui marche à 100%) ===
@app.post("/analyze_image")
async def analyze_image(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    temp_path = None
    try:
        # 1. Sauvegarde image
        suffix = os.path.splitext(file.filename)[1] or ".png"
        temp_path = f"temp_{uuid.uuid4().hex}{suffix}"
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)

        # 2. Prédiction
        with open(temp_path, "rb") as f:
            files = {"file": (file.filename, f, file.content_type)}
            async with httpx.AsyncClient(timeout=120) as client:
                resp = await client.post("http://localhost:8000/predict", files=files)
        
        if resp.status_code != 200:
            raise Exception("Erreur modèle")

        result = resp.json()

        # 3. Génération du BEAU rapport (on passe report_chain)
        pdf_path = await generate_beautiful_report(result, file.filename, report_chain,temp_path)

        # 4. Nettoyage image
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # 5. Envoi + suppression après téléchargement
        background_tasks.add_task(os.remove, pdf_path)

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"Rapport_MedOrient_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )

    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            try: os.remove(temp_path)
            except: pass
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")
                        
# To clear memory if needed
@app.post("/clear_memory")
async def clear_memory():
    memory.clear()
    return {"status": "Memory cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Run on different port to avoid conflict with model pipeline