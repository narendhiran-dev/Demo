import pandas as pd
import whisper
import os
from moviepy import VideoFileClip
from keybert import KeyBERT
import json

input_csv_path = "data/input_videos.csv"
output_csv_path =  "output/processed_videos.csv"
temp_audio_path = "temp_audio.mp3"

def extract_audio(video_path):
    print(f"Extracting audio {video_path}")
    video_clip = VideoFileClip(video_path) 
    if video_clip.audio is None:
        return None
    video_clip.audio.write_audiofile(temp_audio_path)
    video_clip.close()
    return temp_audio_path

whisper_model = whisper.load_model("base")
def transcribe_audio(audio_path):
    print(f"Transcribing audio: {audio_path}")
    result = whisper_model.transcribe(audio_path, fp16 = False)
    return result['text']

kw_model = KeyBERT()
def extract_keywords(text, top_n=15):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), use_maxsum=True, top_n=top_n)
    return ", ".join([str(kw[0])for kw in keywords if isinstance(kw, (list, tuple)) and len(kw) > 0])

def recommend_tasks(transcript):
    keywords = extract_keywords(transcript)
    with open("C:/Users/devid/Downloads/Python_AI_Course_Recommender/task_recommendations.json") as f:
        task_db = json.load(f)
        matched_tasks = set()
        transcript_keywords = [k.strip().lower() for k in keywords.split(",")]
        for entry in task_db.values():
            if not isinstance(entry, dict):
                continue
            task_keywords = [k.strip().lower() for k in entry.get("keywords", "").split(",")]
            for tk in task_keywords:
                if any(tk in kw or kw in tk for kw in transcript_keywords):
                    matched_tasks.add(entry.get("task_recommendation", ""))
                    break
        return "Recommended Tasks: ".join(sorted(matched_tasks))
        
def main():
    df = pd.read_csv(input_csv_path)
    results = []
    for id, row in enumerate(df.itertuples(index=False), start=1):
        course_name = row[0]
        video_path = row[1]
        
        print(f"Processing video {id}/{len(df)}")

        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
        keywords = extract_keywords(transcript)
        tasks = recommend_tasks(transcript)

        results.append({
            'course_name': course_name,
            'video_path': video_path,
            'transcript_text': transcript,
            'keywords': keywords,
            'recommended_tasks': tasks
        })
            
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

        if results:
            output_df = pd.DataFrame(results)
            output_df.to_csv(output_csv_path, index=True)
            print("Processing complete.")

if __name__ == "__main__":
    main()