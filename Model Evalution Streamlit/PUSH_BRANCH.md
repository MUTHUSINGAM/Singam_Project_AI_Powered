# How to Push v4.1.0 Branch to GitHub

## Current Status
✅ Branch `v4.1.0` created locally  
✅ Files committed  
❌ Need to authenticate to push

## Option 1: Fix SSH Authentication (Recommended for long-term)

### Step 1: Add SSH Key to GitHub
1. Copy your SSH public key:
   ```powershell
   Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | Set-Clipboard
   ```

2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
3. Paste your key and save

### Step 2: Test SSH Connection
```powershell
ssh -T git@github.com
```
You should see: "Hi YOUR_USERNAME! You've successfully authenticated..."

### Step 3: Push the Branch
```powershell
cd "C:\Users\dhara\Documents\NLP project\Singam_Project_AI_Powered\Model Evalution Streamlit"
git remote set-url muthusingam git@github.com:MUTHUSINGAM/Singam_Project_AI_Powered.git
git push -u muthusingam v4.1.0
```

## Option 2: Use HTTPS with Personal Access Token (Quick Solution)

### Step 1: Create Personal Access Token
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name it: "Streamlit Deployment"
4. Select scope: `repo` (full control of private repositories)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again!)

### Step 2: Clear Cached Credentials
```powershell
# Remove cached GitHub credentials
cmdkey /delete:LegacyGeneric:target=git:https://github.com
```

### Step 3: Push Using HTTPS
```powershell
cd "C:\Users\dhara\Documents\NLP project\Singam_Project_AI_Powered\Model Evalution Streamlit"
git remote set-url muthusingam https://github.com/MUTHUSINGAM/Singam_Project_AI_Powered.git
git push -u muthusingam v4.1.0
```

When prompted:
- **Username**: Your GitHub username (the one with collaborator access)
- **Password**: Paste your Personal Access Token (not your GitHub password)

## Option 3: Use GitHub CLI (Easiest)

```powershell
# Install GitHub CLI (if not installed)
winget install GitHub.cli

# Authenticate
gh auth login

# Push the branch
cd "C:\Users\dhara\Documents\NLP project\Singam_Project_AI_Powered\Model Evalution Streamlit"
git push -u muthusingam v4.1.0
```

## Verify Push

After successful push, check on GitHub:
- Go to: https://github.com/MUTHUSINGAM/Singam_Project_AI_Powered
- Click on "branches" dropdown
- You should see `v4.1.0` branch listed

## Deploy to Streamlit Cloud

Once the branch is pushed:

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `MUTHUSINGAM/Singam_Project_AI_Powered`
5. Branch: `v4.1.0`
6. Main file path: `app.py`
7. App directory: `Model Evalution Streamlit`
8. Click "Deploy"

Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`
