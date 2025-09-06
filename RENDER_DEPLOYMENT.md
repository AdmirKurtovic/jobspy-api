# Deploy to Render

## Quick Deploy to Render

1. **Go to Render**: https://render.com
2. **Sign up with GitHub** (if you haven't already)
3. **Click "New +"** → **"Web Service"**
4. **Connect your repository**: `AdmirKurtovic/jobspy-api`
5. **Configure deployment**:
   - **Name**: `jobspy-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python minimal_app.py`
   - **Port**: `8000`
6. **Click "Create Web Service"**

## Test Your Deployed API

Once deployed, test with:
```bash
# Test root endpoint
curl https://your-app-name.onrender.com/

# Test health endpoint  
curl https://your-app-name.onrender.com/health

# Test test endpoint
curl https://your-app-name.onrender.com/test
```

## Your API URL

Render will give you a URL like: `https://jobspy-api.onrender.com`

## Next Steps

1. **Deploy to Render** (follow steps above)
2. **Get your API URL** from Render dashboard
3. **Test the endpoints** to make sure they work
4. **Update n8n workflows** with the new URL
5. **Add job scraping functionality** back to the app

## Why Render?

- ✅ **More reliable** than Railway for simple Flask apps
- ✅ **No gunicorn issues** - Uses direct Python startup
- ✅ **Free tier available** - No credit card required
- ✅ **Easy deployment** - Just connect GitHub and deploy
- ✅ **Better error handling** - Clearer error messages
