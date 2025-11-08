# Deploy JWV Bot to Render.com (100% FREE - No Credit Card)

## ✅ What You Get
- FREE forever
- No credit card required
- 750 hours/month free (enough for 24/7)
- Easy deployment from GitHub

## 📋 Step-by-Step Deployment

### Step 1: Create GitHub Account (if you don't have one)

1. Go to https://github.com/signup
2. Create free account
3. Verify email

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `jwv-x-bot`
3. Make it **Private** (to hide your API keys)
4. Click **"Create repository"**

### Step 3: Upload Your Bot to GitHub

#### Option A: Using GitHub Website (Easiest)

1. In your new repository, click **"uploading an existing file"**
2. Drag and drop these files from `c:\X Bot`:
   - `main.py`
   - `scraper.py`
   - `analytics.py`
   - `config.json`
   - `requirements.txt`
   - `Procfile`
   - `render.yaml`
   - `.gitignore`
3. **DO NOT upload `.env`** (contains your API keys)
4. Click **"Commit changes"**

#### Option B: Using Git Command Line

```bash
cd "c:\X Bot"

# Initialize git
git init

# Add files
git add main.py scraper.py analytics.py config.json requirements.txt Procfile render.yaml .gitignore

# Commit
git commit -m "Initial commit"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/jwv-x-bot.git

# Push
git branch -M main
git push -u origin main
```

### Step 4: Create Render Account

1. Go to https://render.com/
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (click GitHub button)
4. Authorize Render to access your GitHub

### Step 5: Deploy Your Bot on Render

1. In Render Dashboard, click **"New +"** → **"Background Worker"**
2. Connect your repository:
   - Click **"Connect"** next to `jwv-x-bot`
3. Configure:
   - **Name**: jwv-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free
4. Click **"Advanced"** and add Environment Variables:
   - Click **"Add Environment Variable"**
   - Add each one from your `.env` file:
     - `X_BEARER_TOKEN` = (paste your token)
     - `X_API_KEY` = (paste your key)
     - `X_API_SECRET` = (paste your secret)
     - `X_ACCESS_TOKEN` = (paste your token)
     - `X_ACCESS_SECRET` = (paste your secret)
5. Click **"Create Background Worker"**

### Step 6: Wait for Deployment

- Render will build and deploy (takes 2-3 minutes)
- Watch the logs in real-time
- When you see "🚀 JWV BOT STARTING", it's working!

### Step 7: Monitor Your Bot

1. In Render Dashboard, click your **jwv-bot** service
2. Click **"Logs"** tab to see live output
3. You'll see posts being made in real-time!

## 🔄 Keep Bot Running 24/7 (Fix Sleep Issue)

Render free tier sleeps after 15 min of inactivity. To keep it awake:

### Option 1: Use UptimeRobot (Free)

1. Go to https://uptimerobot.com/
2. Sign up free (no credit card)
3. Add New Monitor:
   - Type: HTTP(s)
   - URL: Your Render service URL (get from Render dashboard)
   - Interval: 5 minutes
4. This pings your bot every 5 min to keep it awake

### Option 2: Self-Ping (Add to bot)

Add this to `main.py` at the top:
```python
import threading
import time

def keep_alive():
    while True:
        time.sleep(600)  # ping every 10 min
        print("🔄 Keep-alive ping")

threading.Thread(target=keep_alive, daemon=True).start()
```

## 📊 Check Your Bot

- **Logs**: Render Dashboard → Logs tab
- **X Account**: https://x.com/All_You_Need12
- **Analytics**: Can't run directly, but bot auto-learns every 10 posts

## 🛠️ Update Your Bot

When you want to change code:

1. Edit files locally in `c:\X Bot`
2. Upload to GitHub (drag & drop or git push)
3. Render auto-deploys new version!

## ⚠️ Important Notes

- **Free tier limits**: 750 hours/month (enough for 24/7)
- **Sleeps after 15 min**: Use UptimeRobot to prevent
- **No persistent storage**: Database resets on redeploy (we'll fix this)

## 🐛 Troubleshooting

### Bot not posting?
- Check Logs in Render dashboard
- Verify environment variables are set correctly
- Check X API credentials

### Bot stopped?
- Free tier may sleep - use UptimeRobot
- Check if you hit 750 hour limit (unlikely)

### Database keeps resetting?
- Render free tier has no persistent storage
- Bot will work but lose analytics history on restart
- Upgrade to paid ($7/month) for persistent disk

## ✅ You're Done!

Your bot is now running 24/7 on Render for FREE!

Check: https://x.com/All_You_Need12
