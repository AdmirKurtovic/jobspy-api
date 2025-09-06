#!/usr/bin/env python3.10
"""
JobSpy API Server for n8n Cloud Integration
Deploy this to Replit for instant cloud access
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
        
        # Extract parameters
        search_term = data.get('search_term')
        if not search_term:
            return jsonify({"error": "search_term is required"}), 400
        
        location = data.get('location', '')
        results_wanted = data.get('results_wanted', 15)
        site_name = data.get('site_name', ['indeed', 'linkedin'])
        country_indeed = data.get('country_indeed', 'USA')
        hours_old = data.get('hours_old', 24)
        is_remote = data.get('is_remote', False)
        job_type = data.get('job_type', 'fulltime')
        linkedin_fetch_description = data.get('linkedin_fetch_description', False)
        
        logger.info(f"Scraping jobs for: {search_term} in {location}")
        
        # Scrape jobs
        jobs_df = scrape_jobs(
            search_term=search_term,
            location=location,
            results_wanted=results_wanted,
            site_name=site_name,
            country_indeed=country_indeed,
            hours_old=hours_old,
            is_remote=is_remote,
            job_type=job_type,
            linkedin_fetch_description=linkedin_fetch_description
        )
        
        if jobs_df.empty:
            return jsonify({
                "message": "No jobs found",
                "jobs": [],
                "count": 0
            })
        
        # Convert to JSON-serializable format
        jobs_list = []
        for _, job in jobs_df.iterrows():
            job_dict = {
                "title": str(job.get('title', '')),
                "company": str(job.get('company', '')),
                "location": str(job.get('location', '')),
                "job_url": str(job.get('job_url', '')),
                "site": str(job.get('site', '')),
                "date_posted": str(job.get('date_posted', '')),
                "description": str(job.get('description', '')),
                "salary": str(job.get('salary', '')),
                "job_type": str(job.get('job_type', '')),
                "is_remote": bool(job.get('is_remote', False))
            }
            jobs_list.append(job_dict)
        
        return jsonify({
            "message": f"Successfully scraped {len(jobs_list)} jobs",
            "jobs": jobs_list,
            "count": len(jobs_list),
            "search_params": {
                "search_term": search_term,
                "location": location,
                "results_wanted": results_wanted,
                "site_name": site_name
            }
        })
        
    except Exception as e:
        logger.error(f"Error scraping jobs: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": f"Failed to scrape jobs: {str(e)}"
        }), 500

@app.route('/sites', methods=['GET'])
def get_sites():
    return jsonify({
        "sites": [
            "indeed", "linkedin", "glassdoor", "google", 
            "zip_recruiter", "bayt", "naukri", "bdjobs"
        ]
    })

@app.route('/countries', methods=['GET'])
def get_countries():
    return jsonify({
        "countries": [
            "USA", "CAN", "GBR", "AUS", "DEU", "FRA", "IND", "UAE"
        ]
    })

@app.route('/job-types', methods=['GET'])
def get_job_types():
    return jsonify({
        "job_types": [
            "fulltime", "parttime", "contract", "internship", "temporary"
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Replit uses port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=False)
