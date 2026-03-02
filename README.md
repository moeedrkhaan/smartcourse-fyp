# Welcome to SmartCourse Project

## Project Overview

SmartCourse is an intelligent course recommendation system that uses machine learning to provide personalized course suggestions based on natural language queries. The system features two distinct AI models (TF-IDF and Neural) for different recommendation approaches.

**Project Type:** Final Year Project (FYP) Prototype  
**Repository:** https://github.com/moeedrkhaan/smartcourse-fyp

## How to Setup and Run

### Prerequisites

- Node.js & npm - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
- Python 3.8 or higher
- Git

### Quick Start

#### Backend Setup (First Time)

```sh
# Navigate to backend directory
cd backend

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Activate virtual environment (Mac/Linux)
source venv/bin/activate

# Configure environment variables (first time only)
# Copy .env.example to .env
cp .env.example .env
# Or on Windows PowerShell:
# Copy-Item .env.example .env

# Install dependencies (first time only)
pip install -r requirements.txt

# Start backend server
python app.py
```

**Note:** After first-time setup, you only need to activate venv and run `python app.py`

#### Frontend Setup (First Time)

```sh
# In a new terminal, navigate to project root
cd smartcourse-main

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Note:** After first-time setup, you only need to run `npm run dev`

### Accessing the Application

- Frontend: http://localhost:8080
- Backend API: http://localhost:5000

## Important Notes

### First-Time Setup
When you first download/clone this project, the following folders will **NOT** be included (they are generated during setup):
- `backend/venv/` - Python virtual environment (created via `python -m venv venv`)
- `node_modules/` - Node.js dependencies (created via `npm install`)
- `backend/smartcourse.db` - SQLite database (automatically created when backend runs)
- `.env` files - Copy from `.env.example` files and configure

These are automatically generated when you follow the setup instructions above.

### Daily Usage
After initial setup, to run the project:

**Backend:**
```sh
cd backend
.\venv\Scripts\Activate.ps1  # Windows
python app.py
```

**Frontend:** (in a new terminal)
```sh
npm run dev
```

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
