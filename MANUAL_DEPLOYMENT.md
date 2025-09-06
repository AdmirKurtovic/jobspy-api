# 🚀 Manual Cloud Deployment Guide

Since your GitHub account is flagged, here are alternative ways to deploy your JobSpy API:

## Option 1: PythonAnywhere (Recommended - Free)

### Step 1: Create Account
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Sign up for free account
3. Verify email

### Step 2: Upload Files
1. Go to "Files" tab
2. Create new directory: `jobspy-api`
3. Upload these files:
   - `api_server.py`
   - `requirements.txt`
   - `jobspy/` folder (entire directory)

### Step 3: Install Dependencies
1. Go to "Consoles" tab
2. Start new console
3. Run:
```bash
cd jobspy-api
pip3.10 install --user -r requirements.txt
pip3.10 install --user python-jobspy
```

### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Set source code directory to `/home/yourusername/jobspy-api`
6. Set working directory to `/home/yourusername/jobspy-api`
7. Set WSGI file to `api_server.py`

### Step 5: Configure WSGI
1. Click on WSGI configuration file
2. Replace content with:
```python
import sys
path = '/home/yourusername/jobspy-api'
if path not in sys.path:
    sys.path.append(path)

from api_server import app as application
```

### Step 6: Reload Web App
1. Click "Reload" button
2. Your API will be available at: `https://yourusername.pythonanywhere.com`

## Option 2: Replit (Easiest - 5 minutes)

### Step 1: Create Project
1. Go to [replit.com](https://replit.com)
2. Sign up/login
3. Click "Create Repl"
4. Choose "Python" template

### Step 2: Upload Code
1. Copy `api_server.py` content
2. Paste into `main.py`
3. Copy `requirements.txt` content
4. Create requirements.txt file

### Step 3: Install Dependencies
1. In Replit console, run:
```bash
pip install -r requirements.txt
pip install python-jobspy
```

### Step 4: Run and Deploy
1. Click "Run" button
2. Click "Deploy" button
3. Get your public URL

## Option 3: Use Different Git Host

### GitLab Deployment
1. Go to [gitlab.com](https://gitlab.com)
2. Create new repository
3. Push your code:
```bash
git remote add gitlab https://gitlab.com/yourusername/jobspy-api.git
git push gitlab main
```
4. Use GitLab with Railway/Render

### Bitbucket Deployment
1. Go to [bitbucket.org](https://bitbucket.org)
2. Create repository
3. Push code:
```bash
git remote add bitbucket https://bitbucket.org/yourusername/jobspy-api.git
git push bitbucket main
```

## Option 4: Local Network Access (Temporary)

If you just need to test with n8n Cloud temporarily:

### Step 1: Get Your Local IP
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

### Step 2: Update n8n Workflow
- Replace `http://localhost:8000` with `http://YOUR_IP:8000`
- Example: `http://192.168.1.100:8000`

### Step 3: Test
- Make sure your computer and n8n are on same network
- Test the connection

## 🎯 Recommended Approach

**For immediate testing**: Use **Replit** (5 minutes)
**For production**: Use **PythonAnywhere** (more reliable)

## 📋 Quick Replit Setup

1. Go to [replit.com](https://replit.com)
2. Create Python project
3. Copy this code to `main.py`:

```python
#!/usr/bin/env python3.10
"""
JobSpy API Server for n8n Cloud Integration
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
from datetime import datetime
import traceback
import logging

# Import JobSpy
from jobspy import scrape_jobs

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "jobspy-api"
    })

@app.route('/scrape-jobs', methods=['POST'])
def scrape_jobs_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract parameters with defaults
        site_name = data.get('site_name', ['indeed', 'linkedin'])
        search_term = data.get('search_term')
        location = data.get('location')
        results_wanted = data.get('results_wanted', 15)
        country_indeed = data.get('country_indeed', 'USA')
        hours_old = data.get('hours_old')
        is_remote = data.get('is_remote', False)
        job_type = data.get('job_type')
        easy_apply = data.get('easy_apply')
        linkedin_fetch_description = data.get('linkedin_fetch_description', False)
        description_format = data.get('description_format', 'markdown')
        proxies = data.get('proxies')
        offset = data.get('offset', 0)
        google_search_term = data.get('google_search_term')
        distance = data.get('distance', 50)
        linkedin_company_ids = data.get('linkedin_company_ids')
        enforce_annual_salary = data.get('enforce_annual_salary', False)
        verbose = data.get('verbose', 0)
        user_agent = data.get('user_agent')
        
        if not search_term:
            return jsonify({"error": "search_term is required"}), 400
        
        logger.info(f"Scraping jobs for: {search_term} in {location}")
        
        # Call JobSpy
        jobs_df = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            google_search_term=google_search_term,
            location=location,
            distance=distance,
            is_remote=is_remote,
            job_type=job_type,
            easy_apply=easy_apply,
            results_wanted=results_wanted,
            country_indeed=country_indeed,
            proxies=proxies,
            description_format=description_format,
            linkedin_fetch_description=linkedin_fetch_description,
            linkedin_company_ids=linkedin_company_ids,
            offset=offset,
            hours_old=hours_old,
            enforce_annual_salary=enforce_annual_salary,
            verbose=verbose,
            user_agent=user_agent
        )
        
        # Convert DataFrame to JSON-serializable format
        jobs_list = jobs_df.to_dict('records')
        
        # Clean up the data for JSON serialization
        for job in jobs_list:
            for key, value in job.items():
                if pd.isna(value):
                    job[key] = None
                elif isinstance(value, (pd.Timestamp, datetime)):
                    job[key] = value.isoformat()
                elif hasattr(value, 'isoformat'):
                    job[key] = value.isoformat()
        
        response = {
            "success": True,
            "total_jobs": len(jobs_list),
            "jobs": jobs_list,
            "metadata": {
                "search_term": search_term,
                "location": location,
                "sites_searched": site_name,
                "timestamp": datetime.now().isoformat(),
                "results_wanted": results_wanted,
                "actual_results": len(jobs_list)
            }
        }
        
        logger.info(f"Successfully scraped {len(jobs_list)} jobs")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error scraping jobs: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

4. Create `requirements.txt`:
```
flask==3.1.2
flask-cors==6.0.1
pandas==2.3.2
python-jobspy
```

5. Click "Run" then "Deploy"
6. Get your public URL!

## 🎯 Next Steps

1. **Choose one option** above
2. **Deploy your API**
3. **Get your public URL**
4. **Update n8n workflow** with the new URL
5. **Test the integration**

Your API will be accessible from n8n Cloud once deployed!

