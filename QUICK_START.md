# 🚀 JobSpy n8n Cloud - Quick Start Guide

## ✅ What's Working Now

Your JobSpy API server is **running successfully** on `http://localhost:8000`!

### 🧪 Test Results
- ✅ JobSpy installed and working with Python 3.10
- ✅ Flask API server running on port 8000
- ✅ Successfully scraped 4 jobs from Indeed and LinkedIn
- ✅ API endpoints working correctly

## 🎯 Next Steps

### 1. **For Local n8n Development**
```bash
# Your API server is already running at:
http://localhost:8000

# Test endpoints:
curl http://localhost:8000/health
curl -X POST http://localhost:8000/scrape-jobs \
  -H "Content-Type: application/json" \
  -d '{"search_term": "software engineer", "location": "San Francisco, CA", "results_wanted": 5}'
```

### 2. **Import n8n Workflow**
1. Download `n8n_workflow_http.json`
2. Import into your n8n instance
3. The workflow is already configured to use `http://localhost:8000/scrape-jobs`

### 3. **For n8n Cloud Deployment**

#### Option A: Deploy API to Cloud (Recommended)
1. **Railway** (Free tier available):
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Deploy automatically

2. **Render** (Free tier available):
   - Go to [render.com](https://render.com)
   - Create Web Service
   - Connect repository
   - Deploy

3. **Heroku** (Requires payment verification):
   ```bash
   heroku create your-jobspy-api
   git push heroku main
   ```

#### Option B: Use ngrok for Local Testing
```bash
# Install ngrok
brew install ngrok

# Expose your local server
ngrok http 8000

# Use the ngrok URL in n8n Cloud
# Example: https://abc123.ngrok.io/scrape-jobs
```

## 📊 API Endpoints

### Health Check
```bash
GET http://localhost:8000/health
```

### Scrape Jobs
```bash
POST http://localhost:8000/scrape-jobs
Content-Type: application/json

{
  "search_term": "software engineer",
  "location": "San Francisco, CA",
  "results_wanted": 10,
  "site_name": ["indeed", "linkedin"],
  "country_indeed": "USA"
}
```

### Available Sites
- `indeed` - Indeed.com
- `linkedin` - LinkedIn Jobs
- `glassdoor` - Glassdoor
- `google` - Google Jobs
- `zip_recruiter` - ZipRecruiter
- `bayt` - Bayt
- `naukri` - Naukri
- `bdjobs` - BDJobs

## 🔧 Configuration

### Environment Variables
```bash
export FLASK_ENV=production
export PORT=8000
```

### Supported Parameters
- `search_term` (required) - Job search term
- `location` - Job location
- `results_wanted` - Number of jobs to scrape (default: 15)
- `site_name` - Array of job sites to search
- `country_indeed` - Country for Indeed searches
- `hours_old` - Filter jobs by age
- `is_remote` - Remote jobs only
- `job_type` - Job type filter
- `linkedin_fetch_description` - Get full job descriptions

## 🚨 Troubleshooting

### "Invalid URL" Error
- ✅ **FIXED**: API server is running correctly
- Check that n8n is using the correct URL: `http://localhost:8000/scrape-jobs`
- For n8n Cloud, use your deployed API URL

### Port Issues
- ✅ **FIXED**: Using port 8000 (avoiding AirPlay on 5000)
- If port 8000 is busy, change it in `api_server.py`

### Python Version
- ✅ **FIXED**: Using Python 3.10 (required for JobSpy)
- JobSpy requires Python 3.10+ due to union type syntax

## 📁 Files Created

- `api_server.py` - Main Flask API server
- `n8n_workflow_http.json` - n8n workflow (HTTP Request approach)
- `n8n_workflow_code.json` - n8n workflow (Code Node approach)
- `setup.sh` - Quick setup script
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Local development
- `DEPLOYMENT_GUIDE.md` - Complete deployment guide

## 🎉 Success!

Your JobSpy n8n integration is ready to use! The API server is working perfectly and can scrape jobs from multiple job boards. You can now:

1. **Use locally** with n8n running on your machine
2. **Deploy to cloud** for n8n Cloud integration
3. **Customize** the workflows and API as needed

Happy job scraping! 🚀
