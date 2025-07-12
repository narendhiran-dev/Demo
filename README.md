Python AI Course Recommender

Analyze Python course videos, generate transcripts, and recommend practice tasks—all powered by AI. This system provides a fast, searchable API to find relevant educational content based on keywords.

Overview

This project provides a complete pipeline to ingest video files, process them using AI models, and serve the results via a REST API. It is ideal for creating a searchable index of educational video content.

Key Features

🤖 Automatic Transcription: Utilizes OpenAI's Whisper for highly accurate speech-to-text conversion.

🔑 Intelligent Keyword Extraction: Leverages KeyBERT to identify key phrases and topics from video transcripts.

📚 Contextual Task Recommendations: Matches video keywords against a task database to suggest relevant practice exercises.
⚡️ High-Performance API: Built with FastAPI to serve search results quickly and efficiently.

System Architecture

The project is split into two main components: a processing pipeline and an API server.

Generated mermaid
graph TD
    A[Video Files & Task DB] -->|Input to| B(process_videos.py);
    B -->|Generates| C[processed_videos.csv];
    C -->|Loaded by| D(main.py - FastAPI Server);
    D -->|Serves requests from| E{User/Client};
    E -->|Searches via keyword| D;

Project Structure
Generated code
.
├── data/
│   └── input_videos.csv      # REQUIRED: Your list of videos to process
├── output/
│   └── processed_videos.csv  # GENERATED: The processed data
├── process_videos.py         # The main video processing script
├── main.py                   # The FastAPI application
├── task_recommendations.json # REQUIRED: Your database of tasks
├── requirements.txt          # Project dependencies
└── README.md                 # This file

IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
Getting Started

Follow these instructions to set up and run the project locally.

Prerequisites

Python 3.8 or newer.

FFmpeg: This is required by moviepy for audio processing. Download it from ffmpeg.org and ensure the ffmpeg executable is in your system's PATH.

Installation Steps

1. Clone the Repository

Generated bash
git clone https://github.com/your-username/python-ai-course-recommender.git
cd python-ai-course-recommender
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

2. Create and Activate a Virtual Environment

Generated bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS & Linux
python3 -m venv venv
source venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

3. Install Dependencies from requirements.txt
Create a file named requirements.txt in the root of your project with the following content:

Generated txt
# Core Libraries
pandas
openai-whisper
keybert
moviepy

# For KeyBERT backend & performance
torch
torchvision
torchaudio
sentence-transformers

# For the API
fastapi
uvicorn[standard]
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Txt
IGNORE_WHEN_COPYING_END

Now, run the installation command:

Generated bash
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
How to Use the System

The system is run in two stages: first, process the videos, then launch the API.

Step 1: Prepare Input Data

You must create the following two files before running the processor.

A. data/input_videos.csv

Create this file to list the videos you want to process. Use absolute paths to your video files.

Generated csv
course_name,video_path
Python for Beginners,D:/MyCourses/Python_Videos/01_introduction.mp4
Working with NumPy,D:/MyCourses/Python_Videos/02_numpy_basics.mp4
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Csv
IGNORE_WHEN_COPYING_END

B. task_recommendations.json

Create this file to define your database of programming tasks and their associated keywords.

Generated json
{
  "task_1": {
    "task_recommendation": "Compute the factorial of a number using a loop.",
    "keywords": "factorial, loop, for loop, integer"
  },
  "task_2": {
    "task_recommendation": "Create arrays using np.array, np.zeros, and np.arange.",
    "keywords": "numpy, np.array, np.zeros, array"
  }
}
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Json
IGNORE_WHEN_COPYING_END

Important: The process_videos.py and main.py scripts contain hardcoded paths to files. Please update these paths to match your local system's file structure before running.

Step 2: Run the Video Processing Pipeline

Execute the process_videos.py script. This will read your input CSV, analyze each video, and create output/processed_videos.csv.

Generated bash
python process_videos.py
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Note: This is a computationally intensive process and may take a significant amount of time.

Step 3: Launch the API Server

Once processed_videos.csv has been generated, you can start the API.

Generated bash
# Navigate to the app directory
cd app

# Run the server with Uvicorn
uvicorn main:app --reload
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

The API will be available at http://127.0.0.1:8000.

API Usage

You can interact with the API using any HTTP client or your browser.

Search for Videos

Endpoint: /search/

Method: GET

Query Parameter: keyword=<your_search_term>

Example Request using curl:
Generated bash
curl -X GET "http://127.0.0.1:8000/search/?keyword=numpy"
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
Example Request in Browser:

Navigate to: http://127.0.0.1:8000/search/?keyword=numpy

Sample Response:
Generated json
{
  "results": [
    {
      "course_name": "Working with NumPy",
      "video_path": "D:/MyCourses/Python_Videos/02_numpy_basics.mp4",
      "keywords": "numpy array, create arrays, np arange, using numpy",
      "transcript_text": "Today we will explore NumPy and creating arrays...",
      "recommended_tasks": "Create arrays using np.array, np.zeros, and np.arange."
    }
  ]
}
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Json
IGNORE_WHEN_COPYING_END
Future Improvements

Add GPU support for faster transcription with Whisper.

Implement batch processing for handling a large number of videos more efficiently.

Develop a simple web-based user interface for uploading and searching videos.

Containerize the application using Docker for easier deployment.
