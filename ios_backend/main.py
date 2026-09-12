from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI()

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "hermes3"

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "Online", "model": MODEL_NAME, "message": "AI Bridge is active!"}

@app.post("/ask")
async def ask_ai(request: PromptRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": request.prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

