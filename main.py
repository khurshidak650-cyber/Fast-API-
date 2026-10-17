from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Master Controller API is Live!"}
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="SkAi Master Controller API", version="1.0")

class QueryRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Master Controller API is Live!"}

@app.post("/ask")
def ask_assistant(request: QueryRequest):
    user_question = request.prompt
    smart_reply = f"SkAi Assistant ko aapka sawaal mil gaya: '{user_question}'. AI logic yahan jald judegha!"
    
    return {
        "status": "success",
        "query": user_question,
        "reply": smart_reply
    }
