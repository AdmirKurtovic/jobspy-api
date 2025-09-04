# JobSpy n8n Cloud Deployment Guide

This guide provides three different approaches to deploy JobSpy with n8n Cloud.

## 🚀 Quick Start

### Option 1: HTTP Request Approach (Recommended)
- Deploy the Flask API server to a cloud platform
- Use HTTP Request nodes in n8n Cloud to call the API
- Most reliable and scalable approach

### Option 2: Code Node Approach
- Use Python Code nodes directly in n8n Cloud
- Requires JobSpy to be available in n8n's environment
- May have limitations in n8n Cloud

### Option 3: Hybrid Approach
- Combine both methods for maximum flexibility

---

## 📋 Prerequisites

- n8n Cloud account
- Python 3.10+ (for local development)
- Git (for deployment)
- Cloud platform account (Heroku, Railway, Render, etc.)

---

## 🔧 Option 1: HTTP Request Approach (Recommended)

### Step 1: Deploy the API Server

#### Deploy to Heroku:

1. **Install Heroku CLI** and login:
```bash
heroku login
```

2. **Create a new Heroku app**:
```bash
heroku create your-jobspy-api
```

3. **Deploy the app**:
```bash
git add .
git commit -m "Initial JobSpy API deployment"
git push heroku main
```

4. **Set environment variables** (if needed):
```bash
heroku config:set FLASK_ENV=production
```

#### Deploy to Railway:

1. **Connect your GitHub repository** to Railway
2. **Select the repository** and Railway will auto-detect the Python app
3. **Deploy** - Railway will automatically build and deploy

#### Deploy to Render:

1. **Create a new Web Service** on Render
2. **Connect your GitHub repository**
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 300 api_server:app`
4. **Deploy**

### Step 2: Import n8n Workflow

1. **Download** the `n8n_workflow_http.json` file
2. **Log into n8n Cloud**
3. **Import the workflow**:
   - Go to "Workflows"
   - Click "Import from file"
   - Upload `n8n_workflow_http.json`
4. **Update the API URL** in the HTTP Request node:
   - Replace `https://your-jobspy-api.herokuapp.com/scrape-jobs` with your actual API URL
5. **Test the workflow**

### Step 3: Configure Webhooks

Update the webhook URLs in the workflow:
- Replace `https://your-webhook-url.com/job-results` with your actual webhook URL
- Replace `https://your-webhook-url.com/job-errors` with your actual error webhook URL

---

## 🐍 Option 2: Code Node Approach

### Step 1: Import n8n Workflow

1. **Download** the `n8n_workflow_code.json` file
2. **Log into n8n Cloud**
3. **Import the workflow**:
   - Go to "Workflows"
   - Click "Import from file"
   - Upload `n8n_workflow_code.json`

### Step 2: Install JobSpy in n8n Cloud

**Note**: This may not work in n8n Cloud due to environment limitations. If it doesn't work, use Option 1 instead.

1. **Open the Python Code node**
2. **Add JobSpy installation** at the top of the code:
```python
import subprocess
import sys

# Try to install JobSpy if not available
try:
    import jobspy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-jobspy"])
    import jobspy
```

### Step 3: Test the Workflow

1. **Activate the workflow**
2. **Test with sample data**:
```json
{
  "search_term": "software engineer",
  "location": "San Francisco, CA",
  "results_wanted": 10
}
```

---

## 🔄 Option 3: Hybrid Approach

Combine both approaches for maximum flexibility:

1. **Use HTTP Request nodes** for reliable job scraping
2. **Use Code nodes** for data processing and transformation
3. **Add fallback logic** to switch between methods if one fails

---

## 📊 API Endpoints

### Main Endpoint: `/scrape-jobs`

**Method**: POST  
**Content-Type**: application/json

#### Request Body:
```json
{
  "site_name": ["indeed", "linkedin", "glassdoor"],
  "search_term": "software engineer",
  "location": "San Francisco, CA",
  "results_wanted": 20,
  "country_indeed": "USA",
  "hours_old": 72,
  "is_remote": false,
  "job_type": "fulltime",
  "easy_apply": null,
  "linkedin_fetch_description": false,
  "description_format": "markdown",
  "proxies": null,
  "offset": 0
}
```

#### Response:
```json
{
  "success": true,
  "total_jobs": 15,
  "jobs": [
    {
      "id": "indeed-12345",
      "title": "Software Engineer",
      "company_name": "Tech Corp",
      "location": {
        "city": "San Francisco",
        "state": "CA"
      },
      "job_url": "https://indeed.com/viewjob?jk=12345",
      "description": "Job description...",
      "job_type": ["fulltime"],
      "compensation": {
        "min": 80000,
        "max": 120000,
        "interval": "yearly"
      },
      "date_posted": "2024-01-15",
      "is_remote": false,
      "site": "indeed"
    }
  ],
  "metadata": {
    "search_term": "software engineer",
    "location": "San Francisco, CA",
    "sites_searched": ["indeed", "linkedin"],
    "timestamp": "2024-01-15T10:30:00Z",
    "results_wanted": 20,
    "actual_results": 15
  }
}
```

### Other Endpoints:

- `GET /health` - Health check
- `GET /sites` - Available job sites
- `GET /countries` - Available countries
- `GET /job-types` - Available job types
- `GET /description-formats` - Available description formats

---

## 🛠️ Local Development

### Run the API Server Locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python api_server.py
```

The API will be available at `http://localhost:5000`

### Test the API:

```bash
# Health check
curl http://localhost:5000/health

# Scrape jobs
curl -X POST http://localhost:5000/scrape-jobs \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "software engineer",
    "location": "San Francisco, CA",
    "results_wanted": 5
  }'
```

---

## 🔧 Configuration

### Environment Variables:

- `FLASK_ENV` - Flask environment (production/development)
- `PORT` - Port number (default: 5000)
- `PYTHONUNBUFFERED` - Python output buffering

### Optional Configuration:

- `PROXY_LIST` - Comma-separated list of proxies
- `USER_AGENT` - Custom user agent string

---

## 🚨 Troubleshooting

### Common Issues:

1. **"Invalid URL" Error**:
   - Check that the API URL is correct in n8n
   - Ensure the API server is running and accessible
   - Check for typos in the webhook URLs

2. **JobSpy Import Error** (Code Node approach):
   - JobSpy may not be available in n8n Cloud environment
   - Use the HTTP Request approach instead

3. **Timeout Errors**:
   - Increase timeout in n8n HTTP Request nodes
   - Check API server performance
   - Consider using fewer job sites or results

4. **Rate Limiting**:
   - Add delays between requests
   - Use proxies if available
   - Reduce concurrent requests

### Debug Steps:

1. **Check API health**:
   ```bash
   curl https://your-api-url.com/health
   ```

2. **Test with minimal data**:
   ```json
   {
     "search_term": "test",
     "results_wanted": 1
   }
   ```

3. **Check n8n execution logs** for detailed error messages

---

## 📈 Performance Optimization

### API Server:
- Use multiple workers (Gunicorn)
- Implement caching for repeated requests
- Add rate limiting
- Use CDN for static content

### n8n Workflow:
- Add error handling and retries
- Use parallel processing where possible
- Implement data validation
- Add monitoring and alerting

---

## 🔒 Security Considerations

- Use HTTPS for all API calls
- Implement API authentication if needed
- Validate input data
- Rate limit requests
- Monitor for abuse

---

## 📝 Support

For issues and questions:
1. Check the troubleshooting section
2. Review n8n execution logs
3. Test API endpoints directly
4. Check cloud platform logs

---

## 🎯 Next Steps

1. **Deploy** using your preferred approach
2. **Test** with sample data
3. **Configure** webhooks and notifications
4. **Monitor** performance and errors
5. **Scale** as needed

Happy job scraping! 🚀
