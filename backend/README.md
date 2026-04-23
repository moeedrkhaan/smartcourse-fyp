# SmartCourse Backend

Flask API for course recommendations.
It supports TF-IDF and Neural Sentence-BERT models, plus auth, history, and saved courses.

## Requirements

- Python 3.10+
- pip

## Setup

```powershell
cd backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

If PowerShell activation is blocked, you can always run using `venv\Scripts\python.exe` directly.

## Run

```powershell
.\venv\Scripts\python.exe app.py
```

API base URL: http://localhost:5000

## Dataset Cleaning

Run the cleaning pipeline on a local file:

```powershell
.\venv\Scripts\python.exe data\fetch_and_clean.py --source-file data\raw\Courses_dataset.csv
```

Or from URL:

```powershell
.\venv\Scripts\python.exe data\fetch_and_clean.py --source-url "https://example.com/courses.csv"
```

Outputs:
- `data/processed/courses_cleaned.csv`
- `data/courses.json`

The app loads data in this order:
1. `data/processed/courses_cleaned.csv`
2. `data/courses.json`
3. Built-in fallback sample in `data/course_loader.py`

## Core Endpoints

- `GET /api/health`
- `POST /api/register`
- `POST /api/login`
- `GET /api/me`
- `POST /api/recommend`
- `POST /api/compare`
- `GET /api/history`
- `POST /api/save`
- `GET /api/saved`
- `GET /api/courses`

## Quick Test

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get
```

## Important Files

- `app.py`: Flask app and routes
- `models/tfidf_model.py`: TF-IDF recommender
- `models/neural_model.py`: Neural recommender
- `database/db_handler.py`: SQLite operations
- `data/course_loader.py`: dataset loading
- `data/fetch_and_clean.py`: raw-to-clean dataset pipeline
