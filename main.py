from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from detector import EnterpriseGuardian

# This is the "app" variable that Uvicorn is looking for
app = FastAPI()

# Initialize our new V2 Engine
guardian = EnterpriseGuardian()

class PromptRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Enterprise Guardian Online"}

@app.post("/analyze")
def analyze_prompt(request: PromptRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Empty message")
    return guardian.analyze(request.message)