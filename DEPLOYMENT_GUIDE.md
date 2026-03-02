# 🚀 SmartCourse Deployment Guide

## Overview

SmartCourse requires deploying two separate components:
1. **Frontend** (React/Vite) → Vercel
2. **Backend** (Flask/Python) → Render or Railway

---

## 📦 **Option 1: Vercel + Render (Recommended)**

### Part A: Deploy Backend to Render (Free Tier)

#### Step 1: Prepare Backend for Deployment

1. **Create `render.yaml` in project root:**

```yaml
services:
  - type: web
    name: smartcourse-backend
    env: python
    region: oregon
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11.0
    healthCheckPath: /api/health
```

2. **Add `gunicorn` to `backend/requirements.txt`:**

```txt
Flask==3.0.2
Flask-CORS==4.0.0
Flask-JWT-Extended==4.6.0
bcrypt==4.1.2
pandas>=2.0.0
scikit-learn>=1.3.0
sentence-transformers>=2.2.0
joblib>=1.3.0
numpy>=1.24.0
python-dotenv>=1.0.0
gunicorn>=21.2.0
```

3. **Update `backend/app.py` for production:**

Change the last line from:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

To:
```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

#### Step 2: Deploy to Render

1. **Sign up at [render.com](https://render.com)** (free with GitHub)

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository: `smartcourse-main`

3. **Configure Service:**
   - **Name:** `smartcourse-backend`
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free

4. **Add Environment Variables:**
   - `FLASK_ENV` = `production`
   - `JWT_SECRET_KEY` = `your-secure-random-string-here`
   - `PYTHON_VERSION` = `3.11`

5. **Deploy:**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Note your backend URL (e.g., `https://smartcourse-backend.onrender.com`)

⚠️ **Note:** Render free tier spins down after inactivity. First request after inactivity takes ~30 seconds.

---

### Part B: Deploy Frontend to Vercel

#### Step 1: Update Frontend Configuration

1. **Update `.env` file:**

```env
# Replace with your Render backend URL
VITE_API_BASE_URL=https://smartcourse-backend.onrender.com/api
```

2. **Create `vercel.json` in project root:**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

#### Step 2: Deploy to Vercel

1. **Sign up at [vercel.com](https://vercel.com)** (free with GitHub)

2. **Import Project:**
   - Click "Add New..." → "Project"
   - Import from GitHub
   - Select `smartcourse-main` repository

3. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `./` (leave default)
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `dist` (auto-detected)

4. **Add Environment Variable:**
   - Click "Environment Variables"
   - Add: `VITE_API_BASE_URL` = `https://smartcourse-backend.onrender.com/api`

5. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app will be live at `https://smartcourse-main.vercel.app` (or similar)

---

## 📦 **Option 2: Railway (Alternative - Both Frontend & Backend)**

Railway can host both frontend and backend on one platform.

### Step 1: Prepare for Railway

1. **Sign up at [railway.app](https://railway.app)**

2. **Create `railway.json`:**

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy

1. **New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `smartcourse-main`

2. **Add Environment Variables:**
   - `JWT_SECRET_KEY` = generate secure key
   - `FLASK_ENV` = `production`

3. **Deploy:**
   - Railway auto-detects and deploys
   - Get your deployment URL

⚠️ **Note:** Railway free tier has monthly limits ($5 credit, ~500 hours).

---

## 📦 **Option 3: PythonAnywhere (Backend Only)**

Good for Python backends but limited free tier.

### Steps:

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your backend code
3. Create a web app with Flask
4. Configure WSGI file
5. Install dependencies in virtual environment

**Limitations:**
- Manual setup required
- Limited CPU on free tier (Neural model will be slow)
- No always-on support on free tier

---

## 🗄️ **Database Considerations**

Your SQLite database won't persist well on serverless platforms. For production:

### Option A: Use PostgreSQL (Recommended)

1. **Free PostgreSQL hosting:**
   - [Supabase](https://supabase.com) (free tier)
   - [ElephantSQL](https://www.elephantsql.com) (free tier)
   - [Railway](https://railway.app) (includes PostgreSQL)

2. **Update code to use PostgreSQL:**
   - Install: `pip install psycopg2-binary`
   - Update `db_handler.py` to use PostgreSQL connection

### Option B: Keep SQLite (Simple, but limited)

For FYP demo purposes, SQLite works but:
- Data resets on each deployment
- Not ideal for production
- Fine for demonstration

---

## ✅ **Recommended Setup for Your FYP**

### Best Approach:
1. **Backend:** Render (Free tier)
   - Python/Flask support
   - ML models work fine
   - Free PostgreSQL included
   - Easy setup

2. **Frontend:** Vercel (Free tier)
   - Fast CDN
   - Automatic deployments
   - Free SSL
   - Professional URLs

### Estimated Time:
- Backend deployment: 30-45 minutes (first time)
- Frontend deployment: 10-15 minutes
- Total: ~1 hour

---

## 🚨 **Important Notes**

### Free Tier Limitations:

**Render:**
- Spins down after 15 min inactivity
- First request takes ~30 seconds to wake up
- 512MB RAM (enough for your models)
- 750 hours/month free

**Vercel:**
- 100GB bandwidth/month
- Unlimited deployments
- Fast CDN globally

### For FYP Presentation:

1. **Before demo:** Visit your backend URL to wake it up
2. **Wait 30 seconds** for models to load
3. Then demonstrate your app
4. Everything will work smoothly after initial wake-up

---

## 🔧 **Testing Deployed App**

After deployment:

1. **Test Backend:**
   ```bash
   curl https://your-backend.onrender.com/api/health
   ```

2. **Test Frontend:**
   - Visit your Vercel URL
   - Try searching for courses
   - Check if recommendations work

3. **Common Issues:**
   - CORS errors: Update CORS settings in `app.py`
   - Slow first load: Normal for free tier (spinning up)
   - 404 errors: Check environment variables

---

## 📞 **Need Help?**

- Render docs: https://render.com/docs
- Vercel docs: https://vercel.com/docs
- Railway docs: https://docs.railway.app

---

## 🎯 **Quick Start Checklist**

- [ ] Add `gunicorn` to `backend/requirements.txt`
- [ ] Update `app.py` for production mode
- [ ] Create Render account and deploy backend
- [ ] Get backend URL from Render
- [ ] Update frontend `.env` with backend URL
- [ ] Create Vercel account and deploy frontend
- [ ] Test the deployed application
- [ ] Wake up backend before FYP demo

---

**Good luck with your deployment! 🚀**

