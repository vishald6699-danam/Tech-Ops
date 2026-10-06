# 🚀 Finance Tracker Deployment Guide

This project consists of two parts:
1. **Backend**: FastAPI (Python) REST API
2. **Frontend**: Modern Dark Finance Tracker (HTML/CSS/JS)

---

## 🌐 Step 1: Deploy Backend to Render (Free)

1. **Push your code to GitHub**:
   - Repository: `https://github.com/charanbalaji69/Tech-Ops.git` (or your own repository).
2. Go to [Render.com](https://render.com) and sign in.
3. Click **New +** > **Web Service**.
4. Connect your GitHub repository.
5. Fill in the details:
   - **Name**: `finance-tracker-api`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
6. Click **Create Web Service**.
7. Once deployed, copy your backend URL (e.g. `https://finance-tracker-api.onrender.com`).

---

## ⚡ Step 2: Deploy Frontend to Vercel (Free)

### Method A: Via GitHub (Recommended)
1. Go to [Vercel.com](https://vercel.com) and sign in with GitHub.
2. Click **Add New** > **Project**.
3. Import your repository (`Tech-Ops`).
4. In the Project Configuration:
   - Framework Preset: **Other**
   - Root Directory: `./` (or `frontend`)
5. Click **Deploy**.
6. Once deployed, open your live Vercel link!

### Method B: Via Vercel CLI (Instant)
```bash
npx vercel deploy --prod
```

---

## 🔗 Step 3: Connect Frontend to Backend

1. Open your live Vercel website in any browser.
2. On the Login screen, click **⚙️ Cloud Server URL** (or in the app under **Profile** > **Cloud Server Connection**).
3. Enter your Render backend URL:
   `https://finance-tracker-api.onrender.com`
4. Click **Save API URL**.
5. Everything will now connect seamlessly, save your transactions, track monthly/yearly budgets, and power your Finance AI!
