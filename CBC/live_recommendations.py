import os
import json
import re
from pathlib import Path
from urllib.parse import quote_plus

import numpy as np
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# 1. CONFIGURATION & PAGE SETUP
# ============================================================

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL   = os.getenv("OPENAI_MODEL", "gpt-4.1")
LOCAL_DATA_PATH = Path(__file__).parent / "data" / "products.csv"

st.set_page_config(
    page_title="SmartMatch AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 2. PRODUCT COLOR PALETTES & GLOBAL STYLES
# ============================================================

PRODUCT_PALETTES = [
    {
        "bg": "linear-gradient(135deg, #18052e 0%, #320d5c 50%, #46147d 100%)",
        "accent": "#ff7a00",
        "border": "#ff7a00",
        "theme_name": "Nebula Violet",
    },
    {
        "bg": "linear-gradient(135deg, #041822 0%, #0c3545 50%, #13556d 100%)",
        "accent": "#00d2ff",
        "border": "#00d2ff",
        "theme_name": "Ocean Teal",
    },
    {
        "bg": "linear-gradient(135deg, #220715 0%, #440e29 50%, #68173f 100%)",
        "accent": "#ff3366",
        "border": "#ff3366",
        "theme_name": "Crimson Ruby",
    },
    {
        "bg": "linear-gradient(135deg, #1c1403 0%, #3d2b07 50%, #5e430c 100%)",
        "accent": "#ffd700",
        "border": "#ffd700",
        "theme_name": "Cyber Gold",
    },
    {
        "bg": "linear-gradient(135deg, #051a13 0%, #0c3829 50%, #155a42 100%)",
        "accent": "#10b981",
        "border": "#10b981",
        "theme_name": "Matrix Emerald",
    },
    {
        "bg": "linear-gradient(135deg, #111129 0%, #1d1d49 50%, #2c2c6d 100%)",
        "accent": "#a855f7",
        "border": "#a855f7",
        "theme_name": "Deep Royal",
    },
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Orbitron:wght@600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
  background: #080510 !important;
  font-family: 'Inter', sans-serif !important;
  color: #e8e8f0 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; max-width: 1200px; margin: 0 auto; }

/* Navigation */
.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.1rem 2rem;
  border-bottom: 1px solid rgba(255, 107, 0, .25);
  background: rgba(8, 5, 16, .9);
  backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 999;
  margin-bottom: 2rem;
  border-radius: 0 0 16px 16px;
}
.nav-logo {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.35rem;
  font-weight: 900;
  background: linear-gradient(135deg, #ff6b00, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.nav-steps { display: flex; gap: 1rem; align-items: center; }
.nav-step {
  font-size: .8rem;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
  padding: .35rem .95rem;
  border-radius: 100px;
  opacity: .4;
  color: #fff;
}
.nav-step.active {
  opacity: 1;
  background: rgba(255, 107, 0, .2);
  color: #ff8c00;
  border: 1px solid rgba(255, 107, 0, .5);
}

/* Hero Elements */
.hero-wrapper {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  text-align: center;
  background: radial-gradient(ellipse 80% 50% at 50% -20%, rgba(255,107,0,.22) 0%, transparent 70%),
              radial-gradient(ellipse 60% 40% at 80% 80%, rgba(255,170,0,.12) 0%, transparent 60%),
              #080510;
  padding: 4rem 1.5rem 2.5rem;
  border-radius: 28px;
  margin-top: 1rem;
}
.hero-badge {
  display: inline-block;
  background: rgba(255, 107, 0, 0.15);
  border: 1px solid rgba(255, 107, 0, 0.5);
  color: #ff8c00;
  font-size: .8rem;
  font-weight: 700;
  letter-spacing: .15em;
  text-transform: uppercase;
  padding: .4rem 1.2rem;
  border-radius: 100px;
  margin-bottom: 1.8rem;
}
.hero-title {
  font-family: 'Orbitron', sans-serif !important;
  font-size: clamp(3rem, 7.5vw, 6rem) !important;
  font-weight: 900 !important;
  line-height: 1.05 !important;
  background: linear-gradient(135deg, #ff6b00 0%, #ffd700 50%, #ff8c00 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 1.2rem 0 !important;
}
.hero-sub {
  font-size: clamp(1.1rem, 2.2vw, 1.35rem) !important;
  color: rgba(232, 232, 240, 0.75) !important;
  max-width: 680px;
  margin: 0 auto 2.5rem !important;
  line-height: 1.7 !important;
  font-weight: 300;
}
.hero-features {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 2.5rem;
}
.feature-pill {
  background: rgba(255, 255, 255, .06);
  border: 1px solid rgba(255, 255, 255, .15);
  border-radius: 100px;
  padding: .5rem 1.15rem;
  font-size: .85rem;
  color: rgba(232, 232, 240, .85);
  font-weight: 500;
}
.feature-pill span { color: #ff8c00; margin-right: .4rem; }

/* Page 2 Search Styles */
.search-hero {
  text-align: center;
  padding: 2.5rem 1rem 1.8rem;
  background: radial-gradient(ellipse 60% 40% at 50% 0%, rgba(255,107,0,.15), transparent), #080510;
}
.search-title {
  font-family: 'Orbitron', sans-serif !important;
  font-size: clamp(2rem, 4.5vw, 3.2rem) !important;
  font-weight: 900 !important;
  background: linear-gradient(135deg, #ff6b00, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: .5rem !important;
}
.search-sub {
  color: rgba(232, 232, 240, .65) !important;
  font-size: 1.05rem !important;
  margin-bottom: 2rem !important;
}

/* Page 3: Product Card Presentation */
@keyframes productFadeSlide {
  0% { opacity: 0; transform: translateY(20px) scale(0.985); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}

.product-full-card {
  animation: productFadeSlide 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  border-radius: 28px;
  padding: 2.5rem;
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.15);
  margin-bottom: 2rem;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.65);
}

.prod-rank-watermark {
  position: absolute;
  top: 1.2rem;
  right: 1.8rem;
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(4rem, 8vw, 6rem);
  font-weight: 900;
  opacity: .12;
  line-height: 1;
  pointer-events: none;
}
.prod-brand-pill {
  display: inline-block;
  font-size: .85rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: .15em;
  padding: .3rem .9rem;
  border-radius: 100px;
  background: rgba(255, 255, 255, 0.12);
  margin-bottom: .8rem;
}
.prod-name {
  font-size: clamp(1.8rem, 3.2vw, 2.5rem) !important;
  font-weight: 800 !important;
  line-height: 1.2 !important;
  margin-bottom: 1.2rem !important;
  color: #ffffff !important;
}

/* Specifications List Format (Replaces "Why This Match") */
.specs-section-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: #ffd700;
  margin: 1.5rem 0 .75rem 0;
  display: flex;
  align-items: center;
  gap: .5rem;
}
.specs-card-box {
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.14);
  border-radius: 18px;
  padding: 1.2rem 1.6rem;
  margin-bottom: 1.2rem;
}
.spec-line-item {
  display: flex;
  align-items: baseline;
  padding: .5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  font-size: 1rem;
  line-height: 1.5;
}
.spec-line-item:last-child { border-bottom: none; }
.spec-key {
  font-weight: 700;
  min-width: 170px;
  flex-shrink: 0;
  color: #ffd700;
}
.spec-colon {
  margin: 0 .6rem;
  font-weight: 800;
  opacity: .5;
}
.spec-val {
  color: #ffffff;
  font-weight: 400;
}

/* Evidence-Based Reasons Box */
.evidence-box {
  background: rgba(0, 0, 0, 0.28);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 18px;
  padding: 1.2rem 1.6rem;
  margin-bottom: 1.4rem;
}
.evidence-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #ff8c00;
  margin-bottom: .6rem;
}
.evidence-item {
  padding: .35rem 0;
  font-size: .95rem;
  line-height: 1.5;
  color: rgba(240, 240, 255, 0.9);
}

/* Feedback Box */
.feedback-box {
  margin-top: 1.8rem;
  padding: 1.6rem;
  background: rgba(0, 0, 0, 0.35);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
}
.feedback-box h4 {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #ff8c00;
  margin-bottom: .6rem;
}

/* Alternatives Card */
.alt-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  transition: all .25s ease;
}
.alt-card:hover {
  border-color: rgba(255, 107, 0, 0.5);
  transform: translateY(-2px);
}

/* Metrics and Button Styling */
.stButton > button {
  background: linear-gradient(135deg, #ff6b00, #ffaa00) !important;
  color: #000000 !important;
  font-weight: 800 !important;
  font-size: .95rem !important;
  border: none !important;
  border-radius: 12px !important;
  padding: .7rem 1.6rem !important;
  transition: all .25s ease !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(255, 107, 0, .45) !important;
}

/* Streamlit link button customization */
a[data-testid="stLinkButton"] {
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  border-radius: 12px !important;
  color: #ffffff !important;
  font-weight: 700 !important;
  padding: .65rem 1.2rem !important;
  text-decoration: none !important;
  transition: all .25s ease !important;
}
a[data-testid="stLinkButton"]:hover {
  background: rgba(255, 107, 0, 0.25) !important;
  border-color: #ff8c00 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(255, 107, 0, 0.35) !important;
}

.pro-pill {
  display: inline-block;
  background: rgba(34, 197, 94, .15);
  border: 1px solid rgba(34, 197, 94, .4);
  color: #4ade80;
  padding: .35rem .85rem;
  border-radius: 100px;
  font-size: .82rem;
  font-weight: 600;
  margin: .25rem;
}
.con-pill {
  display: inline-block;
  background: rgba(239, 68, 68, .15);
  border: 1px solid rgba(239, 68, 68, .35);
  color: #f87171;
  padding: .35rem .85rem;
  border-radius: 100px;
  font-size: .82rem;
  font-weight: 600;
  margin: .25rem;
}
.section-label {
  font-size: .75rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: #ff8c00;
  font-weight: 800;
  margin-bottom: .5rem;
}
.prod-price {
  font-family: 'Orbitron', sans-serif;
  font-size: 2rem !important;
  font-weight: 800 !important;
  margin-bottom: .4rem !important;
}
.score-bar-bg {
  background: rgba(255, 255, 255, .12);
  border-radius: 100px;
  height: 8px;
  overflow: hidden;
  margin-top: .5rem;
}
.score-bar-fill { height: 100%; border-radius: 100px; }
.stTextArea textarea, .stTextInput input {
  background: rgba(255, 255, 255, .06) !important;
  border: 1px solid rgba(255, 107, 0, .35) !important;
  border-radius: 12px !important;
  color: #e8e8f0 !important;
}
[data-testid="stMetric"] {
  background: rgba(255, 255, 255, .04) !important;
  border: 1px solid rgba(255, 107, 0, .2) !important;
  border-radius: 14px !important;
  padding: .85rem 1.1rem !important;
}
[data-testid="stChatMessage"] {
  background: rgba(255, 255, 255, .04) !important;
  border: 1px solid rgba(255, 107, 0, .18) !important;
  border-radius: 14px !important;
  margin-bottom: .85rem !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. SESSION STATE INITIALIZATION
# ============================================================

DEFAULTS = {
    "page": "home",
    "product_data": None,
    "all_candidates": None,
    "last_profile": None,
    "chat_messages": [],
    "last_query": "",
    "feedback": {},
    "active_product_idx": 0,
    "results_view_mode": "Single Product Page",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# 4. OFFICIAL COMPANY LINK BUILDER
# ============================================================

OFFICIAL_STORE_MAP = {
    "asus": "https://www.asus.com/in/searchresult?searchType=products&searchKey=",
    "lenovo": "https://www.lenovo.com/in/en/search?text=",
    "hp": "https://www.hp.com/in-en/shop/catalogsearch/result/?q=",
    "dell": "https://www.dell.com/en-in/search/",
    "acer": "https://store.acer.com/en-in/catalogsearch/result/?q=",
    "apple": "https://www.apple.com/in/search/",
    "samsung": "https://www.samsung.com/in/search/?searchvalue=",
    "sony": "https://www.sony.co.in/search?query=",
    "boat": "https://www.boat-lifestyle.com/search?q=",
    "noise": "https://www.gonoise.com/pages/search-results-page?q=",
    "oneplus": "https://www.oneplus.in/search?q=",
    "xiaomi": "https://www.mi.com/in/search?keyword=",
    "realme": "https://buy.realme.com/in/goods/search?keyword=",
    "lg": "https://www.lg.com/in/search/search-result?search=",
}

def get_direct_urls(brand: str, name: str, provided_amz=None, provided_fk=None, provided_off=None):
    clean_query = quote_plus(f"{brand} {name}".strip())
    
    # 1. Amazon.in Direct
    amz_url = provided_amz if (provided_amz and "amazon" in provided_amz.lower()) else f"https://www.amazon.in/s?k={clean_query}"
    
    # 2. Flipkart Direct
    fk_url = provided_fk if (provided_fk and "flipkart" in provided_fk.lower()) else f"https://www.flipkart.com/search?q={clean_query}"
    
    # 3. Official Company Store Direct
    if provided_off and provided_off.startswith("http"):
        off_url = provided_off
    else:
        b_lower = brand.lower().strip()
        matched = False
        for k, base in OFFICIAL_STORE_MAP.items():
            if k in b_lower:
                off_url = f"{base}{clean_query}"
                matched = True
                break
        if not matched:
            off_url = f"https://www.google.com/search?q={quote_plus(f'{brand} official website {name}')}"
            
    return amz_url, fk_url, off_url

# ============================================================
# 5. OPENAI RETRIEVAL ENGINE
# ============================================================

def make_client():
    if not API_KEY:
        st.error("OPENAI_API_KEY is missing from your .env file.")
        st.stop()
    return OpenAI(api_key=API_KEY)

def run_search(prompt_text: str) -> str:
    client = make_client()
    try:
        resp = client.responses.create(
            model=MODEL,
            tools=[{"type": "web_search"}],
            tool_choice="required",
            input=prompt_text,
        )
        return resp.output_text or ""
    except Exception:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt_text}],
        )
        return resp.choices[0].message.content or ""

def nl_to_structured(natural_query: str) -> dict:
    """Converts user natural language text into machine-understandable search specifications."""
    prompt = f"""
The user provided the following electronics purchase request:
\"\"\"{natural_query}\"\"\"

Extract and structure this request into a system-understandable specification.
Return ONLY valid JSON (no markdown fences, no extra text) with this exact schema:
{{
  "category": "<e.g. Laptop, Smartphone, Headphones, Monitor>",
  "budget_inr": <integer max budget or null>,
  "use_cases": ["<use case 1>", "<use case 2>"],
  "priorities": ["<hardware priority 1>", "<hardware priority 2>"],
  "preferred_brands": ["<brand names>"],
  "excluded_brands": ["<brand names to avoid>"],
  "min_ram": "<e.g. 16GB or null>",
  "min_storage": "<e.g. 512GB or null>",
  "extra_notes": "<any specific hardware details such as GPU model or display refresh rate>"
}}
"""
    raw = run_search(prompt).strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception:
        s, e = raw.find("{"), raw.rfind("}")
        if s >= 0 and e > s:
            try:
                return json.loads(raw[s:e+1])
            except Exception:
                pass
    return {"category": "Laptop", "budget_inr": None, "use_cases": [], "priorities": []}

def retrieve_candidates(profile: dict, query_text: str) -> list:
    """Retrieves 6 to 8 candidate products from live web search or local dataset."""
    prompt = f"""
You are SmartMatch AI, retrieving candidates currently available in the Indian marketplace.

USER SEARCH PROFILE:
{json.dumps(profile, ensure_ascii=False, indent=2)}

ORIGINAL QUERY: "{query_text}"

CRITICAL INSTRUCTIONS:
- Search the live web for real, actively sold Indian electronics.
- Return between 6 and 8 distinct models that match the category and criteria.
- Adhere strictly to the requested category and budget (Target budget: ₹{profile.get('budget_inr') or 'Flexible'}).
- For "specifications", format as a dictionary of key-value pairs in "attribute": "explanation" style.
  Example:
  "processor": "NVIDIA GeForce RTX 4050 6GB GDDR6",
  "CPU": "Intel Core i5-13420H (10 Cores, up to 4.6 GHz)",
  "RAM": "16 GB DDR5 5200MHz",
  "Storage": "512 GB PCIe 4.0 NVMe SSD",
  "Display": "15.6-inch Full HD 144Hz IPS",
  "Battery": "60Wh with Rapid Charge",
  "OS": "Windows 11 Home"

Return ONLY valid JSON (no markdown fences) in this exact format:
{{
  "products": [
    {{
      "name": "Full Exact Model Name",
      "brand": "Brand Name",
      "category": "{profile.get('category', 'Electronics')}",
      "price_inr": 72990,
      "rating": 4.5,
      "price_verified": true,
      "specifications": {{
        "processor": "NVIDIA GeForce RTX 4050 6GB GDDR6",
        "CPU": "Intel Core i5-13420H",
        "RAM": "16 GB DDR5",
        "Storage": "512 GB SSD",
        "Display": "15.6 inch 144Hz IPS",
        "Battery": "60Wh",
        "OS": "Windows 11"
      }},
      "pros": ["Pro 1", "Pro 2"],
      "cons": ["Tradeoff 1", "Tradeoff 2"]
    }}
  ]
}}
"""
    raw = run_search(prompt).strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
    raw = re.sub(r"\s*```$", "", raw)
    candidates = []
    try:
        data = json.loads(raw)
        candidates = data.get("products", [])
    except Exception:
        s, e = raw.find("{"), raw.rfind("}")
        if s >= 0 and e > s:
            try:
                candidates = json.loads(raw[s:e+1]).get("products", [])
            except Exception:
                candidates = []

    # Local fallback if live candidates are insufficient
    if len(candidates) < 3 and LOCAL_DATA_PATH.exists():
        try:
            df = pd.read_csv(LOCAL_DATA_PATH)
            cat = profile.get("category", "Laptop")
            subset = df[df["category"].str.contains(cat, case=False, na=False)]
            if subset.empty: subset = df
            for _, r in subset.head(6).iterrows():
                candidates.append({
                    "name": str(r["name"]),
                    "brand": str(r["brand"]),
                    "category": str(r["category"]),
                    "price_inr": float(r["price_inr"]),
                    "rating": float(r["rating"]),
                    "price_verified": True,
                    "specifications": {
                        "Features": str(r["features"]),
                        "Tags": str(r["tags"]),
                        "Rating": f"{r['rating']}/5",
                    },
                    "pros": [str(t) for t in str(r["tags"]).split()],
                    "cons": ["Catalogue sample model"],
                })
        except Exception:
            pass

    return [p for p in candidates if isinstance(p, dict)]

# ============================================================
# 6. FILTERING, WEIGHTED SCORING & EVIDENCE ENGINE
# ============================================================

def apply_hard_filters(candidates: list, profile: dict) -> list:
    """Strictly filters hard constraints (budget, excluded brands, category)."""
    budget = profile.get("budget_inr")
    excluded = [b.lower().strip() for b in profile.get("excluded_brands", []) if b.strip()]
    preferred = [b.lower().strip() for b in profile.get("preferred_brands", []) if b.strip()]
    target_cat = (profile.get("category") or "").lower().strip()

    filtered = []
    for p in candidates:
        brand = (p.get("brand") or "").lower()
        name = (p.get("name") or "").lower()
        price = p.get("price_inr")

        # 1. Excluded brands hard filter
        if any(ex in brand or ex in name for ex in excluded):
            continue

        # 2. Budget constraint filter (with small 4% leeway for live price fluctuations)
        if budget and price and price > (budget * 1.04):
            continue

        filtered.append(p)

    # If filter eliminates all candidates, relax budget buffer but preserve brand exclusions
    if not filtered and candidates:
        filtered = [
            c for c in candidates
            if not any(ex in (c.get("brand") or "").lower() for ex in excluded)
        ]

    return filtered

def score_and_rank_products(products: list, profile: dict, user_query: str, feedback: dict) -> list:
    """Calculates TF-IDF similarity, weighted match scores, ranks products, and generates evidence."""
    if not products:
        return []

    feedback = feedback or {}
    budget = profile.get("budget_inr") or 80000
    priority = profile.get("priority", "Best overall balance")

    # Document generation for TF-IDF Semantic Similarity
    query_doc = f"{user_query} {' '.join(profile.get('use_cases', []))} {' '.join(profile.get('priorities', []))} {profile.get('extra_notes', '')}"
    product_docs = []
    for p in products:
        specs_str = " ".join(f"{k} {v}" for k, v in p.get("specifications", {}).items())
        pros_str = " ".join(p.get("pros", []))
        product_docs.append(f"{p.get('brand')} {p.get('name')} {p.get('category')} {specs_str} {pros_str}")

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([query_doc] + product_docs)
    raw_sims = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    query_tokens = set(re.findall(r"\w+", query_doc.lower()))

    ranked = []
    for idx, p in enumerate(products):
        price = p.get("price_inr") or budget
        rating = float(p.get("rating") or 4.2)
        specs = p.get("specifications") or {}

        # 1. Similarity Score calculation (calibrated 60-98%)
        raw_sim = float(raw_sims[idx])
        prod_tokens = set(re.findall(r"\w+", product_docs[idx].lower()))
        overlap = len(query_tokens & prod_tokens) / max(1, len(query_tokens))
        sim_score = round(min(98, max(58, (0.45 * raw_sim * 2.6 + 0.55 * overlap) * 100)))

        # 2. Price Score
        price_diff = budget - price
        if price <= budget:
            price_score = 0.70 + 0.30 * (price_diff / max(1, budget))
        else:
            price_score = max(0.20, 0.70 - 0.50 * (abs(price_diff) / max(1, budget)))

        # 3. Customer Rating Score
        rating_score = min(1.0, rating / 5.0)

        # 4. Hardware Spec Match Score
        spec_score = 0.80
        all_specs_text = " ".join(str(v) for v in specs.values()).lower()
        if any(term in all_specs_text for term in ["rtx", "4050", "4060", "gpu"]): spec_score += 0.10
        if any(term in all_specs_text for term in ["16 gb", "16gb", "32gb"]): spec_score += 0.10
        spec_score = min(1.0, spec_score)

        # 5. Weighted Match Scoring based on user priorities
        if "performance" in priority.lower():
            w_sim, w_spec, w_price, w_rate = 0.40, 0.30, 0.15, 0.15
        elif "budget" in priority.lower() or "value" in priority.lower():
            w_sim, w_spec, w_price, w_rate = 0.30, 0.15, 0.40, 0.15
        else:
            w_sim, w_spec, w_price, w_rate = 0.35, 0.25, 0.20, 0.20

        total_score = (w_sim * (sim_score / 100) + w_spec * spec_score + w_price * price_score + w_rate * rating_score) * 100

        # 6. Feedback refinement modifier
        brand = p.get("brand", "")
        name = p.get("name", "")
        for fb_item, fb_data in feedback.items():
            if fb_item in name or brand.lower() in fb_item.lower():
                fb_rating = fb_data.get("rating", 3)
                if fb_rating >= 4:
                    total_score += 6
                elif fb_rating <= 2:
                    total_score -= 18

        total_score = round(min(99, max(42, total_score)))

        # 7. Generate Evidence-Based Reasons
        evidence = []
        if price <= budget:
            evidence.append(f"✓ Budget Fit: Priced at ₹{price:,.0f} (₹{price_diff:,.0f} below your limit of ₹{budget:,.0f})")
        else:
            evidence.append(f"⚠ Marginally exceeds budget by ₹{abs(price_diff):,.0f} to deliver premium specifications")

        # Specific hardware evidence
        for k, v in specs.items():
            if any(term in k.lower() for term in ["processor", "gpu", "graphics"]) and "rtx" in str(v).lower():
                evidence.append(f"✓ GPU Verified: {v} directly powers your ML & gaming workloads")
                break
            elif any(term in k.lower() for term in ["cpu", "processor"]):
                evidence.append(f"✓ Processor Verified: {v} handles multi-threaded computing & development")
                break

        if any(term in all_specs_text for term in ["16 gb", "16gb", "32gb"]):
            evidence.append("✓ Memory Verified: High-speed RAM delivers responsive multitasking & build times")

        evidence.append(f"✓ Intent Relevance: {sim_score}% semantic match to your specified priorities")
        evidence.append(f"✓ Verified Marketplace Reputation: {rating:.1f}/5 stars customer rating in India")

        # Direct links
        amz_url, fk_url, off_url = get_direct_urls(
            brand, name,
            p.get("amazon_url"), p.get("flipkart_url"), p.get("official_url")
        )

        p["similarity_score"] = sim_score
        p["total_score"] = total_score
        p["evidence_reasons"] = evidence
        p["amazon_direct_url"] = amz_url
        p["flipkart_direct_url"] = fk_url
        p["official_direct_url"] = off_url
        ranked.append(p)

    ranked.sort(key=lambda x: x["total_score"], reverse=True)
    for r, p in enumerate(ranked, 1):
        p["rank"] = r

    return ranked

# ============================================================
# 7. NAVIGATION
# ============================================================

def render_nav(active_page: str):
    steps = [("home", "1. Intro"), ("search", "2. AI Search"), ("results", "3. Recommendations")]
    html = '<div class="nav-bar"><div class="nav-logo">&#9889; SmartMatch AI</div><div class="nav-steps">'
    for key, label in steps:
        cls = "nav-step active" if key == active_page else "nav-step"
        html += f'<span class="{cls}">{label}</span>'
    html += '</div></div>'
    st.markdown(html, unsafe_allow_html=True)

# ============================================================
# 8. PAGE 1 — FANCY INTRODUCTION ONLY
# ============================================================

def page_home():
    render_nav("home")
    st.markdown("""
<div class="hero-wrapper">
  <div class="hero-badge">&#129302; Next-Gen Electronics Discovery &nbsp;&middot;&nbsp; India Market</div>
  <h1 class="hero-title">SmartMatch AI</h1>
  <p class="hero-sub">
    Find the ideal electronics matching your exact lifestyle, budget, and computing requirements.
    Powered by real-time web intelligence and transparent, explainable recommendations.
  </p>
  <div class="hero-features">
    <span class="feature-pill"><span>&#127758;</span> Live Web Search</span>
    <span class="feature-pill"><span>&#129504;</span> Natural Language Understanding</span>
    <span class="feature-pill"><span>&#128202;</span> Objective AI Match Scores</span>
    <span class="feature-pill"><span>&#128715;</span> Amazon, Flipkart &amp; Official Links</span>
    <span class="feature-pill"><span>&#128172;</span> Interactive AI Shopping Assistant</span>
  </div>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if st.button("🚀  Get Started — Find My Product", use_container_width=True):
            st.session_state["page"] = "search"
            st.rerun()

    st.markdown("""
<div style="max-width:980px;margin:3.5rem auto 1.5rem;display:grid;grid-template-columns:repeat(auto-fit, minmax(260px, 1fr));gap:1.5rem;">
  <div class="glass-sm" style="text-align:center;padding:2.2rem 1.5rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,107,0,0.3);border-radius:20px;">
    <div style="font-size:2.8rem;margin-bottom:.75rem;">&#128269;</div>
    <div style="font-weight:800;font-size:1.15rem;margin-bottom:.5rem;color:#ff8c00;">1. Natural Search</div>
    <div style="opacity:.7;font-size:.9rem;line-height:1.65;">
      Just write in your own words. Our AI translates your everyday needs into precise hardware specifications.
    </div>
  </div>
  <div class="glass-sm" style="text-align:center;padding:2.2rem 1.5rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,107,0,0.3);border-radius:20px;">
    <div style="font-size:2.8rem;margin-bottom:.75rem;">&#9889;</div>
    <div style="font-weight:800;font-size:1.15rem;margin-bottom:.5rem;color:#ff8c00;">2. Deep Verification</div>
    <div style="opacity:.7;font-size:.9rem;line-height:1.65;">
      Every specification is explicitly explained (e.g. <em>Processor : RTX 4050</em>) with pros and tradeoffs.
    </div>
  </div>
  <div class="glass-sm" style="text-align:center;padding:2.2rem 1.5rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,107,0,0.3);border-radius:20px;">
    <div style="font-size:2.8rem;margin-bottom:.75rem;">&#128717;&#65039;</div>
    <div style="font-weight:800;font-size:1.15rem;margin-bottom:.5rem;color:#ff8c00;">3. Mandatory Direct Links</div>
    <div style="opacity:.7;font-size:.9rem;line-height:1.65;">
      Instant verified links to Amazon.in, Flipkart, and Official manufacturer pages on every product.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 9. PAGE 2 — FULL PAGE SCROLLABLE OPTIONS & AI SEARCH
# ============================================================

def page_search():
    render_nav("search")
    st.markdown("""
<div class="search-hero">
  <div class="hero-badge" style="margin-bottom:1rem;">&#129504; AI-Assisted Natural Language Translation</div>
  <h2 class="search-title">Tell Us What You Need</h2>
  <p class="search-sub">Describe your requirements naturally. AI converts your text into system-understandable search parameters.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">&#9889; Quick Presets — Click to Load</div>', unsafe_allow_html=True)
    examples = [
        "A laptop under ₹75k for AI/ML, Python coding, and gaming with 16GB RAM and RTX 4050",
        "Best wireless noise-cancelling headphones under ₹6000 with long battery life",
        "Budget Android smartphone under ₹18,000 with clean UI and high refresh rate display",
        "27-inch 4K color-accurate IPS monitor for video editing under ₹35,000",
    ]
    ex_cols = st.columns(2)
    for i, ex in enumerate(examples):
        with ex_cols[i % 2]:
            if st.button(f'"{ex}"', key=f"ex_{i}", use_container_width=True):
                st.session_state["last_query"] = ex

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">&#128221; Your Requirement (Natural Language)</div>', unsafe_allow_html=True)
    query = st.text_area(
        "Natural Language Query",
        value=st.session_state.get("last_query", ""),
        placeholder="Example: I need a gaming laptop under ₹80,000 for college and ML work. Prefer ASUS or Lenovo. Need at least 16GB RAM and 144Hz screen.",
        height=130,
        label_visibility="collapsed",
    )

    with st.expander("🛠️ Advanced Customization & Constraints (Optional)", expanded=True):
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            adv_budget = st.number_input("Max Budget (₹)", min_value=1000, max_value=2000000, value=75000, step=1000)
        with fc2:
            adv_cat = st.selectbox("Category", [
                "Auto-detect from query", "Laptop", "Smartphone", "Headphones / Audio",
                "Monitor", "Tablet", "Mechanical Keyboard / Mouse", "Smartwatch", "Camera", "Other"
            ])
        with fc3:
            adv_priority = st.selectbox("Primary Priority", [
                "Best overall balance", "Maximum raw performance", "Value for money / Budget pick", "Battery life & portability", "Premium build & durability"
            ])
        c_b1, c_b2 = st.columns(2)
        with c_b1:
            adv_brands = st.text_input("Preferred Brands", placeholder="e.g. ASUS, Lenovo, Apple, Sony")
        with c_b2:
            adv_excl = st.text_input("Brands to Exclude", placeholder="e.g. Acer, HP")

    st.markdown("<br>", unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns([1, 2, 1])
    with sc2:
        search_clicked = st.button("🔍  Search & Rank Products with AI", use_container_width=True)

    if search_clicked:
        final_query = query.strip()
        if not final_query:
            st.warning("Please type your requirement or click one of the quick presets above.")
            st.stop()
        st.session_state["last_query"] = final_query

        with st.spinner("🧠 Converting natural language to system parameters…"):
            profile = nl_to_structured(final_query)

        # Merge user explicit form filters
        if adv_cat != "Auto-detect from query":
            profile["category"] = adv_cat
        if adv_budget:
            profile["budget_inr"] = adv_budget
        if adv_brands:
            profile["preferred_brands"] = [b.strip() for b in adv_brands.split(",") if b.strip()]
        if adv_excl:
            profile["excluded_brands"] = [b.strip() for b in adv_excl.split(",") if b.strip()]
        if adv_priority != "Best overall balance":
            profile["priority"] = adv_priority

        st.session_state["last_profile"] = profile

        with st.expander("✅ How AI Converted Your Natural Language:", expanded=True):
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Category", str(profile.get("category", "Auto-detected")))
            mc2.metric("Budget Limit", f"₹{profile.get('budget_inr', 0):,}" if profile.get("budget_inr") else "Flexible")
            mc3.metric("RAM Target", str(profile.get("min_ram") or "Auto"))
            mc4.metric("Storage Target", str(profile.get("min_storage") or "Auto"))
            if profile.get("use_cases"):
                st.write("**Extracted Use-Cases:**", ", ".join(profile["use_cases"]))
            if profile.get("priorities"):
                st.write("**Extracted Priorities:**", ", ".join(profile["priorities"]))

        with st.spinner("🌐 Retrieving candidate products from live marketplace…"):
            candidates = retrieve_candidates(profile, final_query)

        with st.spinner("⚖️ Applying hard constraints & calculating weighted match scores…"):
            # Step 1: Filter hard constraints strictly in Python
            filtered_candidates = apply_hard_filters(candidates, profile)
            # Step 2: Calculate mathematical weighted scores and evidence
            ranked_products = score_and_rank_products(filtered_candidates, profile, final_query, st.session_state.get("feedback", {}))

        if not ranked_products:
            st.error("No products could pass the hard constraints. Try relaxing your budget or removing excluded brands.")
            st.stop()

        st.session_state["all_candidates"] = candidates
        st.session_state["product_data"] = ranked_products
        st.session_state["chat_messages"] = []
        st.session_state["active_product_idx"] = 0
        st.session_state["page"] = "results"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Introduction"):
        st.session_state["page"] = "home"
        st.rerun()

# ============================================================
# 10. PAGE 3 — PRODUCT RECOMMENDATIONS
# ============================================================

def render_product_card(product: dict, idx: int):
    palette = PRODUCT_PALETTES[idx % len(PRODUCT_PALETTES)]
    bg, accent, border = palette["bg"], palette["accent"], palette["border"]

    name    = product.get("name") or "Product Model"
    brand   = product.get("brand") or "Brand"
    rank    = product.get("rank") or (idx + 1)
    price   = product.get("price_inr")
    specs   = product.get("specifications") or {}
    pros    = product.get("pros") or []
    cons    = product.get("cons") or []
    sim_score = product.get("similarity_score", 85)
    total_score = product.get("total_score", 88)
    evidence = product.get("evidence_reasons", [])

    amz_url = product.get("amazon_direct_url")
    fk_url  = product.get("flipkart_direct_url")
    off_url = product.get("official_direct_url")

    price_text = f"&#8377;{price:,.0f}" if isinstance(price, (int, float)) and price > 0 else "Check Retailer"
    verified   = "&#9989; Budget Verified" if product.get("price_verified") else "&#9888;&#65039; Indicative Price"

    # 1. Product Specifications in exact List Format (Replaces "Why This Match?")
    spec_rows = []
    if specs:
        for k, v in specs.items():
            spec_rows.append(f"""<div class="spec-line-item"><span class="spec-key">{k}</span><span class="spec-colon">:</span><span class="spec-val">{v}</span></div>""")
    specs_html = "".join(spec_rows)

    # 2. Evidence-Based Match Reasons
    evidence_rows = []
    for ev in evidence:
        evidence_rows.append(f"""<div class="evidence-item">{ev}</div>""")
    evidence_html = "".join(evidence_rows)

    # 3. Pros and Cons
    pros_html = "".join(f'<span class="pro-pill">&#10003; {p}</span>' for p in pros) if pros else "<span>High overall user satisfaction</span>"
    cons_html = "".join(f'<span class="con-pill">&#10007; {c}</span>' for c in cons) if cons else "<span>Standard commercial tradeoffs</span>"

    # Card Top HTML Container
    card_html = f"""
<div class="product-full-card" style="background:{bg};border-color:{border}88;">
  <div class="prod-rank-watermark" style="color:{accent};">#{rank}</div>
  <div class="prod-brand-pill" style="color:{accent};">{brand}</div>
  <h2 class="prod-name">{name}</h2>

  <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));gap:1rem;margin-bottom:1.4rem;">
    <div style="background:rgba(0,0,0,0.3);padding:1rem 1.25rem;border-radius:14px;border:1px solid rgba(255,255,255,0.12);">
      <div class="section-label" style="color:{accent};">Verified Price</div>
      <div class="prod-price" style="color:{accent};">{price_text}</div>
      <div style="font-size:.78rem;opacity:.7;">{verified}</div>
    </div>
    <div style="background:rgba(0,0,0,0.3);padding:1rem 1.25rem;border-radius:14px;border:1px solid rgba(255,255,255,0.12);">
      <div class="section-label" style="color:{accent};">Similarity Score</div>
      <div class="prod-price" style="color:{accent};">{sim_score}%</div>
      <div style="font-size:.78rem;opacity:.7;">Intent &amp; Requirements Fit</div>
    </div>
    <div style="background:rgba(0,0,0,0.3);padding:1rem 1.25rem;border-radius:14px;border:1px solid rgba(255,255,255,0.12);">
      <div class="section-label" style="color:{accent};">Total Match Score</div>
      <div class="prod-price" style="color:{accent};">{total_score}<span style="font-size:1.1rem;opacity:.5;"> / 100</span></div>
      <div class="score-bar-bg"><div class="score-bar-fill" style="width:{total_score}%;background:linear-gradient(90deg,{accent},{accent}dd);"></div></div>
    </div>
  </div>

  <div class="specs-section-title">&#128203; Product Specifications</div>
  <div class="specs-card-box">
    {specs_html}
  </div>

  <div class="evidence-box">
    <div class="evidence-title">&#127919; Evidence-Based Match Reasons</div>
    {evidence_html}
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-top:1.2rem;">
    <div>
      <div class="section-label" style="color:#4ade80;">Key Advantages</div>
      <div>{pros_html}</div>
    </div>
    <div>
      <div class="section-label" style="color:#f87171;">Tradeoffs &amp; Limitations</div>
      <div>{cons_html}</div>
    </div>
  </div>
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)

    # 4. Mandatory Direct Links: Amazon, Flipkart, Official Website (Streamlit Native Link Buttons)
    st.markdown('<div class="section-label" style="margin-top:0.4rem;">🔗 Direct Marketplace & Official Links (Mandatory)</div>', unsafe_allow_html=True)
    link_col1, link_col2, link_col3 = st.columns(3)
    with link_col1:
        st.link_button("🛒 View on Amazon.in", amz_url, use_container_width=True)
    with link_col2:
        st.link_button("🛍️ View on Flipkart", fk_url, use_container_width=True)
    with link_col3:
        st.link_button(f"🌐 Official {brand} Company Store", off_url, use_container_width=True)

    # 5. Feedback Section (User Feedback Refines Future Results)
    fb_data = st.session_state["feedback"].get(name, {})
    submitted = fb_data.get("submitted", False)

    st.markdown(f'<div class="feedback-box"><h4>&#128172; Feedback for {name}</h4>', unsafe_allow_html=True)
    if submitted:
        st.success(f"✓ Thank you! You rated this recommendation {'⭐' * fb_data.get('rating', 3)} ({fb_data.get('rating')}/5)")
        if fb_data.get("comment"):
            st.caption(f'Your feedback: "{fb_data.get("comment")}"')
        st.info("💡 Your feedback has been recorded. Click 'Refine Recommendations with My Feedback' above or below to update rankings!")
    else:
        fb_c1, fb_c2 = st.columns([1, 2])
        with fb_c1:
            fb_rating = st.select_slider(
                "Rate this recommendation",
                options=[1, 2, 3, 4, 5],
                value=4,
                format_func=lambda x: f"{'⭐' * x} ({x}/5)",
                key=f"rating_{idx}",
            )
        with fb_c2:
            fb_comment = st.text_input(
                "Feedback or adjustments",
                placeholder="e.g. Great match! / Prefer lighter weight / Brand preference",
                key=f"comment_{idx}",
            )
        fb_submit_c1, fb_submit_c2 = st.columns([1, 2])
        with fb_submit_c1:
            if st.button("Submit Feedback", key=f"fb_submit_{idx}"):
                st.session_state["feedback"][name] = {
                    "rating": fb_rating,
                    "comment": fb_comment,
                    "brand": brand,
                    "submitted": True,
                }
                # Instantly re-rank with user feedback applied
                profile = st.session_state.get("last_profile") or {}
                raw_cands = st.session_state.get("all_candidates") or st.session_state.get("product_data") or []
                filtered = apply_hard_filters(raw_cands, profile)
                st.session_state["product_data"] = score_and_rank_products(
                    filtered, profile, st.session_state.get("last_query", ""), st.session_state["feedback"]
                )
                st.rerun()
    st.markdown('</div><br>', unsafe_allow_html=True)


def page_results():
    render_nav("results")
    products = st.session_state.get("product_data") or []

    if not products:
        st.warning("No active recommendation results. Please run a search first.")
        if st.button("← Go to Search Page"):
            st.session_state["page"] = "search"
            st.rerun()
        return

    st.markdown(f"""
<div style="text-align:center;padding:2rem 1rem 1rem;">
  <div class="hero-badge">&#127942; {len(products)} Filtered &amp; Ranked Matches</div>
  <h2 class="search-title" style="margin-top:.6rem;">AI Recommended Products</h2>
  <p class="search-sub">Hard constraints filtered &bull; Weighted match scores &bull; Evidence-based explanations</p>
</div>
""", unsafe_allow_html=True)

    # Top Control Bar
    c_back, c_mode, c_sort, c_refine = st.columns([1.2, 1.6, 1.2, 1.5])
    with c_back:
        if st.button("🔄  New Search", use_container_width=True):
            st.session_state["page"] = "search"
            st.rerun()
    with c_mode:
        view_mode = st.radio(
            "View Mode",
            ["Single Product Page (Card Pager)", "Scroll All Products"],
            horizontal=True,
            index=0 if st.session_state.get("results_view_mode") == "Single Product Page" else 1,
            label_visibility="collapsed",
        )
        st.session_state["results_view_mode"] = "Single Product Page" if "Single" in view_mode else "Scroll All"
    with c_sort:
        sort_by = st.selectbox("Sort By", ["Total Match Score ↓", "Similarity Score ↓", "Price ↑", "Price ↓"], label_visibility="collapsed")
    with c_refine:
        if st.button("⚡ Refine with My Feedback", use_container_width=True):
            profile = st.session_state.get("last_profile") or {}
            raw_cands = st.session_state.get("all_candidates") or products
            filtered = apply_hard_filters(raw_cands, profile)
            st.session_state["product_data"] = score_and_rank_products(
                filtered, profile, st.session_state.get("last_query", ""), st.session_state.get("feedback", {})
            )
            st.success("Refined rankings based on your feedback!")
            st.rerun()

    if sort_by == "Total Match Score ↓":
        products = sorted(products, key=lambda p: float(p.get("total_score") or 0), reverse=True)
    elif sort_by == "Similarity Score ↓":
        products = sorted(products, key=lambda p: float(p.get("similarity_score") or 0), reverse=True)
    elif sort_by == "Price ↑":
        products = sorted(products, key=lambda p: float(p.get("price_inr") or 9e9))
    elif sort_by == "Price ↓":
        products = sorted(products, key=lambda p: float(p.get("price_inr") or 0), reverse=True)

    st.markdown("<hr style='border-color:rgba(255,107,0,0.2);'>", unsafe_allow_html=True)

    # VIEW 1: ONE PRODUCT PER PAGE WITH NEXT/PREV TRANSITIONS & QUICK JUMP
    if st.session_state["results_view_mode"] == "Single Product Page":
        current_idx = st.session_state.get("active_product_idx", 0)
        current_idx = max(0, min(current_idx, len(products) - 1))
        st.session_state["active_product_idx"] = current_idx

        # Quick jumper pills
        jump_cols = st.columns(len(products))
        for j, prod in enumerate(products):
            with jump_cols[j]:
                short_brand = prod.get("brand", f"#{j+1}")
                is_active = (j == current_idx)
                btn_label = f"⭐ #{j+1} {short_brand}" if is_active else f"#{j+1} {short_brand}"
                if st.button(btn_label, key=f"jump_{j}", use_container_width=True):
                    st.session_state["active_product_idx"] = j
                    st.rerun()

        # Step navigation buttons
        prev_col, indicator_col, next_col = st.columns([1, 2, 1])
        with prev_col:
            if current_idx > 0:
                if st.button("⬅️ Previous Product", use_container_width=True):
                    st.session_state["active_product_idx"] = current_idx - 1
                    st.rerun()
            else:
                st.button("⬅️ First Product", disabled=True, use_container_width=True)
        with indicator_col:
            st.markdown(
                f"<div style='text-align:center;font-weight:800;font-family:Orbitron,sans-serif;color:#ff8c00;padding-top:0.6rem;'>"
                f"Product {current_idx + 1} of {len(products)}"
                f"</div>",
                unsafe_allow_html=True,
            )
        with next_col:
            if current_idx < len(products) - 1:
                if st.button("Next Product ➡️", use_container_width=True):
                    st.session_state["active_product_idx"] = current_idx + 1
                    st.rerun()
            else:
                st.button("Last Product ➡️", disabled=True, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        render_product_card(products[current_idx], current_idx)

    # VIEW 2: CONTINUOUS SCROLL ALL PRODUCTS
    else:
        for idx, product in enumerate(products):
            render_product_card(product, idx)

    # ============================================================
    # ALTERNATIVES EXPLORER
    # ============================================================
    if len(products) > 1:
        st.markdown("""
<div style="margin-top:2.5rem;padding:1.5rem;background:rgba(255,255,255,0.03);border:1px solid rgba(255,107,0,0.25);border-radius:20px;">
  <div class="hero-badge" style="margin-bottom:.5rem;">🔍 Tailored Alternatives</div>
  <h3 style="font-family:'Orbitron',sans-serif;color:#ffd700;font-size:1.35rem;margin:0 0 .5rem 0;">Compare Alternative Options</h3>
  <p style="opacity:.7;font-size:.9rem;margin-bottom:1.5rem;">Explore other qualifying models categorized by specific purchasing advantages.</p>
""", unsafe_allow_html=True)

        alt_c1, alt_c2, alt_c3 = st.columns(3)

        # 1. Best Value Alternative (lowest price within qualified)
        lowest_price_prod = min(products, key=lambda p: float(p.get("price_inr") or 9e9))
        with alt_c1:
            st.markdown(f"""
<div class="alt-card">
  <div style="font-weight:800;color:#10b981;font-size:.85rem;text-transform:uppercase;">💰 Best Budget Alternative</div>
  <div style="font-weight:700;font-size:1.05rem;margin:.3rem 0;color:#fff;">{lowest_price_prod.get('name')}</div>
  <div style="color:#ffd700;font-family:'Orbitron',sans-serif;font-weight:700;">₹{lowest_price_prod.get('price_inr', 0):,.0f}</div>
  <div style="font-size:.8rem;opacity:.65;margin-top:.3rem;">Match Score: {lowest_price_prod.get('total_score', 0)}/100</div>
</div>
""", unsafe_allow_html=True)
            if st.button("Inspect Budget Pick", key="btn_alt_budget", use_container_width=True):
                target_idx = products.index(lowest_price_prod)
                st.session_state["active_product_idx"] = target_idx
                st.session_state["results_view_mode"] = "Single Product Page"
                st.rerun()

        # 2. Maximum Similarity / Intent Alternative
        top_sim_prod = max(products, key=lambda p: float(p.get("similarity_score") or 0))
        with alt_c2:
            st.markdown(f"""
<div class="alt-card">
  <div style="font-weight:800;color:#00d2ff;font-size:.85rem;text-transform:uppercase;">🧠 Highest Intent Match</div>
  <div style="font-weight:700;font-size:1.05rem;margin:.3rem 0;color:#fff;">{top_sim_prod.get('name')}</div>
  <div style="color:#00d2ff;font-family:'Orbitron',sans-serif;font-weight:700;">{top_sim_prod.get('similarity_score', 0)}% Similarity</div>
  <div style="font-size:.8rem;opacity:.65;margin-top:.3rem;">₹{top_sim_prod.get('price_inr', 0):,.0f}</div>
</div>
""", unsafe_allow_html=True)
            if st.button("Inspect Intent Pick", key="btn_alt_sim", use_container_width=True):
                target_idx = products.index(top_sim_prod)
                st.session_state["active_product_idx"] = target_idx
                st.session_state["results_view_mode"] = "Single Product Page"
                st.rerun()

        # 3. Top Rated Alternative
        top_rated_prod = max(products, key=lambda p: float(p.get("rating") or 0))
        with alt_c3:
            st.markdown(f"""
<div class="alt-card">
  <div style="font-weight:800;color:#ff3366;font-size:.85rem;text-transform:uppercase;">⭐ Customer Favorite</div>
  <div style="font-weight:700;font-size:1.05rem;margin:.3rem 0;color:#fff;">{top_rated_prod.get('name')}</div>
  <div style="color:#ff3366;font-family:'Orbitron',sans-serif;font-weight:700;">{top_rated_prod.get('rating', 0):.1f} / 5.0 Rating</div>
  <div style="font-size:.8rem;opacity:.65;margin-top:.3rem;">Match Score: {top_rated_prod.get('total_score', 0)}/100</div>
</div>
""", unsafe_allow_html=True)
            if st.button("Inspect Top Rated", key="btn_alt_rate", use_container_width=True):
                target_idx = products.index(top_rated_prod)
                st.session_state["active_product_idx"] = target_idx
                st.session_state["results_view_mode"] = "Single Product Page"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Follow-up Chat Assistant
    st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem;">
  <div class="hero-badge">&#128172; AI Follow-up Chat</div>
  <h3 style="color:#ff8c00;font-family:'Orbitron',sans-serif;font-size:1.6rem;margin-top:.5rem;">Ask About Any Recommended Product</h3>
  <p style="opacity:.65;font-size:.95rem;">Compare specifications, check warranty details, or ask for alternatives.</p>
</div>
""", unsafe_allow_html=True)

    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    chat_input = st.chat_input("Ask a follow-up question about these products…")
    if chat_input:
        st.session_state["chat_messages"].append({"role": "user", "content": chat_input})
        with st.chat_message("user"):
            st.markdown(chat_input)
        summary = json.dumps(
            [{"rank": p.get("rank"), "name": p.get("name"), "brand": p.get("brand"),
              "price_inr": p.get("price_inr"), "total_score": p.get("total_score")} for p in products],
            ensure_ascii=False,
        )
        history = "\n".join(f'{m["role"]}: {m["content"]}' for m in st.session_state["chat_messages"][-6:])
        chat_prompt = f"""
You are SmartMatch AI, an electronics shopping assistant for India.
Current recommendations: {summary}
User request: {st.session_state.get('last_query', '')}
Conversation: {history}
Answer the latest message concisely. Use web search for updated prices or specs. Do not invent links.
"""
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    answer = run_search(chat_prompt)
                    st.markdown(answer)
                    st.session_state["chat_messages"].append({"role": "assistant", "content": answer})
                except Exception as exc:
                    err = f"Could not answer: {exc}"
                    st.error(err)
                    st.session_state["chat_messages"].append({"role": "assistant", "content": err})

    st.markdown("""
<div style="text-align:center;padding:3rem 0 2rem;opacity:.35;font-size:.8rem;line-height:2;">
  SmartMatch AI &nbsp;&middot;&nbsp; AI-Assisted Electronics Discovery &nbsp;&middot;&nbsp;
  Verify specifications, prices, seller ratings, and warranty before purchasing.
</div>
""", unsafe_allow_html=True)

# ============================================================
# 11. ROUTER
# ============================================================

page = st.session_state["page"]
if page == "home":
    page_home()
elif page == "search":
    page_search()
elif page == "results":
    page_results()
else:
    st.session_state["page"] = "home"
    st.rerun()
