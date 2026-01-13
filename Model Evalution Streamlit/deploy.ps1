# Deployment Script for Streamlit Cloud
# This script helps you push your code to GitHub for Streamlit Cloud deployment

Write-Host "=== Streamlit Cloud Deployment Helper ===" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
$currentDir = Get-Location
Write-Host "Current directory: $currentDir" -ForegroundColor Yellow

# Check Git status
Write-Host "`nChecking Git status..." -ForegroundColor Cyan
git status

Write-Host "`n=== Current Git Remotes ===" -ForegroundColor Cyan
git remote -v

Write-Host "`n=== Instructions ===" -ForegroundColor Green
Write-Host "To deploy to Streamlit Cloud, you need to:" -ForegroundColor White
Write-Host "1. Push your code to YOUR OWN GitHub repository" -ForegroundColor Yellow
Write-Host "2. Make sure the repository is PUBLIC (required for free Streamlit Cloud)" -ForegroundColor Yellow
Write-Host "3. Deploy from Streamlit Cloud dashboard" -ForegroundColor Yellow
Write-Host ""

# Ask user for their GitHub username
$githubUsername = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter your repository name (or press Enter for 'Singam_Project_AI_Powered')"

if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "Singam_Project_AI_Powered"
}

$repoUrl = "https://github.com/$githubUsername/$repoName.git"

Write-Host "`nRepository URL: $repoUrl" -ForegroundColor Cyan
$confirm = Read-Host "Is this correct? (Y/N)"

if ($confirm -eq "Y" -or $confirm -eq "y") {
    Write-Host "`nSetting up remote..." -ForegroundColor Cyan
    
    # Remove existing origin if it exists
    git remote remove origin 2>$null
    
    # Add new origin
    git remote add origin $repoUrl
    
    Write-Host "Remote 'origin' set to: $repoUrl" -ForegroundColor Green
    
    Write-Host "`nCurrent branch: " -NoNewline
    git branch --show-current
    
    $branch = git branch --show-current
    Write-Host "`nReady to push! Run the following command:" -ForegroundColor Green
    Write-Host "git push -u origin $branch" -ForegroundColor Yellow
    Write-Host "`nOr if you want to push to main branch:" -ForegroundColor White
    Write-Host "git checkout -b main" -ForegroundColor Yellow
    Write-Host "git push -u origin main" -ForegroundColor Yellow
    Write-Host "`nNote: You may be prompted for GitHub credentials." -ForegroundColor Cyan
    Write-Host "Use a Personal Access Token instead of password if 2FA is enabled." -ForegroundColor Cyan
} else {
    Write-Host "Setup cancelled." -ForegroundColor Red
}

Write-Host "`n=== Next Steps ===" -ForegroundColor Green
Write-Host "1. Push your code: git push -u origin <branch-name>" -ForegroundColor White
Write-Host "2. Go to https://share.streamlit.io" -ForegroundColor White
Write-Host "3. Sign in with GitHub" -ForegroundColor White
Write-Host "4. Click 'New app' and select your repository" -ForegroundColor White
Write-Host "5. Set Main file path: app.py" -ForegroundColor White
Write-Host "6. Set App directory: Model Evalution Streamlit" -ForegroundColor White
Write-Host "7. Click 'Deploy'!" -ForegroundColor White
