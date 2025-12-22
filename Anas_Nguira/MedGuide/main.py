from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from orchestrator import generate_answer
import os

app = FastAPI(title="MedOrient Web Interface")

# servir le dossier frontend
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.post("/ask")
def ask(query: str = Query(..., description="Question du patient")):
    return generate_answer(query)
