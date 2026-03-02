# Welcome to SmartCourse Project

## Project Overview

SmartCourse is an intelligent course recommendation system that uses machine learning to provide personalized course suggestions based on natural language queries. The system features two distinct AI models (TF-IDF and Neural) for different recommendation approaches.

## How to Setup and Run

### Prerequisites

- Node.js & npm - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
- Python 3.8 or higher
- Git

### Quick Start

#### Backend Setup

```sh
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python app.py
```

#### Frontend Setup

```sh
# In a new terminal, navigate to project root
cd smartcourse-main

# Install dependencies
npm install

# Start development server
npm run dev
```

### Accessing the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## Project Structure

```
smartcourse-main/
├── backend/                 # Python Flask API
│   ├── models/             # ML recommendation models
│   ├── database/           # Database handlers
│   └── data/               # Course data
├── src/                    # React frontend
│   ├── components/         # UI components
│   ├── pages/              # Application pages
│   └── services/           # API services
└── public/                 # Static assets
```

## Technologies Used

### Frontend
- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

### Backend
- Python 3
- Flask
- scikit-learn (TF-IDF Model)
- Sentence-BERT (Neural Model)
- SQLite

## Features

- Natural language course search
- Two AI recommendation models (TF-IDF and Neural)
- User search history and saved recommendations
- Model comparison capability
- Real-time recommendations

## Documentation

For detailed information, see:
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup instructions
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture details
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation overview
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference card
