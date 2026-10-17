from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="SkAi Web Search & Info API", version="1.0")

class SearchRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Web Information Fetcher is Live!"}

@app.post("/fetch-info")
def fetch_web_info(request: SearchRequest):
    search_term = request.query
    
    try:
        # Example ke taur par hum public search/web page se data fetch kar rahe hain
        # Yahan aap kisi bhi website ya search result URL ko target kar sakte hain
        url = f"https://html.duckduckgo.com/html/?q={search_term}"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.post(url, headers=headers, data={"q": search_term})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # Web page se results extract karna
            for a in soup.find_all('a', class_='result__snippet', limit=5):
                results.append(a.text.strip())
                
            if not results:
                info_content = "Koi direct snippet nahi mila, par connection successful hai."
            else:
                info_content = " ".join(results)
        else:
            info_content = "Internet se data fetch karne me error aayi."

    except Exception as e:
        info_content = f"Error: {str(e)}"

    return {
        "status": "success",
        "query": search_term,
        "fetched_information": info_content
    }
