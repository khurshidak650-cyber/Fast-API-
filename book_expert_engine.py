# ==========================================
# book_expert_engine.py
# SkAi Smart Book Expert & Catalog Indexer
# Lightweight architecture to save storage & act as a master book locator
# ==========================================

BOOK_EXPERT_CATALOG = {
    # ----------------------------------------------------
    # 1. STUDENT ACADEMIC SUBJECT BOOKS (CGBSE / School Level)
    # ----------------------------------------------------
    "school_academics": {
        "expert_domain": "Middle & High School Curriculum (Math, Science, Social Science, Hindi)",
        "key_references": {
            "mathematics": "Algebra, Geometry, Mensuration formulas & NCERT/CGBSE problem-solving steps.",
            "science": "Physics (Force, Motion, Laws), Chemistry (Atoms, Elements), Biology (Plant & Cell systems).",
            "social_science": "History, Civics, Geography (2011 Census data, civic structures, PM schemes)."
        }
    },

    # ----------------------------------------------------
    # 2. WORLD-FAMOUS REFERENCE BOOKS
    # ----------------------------------------------------
    "world_references": {
        "expert_domain": "Advanced Mathematics, Science & CS Reference Index",
        "key_references": {
            "crc_handbook": "Master reference for mathematical tables, formulas, and physical constants.",
            "schaums_outline": "Step-by-step solved problems for calculus, algebra, and advanced engineering math.",
            "clean_code": "Software engineering principles, SOLID guidelines, and maintainable architecture by Robert C. Martin."
        }
    }
}

def find_book_expert_info(query: str):
    q_lower = query.lower()
    
    # Check for Academic / School Book inquiries
    if any(w in q_lower for w in ["school", "student", "subject", "science", "math", "social", "padhai", "cgbse", "class"]):
        return {
            "status": "success",
            "expert_engine": "SkAi Academic Book Expert",
            "catalog_matched": "School Academics",
            "domain_info": BOOK_EXPERT_CATALOG["school_academics"]
        }
        
    # Check for World-Famous Reference Book inquiries
    elif any(w in q_lower for w in ["crc", "schaum", "handbook", "clean code", "reference", "advanced"]):
        return {
            "status": "success",
            "expert_engine": "SkAi Reference Book Expert",
            "catalog_matched": "World References",
            "domain_info": BOOK_EXPERT_CATALOG["world_references"]
        }
        
    # Universal Fallback Locator
    return {
        "status": "success",
        "expert_engine": "SkAi Universal Book Locator",
        "message": "Yeh query general book index ke liye route ki gayi hai. Aap kisi bhi specific subject ya reference book ka naam pooch sakte hain.",
        "available_categories": list(BOOK_EXPERT_CATALOG.keys())
    }
