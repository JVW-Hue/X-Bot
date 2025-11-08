# Deploy to Fly.io (FREE - No Credit Card for Trial)

## Step 1: Install Fly CLI

Download and install: https://fly.io/docs/hands-on/install-flyctl/

Or use PowerShell:
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

## Step 2: Sign Up

```bash
fly auth signup
```

Or login if you have account:
```bash
fly auth login
```

## Step 3: Deploy Your Bot

```bash
cd "c:\X Bot"

# Launch app
fly launch --no-deploy

# Set your API keys as secrets
fly secrets set X_BEARER_TOKEN="your_bearer_token"
fly secrets set X_API_KEY="your_api_key"
fly secrets set X_API_SECRET="your_api_secret"
fly secrets set X_ACCESS_TOKEN="your_access_token"
fly secrets set X_ACCESS_SECRET="your_access_secret"

# Deploy
fly deploy
```

## Step 4: Check Status

```bash
# View logs
fly logs

# Check status
fly status

# SSH into machine
fly ssh console
```

## ✅ Done!

Your bot runs 24/7 on Fly.io for FREE!

Free tier: 3 VMs with 256MB RAM each
