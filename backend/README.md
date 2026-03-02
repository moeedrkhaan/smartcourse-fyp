# SmartCourse Recommendation System - Backend API

Python Flask backend for the SmartCourse recommendation system using TF-IDF and Neural (Sentence-BERT) models.

## 🚀 Features

- **Dual Recommendation Models:**
  - **TF-IDF Model:** Keyword-based matching using Term Frequency-Inverse Document Frequency
  - **Neural Model:** Semantic understanding using Sentence-BERT transformers

- **REST API Endpoints:**
  - `/api/recommend` - Get course recommendations
  - `/api/history` - Retrieve search history
  - `/api/save` - Save course recommendations
  - `/api/saved` - Get saved recommendations
  - `/api/compare` - Compare both models side-by-side
  - `/api/courses` - Get all available courses

- **SQLite Database:** Persistent storage for search history and saved recommendations
- **CORS Enabled:** Seamless frontend integration
- **Real-time Processing:** Fresh recommendations for each query

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- 2GB+ RAM (for neural model)
- Internet connection (first-time model downloads)

## 🛠️ Installation

### Step 1: Navigate to Backend Directory

```powershell
cd backend
```

### Step 2: Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

**Note:** First-time installation will download the Sentence-BERT model (~80MB). This is normal and only happens once.

### Step 4: Download spaCy Language Model (Optional)

```powershell
python -m spacy download en_core_web_sm
```

## 🏃 Running the Backend

### Start the Flask Server

```powershell
python app.py
```

You should see:
```
==================================================
SmartCourse Recommendation System - Backend API
==================================================
Initializing database...
✓ Database initialized successfully
Loading course dataset...
  → Using default course dataset
  → Loaded 20 courses from data/courses.json
Initializing TF-IDF model...
  → Training TF-IDF vectorizer...
  → TF-IDF matrix shape: (20, 5000)
  → Vocabulary size: 234
Initializing Neural model (this may take a moment)...
  → Using device: cpu
  → Loading Sentence-BERT model: all-MiniLM-L6-v2
  → Model loaded successfully
  → Embedding dimension: 384
  → Encoding course descriptions (this may take a moment)...
  → Encoded 20 courses
  → Embeddings shape: (20, 384)
✓ All models initialized successfully!

Starting Flask server...
API will be available at: http://localhost:5000
==================================================
```

The API is now running at **http://localhost:5000**

## 📁 Project Structure

```
backend/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── smartcourse.db             # SQLite database (auto-created)
├── models/
│   ├── tfidf_model.py         # TF-IDF recommendation model
│   └── neural_model.py        # Neural (Sentence-BERT) model
├── database/
│   └── db_handler.py          # SQLite database operations
└── data/
    └── course_loader.py       # Course dataset loader
```

## 🔌 API Endpoints

### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-27T10:30:00",
  "models_loaded": true
}
```

### 2. Get Recommendations
```http
POST /api/recommend
Content-Type: application/json

{
  "query": "I want to learn Python for data science",
  "model": "neural"
}
```

**Response:**
```json
{
  "success": true,
  "query": "I want to learn Python for data science",
  "model": {
    "type": "Neural (Sentence-BERT)",
    "description": "Semantic understanding using transformers",
    "strengths": "Understands context and meaning, handles synonyms"
  },
  "results": [
    {
      "id": "6",
      "title": "Python for Data Science and Machine Learning",
      "provider": "University of Michigan",
      "description": "Comprehensive Python course for data science...",
      "level": "Intermediate",
      "duration": "14 weeks",
      "students": "420,000+",
      "rating": 4.8,
      "tags": ["Python", "Data Science", "Pandas", "NumPy"],
      "relevanceScore": 87,
      "model": "neural"
    }
  ],
  "history_id": 1,
  "timestamp": "2026-02-27T10:30:00"
}
```

### 3. Get Search History
```http
GET /api/history?limit=50
```

### 4. Save Recommendation
```http
POST /api/save
Content-Type: application/json

{
  "course_id": "6",
  "query": "Python for data science",
  "model": "neural"
}
```

### 5. Get Saved Recommendations
```http
GET /api/saved?limit=100
```

### 6. Compare Models
```http
POST /api/compare
Content-Type: application/json

{
  "query": "machine learning fundamentals"
}
```

**Response:** Returns results from both TF-IDF and Neural models for comparison.

## 🧪 Testing the API

### Using PowerShell:

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method Get

# Get recommendations
$body = @{
    query = "I want to learn web development"
    model = "neural"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/recommend" -Method Post -Body $body -ContentType "application/json"
```

### Using curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Get recommendations
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"query":"machine learning basics","model":"tfidf"}'
```

## 🎯 Model Comparison

### TF-IDF Model
- **Strengths:** Exact keyword matching, fast processing, interpretable
- **Best for:** Queries with specific technical terms (e.g., "Python scikit-learn tutorial")
- **Processing:** ~10-50ms per query

### Neural Model (Sentence-BERT)
- **Strengths:** Semantic understanding, context-aware, handles synonyms
- **Best for:** Natural language queries (e.g., "I want to transition to data science")
- **Processing:** ~50-200ms per query

## 📊 Database Schema

### search_history
- `id` - Auto-increment primary key
- `query` - Search query text
- `model` - Model used (tfidf/neural)
- `results_count` - Number of results returned
- `timestamp` - When search was performed
- `session_id` - Optional session identifier

### saved_recommendations
- `id` - Auto-increment primary key
- `course_id` - Course identifier
- `course_title` - Course title
- `course_provider` - Course provider
- `query` - Original search query
- `model` - Model used
- `relevance_score` - Relevance score (0-100)
- `timestamp` - When saved

## 🔧 Configuration

### Environment Variables (Optional)

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_PATH=smartcourse.db
MODEL_NAME=all-MiniLM-L6-v2
```

### Custom Course Dataset

Replace the default dataset by creating `backend/data/courses.json`:

```json
[
  {
    "id": "1",
    "title": "Course Title",
    "provider": "Provider Name",
    "description": "Detailed course description",
    "level": "Beginner",
    "duration": "8 weeks",
    "students": "10,000+",
    "rating": 4.5,
    "tags": ["tag1", "tag2"]
  }
]
```

## 🐛 Troubleshooting

### Issue: "Module not found" Error
**Solution:** Make sure virtual environment is activated and dependencies are installed:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Neural Model Download Fails
**Solution:** Check internet connection. The model will be downloaded from Hugging Face on first run.

### Issue: Port 5000 Already in Use
**Solution:** Kill the process or change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: CORS Errors
**Solution:** Flask-CORS is enabled by default. Check that frontend is requesting from correct URL.

## 📈 Performance Tips

1. **First Run:** Initial model loading takes 30-60 seconds. Subsequent runs are faster.
2. **GPU Acceleration:** If you have CUDA-enabled GPU, PyTorch will automatically use it.
3. **Model Caching:** Models are kept in memory for fast inference.
4. **Database:** SQLite is lightweight but for production, consider PostgreSQL.

## 🚀 Production Deployment

For production use:

1. Use a production WSGI server (Gunicorn/uWSGI):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. Set up reverse proxy (Nginx)
3. Use PostgreSQL instead of SQLite
4. Enable proper logging and monitoring
5. Set `debug=False` in app.py

## 📝 Dependencies

- **Flask** (3.0.2) - Web framework
- **Flask-CORS** (4.0.0) - Cross-origin resource sharing
- **pandas** (2.2.0) - Data manipulation
- **scikit-learn** (1.4.0) - TF-IDF vectorization
- **sentence-transformers** (2.3.1) - Neural embeddings
- **spacy** (3.7.4) - NLP toolkit
- **joblib** (1.3.2) - Model serialization
- **numpy** (1.26.3) - Numerical computing

## 📄 License

This project is part of the SmartCourse FYP system.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API endpoint documentation
3. Check Flask logs for error messages
