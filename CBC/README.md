# SmartMatch AI — starter project

A small Streamlit prototype for AI/ML-based product discovery and explainable ranking.

## Windows / VS Code setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run this in the same terminal, then activate again:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Data note
`data/products.csv` is an illustrative synthetic dataset made for the prototype. The popularity_score is invented sample data, NOT actual sales. Do not present it as real purchase data.

## AI/ML used
- TF-IDF text vectorization
- Cosine similarity for matching use-case text to product features/tags
- Weighted multi-criteria scoring for recommendations
- Explainable reasons derived from product fields
- Pandas/NumPy for cleaning and scoring

## Next improvements
1. Add a proper user feedback table and SQLite persistence.
2. Use a smaller licensed Amazon Reviews 2023 category dataset to estimate rating/review-based popularity.
3. Add offline evaluation: Precision@K / NDCG@K if user-item relevance labels exist; otherwise use a clearly described hand-labelled test set.
4. Only add live store prices through authorized APIs/affiliate feeds and display last-updated timestamps.
5. Add price history after collecting timestamped, permissioned price observations.

This is a hackathon prototype, not a production marketplace price aggregator.
