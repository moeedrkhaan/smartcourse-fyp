# 🚀 SmartCourse - Complete Deployment Guide (Urdu + English)

## 📋 **Complete Steps (Git → GitHub → Render → Vercel)**

---

## **PART 1: Git Setup aur GitHub par Upload**

### Step 1: Git Initialize karo

PowerShell mein ye commands run karo:

```powershell
# Check karo Git installed hai?
git --version
# Agar error aaye toh Git install karo: https://git-scm.com/download/win

# Apna naam aur email set karo (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Git initialize
git init

# All files add karo
git add .

# First commit
git commit -m "Initial commit - SmartCourse FYP ready for deployment"
```

✅ **Done!** Local Git setup complete.

---

### Step 2: GitHub Repository Banana

#### 2.1: GitHub par jao
1. Browser mein jao: **https://github.com**
2. Sign in karo (ya sign up karo agar account nahi hai)

#### 2.2: New Repository banao
1. Top-right corner mein **"+"** click karo
2. **"New repository"** select karo
3. **Repository settings:**
   - **Repository name:** `smartcourse-fyp`
   - **Description:** "AI-powered course recommendation system using NLP"
   - **Public** select karo (ya Private agar sirf aap dekhna chahte ho)
   - **❌ DON'T check koi bhi option** (README, .gitignore, license - kuch nahi)
4. **"Create repository"** click karo

#### 2.3: Code push karo GitHub par

GitHub page par niche commands dikhengi. **Copy mat karo**, yeh use karo:

```powershell
# GitHub repo connect karo (APNA USERNAME aur REPO NAME lagao)
git remote add origin https://github.com/YOUR-USERNAME/smartcourse-fyp.git

# Branch name set karo
git branch -M main

# Push karo
git push -u origin main
```

**Example:**
Agar aapka username `moeedkhan` hai, toh:
```powershell
git remote add origin https://github.com/moeedkhan/smartcourse-fyp.git
git branch -M main
git push -u origin main
```

📝 **Note:** GitHub password nahi maangega, **Personal Access Token** maangega:
- GitHub → Settings → Developer settings → Personal access tokens → Generate new token
- Ya GitHub Desktop use karo (easier!)

✅ **Done!** Code GitHub par upload ho gaya! 🎉

---

## **PART 2: Backend Deploy karo Render par**

### Step 3: Render Account banao aur Backend Deploy karo

#### 3.1: Render par Sign Up
1. Jao: **https://render.com**
2. **"Get Started"** click karo
3. **"Sign in with GitHub"** select karo (easiest!)
4. GitHub se authorize karo

#### 3.2: New Web Service banao
1. Dashboard mein **"New +"** button click karo
2. **"Web Service"** select karo
3. **Connect GitHub repository:**
   - Apni repository `smartcourse-fyp` search karo
   - **"Connect"** click karo

#### 3.3: Configuration Settings (IMPORTANT!)

Yeh settings exactly aise fill karo:

**Basic Settings:**
- **Name:** `smartcourse-backend` (kuch bhi naam de sakte ho)
- **Region:** `Oregon (US West)` (ya nearest)
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```

- **Start Command:** 
  ```
  gunicorn app:app
  ```

**Instance Type:**
- **Free** select karo

#### 3.4: Environment Variables add karo

"Advanced" section mein jao aur **"Add Environment Variable"** click karo:

**Add these 3 variables:**

1. **Key:** `JWT_SECRET_KEY`
   **Value:** `smartcourse-secret-2026-production-key-xyz123`
   (Ya koi bhi secure random string)

2. **Key:** `FLASK_ENV`
   **Value:** `production`

3. **Key:** `PYTHON_VERSION`
   **Value:** `3.11`

#### 3.5: Deploy karo!
1. **"Create Web Service"** button click karo
2. Wait karo 5-10 minutes pehli baar
3. Logs screen mein deployment dekhenge

✅ **Backend deployed!**

#### 3.6: Backend URL copy karo
Deploy hone ke baad top par aapko URL milega:
```
https://smartcourse-backend-xyz.onrender.com
```

**Ye URL copy kar lo!** Frontend ke liye chahiye hoga. 📋

---

## **PART 3: Frontend Deploy karo Vercel par**

### Step 4: Frontend .env update karo

Pehle local .env file update karo:

```powershell
# Editor mein .env file open karo aur update karo:
# VITE_API_BASE_URL=https://YOUR-RENDER-URL/api

# Example:
VITE_API_BASE_URL=https://smartcourse-backend-xyz.onrender.com/api
```

### Step 5: Changes commit karo

```powershell
# Updated .env commit karo (just for reference, Vercel mein manually add karenge)
git add .env.example
git commit -m "Updated API URL for production"
git push
```

### Step 6: Vercel Account aur Deploy

#### 6.1: Vercel par Sign Up
1. Jao: **https://vercel.com**
2. **"Sign Up"** click karo
3. **"Continue with GitHub"** select karo
4. GitHub se authorize karo

#### 6.2: New Project Import karo
1. Dashboard mein **"Add New..."** → **"Project"** click karo
2. **"Import Git Repository"** section mein
3. Apni repository `smartcourse-fyp` find karo
4. **"Import"** click karo

#### 6.3: Configure Project

**Project Settings:**
- **Framework Preset:** `Vite` (auto-detect ho jayega)
- **Root Directory:** `./` (default rahne do)
- **Build Command:** `npm run build` (auto-detect)
- **Output Directory:** `dist` (auto-detect)

#### 6.4: Environment Variable add karo (IMPORTANT!)

**"Environment Variables"** section mein:

**Add this variable:**
- **Name:** `VITE_API_BASE_URL`
- **Value:** `https://smartcourse-backend-xyz.onrender.com/api`
  (Apna actual Render URL use karo!)

#### 6.5: Deploy karo!
1. **"Deploy"** button click karo
2. Wait karo 2-3 minutes
3. Deployment logs dekhenge

✅ **Frontend deployed!** 🎉

#### 6.6: Frontend URL mil gaya!

Deploy hone ke baad URL milega:
```
https://smartcourse-fyp.vercel.app
```

Ya apni custom domain: `your-project-xyz.vercel.app`

---

## **PART 4: Test karo Deployed App**

### Step 7: Backend Test

1. Browser mein jao:
```
https://smartcourse-backend-xyz.onrender.com/api/health
```

2. Response aise hona chahiye:
```json
{
  "status": "healthy",
  "models_loaded": {
    "tfidf": true,
    "neural": true
  }
}
```

**⏰ Note:** Pehli request 30 seconds lag sakti hai (free tier spin up hota hai)

### Step 8: Frontend Test

1. Browser mein jao:
```
https://smartcourse-fyp.vercel.app
```

2. **Test karo:**
   - Sign up karo
   - Recommendations page jao
   - Koi query search karo: "Python machine learning"
   - Results aane chahiye! ✅

---

## 🎯 **IMPORTANT: Demo se Pehle**

### FYP Presentation ke pehle:

1. **5 minutes pehle backend URL khol lo:**
   - `https://your-backend.onrender.com/api/health`
   - Wait karo models load hone tak
   - Phir demo smooth chalega!

2. **Check kar lo:**
   - Login working hai
   - Search working hai
   - Save functionality working hai

---

## 🔧 **Agar Issues aayein:**

### Issue 1: Backend 502 Error
**Solution:** Wait karo 30 seconds, refresh karo. Render free tier spin up ho raha hai.

### Issue 2: Frontend shows "Network Error"
**Solution:** 
- Vercel environment variable check karo
- Backend URL sahi hai?
- Backend `/api` endpoint hai URL mein?

### Issue 3: CORS Error
**Solution:** `backend/app.py` mein CORS settings check karo. Already updated hai!

---

## 📞 **URLs Summary**

After deployment complete:

**Backend (Render):**
- Health Check: `https://YOUR-BACKEND.onrender.com/api/health`
- API Base: `https://YOUR-BACKEND.onrender.com/api`

**Frontend (Vercel):**
- Website: `https://YOUR-PROJECT.vercel.app`

---

## ✅ **Deployment Checklist**

- [ ] Git initialized and code committed
- [ ] GitHub repository created and code pushed
- [ ] Render account created with GitHub
- [ ] Backend deployed on Render with environment variables
- [ ] Backend URL copied
- [ ] Frontend .env updated with backend URL
- [ ] Vercel account created with GitHub
- [ ] Frontend deployed on Vercel with environment variable
- [ ] Backend health check working
- [ ] Frontend loading properly
- [ ] Search functionality tested
- [ ] Login/Signup tested

---

## 🎓 **For Your FYP Report:**

**Deployment Architecture:**
```
User Browser
    ↓
Vercel (Frontend - Static Site)
    ↓ API Calls
Render (Backend - Python/Flask)
    ↓
ML Models (TF-IDF + Neural)
    ↓
SQLite Database
```

**Technologies Used:**
- **Frontend Hosting:** Vercel (Edge Network, CDN)
- **Backend Hosting:** Render (Container-based deployment)
- **CI/CD:** GitHub integration with auto-deploy
- **Environment:** Production-ready with environment variables

---

**Good luck with your deployment! 🚀**

Agar koi step mein problem aaye, mujhe batao!

