# ==========================================
# main.py
# SkAi Ultimate Master API Backend (Multi-Engine Integrated)
# ==========================================

from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re

# Local Modular Logic Engines
import math_logic
import python_logic        # Dedicated Python Engine
import javascript_logic    # Dedicated JavaScript Engine
import programming_engine  # Universal Engine for ALL OTHER languages (C++, Java, Rust, SQL, etc.)

app = FastAPI(title="SkAi Ultimate Master API", version="8.0")

class SearchRequest(BaseModel):
    query: str
    language: str = "hi"

def analyze_user_intent(text: str):
    text_lower = text.lower()
    
    # 1. Dedicated Python Intent
    if any(word in text_lower for word in ["python", "decorator", "generator", "oop in python"]):
        return "Python Dedicated Engine", "User specifically Python ke baare me puch raha hai."
    
    # 2. Dedicated JavaScript Intent
    if any(word in text_lower for word in ["javascript", "js", "closure", "prototype", "promise", "async js"]):
        return "JavaScript Dedicated Engine", "User specifically JavaScript ke baare me puch raha hai."
        
    # 3. Universal Programming Intent (For C++, Java, Rust, Go, SQL, etc.)
    elif any(word in text_lower for word in ["c++", "cpp", "java", "rust", "go", "golang", "c#", "sql", "code", "banao", "likho", "programming", "compiler"]):
        return "Universal Programming Engine", "User kisi anya language ya general programming ke baare me puch raha hai."
    
    # 4. Math Intent
    elif any(word in text_lower for word in ["math", "ganit", "formula", "calculate", "solve", "+", "-", "*", "/", "area", "volume", "क्षेत्रफल", "आयतन"]):
        return "Mathematical / Calculation", "User math ka koi formula ya concept samajhna chahta hai."
    
    # 5. Emotional Intent
    elif any(word in text_lower for word in ["sad", "dukhi", "pareshan", "lonely", "depressed"]):
        return "Emotional / Vulnerable", "User ko emotional support ki zaroorat hai."
    
    else:
        return "Neutral / General Inquiry", "Direct aur helpful information deni chahiye."

@app.get("/")
def read_root():
    return {"status": "online", "message": "SkAi Multi-Engine Backend is Live with Universal Programming Support!"}

@app.post("/fetch-info")
def fetch_web_info(request: SearchRequest):
    search_term = request.query
    lang = request.language
    
    detected_intent, intent_insight = analyze_user_intent(search_term)
    
    # ----------------------------------------------------
    # ROUTING TO SPECIFIC ENGINES
    # ----------------------------------------------------
    
    # Python Dedicated Route
    if detected_intent == "Python Dedicated Engine":
        py_result = python_logic.solve_python_concept(search_term)
        return {
            "status": "success", "query": search_term, "language_used": lang,
            "user_intent": detected_intent, "source": "Dedicated Python Engine", "data": py_result
        }

    # JavaScript Dedicated Route
    elif detected_intent == "JavaScript Dedicated Engine":
        js_result = javascript_logic.solve_javascript_concept(search_term)
        return {
            "status": "success", "query": search_term, "language_used": lang,
            "user_intent": detected_intent, "source": "Dedicated JavaScript Engine", "data": js_result
        }

    # Universal Programming Route (C++, Java, Rust, SQL, etc.)
    elif detected_intent == "Universal Programming Engine":
        prog_result = programming_engine.solve_programming_query(search_term)
        return {
            "status": "success", "query": search_term, "language_used": lang,
            "user_intent": detected_intent, "source": "Universal Programming Engine (programming_engine.py)", "data": prog_result
        }
        
    # Math Route
    elif detected_intent == "Mathematical / Calculation":
        math_result = math_logic.solve_math_problem(search_term)
        return {
            "status": "success", "query": search_term, "language_used": lang,
            "user_intent": detected_intent, "source": "Local Math Engine", "data": math_result
        }
    
    # Fallback Web Search
    try:
        url = f"https://html.duckduckgo.com/html/?q={search_term}&kl={lang}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.post(url, headers=headers, data={"q": search_term})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = [a.text.strip() for a in soup.find_all('a', class_='result__snippet', limit=4)]
            info_content = " ".join(results) if results else "Live search se data nahi mila."
        else:
            info_content = "Web fetching error."
    except Exception as e:
        info_content = f"Error: {str(e)}"

    return {
        "status": "success",
        "query": search_term,
        "language_used": lang,
        "user_intent": detected_intent,
        "source": "Web Search",
        "fetched_information": info_content
    }
