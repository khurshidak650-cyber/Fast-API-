from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="SkAi Multi-Language Info API", version="1.0")

class SearchRequest(BaseModel):
    query: str
    language: str = "en"  # By default English rahega, aap 'hi', 'es', 'ko' bhej sakte hain

@app.get("/")
def read_root():
    return {"status": "online", "message": "Multi-Language Web Information Fetcher is Live!"}

@app.post("/fetch-info")
def fetch_web_info(request: SearchRequest):
    search_term = request.query
    lang = request.language
    
    try:
        # Search query ke sath language parameter set karna
        url = f"https://html.duckduckgo.com/html/?q={search_term}&kl={lang}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.post(url, headers=headers, data={"q": search_term})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for a in soup.find_all('a', class_='result__snippet', limit=5):
                results.append(a.text.strip())
                
            if not results:
                info_content = "Koi direct snippet nahi mila, par multi-language connection active hai."
            else:
                info_content = " ".join(results)
        else:
            info_content = "Internet se data fetch karne me error aayi."

    except Exception as e:
        info_content = f"Error: {str(e)}"

    return {
        "status": "success",
        "language_used": lang,
        "query": search_term,
        "fetched_information": info_content
    }
