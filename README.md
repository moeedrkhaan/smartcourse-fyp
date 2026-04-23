# SmartCourse

SmartCourse is a course recommendation web application.
It includes a React frontend and a Flask backend with two recommendation models:
- TF-IDF (keyword matching)
- Neural Sentence-BERT (semantic matching)

## Tech Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/ui
- Backend: Flask, scikit-learn, sentence-transformers, SQLite

## Project Structure

- `src/`: frontend application
- `backend/`: API, models, database, data pipeline
- `public/`: static assets

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+

## Quick Start

### 1) Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```

Backend runs at: http://localhost:5000

### 2) Frontend

Open a new terminal:

```powershell
cd D:\smartcourse-fyp\smartcourse-main
npm install
npm run dev
```

Frontend runs at: http://localhost:8080 (or the port shown by Vite)

## Dataset Pipeline

To clean a raw dataset and generate app-ready files:

```powershell
cd backend
.\venv\Scripts\python.exe data\fetch_and_clean.py --source-file data\raw\Courses_dataset.csv
```

Output files:
- `backend/data/processed/courses_cleaned.csv`
- `backend/data/courses.json`

## Main Features

- Natural-language course search
- Model toggle (TF-IDF vs Neural)
- Side-by-side comparison mode
- Search history and saved recommendations
- User authentication

## Documentation

- `SETUP_GUIDE.md`: detailed setup
- `ARCHITECTURE.md`: system architecture
- `backend/README.md`: backend details
