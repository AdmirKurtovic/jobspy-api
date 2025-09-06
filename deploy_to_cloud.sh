#!/bin/bash
# Deploy JobSpy API to Cloud Platforms

echo "🚀 JobSpy Cloud Deployment Script"
echo "================================="

# Check if git is configured
if [ -z "$(git config user.name)" ]; then
    echo "⚠️  Git not configured. Setting up..."
    git config --global user.name "Admir Kurtovic"
    git config --global user.email "hello@admirkurtovic.com"
fi

# Add and commit changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy JobSpy API for n8n Cloud integration"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Code pushed to GitHub!"
echo ""
echo "🌐 Next steps:"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select your JobSpy-1 repository"
echo "5. Railway will auto-deploy your API"
echo ""
echo "🔗 Your API will be available at: https://your-app-name.railway.app"
echo ""
echo "📋 Test your deployed API:"
echo "curl https://your-app-name.railway.app/health"
echo ""
echo "🎯 Then update n8n workflow with your new API URL!"

