import pandas as pd
from fastapi import FastAPI

app = FastAPI()
csv_path = "C:/Users/devid/Downloads/Course Recoomendation System/output/processed_videos.csv"
df = None

@app.on_event("startup")
def load_data():
    global df
    df = pd.read_csv(csv_path)
    df['keywords'] = df['keywords'].astype(str)

@app.get("/search/")
def search_videos(keyword: str):
    if df is None:
        return None
    results = df[df['keywords'].str.contains(keyword, na=False, case=False)]
    expected_columns = ['course_name', 'video_path', 'keywords', 'transcript_text', 'recommended_tasks']
    available_columns = [col for col in expected_columns if col in results.columns]
    if len(available_columns) > 0:
        search_results = results.loc[:, available_columns].to_dict(orient='records')
        return {"results": search_results}
