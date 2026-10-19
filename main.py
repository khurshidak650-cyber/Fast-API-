from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import re
import math_logic

app = FastAPI(title="SkAi Ultimate Master API with Local Math Engine", version="4.0")

class SearchRequest(BaseModel):
    query: str
    language: str = "hi"  # Default language

def analyze_user_intent(text: str):
    text_lower = text.lower()
    
    # 1. Math & Calculation Intent Detection
    if any(word in text_lower for word in ["math", "ganit", "formula", "calculate", "solve", "+", "-", "*", "/", "area", "volume", "क्षेत्रफल", "आयतन", "परिमेय", "rational", "fraction", "bhinn", "algebra"]):
        return "Mathematical / Calculation", "User math ka koi formula, calculation ya concept samajhna chahta hai."
    
    # 2. Emotional / Psychology Intent Detection
    elif any(word in text_lower for word in ["sad", "dukhi", "pareshan", "lonely", "depressed", "rona"]):
        return "Emotional / Vulnerable", "User ko empathy, support aur ek dost ki tarah samjhne ki zaroorat hai."
    
    # 3. Curious / Analytical Detection
    elif any(word in text_lower for word in ["why", "kaise", "kya", "explain", "soch", "mind", "psychology"]):
        return "Curious / Analytical", "User deep information aur logical explanation chahta hai."
    
    # 4. Greetings
    elif any(word in text_lower for word in ["hello", "hi", "hey", "namaste"]):
        return "Friendly / Greeting", "User ke sath warm aur welcoming tone me baat karni chahiye."
    
    else:
        return "Neutral / General Inquiry", "Direct aur helpful information deni chahiye."

@app.get("/")
def read_root():
    return {"status": "online", "message": "SkAi Ultimate Backend with Local Math Engine & Psychology is Live!"}

@app.post("/fetch-info")
def fetch_web_info(request: SearchRequest):
    search_term = request.query
    lang = request.language
    
    # Detect intent
    detected_intent, intent_insight = analyze_user_intent(search_term)
    
    # If math intent, pull directly from our local math_logic.py without searching web!
    if detected_intent == "Mathematical / Calculation":
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
    
    # Otherwise, execute web search for general or psychological queries
    try:
        url = f"https://html.duckduckgo.com/html/?q={search_term}&kl={lang}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.post(url, headers=headers, data={"q": search_term})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for a in soup.find_all('a', class_='result__snippet', limit=4):
                results.append(a.text.strip())
                
            if not results:
                info_content = "Live search se direct data nahi mila."
            else:
                info_content = " ".join(results)
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
