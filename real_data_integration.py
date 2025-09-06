#!/usr/bin/env python3
"""
Real Data Integration Example
Shows how to integrate with real APIs instead of mock data
"""

import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Keys (set these as environment variables)
CLEARBIT_API_KEY = os.environ.get('CLEARBIT_API_KEY')
HUNTER_API_KEY = os.environ.get('HUNTER_API_KEY')
ADZUNA_APP_ID = os.environ.get('ADZUNA_APP_ID')
ADZUNA_API_KEY = os.environ.get('ADZUNA_API_KEY')

@app.route('/real-company-research', methods=['POST'])
def real_company_research():
    """Real company research using Clearbit and Hunter.io"""
    try:
        data = request.get_json()
        company_name = data.get('company_name')
        
        if not company_name:
            return jsonify({"error": "company_name is required"}), 400
        
        # Get company data from Clearbit
        company_data = get_clearbit_company_data(company_name)
        
        # Get email data from Hunter.io
        email_data = get_hunter_email_data(company_data.get('domain', ''))
        
        return jsonify({
            "company_name": company_name,
            "company_data": company_data,
            "email_data": email_data,
            "source": "real_apis"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/real-job-search', methods=['POST'])
def real_job_search():
    """Real job search using Adzuna API"""
    try:
        data = request.get_json()
        search_term = data.get('search_term')
        location = data.get('location', 'us')
        
        if not search_term:
            return jsonify({"error": "search_term is required"}), 400
        
        # Get jobs from Adzuna
        jobs = get_adzuna_jobs(search_term, location)
        
        return jsonify({
            "search_term": search_term,
            "location": location,
            "jobs": jobs,
            "count": len(jobs),
            "source": "adzuna_api"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_clearbit_company_data(company_name):
    """Get company data from Clearbit"""
    if not CLEARBIT_API_KEY:
        return {"error": "Clearbit API key not configured"}
    
    try:
        # Search for company by name
        url = f"https://company.clearbit.com/v2/companies/find"
        headers = {"Authorization": f"Bearer {CLEARBIT_API_KEY}"}
        params = {"name": company_name}
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        return {"error": f"Clearbit API error: {str(e)}"}

def get_hunter_email_data(domain):
    """Get email data from Hunter.io"""
    if not HUNTER_API_KEY or not domain:
        return {"error": "Hunter API key or domain not configured"}
    
    try:
        url = f"https://api.hunter.io/v2/domain-search"
        params = {
            "domain": domain,
            "api_key": HUNTER_API_KEY,
            "limit": 10
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        return {"error": f"Hunter API error: {str(e)}"}

def get_adzuna_jobs(search_term, location):
    """Get jobs from Adzuna API"""
    if not ADZUNA_APP_ID or not ADZUNA_API_KEY:
        return [{"error": "Adzuna API credentials not configured"}]
    
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_API_KEY,
            "what": search_term,
            "results_per_page": 10
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get('results', [])
    except Exception as e:
        return [{"error": f"Adzuna API error: {str(e)}"}]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
