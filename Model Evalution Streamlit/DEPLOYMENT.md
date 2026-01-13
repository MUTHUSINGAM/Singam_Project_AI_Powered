# Deployment Guide for Streamlit Cloud

## Step 1: Fix Git Authentication

You're currently getting permission errors because your Git credentials don't match the repository owners. Here's how to fix it:

### Option A: Push to Your Own Repository (Recommended)

1. **Create a new repository on GitHub** (if you don't have one):
   - Go to https://github.com/new
   - Repository name: `Singam_Project_AI_Powered` (or any name you prefer)
   - Make it **Public** (required for free Streamlit Cloud)
   - Click "Create repository"

2. **Update your Git remote**:
   ```powershell
   cd "C:\Users\dhara\Documents\NLP project\Singam_Project_AI_Powered\Model Evalution Streamlit"
   git remote remove origin
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

3. **Authenticate Git** (choose one method):

   **Method 1: Personal Access Token (Recommended)**
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` scope
   - When pushing, use: `git push -u origin v3.1.0`
   - Enter your username and use the token as password

   **Method 2: GitHub CLI**
   ```powershell
   winget install GitHub.cli
   gh auth login
   ```

   **Method 3: SSH Key**
   - Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
   - Add to GitHub: Settings → SSH and GPG keys
   - Change remote to SSH: `git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git`

4. **Push your code**:
   ```powershell
   git push -u origin v3.1.0
   # Or push main branch:
   git checkout main
   git merge v3.1.0
   git push -u origin main
   ```

### Option B: Use Existing Repository with Proper Access

If `Dharaneesh-ship/Singam_Project_AI_Powered` is your repository:
1. Make sure you're logged in as `Dharaneesh-ship` (not `ssprakash1302`)
2. Update your Git credentials:
   ```powershell
   git config --global user.name "Dharaneesh-ship"
   git config --global user.email "your-email@example.com"
   ```
3. Try pushing again with authentication

## Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: https://share.streamlit.io
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Fill in the deployment form**:
   - **Repository**: Select `YOUR_USERNAME/Singam_Project_AI_Powered`
   - **Branch**: Select `v3.1.0` or `main` (whichever you pushed)
   - **Main file path**: `app.py`
   - **App directory**: `Model Evalution Streamlit` (or leave empty if app.py is in root)
5. **Click "Deploy"**

## Step 3: Verify Deployment

- Your app will be available at: `https://YOUR-APP-NAME.streamlit.app`
- Streamlit Cloud will automatically rebuild when you push new commits
- Check the logs in Streamlit Cloud dashboard if there are any errors

## Troubleshooting

### If deployment fails:
1. Check that `requirements.txt` includes `streamlit`
2. Verify all dependencies are listed correctly
3. Check Streamlit Cloud logs for specific error messages
4. Ensure the app directory path is correct

### If microphone features don't work:
- Microphone access is limited in Streamlit Cloud due to browser security
- Consider adding file upload as an alternative input method
- For full functionality, users may need to run locally

## Quick Commands Reference

```powershell
# Navigate to project
cd "C:\Users\dhara\Documents\NLP project\Singam_Project_AI_Powered\Model Evalution Streamlit"

# Check status
git status
git remote -v

# Push to your repository
git push -u origin v3.1.0

# Or switch to main and push
git checkout main
git merge v3.1.0
git push -u origin main
```
