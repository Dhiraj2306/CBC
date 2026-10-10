from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="SmartMatch AI", page_icon="🛍️", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "products.csv"

st.markdown("""
<style>
.main {background: #f7f9fc;}
[data-testid="stMetric"] {background: white; padding: 14px; border-radius: 12px; border: 1px solid #e7ebf2;}
.product-card {padding: 16px; border: 1px solid #e4e8f0; border-radius: 14px; background: white; margin-bottom: 10px;}
.small-note {color: #5c667a; font-size: 0.9rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_products():
    df = pd.read_csv(DATA_PATH)
    numeric = ["price_inr", "rating", "review_count", "popularity_score"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["features"] = df["features"].fillna("")
    df["tags"] = df["tags"].fillna("")
    return df.dropna(subset=["name", "category", "price_inr", "rating"])

def minmax(series):
    lo, hi = series.min(), series.max()
    if pd.isna(lo) or pd.isna(hi) or hi == lo:
        return pd.Series(1.0, index=series.index)
    return (series - lo) / (hi - lo)

df = load_products()
st.title("🛍️ SmartMatch AI")
st.subheader("Find products that fit your needs — and understand why.")
st.caption("A hackathon prototype for preference-aware recommendations. Demo catalogue contains sample data, not live marketplace prices.")

with st.sidebar:
    st.header("Tell us what matters")
    category = st.selectbox("Product category", ["All categories"] + sorted(df["category"].unique().tolist()))
    budget = st.slider("Maximum budget (₹)", 1000, 150000, 60000, step=1000)
    min_rating = st.slider("Minimum customer rating", 1.0, 5.0, 4.0, step=0.1)
    brand_options = sorted(df["brand"].unique().tolist())
    brands = st.multiselect("Preferred brands (optional)", brand_options)
    query = st.text_input("What will you use it for?", placeholder="e.g. coding, travel, battery, photography")
    st.markdown("### Ranking priorities")
    w_price = st.slider("Low price", 0, 100, 30)
    w_rating = st.slider("Rating", 0, 100, 25)
    w_pop = st.slider("Popularity", 0, 100, 20)
    w_match = st.slider("Use-case match", 0, 100, 25)
    show_all = st.checkbox("Show products even if below minimum rating", value=False)

filtered = df.copy()
if category != "All categories":
    filtered = filtered[filtered["category"] == category]
filtered = filtered[filtered["price_inr"] <= budget]
if not show_all:
    filtered = filtered[filtered["rating"] >= min_rating]
if brands:
    filtered = filtered[filtered["brand"].isin(brands)]

if filtered.empty:
    st.warning("No products match every filter. Try increasing your budget, lowering the minimum rating, or removing brand filters.")
    st.stop()

# Normalize metrics within the current candidate set.
filtered = filtered.copy()
filtered["price_score"] = 1 - minmax(filtered["price_inr"])
filtered["rating_score"] = minmax(filtered["rating"])
filtered["popularity_norm"] = minmax(filtered["popularity_score"])

# Content-based matching: compare the user's use-case text with product tags/features.
corpus = (filtered["tags"].astype(str) + " " + filtered["features"].astype(str)).tolist()
if query.strip():
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus + [query.strip()])
    filtered["match_score"] = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
else:
    filtered["match_score"] = 0.0

weights = np.array([w_price, w_rating, w_pop, w_match], dtype=float)
if weights.sum() == 0:
    weights = np.array([1, 1, 1, 1], dtype=float)
weights = weights / weights.sum()
filtered["recommendation_score"] = (
    weights[0] * filtered["price_score"]
    + weights[1] * filtered["rating_score"]
    + weights[2] * filtered["popularity_norm"]
    + weights[3] * filtered["match_score"]
)
ranked = filtered.sort_values(["recommendation_score", "rating", "review_count"], ascending=False)

tab1, tab2, tab3 = st.tabs(["✨ Recommended for you", "🔥 Popular products", "💰 Best value"])
with tab1:
    st.write(f"Showing **{len(ranked)}** products that meet your current filters.")
    for _, p in ranked.head(12).iterrows():
        reasons = []
        if p["price_score"] >= 0.65: reasons.append("relatively budget-friendly in this result set")
        if p["rating"] >= 4.5: reasons.append(f"strong customer rating ({p['rating']:.1f}/5)")
        if p["popularity_norm"] >= 0.65: reasons.append("high popularity score in the demo catalogue")
        if query.strip() and p["match_score"] > 0: reasons.append("matches some of your use-case keywords")
        if not reasons: reasons.append("best combined score for your selected priorities")
        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.markdown(f"### {p['name']}")
            c1.caption(f"{p['brand']} · {p['category']}")
            c1.write(p["features"])
            c1.markdown("**Why recommended:** " + "; ".join(reasons) + ".")
            c2.metric("Price", f"₹{p['price_inr']:,.0f}")
            c2.metric("Rating", f"{p['rating']:.1f}/5")
            c3.metric("Match score", f"{p['recommendation_score']*100:.0f}/100")
            c3.caption(f"Popularity score: {int(p['popularity_score']):,}")
with tab2:
    popular = df.sort_values(["popularity_score", "review_count"], ascending=False).head(10)
    st.dataframe(popular[["name","category","brand","price_inr","rating","review_count","popularity_score"]], use_container_width=True, hide_index=True)
    st.caption("Popularity score is sample/demo data. It is not verified real purchase volume.")
with tab3:
    value = df.copy()
    value["value_score"] = 0.6 * minmax(value["rating"]) + 0.4 * (1 - minmax(value["price_inr"]))
    value = value.sort_values("value_score", ascending=False).head(10)
    st.dataframe(value[["name","category","brand","price_inr","rating","value_score"]], use_container_width=True, hide_index=True)

st.divider()
st.subheader("How SmartMatch AI works")
st.markdown("""
1. **Filter:** remove products outside the selected category, budget, rating, or brand constraints.
2. **Understand intent:** TF-IDF + cosine similarity estimates whether product tags/features match the use-case text.
3. **Rank:** weighted scoring balances price, rating, popularity, and intent match.
4. **Explain:** each result shows human-readable reasons based on available catalogue fields.
""")
st.info("Important: this starter uses a small synthetic catalogue to demonstrate the workflow. Do not describe its popularity scores as actual sales. Replace sample data with a properly licensed dataset or verified product feed before real-world use.")
