# 🚀 Deploy JWV Bot to Fly.io (FREE)

## Step 1: Install Fly CLI

**Windows PowerShell (Run as Administrator):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

Or download: https://fly.io/docs/hands-on/install-flyctl/

Close and reopen PowerShell after install.

## Step 2: Sign Up & Login

```bash
fly auth signup
```

Follow the browser prompts to create account (free, no credit card needed for trial).

## Step 3: Deploy Your Bot

```bash
cd "c:\X Bot"

# Create app
fly launch --name jwv-x-bot --region iad --no-deploy

# Add your API keys (replace with your actual keys from .env file)
fly secrets set X_BEARER_TOKEN="paste_your_bearer_token_here"
fly secrets set X_API_KEY="paste_your_api_key_here"
fly secrets set X_API_SECRET="paste_your_api_secret_here"
fly secrets set X_ACCESS_TOKEN="paste_your_access_token_here"
fly secrets set X_ACCESS_SECRET="paste_your_access_secret_here"

# Deploy!
fly deploy
```

## Step 4: Monitor Your Bot

```bash
# View live logs
fly logs

# Check status
fly status

# Restart if needed
fly apps restart jwv-x-bot
```

## ✅ Done!

Your bot is now running 24/7 on Fly.io for FREE!

Check your posts: https://x.com/All_You_Need12

## Manage Your Bot

```bash
# Stop bot
fly scale count 0

# Start bot
fly scale count 1

# View all apps
fly apps list

# Delete app
fly apps destroy jwv-x-bot
```
