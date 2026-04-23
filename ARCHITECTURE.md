# SmartCourse System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                   http://localhost:5173                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP Requests
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REACT FRONTEND (Vite)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Pages:                                                   │  │
│  │  - Home (Index.tsx)                                       │  │
│  │  - Recommendations (Recommendations.tsx) 
│  │
│  │  - Dashboard (Dashboard.tsx)                              │  │
│  │  - About (About.tsx)                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Service (api.ts) ◄── NEW                            │  │
│  │  - getRecommendations()                                   │  │
│  │  - getSearchHistory()                                     │  │
│  │  - saveRecommendation()                                   │  │
│  │  - compareModels()                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ REST API Calls
                              │ (JSON over HTTP)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FLASK BACKEND API (Python)                      │
│                   http://localhost:5000                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  app.py - Main Flask Application                         │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  REST API Endpoints:                                │  │  │
│  │  │  - POST /api/recommend                              │  │  │
│  │  │  - GET  /api/history                                │  │  │
│  │  │  - POST /api/save                                    │  │  │
│  │  │  - GET  /api/saved                                   │  │  │
│  │  │  - POST /api/compare                                 │  │  │
│  │  │  - GET  /api/courses                                 │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                    ┌─────────┴─────────┐                        │
│                    │                   │                         │
│                    ▼                   ▼                         │
│  ┌─────────────────────────┐  ┌──────────────────────────┐     │
│  │   ML MODELS             │  │   DATABASE HANDLER       │     │
│  │                         │  │                          │     │
│  │  ┌──────────────────┐  │  │  ┌────────────────────┐ │     │
│  │  │ TF-IDF Model     │  │  │  │ SQLite Database    │ │     │
│  │  │ (tfidf_model.py) │  │  │  │ (db_handler.py)    │ │     │
│  │  │                  │  │  │  │                    │ │     │
│  │  │ • Scikit-learn   │  │  │  │ Tables:            │ │     │
│  │  │ • TfidfVectorizer│  │  │  │ - search_history   │ │     │
│  │  │ • Keyword match  │  │  │  │ - saved_recs       │ │     │
│  │  │ • Fast (10-50ms) │  │  │  └────────────────────┘ │     │
│  │  └──────────────────┘  │  └──────────────────────────┘     │
│  │                         │                                    │
│  │  ┌──────────────────┐  │  ┌──────────────────────────┐     │
│  │  │ Neural Model     │  │  │  COURSE LOADER          │     │
│  │  │ (neural_model.py)│  │  │  (course_loader.py)     │     │
│  │  │                  │  │  │                          │     │
│  │  │ • Sentence-BERT  │  │  │  • Loads courses.json   │     │
│  │  │ • 384-dim embed  │  │  │  • 20 courses default   │     │
│  │  │ • Semantic       │  │  │  • Validates data       │     │
│  │  │ • Slower (50-200)│  │  └──────────────────────────┘     │
│  │  └──────────────────┘  │                                    │
│  └─────────────────────────┘                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Request Flow Diagram

### User Search Flow

```
1. USER ENTERS QUERY
   "I want to learn Python for data science"
   │
   ▼
2. FRONTEND (Recommendations.tsx)
   - User types in SearchInput component
   - Selects model (TF-IDF or Neural)
   - Clicks Search
   │
   ▼
3. API SERVICE (api.ts)
   POST /api/recommend
   Body: { query: "...", model: "neural" }
   │
   ▼
4. FLASK BACKEND (app.py)
   @app.route('/api/recommend')
   - Receives request
   - Validates input
   │
   ├─── If model == "tfidf" ───┐
   │                            ▼
   │                    TF-IDF MODEL
   │                    - Vectorizes query
   │                    - Calculates TF-IDF scores
   │                    - Ranks by cosine similarity
   │                    - Returns top 10
   │                            │
   └─── If model == "neural" ──┤
                                ▼
                        NEURAL MODEL
                        - Encodes query to 384-dim vector
                        - Compares to course embeddings
                        - Ranks by semantic similarity
                        - Returns top 10
                                │
                                ▼
5. DATABASE (db_handler.py)
   - Save search to history
   - Return history_id
   │
   ▼
6. RESPONSE TO FRONTEND
   {
     "success": true,
     "results": [ ...10 courses... ],
     "model": { "type": "...", ... }
   }
   │
   ▼
7. FRONTEND DISPLAYS RESULTS
   - CourseCard components render
   - Relevance scores shown (0-100%)
   - Save buttons available
```

## Data Flow - Model Comparison

```
USER CLICKS "COMPARE MODELS"
│
▼
POST /api/compare
{ query: "machine learning basics" }
│
├─────────────────┬─────────────────┐
│                 │                 │
▼                 ▼                 ▼
TF-IDF Model   Neural Model    Database
│                 │                 │
│ Process query   │ Process query   │ Save history
│ differently     │ differently     │
│                 │                 │
└─────────────────┴─────────────────┘
                  │
                  ▼
          RESPONSE WITH BOTH
          {
            tfidf: { results: [...] },
            neural: { results: [...] }
          }
                  │
                  ▼
          DASHBOARD SHOWS
          SIDE-BY-SIDE COMPARISON
```

## Technology Stack Layers

```
┌────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                     │
│  React • TypeScript • TailwindCSS • Shadcn/ui          │
└────────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│                  APPLICATION LAYER                      │
│  Vite • React Router • API Service • State Management  │
└────────────────────────────────────────────────────────┘
                        │
                        ▼ HTTP/JSON
┌────────────────────────────────────────────────────────┐
│                   API LAYER (REST)                      │
│  Flask • Flask-CORS • JSON Serialization               │
└────────────────────────────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER                   │
│  Recommendation Algorithms • Data Processing           │
└────────────────────────────────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌──────────────────────┐   ┌──────────────────────┐
│   ML MODELS LAYER    │   │   DATA ACCESS LAYER  │
│                      │   │                      │
│ • TF-IDF (sklearn)   │   │ • SQLite             │
│ • Neural (SBERT)     │   │ • Course Data        │
│ • Pandas             │   │ • JSON Parsing       │
└──────────────────────┘   └──────────────────────┘
```

## File Dependencies

```
Frontend Dependencies:
src/pages/Recommendations.tsx
  └── imports src/services/api.ts
  └── imports src/components/recommendation/SearchInput.tsx
  └── imports src/components/recommendation/ModelToggle.tsx
  └── imports src/components/course/CourseCard.tsx

Backend Dependencies:
backend/app.py
  └── imports models/tfidf_model.py
  └── imports models/neural_model.py
  └── imports database/db_handler.py
  └── imports data/course_loader.py

models/tfidf_model.py
  └── uses scikit-learn.TfidfVectorizer
  └── uses pandas.DataFrame

models/neural_model.py
  └── uses sentence_transformers.SentenceTransformer
  └── uses torch (PyTorch)
  └── uses pandas.DataFrame
```

## Model Processing Pipeline

### TF-IDF Pipeline

```
Course Data → Combine text fields → TfidfVectorizer
     │              │                      │
     │              │                      ▼
     │              │              Create vocabulary
     │              │              (234 terms)
     │              │                      │
     │              ▼                      ▼
     │      "Machine Learning        TF-IDF Matrix
     │       course teaches ML"      (20 x 234)
     │              │                      │
     └──────────────┴──────────────────────┘
                    │
                    ▼
User Query → "Python machine learning"
                    │
                    ▼
            Vectorize query → Calculate cosine similarity
                    │                   │
                    ▼                   ▼
            Query Vector         Similarity Scores
            (1 x 234)            [0.85, 0.72, ...]
                                        │
                                        ▼
                                  Rank & Return
                                  Top 10 Courses
```

### Neural Pipeline

```
Course Data → Combine text fields → Sentence-BERT
     │              │                      │
     │              │                      ▼
     │              │              Pre-trained Model
     │              │              (all-MiniLM-L6-v2)
     │              │                      │
     │              ▼                      ▼
     │      "Machine Learning        Embedding Matrix
     │       course teaches ML"      (20 x 384)
     │              │                      │
     └──────────────┴──────────────────────┘
                    │
                    ▼
User Query → "I want to learn ML"
                    │
                    ▼
            Encode query → Calculate cosine similarity
                    │                   │
                    ▼                   ▼
            Query Embedding     Similarity Scores
            (1 x 384)          [0.78, 0.65, ...]
                                        │
                                        ▼
                                  Rank & Return
                                  Top 10 Courses
```

## Deployment Architecture (Future)

```
                    INTERNET
                       │
                       ▼
              ┌────────────────┐
              │  Load Balancer  │
              └────────────────┘
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
┌───────────────┐           ┌───────────────┐
│  Frontend     │           │  Backend      │
│  (Vercel/     │           │  (AWS/Azure)  │
│   Netlify)    │           │               │
│               │◄──────────┤  Flask App    │
│  Static Files │  REST API │  with Gunicorn│
└───────────────┘           └───────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
            ┌───────────────┐              ┌──────────────┐
            │  PostgreSQL   │              │  Redis Cache │
            │  Database     │              │  (Optional)  │
            └───────────────┘              └──────────────┘
```

## System Components Summary

| Component | Technology | Purpose | Status |
|-----------|-----------|---------|--------|
| Frontend UI | React + TS | User interface | ✅ Complete |
| API Layer | Flask | REST endpoints | ✅ Complete |
| TF-IDF Model | Scikit-learn | Keyword matching | ✅ Complete |
| Neural Model | Sentence-BERT | Semantic search | ✅ Complete |
| Database | SQLite | Data persistence | ✅ Complete |
| Course Data | JSON | Course catalog | ✅ Complete |

---

**All components are interconnected and working together!**
