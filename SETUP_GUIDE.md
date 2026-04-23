# SmartCourse - Quick Start Guide

Complete setup instructions for the SmartCourse Recommendation System.

## 🎯 Quick Overview

SmartCourse has two parts:
1. **Frontend** (React + TypeScript) - User interface
2. **Backend** (Python + Flask) - AI recommendation engine

You need to run BOTH simultaneously.

---

## 🚀 Complete Setup & Run Instructions

### Part 1: Backend Setup (Python Flask API)

#### Step 1: Open Terminal in Backend Directory

```powershell
cd "C:\Users\Moeed Khan\OneDrive\Desktop\FYP\smartcourse-main\smartcourse-main\backend"
```

#### Step 2: Create Virtual Environment

```powershell
python -m venv venv
```

#### Step 3: Configure Environment Variables

The backend requires a `.env` file for configuration. A template is provided:

```powershell
# Copy the example file
Copy-Item .env.example .env
```

**Note:** The default configuration works for development. For production, update the `JWT_SECRET_KEY` in `backend/.env`.

#### Step 4: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

**Note:** You should see `(venv)` prefix in your terminal.

#### Step 5: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- scikit-learn (TF-IDF model)
- sentence-transformers (Neural model)
- Other dependencies

**⏱️ Time:** 2-5 minutes (first time only)

#### Step 6: Start Backend Server

```powershell
python app.py
```

✅ **Backend is ready when you see:**
```
API will be available at: http://localhost:5000
```

**Keep this terminal open!** Backend must run continuously.

---

### Part 2: Frontend Setup (React Application)

#### Step 1: Open NEW Terminal (PowerShell)

Don't close the backend terminal! Open a new one.

#### Step 2: Navigate to Project Root

```powershell
cd "C:\Users\Moeed Khan\OneDrive\Desktop\FYP\smartcourse-main\smartcourse-main"
```

#### Step 3: Install Frontend Dependencies (If Not Already Done)

```powershell
npm install
```

**⏱️ Time:** 1-3 minutes (first time only)

#### Step 4: Start Frontend Development Server

```powershell
npm run dev
```

✅ **Frontend is ready when you see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

---

## 🎉 Access the Application

Open your browser and visit:
```
http://localhost:5173
```

---

## 📋 Daily Usage (After Initial Setup)

You need TWO terminals running simultaneously:

### Terminal 1: Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python app.py
```

### Terminal 2: Frontend
```powershell
npm run dev
```

---

## 🧪 Testing the System

### 1. Check Backend Health

Open browser and visit:
```
http://localhost:5000/api/health
```

Should return:
```json
{
  "status": "healthy",
  "models_loaded": true
}
```

### 2. Test Recommendations

1. Go to **Recommendations** page
2. Enter: "I want to learn Python for data science"
3. Select **Neural Model** or **TF-IDF Model**
4. Click **Search**
5. View top 10 recommended courses with relevance scores

### 3. Compare Models

Try the same query with both models and notice the difference:
- **TF-IDF:** Focuses on exact keyword matches
- **Neural:** Understands semantic meaning and context

---

## 🔍 Features Implemented

### ✅ Professional Web Interface
- **Home Page:** System overview and capabilities
- **Recommendations Page:** 
  - Natural language text input
  - Model selection (TF-IDF vs Neural)
  - Top 10 courses with relevance scores (0-100%)
  - Save functionality for courses
- **Dashboard:** Search history and saved recommendations
- **About Page:** Technical implementation details

### ✅ Flask Backend API
- **POST /api/recommend:** Get course recommendations
- **GET /api/history:** Retrieve search history
- **POST /api/save:** Save course recommendations
- **GET /api/saved:** Get saved recommendations
- **POST /api/compare:** Compare both models side-by-side

### ✅ Machine Learning Models
- **TF-IDF Model:** Keyword-based matching
- **Neural Model:** Semantic understanding (Sentence-BERT)

### ✅ Database
- **SQLite:** Persistent storage for history and saved items

---

## 📊 Project Structure

```
smartcourse-main/
├── backend/                      # Python Flask Backend
│   ├── app.py                   # Main Flask app
│   ├── requirements.txt         # Python dependencies
│   ├── models/                  # ML models
│   │   ├── tfidf_model.py      # TF-IDF recommender
│   │   └── neural_model.py     # Neural recommender
│   ├── database/               # Database handlers
│   │   └── db_handler.py       # SQLite operations
│   └── data/                   # Data management
│       └── course_loader.py    # Course dataset
│
├── src/                         # React Frontend
│   ├── pages/                  # Page components
│   │   ├── Index.tsx          # Home page
│   │   ├── Recommendations.tsx # Recommendations page
│   │   ├── Dashboard.tsx      # Dashboard
│   │   └── About.tsx          # About page
│   ├── components/            # UI components
│   ├── services/              # API service
│   │   └── api.ts            # Backend communication
│   └── ...
│
├── package.json               # Frontend dependencies
└── README.md                 # This file
```

---

## 🛠️ Technologies Used

### Backend
- **Python 3.10+**
- **Flask** - REST API framework
- **scikit-learn** - TF-IDF model
- **Sentence-Transformers** - Neural model (BERT)
- **SQLite** - Database
- **Pandas** - Data manipulation

### Frontend
- **React** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Shadcn/ui** - Component library

---

## ⏱️ Estimated Time to Complete

### Initial Setup
- Backend setup: **5-10 minutes**
- Frontend setup: **3-5 minutes**
- **Total:** ~15 minutes

### Daily Development
- Starting both servers: **2-3 minutes**

---

## 🐛 Common Issues & Solutions

### Issue 1: Backend Won't Start
**Error:** "Python not found" or "pip not found"

**Solution:**
```powershell
# Install Python 3.10+ from python.org
# Verify installation:
python --version
```

### Issue 2: Frontend Can't Connect to Backend
**Error:** "Failed to get recommendations"

**Solution:**
1. Make sure backend is running (Terminal 1)
2. Check backend is at http://localhost:5000
3. Check browser console for CORS errors

### Issue 3: Port Already in Use
**Error:** "Port 5000 is already in use"

**Solution:**
```powershell
# Find and kill the process using port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Issue 4: Virtual Environment Not Activating
**Error:** "Execution of scripts is disabled"

**Solution:**
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 5: Models Taking Too Long to Load
**Issue:** Neural model download is slow

**Solution:**
- First time only: Models download from Hugging Face (~80MB)
- Subsequent runs are fast (models cached)
- Be patient on first run!

---

## 📈 Performance Metrics

- **TF-IDF Model:** ~10-50ms per query
- **Neural Model:** ~50-200ms per query
- **Database:** <5ms for queries
- **First Load:** 30-60 seconds (model initialization)

---

## 🎓 How the Models Work

### TF-IDF Model
1. Converts course descriptions to numerical vectors
2. Measures keyword frequency and importance
3. Matches query keywords to course keywords
4. **Best for:** "Python scikit-learn tutorial"

### Neural Model
1. Uses pre-trained BERT transformer
2. Creates semantic embeddings (384 dimensions)
3. Understands context and meaning
4. **Best for:** "I want to transition to data science"

---

## 📝 API Usage Examples

### Get Recommendations (PowerShell)
```powershell
$body = @{
    query = "machine learning fundamentals"
    model = "neural"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/recommend" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

### Get Search History
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/history" -Method Get
```

---

## 🎯 What's Implemented vs Requirements

| Requirement | Status | Notes |
|------------|--------|-------|
| Professional Web Interface | ✅ Complete | Multi-page React app |
| Home Page | ✅ Complete | Overview and capabilities |
| Recommendations Page | ✅ Complete | Text input, model selection, results |
| User Dashboard | ✅ Complete | History and saved items |
| About Page | ✅ Complete | Technical details |
| Flask Backend API | ✅ Complete | All REST endpoints |
| TF-IDF Model | ✅ Complete | Keyword matching |
| Neural Model | ✅ Complete | Semantic understanding |
| SQLite Database | ✅ Complete | History and saved items |
| Model Comparison | ✅ Complete | Side-by-side comparison |

---

## 🚀 Next Steps

### Phase 2 (If Required)
- [ ] User authentication system
- [ ] Course ratings and reviews
- [ ] Advanced filtering options
- [ ] Personalized recommendations based on history
- [ ] Deploy to cloud (AWS/Azure)

---

## 📞 Support

If you encounter issues:

1. **Check both terminals** - Both must be running
2. **Review error messages** - Backend logs show details
3. **Verify ports** - 5000 (backend), 5173 (frontend)
4. **Restart servers** - Sometimes helps resolve issues

---

## 🎉 You're All Set!

Your SmartCourse Recommendation System is ready to use.

**Test queries to try:**
- "I want to learn Python for data science"
- "web development with React and Node.js"
- "machine learning fundamentals for beginners"
- "cybersecurity and ethical hacking"
- "cloud computing with AWS"

Compare results between TF-IDF and Neural models to see the difference!
