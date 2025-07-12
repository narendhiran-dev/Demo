import os
import math
import pandas as pd
import torchaudio
from tqdm import tqdm
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import moviepy as mp
import yake
import json

video_path = "C:/Users/devid/Downloads/Python_AI_Course_Recommender/data/Machine_Learning_for_Everybody.mp4"
audio_path = "temp_audio.wav"
csv_path = "output/video_analysis_output.csv"
duration_seconds = 120

task_suggestion = {
    "linear regression": "Implement a simple linear regression model from scratch in Python using NumPy.",
    "logistic regression": "Find a binary classification dataset (e.g., Titanic) and apply logistic regression using scikit-learn.",
    "neural network": "Build a basic neural network with one hidden layer to classify MNIST digits using TensorFlow or PyTorch.",
    "overfitting": "Explain the concept of overfitting and describe three techniques to prevent it (e.g., regularization, dropout, early stopping).",
    "underfitting": "Describe a scenario where a model is underfitting and what steps you would take to improve its performance.",
    "cost function": "Implement the Mean Squared Error (MSE) cost function in Python.",
    "gradient descent": "Visualize the process of gradient descent on a simple 2D parabola using matplotlib.",
    "supervised learning": "List three examples of supervised learning problems and the algorithms you might use for them.",
    "unsupervised learning": "Research and explain the difference between K-Means and DBSCAN clustering algorithms.",
    "classification": "Train a classifier (like a Decision Tree or SVM) on the Iris dataset and evaluate its accuracy.",
    "data preprocessing": "Take a raw dataset and apply common preprocessing steps: handling missing values, scaling features, and encoding categorical variables."
}
main_task = "Review the key concepts write a paragraph summary."

def extract_audio(video_path, audio_path1):
    video = mp.VideoFileClip(video_path)
    if video.audio is None:
        raise ValueError("No audio found")
    video.audio.write_audiofile(audio_path1)
    print("Audio extracted")

def analyze_text_local(text, top_n = 5):
    kw_extractor = yake.KeywordExtractor(n=3, top=5, top_n=top_n)
    keywords_tuples = kw_extractor.extract_keywords(text)
    keywords = ", ".join([kw[0] for kw in keywords_tuples])

    recommended_task = main_task
    for keyword in keywords.split(", "):
        if keyword in task_suggestion:
            recommended_task = task_suggestion[keyword]
            break
    return keywords, recommended_task

def transcribe_chunk(waveform, sample_rate, processor, model):
    input_features = processor.feature_extractor( waveform.numpy(), sampling_rate=sample_rate, return_tensors="pt")["input_features"]

    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription

def process_video_and_create_csv():
    extract_audio(video_path, audio_path)

    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
    model.eval()

    waveform, sample_rate = torchaudio.load(audio_path)
    total_duration = waveform.shape[1] / sample_rate
    num_chunks = math.ceil(total_duration / duration_seconds)

    processed_data = []

    for i in tqdm(range(num_chunks), desc="Transcribing & Analyzing"):
        start_sample = int(i * duration_seconds * sample_rate)
        end_sample = int(min((i + 1) * duration_seconds * sample_rate, waveform.shape[1]))
        chunk_waveform = waveform[:, start_sample:end_sample]

        transcription = transcribe_chunk(chunk_waveform[0], sample_rate, processor, model)
        keywords, task = analyze_text_local(transcription)

        timestamp = f"{(i * duration_seconds) // 3600:02}:{((i * duration_seconds) % 3600) // 60:02}:{(i * duration_seconds) % 60:02}"

        processed_data.append({
            "timestamp": timestamp,
            "transcript_chunk": transcription.strip(),
            "keywords": keywords,
            "recommended_task": task
        })

    df = pd.DataFrame(processed_data)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    print("Analysis complete")

    os.remove(audio_path)

if __name__ == "__main__":
    process_video_and_create_csv()