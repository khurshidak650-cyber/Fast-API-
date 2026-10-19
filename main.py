from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re
import math_logic
import python_logic  # <-- Python logic file ko yahan import kiya gaya hai

app = FastAPI(title="SkAi Ultimate Master API with Python AI Engine", version="5.0")

class SearchRequest(BaseModel):
    query: str
    language: str = "hi"  # Default language

def analyze_user_intent(text: str):
    text_lower = text.lower()
    
    # 1. Python Programming / Code Writer & Reader Intent Detection
    if any(word in text_lower for word in ["python", "code", "likho", "banao", "write", "analyze", "read", "decorator", "generator", "oop", "class", "function"]):
        return "Python Programming & AI Engine", "User Python code likhwana, padhana ya koi concept sikhna chahta hai."
    
    # 2. Math & Calculation Intent Detection
    elif any(word in text_lower for word in ["math", "ganit", "formula", "calculate", "solve", "+", "-", "*", "/", "area", "volume", "क्षेत्रफल", "आयतन", "परिमेय"]):
        return "Mathematical / Calculation", "User math ka koi formula ya concept samajhna chahta hai."
    
    # 3. Emotional / Psychology
    elif any(word in text_lower for word in ["sad", "dukhi", "pareshan", "lonely", "depressed"]):
        return "Emotional / Vulnerable", "User ko emotional support ki zaroorat hai."
    
    else:
        return "Neutral / General Inquiry", "Direct aur helpful information deni chahiye."

@app.get("/")
def read_root():
    return {"status": "online", "message": "SkAi Ultimate Backend with Python AI Writer, Math & Psychology Engines is Live!"}

@app.post("/fetch-info")
def fetch_web_info(request: SearchRequest):
    search_term = request.query
    lang = request.language
    
    detected_intent, intent_insight = analyze_user_intent(search_term)
    
    # Agar Python programming ya code likhne/padhne ka intent ho
    if detected_intent == "Python Programming & AI Engine":
        python_result = python_logic.solve_python_concept(search_term)
        return {
            "status": "success",
            "query": search_term,
            "language_used": lang,
            "user_intent": detected_intent,
            "intent_insight": intent_insight,
            "source": "Local Python AI Engine (python_logic.py)",
            "python_data": python_result
        }
        
    # Agar Math ka intent ho, toh math_logic.py se data lo
    elif detected_intent == "Mathematical / Calculation":
        math_result = math_logic.solve_math_problem(search_term)
        return {
            "status": "success",
            "query": search_term,
            "language_used": lang,
            "user_intent": detected_intent,
            "intent_insight": intent_insight,
            "source": "Local Math Engine (math_logic.py)",
            "math_data": math_result
        }
    
    # Baaki sabhi queries ke liye Web Search
    try:
        url = f"https://html.duckduckgo.com/html/?q={search_term}&kl={lang}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.post(url, headers=headers, data={"q": search_term})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = [a.text.strip() for a in soup.find_all('a', class_='result__snippet', limit=4)]
            info_content = " ".join(results) if results else "Live search se direct data nahi mila."
        else:
            info_content = "Web fetching error."
    except Exception as e:
        info_content = f"Error: {str(e)}"

    return {
        "status": "success",
        "query": search_term,
        "language_used": lang,
        "user_intent": detected_intent,
        "intent_insight": intent_insight,
        "source": "Web Search",
        "fetched_information": info_content
    }
