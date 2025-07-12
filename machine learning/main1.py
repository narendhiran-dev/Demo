import pandas as pd
import re 
from fastapi import FastAPI, HTTPException

app = FastAPI()

csv_path = "video_analysis_output.csv"
df = None

@app.on_event("startup")
def load_data():
    global df
    df = pd.read_csv(csv_path)
    df['keywords'] = df['keywords'].astype(str).str.strip()
    print("CSV loaded")

@app.get("/search")
def search_for_keyword(keyword: str):
    if df is None:
        return {"Data file not loaded"}
    get_keyword = re.escape(keyword.strip())
    pattern = rf'\b{get_keyword}\b'
    results = df[df['keywords'].str.contains(pattern, case=False, regex=True, na=False)]

    found_items = results.loc[:, ['timestamp', 'keywords', 'transcript_chunk']].to_dict('records')

    return {
        "query": keyword,
        "match_count": len(found_items),
        "results": found_items
    }