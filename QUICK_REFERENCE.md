# 🚀 SmartCourse - Quick Reference Card

## ⚡ Start Everything (2 Terminals Needed)

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

**Access:** http://localhost:5173

---

## 📋 What Was Changed/Added

### ✅ New Backend Files (All in `backend/` folder)
```
backend/
├── app.py                        ← Main Flask API
├── requirements.txt              ← Python dependencies
├── README.md                     ← Backend docs
├── models/
│   ├── tfidf_model.py           ← TF-IDF recommender
│   └── neural_model.py          ← Neural recommender
├── database/
│   └── db_handler.py            ← SQLite operations
└── data/
    └── course_loader.py         ← Course data (20 courses)
```

### ✅ Updated Frontend Files
- `src/pages/Recommendations.tsx` - Now uses real API
- `src/components/recommendation/ModelToggle.tsx` - Added disabled state
- `src/services/api.ts` - NEW: API communication layer
- `.env` - NEW: API configuration

### ✅ Documentation Files
- `SETUP_GUIDE.md` - Complete setup instructions
- `IMPLEMENTATION_SUMMARY.md` - Full implementation details
- `backend/README.md` - Backend API documentation

---

## 🎯 Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Check if backend is running |
| `/api/recommend` | POST | Get recommendations |
| `/api/history` | GET | Get search history |
| `/api/save` | POST | Save a course |
| `/api/saved` | GET | Get saved courses |
| `/api/compare` | POST | Compare both models |

---

## 🧪 Quick Test

### 1. Check Backend Health
Open browser: http://localhost:5000/api/health

### 2. Test Recommendations
PowerShell:
```powershell
$body = '{"query":"Python data science","model":"neural"}' 
Invoke-RestMethod -Uri "http://localhost:5000/api/recommend" -Method Post -Body $body -ContentType "application/json"
```

### 3. Use Web Interface
1. Go to http://localhost:5173
2. Click "Recommendations"
3. Enter: "I want to learn machine learning"
4. Select model and search

---

## 🔧 First-Time Setup

### Backend (One-Time)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend (If Not Done)
```powershell
npm install
```

---

## 💡 Model Differences

### TF-IDF Model
- **Speed:** Fast (10-50ms)
- **Approach:** Keyword matching
- **Best for:** "Python scikit-learn tutorial"

### Neural Model  
- **Speed:** Medium (50-200ms)
- **Approach:** Semantic understanding
- **Best for:** "I want to transition to AI"

---

## 🐛 Troubleshooting

### Backend Not Starting?
```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Reinstall if needed
pip install -r requirements.txt
```

### Frontend Can't Connect?
1. Check backend is running (Terminal 1)
2. Visit: http://localhost:5000/api/health
3. Check for CORS errors in browser console

### Port Already Used?
```powershell
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## 📊 What's Implemented

- ✅ Professional web interface (React + TypeScript)
- ✅ Natural language search
- ✅ TF-IDF model (keyword-based)
- ✅ Neural model (semantic understanding)
- ✅ Top 10 recommendations with scores
- ✅ Save courses functionality
- ✅ Search history tracking
- ✅ Model comparison
- ✅ SQLite database
- ✅ REST API with 6 endpoints

---

## ⏱️ Time Estimates

- **First-time setup:** 15 minutes
- **Daily startup:** 2-3 minutes  
- **Model loading (first time):** 30-60 seconds
- **Query processing:** <200ms

---

## 📁 Important Files to Know

- **Backend entry:** `backend/app.py`
- **Frontend main:** `src/pages/Recommendations.tsx`
- **API service:** `src/services/api.ts`
- **TF-IDF model:** `backend/models/tfidf_model.py`
- **Neural model:** `backend/models/neural_model.py`
- **Database:** `backend/smartcourse.db` (auto-created)

---

## 🎓 Sample Test Queries

1. "I want to learn Python for data science"
2. "web development with React"
3. "machine learning fundamentals"
4. "cybersecurity and ethical hacking"
5. "cloud computing with AWS"

Compare TF-IDF vs Neural results!

---

## 📖 Full Documentation

- **Setup:** See `SETUP_GUIDE.md`
- **Summary:** See `IMPLEMENTATION_SUMMARY.md`  
- **Backend API:** See `backend/README.md`

---

## ✅ Quick Checklist

Before demo/testing:

- [ ] Backend virtual environment created
- [ ] Python dependencies installed
- [ ] Backend server running (Terminal 1)
- [ ] Frontend server running (Terminal 2)
- [ ] Can access http://localhost:5173
- [ ] Can access http://localhost:5000/api/health
- [ ] Tested at least one search query
- [ ] Tested both TF-IDF and Neural models

---

**🎉 You're ready to go!**
