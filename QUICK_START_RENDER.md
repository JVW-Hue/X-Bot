# 🚀 Quick Start - Deploy to Render in 5 Minutes

## Step 1: Create GitHub Account
Go to https://github.com/signup (if you don't have one)

## Step 2: Create Repository
1. Go to https://github.com/new
2. Name: `jwv-x-bot`
3. Make it **Private**
4. Click "Create repository"

## Step 3: Upload Files
1. Click "uploading an existing file"
2. Drag these files from `c:\X Bot`:
   - main.py
   - scraper.py
   - analytics.py
   - config.json
   - requirements.txt
   - Procfile
   - render.yaml
   - .gitignore
3. **DON'T upload .env** (has your API keys)
4. Click "Commit changes"

## Step 4: Deploy on Render
1. Go to https://render.com/
2. Click "Get Started for Free"
3. Sign up with GitHub
4. Click "New +" → "Background Worker"
5. Connect your `jwv-x-bot` repository
6. Configure:
   - Name: jwv-bot
   - Build: `pip install -r requirements.txt`
   - Start: `python main.py`
   - Plan: **Free**
7. Add Environment Variables (from your .env file):
   - X_BEARER_TOKEN
   - X_API_KEY
   - X_API_SECRET
   - X_ACCESS_TOKEN
   - X_ACCESS_SECRET
8. Click "Create Background Worker"

## Step 5: Watch It Run!
- Check "Logs" tab in Render
- See posts in real-time
- Check X: https://x.com/All_You_Need12

## ✅ Done!
Your bot runs 24/7 for FREE!

## 🔄 Keep It Awake (Optional)
1. Go to https://uptimerobot.com/
2. Sign up free
3. Add monitor with your Render URL
4. Interval: 5 minutes

This prevents Render from sleeping.
