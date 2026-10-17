from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Master Controller API is Live!"}
