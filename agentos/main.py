import os
from datetime import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
LOG_FILE = "/home/administrator/agentos/operations.log"

def log_op(lvl, msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{lvl}] {msg}\n")

class GoalRequest(BaseModel):
    goal: str
    priority: Optional[int] = 1
    tier: Optional[str] = "auto"

@app.get("/")
async def root():
    return FileResponse("/home/administrator/agentos/static/index.html")

@app.get("/health")
async def health():
    return {"status": "online", "port": 9000}

@app.get("/logs")
async def logs():
    try:
        with open(LOG_FILE, "r") as f: return {"logs": f.readlines()[-50:]}
    except: return {"logs": []}

@app.post("/execute")
async def execute(req: GoalRequest):
    log_op("INFO", f"Goal: {req.goal}")
    return {"status": "completed", "result": "Success", "model_used": "gemma2:27b", "execution_time": 0.1}

app.mount("/static", StaticFiles(directory="/home/administrator/agentos/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
