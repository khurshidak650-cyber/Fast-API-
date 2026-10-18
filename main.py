from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="SkAi Psychology & Info API", version="2.0")

class SearchRequest(BaseModel):
    query: str
    language: str = "hi"  # Default language

def analyze_human_psychology(text: str):
    text_lower = text.lower()
    
    # Basic Psychology & Intent Analysis Rules
    if any(word in text_lower for word in ["sad", "dukhi", "pareshan", "lonely", "depressed", "rona"]):
        mood = "Emotional / Vulnerable"
        psychology_note = "User ko empathy, support aur ek dost ki tarah samjhne ki zaroorat hai."
    elif any(word in text_lower for word in ["why", "kaise", "kya", "explain", "soch", "mind", "psychology"]):
        mood = "Curious / Analytical"
        psychology_note = "User deep information aur logical explanation chahta hai."
    elif any(word in text_lower for word in ["hello", "hi", "hey", "namaste"]):
        mood = "Friendly / Greeting"
        psychology_note = "User ke sathwarm aur welcoming tone me baat karni chahiye."
    else:
        mood = "Neutral / General Inquiry"
        psychology_note = "Direct aur helpful information deni chahiye."
        
    return mood, psychology_note

@app.get("/")
def read_root():
    return {"status": "online", "message": "SkAi Psychology & Multi-Language Backend is Live!"}

@app.post("/fetch-info")
def fetch_web_info(request: SearchRequest):
    search_term = request.query
    lang = request.language
    
    # Human Psychology Analysis apply karna
    detected_mood, psych_insight = analyze_human_psychology(search_term)
    
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
                info_content = "Live search se direct data nahi mila, par psychology analysis active hai."
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
        "user_mood": detected_mood,
        "psychology_insight": psych_insight,
        "fetched_information": info_content
    }
