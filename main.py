# ==========================================
# main.py
# SkAi Ultimate Master API (No Gemini Key Needed)
# ==========================================
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup
import os
import re

import math_logic
import python_logic
import javascript_logic
import programming_engine

app = FastAPI(title="SkAi Ultimate Master API", version="13.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "").strip()
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "").strip()


class SearchRequest(BaseModel):
    query: str
    language: str = "auto"
    reply_language: Optional[str] = None
    response_style: str = "professional"
    force_google: bool = False
    show_thinking: bool = True


LANGUAGE_NAMES: Dict[str, str] = {
    "hi": "Hindi",
    "hinglish": "Hinglish",
    "en": "English",
    "mr": "Marathi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "kn": "Kannada",
    "ml": "Malayalam",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ar": "Arabic",
}

DDG_REGION_MAP: Dict[str, str] = {
    "hi": "in-hi",
    "hinglish": "in-en",
    "en": "in-en",
    "mr": "in-en",
    "bn": "xa-ar",
    "ta": "in-en",
    "te": "in-en",
    "gu": "in-en",
    "pa": "in-en",
    "kn": "in-en",
    "ml": "in-en",
    "ur": "pk-en",
    "es": "es-es",
    "fr": "fr-fr",
    "de": "de-de",
    "it": "it-it",
    "pt": "pt-pt",
    "ar": "xa-ar",
}

EMOTIONAL_SUPPORT_TEMPLATES: Dict[str, str] = {
    "hi": "मैं समझ सकता हूँ कि अभी समय थोड़ा भारी लग रहा है। आप अकेले नहीं हैं—एक गहरी साँस लें और जो बात सबसे ज़्यादा परेशान कर रही है, उसे साझा करें।",
    "hinglish": "Main samajh sakta hoon ki abhi waqt thoda bhari lag raha hai. Aap akele nahi hain—ek gehri saans lein aur jo baat sabse zyada pareshan kar rahi hai, woh share karein.",
    "en": "I hear that things feel heavy right now. You are not alone—take a slow breath and share what is weighing on you most.",
    "mr": "मला समजते की सध्याचा काळ थोडा कठीण वाटत आहे. तुम्ही एकटे नाही आहात—दीर्घ श्वास घ्या आणि सर्वात जास्त त्रास देणारी गोष्ट सांगा.",
    "es": "Entiendo que este momento se sienta pesado. No estás solo; respira hondo y comparte lo que más te preocupa ahora mismo.",
    "fr": "Je comprends que ce moment soit difficile. Vous n'êtes pas seul ; respirez calmement et partagez ce qui vous pèse le plus.",
}


def has_word(text: str, words: List[str]) -> bool:
    for w in words:
        pattern = r"(?<!\w)" + re.escape(w.lower()) + r"(?!\w)"
        if re.search(pattern, text):
            return True
    return False


def detect_language_profile(text: str) -> Dict[str, str]:
    script_checks = [
        (r"[\u0980-\u09FF]", "bn", "bengali"),
        (r"[\u0B80-\u0BFF]", "ta", "tamil"),
        (r"[\u0C00-\u0C7F]", "te", "telugu"),
        (r"[\u0A80-\u0AFF]", "gu", "gujarati"),
        (r"[\u0A00-\u0A7F]", "pa", "gurmukhi"),
        (r"[\u0C80-\u0CFF]", "kn", "kannada"),
        (r"[\u0D00-\u0D7F]", "ml", "malayalam"),
        (r"[\u0600-\u06FF]", "ur", "arabic_script"),
    ]
    for pattern, code, script_name in script_checks:
        if re.search(pattern, text):
            return {
                "detected_code": code,
                "detected_name": LANGUAGE_NAMES.get(code, code),
                "script_type": script_name,
            }

    if re.search(r"[\u0900-\u097F]", text):
        marathi_markers = ["आहे", "आहेत", "काय", "कसे", "कसा", "कशी", "करू", "मला", "तुम्ही", "आणि", "साठी"]
        if has_word(text, marathi_markers):
            return {"detected_code": "mr", "detected_name": LANGUAGE_NAMES["mr"], "script_type": "devanagari"}
        return {"detected_code": "hi", "detected_name": LANGUAGE_NAMES["hi"], "script_type": "devanagari"}

    lower = text.lower()
    hinglish_markers = [
        "kya", "kaise", "kyun", "kyu", "kise", "banao", "likho", "samjhao",
        "hai", "hain", "me", "mein", "karo", "karna", "aur", "ya", "kuch",
        "bahut", "achha", "accha", "theek", "thik", "mujhe", "tumhe", "aap"
    ]
    if has_word(lower, hinglish_markers):
        return {"detected_code": "hinglish", "detected_name": LANGUAGE_NAMES["hinglish"], "script_type": "latin_roman"}

    if has_word(lower, ["hola", "que", "como", "gracias", "por favor", "ayuda"]):
        return {"detected_code": "es", "detected_name": LANGUAGE_NAMES["es"], "script_type": "latin_roman"}

    if has_word(lower, ["bonjour", "comment", "pourquoi", "merci", "aide"]):
        return {"detected_code": "fr", "detected_name": LANGUAGE_NAMES["fr"], "script_type": "latin_roman"}

    if has_word(lower, ["hallo", "wie", "warum", "danke", "bitte", "hilfe"]):
        return {"detected_code": "de", "detected_name": LANGUAGE_NAMES["de"], "script_type": "latin_roman"}

    if has_word(lower, ["ciao", "come", "perche", "grazie", "aiuto"]):
        return {"detected_code": "it", "detected_name": LANGUAGE_NAMES["it"], "script_type": "latin_roman"}

    return {"detected_code": "en", "detected_name": LANGUAGE_NAMES["en"], "script_type": "latin_roman"}


def resolve_reply_language(detected_code: str, request_lang: str, explicit_reply_lang: Optional[str]) -> Dict[str, str]:
    if explicit_reply_lang:
        code = explicit_reply_lang.strip().lower()
    elif request_lang and request_lang.strip().lower() != "auto":
        code = request_lang.strip().lower()
    else:
        code = detected_code

    lang_label = LANGUAGE_NAMES.get(code, code)
    instruction = f"Respond clearly, naturally, and accurately in {lang_label} ({code})."

    return {
        "reply_language_code": code,
        "reply_language_name": lang_label,
        "ddg_region": DDG_REGION_MAP.get(code, "in-en"),
        "language_instruction": instruction,
    }


def detect_tone(text_lower: str) -> str:
    emotional_words = [
        "sad", "dukhi", "pareshan", "lonely", "depressed", "thak", "dar",
        "दुखी", "परेशान", "उदास", "अकेला", "triste", "cansado"
    ]
    error_words = ["error", "bug", "not working", "kyun nahi chal", "fix", "issue", "एरर"]
    compare_words = ["compare", "vs", "difference", "antar", "fark", "अंतर", "फर्क"]

    if any(w in text_lower for w in emotional_words):
        return "empathetic_support"
    if any(w in text_lower for w in error_words):
        return "diagnostic_helpful"
    if any(w in text_lower for w in compare_words):
        return "analytical_objective"
    return "clear_professional"


def classify_request_type(text_lower: str) -> str:
    if has_word(text_lower, ["code", "banao", "likho", "program", "script", "implement", "function", "कोड", "लिखो", "बनाओ"]):
        return "code_generation"
    if has_word(text_lower, ["calculate", "solve", "area", "volume", "क्षेत्रफल", "आयतन", "formula", "ganit", "math", "गणित", "सूत्र"]):
        return "calculation_or_formula"
    if has_word(text_lower, ["difference", "vs", "compare", "antar", "fark", "comparison", "अंतर", "फर्क"]):
        return "comparison"
    if detect_tone(text_lower) == "empathetic_support":
        return "emotional_support"
    return "concept_explanation"


def analyze_user_intent(text: str, lang_profile: Dict[str, str], reply_lang: Dict[str, str]) -> Dict[str, Any]:
    text_lower = text.lower().strip()
    tone = detect_tone(text_lower)
    request_type = classify_request_type(text_lower)

    stopwords = {
        "kya", "hai", "ka", "ki", "ke", "me", "mein", "aur", "ya", "banao",
        "likho", "samjhao", "please", "what", "is", "are", "how", "to", "in",
        "of", "the", "a", "an", "for", "explain", "tell", "me", "about",
        "क्या", "है", "का", "की", "के", "में", "और", "या", "बताओ", "समझाओ"
    }
    tokens = re.findall(r"[\u0900-\u0D7F\w\+\#]+", text_lower)
    key_terms = [t for t in tokens if t not in stopwords and len(t) > 1][:6]

    if request_type == "emotional_support":
        route_intent = "Emotional / Vulnerable"
        insight = "User needs calm and supportive guidance."
    elif has_word(text_lower, ["python", "decorator", "generator", "oop in python", "pandas", "numpy", "fastapi", "flask", "पायथन"]):
        route_intent = "Python Dedicated Engine"
        insight = "Python concept or code query."
    elif has_word(text_lower, ["javascript", "js", "closure", "prototype", "promise", "async js", "nodejs", "react", "जावास्क्रिप्ट"]):
        route_intent = "JavaScript Dedicated Engine"
        insight = "JavaScript concept or code query."
    elif has_word(text_lower, ["c++", "cpp", "java", "rust", "go", "golang", "c#", "sql", "code", "banao", "likho", "programming", "compiler", "dsa", "algorithm", "कोड", "प्रोग्रामिंग"]):
        route_intent = "Universal Programming Engine"
        insight = "General programming or language query."
    elif request_type == "calculation_or_formula" or any(op in text_lower for op in ["+", "-", "*", "/", "=", "^"]):
        route_intent = "Mathematical / Calculation"
        insight = "Math formula or calculation query."
    else:
        route_intent = "Neutral / General Inquiry"
        insight = "Direct and structured answer needed."

    return {
        "route_intent": route_intent,
        "request_type": request_type,
        "tone": tone,
        "detected_language": lang_profile,
        "reply_language": reply_lang,
        "key_terms": key_terms,
        "insight": insight,
    }


def think_through_question(query: str, analysis: Dict[str, Any], force_google: bool) -> List[str]:
    lang_code = analysis["reply_language"]["reply_language_code"]
    req_type = analysis["request_type"]
    terms = ", ".join(analysis.get("key_terms", [])) or query
    route = analysis["route_intent"]
    use_search = force_google or route == "Neutral / General Inquiry"

    if lang_code == "hi":
        s1 = f"1. प्रश्न समझना: उपयोगकर्ता ने '{query}' पूछा है, जिसका मुख्य विषय '{terms}' है।"
        s2 = f"2. उत्तर का प्रकार: यह '{req_type}' श्रेणी का प्रश्न है, इसलिए मुख्य बात पहले रखी जाएगी।"
        s3 = f"3. स्रोत तय करना: {'लाइव वेब सर्च से तथ्य लेकर उत्तर बनाया जाएगा।' if use_search else f'{route} से प्राप्त जानकारी का उपयोग किया जाएगा।'}"
        return [s1, s2, s3]

    if lang_code == "en":
        s1 = f"1. Understanding the question: The user asked '{query}', focusing on '{terms}'."
        s2 = f"2. Answer strategy: Since this is a '{req_type}' query, I will lead with a clear direct summary followed by points."
        s3 = f"3. Data source: {'Using live web search snippets to build a clear answer.' if use_search else f'Using {route} to solve this accurately.'}"
        return [s1, s2, s3]

    s1 = f"1. Sawaal samajhna: User ne '{query}' pucha hai jiska main focus '{terms}' par hai."
    s2 = f"2. Answer style: Yeh '{req_type}' type ka sawaal hai, isliye pehle seedha jawab aur phir clear points banayenge."
    s3 = f"3. Data source: {'Live search se mile points ko samajh kar jawab tayar karenge.' if use_search else f'{route} ke output ko samajh kar jawab tayar karenge.'}"
    return [s1, s2, s3]


def build_response_blueprint(analysis: Dict[str, Any], style: str) -> Dict[str, Any]:
    req_type = analysis["request_type"]
    tone = analysis["tone"]
    reply_lang = analysis["reply_language"]

    if tone == "empathetic_support":
        sections = ["Warm Acknowledgement", "Calm Perspective", "Small Actionable Step"]
    elif req_type == "code_generation":
        sections = ["Direct Approach", "Clean Code Example", "How It Works", "Next Step"]
    elif req_type == "calculation_or_formula":
        sections = ["Formula", "Step-by-Step Calculation", "Final Result"]
    elif req_type == "comparison":
        sections = ["Quick Summary", "Key Differences", "When to Choose Which"]
    else:
        sections = ["Direct Summary", "Key Points", "Practical Example", "Follow-up Offer"]

    if style == "concise":
        sections = sections[:2]

    return {
        "style": style,
        "tone": tone,
        "reply_language_code": reply_lang["reply_language_code"],
        "reply_language_name": reply_lang["reply_language_name"],
        "language_instruction": reply_lang["language_instruction"],
        "recommended_sections": sections,
        "rules": [
            f"Reply in {reply_lang['reply_language_name']}.",
            "Give a direct answer first, then clear points.",
            "Keep explanation simple and helpful.",
        ],
    }


def build_google_search_query(query: str, analysis: Dict[str, Any]) -> str:
    key_terms = analysis.get("key_terms", [])
    if len(key_terms) >= 2:
        return " ".join(key_terms)
    return query.strip()


def search_google(query: str, analysis: Dict[str, Any], num_results: int = 5) -> Dict[str, Any]:
    optimized_query = build_google_search_query(query, analysis)
    reply_lang = analysis["reply_language"]
    items: List[Dict[str, str]] = []

    if GOOGLE_SEARCH_API_KEY and GOOGLE_CSE_ID:
        try:
            api_url = "https://www.googleapis.com/customsearch/v1"
            params = {
                "key": GOOGLE_SEARCH_API_KEY,
                "cx": GOOGLE_CSE_ID,
                "q": optimized_query,
                "num": min(max(num_results, 1), 10),
            }
            resp = requests.get(api_url, params=params, timeout=10)
            if resp.status_code == 200:
                payload = resp.json()
                for entry in payload.get("items", [])[:num_results]:
                    items.append({
                        "title": entry.get("title", "").strip(),
                        "snippet": re.sub(r"\s+", " ", entry.get("snippet", "")).strip(),
                        "link": entry.get("link", "").strip(),
                    })
                return {
                    "provider": "Google Custom Search API",
                    "search_query_used": optimized_query,
                    "results": items,
                }
        except requests.RequestException:
            pass

    try:
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.post(
            url,
            headers=headers,
            data={"q": optimized_query, "kl": reply_lang["ddg_region"]},
            timeout=10,
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for res in soup.select(".result")[:num_results]:
                title_el = res.select_one(".result__title a")
                snip_el = res.select_one(".result__snippet")
                title = title_el.get_text(" ", strip=True) if title_el else ""
                link = title_el.get("href", "").strip() if title_el else ""
                snippet = re.sub(r"\s+", " ", snip_el.get_text(" ", strip=True)) if snip_el else ""
                if title or snippet:
                    items.append({"title": title, "snippet": snippet, "link": link})
    except requests.RequestException as e:
        return {
            "provider": "Fallback Search Error",
            "search_query_used": optimized_query,
            "error": str(e),
            "results": [],
        }

    return {
        "provider": "Fallback Web Search",
        "search_query_used": optimized_query,
        "results": items,
    }


def synthesize_search_answer(query: str, search_data: Dict[str, Any], blueprint: Dict[str, Any]) -> Dict[str, Any]:
    results = search_data.get("results", [])
    if not results:
        return {
            "direct_answer": "Search se is sawaal par seedha data nahi mila. Kripya sawaal ko thoda aur specific ya simple likhein.",
            "key_points": [],
            "sources": [],
            "answer_guide": blueprint,
        }

    key_points = [r["snippet"] for r in results if r.get("snippet")][:3]
    direct_answer = key_points[0] if key_points else results[0].get("title", "")
    sources = [
        {"title": r.get("title", ""), "link": r.get("link", "")}
        for r in results
        if r.get("link")
    ][:3]

    return {
        "direct_answer": direct_answer,
        "key_points": key_points,
        "sources": sources,
        "answer_guide": blueprint,
    }


def _extract_bullets_from_any(obj: Any, depth: int = 0) -> List[str]:
    if depth > 3 or obj is None:
        return []
    if isinstance(obj, str):
        clean = re.sub(r"\s+", " ", obj).strip()
        return [clean] if clean else []
    if isinstance(obj, list):
        out: List[str] = []
        for item in obj[:5]:
            out.extend(_extract_bullets_from_any(item, depth + 1))
        return out[:6]
    if isinstance(obj, dict):
        lines: List[str] = []
        priority_keys = ["direct_answer", "summary", "explanation", "answer", "result", "formula", "code", "output", "message"]
        for k in priority_keys:
            if k in obj and obj[k]:
                val_str = re.sub(r"\s+", " ", str(obj[k])).strip()
                if val_str:
                    lines.append(f"{k.replace('_', ' ').title()}: {val_str}")
        if not lines:
            for k, v in list(obj.items())[:5]:
                if v:
                    val_str = re.sub(r"\s+", " ", str(v)).strip()
                    lines.append(f"{k.replace('_', ' ').title()}: {val_str}")
        if "key_points" in obj and isinstance(obj["key_points"], list):
            for kp in obj["key_points"][:3]:
                kp_clean = re.sub(r"\s+", " ", str(kp)).strip()
                if kp_clean:
                    lines.append(kp_clean)
        return lines[:6]
    return [str(obj)]


def compose_smart_answer(
    query: str,
    analysis: Dict[str, Any],
    blueprint: Dict[str, Any],
    raw_data: Any,
) -> str:
    lang_code = analysis["reply_language"]["reply_language_code"]
    req_type = analysis["request_type"]

    if req_type == "emotional_support" and isinstance(raw_data, dict) and "message" in raw_data:
        return str(raw_data["message"])

    bullets = _extract_bullets_from_any(raw_data)
    if not bullets:
        if lang_code == "hi":
            return f"'{query}' के लिए फिलहाल कोई सीधा उत्तर नहीं मिल सका। कृपया प्रश्न को थोड़ा और स्पष्ट लिखें।"
        if lang_code == "en":
            return f"I couldn't find a direct answer for '{query}'. Please try rephrasing with a bit more detail."
        return f"'{query}' ke liye abhi seedha jawab nahi mil paaya. Kripya sawaal ko thoda aur clear likhein."

    lead = bullets[0]
    rest = bullets[1:4]

    if lang_code == "hi":
        heading_main = "मुख्य उत्तर"
        heading_points = "महत्वपूर्ण बिंदु"
        footer = "यदि आप इसे और सरल उदाहरण या गहराई से समझना चाहते हैं, तो पूछें।"
    elif lang_code == "en":
        heading_main = "Direct Answer"
        heading_points = "Key Points"
        footer = "Let me know if you want a simpler example or a deeper breakdown."
    else:
        heading_main = "Main Jawab"
        heading_points = "Zaroori Points"
        footer = "Agar iska aasan example ya aur detail chahiye to batayein."

    parts = [f"**{heading_main}:**\n{lead}"]
    if rest:
        formatted_bullets = "\n".join(f"- {item}" for item in rest)
        parts.append(f"**{heading_points}:**\n{formatted_bullets}")
    if blueprint.get("style") != "concise":
        parts.append(footer)

    return "\n\n".join(parts)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "SkAi Multi-Engine Backend is Live!",
        "google_api_configured": bool(GOOGLE_SEARCH_API_KEY and GOOGLE_CSE_ID),
    }


@app.post("/fetch-info")
def fetch_web_info(request: SearchRequest):
    search_term = request.query.strip()

    if not search_term:
        return {    if not search_term:
        return {
            "status": "error",
            "message": "Query is empty."
}
       
